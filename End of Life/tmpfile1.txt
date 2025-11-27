<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔧 VM101 SSH Troubleshooting Guide

**Purpose:** Diagnose and resolve common SSH key deployment and connection issues  
**Last Updated:** November 24, 2025

---

## 🚨 Common Issues & Solutions

### **Issue 1: Connection Refused (Port 22)**

**Symptoms:**
```
ssh: connect to host <VM120_IP> port 22: Connection refused
```

**Diagnosis:**
```bash
# Check if SSH is running on the target VM
ping <VM120_IP>
nc -zv <VM120_IP> 22

# Check VM firewall rules
ssh proxy1@<VM120_IP> sudo ufw status
```

**Solutions:**
1. **SSH service not running:**
   ```bash
   # On the target VM
   sudo systemctl status ssh
   sudo systemctl start ssh
   sudo systemctl enable ssh
   ```

2. **Firewall blocking port 22:**
   ```bash
   # On the target VM
   sudo ufw allow 22/tcp
   sudo ufw allow from <VM101_IP> to any port 22
   ```

3. **Network connectivity issue:**
   ```bash
   # From VM101, test connectivity
   ip route show
   ping -c 3 <VM120_IP>
   ```

---

### **Issue 2: Authentication Denied / Permission Denied**

**Symptoms:**
```
Permission denied (publickey)
Public key authentication failed for user 'proxy1'
```

**Diagnosis:**
```bash
# Check if key exists on VM101
ls -la ~/.ssh/vm-keys/vm120_key*
chmod 600 ~/.ssh/vm-keys/vm120_key

# Check if public key is in authorized_keys on target VM
ssh proxy1@<VM120_IP> "cat ~/.ssh/authorized_keys | grep -c 'vm120_key'"

# Check public key fingerprint
ssh-keygen -lf ~/.ssh/vm-keys/vm120_key.pub
```

**Solutions:**
1. **Public key not in authorized_keys:**
   ```bash
   # Add key manually
   cat ~/.ssh/vm-keys/vm120_key.pub | ssh proxy1@<VM120_IP> \
       "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
   ```

2. **Wrong permissions on authorized_keys:**
   ```bash
   # On target VM
   chmod 600 ~/.ssh/authorized_keys
   ```

3. **Wrong permissions on .ssh directory:**
   ```bash
   # On target VM
   chmod 700 ~/.ssh
   ```

4. **SSH config pointing to wrong key:**
   ```bash
   # Check SSH config on VM101
   cat ~/.ssh/config | grep -A 5 "vm120-proxy"
   # Verify IdentityFile path is correct
   ```

---

### **Issue 3: Timeout / Connection Hanging**

**Symptoms:**
```
ssh: connect to host <VM160_IP> port 22: Operation timed out
# Or just hangs without response
```

**Diagnosis:**
```bash
# Test with explicit timeout
ssh -o ConnectTimeout=5 dbs1@<VM160_IP> "echo test"

# Check if VM is reachable
ping -c 1 <VM160_IP>
mtr -c 1 <VM160_IP>

# Check network routes
ip route | grep <VM160_IP>
```

**Solutions:**
1. **VM is unreachable / down:**
   ```bash
   # Check VM status in Proxmox
   # Or contact infrastructure team
   # Use the add-vm-keys.sh script which has a 15-second timeout
   ```

2. **Network congestion or slow VM:**
   ```bash
   # Increase SSH timeout
   ssh -o ConnectTimeout=30 dbs1@<VM160_IP> "echo test"
   
   # Or update SSH config
   echo "ConnectTimeout 30" >> ~/.ssh/config
   ```

3. **Firewall rule blocking SSH:**
   ```bash
   # On target VM
   sudo ufw allow from <VM101_IP> to any port 22
   ```

---

### **Issue 4: Key Permission Errors**

**Symptoms:**
```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for '/home/mgmt1/.ssh/vm-keys/vm120_key' are too open.
```

**Diagnosis:**
```bash
# Check key file permissions
ls -la ~/.ssh/vm-keys/vm120_key
# Should be: -rw------- (600)

# Check SSH directory permissions
ls -lad ~/.ssh
# Should be: drwx------ (700)
```

**Solutions:**
```bash
# Fix key file permissions
chmod 600 ~/.ssh/vm-keys/vm120_key

# Fix SSH directory permissions
chmod 700 ~/.ssh

# Fix authorized_keys permissions
ssh proxy1@<VM120_IP> "chmod 600 ~/.ssh/authorized_keys"
```

---

### **Issue 5: Wrong Key Being Used**

**Symptoms:**
```
Permission denied (publickey)
# Or connection works but with wrong user context
```

**Diagnosis:**
```bash
# Force verbose SSH to see which key is being used
ssh -v vm120-proxy "whoami" 2>&1 | grep -i "offering"

# Check SSH config
cat ~/.ssh/config | grep -A 10 "vm120-proxy"

# Check which key SSH is trying
ssh -vvv vm120-proxy "echo test" 2>&1 | grep -E "Trying private key|Offering"
```

