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
MODELS     = ["qwen25coder_7b", "mistral_7b", "deepseek_coder_6_7b", "llama31_8b", "gemma2_9b"]
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
            "model":                  data["model"],
            "model_label":            MODEL_LABELS.get(data["model"], data["model"]),
            "strategy":               data["strategy"],
            "strategy_label":         STRATEGY_LABELS.get(data["strategy"], data["strategy"]),
            "bandit_hit_rate":        m.get("bandit_hit_rate_iter0", 0),
            "resolution_rate":        m.get("resolution_rate", 0),
            "unresolved_rate":        m.get("unresolved_rate", 0),
            "avg_iterations":         m.get("avg_iterations", 0),
            "seen_resolution_rate":   m.get("seen_resolution_rate", 0),
            "unseen_resolution_rate": m.get("unseen_resolution_rate", 0),
        })
    return pd.DataFrame(rows)

def plot_bandit_hit_rate(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(MODELS))
    width = 0.25
    for i, strategy in enumerate(STRATEGIES):
        vals = [
            df[(df["model"]==m) & (df["strategy"]==strategy)]["bandit_hit_rate"].values[0] 
            if not df[(df["model"]==m) & (df["strategy"]==strategy)].empty else 0 
            for m in MODELS
        ]
        ax.bar(x + i*width, vals, width, label=STRATEGY_LABELS[strategy], color=COLORS[strategy])
    ax.set_title("Figure 1 - Initial Vulnerability Rate (Bandit Hit Rate @ Iteration 0)")
    ax.set_ylabel("Vulnerability Rate (%)")
    ax.set_xticks(x + width)
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS], fontsize=9)
    ax.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig1_bandit_hit_rate.png")
    plt.close()

def plot_resolution_rate(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(MODELS))
    width = 0.25
    for i, strategy in enumerate(STRATEGIES):
        vals = [
            df[(df["model"]==m) & (df["strategy"]==strategy)]["resolution_rate"].values[0] 
            if not df[(df["model"]==m) & (df["strategy"]==strategy)].empty else 0 
            for m in MODELS
        ]
        ax.bar(x + i*width, vals, width, label=STRATEGY_LABELS[strategy], color=COLORS[strategy])
    ax.set_title("Figure 2 - Resolution Success Rate (SAST Clean & Judge Correct)")
    ax.set_ylabel("Resolution Rate (%)")
    ax.set_xticks(x + width)
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS], fontsize=9)
    ax.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig2_resolution_rate.png")
    plt.close()

def plot_avg_iterations(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(MODELS))
    width = 0.25
    for i, strategy in enumerate(STRATEGIES):
        vals = [
            df[(df["model"]==m) & (df["strategy"]==strategy)]["avg_iterations"].values[0] 
            if not df[(df["model"]==m) & (df["strategy"]==strategy)].empty else 0 
            for m in MODELS
        ]
        ax.bar(x + i*width, vals, width, label=STRATEGY_LABELS[strategy], color=COLORS[strategy])
    ax.set_title("Figure 3 - Average Iterations (Efficiency)")
    ax.set_ylabel("Iterations (Lower is better, Max 5)")
    ax.set_xticks(x + width)
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS], fontsize=9)
    ax.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig3_avg_iterations.png")
    plt.close()

def plot_cwe_heatmap(report: dict):
    all_cwes = sorted(list(set(cwe for data in report.values() for cwe in data["metrics"].get("cwe_bandit_counts", {}).keys())))
    if not all_cwes: return
    exp_keys = [f"{m}_{s}" for m in MODELS for s in STRATEGIES if f"{m}_{s}" in report]
    matrix = [[report[k]["metrics"].get("cwe_bandit_counts", {}).get(cwe, 0) for k in exp_keys] for cwe in all_cwes]
    
    fig, ax = plt.subplots(figsize=(15, 8))
    im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(exp_keys)))
    ax.set_xticklabels([k.replace("_", "\n") for k in exp_keys], fontsize=7)
    ax.set_yticks(range(len(all_cwes)))
    ax.set_yticklabels(all_cwes)
    plt.colorbar(im)
    plt.title("Figure 4 - CWE Vulnerability Heatmap (Bandit Count @ Iteration 0)")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig4_cwe_heatmap.png")
    plt.close()

