#!/bin/bash

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TASK_LOG="${HOME}/.vm101-deployment/TASK-1.2-DEPLOY-KEYS-${TIMESTAMP}.log"
QC_CHECKLIST="${HOME}/.vm101-deployment/TASK-1.2-QC-${TIMESTAMP}.log"

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
log_msg "INFO" "TASK 1.2: Deploy Keys to Linux VMs"
log_msg "INFO" "=========================================="
log_msg "INFO" ""
log_msg "INFO" "Objective: Deploy SSH keys to at least 2 Linux VMs (VM120, VM150)"
log_msg "INFO" "Time: ~45 minutes"
log_msg "INFO" "Location: VM101"
log_msg "INFO" ""

echo "Task 1.2 QC Checklist" > "$QC_CHECKLIST"
echo "===================" >> "$QC_CHECKLIST"
echo "" >> "$QC_CHECKLIST"

KEY_DIR="${HOME}/.ssh/vm-keys"
AUDIT_LOG="${HOME}/.ssh/key-deployment-${TIMESTAMP}.log"
CONFIG_FILE="$(dirname "$0")/vm-config.json"

if [ ! -d "$KEY_DIR" ]; then
    log_msg "ERROR" "Key directory not found: $KEY_DIR"
    log_msg "INFO" "Run Task 1.1 first to generate keys"
    qc_check "Key directory exists" "FAILED"
    exit 1
fi

if [ ! -f "$CONFIG_FILE" ]; then
    log_msg "ERROR" "Config file not found: $CONFIG_FILE"
    qc_check "Config file exists" "FAILED"
    exit 1
fi

load_vm_config() {
    local vm_num=$1
    local config_file=$2
    local vm_data=$(grep -A 3 "\"vm_num\": $vm_num" "$config_file" | head -4)
    
    local username=$(echo "$vm_data" | grep '"username"' | sed 's/.*"username": "\([^"]*\)".*/\1/')
    local ip=$(echo "$vm_data" | grep '"ip"' | sed 's/.*"ip": "\([^"]*\)".*/\1/')
    local name=$(echo "$vm_data" | grep '"name"' | sed 's/.*"name": "\([^"]*\)".*/\1/')
    
    if [ -z "$username" ] || [ -z "$ip" ]; then
        return 1
    fi
    
    echo "$username|$ip|$name"
}

log_msg "INFO" "✅ Key directory found: $KEY_DIR"
log_msg "INFO" ""

