# SHENRON QUEST MANAGER - Deployment Script
# Deploys Quest Manager as a Windows service

Write-Host "`n=== SHENRON QUEST MANAGER DEPLOYMENT ===" -ForegroundColor Cyan
Write-Host "Version: 1.0" -ForegroundColor Gray
Write-Host "Date: $(Get-Date)`n" -ForegroundColor Gray

# Step 1: Copy files
Write-Host "[1/6] Copying Quest Manager files..." -ForegroundColor Yellow
Copy-Item quest_manager.py C:\GOKU-AI\shenron\ -Force
Copy-Item quest_api.py C:\GOKU-AI\shenron\ -Force

if (Test-Path C:\GOKU-AI\shenron\quest_manager.py) {
    Write-Host "  [OK] quest_manager.py copied" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] quest_manager.py not found" -ForegroundColor Red
    exit 1
}

# Step 2: Test Python imports
Write-Host "`n[2/6] Testing Python dependencies..." -ForegroundColor Yellow
$testScript = @"
import sys
sys.path.insert(0, 'C:/GOKU-AI/shenron')
try:
    import quest_manager
    print('[OK] quest_manager imports successfully')
except Exception as e:
    print(f'[FAIL] Import error: {e}')
    sys.exit(1)
"@

$testScript | Out-File C:\temp\test_quest.py -Encoding UTF8
C:\GOKU-AI\venv\Scripts\python.exe C:\temp\test_quest.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "  [FAIL] Python import test failed" -ForegroundColor Red
    exit 1
}

# Step 3: Initialize database
Write-Host "`n[3/6] Initializing Quest database..." -ForegroundColor Yellow
$initScript = @"
import sys
sys.path.insert(0, 'C:/GOKU-AI/shenron')
from quest_manager import QuestDatabase

db = QuestDatabase()
print('[OK] Database initialized')
db.close()
"@

$initScript | Out-File C:\temp\init_quest_db.py -Encoding UTF8
C:\GOKU-AI\venv\Scripts\python.exe C:\temp\init_quest_db.py

if (Test-Path C:\GOKU-AI\quests.db) {
    Write-Host "  [OK] Database created: C:\GOKU-AI\quests.db" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Database not created" -ForegroundColor Red
    exit 1
}

# Step 4: Create service wrapper script
Write-Host "`n[4/6] Creating service wrapper..." -ForegroundColor Yellow
$serviceScript = @"
import sys
sys.path.insert(0, 'C:/GOKU-AI/shenron')

from quest_manager import QuestManager
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('C:/GOKU-AI/quest-service.log'),
        logging.StreamHandler()
    ]
)

if __name__ == '__main__':
    manager = QuestManager()
    print('SHENRON Quest Manager Service starting...')
    try:
        manager.run_manager_loop(delay_seconds=60)
    except KeyboardInterrupt:
        print('Service stopped')
    finally:
        manager.stop()
"@

$serviceScript | Out-File C:\GOKU-AI\shenron\quest_service.py -Encoding UTF8
Write-Host "  [OK] Service wrapper created" -ForegroundColor Green

# Step 5: Install as Windows service using NSSM
Write-Host "`n[5/6] Installing Windows service..." -ForegroundColor Yellow

# Check if service already exists
$existingService = Get-Service -Name "SHENRON-QUESTS" -ErrorAction SilentlyContinue
if ($existingService) {
    Write-Host "  [INFO] Service already exists, removing..." -ForegroundColor Yellow
    Stop-Service -Name "SHENRON-QUESTS" -Force -ErrorAction SilentlyContinue
    C:\ProgramData\nssm\nssm.exe remove "SHENRON-QUESTS" confirm
}

# Install service
C:\ProgramData\nssm\nssm.exe install "SHENRON-QUESTS" `
    "C:\GOKU-AI\venv\Scripts\python.exe" `
    "C:\GOKU-AI\shenron\quest_service.py"

# Configure service
C:\ProgramData\nssm\nssm.exe set "SHENRON-QUESTS" DisplayName "SHENRON Quest Manager"
C:\ProgramData\nssm\nssm.exe set "SHENRON-QUESTS" Description "SHENRON Eternal Quest Manager - Autonomous Problem Solving"
C:\ProgramData\nssm\nssm.exe set "SHENRON-QUESTS" Start SERVICE_AUTO_START
C:\ProgramData\nssm\nssm.exe set "SHENRON-QUESTS" AppDirectory "C:\GOKU-AI\shenron"
C:\ProgramData\nssm\nssm.exe set "SHENRON-QUESTS" AppStdout "C:\GOKU-AI\quest-service-stdout.log"
C:\ProgramData\nssm\nssm.exe set "SHENRON-QUESTS" AppStderr "C:\GOKU-AI\quest-service-stderr.log"

Write-Host "  [OK] Service installed" -ForegroundColor Green

# Step 6: Start services
Write-Host "`n[6/6] Starting services..." -ForegroundColor Yellow

# Start Quest Manager service
Start-Service -Name "SHENRON-QUESTS"
Start-Sleep -Seconds 3

$questService = Get-Service -Name "SHENRON-QUESTS"
if ($questService.Status -eq "Running") {
    Write-Host "  [OK] SHENRON-QUESTS service: RUNNING" -ForegroundColor Green
} else {
    Write-Host "  [WARN] SHENRON-QUESTS service: $($questService.Status)" -ForegroundColor Yellow
}

# Note about API
Write-Host "`n[INFO] Quest API can be started separately:" -ForegroundColor Cyan
Write-Host "  cd C:\GOKU-AI\shenron" -ForegroundColor Gray
Write-Host "  C:\GOKU-AI\venv\Scripts\python.exe quest_api.py" -ForegroundColor Gray

# Summary
Write-Host "`n=== DEPLOYMENT COMPLETE ===" -ForegroundColor Green
Write-Host ""
Write-Host "Services:" -ForegroundColor Cyan
Write-Host "  - SHENRON: $((Get-Service SHENRON).Status)" -ForegroundColor White
Write-Host "  - SHENRON-QUESTS: $((Get-Service SHENRON-QUESTS).Status)" -ForegroundColor White
Write-Host ""
Write-Host "Files:" -ForegroundColor Cyan
Write-Host "  - Database: C:\GOKU-AI\quests.db" -ForegroundColor White
Write-Host "  - Quest Manager: C:\GOKU-AI\shenron\quest_manager.py" -ForegroundColor White
Write-Host "  - Quest API: C:\GOKU-AI\shenron\quest_api.py" -ForegroundColor White
Write-Host "  - Service Log: C:\GOKU-AI\quest-service.log" -ForegroundColor White
Write-Host ""
Write-Host "Test Quest Manager:" -ForegroundColor Cyan
Write-Host "  cd C:\GOKU-AI\shenron" -ForegroundColor White
Write-Host "  C:\GOKU-AI\venv\Scripts\python.exe quest_manager.py create \"Test Goal\"" -ForegroundColor White
Write-Host ""

