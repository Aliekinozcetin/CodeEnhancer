# select_prompts.py — Selects all Python prompts from the LLMSecEval dataset
# Output: data/final_prompts.json

import json
import os

# Define paths relative to the script's location (so it can be run from anywhere)
base_dir = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(base_dir, "llmseceval", "Dataset", "LLMSecEval-Prompts_dataset.json")
OUTPUT_PATH = os.path.join(base_dir, "final_prompts.json")

if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

with open(DATASET_PATH, encoding="utf-8") as f:
    data = json.load(f)

# Filter Python prompts (Language == "Python" or empty)
python_data = [
    item for item in data
    if "python" in item.get("Language", "").lower() or item.get("Language", "") == ""
]

print(f"Total Python prompt count: {len(python_data)}")

# Clean up output format
output = []
seen_ids = set()
for item in python_data:
    p_id = item["Prompt ID"]
    # Avoid duplicates if the same ID already exists
    if p_id in seen_ids:
        continue
    seen_ids.add(p_id)
    
    prompt_text = item.get("Manually-fixed NL Prompt") or item.get("LLM-generated NL Prompt", "")
    # Clean up prompt text
    prompt_text = prompt_text.replace("<language>", "Python")
    prompt_text = prompt_text.replace("Generate Python code for the following:", "")
    prompt_text = prompt_text.strip()
    
    output.append({
        "id": p_id,
        "cwe": p_id.split("_")[0],
        "cwe_name": item["CWE Name"],
        "prompt": prompt_text,
    })

# Sort by ID
output = sorted(output, key=lambda x: x["id"])

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Selected {len(output)} prompts written -> {OUTPUT_PATH}")
