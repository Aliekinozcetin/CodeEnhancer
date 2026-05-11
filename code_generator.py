# Experiment runner: multi-model × multi-prompt-strategy code generation
# Desteklenen modeller: gemini-1.5-flash, gemini-2.0-flash, llama3.1 (Ollama)
# Desteklenen stratejiler: zero_shot, few_shot, chain_of_thought
# Çıktı: experiments/<model>_<strateji>/ klasörlerine izole kaydedilir

import os
import json
import re
import concurrent.futures
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

# ------------------ Configuration ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(BASE_DIR, "data", "mid_phase_prompts.json")

# Her kombinasyon: (model_key, prompt_strategy) → experiments/<model_key>_<strategy>/
EXPERIMENTS = [
    ("gemini20flash", "zero_shot"),
    ("gemini20flash", "few_shot"),
    ("gemini20flash", "chain_of_thought"),
    ("gemini25flash", "zero_shot"),
    ("gemini25flash", "few_shot"),
    ("gemini25flash", "chain_of_thought"),
    ("llama31_8b",    "zero_shot"),
    ("llama31_8b",    "few_shot"),
    ("llama31_8b",    "chain_of_thought"),
]

# Model ID'leri
MODEL_IDS = {
    "gemini20flash": "gemini-2.0-flash",
    "gemini25flash": "gemini-2.5-flash",
    "llama31_8b":    "llama3.1",
}

MAX_RETRIES = 5
MAX_WORKERS = 4  # Ollama single-threaded olduğu için düşük tutuldu
REQUIRED_SECTIONS = ["Input Prompt", "Intention", "Functionality"]

CORRECTION_PROMPT = (
    "The Python script you just provided does NOT start with the required "
    "top-level docstring.\n\n"
    "Please regenerate the ENTIRE script and:\n"
    "- Put a triple-quoted docstring ( \"\"\" ... \"\"\" ) at the VERY TOP.\n"
    "- Inside include these three headings exactly:\n"
    "  **Input Prompt**\n"
    "  **Intention**\n"
    "  **Functionality**\n"
    "Return ONLY a fenced python code block. No explanations outside the block."
)

