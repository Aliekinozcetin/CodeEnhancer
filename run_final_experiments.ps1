# run_final_experiments.ps1 - CodeEnhancer Final Phase Automation Script
# Scope: 5 Models x 3 Strategies x 81 Prompts = 1,215 Scenarios
# Checkpoint & Resume supported, resilient to interruptions.

param (
    [int]$Phase = 0 # 0: All phases, 1: Code Generation only, 2: Validation only
)

$models = @("qwen25coder_7b", "mistral_7b", "deepseek_coder_6_7b", "llama31_8b", "gemma2_9b")
$strategies = @("zero_shot", "few_shot", "chain_of_thought")
$dataset = "data/final_prompts.json"

Write-Host "=== CodeEnhancer: FINAL EXPERIMENT RUNNER ===" -ForegroundColor Cyan
Write-Host "Dataset: $dataset" -ForegroundColor Gray
Write-Host "Scope: 5 Models x 3 Strategies x 81 Prompts = 1,215 Scenarios" -ForegroundColor Gray
if ($Phase -eq 1) {
    Write-Host "Mode: Phase 1 Only (Code Generation)" -ForegroundColor Yellow
} elseif ($Phase -eq 2) {
    Write-Host "Mode: Phase 2 Only (Validation)" -ForegroundColor Yellow
} else {
    Write-Host "Mode: Full Pipeline (Phase 1 + Phase 2)" -ForegroundColor Yellow
}

# ------------------ Phase 1: Code Generation ------------------
if ($Phase -eq 0 -or $Phase -eq 1) {
    Write-Host "`n=== PHASE 1: CODE GENERATION STARTING ===" -ForegroundColor Blue
    
    foreach ($model in $models) {
        foreach ($strategy in $strategies) {
            $exp_dir = "experiments/$($model)_$($strategy)"
            $gen_marker = "$exp_dir/GENERATION_COMPLETE"
            
            # Checkpoint control
            if (Test-Path -Path $gen_marker) {
                Write-Host "[SKIP] $model - $strategy is already generated." -ForegroundColor Gray
                continue
            }
            
            Write-Host "`n>>> [RUNNING] Model: $model - Strategy: $strategy" -ForegroundColor Yellow
            if (!(Test-Path -Path $exp_dir)) {
                New-Item -Path $exp_dir -ItemType Directory -Force | Out-Null
            }
            
            python code_generator.py --model $model --strategy $strategy --dataset $dataset
            
            if ($LASTEXITCODE -eq 0) {
                New-Item -Path $gen_marker -ItemType File -Force | Out-Null
                Write-Host "[OK] Finished generation for $model - $strategy" -ForegroundColor Green
            } else {
                Write-Host "[ERROR] Generation failed for $model - $strategy. Moving on..." -ForegroundColor Red
            }
        }
    }
}

# ------------------ Phase 2: Iterative Validation (SAST + Judge) ------------------
if ($Phase -eq 0 -or $Phase -eq 2) {
    Write-Host "`n=== PHASE 2: ITERATIVE VALIDATION STARTING ===" -ForegroundColor Blue
    
    foreach ($model in $models) {
        foreach ($strategy in $strategies) {
            $exp_dir = "experiments/$($model)_$($strategy)"
            $val_marker = "$exp_dir/VALIDATION_COMPLETE"
            
            # Checkpoint control
            if (Test-Path -Path $val_marker) {
                Write-Host "[SKIP] $model - $strategy validation is already done." -ForegroundColor Gray
                continue
            }
            
            # Generation must be completed before starting validation
            if (!(Test-Path -Path "$exp_dir/code")) {
                Write-Host "[WARNING] Code directory not found for $model - $strategy. Run Phase 1 first." -ForegroundColor Yellow
                continue
            }
            
            Write-Host "`n>>> [RUNNING] Validation: $model - Strategy: $strategy" -ForegroundColor Yellow
            python code_validator.py --model $model --strategy $strategy
            
            if ($LASTEXITCODE -eq 0) {
                New-Item -Path $val_marker -ItemType File -Force | Out-Null
                Write-Host "[OK] Finished validation for $model - $strategy" -ForegroundColor Green
            } else {
                Write-Host "[ERROR] Validation failed for $model - $strategy. Moving on..." -ForegroundColor Red
            }
        }
    }
}

Write-Host "`n=== PIPELINE FINISHED ===" -ForegroundColor Cyan
Write-Host "For analysis and charts, run:" -ForegroundColor Gray
Write-Host "  python analysis/generate_metrics.py" -ForegroundColor Gray
Write-Host "  python analysis/visualize.py" -ForegroundColor Gray
