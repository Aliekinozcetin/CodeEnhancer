import os
import json
import argparse
import concurrent.futures
import re
import sys
from tqdm import tqdm
from dotenv import load_dotenv

# Project imports
from client_factory import get_client
import prompts.zero_shot
import prompts.few_shot
import prompts.chain_of_thought

load_dotenv()

# ------------------ Configuration ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATASET = os.path.join(BASE_DIR, "data", "mid_phase_prompts.json")

# Strategy mapping
STRATEGIES = {
    "zero_shot": prompts.zero_shot,
    "few_shot": prompts.few_shot,
    "chain_of_thought": prompts.chain_of_thought
}

# ------------------ Regex & Helpers ------------------
_fence_pattern = re.compile(r"```(?:python)?\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)

def extract_code_from_response(response: str) -> str:
    text = response.strip()
    code_blocks = _fence_pattern.findall(text)
    if code_blocks:
        return code_blocks[-1].strip()
    inline_match = re.search(r"((?:def |class ).*)", text, re.DOTALL)
    if inline_match:
        return inline_match.group(1).strip()
    return text

def clean_python_code(code: str) -> str:
    code = re.sub(r"^\s*```(?:python)?", "", code, flags=re.IGNORECASE).strip()
    code = re.sub(r"```$", "", code).strip()
    code = "\n".join(line.rstrip() for line in code.splitlines())
    # Note: black formatting skipped for local environment stability
    return code.rstrip() + "\n"

def has_required_docstring_sections(code: str) -> bool:
    required = ["Input Prompt", "Intention", "Functionality"]
    return all(section in code for section in required)

# ------------------ Core Logic ------------------

def process_prompt(client, model_id, strategy_module, prompt, prompt_id, output_dir):
    """
    Generates code for a single prompt.
    """
    code_dir = os.path.join(output_dir, "code")
    os.makedirs(code_dir, exist_ok=True)

    code_file = os.path.join(code_dir, f"{prompt_id}.py")
    dialogue_file = os.path.join(output_dir, f"{prompt_id}_dialogue.json")

    # Skip if already generated
    if os.path.exists(code_file) and os.path.exists(dialogue_file):
        return {"prompt_id": prompt_id, "status": "skipped"}

    # Build prompt using strategy
    full_prompt = strategy_module.create_prompt(prompt)
    
    system_msg = "You are a secure code generation assistant."
    if hasattr(strategy_module, "SYSTEM_PROMPT"):
        system_msg = strategy_module.SYSTEM_PROMPT

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": full_prompt},
    ]

    cleaned_code = ""
    pass_check = False
    retry_count = 0
    max_retries = 3

    while retry_count <= max_retries:
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=messages,
                max_tokens=2048,
                temperature=0,
            )
            assistant_reply = response.choices[0].message.content.strip()
        except Exception as e:
            return {"prompt_id": prompt_id, "status": f"error: {e}"}

        raw_code = extract_code_from_response(assistant_reply)
        cleaned_code = clean_python_code(raw_code)

        if has_required_docstring_sections(cleaned_code):
            pass_check = True
            messages.append({"role": "assistant", "content": assistant_reply})
            break

        retry_count += 1
        messages.append({"role": "assistant", "content": assistant_reply})
        
        correction_prompt = (
            "Your output is missing the required triple-quoted docstring sections: "
            "Input Prompt, Intention, and Functionality. "
            "Please rewrite the ENTIRE script with these sections at the top."
        )
        messages.append({"role": "user", "content": correction_prompt})

    # Save
    with open(code_file, "w", encoding="utf-8") as f:
        f.write(cleaned_code)

    dialogue_history = [
        {"role": m["role"], "content": [{"text": m["content"], "type": "text"}]}
        for m in messages
    ]
    with open(dialogue_file, "w", encoding="utf-8") as f:
        json.dump(dialogue_history, f, indent=2, ensure_ascii=False)

    return {"prompt_id": prompt_id, "status": "success" if pass_check else "fail_docstring"}

def run_experiment(model_key, strategy_name, dataset_path, limit=None, workers=1):
    model_folder = os.path.join(BASE_DIR, "experiments", f"{model_key}_{strategy_name}")
    os.makedirs(model_folder, exist_ok=True)
    
    print(f"\n🚀 Experiment Starting: {model_key} | {strategy_name}")
    print(f"📁 Folder: {model_folder}")

    # Initialize client
    try:
        client, model_id = get_client(model_key)
    except Exception as e:
        print(f"❌ Initialization Error: {e}")
        return

    # Load dataset
    with open(dataset_path, encoding="utf-8") as f:
        data = json.load(f)
    
    if limit:
        data = data[:limit]

    strategy_module = STRATEGIES[strategy_name]
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                process_prompt, 
                client, 
                model_id, 
                strategy_module, 
                d["prompt"], 
                d["id"], 
                model_folder
            ): d["id"]
            for d in data
        }

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Generating Code"):
            results.append(future.result())

    # Save summary
    with open(os.path.join(model_folder, "results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    
    success_count = sum(1 for r in results if r["status"] == "success")
    print(f"✅ Finished! Success: {success_count}/{len(data)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CodeEnhancer - Code Generator (Ollama)")
    parser.add_argument("--model", required=True, help="Model key (e.g. qwen25coder_7b)")
    parser.add_argument("--strategy", required=True, choices=STRATEGIES.keys(), help="Prompting strategy")
    parser.add_argument("--dataset", default=DEFAULT_DATASET, help="Path to mid_phase_prompts.json")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of prompts")
    parser.add_argument("--workers", type=int, default=1, help="Parallel workers (default 1 for local)")

    args = parser.parse_args()
    
    run_experiment(
        model_key=args.model,
        strategy_name=args.strategy,
        dataset_path=args.dataset,
        limit=args.limit,
        workers=args.workers
    )
