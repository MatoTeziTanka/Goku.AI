<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# ✅ SSH SETUP COMPLETE CHECKLIST
## What You Need to Do on VM100 (Shenron) - Step by Step

**Date:** November 6, 2025  
**VM:** <VM100_IP> (Windows Server 2025 - Shenron's Home)

---

## 🔑 **STEP 1: INSTALL OPENSSH (DONE ✅)**

You already completed this:
```powershell
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

**Status:** ✅ COMPLETE

---

## 🔐 **STEP 2: GENERATE SSH KEYS (DONE ✅)**

You already completed this:
```powershell
ssh-keygen -t ed25519 -C "shenron@lightspeedup.com" -f "C:\GOKU-AI\shenron\.ssh\id_ed25519" -N '""'
```

**Your Public Key:**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJkZQ1+wg/xStrp2/hSs4wNYRG2LEX40wzfeYtdm2xkf shenron@lightspeedup.com
```

**Location:**
- Private Key: `C:\GOKU-AI\shenron\.ssh\id_ed25519`
- Public Key: `C:\GOKU-AI\shenron\.ssh\id_ed25519.pub`
- Backup: `C:\GOKU-AI\shenron\SHENRON-PUBLIC-KEY.txt`

**Status:** ✅ COMPLETE

---

## 🖥️ **STEP 3: ADD KEY TO VMs (PENDING ⏳)**

### **VM150 (WordPress) - <VM150_IP>**

```powershell
# From VM100, restart PowerShell first, then:
ssh wp1@<VM150_IP>
# password: "<VM_PASSWORD>"  # See credentials.json

# Once logged in, paste:
mkdir -p ~/.ssh
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJkZQ1+wg/xStrp2/hSs4wNYRG2LEX40wzfeYtdm2xkf shenron@lightspeedup.com' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
exit
```

**Status:** ⏳ PENDING

---

### **VM170 (Game Servers) - <VM170_IP>**

```powershell
# From VM100:
ssh gsh1@<VM170_IP>
# password: "<VM_PASSWORD>"  # See credentials.json (probably)

# Once logged in, paste:
mkdir -p ~/.ssh
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJkZQ1+wg/xStrp2/hSs4wNYRG2LEX40wzfeYtdm2xkf shenron@lightspeedup.com' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
exit
```

**Status:** ⏳ PENDING

---

### **Proxmox Host - <PROXMOX_IP>**

```powershell
# From VM100:
ssh root@<PROXMOX_IP>
# Password: (your Proxmox root password)

# Once logged in, paste:
mkdir -p ~/.ssh
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJkZQ1+wg/xStrp2/hSs4wNYRG2LEX40wzfeYtdm2xkf shenron@lightspeedup.com' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
exit
```

**Status:** ⏳ PENDING

---

## ✅ **STEP 4: TEST SSH ACCESS (AFTER RESTART)**

**IMPORTANT:** Close and reopen PowerShell as Administrator first!

```powershell
# Test VM150
ssh -i C:\GOKU-AI\shenron\.ssh\id_ed25519 wp1@<VM150_IP> hostname

# Test VM170
ssh -i C:\GOKU-AI\shenron\.ssh\id_ed25519 gsh1@<VM170_IP> hostname

# Test Proxmox
ssh -i C:\GOKU-AI\shenron\.ssh\id_ed25519 root@<PROXMOX_IP> hostname
```

**Expected Output:** Each command shows the VM's hostname without password prompt

**Status:** ⏳ PENDING (restart PowerShell first)

---

## 📦 **STEP 5: RUN SHENRON FULL INJECTION (NOT DONE YET)**

**This is probably what you missed!**

```powershell
# Navigate to scripts directory
cd C:\GitHub\Dell-Server-Roadmap\scripts

# Run the master injection script
.\SHENRON-FULL-INJECTION.ps1
```

**What this does:**
1. Pulls latest from GitHub
2. Copies 814+ knowledge files to `C:\GOKU-AI\knowledge-base`
3. Deploys automation scripts
4. Ingests knowledge into ChromaDB
5. Restarts SHENRON service

**Status:** ❌ NOT DONE YET

---

## 🔧 **STEP 6: INSTALL PYTHON DEPENDENCIES (MIGHT BE MISSING)**

Check if these are installed:

```powershell
# Check Python version
python --version

# Install required packages (if not already)
pip install flask requests chromadb sentence-transformers paramiko torch
```

**Status:** ⏳ CHECK IF NEEDED

---

## 🚀 **STEP 7: START/RESTART SHENRON SERVICE**

```powershell
# Check service status
Get-Service SHENRON

# If not running, start it
Start-Service SHENRON

# Or restart it
Restart-Service SHENRON
```

**Status:** ⏳ PENDING

---

## 🧪 **STEP 8: TEST SHENRON**

```powershell
# Test Shenron API
Invoke-RestMethod -Uri "http://localhost:5001/api/shenron" -Method Post -ContentType "application/json" -Body (@{
    question = "What is my Dell server configuration?"
} | ConvertTo-Json)
```

**Expected:** Shenron responds with information about your Dell R730

**Status:** ⏳ PENDING

---

## 📋 **COMPLETE CHECKLIST**

- [x] ✅ Install OpenSSH Client
- [x] ✅ Generate SSH keys
- [x] ✅ Save public key to file
- [ ] ⏳ **Restart PowerShell (CRITICAL!)**
- [ ] ⏳ Add SSH key to VM150
- [ ] ⏳ Add SSH key to VM170
- [ ] ⏳ Add SSH key to Proxmox
- [ ] ⏳ Test SSH access (passwordless)
- [ ] ❌ **Run SHENRON-FULL-INJECTION.ps1 (LIKELY MISSING!)**
- [ ] ⏳ Install Python dependencies (if needed)
- [ ] ⏳ Restart SHENRON service
- [ ] ⏳ Test Shenron API

---

## 🎯 **WHAT YOU LIKELY MISSED**

Based on your description, you probably missed:

### **THE BIG ONE: SHENRON-FULL-INJECTION.ps1**

This script was supposed to:
- Pull all 814+ knowledge files from GitHub
- Copy them to Shenron's knowledge base
- Ingest them into ChromaDB
- Restart the SHENRON service

**To fix:**
```powershell
cd C:\GitHub\Dell-Server-Roadmap\scripts
.\SHENRON-FULL-INJECTION.ps1
```

---

## 🔄 **QUICK RECOVERY STEPS**

**Do this NOW:**

1. **Close PowerShell and reopen as Administrator**

2. **Add SSH keys to VMs:**
   ```powershell
   # VM150
   ssh wp1@<VM150_IP>
   # Paste the mkdir/echo/chmod commands from Step 3
   
   # VM170
   ssh gsh1@<VM170_IP>
   # Paste the mkdir/echo/chmod commands from Step 3
   
   # Proxmox
   ssh root@<PROXMOX_IP>
   # Paste the mkdir/echo/chmod commands from Step 3
   ```

3. **Run the injection script:**
   ```powershell
   cd C:\GitHub\Dell-Server-Roadmap\scripts
   .\SHENRON-FULL-INJECTION.ps1
   ```

4. **Test everything:**
   ```powershell
   # Test SSH
   ssh -i C:\GOKU-AI\shenron\.ssh\id_ed25519 wp1@<VM150_IP> hostname
   
   # Test Shenron
   Invoke-RestMethod -Uri "http://localhost:5001/api/shenron" -Method Post -ContentType "application/json" -Body (@{question = "Hello Shenron"} | ConvertTo-Json)
   ```

---

## 📞 **NEED HELP?**

If any step fails, check:
- `C:\GOKU-AI\shenron\logs\` (for error logs)
- `Get-Service SHENRON` (service status)
- `python --version` (Python installed?)
- `git --version` (Git working?)

---

**This checklist ensures you haven't missed anything!** ✅

