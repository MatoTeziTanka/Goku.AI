# SHENRON API Startup Script
# This script starts the SHENRON API and ensures it's running

$logFile = "C:\GOKU-AI\shenron\logs\shenron-startup.log"
$apiScript = "C:\GOKU-AI\shenron\shenron-v4-api-server.py"
$pythonExe = "C:\Program Files\Python311\python.exe"
$workingDir = "C:\GOKU-AI\shenron"

# Create log directory if it doesn't exist
$logDir = Split-Path $logFile -Parent
if (!(Test-Path $logDir)) {
    New-Item -Path $logDir -ItemType Directory -Force | Out-Null
}

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "${timestamp} - $Message" | Out-File -FilePath $logFile -Append
    Write-Host "$timestamp - $Message"
}

Write-Log "=========================================="
Write-Log "SHENRON API Startup Script"
Write-Log "=========================================="

# Check if something is already bound to port 5000
$existingConnection = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
if ($existingConnection) {
    $existingPid = $existingConnection.OwningProcess
    Write-Log "SHENRON already running (PID: $existingPid)"

    $existingProcess = Get-Process -Id $existingPid -ErrorAction SilentlyContinue
    if ($existingProcess -and $existingProcess.Name -eq "python") {
        Write-Log "Confirmed: Python process on port 5000 is active"
        exit 0
    } else {
        Write-Log "WARNING: Port 5000 occupied by non-Python process, attempting to start anyway..."
    }
}

# Kill orphaned SHENRON python processes
Write-Log "Checking for orphaned Python processes..."
Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId = $($_.Id)" -ErrorAction SilentlyContinue).CommandLine
    $cmdLine -like "*shenron*api*"
} | ForEach-Object {
    Write-Log "Killing orphaned process: PID $($_.Id)"
    Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
}

Start-Sleep -Seconds 2

Write-Log "Starting SHENRON API..."
Write-Log "Python: $pythonExe"
Write-Log "Script: $apiScript"
Write-Log "Working Dir: $workingDir"

try {
    $process = Start-Process -FilePath $pythonExe `
                             -ArgumentList $apiScript `
                             -WorkingDirectory $workingDir `
                             -WindowStyle Minimized `
                             -PassThru

    Write-Log "SHENRON API started with PID: $($process.Id)"
    Start-Sleep -Seconds 5

    $verification = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
    if ($verification) {
        Write-Log "SUCCESS: SHENRON API is now listening on port 5000"
        Write-Log "=========================================="
        exit 0
    } else {
        Write-Log "ERROR: SHENRON API did not start listening on port 5000"
        Write-Log "=========================================="
        exit 1
    }
} catch {
    Write-Log "ERROR: Failed to start SHENRON API"
    Write-Log "Error details: $_"
    Write-Log "=========================================="
    exit 1
}
