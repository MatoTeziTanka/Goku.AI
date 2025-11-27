<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
#!/bin/bash
# VM101 Separate SSH Keys Per VM - Security Setup
# This script creates separate SSH keys for each VM to prevent cross-VM access

set -e  # Exit on error

echo "🔐 VM101 Separate SSH Keys Setup"
echo "=================================="
echo ""
echo "This will:"
echo "  1. Generate separate SSH keys for each VM"
echo "  2. Create SSH config to use specific keys"
echo "  3. Display public keys to add to each VM"
echo "  4. Remove old shared keys from VMs (manual step)"
echo ""

# Create directory for VM-specific keys
KEY_DIR="$HOME/.ssh/vm-keys"
mkdir -p "$KEY_DIR"
chmod 700 "$KEY_DIR"

# VMs configuration
declare -A VMS
VMS[100]="Administrator@<VM100_IP>:Windows"
VMS[120]="proxy1@<VM120_IP>:Linux"
VMS[150]="wp1@<VM150_IP>:Linux"
VMS[160]="dbs1@<VM160_IP>:Linux"
VMS[170]="gsh1@<VM170_IP>:Linux"
VMS[180]="apis1@<VM180_IP>:Linux"
VMS[200]="Administrator@<VM200_IP>:Windows"

echo "📝 Step 1: Generating separate keys for each VM..."
echo ""

# Generate keys for each VM
for vm_num in "${!VMS[@]}"; do
    IFS=':' read -r user_host os_type <<< "${VMS[$vm_num]}"
    key_file="$KEY_DIR/vm${vm_num}_key"
    
    if [ -f "$key_file" ]; then
        echo "  ⚠️  Key for VM${vm_num} already exists, skipping..."
    else
        echo "  🔑 Generating key for VM${vm_num} ($user_host)..."
        ssh-keygen -t ed25519 -C "vm101-to-vm${vm_num}-$(date +%Y%m%d)" \
            -f "$key_file" -N "" -q
        chmod 600 "$key_file"
        chmod 644 "${key_file}.pub"
    fi
done

echo ""
echo "✅ Keys generated in: $KEY_DIR"
echo ""

# Create SSH config
echo "📝 Step 2: Creating SSH config..."
SSH_CONFIG="$HOME/.ssh/config"

# Backup existing SSH keys and config before migration
echo "📝 Step 1.5: Backing up existing SSH keys and config..."
BACKUP_DIR="$HOME/.ssh/backup-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
if [ -f "$SSH_CONFIG" ]; then
    cp "$SSH_CONFIG" "$BACKUP_DIR/config"
    echo "  💾 Backed up SSH config"
fi
if [ -f "$HOME/.ssh/id_rsa" ]; then
    cp "$HOME/.ssh/id_rsa"* "$BACKUP_DIR/" 2>/dev/null || true
    echo "  💾 Backed up existing RSA keys"
fi
if [ -f "$HOME/.ssh/id_ed25519" ]; then
    cp "$HOME/.ssh/id_ed25519"* "$BACKUP_DIR/" 2>/dev/null || true
    echo "  💾 Backed up existing ED25519 keys"
fi
echo "  ✅ Backup complete: $BACKUP_DIR"
echo "  ⚠️  IMPORTANT: Store this backup securely outside VM101!"
echo ""

# Create new SSH config
cat > "$SSH_CONFIG" << 'EOF'
# VM101 Separate SSH Keys Configuration
# Each VM uses a unique key for security isolation
# Generated: $(date)

EOF

for vm_num in "${!VMS[@]}"; do
    IFS=':' read -r user_host os_type <<< "${VMS[$vm_num]}"
    IFS='@' read -r user hostname <<< "$user_host"
    
    # Determine hostname based on VM number
    case $vm_num in
        100) host_alias="vm100-goku" ;;
        120) host_alias="vm120-proxy" ;;
        150) host_alias="vm150-wordpress" ;;
        160) host_alias="vm160-database" ;;
        170) host_alias="vm170-gameservers" ;;
        180) host_alias="vm180-apiservices" ;;
        200) host_alias="vm200-plex" ;;
        *) host_alias="vm${vm_num}" ;;
    esac
    
    cat >> "$SSH_CONFIG" << EOF
