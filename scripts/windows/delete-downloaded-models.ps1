# ================================================================
#   DELETE DOWNLOADED MODELS - CLEAN SLATE
# ================================================================

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  DELETING DOWNLOADED MODELS FROM VM100" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

$downloadDir = "C:\AI-Models-Q8_0"
$lmsModelsDir = "$env:USERPROFILE\.lmstudio\models"

Write-Host "[1/3] Backing up LM Studio conversations..." -ForegroundColor Green
$backupDir = "C:\GOKU-AI\lmstudio-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
}

$conversationsDir = "$env:USERPROFILE\.lmstudio\conversations"
if (Test-Path $conversationsDir) {
    Copy-Item -Path $conversationsDir -Destination "$backupDir\conversations" -Recurse -Force
    Write-Host "  [OK] Conversations backed up to: $backupDir" -ForegroundColor Green
} else {
    Write-Host "  [INFO] No conversations to backup" -ForegroundColor Gray
}

Write-Host ""
Write-Host "[2/3] Deleting downloaded models..." -ForegroundColor Green

# Delete download directory
if (Test-Path $downloadDir) {
    Write-Host "  Deleting: $downloadDir" -ForegroundColor Yellow
    Remove-Item -Path $downloadDir -Recurse -Force
    Write-Host "  [OK] Deleted: C:\AI-Models-Q8_0" -ForegroundColor Green
} else {
    Write-Host "  [INFO] C:\AI-Models-Q8_0 already deleted" -ForegroundColor Gray
}

# Delete models from LM Studio directory
if (Test-Path $lmsModelsDir) {
    Write-Host "  Deleting models from LM Studio directory..." -ForegroundColor Yellow
    
    # List what will be deleted
    $models = Get-ChildItem -Path $lmsModelsDir -Recurse -Filter "*.gguf" -ErrorAction SilentlyContinue
    if ($models) {
        Write-Host "  Found $($models.Count) model files:" -ForegroundColor Cyan
        foreach ($model in $models) {
            $sizeGB = [math]::Round($model.Length / 1GB, 2)
            Write-Host "    - $($model.Name) ($sizeGB GB)" -ForegroundColor Gray
        }
        Write-Host ""
        
        $confirm = Read-Host "  Delete all models from LM Studio? (Y/N)"
        if ($confirm -eq "Y") {
            # Delete all publisher directories
            $publishers = Get-ChildItem -Path $lmsModelsDir -Directory -ErrorAction SilentlyContinue
            foreach ($publisher in $publishers) {
                Write-Host "    Deleting: $($publisher.Name)..." -ForegroundColor Yellow
                Remove-Item -Path $publisher.FullName -Recurse -Force
            }
            Write-Host "  [OK] All models deleted from LM Studio" -ForegroundColor Green
        } else {
            Write-Host "  [SKIP] Keeping LM Studio models" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  [INFO] No models found in LM Studio directory" -ForegroundColor Gray
    }
} else {
    Write-Host "  [INFO] LM Studio models directory doesn't exist" -ForegroundColor Gray
}

Write-Host ""
Write-Host "[3/3] Cleaning up..." -ForegroundColor Green

# Delete extracted warrior directories from earlier
$warriorDirs = @(
    "C:\GOKU-AI\GOKU-deepseek-coder-v2-lite-instruct",
    "C:\GOKU-AI\VEGETA-llama-3.2-3b-instruct",
    "C:\GOKU-AI\PICCOLO-qwen2.5-coder-7b-instruct",
    "C:\GOKU-AI\GOHAN-mistral-7b-instruct-v0.3",
    "C:\GOKU-AI\KRILLIN-phi-3-mini-128k-instruct",
    "C:\GOKU-AI\FRIEZA-phi-3-mini-128k-instruct-v2"
)

foreach ($dir in $warriorDirs) {
    if (Test-Path $dir) {
        Write-Host "  Deleting: $(Split-Path $dir -Leaf)" -ForegroundColor Yellow
        Remove-Item -Path $dir -Recurse -Force
    }
}

# Delete old tarballs
$tarballs = @(
    "C:\GOKU-AI\shenrons-syndicate-warriors-v2.tar.gz",
    "C:\GOKU-AI\shenrons-syndicate-warriors-v3.tar.gz"
)

foreach ($tarball in $tarballs) {
    if (Test-Path $tarball) {
        Write-Host "  Deleting: $(Split-Path $tarball -Leaf)" -ForegroundColor Yellow
        Remove-Item -Path $tarball -Force
    }
}

Write-Host "  [OK] Cleanup complete" -ForegroundColor Green

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  CLEANUP COMPLETE - READY FOR FRESH START!" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  ✅ Downloaded models deleted" -ForegroundColor Green
Write-Host "  ✅ LM Studio models deleted (if confirmed)" -ForegroundColor Green
Write-Host "  ✅ Old warrior directories deleted" -ForegroundColor Green
Write-Host "  ✅ Old tarballs deleted" -ForegroundColor Green
Write-Host "  ✅ Conversations backed up: $backupDir" -ForegroundColor Green
Write-Host ""
Write-Host "VM100 is now clean and ready for proper preset download!" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Delete warriors from LM Studio Hub (web UI)" -ForegroundColor White
Write-Host "2. Wait for new PRESETS to be created" -ForegroundColor White
Write-Host "3. Download presets from YOUR Hub" -ForegroundColor White
Write-Host "4. Download base models (via LM Studio GUI)" -ForegroundColor White
Write-Host "5. Apply presets to models" -ForegroundColor White
Write-Host ""
Write-Host "🐉 READY FOR PROPER HUB DEPLOYMENT! ⚡" -ForegroundColor Green

