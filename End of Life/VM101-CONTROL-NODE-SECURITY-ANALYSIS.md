<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔒 VM101 Control Node Security Analysis

**Created:** November 23, 2025  
**Purpose:** Analyze security implications of VM101 as control node with SSH access to all VMs  
**Status:** ⚠️ Critical Security Consideration

---

## 🚨 THE FUNDAMENTAL SECURITY QUESTION

**Question:** If VM101 is compromised, what stops an attacker from SSH'ing into all other VMs?

**Answer:** **Nothing directly stops it** - this is an inherent risk of a control node architecture.

**However:** Multiple security layers can detect, prevent, and limit the damage.

---

## 🎯 THE CONTROL NODE DILEMMA

### **The Problem:**

```
VM101 (Control Node)
    ├── SSH Key → VM100 ✅
    ├── SSH Key → VM120 ✅
    ├── SSH Key → VM150 ✅
    ├── SSH Key → VM160 ✅
    ├── SSH Key → VM170 ✅
    ├── SSH Key → VM180 ✅
    └── SSH Key → VM200 ✅

If VM101 is compromised:
    Attacker has access to ALL VMs via SSH keys
```

**This is BY DESIGN:**
- VM101 is the control node
- It needs SSH access to all VMs for management
- This is the same risk as any orchestration system (Ansible, Puppet, etc.)

---

## 🛡️ DEFENSE IN DEPTH STRATEGY

### **Layer 1: Protect VM101 Itself (Primary Defense)**

**This is the most important layer** - prevent VM101 from being compromised.

#### **1a. Network Isolation:**
```bash
# VM101 should be on a management network (if possible)
# Or use firewall rules to limit inbound access

# On VM101 (UFW):
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from 192.168.12.0/24 to any port 22  # Only local network
sudo ufw allow from 192.168.12.0/24 to any port 9001 # code-server
sudo ufw deny from any to any port 22  # Block external SSH
```

#### **1b. API Security (VM100 → VM101):**
```python
# VM101 should validate and sanitize ALL API inputs
# Example: Rate limiting, authentication, input validation

from flask import Flask, request, abort
from functools import wraps
import time

app = Flask(__name__)

# Rate limiting with Redis (persistent across restarts)
from redis import Redis
from functools import wraps

redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)

def rate_limit(max_per_minute=60):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            client_ip = request.remote_addr
            key = f"rate_limit:{client_ip}"
            
            # Increment request count
            current = redis_client.incr(key)
            
            # Set expiration on first request
            if current == 1:
                redis_client.expire(key, 60)
            
            # Check if limit exceeded
            if current > max_per_minute:
                abort(429)  # Too Many Requests
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

# Example usage:
@app.route('/api/deploy', methods=['POST'])
@rate_limit(max_per_minute=30)  # Max 30 requests per minute
def deploy_service():
    # Protected API endpoint
    return jsonify({"status": "deployed"})

@app.route('/api/command', methods=['POST'])
@rate_limit(max_per_minute=10)  # Limit to 10 requests/minute
def execute_command():
    # Validate input
    data = request.json
    if not data or 'command' not in data:
        abort(400)
    
    command = data['command']
    
    # Whitelist allowed commands (NEVER execute arbitrary commands)
    ALLOWED_COMMANDS = ['hostname', 'uptime', 'df -h']
    if command not in ALLOWED_COMMANDS:
        abort(403)  # Forbidden
    
    # Execute safely
    result = subprocess.run(command, shell=True, capture_output=True)
    return {'output': result.stdout.decode()}
```

#### **1c. Input Validation:**
```python
# NEVER trust input from VM100 (or any external source)
# Always validate, sanitize, and whitelist

import re

def validate_command(command):
    # Whitelist approach (only allow specific commands)
    ALLOWED_PATTERNS = [
        r'^hostname$',
        r'^uptime$',
        r'^df -h$',
        r'^systemctl status [a-zA-Z0-9-]+$',
    ]
    
    for pattern in ALLOWED_PATTERNS:
        if re.match(pattern, command):
            return True
    
    return False  # Reject everything else
```

#### **1d. Authentication & Authorization:**
```python
# Require API keys or tokens for VM100 → VM101 communication
API_KEYS = {
    'vm100': os.environ.get('VM100_API_KEY', 'change-me-in-production')
}

@app.before_request
def require_api_key():
    if request.path.startswith('/api/'):
        api_key = request.headers.get('X-API-Key')
        if api_key not in API_KEYS.values():
            abort(401)  # Unauthorized
```

---

### **Layer 2: Separate Keys Per VM (Limits Blast Radius)**

**What separate keys help with:**

