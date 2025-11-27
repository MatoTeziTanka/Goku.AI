# Azure VM101 Review - Quick Start Script
# This script sets up Azure credentials and runs the review

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Azure VM101 Zencoder Review Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if credentials are already set
if ($env:AZURE_OPENAI_ENDPOINT -and $env:AZURE_OPENAI_API_KEY) {
    Write-Host "[OK] Azure credentials found in environment" -ForegroundColor Green
    Write-Host "  Endpoint: $env:AZURE_OPENAI_ENDPOINT" -ForegroundColor Gray
    Write-Host "  Deployment: $env:AZURE_OPENAI_DEPLOYMENT" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "[WARNING] Azure credentials not set!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please set the following environment variables:" -ForegroundColor Yellow
    Write-Host "  AZURE_OPENAI_ENDPOINT" -ForegroundColor White
    Write-Host "  AZURE_OPENAI_API_KEY" -ForegroundColor White
    Write-Host "  AZURE_OPENAI_DEPLOYMENT (optional, defaults to gpt-4.1)" -ForegroundColor White
    Write-Host ""
    Write-Host "Example:" -ForegroundColor Cyan
    Write-Host '  $env:AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"' -ForegroundColor Gray
    Write-Host '  $env:AZURE_OPENAI_API_KEY = "your-api-key-here"' -ForegroundColor Gray
    Write-Host '  $env:AZURE_OPENAI_DEPLOYMENT = "gpt-4.1"' -ForegroundColor Gray
    Write-Host ""
    
    # Prompt for credentials
    $endpoint = Read-Host "Enter Azure OpenAI Endpoint (or press Enter to skip)"
    if ($endpoint) {
        $env:AZURE_OPENAI_ENDPOINT = $endpoint
    }
    
    $apiKey = Read-Host "Enter Azure OpenAI API Key (or press Enter to skip)" -AsSecureString
    if ($apiKey) {
        $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKey)
        $env:AZURE_OPENAI_API_KEY = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    }
    
    $deployment = Read-Host "Enter Deployment Name (default: gpt-4.1)"
    if ($deployment) {
        $env:AZURE_OPENAI_DEPLOYMENT = $deployment
    } else {
        $env:AZURE_OPENAI_DEPLOYMENT = "gpt-4.1"
    }
    
    Write-Host ""
}

# Check if credentials are now set
if (-not $env:AZURE_OPENAI_ENDPOINT -or -not $env:AZURE_OPENAI_API_KEY) {
    Write-Host "[ERROR] Azure credentials are required!" -ForegroundColor Red
    Write-Host "Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY" -ForegroundColor Red
    exit 1
}

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if openai package is installed
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Cyan
try {
    python -c "import openai" 2>&1 | Out-Null
    Write-Host "[OK] openai package installed" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] openai package not found. Installing..." -ForegroundColor Yellow
    pip install openai
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install openai package" -ForegroundColor Red
        exit 1
    }
}

# Run the script
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running Azure Review Script..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

python azure_vm101_zencoder_gpt41_review.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[SUCCESS] Review complete!" -ForegroundColor Green
    Write-Host "Check azure_reviews/ directory for output files" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "[ERROR] Script failed with exit code $LASTEXITCODE" -ForegroundColor Red
    Write-Host "Check azure_reviews/vm101_review.log for details" -ForegroundColor Yellow
}
