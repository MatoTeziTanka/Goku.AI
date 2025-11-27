<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔐 VM101 Separate SSH Keys Migration Guide

**Security Goal:** One key per VM - no shared keys  
**Risk Mitigation:** If one VM is compromised, others remain secure  
**Status:** Ready to execute

---

## 🎯 Current Situation

**Current Setup:**
- ✅ VM101 has multiple keys: `id_rsa`, `id_ed25519`, `shenron_key`, `vm100_shenron`
- ⚠️ **Currently using `id_rsa` for ALL VMs** (VM100, VM120, VM150)
- ⚠️ VM120 and VM150 have multiple keys in `authorized_keys`:
  - GitHub-imported key (MatoTeziTanka)
  - VM101 ed25519 key
  - **Shared id_rsa key** (mgmt1@vm101-management) ← **SECURITY RISK**

**Problem:**
- If `id_rsa` is compromised, attacker has access to ALL VMs
- If any VM is compromised, attacker could extract the shared key

**Solution:**
- Generate separate key for each VM
- Each VM only has ONE key in `authorized_keys`
- VM101 uses different key for each VM via SSH config

---

## 📋 Migration Steps

### **Step 1: Run Setup Script**

```bash
# Make script executable
chmod +x ~/VM101-SEPARATE-KEYS-SETUP.sh

# Run setup (generates keys, creates SSH config)
~/VM101-SEPARATE-KEYS-SETUP.sh
```

**What it does:**
- Creates `~/.ssh/vm-keys/` directory
- Generates separate ed25519 key for each VM (VM100, VM120, VM150, VM160, VM170, VM180, VM200)
- Creates `~/.ssh/config` with VM-specific key mappings
- Creates helper scripts for adding keys and testing

### **Step 2: Add Keys to Each VM**

**Option A: Use Helper Script (for accessible VMs)**

```bash
# Run the helper script
~/add-vm-keys.sh
```

**Option B: Manual (for Windows VMs or if script fails)**

**For Linux VMs (VM120, VM150, VM160, VM170, VM180):**
```bash
# Display the key
cat ~/.ssh/vm-keys/vm120_key.pub

# Add to VM (replace with correct VM number and user)
cat ~/.ssh/vm-keys/vm120_key.pub | ssh proxy1@<VM120_IP> \
    "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

**For Windows VMs (VM100, VM200):**
```bash
# Display the key
cat ~/.ssh/vm-keys/vm100_key.pub

# Copy the key, then on Windows VM (via RDP or existing SSH):
# PowerShell:
$key = "PASTE_PUBLIC_KEY_HERE"
$sshDir = "C:/Users/Administrator/.ssh"
if (!(Test-Path $sshDir)) { New-Item -ItemType Directory -Path $sshDir }
Add-Content -Path "$sshDir/authorized_keys" -Value $key
```

### **Step 3: Test New Keys**

```bash
# Test using SSH config aliases
~/test-vm-keys.sh

# Or test manually:
ssh vm120-proxy "hostname"
ssh vm150-wordpress "hostname"
ssh vm100-goku "hostname"
```

**Expected Output:**
```
Testing vm100-goku (VM100): ✅ OK
Testing vm120-proxy (VM120): ✅ OK
Testing vm150-wordpress (VM150): ✅ OK
...
```

### **Step 4: Remove Old Shared Keys**

**⚠️ IMPORTANT: Only do this AFTER verifying new keys work!**

```bash
# Review what will be removed
~/remove-old-shared-keys.sh
```

**Manual Removal (if script doesn't work):**

**For Linux VMs:**
```bash
# SSH to VM and remove old keys
ssh proxy1@<VM120_IP> "sed -i '/mgmt1@vm101-management/d' ~/.ssh/authorized_keys"
ssh wp1@<VM150_IP> "sed -i '/mgmt1@vm101-management/d' ~/.ssh/authorized_keys"
```

**For Windows VMs:**
```powershell
# Via RDP or existing SSH, edit C:/Users/Administrator/.ssh/authorized_keys
# Remove lines containing:
# - mgmt1@vm101-management
# - Any other shared keys
```

---

## 🔍 Verification

### **Check SSH Config**

```bash
cat ~/.ssh/config
```

**Should show:**
```
Host vm100-goku
    HostName <VM100_IP>
    User Administrator
    IdentityFile ~/.ssh/vm-keys/vm100_key
    IdentitiesOnly yes
