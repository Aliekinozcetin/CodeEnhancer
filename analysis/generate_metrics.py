# analysis/generate_metrics.py
import json
import os
import sys
import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
EXPERIMENTS_DIR = BASE_DIR / "experiments"
OUTPUT_PATH = Path(__file__).parent / "comparison_report.json"
CSV_PATH = Path(__file__).parent / "metrics.csv"

# Bizim kullandigimiz 5 model
MODELS     = ["qwen25coder_7b", "mistral_7b", "deepseek_coder_6_7b", "llama31_8b", "gemma2_9b"]
STRATEGIES = ["zero_shot", "few_shot", "chain_of_thought"]

MODEL_LABELS = {
    "qwen25coder_7b":      "Qwen 2.5 Coder 7B",
    "mistral_7b":          "Mistral 7B",
    "deepseek_coder_6_7b": "DeepSeek-Coder 6.7B",
    "llama31_8b":          "Llama 3.1 8B",
    "gemma2_9b":           "Gemma 2 9B",
}

STRATEGY_LABELS = {
    "zero_shot":        "Zero-shot",
    "few_shot":         "Few-shot",
    "chain_of_thought": "Chain-of-Thought",
}

# Few-shot icin "seen" (ornek olarak promptlarda gosterilen) CWE'ler
SEEN_CWES = {"CWE-78", "CWE-89", "CWE-502", "CWE-434", "CWE-22"}

def load_validation_results(model_key: str, strategy: str) -> list | None:
    exp_dir = EXPERIMENTS_DIR / f"{model_key}_{strategy}"
    if not exp_dir.exists(): return None
    
    logs = sorted(exp_dir.glob("*_log.json"))
    if not logs: return None
    
    results = []
    for lp in logs:
        with open(lp, encoding="utf-8") as f:
            results.append(json.load(f))
    return results

def compute_metrics(file_results: list) -> dict:
    total = len(file_results)
    if total == 0: return {}

    bandit_iter0 = 0
    resolved = 0
    unresolved = 0
    total_iterations = 0
    cwe_bandit_counts = {}
    
    seen_resolved = 0
    seen_total = 0
    unseen_resolved = 0
    unseen_total = 0

    for file_res in file_results:
        revisions = file_res.get("revisions", [])
        fname = file_res.get("filename", "")
        cwe = fname.split("_")[0] if "_" in fname else "UNKNOWN"
        total_iterations += len(revisions)

        is_correct = any(rev.get("status") == "Correct" for rev in revisions)
        if is_correct: resolved += 1
        else: unresolved += 1

        if revisions:
            # Iteration 0 (Initial) Bandit check
            if revisions[0].get("bandit", 0) > 0:
                bandit_iter0 += 1
                cwe_bandit_counts[cwe] = cwe_bandit_counts.get(cwe, 0) + revisions[0].get("bandit")

        if cwe in SEEN_CWES:
            seen_total += 1
            if is_correct: seen_resolved += 1
        else:
            unseen_total += 1
            if is_correct: unseen_resolved += 1

    return {
        "total_files": total,
        "bandit_hit_rate_iter0": round(bandit_iter0 / total * 100, 1),
        "resolution_rate": round(resolved / total * 100, 1),
        "unresolved_rate": round(unresolved / total * 100, 1),
        "avg_iterations": round(total_iterations / total, 2),
        "cwe_bandit_counts": cwe_bandit_counts,
        "seen_resolution_rate": round(seen_resolved / seen_total * 100, 1) if seen_total > 0 else 0.0,
        "unseen_resolution_rate": round(unseen_resolved / unseen_total * 100, 1) if unseen_total > 0 else 0.0,
        "seen_total": seen_total,
        "unseen_total": unseen_total
    }

def print_summary_table(report: dict):
    print("\n" + "=" * 115)
    print("ÖZET: Güvenlik ve Doğruluk Analizi (Final Deneyleri)")
    print("=" * 115)
    header = f"{'Model':<22} {'Strateji':<18} {'Bandit@0':>9} {'Basari':>8} {'Hata':>12} {'Ort.Iter':>9} {'Seen CWE':>10} {'Unseen CWE':>12}"
    print(header)
    print("-" * 115)
    for key in sorted(report.keys()):
        data = report[key]
        m = data["metrics"]
        print(f"{MODEL_LABELS[data['model']]:<22} {STRATEGY_LABELS[data['strategy']]:<18} {m['bandit_hit_rate_iter0']:>8.1f}% {m['resolution_rate']:>7.1f}% {m['unresolved_rate']:>11.1f}% {m['avg_iterations']:>9.2f} {m['seen_resolution_rate']:>9.1f}% {m['unseen_resolution_rate']:>11.1f}%")
    print("=" * 115)

if __name__ == "__main__":
    report = {}
    for model in MODELS:
        for strategy in STRATEGIES:
            res = load_validation_results(model, strategy)
            if res:
                report[f"{model}_{strategy}"] = {
                    "model": model,
                    "strategy": strategy,
                    "metrics": compute_metrics(res)
                }

    if not report:
        print("Sonuç bulunamadı (experiments dizinini kontrol edin).")
        sys.exit(0)

    print_summary_table(report)
    
    # Save JSON for visualize.py
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Save CSV for generic use
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Model", "Strategy", "Total", "Success_Rate", "Avg_Attempts", "Seen_CWE_Rate", "Unseen_CWE_Rate"])
        for k, v in report.items():
            writer.writerow([
                v["model"], 
                v["strategy"], 
                v["metrics"]["total_files"], 
                f"{v['metrics']['resolution_rate']}%", 
                v["metrics"]["avg_iterations"],
                f"{v['metrics']['seen_resolution_rate']}%",
                f"{v['metrics']['unseen_resolution_rate']}%"
            ])

    print(f"\nRaporlar kaydedildi: {OUTPUT_PATH} ve {CSV_PATH}")
