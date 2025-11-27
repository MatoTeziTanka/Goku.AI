# ============================================================================
# SHENRON SYNDICATE - MASTER STARTUP SCRIPT (FIXED v4.1.4)
# ============================================================================
# This script ensures proper startup sequence for all SHENRON components
# Save to: C:\GOKU-AI\START-SHENRON.ps1
# Run manually or create desktop shortcut
# ============================================================================

param(
    [switch]$SkipChecks = $false,
    [switch]$Verbose = $false,
    [switch]$ForceRestart = $false
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

# ============================================================================
# CONFIGURATION
# ============================================================================

$LM_STUDIO_EXE = "C:\Users\Administrator\AppData\Local\Programs\LM Studio\LM Studio.exe"
$SHENRON_API_SCRIPT = "C:\GOKU-AI\shenron\shenron-v4-api-server.py"
$PYTHON_EXE = "C:\GOKU-AI\venv\Scripts\python.exe"
$VENV_ACTIVATE = "C:\GOKU-AI\venv\Scripts\Activate.ps1"

# ACTUAL DEPLOYED MODELS (November 7, 2025)
$MODELS_TO_LOAD = @(
    @{id="Goku-deepseek-coder-v2-lite-instruct"; warrior="GOKU"; size="~15GB"; context=163840},
    @{id="Vegeta-llama-3.2-3b-instruct"; warrior="VEGETA"; size="~2GB"; context=8192},
    @{id="Piccolo-qwen2.5-coder-7b-instruct"; warrior="PICCOLO"; size="~4GB"; context=32768},
    @{id="Gohan-mistral-7b-instruct-v0.3"; warrior="GOHAN"; size="~4GB"; context=32768},
    @{id="Krillin-phi-3-mini-128k-instruct"; warrior="KRILLIN"; size="~2GB"; context=131072},
    @{id="Frieza-phi-3-mini-128k-instruct"; warrior="FRIEZA"; size="~2GB"; context=131072}
)

$MAX_WAIT_LM_STUDIO = 120  # seconds (increased for model loading)
$MAX_WAIT_API = 30         # seconds
$API_PORT = 1234
$SHENRON_PORT = 5000

# Global flag to track if LM Studio was already running
$script:LM_STUDIO_ALREADY_RUNNING = $false
$script:SKIP_LM_STUDIO_START = $false

# ============================================================================
# LOGGING
# ============================================================================

$LOG_FILE = "C:\GOKU-AI\startup-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    $color = switch ($Level) {
        "SUCCESS" { "Green" }
        "WARNING" { "Yellow" }
        "ERROR" { "Red" }
        default { "White" }
    }
    
    $icon = switch ($Level) {
        "SUCCESS" { "✅" }
        "WARNING" { "⚠️" }
        "ERROR" { "❌" }
        default { "ℹ️" }
    }
    
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host "$icon $Message" -ForegroundColor $color
    Add-Content -Path $LOG_FILE -Value $logMessage
}

# ============================================================================
# FUNCTIONS
# ============================================================================

function Test-PortListening {
    param([int]$Port)
    try {
        $connection = Test-NetConnection -ComputerName localhost -Port $Port -WarningAction SilentlyContinue -InformationLevel Quiet
        return $connection
    } catch {
        return $false
    }
}

function Wait-ForPort {
    param([int]$Port, [int]$MaxWaitSeconds)
    Write-Log "Waiting for port $Port to be available (max $MaxWaitSeconds seconds)..."
    $elapsed = 0
    while ($elapsed -lt $MaxWaitSeconds) {
        if (Test-PortListening -Port $Port) {
            Write-Log "Port $Port is now available!" "SUCCESS"
            return $true
        }
        Start-Sleep -Seconds 5
        $elapsed += 5
        Write-Host "." -NoNewline
    }
    Write-Host ""
    Write-Log "Timeout waiting for port $Port" "ERROR"
    return $false
}

