# Analysis: visualization of cross-experiment results
# analysis/comparison_report.json dosyasını okur,
# bar chart, heatmap ve iterasyon dağılımı grafikleri üretir.
# Çıktı: analysis/figures/ klasörüne PNG olarak kaydedilir.

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

BASE_DIR    = Path(__file__).parent.parent
REPORT_PATH = Path(__file__).parent / "comparison_report.json"
FIGURES_DIR = Path(__file__).parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

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
MODELS     = ["llama31_8b", "deepseek_coder", "mistral7b"]
STRATEGIES = ["zero_shot", "few_shot", "chain_of_thought"]
COLORS     = {"zero_shot": "#4C72B0", "few_shot": "#DD8452", "chain_of_thought": "#55A868"}

# ------------------ Data Loader ------------------
def load_report() -> dict:
    if not REPORT_PATH.exists():
        print(f"[ERR] {REPORT_PATH} bulunamadı. Önce compare_results.py çalıştır.")
        sys.exit(1)
    with open(REPORT_PATH, encoding="utf-8") as f:
        return json.load(f)

def to_dataframe(report: dict) -> pd.DataFrame:
    rows = []
    for key, data in report.items():
        m = data["metrics"]
        rows.append({
            "experiment":       key,
            "model":            data["model"],
            "model_label":      MODEL_LABELS[data["model"]],
            "strategy":         data["strategy"],
            "strategy_label":   STRATEGY_LABELS[data["strategy"]],
            "bandit_hit_rate":  m.get("bandit_hit_rate_iter0", 0),
            "resolution_rate":  m.get("resolution_rate", 0),
            "unresolved_rate":  m.get("unresolved_rate", 0),
            "avg_iterations":   m.get("avg_iterations", 0),
        })
    return pd.DataFrame(rows)

# ------------------ Figure 1: Bandit Hit Rate @ Iter 0 ------------------
def plot_bandit_hit_rate(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(MODELS))
    width = 0.25

    for i, strategy in enumerate(STRATEGIES):
        vals = []
        for model in MODELS:
            row = df[(df["model"] == model) & (df["strategy"] == strategy)]
            vals.append(row["bandit_hit_rate"].values[0] if len(row) else 0)
        bars = ax.bar(x + i * width, vals, width, label=STRATEGY_LABELS[strategy],
                      color=COLORS[strategy], alpha=0.85)
        for bar, val in zip(bars, vals):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                        f"{val:.0f}%", ha="center", va="bottom", fontsize=8)

    ax.set_xlabel("Model")
    ax.set_ylabel("Bandit Hit Rate (%)")
    ax.set_title("Figure 1 — Initial Vulnerability Rate (Bandit @ Iteration 0)")
    ax.set_xticks(x + width)
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS])
    ax.set_ylim(0, 115)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    out = FIGURES_DIR / "fig1_bandit_hit_rate.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"  → {out}")

# ------------------ Figure 2: Resolution Rate ------------------
def plot_resolution_rate(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(MODELS))
    width = 0.25

    for i, strategy in enumerate(STRATEGIES):
        vals = []
        for model in MODELS:
            row = df[(df["model"] == model) & (df["strategy"] == strategy)]
            vals.append(row["resolution_rate"].values[0] if len(row) else 0)
        bars = ax.bar(x + i * width, vals, width, label=STRATEGY_LABELS[strategy],
                      color=COLORS[strategy], alpha=0.85)
        for bar, val in zip(bars, vals):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                        f"{val:.0f}%", ha="center", va="bottom", fontsize=8)

    ax.set_xlabel("Model")
    ax.set_ylabel("Resolution Rate (%)")
    ax.set_title("Figure 2 — Vulnerability Resolution Rate (after 5 iterations)")
    ax.set_xticks(x + width)
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS])
    ax.set_ylim(0, 115)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    out = FIGURES_DIR / "fig2_resolution_rate.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"  → {out}")

