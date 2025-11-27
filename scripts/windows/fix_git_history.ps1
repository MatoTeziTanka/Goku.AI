# PowerShell script to rewrite git history and remove secrets
# This removes commit 990814e from history

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  REMOVING SECRETS FROM GIT HISTORY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Verify current state
Write-Host "Step 1: Checking current commits..." -ForegroundColor Yellow
git log --oneline -5
Write-Host ""

# Step 2: Reset to commit before secrets (keeping files)
Write-Host "Step 2: Resetting to commit 2c393fd (before secrets)..." -ForegroundColor Yellow
Write-Host "  This will keep all your sanitized files" -ForegroundColor Gray
Write-Host ""

$confirm = Read-Host "Continue? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "Cancelled." -ForegroundColor Red
    exit
}

# Reset to base commit, keeping all files staged
Write-Host "Resetting to base commit (soft reset)..." -ForegroundColor Green
git reset --soft 2c393fd

# Verify files are staged
Write-Host ""
Write-Host "Step 3: Verifying sanitized files are staged..." -ForegroundColor Yellow
$staged = git diff --cached --name-only
Write-Host "  Staged files: $($staged.Count)" -ForegroundColor Green

# Create new clean commit
Write-Host ""
Write-Host "Step 4: Creating new clean commit..." -ForegroundColor Yellow
git commit -m "feat(repo): initial commit - Goku.AI framework v2.9.0 (sanitized)"

# Show new history
Write-Host ""
Write-Host "Step 5: New commit history:" -ForegroundColor Yellow
git log --oneline -5

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  HISTORY REWRITE COMPLETE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step: Force push to GitHub" -ForegroundColor Yellow
Write-Host "  git push -u origin main --force" -ForegroundColor White
Write-Host ""
Write-Host "WARNING: Force push will overwrite remote history!" -ForegroundColor Red
Write-Host ""