**Solutions:**
```bash
# Force specific key
ssh -i ~/.ssh/vm-keys/vm120_key proxy1@<VM120_IP> "whoami"

# Update SSH config to use correct key
# Edit ~/.ssh/config and ensure:
#   IdentityFile ~/.ssh/vm-keys/vm120_key
#   IdentitiesOnly yes
```

---

### **Issue 6: Too Many Authentication Attempts**

**Symptoms:**
```
Received disconnect from <VM120_IP> port 22:2: Too many authentication failures for proxy1
```

**Diagnosis:**
```bash
# SSH tried too many keys
ssh -v vm120-proxy "echo test" 2>&1 | grep -i "attempt"

# Check SSH config for IdentitiesOnly
cat ~/.ssh/config | grep -i "identitiesonly"
```

**Solutions:**
```bash
# Add to SSH config for this host
cat >> ~/.ssh/config << EOF
Host vm120-proxy
    IdentitiesOnly yes
    IdentityFile ~/.ssh/vm-keys/vm120_key
EOF

# Or use specific key only
ssh -i ~/.ssh/vm-keys/vm120_key -o IdentitiesOnly=yes proxy1@<VM120_IP>
```

---

### **Issue 7: Audit Log Shows FAILURE Status**

**Symptoms:**
```
cat ~/.ssh/key-deployment.log
[2025-11-24 10:30:00] VM160: FAILURE - SSH key deployment failed
```

**Diagnosis:**
```bash
# Check if VM was accessible
ssh -o ConnectTimeout=15 dbs1@<VM160_IP> "echo test"

# Check if SSH key was actually added
ssh dbs1@<VM160_IP> "cat ~/.ssh/authorized_keys | grep -c vm160_key"

# Run add-vm-keys.sh again with verbose output
bash -x ~/add-vm-keys.sh 2>&1 | head -50
```

**Solutions:**
1. **VM was inaccessible:**
   - Wait for VM to come online
   - Check network connectivity
   - Run deployment again

2. **Manual deployment needed:**
   ```bash
   # On the target VM (via RDP/direct access)
   cat ~/.ssh/authorized_keys >> ~/.ssh/authorized_keys.backup
   # Add key manually from ~/.ssh/vm-keys/vmXXX_key.pub
   chmod 600 ~/.ssh/authorized_keys
   ```

---

## 🔍 Diagnostic Commands

### **Quick Health Check**
```bash
# Test connection to all VMs
for vm in 100 120 150 160 170 180 200; do
    echo "Testing VM${vm}..."
    ssh -o ConnectTimeout=5 vm$(printf "%03d" $vm) "echo OK" 2>/dev/null || echo "FAILED"
done

# Check deployment log
tail -20 ~/.ssh/key-deployment.log

# Check key rotation log (if available)
tail -20 ~/.ssh/key-rotation.log
```

### **Verify SSH Config**
```bash
# Check all VM aliases
cat ~/.ssh/config | grep "^Host vm"

# Verify key paths
grep "IdentityFile" ~/.ssh/config

# Test specific alias
ssh -T vm120-proxy "hostname"
```

### **Check Key Files**
```bash
# List all keys
ls -la ~/.ssh/vm-keys/

# Verify key fingerprints
for key in ~/.ssh/vm-keys/vm*_key.pub; do
    echo "=== $(basename $key) ==="
    ssh-keygen -lf $key
done
```

---

## 📋 Verification Checklist

Before contacting support, verify:

- [ ] VM is reachable (ping succeeds)
- [ ] SSH port 22 is open (telnet/nc succeeds)
- [ ] Public key is in authorized_keys on target VM
- [ ] authorized_keys has 600 permissions
- [ ] ~/.ssh directory has 700 permissions
- [ ] SSH config points to correct key
- [ ] Key file has 600 permissions on VM101
- [ ] SSH config uses IdentitiesOnly=yes
- [ ] No firewall rules blocking SSH

---

## 📞 Escalation Path

If issues persist after troubleshooting:

1. Collect diagnostic output:
   ```bash
   mkdir -p /tmp/ssh-diagnostics
   cd /tmp/ssh-diagnostics
   
   # Collect logs
   cp ~/.ssh/key-deployment.log .
   cp ~/.ssh/key-rotation.log . 2>/dev/null || true
   
   # Run verbose SSH test
   ssh -vvv vm120-proxy "hostname" > ssh-test.log 2>&1
   
   # Collect config
   cp ~/.ssh/config .
   
   # Create tar archive
   tar -czf ssh-diagnostics.tar.gz *
   ```

2. Contact infrastructure team with:
   - SSH diagnostics archive
   - Specific VM(s) affected
   - When the issue started
   - Any recent network changes

---

**Last Updated:** November 24, 2025  
**Created by:** Zencoder VM101 Security Review