# ------------------ Figure 3: Average Iterations ------------------
def plot_avg_iterations(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(MODELS))
    width = 0.25

    for i, strategy in enumerate(STRATEGIES):
        vals = []
        for model in MODELS:
            row = df[(df["model"] == model) & (df["strategy"] == strategy)]
            vals.append(row["avg_iterations"].values[0] if len(row) else 0)
        bars = ax.bar(x + i * width, vals, width, label=STRATEGY_LABELS[strategy],
                      color=COLORS[strategy], alpha=0.85)
        for bar, val in zip(bars, vals):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                        f"{val:.1f}", ha="center", va="bottom", fontsize=8)

    ax.set_xlabel("Model")
    ax.set_ylabel("Average Iterations")
    ax.set_title("Figure 3 — Average Validation Iterations per File")
    ax.set_xticks(x + width)
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS])
    ax.set_ylim(0, 6.5)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    out = FIGURES_DIR / "fig3_avg_iterations.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"  → {out}")

# ------------------ Figure 4: CWE Heatmap ------------------
def plot_cwe_heatmap(report: dict):
    # CWE × experiment matrisi oluştur
    all_cwes = set()
    for data in report.values():
        all_cwes.update(data["metrics"].get("cwe_bandit_counts", {}).keys())
    if not all_cwes:
        print("  [SKIP] CWE verisi henüz yok — heatmap atlandı")
        return

    cwes = sorted(all_cwes)
    exp_keys = [f"{m}_{s}" for m in MODELS for s in STRATEGIES if f"{m}_{s}" in report]
    exp_labels = [
        f"{MODEL_LABELS[report[k]['model']].split()[0]}\n{STRATEGY_LABELS[report[k]['strategy']]}"
        for k in exp_keys
    ]

    matrix = []
    for cwe in cwes:
        row = [report[k]["metrics"].get("cwe_bandit_counts", {}).get(cwe, 0) for k in exp_keys]
        matrix.append(row)

    matrix_np = np.array(matrix, dtype=float)

    fig, ax = plt.subplots(figsize=(max(10, len(exp_keys) * 1.2), max(5, len(cwes) * 0.6)))
    im = ax.imshow(matrix_np, cmap="YlOrRd", aspect="auto")
    plt.colorbar(im, ax=ax, label="Bandit Issue Count")

    ax.set_xticks(range(len(exp_labels)))
    ax.set_xticklabels(exp_labels, fontsize=8)
    ax.set_yticks(range(len(cwes)))
    ax.set_yticklabels(cwes, fontsize=9)
    ax.set_title("Figure 4 — CWE-level Bandit Issues Heatmap (Iteration 0)")

    for i in range(len(cwes)):
        for j in range(len(exp_keys)):
            val = int(matrix_np[i, j])
            if val > 0:
                ax.text(j, i, str(val), ha="center", va="center", fontsize=8,
                        color="black" if matrix_np[i, j] < matrix_np.max() * 0.6 else "white")

    plt.tight_layout()
    out = FIGURES_DIR / "fig4_cwe_heatmap.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"  → {out}")

# ------------------ Figure 5: Stacked Bar — Final Status ------------------
def plot_final_status(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(df))
    labels = [f"{row['model_label'].split()[0]}\n{row['strategy_label']}" for _, row in df.iterrows()]

    resolved   = df["resolution_rate"].values
    unresolved = df["unresolved_rate"].values

    ax.bar(x, resolved,   label="Resolved",   color="#55A868", alpha=0.85)
    ax.bar(x, unresolved, bottom=resolved,     label="Unresolved", color="#C44E52", alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Percentage (%)")
    ax.set_title("Figure 5 — Final Validation Status per Experiment")
    ax.set_ylim(0, 115)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    out = FIGURES_DIR / "fig5_final_status.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"  → {out}")

# ------------------ Main ------------------
if __name__ == "__main__":
    report = load_report()
    if not report:
        print("Rapor boş.")
        sys.exit(0)

    df = to_dataframe(report)
    print(f"\nGrafik üretiliyor ({len(df)} deney)...")

    plot_bandit_hit_rate(df)
    plot_resolution_rate(df)
    plot_avg_iterations(df)
    plot_cwe_heatmap(report)
    plot_final_status(df)

    print(f"\nTüm grafikler → {FIGURES_DIR}/")