function Stop-ShenronComponents {
    Write-Log "Checking existing SHENRON components..."
    
    # Check if LM Studio is running AND has models loaded
    $lmProc = Get-Process | Where-Object {$_.ProcessName -match "LM.*Studio"} | Select-Object -First 1
    if ($lmProc -and -not $ForceRestart) {
        Write-Log "LM Studio is running (PID: $($lmProc.Id)). Checking status..."
        
        try {
            $models = Invoke-RestMethod -Uri "http://localhost:$API_PORT/v1/models" -TimeoutSec 5
            $modelCount = $models.data.Count
            
            if ($modelCount -ge 6) {
                Write-Log "LM Studio has $modelCount models loaded - keeping it running!" "SUCCESS"
                $script:LM_STUDIO_ALREADY_RUNNING = $true
                $script:SKIP_LM_STUDIO_START = $true
                
                Write-Log "Models currently loaded:" "INFO"
                $models.data | ForEach-Object {
                    Write-Log "   - $($_.id)" "INFO"
                }
                return
            } else {
                Write-Log "LM Studio only has $modelCount models - will restart" "WARNING"
            }
        } catch {
            Write-Log "LM Studio API not responding - will restart" "WARNING"
        }
        
        # Only kill if models aren't loaded or API not responding
        Write-Log "Stopping LM Studio (PID: $($lmProc.Id))..."
        Stop-Process -Id $lmProc.Id -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 3
    } elseif ($ForceRestart -and $lmProc) {
        Write-Log "Force restart requested - stopping LM Studio..." "WARNING"
        Stop-Process -Id $lmProc.Id -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 3
    }
    
    # Stop SHENRON API (always safe to restart)
    $shenronProc = Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {
        try {
            $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId = $($_.Id)" -ErrorAction SilentlyContinue).CommandLine
            $cmd -like "*shenron*"
        } catch {
            $false
        }
    }
    
    if ($shenronProc) {
        Write-Log "Stopping SHENRON API processes..."
        $shenronProc | ForEach-Object { 
            Write-Log "   Stopping PID $($_.Id)..."
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue 
        }
        Start-Sleep -Seconds 2
        Write-Log "SHENRON API processes stopped" "SUCCESS"
    }
}

# ============================================================================
# MAIN STARTUP SEQUENCE
# ============================================================================

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      🐉 SHENRON SYNDICATE - STARTUP SCRIPT v4.1.4 🐉         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Log "Startup initiated at $(Get-Date)"
Write-Log "Log file: $LOG_FILE"

# ============================================================================
# STEP 1: CLEAN START (Check existing processes)
# ============================================================================

Write-Host ""
Write-Log "══╣ STEP 1: Checking existing processes ╠══" "INFO"

Stop-ShenronComponents

# ============================================================================
# STEP 2: START LM STUDIO (if not already running)
# ============================================================================

if (-not $script:SKIP_LM_STUDIO_START) {
    Write-Host ""
    Write-Log "══╣ STEP 2: Starting LM Studio ╠══" "INFO"

    if (-not (Test-Path $LM_STUDIO_EXE)) {
        Write-Log "LM Studio not found at: $LM_STUDIO_EXE" "ERROR"
        Write-Log "Please install LM Studio or update the path" "ERROR"
        exit 1
    }

    Write-Log "Launching LM Studio..."
    Start-Process -FilePath $LM_STUDIO_EXE -WindowStyle Minimized

    # Wait for LM Studio API to be ready
    if (Wait-ForPort -Port $API_PORT -MaxWaitSeconds $MAX_WAIT_LM_STUDIO) {
        Write-Log "LM Studio API is ready on port $API_PORT" "SUCCESS"
    } else {
        Write-Log "LM Studio API did not start in time" "ERROR"
        Write-Log "Check logs at: C:\Users\Administrator\.lmstudio\logs\" "INFO"
        exit 1
    }

    # Give LM Studio extra time to fully initialize
    Write-Log "Waiting additional 10 seconds for LM Studio to stabilize..."
    Start-Sleep -Seconds 10
} else {
    Write-Host ""
    Write-Log "══╣ STEP 2: LM Studio (skipped - already running) ╠══" "SUCCESS"
}

# ============================================================================
# STEP 3: VERIFY MODELS ARE LOADED
# ============================================================================

Write-Host ""
Write-Log "══╣ STEP 3: Verifying AI Models ╠══" "INFO"

try {
    $loadedModels = Invoke-RestMethod -Uri "http://localhost:$API_PORT/v1/models" -TimeoutSec 10
    $loadedCount = $loadedModels.data.Count
    
    Write-Log "Models loaded: $loadedCount / $($MODELS_TO_LOAD.Count)"
    
    if ($loadedCount -eq 0) {
        Write-Log "No models loaded!" "ERROR"
        Write-Log "" "INFO"
        Write-Log "MANUAL ACTION REQUIRED:" "WARNING"
        Write-Log "1. Open LM Studio GUI" "INFO"
        Write-Log "2. Load these 6 models:" "INFO"
        foreach ($model in $MODELS_TO_LOAD) {
            Write-Log "   - $($model.id)" "INFO"
        }
        Write-Log "3. Press Enter to continue once models are loaded..." "INFO"
        Read-Host
    } elseif ($loadedCount -lt $MODELS_TO_LOAD.Count) {
        Write-Log "Only $loadedCount/$($MODELS_TO_LOAD.Count) models loaded" "WARNING"
        Write-Log "Loaded models:" "INFO"
        $loadedModels.data | ForEach-Object {
            Write-Log "   - $($_.id)" "INFO"
        }
        Write-Log "Continuing anyway..." "WARNING"
    } else {
        Write-Log "All models loaded successfully!" "SUCCESS"
        $loadedModels.data | ForEach-Object {
            Write-Log "   ✓ $($_.id)" "SUCCESS"
        }
    }
} catch {
    Write-Log "Could not verify models: $_" "ERROR"
    Write-Log "Continuing anyway..." "WARNING"
}