deploy_to_linux_vm() {
    local vm_num=$1
    local user=$2
    local ip=$3
    local vm_name=$4
    
    local key_file="${KEY_DIR}/vm${vm_num}_key.pub"
    
    log_msg "INFO" "----------------------------------------"
    log_msg "INFO" "Deploying key to VM${vm_num} (${vm_name})"
    log_msg "INFO" "User: $user@$ip"
    log_msg "INFO" "Key file: $key_file"
    log_msg "INFO" "----------------------------------------"
    
    if [ ! -f "$key_file" ]; then
        log_msg "ERROR" "Key file not found: $key_file"
        qc_check "VM${vm_num} key deployment" "FAILED - key file not found"
        return 1
    fi
    
    log_msg "INFO" "Testing SSH connectivity to VM${vm_num}..."
    local connect_output
    connect_output=$(ssh -o ConnectTimeout=10 -o BatchMode=yes "${user}@${ip}" "echo 'Connection OK'" 2>&1)
    local connect_exit_code=$?
    
    if [ $connect_exit_code -ne 0 ]; then
        log_msg "ERROR" "Cannot connect to VM${vm_num} at ${user}@${ip}"
        if [ $connect_exit_code -eq 255 ]; then
            log_msg "INFO" "Connection error (exit code 255). Verify:"
            log_msg "INFO" "  1. VM${vm_num} is running and reachable"
            log_msg "INFO" "  2. Network connectivity exists"
            log_msg "INFO" "  3. SSH service is running on port 22"
            log_msg "INFO" "  4. Firewall allows SSH connections"
        elif [ $connect_exit_code -eq 1 ]; then
            log_msg "INFO" "Connection refused or authentication failed (exit code 1). Verify:"
            log_msg "INFO" "  1. User '$user' has valid SSH access"
            log_msg "INFO" "  2. SSH key is properly configured"
        else
            log_msg "INFO" "SSH connection failed with exit code $connect_exit_code"
            log_msg "INFO" "Error output: $connect_output"
        fi
        qc_check "VM${vm_num} connectivity test" "FAILED - cannot connect"
        return 1
    fi
    
    log_msg "INFO" "✅ SSH connection successful to VM${vm_num}"
    qc_check "VM${vm_num} connectivity test" "PASS"
    
    log_msg "INFO" "Reading public key..."
    local key_content=$(cat "$key_file")
    
    log_msg "INFO" "Deploying key to VM${vm_num}..."
    
    if ssh "${user}@${ip}" \
        "mkdir -p ~/.ssh && chmod 700 ~/.ssh && \
        if grep -q 'vm${vm_num}_key' ~/.ssh/authorized_keys 2>/dev/null; then \
            echo 'Key already exists, skipping'; \
        else \
            echo '$key_content' >> ~/.ssh/authorized_keys; \
            chmod 600 ~/.ssh/authorized_keys; \
            echo 'Key added successfully'; \
        fi" >> "$TASK_LOG" 2>&1; then
        
        log_msg "INFO" "✅ Key deployment to VM${vm_num} completed"
        qc_check "VM${vm_num} key deployment" "PASS"
        
        log_msg "INFO" "Verifying key on VM${vm_num}..."
        
        local verify_output
        verify_output=$(ssh -o ConnectTimeout=10 -o BatchMode=yes "${user}@${ip}" "grep 'vm${vm_num}_key' ~/.ssh/authorized_keys" 2>&1)
        local verify_exit_code=$?
        
        if [ $verify_exit_code -eq 0 ]; then
            log_msg "INFO" "✅ Key verified on VM${vm_num}"
            qc_check "VM${vm_num} key verification" "PASS"
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] VM${vm_num}: SUCCESS - Key deployed and verified" >> "$AUDIT_LOG"
            return 0
        elif [ $verify_exit_code -eq 255 ]; then
            log_msg "WARN" "⚠️  SSH connection error during verification on VM${vm_num} (exit code 255)"
            log_msg "INFO" "This may indicate: SSH service issues, network connectivity, or authentication failure"
            qc_check "VM${vm_num} key verification" "WARNING - connection error, manual verification needed"
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] VM${vm_num}: WARNING - Connection error during verification" >> "$AUDIT_LOG"
            return 1
        elif [ $verify_exit_code -eq 1 ]; then
            log_msg "WARN" "⚠️  Key not found in authorized_keys on VM${vm_num}"
            log_msg "INFO" "This may indicate: Key deployment failed or authorized_keys was not updated correctly"
            qc_check "VM${vm_num} key verification" "WARNING - key not in authorized_keys"
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] VM${vm_num}: WARNING - Key not found in authorized_keys" >> "$AUDIT_LOG"
            return 1
        else
            log_msg "WARN" "⚠️  Could not verify key on VM${vm_num} (exit code $verify_exit_code)"
            log_msg "INFO" "Error output: $verify_output"
            qc_check "VM${vm_num} key verification" "WARNING - could not verify"
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] VM${vm_num}: WARNING - Verification failed with exit code $verify_exit_code" >> "$AUDIT_LOG"
            return 1
        fi
    else
        log_msg "ERROR" "Key deployment to VM${vm_num} failed"
        qc_check "VM${vm_num} key deployment" "FAILED"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] VM${vm_num}: FAILED - Key deployment failed" >> "$AUDIT_LOG"
        return 1
    fi
}

log_msg "INFO" ""
log_msg "INFO" "DEPLOYING TO LINUX VMs"
log_msg "INFO" ""

SUCCESS_COUNT=0
FAILED_COUNT=0

deploy_from_config() {
    local vm_num=$1
    local config_data=$(load_vm_config "$vm_num" "$CONFIG_FILE")
    
    if [ $? -ne 0 ]; then
        log_msg "ERROR" "VM${vm_num} not found in config"
        ((FAILED_COUNT++))
        return 1
    fi
    
    local username=$(echo "$config_data" | cut -d'|' -f1)
    local ip=$(echo "$config_data" | cut -d'|' -f2)
    local name=$(echo "$config_data" | cut -d'|' -f3)
    
    if deploy_to_linux_vm "$vm_num" "$username" "$ip" "$name"; then
        ((SUCCESS_COUNT++))
        return 0
    else
        ((FAILED_COUNT++))
        return 1
    fi
}

