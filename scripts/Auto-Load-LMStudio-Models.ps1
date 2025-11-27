# ============================================================================
# AUTO-LOAD LM STUDIO MODELS AT STARTUP
# ============================================================================
# This script waits for LM Studio to start, then checks if models are loaded.
# If 0 models are loaded, it opens LM Studio GUI to trigger auto-load.
# ============================================================================

Write-Host "`n🐉 LM Studio Auto-Loader Starting..." -ForegroundColor Cyan
Write-Host "Timestamp: $(Get-Date)" -ForegroundColor Gray

# Wait for LM Studio to start (max 5 minutes)
$maxWait = 300  # 5 minutes
$waited = 0
$interval = 10  # Check every 10 seconds

Write-Host "`nWaiting for LM Studio to start..." -ForegroundColor Yellow

while ($waited -lt $maxWait) {
    $lmProcess = Get-Process | Where-Object {$_.ProcessName -like "*LM*Studio*"}
    if ($lmProcess) {
        Write-Host "✅ LM Studio process detected!" -ForegroundColor Green
        break
    }
    Start-Sleep -Seconds $interval
    $waited += $interval
    Write-Host "   Waiting... $waited/$maxWait seconds" -ForegroundColor Gray
}

if ($waited -ge $maxWait) {
    Write-Host "❌ LM Studio did not start within $maxWait seconds" -ForegroundColor Red
    exit 1
}

# Wait additional 30 seconds for LM Studio to fully initialize
Write-Host "`nWaiting 30 seconds for LM Studio to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check if API is responding
Write-Host "`nChecking LM Studio API..." -ForegroundColor Yellow
$apiReady = $false
for ($i = 1; $i -le 6; $i++) {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:1234/v1/models" -Method Get -TimeoutSec 5
        Write-Host "✅ API is responding!" -ForegroundColor Green
        $apiReady = $true
        
        # Check how many models are loaded
        $modelCount = $response.data.Count
        Write-Host "📊 Models loaded: $modelCount" -ForegroundColor Cyan
        
        if ($modelCount -ge 6) {
            Write-Host "✅ All models already loaded! Nothing to do." -ForegroundColor Green
            exit 0
        } elseif ($modelCount -gt 0) {
            Write-Host "⚠️  Only $modelCount models loaded (expected 6)" -ForegroundColor Yellow
        } else {
            Write-Host "⚠️  No models loaded - will attempt to restore session" -ForegroundColor Yellow
        }
        break
    } catch {
        Write-Host "   Attempt $i/6: API not ready yet..." -ForegroundColor Gray
        Start-Sleep -Seconds 10
    }
}

if (-not $apiReady) {
    Write-Host "❌ LM Studio API did not respond after 60 seconds" -ForegroundColor Red
    Write-Host "   LM Studio may have started but API server is not running" -ForegroundColor Yellow
    Write-Host "   Please check LM Studio manually" -ForegroundColor Yellow
    exit 1
}

# ============================================================================
# WORKAROUND: If models aren't loaded, bring LM Studio to foreground
# ============================================================================
# LM Studio often auto-loads models when the window is focused/opened
# This is a workaround until we find the proper API or config setting

Write-Host "`n🔄 Attempting to trigger model auto-load..." -ForegroundColor Yellow
Write-Host "   Strategy: Bringing LM Studio window to foreground" -ForegroundColor Gray

# Get LM Studio window
Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class Win32 {
        [DllImport("user32.dll")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
        
        [DllImport("user32.dll")]
        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        
        public const int SW_RESTORE = 9;
    }
"@

$lmProcess = Get-Process | Where-Object {$_.ProcessName -like "*LM*Studio*" -and $_.MainWindowHandle -ne 0} | Select-Object -First 1

if ($lmProcess) {
    Write-Host "   Found LM Studio window (Handle: $($lmProcess.MainWindowHandle))" -ForegroundColor Gray
    
    # Restore and bring to foreground
    [Win32]::ShowWindow($lmProcess.MainWindowHandle, [Win32]::SW_RESTORE)
    Start-Sleep -Milliseconds 500
    [Win32]::SetForegroundWindow($lmProcess.MainWindowHandle)
    
    Write-Host "✅ LM Studio window activated" -ForegroundColor Green
    Write-Host "   If session restore is enabled, models should load now..." -ForegroundColor Gray
} else {
    Write-Host "⚠️  Could not find LM Studio main window" -ForegroundColor Yellow
}

# Wait and check again
Write-Host "`nWaiting 20 seconds for models to load..." -ForegroundColor Yellow
Start-Sleep -Seconds 20

try {
    $finalCheck = Invoke-RestMethod -Uri "http://localhost:1234/v1/models" -Method Get -TimeoutSec 5
    $finalCount = $finalCheck.data.Count
    
    if ($finalCount -ge 6) {
        Write-Host "`n✅✅✅ SUCCESS! All $finalCount models loaded!" -ForegroundColor Green
        Write-Host "`nLoaded models:" -ForegroundColor Cyan
        $finalCheck.data | ForEach-Object {
            Write-Host "   - $($_.id)" -ForegroundColor White
        }
    } elseif ($finalCount -gt 0) {
        Write-Host "`n⚠️  $finalCount models loaded (expected 6)" -ForegroundColor Yellow
        Write-Host "   You may need to load remaining models manually" -ForegroundColor Gray
    } else {
        Write-Host "`n❌ No models loaded automatically" -ForegroundColor Red
        Write-Host "`n📋 MANUAL STEPS REQUIRED:" -ForegroundColor Yellow
        Write-Host "   1. Open LM Studio" -ForegroundColor White
        Write-Host "   2. Load your 6 models (GOKU, VEGETA, PICCOLO, GOHAN, KRILLIN, FRIEZA)" -ForegroundColor White
        Write-Host "   3. Enable 'Restore session on startup' in LM Studio settings (if available)" -ForegroundColor White
    }
} catch {
    Write-Host "`n❌ Could not verify model loading" -ForegroundColor Red
}

Write-Host "`n🐉 Auto-Loader Complete - $(Get-Date)" -ForegroundColor Cyan

