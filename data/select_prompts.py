# select_prompts.py — Selects all Python prompts from the LLMSecEval dataset
# Cikti: data/final_prompts.json

import json
import os

# Dosyanin kendi konumuna gore yollari belirleyelim (her yerden calisabilmesi icin)
base_dir = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(base_dir, "llmseceval", "Dataset", "LLMSecEval-Prompts_dataset.json")
OUTPUT_PATH = os.path.join(base_dir, "final_prompts.json")

if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"Dataset bulunamadi: {DATASET_PATH}")

with open(DATASET_PATH, encoding="utf-8") as f:
    data = json.load(f)

# Python promptlarini filtrele (Language == "Python" veya bos olanlar)
python_data = [
    item for item in data
    if "python" in item.get("Language", "").lower() or item.get("Language", "") == ""
]

print(f"Toplam Python prompt adedi: {len(python_data)}")

# Cikti formatini temizle
output = []
seen_ids = set()
for item in python_data:
    p_id = item["Prompt ID"]
    # Eger ayni ID varsa ciftleme yapmayalim
    if p_id in seen_ids:
        continue
    seen_ids.add(p_id)
    
    prompt_text = item.get("Manually-fixed NL Prompt") or item.get("LLM-generated NL Prompt", "")
    # Prompt metnini temizle
    prompt_text = prompt_text.replace("<language>", "Python")
    prompt_text = prompt_text.replace("Generate Python code for the following:", "")
    prompt_text = prompt_text.strip()
    
    output.append({
        "id": p_id,
        "cwe": p_id.split("_")[0],
        "cwe_name": item["CWE Name"],
        "prompt": prompt_text,
    })

# ID'ye gore sirala
output = sorted(output, key=lambda x: x["id"])

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Secilen {len(output)} prompt yazildi -> {OUTPUT_PATH}")
