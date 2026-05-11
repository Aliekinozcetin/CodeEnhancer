# Experiment runner: multi-model × multi-strategy validation pipeline
# Her experiments/<model>_<strategy>/code/ klasöründeki .py dosyalarını
# Bandit + Pylint ile analiz eder, sorun varsa aynı modeli kullanarak düzeltir.
# Çıktı: experiments/<model>_<strategy>/validation/ altına kaydedilir.

import os
import json
import re
import subprocess
import glob
import argparse
from pathlib import Path
from typing import Any, Dict, List, Tuple
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

# ------------------ Configuration ------------------
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
EXPERIMENTS_DIR = BASE_DIR / "experiments"

MODEL_IDS = {
    "llama31_8b":     "llama3.1",
    "deepseek_coder": "deepseek-coder:6.7b",
    "mistral7b":      "mistral:7b",
}

MAX_ATTEMPTS = 5

# ------------------ LLM Call ------------------
def call_ollama(model_id: str, prompt: str) -> str:
    import ollama
    response = ollama.chat(
        model=model_id,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.message.content.strip()

# ------------------ Docstring Utilities ------------------
def extract_module_docstring(code: str) -> str:
    for m in re.finditer(r'("""|\'\'\')([\s\S]*?)\1', code):
        ds = m.group(0)
        if all(k in ds for k in ("Input Prompt", "Intention", "Functionality")):
            return ds
    return '"""\nInput Prompt:\nIntention:\nFunctionality:\n"""'

def strip_module_docstring(code: str) -> str:
    for m in re.finditer(r'("""|\'\'\')([\s\S]*?)\1', code):
        ds = m.group(0)
        if all(k in ds for k in ("Input Prompt", "Intention", "Functionality")):
            return (code[:m.start()] + code[m.end():]).lstrip()
    return code.lstrip()

def ensure_module_docstring(body: str, doc: str) -> str:
    return doc.strip() + "\n\n" + body.lstrip()

def split_docstring_and_code(code: str) -> Tuple[str, str]:
    return extract_module_docstring(code).strip(), strip_module_docstring(code).lstrip()

# ------------------ Code Extraction ------------------
def extract_tag_section(text: str, tag: str) -> str | None:
    m = re.search(fr"<{tag}>([\s\S]*?)</{tag}>", text, re.IGNORECASE)
    return m.group(1).strip() if m else None

def strip_code_fence(txt: str) -> str:
    lines = txt.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()

def extract_pure_code(content: str) -> str:
    tagged = extract_tag_section(content, "Code")
    if tagged:
        return tagged
    start, end = content.find("```python"), content.rfind("```")
    if start != -1 and end != -1 and end > start:
        return content[start + 10:end].strip()
    return strip_code_fence(content)

# ------------------ SAST Runners ------------------
def run_bandit(path: Path) -> Dict[str, Any]:
    out = subprocess.run(
        ["bandit", "-f", "json", "-q", str(path)],
        capture_output=True, text=True, check=False
    ).stdout
    return json.loads(out or '{"results": []}')

def run_pylint(path: Path) -> List[Dict[str, Any]]:
    out = subprocess.run(
        ["pylint", "-f", "json", "--disable=all", "--enable=E0001", str(path)],
        capture_output=True, text=True, check=False
    ).stdout
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return []

# ------------------ Functional Check ------------------
def functional_check(full_code: str, model_id: str) -> Tuple[str, str, str]:
    doc, body = split_docstring_and_code(full_code)
    prompt = f"""
<Instruction>
Follow these rules exactly when you answer.
1. Determine whether the implementation in <Code> mostly satisfies the requirements described in <Docstring>,
   including cases where it uses a different library or algorithm that achieves the same observable behaviour
   while improving security or performance.
2. If the implementation meets the intention — output one word only: Correct
3. If any change is needed, output in precisely this structure:
Incorrect
<Code>
# (full corrected code body — do NOT include the docstring)
</Code>
<Reason>
# (brief explanation of what you fixed and why)
</Reason>
Formatting constraints:
• Start corrected code block with <Code> and end with </Code>.
• Start reason block with <Reason> and end with </Reason>.
• Do NOT add Markdown fences, line numbers, or extra text.
• Never duplicate, delete, or modify the original docstring.
</Instruction>
<Docstring>
{doc}
</Docstring>
<Code>
{body}
</Code>
""".strip()
    resp = call_ollama(model_id, prompt)
    if resp.strip() == "Correct":
        return "Correct", prompt, resp
    fixed_body = strip_module_docstring(extract_pure_code(resp))
    return fixed_body, prompt, resp

# ------------------ File Validator ------------------
def validate_file(fpath: Path, model_id: str, out_dir: Path) -> Dict:
    fname = fpath.name
    final_dir = out_dir / "final_code"
    final_dir.mkdir(parents=True, exist_ok=True)

    original = fpath.read_text(encoding="utf-8")
    latest_doc = extract_module_docstring(original)
    code_body = strip_module_docstring(original)
    revisions = []

    for att in range(1, MAX_ATTEMPTS + 1):
        att_dir = out_dir / f"attempt_{att}"
        att_dir.mkdir(exist_ok=True)
        code_full = ensure_module_docstring(code_body, latest_doc)
        tmp = att_dir / f"tmp_{fname}"
        tmp.write_text(code_full, encoding="utf-8")

        pylint_iss = [{"line": i["line"], "message": i["message"]} for i in run_pylint(tmp)]
        bandit_iss = run_bandit(tmp).get("results", [])
        sast_fixed = False

        if pylint_iss or bandit_iss:
            sast_prompt = f"""
The static-analysis tools reported problems in the implementation.
<Code>
{code_body}
</Code>
<PylintIssues>
{chr(10).join(i['message'] for i in pylint_iss) if pylint_iss else 'None'}
</PylintIssues>
<BanditIssues>
{chr(10).join(i['issue_text'] for i in bandit_iss) if bandit_iss else 'None'}
</BanditIssues>
Instructions:
• Fix every issue listed above.
• Keep all existing docstrings and comments exactly as they are.
• Reply with only the corrected implementation:
<Code>
... full fixed code body (docstring excluded) ...
</Code>
The first line must be "<Code>" and the last line must be "</Code>".
Do not output anything else.
""".strip()
            sast_resp = call_ollama(model_id, sast_prompt)
            if sast_resp.strip() != "Correct":
                code_body = strip_module_docstring(extract_pure_code(sast_resp))
            sast_fixed = True
        else:
            sast_prompt, sast_resp = "No SAST issues found.", ""

        (att_dir / f"{fname[:-3]}_attempt_{att}.py").write_text(
            ensure_module_docstring(code_body, latest_doc), encoding="utf-8"
        )
        tmp.unlink(missing_ok=True)

        if sast_fixed and (pylint_iss or bandit_iss):
            revisions.append({
                "attempt": att,
                "pylint_issues": pylint_iss,
                "bandit_issues": [{"issue_text": i["issue_text"], "severity": i["issue_severity"], "line": i["line_number"]} for i in bandit_iss],
                "sast_prompt": sast_prompt,
                "sast_response": sast_resp,
                "functional_prompt": "",
                "functional_response": "",
                "status": "SAST-Fixed",
            })
            continue

        func_res, func_prompt, func_resp = functional_check(
            ensure_module_docstring(code_body, latest_doc), model_id
        )
        if func_res == "Correct":
            status = "Correct"
        else:
            code_body = strip_module_docstring(func_res)
            status = "Incorrect"

        revisions.append({
            "attempt": att,
            "pylint_issues": pylint_iss,
            "bandit_issues": [{"issue_text": i["issue_text"], "severity": i["issue_severity"], "line": i["line_number"]} for i in bandit_iss],
            "sast_prompt": sast_prompt,
            "sast_response": sast_resp,
            "functional_prompt": func_prompt,
            "functional_response": func_resp,
            "status": status,
        })

        if status == "Correct":
            (final_dir / fname).write_text(
                ensure_module_docstring(code_body, latest_doc), encoding="utf-8"
            )
            break

    if revisions[-1]["status"] != "Correct":
        (final_dir / fname).write_text(
            ensure_module_docstring(code_body, latest_doc), encoding="utf-8"
        )

    result = {"filename": fname, "revisions": revisions}
    (out_dir / f"{fname[:-3]}_validation_results.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return result

# ------------------ Experiment Runner ------------------
def run_validation(model_key: str, strategy: str):
    exp_name = f"{model_key}_{strategy}"
    exp_dir = EXPERIMENTS_DIR / exp_name
    code_dir = exp_dir / "code"
    val_dir = exp_dir / "validation"
    val_dir.mkdir(parents=True, exist_ok=True)

    if not code_dir.exists():
        print(f"[SKIP] {exp_name} — code/ klasörü bulunamadı")
        return

    model_id = MODEL_IDS[model_key]
    py_files = sorted(code_dir.glob("*.py"))
    print(f"\n▶ {exp_name} | model={model_id} | {len(py_files)} dosya")

    all_results = []
    for fpath in tqdm(py_files, desc=exp_name):
        result = validate_file(fpath, model_id, val_dir)
        all_results.append(result)

    # Özet istatistik
    def last_status(r):
        return r["revisions"][-1]["status"] if r["revisions"] else "unknown"

    correct  = sum(1 for r in all_results if last_status(r) == "Correct")
    sast_fix = sum(1 for r in all_results if last_status(r) == "SAST-Fixed")
    incorrect = sum(1 for r in all_results if last_status(r) == "Incorrect")

    summary = {
        "experiment": exp_name,
        "model": model_id,
        "strategy": strategy,
        "total": len(all_results),
        "correct": correct,
        "sast_fixed_last": sast_fix,
        "incorrect": incorrect,
        "files": all_results,
    }
    (val_dir / "validation_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  ✓ correct={correct}  sast_fixed={sast_fix}  incorrect={incorrect}")
    return summary

# ------------------ Entrypoint ------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CodeEnhancer validation pipeline")
    parser.add_argument("--model",    choices=list(MODEL_IDS.keys()) + ["all"], default="all")
    parser.add_argument("--strategy", choices=["zero_shot", "few_shot", "chain_of_thought", "all"], default="all")
    args = parser.parse_args()

    strategies = ["zero_shot", "few_shot", "chain_of_thought"] if args.strategy == "all" else [args.strategy]
    models     = list(MODEL_IDS.keys()) if args.model == "all" else [args.model]

    all_summaries = []
    for model_key in models:
        for strategy in strategies:
            summary = run_validation(model_key, strategy)
            if summary:
                all_summaries.append(summary)

    (EXPERIMENTS_DIR / "all_validation_results.json").write_text(
        json.dumps(all_summaries, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\n=== Tüm validation tamamlandı ===")
