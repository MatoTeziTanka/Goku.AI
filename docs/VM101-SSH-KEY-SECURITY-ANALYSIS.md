<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔐 VM101 SSH Key Security Analysis

**Question:** Are all VMs sharing the same SSH key?  
**Security Concern:** One compromised key = access to all VMs  
**Architecture Clarification:** VM101 (control node) vs VM100 (AI host)

---

## 🏗️ Architecture Overview

### **VM101 - Control Node (Orchestrator)**
- **Role:** Central management and orchestration
- **Purpose:** Needs SSH access to ALL VMs to:
  - Deploy code updates
  - Run management scripts
  - Monitor services
  - Execute commands across infrastructure
- **Access:** Should have SSH keys to all VMs (by design)

### **VM100 - AI Host (LM Studio + SHENRON)**
- **Role:** AI model hosting and API server
- **Purpose:** Runs LM Studio and SHENRON API
- **Access:** Does NOT need SSH access to other VMs
- **Note:** VM100 is a service provider, not a control node

---

## 🔍 Check Current SSH Key Setup

### **On VM101 - Check What Keys You Have**

```bash
# List all SSH keys
ls -la ~/.ssh/*.pub

# Check which keys are being used
cat ~/.ssh/id_ed25519.pub
cat ~/.ssh/id_rsa.pub
cat ~/.ssh/shenron_key.pub
cat ~/.ssh/vm100_shenron.pub
cat ~/.ssh/id_ed25519_sethp.pub

# Check SSH config (if exists)
cat ~/.ssh/config 2>/dev/null || echo "No SSH config file"
```

### **Check Which Key is Used for Each VM**

```bash
# Test with verbose SSH to see which key is used
ssh -v proxy1@<VM120_IP> "hostname" 2>&1 | grep -i "identity\|key"
ssh -v wp1@<VM150_IP> "hostname" 2>&1 | grep -i "identity\|key"
ssh -v Administrator@<VM100_IP> "hostname" 2>&1 | grep -i "identity\|key"
```

### **Check What Keys Are on Each VM**

**For accessible VMs, check their authorized_keys:**

```bash
# VM100
ssh Administrator@<VM100_IP> "cat C:/Users/Administrator/.ssh/authorized_keys 2>/dev/null || cat ~/.ssh/authorized_keys"

# VM120
ssh proxy1@<VM120_IP> "cat ~/.ssh/authorized_keys"

# VM150
ssh wp1@<VM150_IP> "cat ~/.ssh/authorized_keys"
```

---

## 🔐 Security Model Options

### **Option 1: Single Key for Control Node (Current/Recommended)**