# VM${vm_num} - ${os_type}
# Usage: ssh ${host_alias} "command"
Host ${host_alias}
    HostName ${hostname}
    User ${user}
    IdentityFile ~/.ssh/vm-keys/vm${vm_num}_key
    IdentitiesOnly yes
    StrictHostKeyChecking yes
    UserKnownHostsFile ~/.ssh/known_hosts
    ServerAliveInterval 60
    ServerAliveCountMax 3
    ConnectTimeout 10

EOF
done

chmod 600 "$SSH_CONFIG"
echo "✅ SSH config created: $SSH_CONFIG"
echo ""

# Display public keys for each VM
echo "📋 Step 3: Public keys to add to each VM"
echo "=========================================="
echo ""
echo "⚠️  IMPORTANT: Add ONLY the VM-specific key to each VM's authorized_keys"
echo "   Remove the old shared keys (id_rsa, id_ed25519) after testing!"
echo ""

for vm_num in "${!VMS[@]}"; do
    IFS=':' read -r user_host os_type <<< "${VMS[$vm_num]}"
    key_file="$KEY_DIR/vm${vm_num}_key.pub"
    
    echo "--- VM${vm_num} ($user_host) ---"
    echo "Key file: $key_file"
    cat "$key_file"
    echo ""
done

# Create add-keys script
echo "📝 Step 4: Creating helper script to add keys..."
ADD_KEYS_SCRIPT="$HOME/add-vm-keys.sh"
cat > "$ADD_KEYS_SCRIPT" << 'SCRIPT_EOF'
#!/bin/bash
# Helper script to add VM-specific keys to each VM
# Run this AFTER you've verified the keys work

set -e

KEY_DIR="$HOME/.ssh/vm-keys"
AUDIT_LOG="$HOME/.ssh/key-deployment.log"

log_action() {
    local vm=$1
    local status=$2
    local message=$3
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] VM${vm}: ${status} - ${message}" >> "$AUDIT_LOG"
}

echo "🔐 Adding VM-specific keys to each VM..."
echo "📋 Logging to: $AUDIT_LOG"
echo ""

# VM100 (Windows)
echo "Adding key to VM100..."
if cat "$KEY_DIR/vm100_key.pub" | ssh Administrator@<VM100_IP> \
    'powershell -Command "$key = [Console]::In.ReadLine(); $sshDir = \"C:\\Users\\Administrator\\.ssh\"; if (!(Test-Path $sshDir)) { New-Item -ItemType Directory -Path $sshDir -Force | Out-Null }; Add-Content -Path \"$sshDir\\authorized_keys\" -Value $key; icacls \"$sshDir\\authorized_keys\" /inheritance:r /grant \"Administrator:F\" | Out-Null"'; then
    log_action "100" "SUCCESS" "SSH key deployed"
    echo "  ✅ Key added to VM100"
else
    log_action "100" "FAILURE" "SSH key deployment failed"
    echo "  ❌ Failed to add key to VM100"
fi

# VM120 (Linux)
echo "Adding key to VM120..."
KEY_CONTENT=$(cat "$KEY_DIR/vm120_key.pub")
if ssh proxy1@<VM120_IP> \
    "mkdir -p ~/.ssh && chmod 700 ~/.ssh && \
    if grep -q '$KEY_CONTENT' ~/.ssh/authorized_keys 2>/dev/null; then \
        echo '  ℹ️  Key already exists, skipping'; \
    else \
        echo '$KEY_CONTENT' >> ~/.ssh/authorized_keys; \
        chmod 600 ~/.ssh/authorized_keys; \
        echo '  ✅ Key added'; \
    fi && \
    stat -c 'Permissions: %a' ~/.ssh/authorized_keys"; then
    log_action "120" "SUCCESS" "SSH key processed"
else
    log_action "120" "FAILURE" "SSH key deployment failed"
    echo "  ❌ Failed to add key to VM120"
fi

# VM150 (Linux)
echo "Adding key to VM150..."
KEY_CONTENT=$(cat "$KEY_DIR/vm150_key.pub")
if ssh wp1@<VM150_IP> \
    "mkdir -p ~/.ssh && chmod 700 ~/.ssh && \
    if grep -q '$KEY_CONTENT' ~/.ssh/authorized_keys 2>/dev/null; then \
        echo '  ℹ️  Key already exists, skipping'; \
    else \
        echo '$KEY_CONTENT' >> ~/.ssh/authorized_keys; \
        chmod 600 ~/.ssh/authorized_keys; \
        echo '  ✅ Key added'; \
    fi && \
    stat -c 'Permissions: %a' ~/.ssh/authorized_keys"; then
    log_action "150" "SUCCESS" "SSH key processed"
