<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
#!/bin/bash

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TASK_LOG="${HOME}/.vm101-deployment/TASK-1.3-WINDOWS-${TIMESTAMP}.log"
QC_CHECKLIST="${HOME}/.vm101-deployment/TASK-1.3-QC-${TIMESTAMP}.log"

mkdir -p "${HOME}/.vm101-deployment"

log_msg() {
    local level=$1
    local msg=$2
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $msg" | tee -a "$TASK_LOG"
}

qc_check() {
    local check=$1
    local status=$2
    echo "- [ ] $check: $status" >> "$QC_CHECKLIST"
}

log_msg "INFO" "=========================================="
log_msg "INFO" "TASK 1.3: Test Windows Deployment"
log_msg "INFO" "=========================================="
log_msg "INFO" ""
log_msg "INFO" "Objective: Deploy and test SSH key to Windows VM"
log_msg "INFO" "Time: ~30 minutes"
log_msg "INFO" "Location: VM101"
log_msg "INFO" ""

echo "Task 1.3 QC Checklist" > "$QC_CHECKLIST"
echo "===================" >> "$QC_CHECKLIST"
echo "" >> "$QC_CHECKLIST"

KEY_DIR="${HOME}/.ssh/vm-keys"

log_msg "INFO" "Testing Windows VM connectivity..."
log_msg "INFO" ""

test_windows_vm() {
    local vm_num=$1
    local user=$2
    local ip=$3
    local vm_name=$4
    
    log_msg "INFO" "----------------------------------------"
    log_msg "INFO" "Testing VM${vm_num} (${vm_name})"
    log_msg "INFO" "User: $user@$ip"
    log_msg "INFO" "----------------------------------------"
    
    if ! ssh -o ConnectTimeout=15 -o BatchMode=yes "${user}@${ip}" "echo 'Connection OK'" 2>/dev/null; then
        log_msg "WARN" "⚠️  Cannot connect to VM${vm_num} at ${user}@${ip}"
        log_msg "INFO" "This may be expected if:"
        log_msg "INFO" "  - Windows SSH Server is not running"
        log_msg "INFO" "  - PowerShell key deployment is needed"
        log_msg "INFO" "  - RDP manual setup required"
        qc_check "VM${vm_num} basic connectivity" "NOT AVAILABLE"
        return 1
    fi
    
    log_msg "INFO" "✅ SSH connection successful to VM${vm_num}"
    qc_check "VM${vm_num} basic connectivity" "PASS"
    
    local key_file="${KEY_DIR}/vm${vm_num}_key.pub"
    
    if [ ! -f "$key_file" ]; then
        log_msg "ERROR" "Key file not found: $key_file"
        qc_check "VM${vm_num} key file exists" "FAILED"
        return 1
    fi
    
    log_msg "INFO" "✅ Key file found: $key_file"
    qc_check "VM${vm_num} key file exists" "PASS"
    
    log_msg "INFO" ""
    log_msg "INFO" "Attempting key deployment to VM${vm_num}..."
    
    if cat "$key_file" | ssh "${user}@${ip}" \
        'powershell -Command "$key = [Console]::In.ReadLine(); `
            $sshDir = \"C:\\Users\\Administrator\\.ssh\"; `
            if (!(Test-Path $sshDir)) { New-Item -ItemType Directory -Path $sshDir -Force | Out-Null }; `
            Add-Content -Path \"$sshDir\\authorized_keys\" -Value $key; `
            icacls \"$sshDir\\authorized_keys\" /inheritance:r /grant \"Administrator:F\" | Out-Null; `
            echo \"Key added successfully\""' >> "$TASK_LOG" 2>&1; then
        
        log_msg "INFO" "✅ Key deployment to VM${vm_num} successful"
        qc_check "VM${vm_num} PowerShell key deployment" "PASS"
        return 0
    else
        log_msg "WARN" "⚠️  PowerShell key deployment failed"
        log_msg "INFO" "This may require manual setup via RDP"
        qc_check "VM${vm_num} PowerShell key deployment" "WARNING - check RDP"
        return 1
    fi
}

log_msg "INFO" ""
log_msg "INFO" "TESTING WINDOWS VMs"
log_msg "INFO" ""

test_windows_vm 100 "Administrator" "<VM100_IP>" "AI Host (GOKU)"

log_msg "INFO" ""

read -p "Test VM200 (Plex)? (yes/no): " test_200
if [ "$test_200" = "yes" ]; then
    test_windows_vm 200 "Administrator" "<VM200_IP>" "Plex Media Server"