**Architecture:**
- VM101 has ONE key (`id_ed25519`)
- This key is added to all VMs' `authorized_keys`
- VM101 can access all VMs (by design - it's the control node)

**Security:**
- ✅ **Pros:** Simple, easy to manage, standard for control nodes
- ⚠️ **Cons:** If VM101 is compromised, attacker has access to all VMs
- ✅ **Mitigation:** Secure VM101 (firewall, updates, monitoring)

**This is NORMAL for control/orchestration nodes!**

### **Option 2: Separate Key Per VM (More Secure)**

**Architecture:**
- VM101 has MULTIPLE keys (one per VM)
- Each VM only has ONE key in `authorized_keys`
- VM101 uses different keys for different VMs

**Security:**
- ✅ **Pros:** If one key is compromised, only one VM is at risk
- ⚠️ **Cons:** More complex to manage, more keys to rotate
- ✅ **Better:** Defense in depth, principle of least privilege

---

## 🛠️ Setup Separate Keys Per VM

### **Step 1: Generate Separate Keys**

```bash
# Create directory for VM-specific keys
mkdir -p ~/.ssh/vm-keys

# Generate key for each VM
ssh-keygen -t ed25519 -C "vm101-to-vm100" -f ~/.ssh/vm-keys/vm100_key -N ""
ssh-keygen -t ed25519 -C "vm101-to-vm120" -f ~/.ssh/vm-keys/vm120_key -N ""
ssh-keygen -t ed25519 -C "vm101-to-vm150" -f ~/.ssh/vm-keys/vm150_key -N ""
ssh-keygen -t ed25519 -C "vm101-to-vm160" -f ~/.ssh/vm-keys/vm160_key -N ""
ssh-keygen -t ed25519 -C "vm101-to-vm170" -f ~/.ssh/vm-keys/vm170_key -N ""
ssh-keygen -t ed25519 -C "vm101-to-vm180" -f ~/.ssh/vm-keys/vm180_key -N ""
ssh-keygen -t ed25519 -C "vm101-to-vm200" -f ~/.ssh/vm-keys/vm200_key -N ""

# Set permissions
chmod 700 ~/.ssh/vm-keys
chmod 600 ~/.ssh/vm-keys/*
chmod 644 ~/.ssh/vm-keys/*.pub
```

### **Step 2: Create SSH Config**

```bash
# Create SSH config to use specific keys
cat > ~/.ssh/config << 'EOF'
# VM100 - Windows Server 2025 (GOKU-AI)
Host vm100
    HostName <VM100_IP>
    User Administrator
    IdentityFile ~/.ssh/vm-keys/vm100_key
    IdentitiesOnly yes

# VM120 - Reverse Proxy
Host vm120
    HostName <VM120_IP>
    User proxy1
    IdentityFile ~/.ssh/vm-keys/vm120_key
    IdentitiesOnly yes

# VM150 - WordPress
Host vm150
    HostName <VM150_IP>
    User wp1
    IdentityFile ~/.ssh/vm-keys/vm150_key
    IdentitiesOnly yes

# VM160 - Database
Host vm160
    HostName <VM160_IP>
    User dbs1
    IdentityFile ~/.ssh/vm-keys/vm160_key
    IdentitiesOnly yes

# VM170 - Game Servers
Host vm170
    HostName <VM170_IP>
    User gsh1
    IdentityFile ~/.ssh/vm-keys/vm170_key
    IdentitiesOnly yes

# VM180 - API Services
Host vm180
    HostName <VM180_IP>
    User apis1
    IdentityFile ~/.ssh/vm-keys/vm180_key
    IdentitiesOnly yes

# VM200 - Plex (Windows)
Host vm200
    HostName <VM200_IP>
    User Administrator
    IdentityFile ~/.ssh/vm-keys/vm200_key
    IdentitiesOnly yes
EOF

chmod 600 ~/.ssh/config
```

### **Step 3: Add Keys to Each VM**

```bash
# VM100
cat ~/.ssh/vm-keys/vm100_key.pub | ssh Administrator@<VM100_IP> "mkdir -p C:/Users/Administrator/.ssh && cat >> C:/Users/Administrator/.ssh/authorized_keys"

# VM120
cat ~/.ssh/vm-keys/vm120_key.pub | ssh proxy1@<VM120_IP> "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# VM150
cat ~/.ssh/vm-keys/vm150_key.pub | ssh wp1@<VM150_IP> "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# VM160
cat ~/.ssh/vm-keys/vm160_key.pub | ssh dbs1@<VM160_IP> "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# VM170
cat ~/.ssh/vm-keys/vm170_key.pub | ssh gsh1@<VM170_IP> "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# VM180
cat ~/.ssh/vm-keys/vm180_key.pub | ssh apis1@<VM180_IP> "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# VM200
cat ~/.ssh/vm-keys/vm200_key.pub | ssh Administrator@<VM200_IP> "mkdir -p C:/Users/Administrator/.ssh && cat >> C:/Users/Administrator/.ssh/authorized_keys"
```

### **Step 4: Test with New Keys**

```bash
# Test using SSH config aliases
ssh vm100 "hostname"
ssh vm120 "hostname"
ssh vm150 "hostname"
# etc.
```

---

## 🔍 Diagnostic Commands

### **Check Current Key Usage**

```bash
# See which key SSH uses for each VM
for vm in "Administrator@<VM100_IP>" "proxy1@<VM120_IP>" "wp1@<VM150_IP>"; do
  echo "=== Testing $vm ==="
  ssh -v $vm "hostname" 2>&1 | grep -E "identity|Offering|Authenticating" | head -5
  echo ""
done
```

### **Check Authorized Keys on Each VM**

```bash
# Check what keys are authorized on each accessible VM
echo "=== VM100 Authorized Keys ==="
ssh Administrator@<VM100_IP> "cat C:/Users/Administrator/.ssh/authorized_keys 2>/dev/null || echo 'No authorized_keys found'"

echo ""
echo "=== VM120 Authorized Keys ==="
ssh proxy1@<VM120_IP> "cat ~/.ssh/authorized_keys"

echo ""
echo "=== VM150 Authorized Keys ==="
ssh wp1@<VM150_IP> "cat ~/.ssh/authorized_keys"
```

### **Compare Keys**

```bash
# Compare your public keys
echo "=== All Public Keys on VM101 ==="
for key in ~/.ssh/*.pub; do
  echo "File: $key"
  cat "$key"
  echo ""
done
```

---

## 💡 Security Recommendations

### **For Control Node (VM101):**

1. **Single Key Approach (Current):**
   - ✅ Acceptable for control nodes
   - ✅ Standard practice in orchestration
   - ⚠️ Secure VM101 heavily (firewall, updates, monitoring)
   - ⚠️ Use strong passphrase on key (if using encrypted key)

2. **Separate Keys Approach (More Secure):**
   - ✅ Better security isolation
   - ✅ Limits blast radius if compromised
   - ⚠️ More complex to manage
   - ⚠️ More keys to rotate

### **For VM100 (AI Host):**

- **VM100 should NOT have SSH keys to other VMs**
- VM100 only needs to:
  - Accept connections from VM101 (for management)
  - Run LM Studio (port 1234)
  - Run SHENRON API (port 5000)
- VM100 does NOT need to SSH to other VMs

---

## 🎯 Recommended Setup

**For Your Architecture:**

1. **VM101 (Control Node):**
   - Use separate keys per VM (more secure)
   - Or use single key with strong security on VM101
   - Has access to all VMs (by design)

2. **VM100 (AI Host):**
   - Only has SSH server (accepts connections)
   - Does NOT have keys to other VMs
   - Isolated service provider

3. **Other VMs:**
   - Only have VM101's key(s) in authorized_keys
   - Do NOT have keys to each other
   - Isolated from each other

---

## 📋 Quick Check Script

```bash
#!/bin/bash
# Check SSH key security setup

echo "=== VM101 SSH Key Security Check ==="
echo ""

echo "1. Keys on VM101:"
ls -la ~/.ssh/*.pub | awk '{print $9, "(" $5 " bytes)"}'
echo ""

echo "2. SSH Config:"
if [ -f ~/.ssh/config ]; then
  cat ~/.ssh/config
else
  echo "  No SSH config - using default key selection"
fi
echo ""

echo "3. Testing which key is used (first 3 VMs):"
for vm in "Administrator@<VM100_IP>" "proxy1@<VM120_IP>" "wp1@<VM150_IP>"; do
  echo "  $vm:"
  ssh -v $vm "hostname" 2>&1 | grep -E "identity file|Offering.*key" | head -2
done
echo ""

echo "4. Authorized keys on accessible VMs:"
echo "  VM100:"
ssh Administrator@<VM100_IP> "cat C:/Users/Administrator/.ssh/authorized_keys 2>/dev/null | wc -l" 2>/dev/null || echo "    Cannot check"
echo "  VM120:"
ssh proxy1@<VM120_IP> "cat ~/.ssh/authorized_keys | wc -l" 2>/dev/null || echo "    Cannot check"
echo "  VM150:"
ssh wp1@<VM150_IP> "cat ~/.ssh/authorized_keys | wc -l" 2>/dev/null || echo "    Cannot check"
```

---

**Run the diagnostic commands to see your current setup, then decide on single key vs separate keys!**