else
    log_action "150" "FAILURE" "SSH key deployment failed"
    echo "  ❌ Failed to add key to VM150"
fi

# VM160 (Linux) - if accessible
echo "Adding key to VM160..."
if ssh -o ConnectTimeout=15 dbs1@<VM160_IP> "echo 'Connected'" 2>/dev/null; then
    KEY_CONTENT=$(cat "$KEY_DIR/vm160_key.pub")
    if ssh dbs1@<VM160_IP> \
        "mkdir -p ~/.ssh && chmod 700 ~/.ssh && \
        if grep -q '$KEY_CONTENT' ~/.ssh/authorized_keys 2>/dev/null; then \
            echo '  ℹ️  Key already exists, skipping'; \
        else \
            echo '$KEY_CONTENT' >> ~/.ssh/authorized_keys; \
            chmod 600 ~/.ssh/authorized_keys; \
            echo '  ✅ Key added'; \
        fi && \
        stat -c 'Permissions: %a' ~/.ssh/authorized_keys"; then
        log_action "160" "SUCCESS" "SSH key processed"
    else
        log_action "160" "FAILURE" "SSH key deployment failed"
        echo "  ❌ Failed to add key to VM160"
    fi
else
    log_action "160" "WARNING" "VM not accessible, manual deployment needed"
    echo "  ⚠️  VM160 not accessible, add key manually"
fi

# VM170 (Linux) - if accessible
echo "Adding key to VM170..."
if ssh -o ConnectTimeout=15 gsh1@<VM170_IP> "echo 'Connected'" 2>/dev/null; then
    KEY_CONTENT=$(cat "$KEY_DIR/vm170_key.pub")
    if ssh gsh1@<VM170_IP> \
        "mkdir -p ~/.ssh && chmod 700 ~/.ssh && \
        if grep -q '$KEY_CONTENT' ~/.ssh/authorized_keys 2>/dev/null; then \
            echo '  ℹ️  Key already exists, skipping'; \
        else \
            echo '$KEY_CONTENT' >> ~/.ssh/authorized_keys; \
            chmod 600 ~/.ssh/authorized_keys; \
            echo '  ✅ Key added'; \
        fi && \
        stat -c 'Permissions: %a' ~/.ssh/authorized_keys"; then
        log_action "170" "SUCCESS" "SSH key processed"
    else
        log_action "170" "FAILURE" "SSH key deployment failed"
        echo "  ❌ Failed to add key to VM170"
    fi
else
    log_action "170" "WARNING" "VM not accessible, manual deployment needed"
    echo "  ⚠️  VM170 not accessible, add key manually"
fi

# VM180 (Linux) - if accessible
echo "Adding key to VM180..."
if ssh -o ConnectTimeout=15 apis1@<VM180_IP> "echo 'Connected'" 2>/dev/null; then
    KEY_CONTENT=$(cat "$KEY_DIR/vm180_key.pub")
    if ssh apis1@<VM180_IP> \
        "mkdir -p ~/.ssh && chmod 700 ~/.ssh && \
        if grep -q '$KEY_CONTENT' ~/.ssh/authorized_keys 2>/dev/null; then \
            echo '  ℹ️  Key already exists, skipping'; \
        else \
            echo '$KEY_CONTENT' >> ~/.ssh/authorized_keys; \
            chmod 600 ~/.ssh/authorized_keys; \
            echo '  ✅ Key added'; \
        fi && \
        stat -c 'Permissions: %a' ~/.ssh/authorized_keys"; then
        log_action "180" "SUCCESS" "SSH key processed"
    else
        log_action "180" "FAILURE" "SSH key deployment failed"
        echo "  ❌ Failed to add key to VM180"
    fi
else
    log_action "180" "WARNING" "VM not accessible, manual deployment needed"
    echo "  ⚠️  VM180 not accessible, add key manually"
fi

# VM200 (Windows) - if accessible
echo "Adding key to VM200..."
if ssh -o ConnectTimeout=15 Administrator@<VM200_IP> "echo 'Connected'" 2>/dev/null; then
    if cat "$KEY_DIR/vm200_key.pub" | ssh Administrator@<VM200_IP> \
        'powershell -Command "$key = [Console]::In.ReadLine(); $sshDir = \"C:\\Users\\Administrator\\.ssh\"; if (!(Test-Path $sshDir)) { New-Item -ItemType Directory -Path $sshDir -Force | Out-Null }; Add-Content -Path \"$sshDir\\authorized_keys\" -Value $key; icacls \"$sshDir\\authorized_keys\" /inheritance:r /grant \"Administrator:F\" | Out-Null"'; then
        log_action "200" "SUCCESS" "SSH key deployed"
        echo "  ✅ Key added to VM200"
    else
        log_action "200" "FAILURE" "SSH key deployment failed"
        echo "  ❌ Failed to add key to VM200"
    fi
