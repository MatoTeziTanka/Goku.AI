<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔐 VM100 vs VM101 Security Isolation Analysis

**Critical Question:** If VM100 is compromised, can it use VM101 to access all VMs?

---

## 🎯 Architecture Security Model

### **Current Architecture:**

```
VM100 (AI Host - Windows)
├── LM Studio (port 1234)
├── SHENRON API (port 5000)
└── SSH Server (accepts connections)

VM101 (Control Node - Ubuntu)
├── SSH Client (initiates connections)
├── SSH Keys to ALL VMs
└── Management Scripts
```

### **Security Question:**

**If VM100 is compromised, can attacker:**
1. SSH to VM101? ❌ **Should NOT be possible**
2. Extract VM101's SSH keys? ❌ **Should NOT have access**
3. Use VM101 to access other VMs? ❌ **Should NOT be possible**

---

## 🛡️ Required Security Configuration

### **VM100 → VM101 Access: BLOCKED**

**VM100 should NOT have:**
- ❌ SSH keys to VM101
- ❌ SSH access to VM101
- ❌ Ability to control VM101
- ❌ Network access to VM101's SSH port (if possible)

**VM101 should:**
- ✅ Only accept SSH from authorized sources
- ✅ Use firewall to block VM100 SSH access (if desired)
- ✅ Use SSH key-based auth (no password)
- ✅ Have separate keys for each VM (already planned)

### **VM101 → VM100 Access: ALLOWED (One-Way)**

**VM101 should have:**
- ✅ SSH key to VM100 (for management)
- ✅ Ability to SSH to VM100
- ✅ Ability to manage VM100 services

**This is ONE-WAY:**
- VM101 → VM100: ✅ Allowed (control node manages AI host)
- VM100 → VM101: ❌ Blocked (AI host cannot control control node)

---

## 🔍 Verification Steps

### **Check if VM100 can SSH to VM101**

**On VM100 (Windows):**
```powershell
# Check if VM100 has SSH keys to VM101
dir C:\Users\Administrator\.ssh\*.pub
type C:\Users\Administrator\.ssh\authorized_keys

# Try to SSH to VM101 (should FAIL)
ssh mgmt1@<VM101_IP> "hostname"
```

**Expected Result:** ❌ Connection refused or authentication failed

### **Check VM101's SSH Configuration**

**On VM101 (Ubuntu):**
```bash
# Check who can SSH to VM101
cat ~/.ssh/authorized_keys

# Check if VM100's key is in authorized_keys
cat ~/.ssh/authorized_keys | grep -i "vm100\|<VM100_IP>"

# Check SSH server config
sudo cat /etc/ssh/sshd_config | grep -E "AllowUsers|DenyUsers|PasswordAuthentication"
```

**Expected Result:** 
- ✅ No VM100 keys in VM101's authorized_keys
- ✅ PasswordAuthentication no (key-based only)

### **Check Firewall Rules**

**On VM101:**
```bash
# Check UFW rules
sudo ufw status verbose

# Check if VM100 IP is blocked (optional)
sudo ufw status | grep <VM100_IP>
```

**Recommendation:** 
- Allow SSH from specific IPs only (if possible)
- Or use SSH key restrictions

---

## 🛠️ Security Hardening Steps

### **Step 1: Verify VM100 Cannot SSH to VM101**

```bash
# On VM100, test SSH to VM101
ssh mgmt1@<VM101_IP> "hostname"
# Should FAIL with "Permission denied" or "Connection refused"
```

### **Step 2: Ensure VM101 Only Accepts Authorized Keys**

**On VM101:**
```bash
# Review authorized_keys
cat ~/.ssh/authorized_keys

# Remove any VM100 keys (if present)
# Edit ~/.ssh/authorized_keys and remove lines containing VM100 references
```

### **Step 3: Harden SSH on VM101 (Optional but Recommended)**

**Edit `/etc/ssh/sshd_config`:**
```bash
sudo nano /etc/ssh/sshd_config
```

**Add/Modify:**
```
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no
AllowUsers mgmt1
# Or use: DenyUsers Administrator (if VM100 user is Administrator)
```

