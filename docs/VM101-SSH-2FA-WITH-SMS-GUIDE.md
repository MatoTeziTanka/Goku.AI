<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔐 VM101 SSH 2FA with Google Authenticator + SMS Notifications

**Created:** November 23, 2025  
**Purpose:** Add time-based 2FA (TOTP) with SMS notifications for SSH access from VM101 to other VMs  
**Status:** 📋 Implementation Guide

---

## 🎯 GOAL

**When VM101 attempts to SSH into another VM (e.g., VM120):**
1. ✅ SSH key authentication happens (existing)
2. ✅ **NEW:** SMS sent to your phone: "VM101 attempting SSH to VM120. Enter 2FA code:"
3. ✅ **NEW:** You enter current Google Authenticator code
4. ✅ **NEW:** Validate code via text response or web prompt
5. ✅ **NEW:** SSH connection proceeds only after 2FA validation

**This adds a second factor even if SSH keys are compromised!**

---

## 📋 ARCHITECTURE OVERVIEW

```
VM101 (Control Node)
    ↓ SSH Connection Attempt
    ↓ ssh vm120 "command"
VM120 (Target VM)
    ↓ PAM Module Intercepts
    ↓ Requires 2FA
    ↓ Sends SMS to Your Phone
Your Phone
    ↓ You Enter Google Authenticator Code
    ↓ Respond via SMS or Web
VM120
    ↓ Validates TOTP Code
    ↓ Grants SSH Access
```

---

## 🔧 IMPLEMENTATION OPTIONS

### **Option 1: PAM + Google Authenticator + SMS (Recommended)**

**Components:**
- `libpam-google-authenticator` - TOTP validation
- `pam_exec` - Custom script for SMS notification
- SMS service (Twilio, AWS SNS, or simple email-to-SMS)
- Web interface (optional) for code entry

**Pros:**
- ✅ Works with existing SSH key setup
- ✅ Standard PAM integration
- ✅ Can be configured per-user or per-VM
- ✅ Supports both SMS and web approval

**Cons:**
- ⚠️ Requires manual approval (breaks full automation)
- ⚠️ Need to handle automation scripts separately

---

### **Option 2: SSH ForceCommand + Custom Script**

**Components:**
- Custom SSH wrapper script
- TOTP validation library
- SMS notification service
- Web approval endpoint

**Pros:**
- ✅ More flexible control
- ✅ Can bypass for specific trusted scripts
- ✅ Better automation handling

**Cons:**
- ⚠️ More complex setup
- ⚠️ Need to modify SSH config on each VM

---

## 🚀 IMPLEMENTATION: OPTION 1 (PAM + Google Authenticator)

### **Step 1: Install Required Packages**

**On Each Target VM (VM120, VM150, VM160, VM170, VM180):**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y libpam-google-authenticator qrencode

# For SMS integration (choose one):
# Option A: Twilio (recommended)
sudo apt-get install -y curl jq

# Option B: AWS SNS
sudo apt-get install -y awscli

# Option C: Email-to-SMS (simpler, free)
sudo apt-get install -y mailutils
```

---

### **Step 2: Setup Google Authenticator for Each User**

**On Each Target VM, for each user that needs SSH access:**

```bash
# Example: On VM120, for user 'proxy1'
ssh proxy1@<VM120_IP>

# Generate Google Authenticator secret
google-authenticator

# Follow prompts:
# - Scan QR code with Google Authenticator app
# - Save emergency codes
# - Answer: y, y, n, y, y
```

**This creates:** `~/.google_authenticator` file

**For VM101's SSH user (mgmt1 equivalent on each VM):**
```bash
# On VM120
sudo -u proxy1 google-authenticator

# On VM150
sudo -u wp1 google-authenticator

# On VM160
sudo -u dbs1 google-authenticator

# ... (repeat for each VM)
```

---

### **Step 3: Configure PAM for SSH**

**On Each Target VM:**

```bash
# Edit PAM SSH configuration
sudo nano /etc/pam.d/sshd

