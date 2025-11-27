# ============================================================================
# SETUP LM STUDIO AUTO-LOAD AT STARTUP
# ============================================================================
# Run this script ONCE as Administrator to configure auto-loading
# ============================================================================

Write-Host "`n🐉 Setting up LM Studio Auto-Load..." -ForegroundColor Cyan

# 1. Copy the auto-load script to a permanent location
$scriptPath = "C:\GOKU-AI\scripts\Auto-Load-LMStudio-Models.ps1"
$scriptDir = Split-Path $scriptPath

if (!(Test-Path $scriptDir)) {
    New-Item -ItemType Directory -Path $scriptDir -Force | Out-Null
    Write-Host "✅ Created: $scriptDir" -ForegroundColor Green
}

# Copy the script (assuming it's on the Desktop)
$sourceScript = "C:\Users\Administrator\Desktop\Auto-Load-LMStudio-Models.ps1"
if (Test-Path $sourceScript) {
    Copy-Item $sourceScript $scriptPath -Force
    Write-Host "✅ Copied script to: $scriptPath" -ForegroundColor Green
} else {
    Write-Host "❌ Source script not found at: $sourceScript" -ForegroundColor Red
    Write-Host "   Please ensure Auto-Load-LMStudio-Models.ps1 is on the Desktop" -ForegroundColor Yellow
    exit 1
}

# 2. Create a Scheduled Task to run at startup
$taskName = "LMStudio-AutoLoad-Models"
$taskDescription = "Automatically load LM Studio models at startup for Shenron AI"

# Remove existing task if it exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "⚠️  Removed existing task" -ForegroundColor Yellow
}

# Create action
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`""

# Create trigger (at startup, with 2-minute delay to let LM Studio start first)
$trigger = New-ScheduledTaskTrigger -AtStartup
$trigger.Delay = "PT2M"  # 2-minute delay

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

# Create principal (run as current user)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

# Register the task
Register-ScheduledTask `
    -TaskName $taskName `
    -Description $taskDescription `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Force

Write-Host "✅ Scheduled Task created: $taskName" -ForegroundColor Green

# 3. Display task info
Write-Host "`n📋 Task Configuration:" -ForegroundColor Cyan
Get-ScheduledTask -TaskName $taskName | Format-List TaskName, State, Description

Write-Host "`n✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "`nThe script will now run automatically:" -ForegroundColor White
Write-Host "   - 2 minutes after Windows starts" -ForegroundColor Gray
Write-Host "   - Waits for LM Studio to initialize" -ForegroundColor Gray
Write-Host "   - Checks if 6 models are loaded" -ForegroundColor Gray
Write-Host "   - Attempts to trigger auto-load if needed" -ForegroundColor Gray

Write-Host "`n🧪 To test now, run:" -ForegroundColor Yellow
Write-Host "   Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor White

Write-Host "`n📝 To view task logs:" -ForegroundColor Yellow
Write-Host "   Get-ScheduledTaskInfo -TaskName '$taskName'" -ForegroundColor White

Write-Host "`n❗ IMPORTANT:" -ForegroundColor Red
Write-Host "   LM Studio does not have a documented API for loading models" -ForegroundColor Yellow
Write-Host "   The script will try to trigger session restore by activating the window" -ForegroundColor Yellow
Write-Host "   If this doesn't work, check if LM Studio has a 'Restore session' setting" -ForegroundColor Yellow

Write-Host "`n🐉 Shenron automation enhanced!" -ForegroundColor Cyan

