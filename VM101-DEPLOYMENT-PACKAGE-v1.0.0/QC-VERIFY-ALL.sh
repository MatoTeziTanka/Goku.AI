#!/bin/bash

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
VERIFICATION_LOG="${HOME}/.vm101-deployment/QC-VERIFICATION-${TIMESTAMP}.log"
REPORT="${HOME}/.vm101-deployment/QC-REPORT-${TIMESTAMP}.json"

mkdir -p "${HOME}/.vm101-deployment"

log_msg() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$VERIFICATION_LOG"
}

print_header() {
    cat <<'EOF'

╔════════════════════════════════════════════════════════════════════╗
║              ZENCODER v1.0.0 QC VERIFICATION                       ║
║                                                                    ║
║  This script verifies all deployment components are working        ║
║  Expected duration: ~10 minutes                                    ║
╚════════════════════════════════════════════════════════════════════╝

EOF
}

print_header

log_msg "Starting QC Verification"
log_msg "Timestamp: $TIMESTAMP"
log_msg ""

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

check_item() {
    local name=$1
    local command=$2
    
    if eval "$command" >> "$VERIFICATION_LOG" 2>&1; then
        echo "✅ PASS: $name"
        ((PASS_COUNT++))
        return 0
    else
        echo "❌ FAIL: $name"
        ((FAIL_COUNT++))
        return 1
    fi
}

warn_item() {
    local name=$1
    echo "⚠️  WARN: $name"
    ((WARN_COUNT++))
}

log_msg ""
log_msg "VERIFICATION CHECKS"
log_msg "==================="
log_msg ""

log_msg "1. SSH KEY VERIFICATION"
check_item "Key directory exists" "[ -d ${HOME}/.ssh/vm-keys ]"
check_item "SSH config exists" "[ -f ${HOME}/.ssh/config ]"
check_item "Key permissions correct" "find ${HOME}/.ssh/vm-keys -name 'vm*_key' -perm 600 | wc -l | grep -q [1-9]"

log_msg ""
log_msg "2. HELPER SCRIPTS VERIFICATION"
check_item "add-vm-keys.sh exists" "[ -f ${HOME}/add-vm-keys.sh ]"
check_item "test-vm-keys.sh exists" "[ -f ${HOME}/test-vm-keys.sh ]"
check_item "remove-old-shared-keys.sh exists" "[ -f ${HOME}/remove-old-shared-keys.sh ]"

log_msg ""
log_msg "3. SERVICE VERIFICATION"
check_item "Docker installed" "command -v docker"
check_item "Docker running" "docker ps > /dev/null 2>&1"
check_item "Git installed" "command -v git"
check_item "Python3 installed" "command -v python3"

log_msg ""
log_msg "4. SSH ALIAS TEST"

test_ssh_alias() {
    ssh -o ConnectTimeout=3 -o BatchMode=yes $1 "echo OK" > /dev/null 2>&1
}

if test_ssh_alias "vm120-proxy"; then
    echo "✅ PASS: SSH to vm120-proxy"
    ((PASS_COUNT++))
else
    warn_item "SSH to vm120-proxy (may require manual setup)"
fi

if test_ssh_alias "vm150-wordpress"; then
    echo "✅ PASS: SSH to vm150-wordpress"
    ((PASS_COUNT++))
else
    warn_item "SSH to vm150-wordpress (may require manual setup)"
fi

if test_ssh_alias "vm100-goku"; then
    echo "✅ PASS: SSH to vm100-goku"
    ((PASS_COUNT++))
else
    warn_item "SSH to vm100-goku (Windows, may require manual setup)"
fi

log_msg ""
log_msg "5. LOGGING VERIFICATION"
check_item "Deployment logs exist" "[ -d ${HOME}/.vm101-deployment ]"
check_item "Monitoring directory exists" "[ -d ${HOME}/.vm101-deployment/monitoring ]"

log_msg ""
log_msg "6. FILE INTEGRITY CHECK"
check_item "SSH config readable" "[ -r ${HOME}/.ssh/config ]"
check_item "Keys directory readable" "[ -r ${HOME}/.ssh/vm-keys ]"

log_msg ""
log_msg "=========================================="
log_msg "QC VERIFICATION SUMMARY"
log_msg "=========================================="
log_msg ""
log_msg "RESULTS:"
echo "  ✅ PASS: $PASS_COUNT"
echo "  ⚠️  WARN: $WARN_COUNT"
echo "  ❌ FAIL: $FAIL_COUNT"
log_msg ""

if [ $FAIL_COUNT -eq 0 ]; then
    log_msg "✅ ALL CRITICAL CHECKS PASSED"
    if [ $WARN_COUNT -gt 0 ]; then
        log_msg "⚠️  $WARN_COUNT warnings (review logs for details)"
    fi
else
    log_msg "❌ CRITICAL FAILURES DETECTED"
    log_msg "Review logs and fix issues before proceeding"
fi

log_msg ""
log_msg "Verification Log: $VERIFICATION_LOG"
log_msg "Timestamp: $(date)"

echo ""
echo "Full verification log: $VERIFICATION_LOG"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    exit 0
else
    exit 1
fi
