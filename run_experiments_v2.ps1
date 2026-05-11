# run_experiments_v2.ps1 - 15 Prompt Automation Script
# Runs 3 models x 3 strategies with 15 prompts each.

$models = @("qwen25coder_7b", "llama31_8b", "gemma2_9b")
$strategies = @("zero_shot", "few_shot", "chain_of_thought")
$limit = 15
$dataset = "data/mid_phase_prompts.json"

Write-Host "🚀 CodeEnhancer: FINAL EXPERIMENT (15 Prompts)" -ForegroundColor Cyan
Write-Host "Dataset: $dataset" -ForegroundColor Gray
Write-Host "Kapsam: 3 Model x 3 Strateji x 15 Prompt = 135 Senaryo" -ForegroundColor Gray

foreach ($model in $models) {
    foreach ($strategy in $strategies) {
        Write-Host "`n>>> [DENEY BASLIYOR] Model: $model | Strateji: $strategy" -ForegroundColor Yellow
        
        # 1. Kod Üretimi
        Write-Host "1. Adim: Kod Üretiliyor (Limit: $limit)..." -ForegroundColor Gray
        python code_generator.py --model $model --strategy $strategy --limit $limit --dataset $dataset
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "X Hata: Generator basarisiz oldu." -ForegroundColor Red
            continue
        }

        # 2. Validasyon
        Write-Host "2. Adim: Validasyon Baslatiliyor..." -ForegroundColor Gray
        python code_validator.py --model $model --strategy $strategy
        
        Write-Host "V [TAMAMLANDI] $model + $strategy" -ForegroundColor Green
    }
}

Write-Host "`n=== FINAL DENEY SETI BITTI! ===" -ForegroundColor Cyan
Write-Host "Analiz icin: python analysis/generate_metrics.py" -ForegroundColor Gray
