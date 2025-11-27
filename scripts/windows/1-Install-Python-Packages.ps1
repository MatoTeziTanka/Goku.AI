# ============================================================================
# SHENRON v3.0 - Phase 1: Install RAG Dependencies
# ============================================================================
# Run this on VM100 (Windows Server 2025) via PowerShell as Administrator
# ============================================================================

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🐉 SHENRON v3.0 - Installing RAG Backend                     ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "⚡ Step 1: Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ Python is installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python is NOT installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "   Please install Python 3.11+ from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "   Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Check if pip is available
Write-Host ""
Write-Host "⚡ Step 2: Checking pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "   ✅ pip is installed: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ pip is NOT installed!" -ForegroundColor Red
    Write-Host "   Installing pip..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
}

# Upgrade pip
Write-Host ""
Write-Host "⚡ Step 3: Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Create virtual environment
Write-Host ""
Write-Host "⚡ Step 4: Creating Python virtual environment..." -ForegroundColor Yellow
$venvPath = "C:\GOKU-AI\venv"
if (Test-Path $venvPath) {
    Write-Host "   ℹ️  Virtual environment already exists at $venvPath" -ForegroundColor Cyan
} else {
    python -m venv $venvPath
    Write-Host "   ✅ Virtual environment created at $venvPath" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "⚡ Step 5: Activating virtual environment..." -ForegroundColor Yellow
& "$venvPath\Scripts\Activate.ps1"

# Install ChromaDB
Write-Host ""
Write-Host "⚡ Step 6: Installing ChromaDB (Vector Database)..." -ForegroundColor Yellow
Write-Host "   This may take 2-3 minutes..." -ForegroundColor Cyan
pip install chromadb

# Install sentence-transformers
Write-Host ""
Write-Host "⚡ Step 7: Installing sentence-transformers (Embedding Model)..." -ForegroundColor Yellow
Write-Host "   This may take 3-5 minutes and download ~400MB..." -ForegroundColor Cyan
pip install sentence-transformers

# Install additional dependencies
Write-Host ""
Write-Host "⚡ Step 8: Installing additional dependencies..." -ForegroundColor Yellow
pip install requests flask numpy tiktoken paramiko

# Verify installations
Write-Host ""
Write-Host "⚡ Step 9: Verifying installations..." -ForegroundColor Yellow

$packages = @("chromadb", "sentence-transformers", "requests", "flask", "numpy", "tiktoken", "paramiko")
$allInstalled = $true

foreach ($package in $packages) {
    try {
        pip show $package | Out-Null
        Write-Host "   ✅ $package is installed" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ $package failed to install" -ForegroundColor Red
        $allInstalled = $false
    }
}

Write-Host ""
if ($allInstalled) {
    Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  ✅ RAG BACKEND DEPENDENCIES INSTALLED SUCCESSFULLY!          ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "📦 INSTALLED PACKAGES:" -ForegroundColor Cyan
    Write-Host "   - ChromaDB (Vector Database)" -ForegroundColor White
    Write-Host "   - sentence-transformers (Embedding Model)" -ForegroundColor White
    Write-Host "   - requests (HTTP client)" -ForegroundColor White
    Write-Host "   - flask (Web framework)" -ForegroundColor White
    Write-Host "   - numpy (Numerical computing)" -ForegroundColor White
    Write-Host "   - tiktoken (Token counting)" -ForegroundColor White
    Write-Host "   - paramiko (SSH client)" -ForegroundColor White
    Write-Host ""
    Write-Host "🐉 NEXT STEP: Run 2-Ingest-Knowledge-Base.ps1" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Red
    Write-Host "║  ⚠️  SOME PACKAGES FAILED TO INSTALL                          ║" -ForegroundColor Red
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please review errors above and try again." -ForegroundColor Yellow
}

Write-Host ""
pause