# ------------------ Dataset ------------------
def read_dataset(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return [{"id": item["id"], "prompt": item["prompt"]} for item in data]

# ------------------ Code Cleaning ------------------
_fence_pattern = re.compile(r"```(?:python)?\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)

def extract_code(response: str) -> str:
    text = response.strip()
    blocks = _fence_pattern.findall(text)
    if blocks:
        return blocks[-1].strip()
    match = re.search(r"((?:def |class |import |from ).*)", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text

def clean_code(code: str) -> str:
    code = re.sub(r"^\s*```(?:python)?", "", code, flags=re.IGNORECASE).strip()
    code = re.sub(r"```\s*$", "", code).strip()
    code = "\n".join(line.rstrip() for line in code.splitlines())
    try:
        import black
        code = black.format_str(code, mode=black.FileMode())
    except Exception:
        pass
    return code.rstrip() + "\n"

def has_docstring(code: str) -> bool:
    return all(section in code for section in REQUIRED_SECTIONS)

# ------------------ LLM Clients ------------------
def call_gemini(model_id: str, messages: list) -> str:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    # system mesajını ayır, geri kalanı history'e dönüştür
    system_msg = next((m["content"] for m in messages if m["role"] == "system"), None)
    history = []
    for m in messages[:-1]:
        if m["role"] == "system":
            continue
        role = "model" if m["role"] == "assistant" else "user"
        history.append(types.Content(role=role, parts=[types.Part(text=m["content"])]))

    config = types.GenerateContentConfig(
        system_instruction=system_msg,
        temperature=0,
        max_output_tokens=2048,
    )
    chat = client.chats.create(model=model_id, history=history, config=config)
    response = chat.send_message(messages[-1]["content"])
    return response.text.strip()

def call_ollama(model_id: str, messages: list) -> str:
    import ollama
    ollama_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in messages
    ]
    response = ollama.chat(model=model_id, messages=ollama_messages)
    return response.message.content.strip()

def call_llm(model_key: str, messages: list) -> str:
    model_id = MODEL_IDS[model_key]
    if model_key.startswith("gemini"):
        return call_gemini(model_id, messages)
    elif model_key == "llama31_8b":
        return call_ollama(model_id, messages)
    raise ValueError(f"Bilinmeyen model: {model_key}")

# ------------------ Prompt Builder ------------------
def build_prompt(strategy: str, task: str) -> tuple[str, str]:
    """(system_message, user_message) döndürür."""
    if strategy == "zero_shot":
        from prompts.zero_shot import build_prompt as bp, SYSTEM_MESSAGE
    elif strategy == "few_shot":
        from prompts.few_shot import build_prompt as bp, SYSTEM_MESSAGE
    elif strategy == "chain_of_thought":
        from prompts.chain_of_thought import build_prompt as bp, SYSTEM_MESSAGE
    else:
        raise ValueError(f"Bilinmeyen strateji: {strategy}")
    return SYSTEM_MESSAGE, bp(task)

# ------------------ Core Runner ------------------
def process_prompt(model_key, strategy, prompt_id, prompt, output_dir):
    code_dir = os.path.join(output_dir, "code")
    os.makedirs(code_dir, exist_ok=True)

    code_file = os.path.join(code_dir, f"{prompt_id}.py")
    dialogue_file = os.path.join(output_dir, f"{prompt_id}_dialogue.json")

    if os.path.exists(code_file) and os.path.exists(dialogue_file):
        return {"prompt_id": prompt_id, "status": "skipped"}

    system_msg, user_msg = build_prompt(strategy, prompt)
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user",   "content": user_msg},
    ]

    cleaned_code = ""
    passed = False

    for attempt in range(MAX_RETRIES + 1):
        try:
            reply = call_llm(model_key, messages)
        except Exception as e:
            return {"prompt_id": prompt_id, "status": f"error: {e}"}

        cleaned_code = clean_code(extract_code(reply))
        messages.append({"role": "assistant", "content": reply})

        if has_docstring(cleaned_code):
            passed = True
            break

        if attempt < MAX_RETRIES:
            messages.append({"role": "user", "content": CORRECTION_PROMPT})

    status = "success" if passed else "fail_docstring"

    with open(code_file, "w", encoding="utf-8") as f:
        f.write(cleaned_code)

    dialogue = [
        {"role": m["role"], "content": [{"text": m["content"], "type": "text"}]}
        for m in messages
    ]
    with open(dialogue_file, "w", encoding="utf-8") as f:
        json.dump(dialogue, f, indent=2, ensure_ascii=False)

    return {"prompt_id": prompt_id, "status": status}

def run_experiment(model_key, strategy, dataset):
    exp_name = f"{model_key}_{strategy}"
    output_dir = os.path.join(BASE_DIR, "experiments", exp_name)
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n▶ {exp_name} ({len(dataset)} prompt)")
    results = []

    # Ollama paralel çağrıya uygun değil → sequential
    workers = 1 if model_key == "llama31_8b" else MAX_WORKERS

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(process_prompt, model_key, strategy, d["id"], d["prompt"], output_dir): d["id"]
            for d in dataset
        }
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc=exp_name):
            results.append(future.result())

    success = sum(1 for r in results if r["status"] == "success")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    failed  = sum(1 for r in results if r["status"] not in ("success", "skipped"))

    summary = {
        "experiment": exp_name,
        "model": MODEL_IDS[model_key],
        "strategy": strategy,
        "total": len(results),
        "success": success,
        "skipped": skipped,
        "failed": failed,
        "results": results,
    }
    with open(os.path.join(output_dir, "results.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"  ✓ success={success}  skipped={skipped}  failed={failed}")
    return summary

# ------------------ Entrypoint ------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CodeEnhancer multi-model experiment runner")
    parser.add_argument("--model",    choices=list(MODEL_IDS.keys()) + ["all"], default="all")
    parser.add_argument("--strategy", choices=["zero_shot", "few_shot", "chain_of_thought", "all"], default="all")
    parser.add_argument("--dataset",  default=DATASET_PATH)
    args = parser.parse_args()

    dataset = read_dataset(args.dataset)

    experiments = [
        (m, s) for m, s in EXPERIMENTS
        if (args.model == "all" or m == args.model)
        and (args.strategy == "all" or s == args.strategy)
    ]

    print(f"Çalıştırılacak deney sayısı: {len(experiments)}")
    print(f"Prompt sayısı: {len(dataset)}")

    all_summaries = []
    for model_key, strategy in experiments:
        summary = run_experiment(model_key, strategy, dataset)
        all_summaries.append(summary)

    with open(os.path.join(BASE_DIR, "experiments", "all_results.json"), "w", encoding="utf-8") as f:
        json.dump(all_summaries, f, indent=2, ensure_ascii=False)

    print("\n=== Tüm deneyler tamamlandı ===")
