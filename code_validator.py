import os
import json
import re
import subprocess
import time
import argparse
from pathlib import Path
from typing import Any, Dict, List, Tuple
from tqdm import tqdm
from dotenv import load_dotenv

# Project imports
from client_factory import get_client
from judge_factory import get_judge_client

load_dotenv()

# =================== Configuration ===================
BASE_DIR = Path(__file__).parent.absolute()
MAX_ATTEMPTS = 5

# =================== Utility: Docstring & Parsing ===================
def split_docstring_and_code(code: str) -> Tuple[str, str]:
    """Splits the code into its docstring and main code body."""
    for m in re.finditer(r'("""|\'\'\')([\s\S]*?)\1', code):
        ds = m.group(0)
        if all(k in ds for k in ("Input Prompt", "Intention", "Functionality")):
            body = (code[:m.start()] + code[m.end():]).lstrip()
            return ds.strip(), body
    return '"""\nInput Prompt:\nIntention:\nFunctionality:\n"""', code.lstrip()

def ensure_module_docstring(body: str, doc: str) -> str:
    return doc.strip() + "\n\n" + body.lstrip()

def extract_pure_code(content: str) -> str:
    m = re.search(r"<Code>([\s\S]*?)</Code>", content, re.IGNORECASE)
    if m: return m.group(1).strip()
    
    start, end = content.find("```python"), content.rfind("```")
    if start != -1 and end != -1 and end > start:
        return content[start+9:end].strip()
    
    return content.strip()

# =================== SAST Runners ===================
def run_bandit(path: Path) -> Dict[str, Any]:
    out = subprocess.run(["bandit", "-f", "json", "-q", str(path)],
                         capture_output=True, text=True, check=False).stdout
    try:
        return json.loads(out or '{"results": []}')
    except:
        return {"results": []}

def run_pylint(path: Path) -> List[Dict[str, Any]]:
    out = subprocess.run(
        ["pylint", "-f", "json", "--disable=all", "--enable=E0001", str(path)],
        capture_output=True, text=True, check=False
    ).stdout
    try:
        return json.loads(out or "[]")
    except:
        return []

# =================== LLM Interaction ===================
def call_llm(client, model_id, prompt, retries=3):
    wait = 2.0
    for i in range(retries):
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
                temperature=0,
                extra_body={"num_ctx": 8192}
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if i == retries - 1: raise e
            time.sleep(wait)
            wait *= 2

def call_judge(client, model_id, prompt, retries=3):
    """GPT-4o-mini API cagrisi - JSON response."""
    wait = 2.0
    for i in range(retries):
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=256,
                temperature=0,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if i == retries - 1: raise e
            time.sleep(wait)
            wait *= 2