# Add BEFORE the @include common-auth line:
auth required pam_google_authenticator.so nullok
# 'nullok' allows users without 2FA to still login (remove after setup)
```

**Full `/etc/pam.d/sshd` should look like:**
```
# PAM configuration for the Secure Shell service

# Standard Un*x authentication.
@include common-auth

# Add Google Authenticator 2FA
auth required pam_google_authenticator.so nullok

# Disallow non-root logins when /etc/nologin exists.
account    required     pam_nologin.so

# Uncomment and edit /etc/security/access.conf if you need to set complex
# access limits that are hard to express in sshd_config.
# account  required     pam_access.so

# Standard Un*x authorization.
@include common-account

# Standard Un*x session setup and teardown.
@include common-session

# Print the message of the day upon successful login.
# This includes a dynamically generated part from /run/motd.dynamic
# and a static part from /etc/motd.
session    optional     pam_motd.so  motd=/run/motd.dynamic
session    optional     pam_motd.so noupdate

# Print the status of the user's mailbox upon successful login.
session    optional     pam_mail.so standard noenv # [1]

# Set up user limits from /etc/security/limits.conf.
session    required     pam_limits.so

# Read environment variables from /etc/environment and
# /etc/security/pam_env.conf.
session    required     pam_env.so # [1]
# In Debian 4.0 (etch), locale-related environment variables were moved to
# /etc/default/locale, so read that as well.
session    required     pam_env.so user_readenv=1 envfile=/etc/default/locale

# Standard Un*x password updating.
@include common-password
```

---

### **Step 4: Configure SSH to Require 2FA**

**On Each Target VM:**

```bash
# Edit SSH configuration
sudo nano /etc/ssh/sshd_config

# Add or modify:
ChallengeResponseAuthentication yes
UsePAM yes
AuthenticationMethods publickey,keyboard-interactive

# Restart SSH
sudo systemctl restart sshd
```

**Explanation:**
- `ChallengeResponseAuthentication yes` - Enables challenge/response (2FA prompt)
- `UsePAM yes` - Use PAM for authentication
- `AuthenticationMethods publickey,keyboard-interactive` - Require BOTH SSH key AND 2FA

---

### **Step 5: Setup SMS Notification Script**

**Create SMS notification script on each target VM:**

```bash
# Create notification script
sudo nano /usr/local/bin/ssh-2fa-notify.sh
```

**Script Content (Twilio Example):**
```bash
#!/bin/bash
# SSH 2FA Notification Script
# Sends SMS when SSH connection requires 2FA

# Configuration
TWILIO_ACCOUNT_SID="your-account-sid"
TWILIO_AUTH_TOKEN="your-auth-token"
TWILIO_PHONE="+1234567890"  # Your Twilio number
YOUR_PHONE="+1987654321"     # Your cell phone
VM_NAME="${HOSTNAME}"
SSH_USER="${PAM_USER}"
SSH_FROM="${PAM_RHOST:-unknown}"

# Create notification message
MESSAGE="🔐 SSH 2FA Required\n\nVM: ${VM_NAME}\nUser: ${SSH_USER}\nFrom: ${SSH_FROM}\n\nEnter Google Authenticator code to proceed."

# Send SMS via Twilio
curl -X POST "https://api.twilio.com/2010-04-01/Accounts/${TWILIO_ACCOUNT_SID}/Messages.json" \
    --data-urlencode "From=${TWILIO_PHONE}" \
    --data-urlencode "To=${YOUR_PHONE}" \
    --data-urlencode "Body=${MESSAGE}" \
    -u "${TWILIO_ACCOUNT_SID}:${TWILIO_AUTH_TOKEN}"

# Log notification
echo "$(date): 2FA notification sent for ${SSH_USER} from ${SSH_FROM}" >> /var/log/ssh-2fa.log
```

**Alternative: Email-to-SMS (Simpler, Free):**
```bash
#!/bin/bash
# SSH 2FA Notification via Email-to-SMS

VM_NAME="${HOSTNAME}"
SSH_USER="${PAM_USER}"
SSH_FROM="${PAM_RHOST:-unknown}"
YOUR_PHONE_EMAIL="your-phone@txt.att.net"  # AT&T example
# T-Mobile: your-phone@tmomail.net
# Verizon: your-phone@vtext.com
# Sprint: your-phone@messaging.sprintpcs.com