...
```

### **Check Which Key is Used**

```bash
# Verbose SSH to see which key is used
ssh -v vm120-proxy "hostname" 2>&1 | grep -E "identity file|Offering.*key"
```

**Should show:**
```
debug1: identity file /home/mgmt1/.ssh/vm-keys/vm120_key type 3
```

### **Check Authorized Keys on Each VM**

```bash
# Linux VMs
ssh vm120-proxy "cat ~/.ssh/authorized_keys"
ssh vm150-wordpress "cat ~/.ssh/authorized_keys"

# Should only show ONE key (the VM-specific one)
```

---

## 🛡️ Security Benefits

**Before (Shared Key):**
- ❌ One key (`id_rsa`) on all VMs
- ❌ If VM101 compromised → all VMs accessible
- ❌ If any VM compromised → key extracted → all VMs accessible

**After (Separate Keys):**
- ✅ Each VM has unique key
- ✅ If VM101 compromised → attacker has keys, but can rotate
- ✅ If one VM compromised → only that VM at risk
- ✅ Can revoke individual keys without affecting others

---

## 📁 File Structure

```
~/.ssh/
├── config                    # SSH config with VM-specific keys
├── vm-keys/                  # Directory for VM-specific keys
│   ├── vm100_key             # Private key for VM100
│   ├── vm100_key.pub         # Public key for VM100
│   ├── vm120_key             # Private key for VM120
│   ├── vm120_key.pub         # Public key for VM120
│   └── ...                   # (one key pair per VM)
├── id_rsa                    # OLD - Remove after migration
├── id_rsa.pub                # OLD - Remove after migration
└── id_ed25519                # Keep for other purposes (if needed)

~/add-vm-keys.sh              # Helper script to add keys
~/test-vm-keys.sh             # Test script
~/remove-old-shared-keys.sh   # Cleanup script
```

---

## 🚨 Troubleshooting

### **SSH Connection Refused**

```bash
# Check if key is added to VM
ssh vm120-proxy "cat ~/.ssh/authorized_keys | grep -c vm120_key"

# Check key permissions
ls -la ~/.ssh/vm-keys/
# Should be: -rw------- (600) for private keys
# Should be: -rw-r--r-- (644) for public keys
```

### **Wrong Key Being Used**

```bash
# Check SSH config
cat ~/.ssh/config | grep -A 5 "vm120-proxy"

# Force specific key
ssh -i ~/.ssh/vm-keys/vm120_key proxy1@<VM120_IP> "hostname"
```

### **Key Already Exists**

```bash
# If key already exists, script will skip it
# To regenerate:
rm ~/.ssh/vm-keys/vm120_key*
# Then re-run setup script
```

---

## ✅ Post-Migration Checklist

- [ ] All VMs have unique keys in `~/.ssh/vm-keys/`
- [ ] SSH config created with VM aliases
- [ ] Keys added to all VMs' `authorized_keys`
- [ ] Tested SSH access to all VMs using new keys
- [ ] Old shared keys removed from all VMs
- [ ] Verified each VM only has ONE key in `authorized_keys`
- [ ] Updated any automation scripts to use new SSH aliases
- [ ] Documented key locations and rotation procedures

---

## 🔄 Key Rotation (Future)

**To rotate a key for a specific VM:**

```bash
# 1. Generate new key
ssh-keygen -t ed25519 -C "vm101-to-vm120-rotated-$(date +%Y%m%d)" \
    -f ~/.ssh/vm-keys/vm120_key_new -N ""

# 2. Add new key to VM
cat ~/.ssh/vm-keys/vm120_key_new.pub | ssh vm120-proxy \
    "cat >> ~/.ssh/authorized_keys"

# 3. Test new key
ssh -i ~/.ssh/vm-keys/vm120_key_new vm120-proxy "hostname"