else
    log_action "200" "WARNING" "VM not accessible, manual deployment needed"
    echo "  ⚠️  VM200 not accessible, add key manually"
fi

echo ""
echo "✅ Keys added! Now test with: ssh vm120-proxy 'hostname'"
SCRIPT_EOF

chmod +x "$ADD_KEYS_SCRIPT"
echo "✅ Helper script created: $ADD_KEYS_SCRIPT"
echo ""

# Create test script
echo "📝 Step 5: Creating test script..."
TEST_SCRIPT="$HOME/test-vm-keys.sh"
cat > "$TEST_SCRIPT" << 'TEST_EOF'
#!/bin/bash
# Test SSH access using new separate keys

echo "🧪 Testing SSH access with new keys..."
echo ""

declare -A VMS
VMS[100]="vm100-goku"
VMS[120]="vm120-proxy"
VMS[150]="vm150-wordpress"
VMS[160]="vm160-database"
VMS[170]="vm170-gameservers"
VMS[180]="vm180-apiservices"
VMS[200]="vm200-plex"

for vm_num in "${!VMS[@]}"; do
    host_alias="${VMS[$vm_num]}"
    echo -n "Testing ${host_alias} (VM${vm_num}): "
    
    if ssh -o ConnectTimeout=5 -o BatchMode=yes "$host_alias" "hostname" 2>/dev/null; then
        echo "✅ OK"
    else
        echo "❌ FAILED"
    fi
done

echo ""
echo "✅ Testing complete!"
TEST_EOF

chmod +x "$TEST_SCRIPT"
echo "✅ Test script created: $TEST_SCRIPT"
echo ""

# Create cleanup script
echo "📝 Step 6: Creating cleanup script (remove old shared keys)..."
CLEANUP_SCRIPT="$HOME/remove-old-shared-keys.sh"
cat > "$CLEANUP_SCRIPT" << 'CLEANUP_EOF'
#!/bin/bash
# Remove old shared SSH keys from VMs
# Run this AFTER you've verified new keys work

echo "🧹 Removing old shared keys from VMs..."
echo "⚠️  This will remove id_rsa and id_ed25519 keys from authorized_keys"
echo ""
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

# Get old key fingerprints
OLD_RSA_KEY=$(ssh-keygen -lf ~/.ssh/id_rsa.pub 2>/dev/null | awk '{print $2}')
OLD_ED25519_KEY=$(ssh-keygen -lf ~/.ssh/id_ed25519.pub 2>/dev/null | awk '{print $2}')

echo "Old RSA key fingerprint: $OLD_RSA_KEY"
echo "Old ED25519 key fingerprint: $OLD_ED25519_KEY"
echo ""

# Remove from Linux VMs
for vm in "proxy1@<VM120_IP>" "wp1@<VM150_IP>"; do
    echo "Removing old keys from $vm..."
    ssh "$vm" "sed -i '/$OLD_RSA_KEY/d; /$OLD_ED25519_KEY/d' ~/.ssh/authorized_keys"
done

echo ""
echo "✅ Old keys removed from Linux VMs"
echo "⚠️  For Windows VMs (VM100, VM200), remove keys manually via RDP or PowerShell"
CLEANUP_EOF

chmod +x "$CLEANUP_SCRIPT"
echo "✅ Cleanup script created: $CLEANUP_SCRIPT"
echo ""

echo "=========================================="
echo "✅ Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "  1. Review the public keys above"
echo "  2. Run: ./add-vm-keys.sh (or add keys manually)"
echo "  3. Test: ./test-vm-keys.sh"
echo "  4. After verification, run: ./remove-old-shared-keys.sh"
echo ""
echo "🔐 Security Notes:"
echo "  - Each VM now has a unique key"
echo "  - If one key is compromised, only one VM is at risk"
echo "  - Remove old shared keys after testing"
echo "  - Use SSH aliases: ssh vm120-proxy, ssh vm150-wordpress, etc."
echo ""


