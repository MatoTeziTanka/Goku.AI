#!/bin/bash

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TASK_LOG="${HOME}/.vm101-deployment/TASK-1.1-SETUP-${TIMESTAMP}.log"
QC_CHECKLIST="${HOME}/.vm101-deployment/TASK-1.1-QC-${TIMESTAMP}.log"

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
log_msg "INFO" "TASK 1.1: Execute Setup Script"
log_msg "INFO" "=========================================="
log_msg "INFO" ""
log_msg "INFO" "Objective: Generate SSH keys for all VMs and create SSH config"
log_msg "INFO" "Time: ~30 minutes"
log_msg "INFO" "Location: VM101"
log_msg "INFO" ""

echo "Task 1.1 QC Checklist" > "$QC_CHECKLIST"
echo "===================" >> "$QC_CHECKLIST"
echo "" >> "$QC_CHECKLIST"

SETUP_SCRIPT="${HOME}/VM101-SEPARATE-KEYS-SETUP.sh"

if [ ! -f "$SETUP_SCRIPT" ]; then
    log_msg "ERROR" "Setup script not found: $SETUP_SCRIPT"
    log_msg "INFO" "Checking current directory..."
    
    if [ -f "VM101-SEPARATE-KEYS-SETUP.sh" ]; then
        cp VM101-SEPARATE-KEYS-SETUP.sh "$SETUP_SCRIPT"
        log_msg "INFO" "Copied setup script from current directory"
    else
        log_msg "ERROR" "Setup script not found in any location"
        qc_check "Setup script located" "FAILED - not found"
        exit 1
    fi
fi

log_msg "INFO" "✅ Setup script found: $SETUP_SCRIPT"
qc_check "Setup script located" "PASS"

log_msg "INFO" ""
log_msg "INFO" "Making setup script executable..."
chmod +x "$SETUP_SCRIPT"
log_msg "INFO" "✅ Setup script is executable"

log_msg "INFO" ""
log_msg "INFO" "Executing VM101-SEPARATE-KEYS-SETUP.sh..."
log_msg "INFO" ""

if bash "$SETUP_SCRIPT" >> "$TASK_LOG" 2>&1; then
    log_msg "SUCCESS" "✅ Setup script executed successfully"
    qc_check "Setup script execution" "PASS"
else
    log_msg "ERROR" "❌ Setup script execution failed"
    qc_check "Setup script execution" "FAILED - check logs"
    exit 1
fi

log_msg "INFO" ""
log_msg "INFO" "Verifying key generation..."

KEY_DIR="${HOME}/.ssh/vm-keys"

if [ ! -d "$KEY_DIR" ]; then
    log_msg "ERROR" "Key directory not created: $KEY_DIR"
    qc_check "Key directory created" "FAILED - not found"
    exit 1
fi

log_msg "INFO" "✅ Key directory exists: $KEY_DIR"
qc_check "Key directory created" "PASS"

KEY_COUNT=$(find "$KEY_DIR" -name "vm*_key" -type f | wc -l)
PUB_KEY_COUNT=$(find "$KEY_DIR" -name "vm*_key.pub" -type f | wc -l)

log_msg "INFO" "Keys generated:"
log_msg "INFO" "  - Private keys: $KEY_COUNT"
log_msg "INFO" "  - Public keys: $PUB_KEY_COUNT"

if [ $KEY_COUNT -lt 3 ]; then
    log_msg "WARN" "Expected at least 3 VM keys, found $KEY_COUNT"
    qc_check "Keys generated (minimum 3)" "WARNING - only $KEY_COUNT found"
else
    log_msg "INFO" "✅ Expected number of keys generated"
    qc_check "Keys generated (minimum 3)" "PASS"
fi

log_msg "INFO" ""
log_msg "INFO" "Listing generated keys:"
ls -lah "$KEY_DIR"/ 2>&1 | tee -a "$TASK_LOG"

log_msg "INFO" ""
log_msg "INFO" "Checking SSH config..."

SSH_CONFIG="${HOME}/.ssh/config"

if [ ! -f "$SSH_CONFIG" ]; then
    log_msg "ERROR" "SSH config not created: $SSH_CONFIG"
    qc_check "SSH config created" "FAILED - not found"
    exit 1
fi

log_msg "INFO" "✅ SSH config created: $SSH_CONFIG"
qc_check "SSH config created" "PASS"

CONFIG_ENTRIES=$(grep -c "^Host vm" "$SSH_CONFIG" || true)
log_msg "INFO" "SSH config entries: $CONFIG_ENTRIES"

if [ $CONFIG_ENTRIES -lt 3 ]; then
    log_msg "WARN" "Expected at least 3 Host entries, found $CONFIG_ENTRIES"
    qc_check "SSH config entries (minimum 3)" "WARNING - only $CONFIG_ENTRIES found"
else
    log_msg "INFO" "✅ Expected number of SSH config entries"
    qc_check "SSH config entries (minimum 3)" "PASS"
fi

log_msg "INFO" ""
log_msg "INFO" "SSH config contents (first 50 lines):"
head -50 "$SSH_CONFIG" 2>&1 | tee -a "$TASK_LOG"

log_msg "INFO" ""
log_msg "INFO" "Checking helper scripts..."

HELPER_SCRIPTS=("${HOME}/add-vm-keys.sh" "${HOME}/test-vm-keys.sh" "${HOME}/remove-old-shared-keys.sh")

for script in "${HELPER_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        log_msg "INFO" "✅ Found: $script"
        qc_check "Helper script $(basename $script)" "PASS"
    else
        log_msg "WARN" "⚠️  Missing: $script"
        qc_check "Helper script $(basename $script)" "WARNING - not found"
    fi
done

log_msg "INFO" ""
log_msg "INFO" "Testing key file permissions..."

PERM_CHECK=$(stat -c "%a" "$KEY_DIR"/vm*_key 2>/dev/null | sort | uniq)
log_msg "INFO" "Private key permissions: $PERM_CHECK (should be 600)"

if [ "$PERM_CHECK" = "600" ]; then
    log_msg "INFO" "✅ Key permissions are correct"
    qc_check "Key file permissions (600)" "PASS"
else
    log_msg "WARN" "⚠️  Key permissions may not be correct: $PERM_CHECK"
    qc_check "Key file permissions (600)" "WARNING - $PERM_CHECK"
fi

log_msg "INFO" ""
log_msg "INFO" "=========================================="
log_msg "INFO" "TASK 1.1 VERIFICATION SUMMARY"
log_msg "INFO" "=========================================="
log_msg "INFO" ""
log_msg "INFO" "✅ All required components generated:"
log_msg "INFO" "  - SSH keys directory: $KEY_DIR"
log_msg "INFO" "  - SSH config: $SSH_CONFIG"
log_msg "INFO" "  - Helper scripts: add-vm-keys.sh, test-vm-keys.sh, remove-old-shared-keys.sh"
log_msg "INFO" ""
log_msg "INFO" "Next Steps:"
log_msg "INFO" "  1. Review generated keys: ls -la $KEY_DIR/"
log_msg "INFO" "  2. Review SSH config: cat $SSH_CONFIG"
log_msg "INFO" "  3. Run QC checklist: cat $QC_CHECKLIST"
log_msg "INFO" "  4. Proceed to Task 1.2 (deploy keys to VMs)"
log_msg "INFO" ""
log_msg "SUCCESS" "✅ Task 1.1 Complete"

echo ""
echo "QC Checklist saved to: $QC_CHECKLIST"
echo ""
cat "$QC_CHECKLIST"