def plot_final_status(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(15, 6))
    df['label'] = df['model_label'] + "\n(" + df['strategy_label'] + ")"
    ax.bar(df['label'], df['resolution_rate'], label='Resolved', color='#55A868', width=0.6)
    ax.bar(df['label'], df['unresolved_rate'], bottom=df['resolution_rate'], label='Unresolved', color='#C44E52', width=0.6)
    plt.xticks(rotation=45, fontsize=8)
    plt.ylabel("Percentage (%)")
    plt.title("Figure 5 - Final Status (Resolved vs Unresolved)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig5_final_status.png")
    plt.close()

def plot_radar_per_model(df: pd.DataFrame):
    categories = ['Resolution Rate', 'Security Rate\n(100 - Bandit Hit)', 'Efficiency\n(Scaled Iter)', 'Seen CWE Success', 'Unseen CWE Success']
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, polar=True)
    
    plt.xticks(angles[:-1], categories, color='black', size=9)
    ax.set_rlabel_position(0)
    plt.yticks([20,40,60,80,100], ["20","40","60","80","100"], color="grey", size=7)
    plt.ylim(0,100)
    
    model_groups = df.groupby('model').mean(numeric_only=True)
    
    for idx, model in enumerate(MODELS):
        if model not in model_groups.index: continue
        row = model_groups.loc[model]
        
        resolution = row.get('resolution_rate', 0)
        security = 100 - row.get('bandit_hit_rate', 0)
        avg_iter = row.get('avg_iterations', 1)
        efficiency = max(0, min(100, (5.0 - avg_iter) / 4.0 * 100)) # 1 iter -> 100%, 5 iter -> 0%
        seen_cwe = row.get('seen_resolution_rate', 0)
        unseen_cwe = row.get('unseen_resolution_rate', 0)
        
        values = [resolution, security, efficiency, seen_cwe, unseen_cwe]
        values += values[:1]
        
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=MODEL_LABELS[model])
        ax.fill(angles, values, alpha=0.08)
        
    plt.title("Figure 6 - Multi-Dimensional Model Comparison (Radar Chart)", size=12, y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig6_radar_per_model.png")
    plt.close()

def plot_box_iterations():
    data_to_plot = []
    labels = []
    for model in MODELS:
        model_iters = []
        for strategy in STRATEGIES:
            exp_dir = REPORT_PATH.parent.parent / "experiments" / f"{model}_{strategy}"
            if not exp_dir.exists(): continue
            logs = exp_dir.glob("*_log.json")
            for lp in logs:
                try:
                    with open(lp, encoding="utf-8") as f:
                        log_data = json.load(f)
                        model_iters.append(len(log_data.get("revisions", [])))
                except:
                    pass
        if model_iters:
            data_to_plot.append(model_iters)
            labels.append(MODEL_LABELS[model])
            
    if not data_to_plot: return
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(data_to_plot, labels=labels)
    ax.set_title("Figure 7 - Iteration Distribution per Model (Spread & Medians)")
    ax.set_ylabel("Iterations (Attempts)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig7_box_iterations.png")
    plt.close()

def plot_code_vs_general(df: pd.DataFrame):
    code_models = ["qwen25coder_7b", "deepseek_coder_6_7b"]
    general_models = ["mistral_7b", "llama31_8b", "gemma2_9b"]
    
    code_df = df[df["model"].isin(code_models)]
    general_df = df[df["model"].isin(general_models)]
    
    code_res = code_df["resolution_rate"].mean() if not code_df.empty else 0
    general_res = general_df["resolution_rate"].mean() if not general_df.empty else 0
    
    code_iter = code_df["avg_iterations"].mean() if not code_df.empty else 0
    general_iter = general_df["avg_iterations"].mean() if not general_df.empty else 0
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    ax1.bar(["Code-Specialized\n(Qwen, DeepSeek)", "General-Purpose\n(Mistral, Llama, Gemma)"], 
            [code_res, general_res], color=["#4C72B0", "#C44E52"], width=0.4)
    ax1.set_ylabel("Resolution Success Rate (%)")
    ax1.set_title("Resolution Comparison")
    ax1.set_ylim(0, 100)
    for i, v in enumerate([code_res, general_res]):
        ax1.text(i, v + 2, f"{v:.1f}%", ha='center', fontweight='bold')
        
    ax2.bar(["Code-Specialized\n(Qwen, DeepSeek)", "General-Purpose\n(Mistral, Llama, Gemma)"], 
            [code_iter, general_iter], color=["#4C72B0", "#C44E52"], width=0.4)
    ax2.set_ylabel("Average Iterations")
    ax2.set_title("Efficiency Comparison (Lower is better)")
    ax2.set_ylim(0, 5)
    for i, v in enumerate([code_iter, general_iter]):
        ax2.text(i, v + 0.1, f"{v:.2f}", ha='center', fontweight='bold')
        
    plt.suptitle("Figure 8 - Code-Specialized vs General-Purpose Models", size=13)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig8_code_vs_general.png")
    plt.close()

def plot_seen_unseen_cwe(df: pd.DataFrame):
    fs_df = df[df["strategy"] == "few_shot"]
    if fs_df.empty: return
    
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(MODELS))
    width = 0.35
    
    seen_vals = [fs_df[fs_df["model"] == m]["seen_resolution_rate"].values[0] if not fs_df[fs_df["model"] == m].empty else 0 for m in MODELS]
    unseen_vals = [fs_df[fs_df["model"] == m]["unseen_resolution_rate"].values[0] if not fs_df[fs_df["model"] == m].empty else 0 for m in MODELS]
    
    ax.bar(x - width/2, seen_vals, width, label='Seen CWEs (in prompt)', color='#55A868')
    ax.bar(x + width/2, unseen_vals, width, label='Unseen CWEs (generalization)', color='#DD8452')
    
    ax.set_ylabel("Resolution Success Rate (%)")
    ax.set_title("Figure 9 - Few-Shot Generalization: Seen vs Unseen CWEs")
    ax.set_xticks(x)
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS], fontsize=9)
    ax.set_ylim(0, 100)
    ax.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig9_seen_unseen_cwe.png")
    plt.close()

