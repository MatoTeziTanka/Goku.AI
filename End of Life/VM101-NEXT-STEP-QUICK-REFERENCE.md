<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🎯 VM101 Migration - Next Step Quick Reference

**Current Status:** Step 1 ✅ COMPLETE (Backup created)  
**Next Step:** Step 2 - Generate Per-VM SSH Keys  
**Date:** November 23, 2025

---

## ✅ STEP 1: COMPLETE

**Backup Created:**
- ✅ File: `vzdump-qemu-101-2025_11_23-05_52_32.vma.gz`
- ✅ Size: 19.94 GB
- ✅ Location: `/var/lib/vz/dump/` on Proxmox

---

## 🎯 STEP 2: GENERATE PER-VM SSH KEYS (DO THIS NOW)

**What to do:** Run the SSH key generation script on VM101

### **On VM101:**

```bash
# 1. Navigate to script location
cd ~/GitHub

# 2. Verify script exists
ls -la VM101-SEPARATE-KEYS-SETUP.sh

# 3. Make executable (if needed)
chmod +x VM101-SEPARATE-KEYS-SETUP.sh

# 4. Run the script
./VM101-SEPARATE-KEYS-SETUP.sh
```

**What the script does:**
- Generates 7 unique SSH keys (one per VM)
- Creates keys in `~/.ssh/vm-keys/` directory
- Creates SSH config entries for easy access
- Displays public keys to add to each VM

**Expected Output:**
```
🔐 VM101 Separate SSH Keys Setup
==================================
📝 Step 1: Generating separate keys for each VM...
  🔑 Generating key for VM100 (Administrator@<VM100_IP>)...
  🔑 Generating key for VM120 (proxy1@<VM120_IP>)...
  ... (and so on for all 7 VMs)

📋 Step 3: Public keys to add to each VM
--- VM100 (Administrator@<VM100_IP>) ---
ssh-ed25519 AAAAC3... vm101-to-vm100-20251123
...
```

**After script completes:**
- ✅ 7 new key pairs created in `~/.ssh/vm-keys/`
- ✅ SSH config updated with aliases
- ✅ Public keys displayed (copy these for Step 3)

---

## ⏭️ WHAT COMES AFTER STEP 2

**Step 3:** Deploy keys to all VMs (add public keys to authorized_keys)  
**Step 4:** Verify SSH connectivity  
**Step 5:** Backup repositories, ChromaDB, knowledge base  
**... (continue through Step 10)**

**Step 13a (Much Later):** SSH 2FA setup (that's when you'll use the bypass config)

---

## 📝 ABOUT THE 2FA BYPASS CONFIG

**That config is for Step 13a (much later):**
```bash
# /etc/security/access-2fa-bypass.conf
+ : ALL : 192.168.12.77  # Your PC - bypass 2FA
- : ALL : ALL            # Everything else requires 2FA
```

**When to use it:**
- After Steps 2-10 are complete
- After SSH keys are deployed and working
- When setting up 2FA (Step 13a)
- This allows your PC (192.168.12.77) to bypass 2FA while VM101 requires it

**Don't create this file yet** - it's part of the 2FA setup, not the SSH key migration.

---

## 🚀 QUICK START: STEP 2

**Right now, on VM101, run:**

```bash
cd ~/GitHub
chmod +x VM101-SEPARATE-KEYS-SETUP.sh
./VM101-SEPARATE-KEYS-SETUP.sh
```

**Then follow the script's output** - it will tell you what to do next (copy public keys to each VM).

---

**See:** `VM101-MIGRATION-EXECUTION-GUIDE.md` for complete Step 2 instructions