# 4. Update SSH config to use new key
# Edit ~/.ssh/config, change IdentityFile to vm120_key_new

# 5. Remove old key from VM
ssh vm120-proxy "sed -i '/OLD_KEY_FINGERPRINT/d' ~/.ssh/authorized_keys"

# 6. Replace old key file
mv ~/.ssh/vm-keys/vm120_key ~/.ssh/vm-keys/vm120_key.old
mv ~/.ssh/vm-keys/vm120_key_new ~/.ssh/vm-keys/vm120_key
```

---

## ⏰ Automated Key Rotation Schedule

**Setup automatic key rotation every 90 days:**

```bash
# 1. Create rotation script
cat > ~/rotate-vm-keys.sh << 'ROTATE_SCRIPT'
#!/bin/bash
# Automated SSH key rotation script
# Rotates keys every 90 days

set -e

KEY_DIR="$HOME/.ssh/vm-keys"
AUDIT_LOG="$HOME/.ssh/key-rotation.log"
ROTATION_DAYS=90

rotate_key() {
    local vm=$1
    local vm_user=$2
    local vm_ip=$3
    
    KEY_FILE="$KEY_DIR/vm${vm}_key"
    CURRENT_KEY_AGE=$(find "$KEY_FILE" -mtime +$ROTATION_DAYS -print)
    
    if [ ! -z "$CURRENT_KEY_AGE" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting rotation for VM${vm}..." >> "$AUDIT_LOG"
        
        # Generate new key
        ssh-keygen -t ed25519 -C "vm101-to-vm${vm}-rotated-$(date +%Y%m%d)" \
            -f "${KEY_FILE}_new" -N "" -q
        
        # Add new key to VM
        ssh -o ConnectTimeout=15 "${vm_user}@${vm_ip}" \
            "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys" < "${KEY_FILE}_new.pub"
        
        # Test new key
        if ssh -i "${KEY_FILE}_new" -o ConnectTimeout=5 "${vm_user}@${vm_ip}" "hostname" >/dev/null 2>&1; then
            # Update SSH config
            sed -i "s|IdentityFile ~/.ssh/vm-keys/vm${vm}_key|IdentityFile ~/.ssh/vm-keys/vm${vm}_key_new|" ~/.ssh/config
            
            # Remove old key from VM
            OLD_FINGERPRINT=$(ssh-keygen -lf "$KEY_FILE" 2>/dev/null | awk '{print $2}' | tr ':' '-')
            ssh "${vm_user}@${vm_ip}" "grep -v '$OLD_FINGERPRINT' ~/.ssh/authorized_keys > /tmp/ak && mv /tmp/ak ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys" || true
            
            # Replace old key
            mv "$KEY_FILE" "${KEY_FILE}.old"
            mv "${KEY_FILE}_new" "$KEY_FILE"
            mv "${KEY_FILE}_new.pub" "${KEY_FILE}.pub"
            
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Successfully rotated VM${vm} key" >> "$AUDIT_LOG"
        else
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAILED to rotate VM${vm} key" >> "$AUDIT_LOG"
            rm "${KEY_FILE}_new"*
        fi
    fi
}

# Rotate all VM keys
rotate_key 100 Administrator <VM100_IP>
rotate_key 120 proxy1 <VM120_IP>
rotate_key 150 wp1 <VM150_IP>
rotate_key 160 dbs1 <VM160_IP>
rotate_key 170 gsh1 <VM170_IP>
rotate_key 180 apis1 <VM180_IP>
rotate_key 200 Administrator <VM200_IP>

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Key rotation cycle complete" >> "$AUDIT_LOG"
ROTATE_SCRIPT

chmod +x ~/rotate-vm-keys.sh
```

# 2. Add to crontab for automatic execution
```bash
crontab -e

# Add this line to run rotation on the 1st of every 3 months
0 2 1 */3 * /home/mgmt1/rotate-vm-keys.sh
```

# 3. Monitor rotation with
```bash
tail -f ~/.ssh/key-rotation.log
```

---

**Security is now significantly improved! Each VM is isolated with its own key.** 🔐




