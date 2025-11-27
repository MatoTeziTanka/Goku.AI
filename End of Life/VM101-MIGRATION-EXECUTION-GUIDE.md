<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🚀 VM101 MIGRATION EXECUTION GUIDE

**Created:** November 23, 2025  
**Purpose:** Step-by-step execution guide for VM101 migration to control node  
**Status:** Ready to Execute

---

## ⚠️ PRE-FLIGHT CHECKLIST

Before starting, verify:
- [x] ✅ VM101 is fully operational
- [x] ✅ All repositories synced with GitHub
- [x] ✅ SSH access to VM100, VM120, VM150 working
- [x] ✅ Proxmox web interface accessible (https://<PROXMOX_IP>:8006)
- [x] ✅ You have root/administrator access to Proxmox host
- [x] ✅ Backup storage location identified

---

## 📋 STEP 1: BACKUP VM101 (PRE-MIGRATION) ✅ **COMPLETED**

**Purpose:** Create a restore point before making changes

**⚠️ IMPORTANT:** VM101 has VFIO device (GPU passthrough) - snapshots fail, use backup instead.

### **✅ Backup Completed (November 23, 2025)**

**Backup Details:**
- **File:** `vzdump-qemu-101-2025_11_23-05_52_32.vma.gz`
- **Location:** `/var/lib/vz/dump/` on Proxmox host
- **Size:** 19.94 GB (compressed from 500 GB)
- **Duration:** 48 minutes 22 seconds
- **Status:** ✅ Successfully completed

**VFIO Device:**
- `hostpci0: 0000:86:00,pcie=1,x-vga=1` (GPU passthrough)

**Command Used:**
```bash
# On Proxmox host
vzdump 101 --mode stop --storage local --compress gzip
```

**✅ Verification:**
- [x] Backup file exists: `/var/lib/vz/dump/vzdump-qemu-101-2025_11_23-05_52_32.vma.gz`
- [x] Backup size: 19.94 GB
- [x] Backup completed successfully
- [x] VM101 can now be safely modified

**See:** `VM101-BACKUP-COMPLETED.md` for full details

**⏱️ Time Taken:** 48 minutes 22 seconds

---

## 📋 STEP 2: GENERATE PER-VM SSH KEYS

**Purpose:** Create unique SSH keys for each VM (replacing shared `id_rsa`)

### **On VM101:**
```bash
# Navigate to script location
cd ~/GitHub

# Verify script exists
ls -la VM101-SEPARATE-KEYS-SETUP.sh

# Review script contents (optional)
cat VM101-SEPARATE-KEYS-SETUP.sh

# Make executable (if needed)
chmod +x VM101-SEPARATE-KEYS-SETUP.sh

# Run the script
./VM101-SEPARATE-KEYS-SETUP.sh
```

**What the script does:**
- Generates unique SSH keys for each VM in `~/.ssh/vm-keys/`:
  - `vm100_key` → VM100 (Windows)
  - `vm120_key` → VM120 (Ubuntu)
  - `vm150_key` → VM150 (Ubuntu)
  - `vm160_key` → VM160 (Ubuntu)
  - `vm170_key` → VM170 (Ubuntu)
  - `vm180_key` → VM180 (Ubuntu)
  - `vm200_key` → VM200 (Windows)
- Creates SSH config entries for easy access
- Backs up existing keys
- Displays public keys to add to each VM

**✅ Verification:**
```bash
# Check new keys were created
ls -la ~/.ssh/vm-keys/

# Should see 7 new key pairs (14 files total)
# Example output:
# vm100_key
# vm100_key.pub
# vm120_key
# vm120_key.pub
# ... (and so on)

# Check SSH config was updated
cat ~/.ssh/config | grep -A 3 "Host vm"
```

**Expected Output:**
```
Host vm100
    HostName <VM100_IP>
    User Administrator
    IdentityFile ~/.ssh/id_ed25519_vm100
    IdentitiesOnly yes
...
```

**⏱️ Estimated Time:** 2-3 minutes

---

## 📋 STEP 3: DEPLOY KEYS TO ALL VMs

**Purpose:** Add new SSH public keys to each VM's authorized_keys

### **For VM100 (Windows Server 2025):**

```bash
# On VM101, copy the public key
cat ~/.ssh/vm-keys/vm100_key.pub

# Copy the output, then on VM100 (via RDP or existing SSH):
# 1. Open PowerShell as Administrator
# 2. Create .ssh directory if it doesn't exist:
New-Item -ItemType Directory -Force -Path C:\Users\Administrator\.ssh

# 3. Add the public key to authorized_keys:
Add-Content -Path C:\Users\Administrator\.ssh\authorized_keys -Value "PASTE_PUBLIC_KEY_HERE"

# 4. Set permissions:
icacls C:\Users\Administrator\.ssh\authorized_keys /inheritance:r
icacls C:\Users\Administrator\.ssh\authorized_keys /grant "Administrator:F"
```

### **For VM120, VM150, VM160, VM170, VM180 (Ubuntu):**

```bash
# On VM101, for each VM, run:
# VM120
ssh-copy-id -i ~/.ssh/vm-keys/vm120_key.pub proxy1@<VM120_IP>

# VM150
ssh-copy-id -i ~/.ssh/vm-keys/vm150_key.pub wp1@<VM150_IP>

# VM160
ssh-copy-id -i ~/.ssh/vm-keys/vm160_key.pub dbs1@<VM160_IP>

# VM170
ssh-copy-id -i ~/.ssh/vm-keys/vm170_key.pub gsh1@<VM170_IP>

# VM180
ssh-copy-id -i ~/.ssh/vm-keys/vm180_key.pub apis1@<VM180_IP>
```

**Alternative (Manual) for VMs without existing SSH access:**
```bash
# On VM101, get the public key
cat ~/.ssh/vm-keys/vm160_key.pub

# Then manually add to VM160 (via console or existing method):
# On VM160:
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "PASTE_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### **For VM200 (Windows):**
Same process as VM100 (Windows Server)

**✅ Verification (After Each Deployment):**
```bash
# Test SSH connection with new key
ssh -i ~/.ssh/id_ed25519_vm120 proxy1@<VM120_IP> "hostname"
ssh -i ~/.ssh/id_ed25519_vm150 wp1@<VM150_IP> "hostname"
# ... (test each VM)

# Or use SSH config aliases (if configured):
ssh vm120 "hostname"
ssh vm150 "hostname"
```

**Expected Output:**
```
reverse-proxy-gateway
wordpress-1
...
```

**⏱️ Estimated Time:** 10-20 minutes (depending on manual steps)

---

## 📋 STEP 4: VERIFY SSH CONNECTIVITY

**Purpose:** Ensure all VMs are accessible with new keys

### **Create Verification Script:**
```bash
# On VM101, create test script
cat > ~/test-ssh-access.sh << 'EOF'
#!/bin/bash
echo "🔍 Testing SSH Access to All VMs..."
echo "===================================="
echo ""

VMs=(
    "vm100:Administrator@<VM100_IP>"
    "vm120:proxy1@<VM120_IP>"
    "vm150:wp1@<VM150_IP>"
    "vm160:dbs1@<VM160_IP>"
    "vm170:gsh1@<VM170_IP>"
    "vm180:apis1@<VM180_IP>"
    "vm200:Administrator@<VM200_IP>"
)

for vm_entry in "${VMs[@]}"; do
    IFS=':' read -r vm_name vm_userhost <<< "$vm_entry"
    echo -n "Testing $vm_name ($vm_userhost)... "
    
    if ssh -i ~/.ssh/vm-keys/${vm_name}_key -o ConnectTimeout=5 -o StrictHostKeyChecking=no \
       ${vm_userhost} "hostname" 2>/dev/null; then
        echo "✅ SUCCESS"
    else
        echo "❌ FAILED"
    fi
done

echo ""
echo "✅ Verification complete!"
EOF

chmod +x ~/test-ssh-access.sh
./test-ssh-access.sh
```

**✅ Expected Output:**
```
🔍 Testing SSH Access to All VMs...
====================================

Testing vm100 (Administrator@<VM100_IP>)... ✅ SUCCESS
Testing vm120 (proxy1@<VM120_IP>)... ✅ SUCCESS
Testing vm150 (wp1@<VM150_IP>)... ✅ SUCCESS
Testing vm160 (dbs1@<VM160_IP>)... ✅ SUCCESS
Testing vm170 (gsh1@<VM170_IP>)... ✅ SUCCESS
Testing vm180 (apis1@<VM180_IP>)... ✅ SUCCESS
Testing vm200 (Administrator@<VM200_IP>)... ✅ SUCCESS

✅ Verification complete!
```

**⏱️ Estimated Time:** 2-3 minutes

---

## 📋 STEP 5: BACKUP REPOSITORIES, CHROMADB, AND KNOWLEDGE BASE

**Purpose:** Create backups before migration changes

### **5a. Backup ChromaDB from VM100:**

```bash
# On VM101, create backup directory
mkdir -p ~/backups/chromadb-$(date +%Y%m%d)

# Copy ChromaDB from VM100
scp -i ~/.ssh/vm-keys/vm100_key \
    -r Administrator@<VM100_IP>:"C:/GOKU-AI/chroma_db" \
    ~/backups/chromadb-$(date +%Y%m%d)/

# Verify backup
du -sh ~/backups/chromadb-$(date +%Y%m%d)/
ls -la ~/backups/chromadb-$(date +%Y%m%d)/
```

### **5b. Backup Knowledge Base Files:**

```bash
# On VM101, backup knowledge base
mkdir -p ~/backups/knowledge-base-$(date +%Y%m%d)

# Copy knowledge base files from VM100
scp -i ~/.ssh/vm-keys/vm100_key \
    -r Administrator@<VM100_IP>:"C:/GOKU-AI/shenron/knowledge-base" \
    ~/backups/knowledge-base-$(date +%Y%m%d)/ 2>/dev/null || \
scp -i ~/.ssh/vm-keys/vm100_key \
    -r Administrator@<VM100_IP>:"C:/GOKU-AI/knowledge-base" \
    ~/backups/knowledge-base-$(date +%Y%m%d)/ 2>/dev/null || \
echo "⚠️ Knowledge base location not found, skipping..."
```

### **5c. Backup Repository Snapshots:**

```bash
# On VM101, create repository backup (already synced with GitHub, but local snapshot)
mkdir -p ~/backups/repos-$(date +%Y%m%d)

# Create tarball of Dell-Server-Roadmap (most important)
cd ~/GitHub
tar -czf ~/backups/repos-$(date +%Y%m%d)/Dell-Server-Roadmap-backup.tar.gz \
    Dell-Server-Roadmap/

# Verify backup
ls -lh ~/backups/repos-$(date +%Y%m%d)/
```

**✅ Verification:**
```bash
# Check all backups exist
ls -lh ~/backups/
du -sh ~/backups/*/
```

**⏱️ Estimated Time:** 10-30 minutes (depending on data size)

---

## 📋 STEP 6: STOP PYTHON HTTP SERVER (PORT 8080)

**Purpose:** Free up port 8080 if needed (code-server is on 9001, so optional)

### **Check if Python HTTP server is running:**
```bash
# On VM101
ps aux | grep "python3 -m http.server 8080"
```

### **Stop it if running:**
```bash
# Find and stop the process
pkill -f "python3 -m http.server 8080"

# Verify it's stopped
ps aux | grep "python3 -m http.server 8080"
# Should return nothing (or just the grep command itself)
```

**✅ Verification:**
```bash
# Check port 8080 is free
sudo ss -tlnp | grep :8080
# Should return nothing
```

**⏱️ Estimated Time:** 1 minute

---

## 📋 STEP 7: VERIFY SERVICES AFTER KEY CHANGES

**Purpose:** Ensure all services still work after SSH key migration

### **7a. Verify Docker:**
```bash
# On VM101
sudo systemctl status docker
docker ps
docker run hello-world
```

**Expected:** Docker running, containers accessible

### **7b. Verify code-server:**
```bash
# On VM101
sudo systemctl status code-server
curl -I http://localhost:9001
```

**Expected:** Service active, web interface accessible

### **7c. Verify FastAPI Backend:**
```bash
# On VM101
ps aux | grep uvicorn
curl http://localhost:8001/health 2>/dev/null || curl http://localhost:8001/ 2>/dev/null
```

**Expected:** Process running, API responds

**✅ Verification Checklist:**
- [ ] Docker service: Active (running)
- [ ] Docker containers: Accessible
- [ ] code-server: Active (running) on port 9001
- [ ] FastAPI backend: Running on port 8001
- [ ] All services respond to requests

**⏱️ Estimated Time:** 3-5 minutes

---

## 📋 STEP 8: REMOVE OLD SHARED KEYS

**Purpose:** Remove the old `id_rsa` key from all VMs for security

### **On Each VM (VM100, VM120, VM150, VM160, VM170, VM180, VM200):**

**For Ubuntu VMs:**
```bash
# On VM101, connect to each Ubuntu VM and remove old key
ssh vm120 "sed -i '/mgmt1@vm101-management/d' ~/.ssh/authorized_keys"
ssh vm150 "sed -i '/mgmt1@vm101-management/d' ~/.ssh/authorized_keys"
ssh vm160 "sed -i '/mgmt1@vm101-management/d' ~/.ssh/authorized_keys"
ssh vm170 "sed -i '/mgmt1@vm101-management/d' ~/.ssh/authorized_keys"
ssh vm180 "sed -i '/mgmt1@vm101-management/d' ~/.ssh/authorized_keys"
```

**For Windows VMs (VM100, VM200):**
```powershell
# On VM100/VM200 (via RDP or existing SSH):
# Open PowerShell as Administrator
# Remove old key from authorized_keys
(Get-Content C:\Users\Administrator\.ssh\authorized_keys) | 
    Where-Object { $_ -notmatch "mgmt1@vm101-management" } | 
    Set-Content C:\Users\Administrator\.ssh\authorized_keys
```

### **Verify Old Key No Longer Works:**
```bash
# On VM101, test old key (should fail)
ssh -i ~/.ssh/id_rsa proxy1@<VM120_IP> "hostname"
# Expected: Permission denied (publickey)

# Test new keys work (should succeed)
ssh -i ~/.ssh/vm-keys/vm120_key proxy1@<VM120_IP> "hostname"
# Expected: reverse-proxy-gateway
```

**✅ Verification:**
```bash
# Test old key fails on all VMs
for vm in "proxy1@<VM120_IP>" "wp1@<VM150_IP>"; do
    echo "Testing old key on $vm..."
    ssh -i ~/.ssh/id_rsa -o ConnectTimeout=5 $vm "hostname" 2>&1 | grep -q "Permission denied" && echo "✅ Old key rejected" || echo "❌ Old key still works!"
done
```

**⏱️ Estimated Time:** 5-10 minutes

---

## 📋 STEP 9: UPDATE SCRIPTS TO USE NEW KEYS

**Purpose:** Update automation scripts to use new per-VM keys

### **Locate Scripts:**
```bash
# On VM101
cd ~/GitHub/Dell-Server-Roadmap/scripts
ls -la *.sh
```

### **Update SSH Commands in Scripts:**

**Find scripts using SSH:**
```bash
# Find all scripts with SSH commands
grep -r "ssh.*@192.168.12" ~/GitHub/Dell-Server-Roadmap/scripts/
```

**Update each script to use new keys:**
```bash
# Example: Update script to use new key
# OLD: ssh proxy1@<VM120_IP> "command"
# NEW: ssh -i ~/.ssh/vm-keys/vm120_key proxy1@<VM120_IP> "command"

# Or use SSH config aliases (if configured by the script):
# OLD: ssh proxy1@<VM120_IP> "command"
# NEW: ssh vm120 "command"
```

### **Test Updated Scripts:**
```bash
# Test each script after updating
cd ~/GitHub/Dell-Server-Roadmap/scripts
./script-name.sh
```

**✅ Verification:**
- [ ] All scripts updated to use new keys
- [ ] Scripts tested and working
- [ ] No references to old `id_rsa` key in scripts

**⏱️ Estimated Time:** 15-30 minutes (depending on number of scripts)

---

## 📋 STEP 10: DOCUMENT VERIFICATION RESULTS

**Purpose:** Record migration completion and verification results

### **Create Verification Report:**
```bash
# On VM101
cat > ~/migration-verification-$(date +%Y%m%d).md << 'EOF'
# VM101 Migration Verification Report

**Date:** $(date +%Y-%m-%d)
**Migration Type:** SSH Key Separation & Control Node Setup

## SSH Access Verification

| VM | IP | User | Status | Notes |
|----|----|----|--------|-------|
| VM100 | <VM100_IP> | Administrator | ✅ | |
| VM120 | <VM120_IP> | proxy1 | ✅ | |
| VM150 | <VM150_IP> | wp1 | ✅ | |
| VM160 | <VM160_IP> | dbs1 | ✅ | |
| VM170 | <VM170_IP> | gsh1 | ✅ | |
| VM180 | <VM180_IP> | apis1 | ✅ | |
| VM200 | <VM200_IP> | Administrator | ✅ | |

## Service Status

- [ ] Docker: ✅ Running
- [ ] code-server: ✅ Running (port 9001)
- [ ] FastAPI Backend: ✅ Running (port 8001)

## Backups Created

- [ ] ChromaDB: ~/backups/chromadb-YYYYMMDD/
- [ ] Knowledge Base: ~/backups/knowledge-base-YYYYMMDD/
- [ ] Repositories: ~/backups/repos-YYYYMMDD/

## Issues Encountered

(None / List any issues here)

## Next Steps

- [ ] Update VM101-MIGRATION-SUMMARY.md
- [ ] Update VM101-SECURITY-VERIFICATION-RESULTS.md
- [ ] Test all automation scripts
- [ ] Schedule regular backups
EOF

cat ~/migration-verification-$(date +%Y%m%d).md
```

### **Update Main Documentation:**
```bash
# Update VM101-MIGRATION-SUMMARY.md with completion status
# (Edit manually or use script)
```

**✅ Final Checklist:**
- [ ] All 7 VMs accessible with new keys
- [ ] Old keys removed from all VMs
- [ ] All services running (Docker, code-server, FastAPI)
- [ ] Backups created and verified
- [ ] Scripts updated to use new keys
- [ ] Documentation updated
- [ ] Verification report created

**⏱️ Estimated Time:** 10-15 minutes

---

## 🎉 MIGRATION COMPLETE!

**Total Estimated Time:** 2-4 hours  
**Risk Level:** Low (with snapshot, all changes reversible)

### **Post-Migration Tasks:**
1. Monitor services for 24-48 hours
2. Test all automation scripts
3. Schedule regular backups
4. Update team documentation
5. Consider removing Proxmox snapshot after 1 week (if everything stable)

### **Rollback Procedure (If Needed):**
```bash
# Via Proxmox Web UI:
# VM 101 → Snapshots → vm101-pre-migration-YYYYMMDD → Rollback

# Or via CLI:
ssh root@<PROXMOX_IP>
qm rollback 101 vm101-pre-migration-YYYYMMDD
```

---

**Last Updated:** November 23, 2025  
**Status:** Ready for Execution

