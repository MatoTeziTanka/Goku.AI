<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔑 VM101 SSH Key Setup for Failed VMs

**Status:** 3/7 VMs accessible, 4 VMs need SSH key setup  
**Date:** November 23, 2025

---

## ✅ Currently Accessible VMs

- ✅ **VM100** (GOKU-AI) - Administrator@<VM100_IP>
- ✅ **VM120** (reverse-proxy-gateway) - proxy1@<VM120_IP>
- ✅ **VM150** (wordpress-1) - wp1@<VM150_IP>

---

## ❌ VMs Needing SSH Key Setup

- ❌ **VM160** - dbs1@<VM160_IP>
- ❌ **VM170** - gsh1@<VM170_IP>
- ❌ **VM180** - apis1@<VM180_IP>
- ❌ **VM200** - Administrator@<VM200_IP> (Windows)

---

## 🔧 Setup Instructions

### **Step 1: Get Your Public Key**

**On VM101:**
```bash
# Display your public key
cat ~/.ssh/id_ed25519.pub

# Or copy to clipboard (if xclip available)
cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard
```

**Your public key should look like:**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIL4D2F2vYoyxZor/tUYMokLP7MWoU2tTe5o22XdVb5p9 vm101
```

---

### **Step 2: Add Key to Linux VMs (160, 170, 180)**

**For each VM (160, 170, 180), SSH in with password first:**

```bash
# VM160
ssh dbs1@<VM160_IP>
# Enter password when prompted

# Once connected, add the key:
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIL4D2F2vYoyxZor/tUYMokLP7MWoU2tTe5o22XdVb5p9 vm101" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
exit

# Repeat for VM170
ssh gsh1@<VM170_IP>
# ... same commands ...

# Repeat for VM180
ssh apis1@<VM180_IP>
# ... same commands ...
```

**Or use ssh-copy-id (if password auth works):**
```bash
# From VM101
ssh-copy-id dbs1@<VM160_IP>
ssh-copy-id gsh1@<VM170_IP>
ssh-copy-id apis1@<VM180_IP>
```

---

### **Step 3: Add Key to Windows VM (200)**

**VM200 is Windows, so use RDP or Windows SSH:**

**Option A: Via RDP**
1. RDP to <VM200_IP>
2. Open PowerShell or Command Prompt
3. Create `.ssh` directory: `mkdir C:\Users\Administrator\.ssh`
4. Add key to `C:\Users\Administrator\.ssh\authorized_keys`
5. Set permissions: `icacls C:\Users\Administrator\.ssh\authorized_keys /inheritance:r /grant Administrator:F`

**Option B: Via SSH (if Windows SSH server allows password auth)**
```bash
# From VM101, try password auth first
ssh Administrator@<VM200_IP>
# Enter password, then add key manually
```

**Option C: Manual Copy**
```bash
# From VM101, copy key to Windows VM
scp ~/.ssh/id_ed25519.pub Administrator@<VM200_IP>:C:/Users/Administrator/.ssh/
# Then SSH in and append to authorized_keys
```

---

## 🎯 Automated Setup Script

**Create this script on VM101:**

```bash
cat > ~/setup-ssh-keys.sh << 'EOF'
#!/bin/bash
# SSH Key Setup Script for Failed VMs

PUBLIC_KEY=$(cat ~/.ssh/id_ed25519.pub)

echo "Your public key:"
echo "$PUBLIC_KEY"
echo ""
echo "========================================="
echo "SSH Key Setup Instructions"
echo "========================================="
echo ""
echo "For each failed VM, run these commands:"
echo ""
echo "VM160 (dbs1@<VM160_IP>):"
echo "  ssh dbs1@<VM160_IP>"
echo "  mkdir -p ~/.ssh && chmod 700 ~/.ssh"
echo "  echo '$PUBLIC_KEY' >> ~/.ssh/authorized_keys"
echo "  chmod 600 ~/.ssh/authorized_keys"
echo ""
echo "VM170 (gsh1@<VM170_IP>):"
echo "  ssh gsh1@<VM170_IP>"
echo "  mkdir -p ~/.ssh && chmod 700 ~/.ssh"
echo "  echo '$PUBLIC_KEY' >> ~/.ssh/authorized_keys"
echo "  chmod 600 ~/.ssh/authorized_keys"
echo ""
echo "VM180 (apis1@<VM180_IP>):"
echo "  ssh apis1@<VM180_IP>"
echo "  mkdir -p ~/.ssh && chmod 700 ~/.ssh"
echo "  echo '$PUBLIC_KEY' >> ~/.ssh/authorized_keys"
echo "  chmod 600 ~/.ssh/authorized_keys"
echo ""
echo "VM200 (Administrator@<VM200_IP> - Windows):"
echo "  Use RDP or Windows SSH to add key manually"
echo ""
EOF

chmod +x ~/setup-ssh-keys.sh
./setup-ssh-keys.sh
```

---

## ✅ Verify After Setup

**After adding keys, test again:**

```bash
# Quick test
for vm in "dbs1@<VM160_IP>:VM160" "gsh1@<VM170_IP>:VM170" "apis1@<VM180_IP>:VM180" "Administrator@<VM200_IP>:VM200"; do
  IFS=':' read -r userhost name <<< "$vm"
  echo -n "$name: "
  timeout 5 ssh -o ConnectTimeout=3 -o BatchMode=yes $userhost "hostname" 2>/dev/null && echo "✅ OK" || echo "❌ FAILED"
done
```

---

## 📝 Notes

- **Password:** If you need the password for these VMs, it's likely `Norelec7!` (universal password)
- **Windows SSH:** VM200 may need Windows SSH server configured differently
- **Firewall:** Ensure port 22 is open on all VMs
- **Key Type:** Using ED25519 key (most secure, recommended)

---

**After setup, all VMs should be accessible via SSH from VM101!**