#### **2a. Audit Trail:**
```bash
# Each VM uses a different key
# Can identify which VM was accessed

# On VM101, check which key was used:
ssh -v vm120 "hostname" 2>&1 | grep "Offering.*key"
# Output: Offering public key: /home/mgmt1/.ssh/vm-keys/vm120_key

# If VM101 is compromised, logs show which VMs were accessed
```

#### **2b. Revocation:**
```bash
# If one VM is compromised, can revoke its key without affecting others
# Remove key from VM101:
rm ~/.ssh/vm-keys/vm160_key*

# Other VMs still accessible with their keys
```

#### **2c. Principle of Least Privilege:**
```bash
# Each key can have different permissions
# Example: VM100 key might only allow specific commands

# In ~/.ssh/config:
Host vm100-goku
    HostName <VM100_IP>
    User Administrator
    IdentityFile ~/.ssh/vm-keys/vm100_key
    IdentitiesOnly yes
    # Restrict to specific commands
    Command="restricted-shell.sh"
```

**What separate keys DON'T help with:**
- ❌ Don't prevent VM101 compromise
- ❌ Don't stop attacker from using all keys if VM101 is compromised
- ❌ Don't prevent lateral movement

---

### **Layer 3: Network Segmentation & Firewall Rules**

#### **3a. Restrict SSH Access:**
```bash
# On each VM (VM100, VM120, etc.), restrict SSH to VM101 only

# On VM120 (Ubuntu):
sudo ufw allow from <VM101_IP> to any port 22
sudo ufw deny from any to any port 22  # Block all other SSH

# On VM100 (Windows Firewall):
# Allow SSH (port 22) only from <VM101_IP>
# Block all other IPs
```

#### **3b. Network Monitoring:**
```bash
# Monitor SSH connections
# Alert on unexpected SSH activity

# On VM101, log all SSH connections:
# Add to /etc/ssh/sshd_config:
LogLevel VERBOSE

# Monitor logs:
tail -f /var/log/auth.log | grep ssh

# Set up alerts for:
# - SSH connections from unexpected IPs
# - Multiple failed login attempts
# - SSH connections outside business hours
```

---

### **Layer 4: Monitoring & Detection**

#### **4a. SSH Connection Monitoring:**
```bash
# Monitor all SSH connections from VM101
# Alert on suspicious activity

# Script to monitor SSH connections:
cat > ~/monitor-ssh.sh << 'EOF'
#!/bin/bash
# Monitor SSH connections from VM101 to other VMs

LOG_FILE="/var/log/vm101-ssh-monitor.log"
ALERT_EMAIL="admin@example.com"

# Check recent SSH connections
recent_ssh=$(journalctl -u ssh -n 100 --since "5 minutes ago" | grep "Accepted")

if [ -n "$recent_ssh" ]; then
    echo "$(date): SSH activity detected" >> "$LOG_FILE"
    echo "$recent_ssh" >> "$LOG_FILE"
    
    # Alert if multiple connections in short time
    count=$(echo "$recent_ssh" | wc -l)
    if [ "$count" -gt 10 ]; then
        echo "ALERT: $count SSH connections in 5 minutes!" | mail -s "SSH Alert" "$ALERT_EMAIL"
    fi
fi
EOF

# Run every 5 minutes via cron
chmod +x ~/monitor-ssh.sh
crontab -e
# Add: */5 * * * * /home/mgmt1/monitor-ssh.sh
```

#### **4b. File Integrity Monitoring:**
```bash
# Monitor SSH key files for changes
# Alert if keys are modified

# Install AIDE (Advanced Intrusion Detection Environment)
sudo apt-get install aide

# Initialize database
sudo aide --init

# Check for changes
sudo aide --check
```

#### **4c. Process Monitoring:**
```bash
# Monitor for suspicious processes
# Alert on unexpected SSH connections

# Script to monitor SSH processes:
ps aux | grep ssh | grep -v grep | while read line; do
    # Check if SSH connection is to unexpected VM
    # Alert if detected
done
```

---

### **Layer 5: Least Privilege & Command Restrictions**

#### **5a. Restricted Shells:**
```bash
# Create restricted shells for each VM
# Limit what commands can be executed

# Example: restricted-shell.sh
cat > ~/restricted-shell.sh << 'EOF'
#!/bin/bash
# Restricted shell - only allow specific commands

ALLOWED_COMMANDS=(
    "hostname"
    "uptime"
    "df -h"
    "systemctl status"
    "systemctl restart"
)

command="$1"
if [[ " ${ALLOWED_COMMANDS[@]} " =~ " ${command} " ]]; then
    exec "$command" "$@"
else
    echo "Command not allowed: $command"
    exit 1
fi
EOF

chmod +x ~/restricted-shell.sh
```