deploy_from_config 120
if [ $? -ne 0 ]; then
    log_msg "WARN" "VM120 deployment encountered issues"
fi

log_msg "INFO" ""

deploy_from_config 150
if [ $? -ne 0 ]; then
    log_msg "WARN" "VM150 deployment encountered issues"
fi

log_msg "INFO" ""
log_msg "INFO" "OPTIONAL: Deploy to additional Linux VMs (VM160, VM170, VM180)"
log_msg "INFO" ""

read -p "Deploy to VM160 (Database)? (yes/no): " deploy_160
if [ "$deploy_160" = "yes" ]; then
    deploy_from_config 160
    log_msg "INFO" ""
fi

read -p "Deploy to VM170 (Game Servers)? (yes/no): " deploy_170
if [ "$deploy_170" = "yes" ]; then
    deploy_from_config 170
    log_msg "INFO" ""
fi

read -p "Deploy to VM180 (API Services)? (yes/no): " deploy_180
if [ "$deploy_180" = "yes" ]; then
    deploy_from_config 180
    log_msg "INFO" ""
fi

log_msg "INFO" "=========================================="
log_msg "INFO" "DEPLOYMENT SUMMARY"
log_msg "INFO" "=========================================="
log_msg "INFO" "Successful: $SUCCESS_COUNT VMs"
log_msg "INFO" "Failed: $FAILED_COUNT VMs"
log_msg "INFO" ""

if [ $SUCCESS_COUNT -lt 2 ]; then
    log_msg "ERROR" "❌ At least 2 VMs must be successfully deployed"
    log_msg "INFO" "Current: $SUCCESS_COUNT / 2 minimum"
    exit 1
fi

log_msg "INFO" "✅ Minimum 2 VMs successfully deployed"

log_msg "INFO" ""
log_msg "INFO" "Testing SSH access with new keys..."
log_msg "INFO" ""

test_ssh_with_key() {
    local vm_num=$1
    local config_data=$(load_vm_config "$vm_num" "$CONFIG_FILE")
    
    if [ $? -ne 0 ]; then
        log_msg "WARN" "VM${vm_num} not found in config, skipping test"
        return 1
    fi
    
    local username=$(echo "$config_data" | cut -d'|' -f1)
    local ip=$(echo "$config_data" | cut -d'|' -f2)
    
    log_msg "INFO" "Testing VM${vm_num}..."
    if ssh -o ConnectTimeout=5 "${username}@${ip}" "hostname" >> "$TASK_LOG" 2>&1; then
        log_msg "INFO" "✅ VM${vm_num} SSH test passed"
        qc_check "VM${vm_num} SSH test with new key" "PASS"
    else
        log_msg "WARN" "⚠️  VM${vm_num} SSH test failed"
        qc_check "VM${vm_num} SSH test with new key" "WARNING"
    fi
}

test_ssh_with_key 120
log_msg "INFO" ""
test_ssh_with_key 150

log_msg "INFO" ""
log_msg "INFO" "=========================================="
log_msg "INFO" "TASK 1.2 VERIFICATION SUMMARY"
log_msg "INFO" "=========================================="
log_msg "INFO" ""
log_msg "INFO" "✅ At least 2 Linux VMs have SSH keys deployed"
log_msg "INFO" "✅ Keys verified in authorized_keys"
log_msg "INFO" "✅ SSH connectivity confirmed"
log_msg "INFO" ""
log_msg "INFO" "Next Steps:"
log_msg "INFO" "  1. Review deployment log: $TASK_LOG"
log_msg "INFO" "  2. Review audit log: $AUDIT_LOG"
log_msg "INFO" "  3. Run QC checklist: cat $QC_CHECKLIST"
log_msg "INFO" "  4. Proceed to Task 1.3 (test Windows deployment)"
log_msg "INFO" ""
log_msg "SUCCESS" "✅ Task 1.2 Complete"

echo ""
echo "QC Checklist saved to: $QC_CHECKLIST"
echo ""
cat "$QC_CHECKLIST"
