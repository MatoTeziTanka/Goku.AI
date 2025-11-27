<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# BitPhoenix SSH Connectivity Test Script
# Run this in PowerShell (not WSL) to test SSH access

Write-Host "🔍 BitPhoenix SSH Connectivity Test" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Get local IP
$localIP = (Get-NetIPConfiguration | Where-Object { $_.IPv4DefaultGateway -ne $null -and $_.NetAdapter.Status -ne "Disconnected" }).IPv4Address.IPAddress
Write-Host "Local IP: $localIP" -ForegroundColor White

# Test 1: Check if SSH port is open locally
Write-Host ""
Write-Host "🔍 Test 1: Local SSH Port Check" -ForegroundColor Yellow
Write-Host "-------------------------------" -ForegroundColor Yellow

try {
    $localTest = Test-NetConnection -ComputerName localhost -Port 22
    if ($localTest.TcpTestSucceeded) {
        Write-Host "✅ SSH port 22 is open locally" -ForegroundColor Green
    } else {
        Write-Host "❌ SSH port 22 is closed locally" -ForegroundColor Red
    }
} catch {
    Write-Host "⚠️  Could not test local port" -ForegroundColor Yellow
}

# Test 2: Check Windows Firewall
Write-Host ""
Write-Host "🔍 Test 2: Windows Firewall Rules" -ForegroundColor Yellow
Write-Host "----------------------------------" -ForegroundColor Yellow

$sshRules = Get-NetFirewallRule -DisplayName "*SSH*" -ErrorAction SilentlyContinue
if ($sshRules) {
    Write-Host "✅ SSH firewall rules found:" -ForegroundColor Green
    foreach ($rule in $sshRules) {
        Write-Host "   - $($rule.DisplayName) ($($rule.Name)): $($rule.Enabled)" -ForegroundColor White
    }
} else {
    Write-Host "❌ No SSH firewall rules found" -ForegroundColor Red
}

# Test 3: Check SSH service status
Write-Host ""
Write-Host "🔍 Test 3: SSH Service Status" -ForegroundColor Yellow
Write-Host "----------------------------" -ForegroundColor Yellow

$sshService = Get-Service -Name sshd -ErrorAction SilentlyContinue
if ($sshService) {
    Write-Host "✅ SSH service found: $($sshService.Status)" -ForegroundColor Green
    if ($sshService.Status -ne "Running") {
        Write-Host "⚠️  SSH service not running - starting..." -ForegroundColor Yellow
        Start-Service sshd -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        $sshService = Get-Service -Name sshd
        Write-Host "   Service status: $($sshService.Status)" -ForegroundColor White
    }
} else {
    Write-Host "❌ SSH service (sshd) not found" -ForegroundColor Red
}

# Test 4: Network connectivity test
Write-Host ""
Write-Host "🔍 Test 4: Network Connectivity" -ForegroundColor Yellow
Write-Host "-------------------------------" -ForegroundColor Yellow

# Test basic connectivity
$testIPs = @("<VM101_IP>", "8.8.8.8", "google.com")
foreach ($ip in $testIPs) {
    try {
        $ping = Test-Connection -ComputerName $ip -Count 1 -ErrorAction Stop
        Write-Host "✅ Can reach $ip ($($ping.ResponseTime)ms)" -ForegroundColor Green
    } catch {
        Write-Host "❌ Cannot reach $ip" -ForegroundColor Red
    }
}

# Test 5: WSL Network Info
Write-Host ""
Write-Host "🔍 Test 5: WSL Network Information" -ForegroundColor Yellow
Write-Host "----------------------------------" -ForegroundColor Yellow

Write-Host "If WSL SSH is configured, run this in WSL Ubuntu terminal:" -ForegroundColor Cyan
Write-Host "  sudo systemctl status ssh" -ForegroundColor White
Write-Host "  sudo netstat -tlnp | grep :22" -ForegroundColor White
Write-Host "  ip addr show | grep inet" -ForegroundColor White

# Test 6: Port forwarding suggestion
Write-Host ""
Write-Host "🔍 Test 6: Port Forwarding Setup" -ForegroundColor Yellow
Write-Host "--------------------------------" -ForegroundColor Yellow

Write-Host "If WSL SSH is running but not accessible externally," -ForegroundColor Yellow
Write-Host "you may need to set up port forwarding from Windows to WSL:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Run in PowerShell (Administrator):" -ForegroundColor Cyan
Write-Host "  netsh interface portproxy add v4tov4 listenport=22 listenaddress=0.0.0.0 connectport=22 connectaddress=172.17.48.1" -ForegroundColor White
Write-Host ""
Write-Host "Note: 172.17.48.1 is the WSL virtual adapter IP from ipconfig" -ForegroundColor Yellow

# Summary
Write-Host ""
Write-Host "📋 Connectivity Test Summary" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔹 Local SSH: Test with 'ssh sethp@localhost'" -ForegroundColor White
Write-Host "🔹 WSL SSH: Test with 'ssh sethp@172.17.48.1' (from Windows)" -ForegroundColor White
Write-Host "🔹 External SSH: Test with 'ssh sethp@192.168.12.38' (from another machine)" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Quick Fix Commands:" -ForegroundColor Green
Write-Host "   1. Windows SSH: Run .\scripts\fix-ssh-access.ps1 (as Admin)" -ForegroundColor White
Write-Host "   2. WSL SSH: Run bash scripts/fix-wsl-ssh.sh (in WSL)" -ForegroundColor White
Write-Host "   3. Test: ssh sethp@192.168.12.38" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Once SSH works, I can deploy BitPhoenix remotely!" -ForegroundColor Green