# =================== Validation Logic ===================
def validate_file(fpath: Path, gen_client, gen_model_id, judge_client, judge_model_id, output_dir: Path):
    fname = fpath.name
    original = fpath.read_text(encoding="utf-8")
    doc, code_body = split_docstring_and_code(original)
    revisions = []

    for att in range(1, MAX_ATTEMPTS + 1):
        att_dir = output_dir / f"attempt_{att}"
        att_dir.mkdir(parents=True, exist_ok=True)
        
        current_full = ensure_module_docstring(code_body, doc)
        tmp_file = att_dir / f"tmp_{fname}"
        tmp_file.write_text(current_full, encoding="utf-8")

        # 1. SAST Check
        pylint_iss = run_pylint(tmp_file)
        bandit_iss = run_bandit(tmp_file).get("results", [])
        
        sast_prompt, sast_resp = "", ""
        if pylint_iss or bandit_iss:
            sast_prompt = f"""
The code has issues. Fix them. Keep the logic, but make it secure/valid.
<Code>
{code_body}
</Code>
<Issues>
Pylint: {json.dumps(pylint_iss)}
Bandit: {json.dumps(bandit_iss)}
</Issues>
Instructions:
- Fix every issue. 
- Return only the code body (no docstring) inside <Code>...</Code> tags.
"""
            sast_resp = call_llm(gen_client, gen_model_id, sast_prompt)
            code_body = extract_pure_code(sast_resp)
            
            # Save fixed attempt
            (att_dir / f"{fname[:-3]}_fixed.py").write_text(ensure_module_docstring(code_body, doc), encoding="utf-8")
            revisions.append({"attempt": att, "type": "SAST_FIX", "pylint": len(pylint_iss), "bandit": len(bandit_iss)})
            tmp_file.unlink(missing_ok=True)
            continue # Re-run SAST on fixed code in next iteration

        # 2. Functional Check (LLM Judge GPT-4o-mini)
        func_prompt = f"""Compare the <Docstring> and <Code>. Does the code fulfill the intention?
Respond ONLY with a valid JSON object matching this schema:
- If correct:
  {{"verdict": "Correct"}}
- If incorrect:
  {{"verdict": "Incorrect", "reason": "brief explanation of why the code does not fulfill the docstring intention"}}

<Docstring>
{doc}
</Docstring>
<Code>
{code_body}
</Code>
"""
        func_resp = call_judge(judge_client, judge_model_id, func_prompt)
        
        try:
            verdict = json.loads(func_resp)
        except Exception as e:
            verdict = {}
            if "Correct" in func_resp:
                verdict["verdict"] = "Correct"
            else:
                verdict["verdict"] = "Incorrect"
                verdict["reason"] = f"JSON parse error: {e}. Raw response: {func_resp}"
        
        if verdict.get("verdict") == "Correct":
            revisions.append({"attempt": att, "status": "Correct"})
            tmp_file.unlink(missing_ok=True)
            break
        else:
            reason = verdict.get("reason", "Functional issue detected by judge.")
            fix_prompt = f"""A code reviewer found a functional issue in the code:
<Reason>{reason}</Reason>

<Code>
{code_body}
</Code>

Fix the issue based on the reviewer's reason. Keep the logic, but make it secure and correct.
Return ONLY the code body inside <Code>...</Code> tags. Do not include any docstring.
"""
            fix_resp = call_llm(gen_client, gen_model_id, fix_prompt)
            code_body = extract_pure_code(fix_resp)
            revisions.append({
                "attempt": att,
                "status": "Incorrect",
                "reason": reason,
                "judge_raw_response": func_resp
            })
            tmp_file.unlink(missing_ok=True)

    # Save final results for this file
    final_code_dir = output_dir / "final_code"
    final_code_dir.mkdir(exist_ok=True)
    (final_code_dir / fname).write_text(ensure_module_docstring(code_body, doc), encoding="utf-8")
    
    with open(output_dir / f"{fname[:-3]}_log.json", "w", encoding="utf-8") as f:
        json.dump({"filename": fname, "revisions": revisions}, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="CodeEnhancer - Validator (Ollama)")
    parser.add_argument("--model", required=True, help="Model key (e.g. qwen25coder_7b)")
    parser.add_argument("--strategy", required=True, help="Strategy (e.g. zero_shot)")
    args = parser.parse_args()

    exp_folder = BASE_DIR / "experiments" / f"{args.model}_{args.strategy}"
    code_dir = exp_folder / "code"
    
    if not code_dir.exists():
        print(f"[ERROR] {code_dir} not found. Run generator first.")
        return

    print(f"\n[STARTING] Validating Experiment: {args.model}_{args.strategy}")
    gen_client, gen_model_id = get_client(args.model)
    judge_client, judge_model_id = get_judge_client()
    
    python_files = list(code_dir.glob("*.py"))
    for f in tqdm(python_files, desc="Validating Files"):
        if (exp_folder / f"{f.name[:-3]}_log.json").exists():
            continue
        validate_file(f, gen_client, gen_model_id, judge_client, judge_model_id, exp_folder)

    print(f"[FINISHED] Validation complete. Results in: {exp_folder}")

if __name__ == "__main__":
    main()
