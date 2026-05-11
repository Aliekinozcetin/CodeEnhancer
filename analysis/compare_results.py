# Analysis: cross-experiment comparison
# experiments/<model>_<strategy>/validation/validation_summary.json dosyalarını okur,
# zafiyet oranları, iterasyon sayıları ve CWE bazlı kırılımı karşılaştırır.
# Çıktı: terminalde tablo + analysis/comparison_report.json

import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
EXPERIMENTS_DIR = BASE_DIR / "experiments"
OUTPUT_PATH = Path(__file__).parent / "comparison_report.json"

MODELS     = ["llama31_8b", "deepseek_coder", "mistral7b"]
STRATEGIES = ["zero_shot", "few_shot", "chain_of_thought"]

MODEL_LABELS = {
    "llama31_8b":     "Llama 3.1 8B",
    "deepseek_coder": "DeepSeek-Coder 6.7B",
    "mistral7b":      "Mistral 7B",
}
STRATEGY_LABELS = {
    "zero_shot":        "Zero-shot",
    "few_shot":         "Few-shot",
    "chain_of_thought": "Chain-of-Thought",
}

# ------------------ Loader ------------------
def load_validation_results(model_key: str, strategy: str) -> list | None:
    """validation_summary.json veya tek tek _validation_results.json dosyalarını yükler."""
    exp_dir = EXPERIMENTS_DIR / f"{model_key}_{strategy}" / "validation"
    summary_path = exp_dir / "validation_summary.json"

    if summary_path.exists():
        with open(summary_path, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("files", [])

    # summary yoksa tek tek dosyaları topla
    files = sorted(exp_dir.glob("*_validation_results.json"))
    if not files:
        return None
    results = []
    for fp in files:
        with open(fp, encoding="utf-8") as f:
            results.append(json.load(f))
    return results

# ------------------ Metrics ------------------
def compute_metrics(file_results: list) -> dict:
    """Bir deney kombinasyonu için metrikleri hesaplar."""
    total = len(file_results)
    if total == 0:
        return {}

    bandit_iter0       = 0   # ilk iterasyonda Bandit bulgusu olan dosya sayısı
    resolved           = 0   # en sonunda Correct olan dosya sayısı
    unresolved         = 0   # 5 iterasyon sonunda hâlâ sorunlu
    total_iterations   = 0   # ortalama iterasyon hesabı için
    iter_to_resolve    = []  # kaçıncı iterasyonda düzeldi
    cwe_bandit_counts  = {}  # CWE → ilk iterasyonda bulunan Bandit sayısı
    severity_counts    = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for file_res in file_results:
        revisions = file_res.get("revisions", [])
        fname = file_res.get("filename", "")
        cwe = fname.split("_")[0] if "_" in fname else "UNKNOWN"
        total_iterations += len(revisions)

        # İlk iterasyon Bandit bulguları
        if revisions:
            first_bandit = revisions[0].get("bandit_issues", [])
            if first_bandit:
                bandit_iter0 += 1
                cwe_bandit_counts[cwe] = cwe_bandit_counts.get(cwe, 0) + len(first_bandit)
                for issue in first_bandit:
                    sev = issue.get("severity", "LOW").upper()
                    severity_counts[sev] = severity_counts.get(sev, 0) + 1

        # Son durum
        last_status = revisions[-1]["status"] if revisions else "unknown"
        if last_status == "Correct":
            resolved += 1
            # kaçıncı iterasyonda düzeldi
            for i, rev in enumerate(revisions, 1):
                if rev["status"] == "Correct":
                    iter_to_resolve.append(i)
                    break
        else:
            unresolved += 1

    return {
        "total_files":            total,
        "bandit_hit_iter0":       bandit_iter0,
        "bandit_hit_rate_iter0":  round(bandit_iter0 / total * 100, 1),
        "resolved":               resolved,
        "unresolved":             unresolved,
        "resolution_rate":        round(resolved / total * 100, 1),
        "unresolved_rate":        round(unresolved / total * 100, 1),
        "avg_iterations":         round(total_iterations / total, 2),
        "avg_iter_to_resolve":    round(sum(iter_to_resolve) / len(iter_to_resolve), 2) if iter_to_resolve else None,
        "cwe_bandit_counts":      cwe_bandit_counts,
        "severity_counts":        severity_counts,
    }

# ------------------ Report Builder ------------------
def build_report() -> dict:
    report = {}
    missing = []

    for model in MODELS:
        for strategy in STRATEGIES:
            key = f"{model}_{strategy}"
            results = load_validation_results(model, strategy)
            if results is None:
                missing.append(key)
                continue
            report[key] = {
                "model":    model,
                "strategy": strategy,
                "metrics":  compute_metrics(results),
            }

    if missing:
        print(f"[WARN] Henüz tamamlanmamış deneyler: {', '.join(missing)}")
    return report

# ------------------ Printers ------------------
def print_summary_table(report: dict):
    print("\n" + "=" * 90)
    print("ÖZET: Bandit Hit Rate @ İterasyon 0 (ilk üretimde zafiyet oranı)")
    print("=" * 90)
    header = f"{'Model':<22} {'Strateji':<18} {'Bandit@0':>9} {'Çözüm':>8} {'Çözülemeyen':>12} {'Ort.İter':>9}"
    print(header)
    print("-" * 90)
    for key, data in sorted(report.items()):
        m = data["metrics"]
        if not m:
            continue
        print(
            f"{MODEL_LABELS[data['model']]:<22} "
            f"{STRATEGY_LABELS[data['strategy']]:<18} "
            f"{m['bandit_hit_rate_iter0']:>8.1f}% "
            f"{m['resolution_rate']:>7.1f}% "
            f"{m['unresolved_rate']:>11.1f}% "
            f"{m['avg_iterations']:>9.2f}"
        )
    print("=" * 90)

def print_cwe_table(report: dict):
    # Tüm CWE'leri topla
    all_cwes = set()
    for data in report.values():
        all_cwes.update(data["metrics"].get("cwe_bandit_counts", {}).keys())
    if not all_cwes:
        return

    print("\n" + "=" * 90)
    print("CWE BAZINDA BANDIT BULGULARI (ilk iterasyon)")
    print("=" * 90)
    cwes = sorted(all_cwes)
    col_w = 12
    header = f"{'CWE':<12}" + "".join(f"{k:<{col_w}}" for k in sorted(report.keys()))
    print(header)
    print("-" * 90)
    for cwe in cwes:
        row = f"{cwe:<12}"
        for key in sorted(report.keys()):
            count = report[key]["metrics"].get("cwe_bandit_counts", {}).get(cwe, 0)
            row += f"{count:<{col_w}}"
        print(row)
    print("=" * 90)

def print_model_comparison(report: dict):
    print("\n" + "=" * 70)
    print("MODEL BAZINDA ORTALAMA (tüm stratejiler)")
    print("=" * 70)
    for model in MODELS:
        model_data = [v for v in report.values() if v["model"] == model]
        if not model_data:
            continue
        avg_hit  = sum(d["metrics"]["bandit_hit_rate_iter0"] for d in model_data) / len(model_data)
        avg_res  = sum(d["metrics"]["resolution_rate"]       for d in model_data) / len(model_data)
        avg_unr  = sum(d["metrics"]["unresolved_rate"]       for d in model_data) / len(model_data)
        print(f"{MODEL_LABELS[model]:<22} → Bandit@0={avg_hit:.1f}%  Çözüm={avg_res:.1f}%  Çözülemeyen={avg_unr:.1f}%")
    print("=" * 70)

def print_strategy_comparison(report: dict):
    print("\n" + "=" * 70)
    print("PROMPT STRATEJİSİ BAZINDA ORTALAMA (tüm modeller)")
    print("=" * 70)
    for strategy in STRATEGIES:
        strat_data = [v for v in report.values() if v["strategy"] == strategy]
        if not strat_data:
            continue
        avg_hit  = sum(d["metrics"]["bandit_hit_rate_iter0"] for d in strat_data) / len(strat_data)
        avg_res  = sum(d["metrics"]["resolution_rate"]       for d in strat_data) / len(strat_data)
        avg_unr  = sum(d["metrics"]["unresolved_rate"]       for d in strat_data) / len(strat_data)
        print(f"{STRATEGY_LABELS[strategy]:<20} → Bandit@0={avg_hit:.1f}%  Çözüm={avg_res:.1f}%  Çözülemeyen={avg_unr:.1f}%")
    print("=" * 70)

# ------------------ Main ------------------
if __name__ == "__main__":
    report = build_report()

    if not report:
        print("Henüz tamamlanmış validation sonucu bulunamadı.")
        sys.exit(0)

    print_summary_table(report)
    print_model_comparison(report)
    print_strategy_comparison(report)
    print_cwe_table(report)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nDetaylı rapor kaydedildi → {OUTPUT_PATH}")