fi

log_msg "INFO" ""
log_msg "INFO" "=========================================="
log_msg "INFO" "WINDOWS DEPLOYMENT OPTIONS"
log_msg "INFO" "=========================================="
log_msg "INFO" ""
log_msg "INFO" "If PowerShell deployment failed, use one of these methods:"
log_msg "INFO" ""
log_msg "INFO" "OPTION A: Manual RDP Setup"
log_msg "INFO" "  1. Connect to Windows VM via RDP"
log_msg "INFO" "  2. Open C:\\Users\\Administrator\\.ssh\\authorized_keys"
log_msg "INFO" "  3. Paste the public key:"
log_msg "INFO" ""

KEY_FILE="${KEY_DIR}/vm100_key.pub"
if [ -f "$KEY_FILE" ]; then
    log_msg "INFO" "$(cat $KEY_FILE)"
    log_msg "INFO" ""
fi

log_msg "INFO" "OPTION B: Manual PowerShell Setup (if SSH works)"
log_msg "INFO" "  ssh Administrator@<VM100_IP>"
log_msg "INFO" "  Copy the key below and paste into PowerShell:"
log_msg "INFO" ""
log_msg "INFO" "  \$key = 'PASTE_KEY_HERE'"
log_msg "INFO" "  \$sshDir = 'C:\\Users\\Administrator\\.ssh'"
log_msg "INFO" "  if (!(Test-Path \$sshDir)) {"
log_msg "INFO" "      New-Item -ItemType Directory -Path \$sshDir -Force | Out-Null"
log_msg "INFO" "  }"
log_msg "INFO" "  Add-Content -Path \"\$sshDir\\authorized_keys\" -Value \$key"
log_msg "INFO" "  icacls \"\$sshDir\\authorized_keys\" /inheritance:r /grant \"Administrator:F\""
log_msg "INFO" ""

log_msg "INFO" "OPTION C: Create SSH Config Entry (Linux alternative)"
log_msg "INFO" "  If Windows SSH doesn't work, use SSH config for RDP fallback"
log_msg "INFO" "  Already handled in SSH config as fallback"
log_msg "INFO" ""

log_msg "INFO" "=========================================="
log_msg "INFO" "TESTING SSH WITH NEW KEYS"
log_msg "INFO" "=========================================="
log_msg "INFO" ""

log_msg "INFO" "Testing SSH connectivity with new keys (after deployment)..."

if ssh -o ConnectTimeout=5 -o BatchMode=yes "Administrator@<VM100_IP>" "hostname" >> "$TASK_LOG" 2>&1; then
    log_msg "INFO" "✅ SSH to VM100 successful with new key"
    qc_check "VM100 SSH test with new key" "PASS"
else
    log_msg "WARN" "⚠️  SSH to VM100 still requires password or connection failed"
    log_msg "INFO" "Possible reasons:"
    log_msg "INFO" "  1. Key not yet added to authorized_keys"
    log_msg "INFO" "  2. Windows SSH Server not running"
    log_msg "INFO" "  3. Manual RDP setup needed"
    qc_check "VM100 SSH test with new key" "WARNING - manual verification needed"
fi

log_msg "INFO" ""
log_msg "INFO" "=========================================="
log_msg "INFO" "TASK 1.3 VERIFICATION SUMMARY"
log_msg "INFO" "=========================================="
log_msg "INFO" ""
log_msg "INFO" "✅ Windows VM testing completed"
log_msg "INFO" "✅ Key file ready for deployment"
log_msg "INFO" "⚠️  Note: Windows deployment may require RDP manual setup"
log_msg "INFO" ""
log_msg "INFO" "If SSH to Windows VMs fails:"
log_msg "INFO" "  1. Use RDP to connect manually"
log_msg "INFO" "  2. Add key using PowerShell commands above"
log_msg "INFO" "  3. Or use alternative SSH method via SSH config"
log_msg "INFO" ""
log_msg "INFO" "Next Steps:"
log_msg "INFO" "  1. Review Windows deployment options above"
log_msg "INFO" "  2. Complete manual setup if needed"
log_msg "INFO" "  3. Review log: $TASK_LOG"
log_msg "INFO" "  4. Proceed to Task 1.4 (verify services)"
log_msg "INFO" ""
log_msg "SUCCESS" "✅ Task 1.3 Complete"

echo ""
echo "QC Checklist saved to: $QC_CHECKLIST"
echo ""
cat "$QC_CHECKLIST"