#### **5b. SSH Forced Commands:**
```bash
# In each VM's authorized_keys, restrict commands
# Example on VM120:

# In ~/.ssh/authorized_keys:
command="/home/proxy1/restricted-shell.sh" ssh-ed25519 AAAAC3... vm101-key
```

---

### **Layer 6: Backup & Recovery**

#### **6a. Regular Backups:**
```bash
# Regular backups of VM101
# Can restore to known-good state if compromised

# Automated backup script:
cat > ~/backup-vm101.sh << 'EOF'
#!/bin/bash
# Backup VM101 configuration and keys

BACKUP_DIR="/mnt/backups/vm101"
DATE=$(date +%Y%m%d)

mkdir -p "$BACKUP_DIR/$DATE"

# Backup SSH keys (encrypted)
tar -czf "$BACKUP_DIR/$DATE/ssh-keys.tar.gz" ~/.ssh/
gpg --encrypt --recipient admin@example.com "$BACKUP_DIR/$DATE/ssh-keys.tar.gz"
rm "$BACKUP_DIR/$DATE/ssh-keys.tar.gz"  # Remove unencrypted version

# Backup configuration files
tar -czf "$BACKUP_DIR/$DATE/config.tar.gz" \
    ~/.ssh/config \
    /etc/ufw/ \
    ~/GitHub/Dell-Server-Roadmap/scripts/

echo "Backup completed: $BACKUP_DIR/$DATE"
EOF

# Run daily
chmod +x ~/backup-vm101.sh
```

---

## 🔍 DETECTION & RESPONSE

### **If VM101 is Compromised:**

#### **Immediate Actions:**
1. **Isolate VM101:**
   ```bash
   # On Proxmox host
   qm shutdown 101
   # Or disconnect network
   ```

2. **Revoke All SSH Keys:**
   ```bash
   # On each VM, remove VM101's keys
   # VM120:
   sed -i '/vm101/d' ~/.ssh/authorized_keys
   
   # VM100 (Windows):
   # Remove VM101 keys from authorized_keys
   ```

3. **Investigate:**
   - Check logs for unauthorized access
   - Identify what was accessed
   - Determine attack vector

4. **Restore:**
   - Restore VM101 from backup
   - Regenerate all SSH keys
   - Re-deploy keys to VMs

---

## 📊 RISK ASSESSMENT

### **Current Risk Level: MEDIUM-HIGH**

**Why:**
- ✅ VM101 has access to all VMs (by design)
- ⚠️ If compromised, attacker has access to everything
- ⚠️ Limited monitoring currently
- ⚠️ No network segmentation

**Mitigation:**
- ✅ Separate keys per VM (limits blast radius)
- ✅ One-way trust (VM100 can't SSH to VM101)
- ⚠️ Need: Monitoring, alerting, network segmentation
- ⚠️ Need: Input validation on API endpoints
- ⚠️ Need: Rate limiting on API calls

---

## ✅ RECOMMENDED SECURITY IMPROVEMENTS

### **Priority 1 (Critical):**
1. ✅ **Separate SSH keys per VM** (in progress)
2. ⚠️ **API input validation** (need to implement)
3. ⚠️ **Rate limiting on API endpoints** (need to implement)
4. ⚠️ **Firewall rules** (restrict SSH to VM101 only on each VM)

### **Priority 2 (High):**
5. ⚠️ **SSH connection monitoring** (need to implement)
6. ⚠️ **File integrity monitoring** (AIDE or similar)
7. ⚠️ **Regular backups** (automated)
8. ⚠️ **Network segmentation** (management network)

### **Priority 3 (Medium):**
9. ⚠️ **Restricted shells** (limit commands per VM)
10. ⚠️ **SSH forced commands** (in authorized_keys)
11. ⚠️ **SIEM/Security monitoring** (centralized logging)
12. ⚠️ **Incident response plan** (documented procedures)

---

## 🎯 SUMMARY

**The Reality:**
- VM101 is a **single point of failure** (by design)
- If compromised, attacker has access to all VMs
- This is the **inherent risk** of a control node architecture

**The Defense:**
- **Protect VM101** (most important)
- **Monitor everything** (detect compromise quickly)
- **Limit damage** (separate keys, network segmentation)
- **Have a plan** (incident response, backups)

**The Bottom Line:**
- Separate keys help with **isolation and audit**, not prevention
- **Primary defense** is protecting VM101 itself
- **Secondary defense** is monitoring and detection
- **Tertiary defense** is limiting blast radius and quick response

---

**Last Updated:** November 23, 2025  
**Status:** ⚠️ Security Analysis Complete - Action Items Identified