def plot_judge_analysis():
    correct_counts = []
    incorrect_counts = []
    for model in MODELS:
        correct = 0
        incorrect = 0
        for strategy in STRATEGIES:
            exp_dir = REPORT_PATH.parent.parent / "experiments" / f"{model}_{strategy}"
            if not exp_dir.exists(): continue
            logs = exp_dir.glob("*_log.json")
            for lp in logs:
                try:
                    with open(lp, encoding="utf-8") as f:
                        log_data = json.load(f)
                        for rev in log_data.get("revisions", []):
                            status = rev.get("status")
                            if status == "Correct":
                                correct += 1
                            elif status == "Incorrect":
                                incorrect += 1
                except:
                    pass
        correct_counts.append(correct)
        incorrect_counts.append(incorrect)
        
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = [MODEL_LABELS[m] for m in MODELS]
    
    ax.bar(labels, correct_counts, label='Correct Verdicts', color='#55A868', width=0.4)
    ax.bar(labels, incorrect_counts, bottom=correct_counts, label='Incorrect Verdicts', color='#C44E52', width=0.4)
    
    ax.set_ylabel("Count of Judge Decisions")
    ax.set_title("Figure 10 - LLM Judge Decisions (Correct vs Incorrect Verdicts)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig10_judge_analysis.png")
    plt.close()

if __name__ == "__main__":
    report = load_report()
    df = to_dataframe(report)
    print("Grafikler çiziliyor (10 adet)...")
    plot_bandit_hit_rate(df)
    plot_resolution_rate(df)
    plot_avg_iterations(df)
    plot_cwe_heatmap(report)
    plot_final_status(df)
    plot_radar_per_model(df)
    plot_box_iterations()
    plot_code_vs_general(df)
    plot_seen_unseen_cwe(df)
    plot_judge_analysis()
    print(f"Grafikler başarıyla kaydedildi -> {FIGURES_DIR}")