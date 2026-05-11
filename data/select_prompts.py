# Experiment: Mid-phase prompt selection
# 18 CWE kategorisinden katmanlı örnekleme ile 15 prompt seçer.
# Her kategoriden 1 prompt alınır (18 > 15 olduğu için en küçük 3 kategori elenur),
# seçim kriteri: her CWE'yi temsil etmek + toplam 15'e ulaşmak.
# Çıktı: data/mid_phase_prompts.json

import json
import random

DATASET_PATH = "llmseceval/Dataset/LLMSecEval-Prompts_dataset.json"
OUTPUT_PATH = "mid_phase_prompts.json"
TARGET_COUNT = 15
SEED = 42  # tekrarlanabilirlik için sabit seed

random.seed(SEED)

with open(DATASET_PATH, encoding="utf-8") as f:
    data = json.load(f)

# Sadece Python promptlarını filtrele (Language == "Python" veya dil belirtilmemişse dahil et)
python_data = [
    item for item in data
    if "python" in item.get("Language", "").lower() or item.get("Language", "") == ""
]

# CWE bazında grupla
cwe_groups = {}
for item in python_data:
    cwe = item["Prompt ID"].split("_")[0]
    cwe_groups.setdefault(cwe, []).append(item)

print(f"CWE kategorileri: {len(cwe_groups)}, toplam Python prompt: {len(python_data)}")

# Her CWE'den 1 prompt seç (random, seed sabit)
one_per_cwe = []
for cwe, items in sorted(cwe_groups.items()):
    selected = random.choice(items)
    one_per_cwe.append(selected)

# 12 kategori var → her birinden 1 alındı (12 prompt)
# 15'e tamamlamak için en büyük 3 kategoriden 1'er tane daha seç
cwe_sizes = sorted(cwe_groups.items(), key=lambda x: len(x[1]), reverse=True)
already_selected_ids = {item["Prompt ID"] for item in one_per_cwe}
extras = []
for cwe, items in cwe_sizes:
    if len(extras) >= 3:
        break
    remaining = [i for i in items if i["Prompt ID"] not in already_selected_ids]
    if remaining:
        extras.append(random.choice(remaining))

selected_15 = sorted(one_per_cwe + extras, key=lambda x: x["Prompt ID"])

# Çıktı formatını temizle
output = []
for item in selected_15:
    prompt_text = item.get("Manually-fixed NL Prompt") or item.get("LLM-generated NL Prompt", "")
    prompt_text = prompt_text.replace("<language>", "Python").replace("Generate Python code for the following:", "").strip()
    output.append({
        "id": item["Prompt ID"],
        "cwe": item["Prompt ID"].split("_")[0],
        "cwe_name": item["CWE Name"],
        "prompt": prompt_text,
    })

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nSeçilen 15 prompt → {OUTPUT_PATH}")
print(f"{'ID':<25} {'CWE':<12} {'CWE Adı'}")
print("-" * 80)
for item in output:
    print(f"{item['id']:<25} {item['cwe']:<12} {item['cwe_name'][:45]}")