**Restart SSH:**
```bash
sudo systemctl restart sshd
```

### **Step 4: Use Firewall to Block VM100 (Optional)**

**On VM101:**
```bash
# Option 1: Block VM100 IP from SSH (if you don't need VM100 to access VM101)
sudo ufw deny from <VM100_IP> to any port 22

# Option 2: Allow only specific IPs (more restrictive)
sudo ufw delete allow 22/tcp
sudo ufw allow from YOUR_TRUSTED_IP to any port 22
```

**⚠️ Warning:** If you block VM100, make sure you have another way to manage VM101!

### **Step 5: Use SSH Key Restrictions (Recommended)**

**On VM101, edit `~/.ssh/authorized_keys` and add restrictions:**

```bash
# Instead of:
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... key-comment

# Use:
from="192.168.12.X",command="/bin/false",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... key-comment
```

**This prevents:**
- Port forwarding
- X11 forwarding
- Agent forwarding
- Command execution (if using command restriction)

---

## 🔐 Security Model Summary

### **Ideal Architecture:**

```
VM100 (AI Host)
├── Services: LM Studio, SHENRON API
├── SSH Server: Accepts connections from VM101 only
└── NO SSH keys to other VMs
└── NO SSH access to VM101

VM101 (Control Node)
├── SSH Client: Can connect to all VMs
├── SSH Keys: Separate key for each VM
├── SSH Server: Accepts connections from authorized sources only
└── NO access from VM100
```

### **Attack Scenarios:**

**Scenario 1: VM100 Compromised**
- ✅ Attacker has access to VM100
- ❌ Cannot SSH to VM101 (no keys, blocked)
- ❌ Cannot extract VM101's keys (not on VM100)
- ❌ Cannot use VM101 to access other VMs
- ✅ **Result: Only VM100 is compromised**

**Scenario 2: VM101 Compromised**
- ⚠️ Attacker has access to VM101
- ⚠️ Attacker has keys to all VMs
- ⚠️ Can access all VMs
- ✅ **Mitigation: Separate keys per VM (limits damage)**
- ✅ **Mitigation: Rotate keys immediately**

**Scenario 3: VM100 + VM101 Both Compromised**
- ❌ Attacker has full infrastructure access
- ✅ **Mitigation: Network segmentation, monitoring, alerts**

---

## 📋 Security Checklist

- [ ] Verify VM100 cannot SSH to VM101
- [ ] Verify VM101's authorized_keys does not contain VM100 keys
- [ ] Verify VM100 does not have SSH keys to other VMs
- [ ] Verify VM101 uses key-based auth only (no passwords)
- [ ] Verify separate SSH keys per VM (migration in progress)
- [ ] Consider firewall rules to block VM100 → VM101 SSH
- [ ] Consider SSH key restrictions (no-port-forwarding, etc.)
- [ ] Document authorized SSH access sources
- [ ] Set up monitoring/alerts for unauthorized SSH attempts

---

## 🚨 Critical Security Rules

1. **VM100 is a SERVICE PROVIDER, not a controller**
   - VM100 provides AI services (LM Studio, SHENRON API)
   - VM100 does NOT control other VMs
   - VM100 does NOT have SSH keys to other VMs

2. **VM101 is the CONTROL NODE**
   - VM101 controls all VMs (one-way)
   - VM101 has SSH keys to all VMs
   - VM101 should NOT accept SSH from VM100

3. **One-Way Trust Model**
   - VM101 → VM100: ✅ Trusted (control node manages AI host)
   - VM100 → VM101: ❌ Not trusted (AI host cannot control control node)
   - VM100 → Other VMs: ❌ Not trusted (AI host cannot control other VMs)

---

**If VM100 is compromised, VM101 and other VMs remain secure IF:**
- ✅ VM100 cannot SSH to VM101
- ✅ VM100 does not have VM101's SSH keys
- ✅ VM101's SSH keys are not stored on VM100
- ✅ Network/firewall blocks VM100 → VM101 SSH

**Verify these conditions NOW!**