MESSAGE="SSH 2FA Required - VM: ${VM_NAME}, User: ${SSH_USER}, From: ${SSH_FROM}. Enter Google Authenticator code."

echo "${MESSAGE}" | mail -s "SSH 2FA Alert" "${YOUR_PHONE_EMAIL}"

echo "$(date): 2FA notification sent for ${SSH_USER} from ${SSH_FROM}" >> /var/log/ssh-2fa.log
```

**Make executable:**
```bash
sudo chmod +x /usr/local/bin/ssh-2fa-notify.sh
```

---

### **Step 6: Integrate SMS Notification with PAM**

**Modify PAM configuration to call notification script:**

```bash
# Edit PAM SSH configuration
sudo nano /etc/pam.d/sshd

# Add BEFORE pam_google_authenticator:
auth optional pam_exec.so quiet /usr/local/bin/ssh-2fa-notify.sh

# Full auth section should look like:
auth optional pam_exec.so quiet /usr/local/bin/ssh-2fa-notify.sh
auth required pam_google_authenticator.so nullok
```

**Note:** `quiet` flag prevents script errors from blocking authentication.

---

### **Step 7: Test 2FA Setup**

**From VM101, test SSH connection:**

```bash
# Test SSH to VM120
ssh proxy1@<VM120_IP>

# Expected flow:
# 1. SSH key authentication (automatic)
# 2. SMS sent to your phone
# 3. Prompt: "Verification code:"
# 4. Enter 6-digit code from Google Authenticator
# 5. Connection proceeds
```

---

## 📱 WEB-BASED APPROVAL (OPTIONAL)

**For web-based approval instead of SMS response:**

### **Step 1: Create Web Approval Endpoint**

**On VM101 (or central server):**

```python
# /opt/ssh-2fa-approval/app.py
from flask import Flask, request, jsonify
import pyotp
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
DB_PATH = '/opt/ssh-2fa-approval/pending_requests.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pending_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vm_name TEXT,
            ssh_user TEXT,
            ssh_from TEXT,
            totp_secret TEXT,
            created_at TIMESTAMP,
            approved BOOLEAN DEFAULT 0,
            approved_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/api/pending', methods=['GET'])
def get_pending():
    """Get pending SSH 2FA requests"""
    conn = sqlite3.connect(DB_PATH)
    requests = conn.execute('''
        SELECT * FROM pending_requests 
        WHERE approved = 0 
        AND created_at > datetime('now', '-5 minutes')
        ORDER BY created_at DESC
    ''').fetchall()
    conn.close()
    return jsonify(requests)