# ============================================================================
# STEP 4: CHECK RAM USAGE
# ============================================================================

Write-Host ""
Write-Log "══╣ STEP 4: System Resources Check ╠══" "INFO"

$mem = Get-CimInstance Win32_OperatingSystem
$totalRAM = [math]::Round($mem.TotalVisibleMemorySize / 1MB, 2)
$freeRAM = [math]::Round($mem.FreePhysicalMemory / 1MB, 2)
$usedRAM = $totalRAM - $freeRAM
$ramPercent = [math]::Round(($usedRAM / $totalRAM) * 100, 1)

Write-Log "RAM: $usedRAM GB / $totalRAM GB ($ramPercent%)"

if ($ramPercent -gt 90) {
    Write-Log "RAM usage is very high!" "WARNING"
} elseif ($ramPercent -gt 75) {
    Write-Log "RAM usage is elevated" "WARNING"
} else {
    Write-Log "RAM usage is acceptable" "SUCCESS"
}

# ============================================================================
# STEP 5: START SHENRON API SERVER
# ============================================================================

Write-Host ""
Write-Log "══╣ STEP 5: Starting SHENRON API Server ╠══" "INFO"

if (-not (Test-Path $SHENRON_API_SCRIPT)) {
    Write-Log "SHENRON API script not found at: $SHENRON_API_SCRIPT" "ERROR"
    exit 1
}

Write-Log "Activating Python virtual environment..."
& $VENV_ACTIVATE

Write-Log "Starting SHENRON orchestrator API..."
Start-Job -Name "SHENRON-API" -ScriptBlock {
    param($venvActivate, $pythonExe, $apiScript)
    & $venvActivate
    & $pythonExe $apiScript
} -ArgumentList $VENV_ACTIVATE, $PYTHON_EXE, $SHENRON_API_SCRIPT | Out-Null

Write-Log "SHENRON API started as background job"

# Wait for SHENRON API to be ready
if (Wait-ForPort -Port $SHENRON_PORT -MaxWaitSeconds $MAX_WAIT_API) {
    Write-Log "SHENRON API is ready on port $SHENRON_PORT" "SUCCESS"
} else {
    Write-Log "SHENRON API did not start in time" "ERROR"
    Write-Log "Check logs in C:\GOKU-AI\" "INFO"
    
    # Show job status
    $job = Get-Job -Name "SHENRON-API" -ErrorAction SilentlyContinue
    if ($job) {
        Write-Log "Job State: $($job.State)" "INFO"
        if ($job.State -eq "Failed") {
            Write-Log "Job Error:" "ERROR"
            Receive-Job -Job $job 2>&1 | ForEach-Object { Write-Log "   $_" "ERROR" }
        }
    }
    exit 1
}

# ============================================================================
# STEP 6: FINAL SYSTEM CHECK
# ============================================================================

Write-Host ""
Write-Log "══╣ STEP 6: Final System Check ╠══" "INFO"

# Check SHENRON health
try {
    $health = Invoke-RestMethod -Uri "http://localhost:$SHENRON_PORT/health" -TimeoutSec 5
    Write-Log "SHENRON health check: $($health.status)" "SUCCESS"
    Write-Log "Dragon awakened: $($health.dragon_awakened)" "SUCCESS"
    Write-Log "Features: $($health.features -join ', ')" "INFO"
} catch {
    Write-Log "SHENRON health check failed: $_" "ERROR"
}

# ============================================================================
# COMPLETION
# ============================================================================

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║          🐉 SHENRON SYNDICATE - STARTUP COMPLETE! 🐉          ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Log "🌐 SHENRON is now ready to grant wishes!" "SUCCESS"
Write-Log "" "INFO"
Write-Log "Access points:" "INFO"
Write-Log "   - LM Studio API:  http://localhost:$API_PORT" "INFO"
Write-Log "   - SHENRON API:    http://localhost:$SHENRON_PORT" "INFO"
Write-Log "   - Web Interface:  https://shenron.lightspeedup.com" "INFO"
Write-Log "" "INFO"
Write-Log "Log file saved to: $LOG_FILE" "INFO"
Write-Host ""

# Keep window open
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
