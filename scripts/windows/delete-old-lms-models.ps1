# Delete Old LM Studio Models & Prepare for New Ones
# Part of Shenron's Syndicate AI Council Deployment
# Author: MatoTezi Tanka

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  DELETE OLD MODELS & PREPARE FOR SHENRON'S SYNDICATE" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

$LMS_MODELS_DIR = "$env:USERPROFILE\.lmstudio\models"

Write-Host "[1/4] Backing up LM Studio configuration..." -ForegroundColor Yellow
$backupDir = "C:\GOKU-AI\lmstudio-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
try {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    
    # Backup conversations and settings
    if (Test-Path "$env:USERPROFILE\.lmstudio\conversations") {
        Copy-Item -Path "$env:USERPROFILE\.lmstudio\conversations" -Destination "$backupDir\conversations" -Recurse -Force
        Write-Host "  [OK] Conversations backed up" -ForegroundColor Green
    }
    
    if (Test-Path "$env:USERPROFILE\.lmstudio\settings.json") {
        Copy-Item -Path "$env:USERPROFILE\.lmstudio\settings.json" -Destination "$backupDir\settings.json" -Force
        Write-Host "  [OK] Settings backed up" -ForegroundColor Green
    }
    
    Write-Host "  [INFO] Backup location: $backupDir" -ForegroundColor Cyan
} catch {
    Write-Host "  [WARN] Backup failed: $_" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[2/4] Listing current models..." -ForegroundColor Yellow
$existingModels = Get-ChildItem "$LMS_MODELS_DIR\*\*\*.gguf" -Recurse -ErrorAction SilentlyContinue

if ($existingModels) {
    Write-Host "  Found $($existingModels.Count) models:" -ForegroundColor Cyan
    foreach ($model in $existingModels) {
        $sizeGB = [math]::Round($model.Length / 1GB, 2)
        $relativePath = $model.FullName.Replace($LMS_MODELS_DIR, "").TrimStart("\")
        Write-Host "    - $relativePath (${sizeGB} GB)" -ForegroundColor White
    }
} else {
    Write-Host "  [INFO] No models found" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "[3/4] Deleting old models..." -ForegroundColor Yellow
Write-Host "  [WARN] This will delete ALL models in: $LMS_MODELS_DIR" -ForegroundColor Yellow
Write-Host ""
$confirmation = Read-Host "  Are you sure you want to delete all models? (yes/no)"

if ($confirmation -eq "yes") {
    try {
        # List of publishers/directories to remove
        $publishers = @(
            "deepseek-ai",
            "lmstudio-community",
            "Qwen",
            "mistralai",
            "microsoft",
            "jfer1015",
            "seawolf2357",
            "bartowski"
        )
        
        $deletedCount = 0
        foreach ($publisher in $publishers) {
            $publisherPath = Join-Path $LMS_MODELS_DIR $publisher
            if (Test-Path $publisherPath) {
                Write-Host "    Deleting: $publisher..." -ForegroundColor Gray
                Remove-Item -Path $publisherPath -Recurse -Force -ErrorAction SilentlyContinue
                $deletedCount++
            }
        }
        
        Write-Host "  [OK] Deleted $deletedCount publisher directories" -ForegroundColor Green
        
        # Verify deletion
        $remainingModels = Get-ChildItem "$LMS_MODELS_DIR\*\*\*.gguf" -Recurse -ErrorAction SilentlyContinue
        if ($remainingModels.Count -eq 0) {
            Write-Host "  [OK] All old models deleted successfully" -ForegroundColor Green
        } else {
            Write-Host "  [WARN] $($remainingModels.Count) models still present" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  [FAIL] Deletion failed: $_" -ForegroundColor Red
    }
} else {
    Write-Host "  [SKIP] Deletion cancelled by user" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[4/4] Preparing for new models..." -ForegroundColor Yellow
Write-Host "  [INFO] Next steps:" -ForegroundColor Cyan
Write-Host "    1. Extract shenron-warriors-lms-hub.tar.gz" -ForegroundColor White
Write-Host "    2. Run: lms login (GitHub auth)" -ForegroundColor White
Write-Host "    3. Publish each warrior: lms push" -ForegroundColor White
Write-Host "    4. Download from your Hub:" -ForegroundColor White
Write-Host "       lms get matotezitanka/goku-ai-deepseek-coder-v2-lite-instruct" -ForegroundColor Gray
Write-Host "       lms get matotezitanka/vegeta-ai-llama-3.2-3b-instruct" -ForegroundColor Gray
Write-Host "       lms get matotezitanka/piccolo-ai-qwen2.5-coder-7b-instruct" -ForegroundColor Gray
Write-Host "       lms get matotezitanka/gohan-ai-mistral-7b-instruct-v0.3" -ForegroundColor Gray
Write-Host "       lms get matotezitanka/krillin-ai-phi-3-mini-128k-instruct" -ForegroundColor Gray
Write-Host "       lms get matotezitanka/frieza-ai-phi-3-mini-128k-instruct-v2" -ForegroundColor Gray

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "  OLD MODELS CLEANUP COMPLETE!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backup location: $backupDir" -ForegroundColor Cyan
Write-Host "Ready for Shenron's Syndicate warriors!" -ForegroundColor Green