@app.route('/api/approve', methods=['POST'])
def approve():
    """Approve SSH 2FA request with TOTP code"""
    data = request.json
    request_id = data.get('id')
    totp_code = data.get('code')
    
    conn = sqlite3.connect(DB_PATH)
    req = conn.execute(
        'SELECT * FROM pending_requests WHERE id = ?',
        (request_id,)
    ).fetchone()
    
    if not req:
        return jsonify({'error': 'Request not found'}), 404
    
    # Validate TOTP code
    totp = pyotp.TOTP(req[4])  # totp_secret
    if not totp.verify(totp_code, valid_window=1):
        return jsonify({'error': 'Invalid code'}), 400
    
    # Mark as approved
    conn.execute(
        'UPDATE pending_requests SET approved = 1, approved_at = ? WHERE id = ?',
        (datetime.now(), request_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'approved'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=9002, ssl_context='adhoc')
```

### **Step 2: Modify Notification Script to Create Web Request**

```bash
#!/bin/bash
# Create pending request in database
# Send SMS with link to web approval page

VM_NAME="${HOSTNAME}"
SSH_USER="${PAM_USER}"
SSH_FROM="${PAM_RHOST}"
APPROVAL_URL="https://<VM101_IP>:9002"

# Create pending request (via API)
REQUEST_ID=$(curl -s -X POST "${APPROVAL_URL}/api/request" \
    -H "Content-Type: application/json" \
    -d "{\"vm_name\":\"${VM_NAME}\",\"ssh_user\":\"${SSH_USER}\",\"ssh_from\":\"${SSH_FROM}\"}")

# Send SMS with approval link
MESSAGE="SSH 2FA: ${VM_NAME} - ${SSH_USER} from ${SSH_FROM}\nApprove: ${APPROVAL_URL}/approve/${REQUEST_ID}"

# Send SMS (Twilio or email-to-SMS)
# ... (SMS sending code)
```

---

## 🔄 HANDLING AUTOMATION SCRIPTS & DIRECT PC ACCESS

**Your Use Case:**
- ✅ Your PC connects via `shenron.lightspeedup.com` (Cloudflare Tunnel) or MobaXterm
- ✅ You want direct SSH access from your PC **without 2FA** (convenient)
- ✅ VM101 automation should **still require 2FA** (secure)
- ✅ Your PC IP is the only internal IP allowed via Cloudflare Tunnel

**Solution:** IP-based bypass for your PC while requiring 2FA for VM101 and all other connections.

### **Option A: IP-Based Bypass (Recommended for Your Use Case)**

**Your Setup:**
- Your PC connects via `shenron.lightspeedup.com` (Cloudflare Tunnel) or MobaXterm
- You want direct SSH access without 2FA
- VM101 automation should still require 2FA

**Implementation:**

```bash
# Install pam_access module
sudo apt-get install -y libpam-modules

# Edit PAM configuration
sudo nano /etc/pam.d/sshd

# Add BEFORE pam_google_authenticator:
auth [success=1 default=ignore] pam_access.so accessfile=/etc/security/access-2fa-bypass.conf
auth required pam_google_authenticator.so nullok

# Create bypass config
sudo nano /etc/security/access-2fa-bypass.conf
```

**Bypass Configuration:**

```bash
# /etc/security/access-2fa-bypass.conf
# Format: permission : users : origins

# YOUR PC's IP
# Verified: 192.168.12.77 (Debbie-PC - internal IP on same network)
+ : ALL : 192.168.12.77

# OR: Your PC's Public IP (when connecting via Cloudflare Tunnel)
# Find it: curl ifconfig.me (from your PC)
# + : ALL : YOUR_PC_PUBLIC_IP

# OR: Cloudflare IP ranges (optional - less secure, allows all Cloudflare IPs)
# WARNING: Only use if you want all Cloudflare IPs to bypass 2FA
# + : ALL : 104.16.0.0/12
# + : ALL : 172.64.0.0/13

# Block all others (require 2FA for VM101, etc.)
- : ALL : ALL
```

**Your PC IP (Verified):**
- **Internal IP:** `192.168.12.77` (Debbie-PC)
- **Network:** Same network as VMs (192.168.12.0/24)
- **Use This:** Add `192.168.12.77` to bypass list

**Finding Your Public IP (if needed for Cloudflare Tunnel):**
```bash
# From your PC:
curl ifconfig.me
# Or: curl ipinfo.io/ip
```

**Result:**
- ✅ Your PC → No 2FA required (direct access)
- ✅ VM101 → 2FA required (SMS + Google Authenticator)
- ✅ All other IPs → 2FA required

### **Option B: Separate SSH User for Automation (Alternative)**

```bash
# On each target VM, create automation user
sudo useradd -m -s /bin/bash automator
sudo mkdir -p /home/automator/.ssh

# Copy VM101's SSH key
sudo cp ~/.ssh/vm-keys/vm120_key.pub /home/automator/.ssh/authorized_keys
sudo chown -R automator:automator /home/automator/.ssh

# Configure PAM to skip 2FA for automator user
sudo nano /etc/pam.d/sshd

# Add at top:
auth sufficient pam_google_authenticator.so nullok user=!automator
```

### **Option A: IP-Based Bypass (RECOMMENDED - For Your PC)**

**Your Setup:**
- Your PC connects via `shenron.lightspeedup.com` (Cloudflare Tunnel) or MobaXterm
- You want direct SSH access without 2FA (convenient)
- VM101 automation still requires 2FA (secure)
- Your PC IP is the only internal IP allowed

**Setup:**

```bash
# Install pam_access module
sudo apt-get install -y libpam-modules

# Edit PAM configuration
sudo nano /etc/pam.d/sshd

# Add BEFORE pam_google_authenticator:
auth [success=1 default=ignore] pam_access.so accessfile=/etc/security/access-2fa-bypass.conf
auth required pam_google_authenticator.so nullok

# Create bypass config
sudo nano /etc/security/access-2fa-bypass.conf
```

**Bypass Configuration (`/etc/security/access-2fa-bypass.conf`):**
```bash
# Allow 2FA bypass for your PC IP (via Cloudflare Tunnel or direct connection)
# Format: permission : users : origins

# Your PC's public IP (check via: curl ifconfig.me)
# Example: + : ALL : 123.45.67.89

# OR: Your PC's internal IP if connecting directly
# Example: + : ALL : 192.168.12.50

# OR: Cloudflare Tunnel IP ranges (if applicable)
# Example: + : ALL : 104.16.0.0/12

# Block all others (require 2FA)
- : ALL : ALL
```

**Finding Your PC's IP:**

**Option 1: Public IP (via Cloudflare Tunnel):**
```bash
# On your PC, check public IP
curl ifconfig.me
# Or: curl ipinfo.io/ip

# Add this IP to bypass list
```

**Option 2: Internal IP (if on same network):**
```bash
# On your PC (Windows):
ipconfig
# Look for IPv4 Address (e.g., 192.168.12.50)

# On your PC (Linux/Mac):
ip addr show
# Or: ifconfig
```

**Option 3: Cloudflare Tunnel IP Detection:**
```bash
# On target VM, check recent SSH connections
sudo tail -f /var/log/auth.log | grep "Accepted publickey"

# When you SSH from your PC, note the source IP
# Add that IP to bypass list
```

**Complete Example Configuration:**

```bash
# /etc/security/access-2fa-bypass.conf
# Format: permission : users : origins

# YOUR PC's Public IP (when connecting via Cloudflare Tunnel)
# Find it: curl ifconfig.me (from your PC)
# + : ALL : YOUR_PC_PUBLIC_IP

# Your PC's Internal IP (on same network 192.168.12.x)
# Verified: 192.168.12.77 (Debbie-PC)
+ : ALL : 192.168.12.77

# Cloudflare IP ranges (optional - if you want to allow all Cloudflare IPs)
# WARNING: This is less secure - only your PC should bypass
# + : ALL : 104.16.0.0/12
# + : ALL : 172.64.0.0/13

# Block all others (require 2FA for VM101, etc.)
- : ALL : ALL
```

**Important Notes:**
- ⚠️ **Only add YOUR PC's IP** - not VM101's IP (<VM101_IP>)
- ⚠️ **VM101 should still require 2FA** - don't add <VM101_IP> to bypass list
- ✅ Your PC → No 2FA (convenient direct access)
- ✅ VM101 → 2FA required (secure automation)
- ✅ All other IPs → 2FA required

**Testing Bypass:**

```bash
# From your PC (should bypass 2FA):
ssh proxy1@shenron.lightspeedup.com
# Expected: No 2FA prompt, direct access

# From VM101 (should require 2FA):
ssh proxy1@<VM120_IP>
# Expected: SMS sent, 2FA code required
```

**⚠️ Security Notes:**
- Only add YOUR PC's IP (not VM101's IP)
- Monitor `/var/log/auth.log` to verify bypass is working correctly
- Consider using dynamic DNS if your IP changes frequently
- Review bypass list regularly

---

## 📋 DEPLOYMENT CHECKLIST

### **On Each Target VM (VM120, VM150, VM160, VM170, VM180):**

- [ ] Install `libpam-google-authenticator`
- [ ] Generate Google Authenticator secret for SSH user
- [ ] Configure PAM (`/etc/pam.d/sshd`)
- [ ] Configure SSH (`/etc/ssh/sshd_config`)
- [ ] Create SMS notification script
- [ ] Test SMS delivery
- [ ] Test SSH connection with 2FA
- [ ] Remove `nullok` from PAM config (after all users have 2FA)
- [ ] Setup automation bypass (if needed)

### **On VM101 (Control Node):**

- [ ] Install Google Authenticator app on phone
- [ ] Scan QR codes from each VM
- [ ] Test SSH connections with 2FA
- [ ] Setup web approval interface (optional)
- [ ] Configure automation scripts to use bypass (if needed)

---

## 🔒 SECURITY CONSIDERATIONS

### **Strengths:**
- ✅ Adds second factor even if SSH keys compromised
- ✅ SMS notification alerts you to all SSH attempts
- ✅ Time-based codes (TOTP) are secure
- ✅ Can see who's trying to access what

### **Weaknesses:**
- ⚠️ SMS can be intercepted (use encrypted channels if possible)
- ⚠️ Requires phone to be available
- ⚠️ Breaks full automation (need bypass mechanism)
- ⚠️ Single point of failure (your phone)

### **Best Practices:**
- ✅ Store emergency codes securely
- ✅ Use encrypted SMS or app-based notifications
- ✅ Monitor 2FA logs for suspicious activity
- ✅ Have backup authentication method
- ✅ Test regularly to ensure it works

---

## 🧪 TESTING

### **Test 1: Normal SSH with 2FA**
```bash
# From VM101
ssh proxy1@<VM120_IP> "hostname"

# Expected:
# 1. SMS received
# 2. Prompt for verification code
# 3. Enter code from Google Authenticator
# 4. Connection succeeds
```

### **Test 2: Invalid Code**
```bash
# Enter wrong code
# Expected: Authentication failure
```

### **Test 3: IP-Based Bypass (Your PC)**
```bash
# From your PC via shenron.lightspeedup.com or MobaXterm
ssh proxy1@shenron.lightspeedup.com
# Expected: No 2FA prompt, direct access

# Verify your IP is in bypass list
sudo cat /etc/security/access-2fa-bypass.conf
```

### **Test 4: VM101 Still Requires 2FA**
```bash
# From VM101 (should still require 2FA)
ssh proxy1@<VM120_IP>
# Expected: SMS sent, 2FA code required
```

---

## 📱 GOOGLE AUTHENTICATOR SETUP

**On Your Phone:**

1. Install **Google Authenticator** app (iOS/Android)
2. For each VM, scan QR code generated by `google-authenticator`
3. Label each entry: "VM120 SSH", "VM150 SSH", etc.
4. Save emergency codes in password manager

**Emergency Codes:**
- Generated during `google-authenticator` setup
- Use if phone is lost/unavailable
- Store securely (password manager)

---

## 🔧 TROUBLESHOOTING

### **Issue: 2FA prompt not appearing**
```bash
# Check PAM configuration
cat /etc/pam.d/sshd | grep google

# Check SSH configuration
grep -i "ChallengeResponseAuthentication\|UsePAM\|AuthenticationMethods" /etc/ssh/sshd_config

# Check SSH logs
sudo tail -f /var/log/auth.log
```

### **Issue: SMS not received**
```bash
# Test SMS script manually
sudo /usr/local/bin/ssh-2fa-notify.sh

# Check logs
tail -f /var/log/ssh-2fa.log

# Verify phone number format (+1234567890)
```

### **Issue: Code always invalid**
```bash
# Check time sync on VM
sudo ntpdate -s time.nist.gov

# Verify secret in ~/.google_authenticator matches phone
# Regenerate if needed
```

---

## 📚 REFERENCES

- **Google Authenticator PAM:** https://github.com/google/google-authenticator-libpam
- **Twilio SMS API:** https://www.twilio.com/docs/sms
- **PAM Documentation:** https://linux.die.net/man/8/pam
- **SSH 2FA Guide:** https://www.digitalocean.com/community/tutorials/how-to-set-up-multi-factor-authentication-for-ssh-on-ubuntu-20-04

---

**Last Updated:** November 23, 2025  
**Status:** 📋 Implementation Guide Ready

