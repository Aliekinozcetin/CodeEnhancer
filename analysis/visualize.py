# analysis/visualize.py
import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Configuration
REPORT_PATH = Path(__file__).parent / "comparison_report.json"
FIGURES_DIR = Path(__file__).parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

MODEL_LABELS = {
    "qwen25coder_7b": "Qwen 2.5 Coder 7B",
    "llama31_8b":     "Llama 3.1 8B",
    "gemma2_9b":      "Gemma 2 9B",
}
STRATEGY_LABELS = {
    "zero_shot":        "Zero-shot",
    "few_shot":         "Few-shot",
    "chain_of_thought": "Chain-of-Thought",
}
MODELS     = ["qwen25coder_7b", "llama31_8b", "gemma2_9b"]
STRATEGIES = ["zero_shot", "few_shot", "chain_of_thought"]
COLORS     = {"zero_shot": "#4C72B0", "few_shot": "#DD8452", "chain_of_thought": "#55A868"}

def load_report() -> dict:
    if not REPORT_PATH.exists():
        print(f"[ERR] {REPORT_PATH} bulunamadi. Önce generate_metrics.py calistir.")
        sys.exit(1)
    with open(REPORT_PATH, encoding="utf-8") as f:
        return json.load(f)

def to_dataframe(report: dict) -> pd.DataFrame:
    rows = []
    for key, data in report.items():
        m = data["metrics"]
        rows.append({
            "model":            data["model"],
            "model_label":      MODEL_LABELS.get(data["model"], data["model"]),
            "strategy":         data["strategy"],
            "strategy_label":   STRATEGY_LABELS.get(data["strategy"], data["strategy"]),
            "bandit_hit_rate":  m.get("bandit_hit_rate_iter0", 0),
            "resolution_rate":  m.get("resolution_rate", 0),
            "unresolved_rate":  m.get("unresolved_rate", 0),
            "avg_iterations":   m.get("avg_iterations", 0),
        })
    return pd.DataFrame(rows)

def plot_bandit_hit_rate(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(MODELS))
    width = 0.25
    for i, strategy in enumerate(STRATEGIES):
        vals = [df[(df["model"]==m) & (df["strategy"]==strategy)]["bandit_hit_rate"].values[0] if not df[(df["model"]==m) & (df["strategy"]==strategy)].empty else 0 for m in MODELS]
        ax.bar(x + i*width, vals, width, label=STRATEGY_LABELS[strategy], color=COLORS[strategy])
    ax.set_title("Figure 1 - Initial Vulnerability Rate")
    ax.set_xticks(x + width)
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS])
    ax.legend(); plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig1_bandit_hit_rate.png")

def plot_resolution_rate(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(MODELS))
    width = 0.25
    for i, strategy in enumerate(STRATEGIES):
        vals = [df[(df["model"]==m) & (df["strategy"]==strategy)]["resolution_rate"].values[0] if not df[(df["model"]==m) & (df["strategy"]==strategy)].empty else 0 for m in MODELS]
        ax.bar(x + i*width, vals, width, label=STRATEGY_LABELS[strategy], color=COLORS[strategy])
    ax.set_title("Figure 2 - Resolution Success Rate")
    ax.set_xticks(x + width)
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS])
    ax.legend(); plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig2_resolution_rate.png")

def plot_avg_iterations(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(MODELS))
    width = 0.25
    for i, strategy in enumerate(STRATEGIES):
        vals = [df[(df["model"]==m) & (df["strategy"]==strategy)]["avg_iterations"].values[0] if not df[(df["model"]==m) & (df["strategy"]==strategy)].empty else 0 for m in MODELS]
        ax.bar(x + i*width, vals, width, label=STRATEGY_LABELS[strategy], color=COLORS[strategy])
    ax.set_title("Figure 3 - Average Iterations (Efficiency)")
    ax.set_ylabel("Iterations (Lower is better)")
    ax.set_xticks(x + width)
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS])
    ax.legend(); plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig3_avg_iterations.png")

def plot_cwe_heatmap(report: dict):
    all_cwes = sorted(list(set(cwe for data in report.values() for cwe in data["metrics"].get("cwe_bandit_counts", {}).keys())))
    if not all_cwes: return
    exp_keys = [f"{m}_{s}" for m in MODELS for s in STRATEGIES if f"{m}_{s}" in report]
    matrix = [[report[k]["metrics"].get("cwe_bandit_counts", {}).get(cwe, 0) for k in exp_keys] for cwe in all_cwes]
    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(exp_keys))); ax.set_xticklabels([k.replace("_", "\n") for k in exp_keys], fontsize=8)
    ax.set_yticks(range(len(all_cwes))); ax.set_yticklabels(all_cwes)
    plt.colorbar(im); plt.title("Figure 4 - CWE Vulnerability Heatmap"); plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig4_cwe_heatmap.png")

def plot_final_status(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 5))
    # Simplify for stacked bar
    df['label'] = df['model_label'] + "\n" + df['strategy_label']
    ax.bar(df['label'], df['resolution_rate'], label='Resolved', color='#55A868')
    ax.bar(df['label'], df['unresolved_rate'], bottom=df['resolution_rate'], label='Unresolved', color='#C44E52')
    plt.xticks(rotation=45, fontsize=8); plt.ylabel("Percentage (%)"); plt.title("Figure 5 - Final Status (Resolved vs Unresolved)")
    plt.legend(); plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig5_final_status.png")

if __name__ == "__main__":
    report = load_report()
    df = to_dataframe(report)
    print("Grafikler üretiliyor...")
    plot_bandit_hit_rate(df)
    plot_resolution_rate(df)
    plot_avg_iterations(df)
    plot_cwe_heatmap(report)
    plot_final_status(df)
    print(f"Bitti! Cikti: {FIGURES_DIR}")