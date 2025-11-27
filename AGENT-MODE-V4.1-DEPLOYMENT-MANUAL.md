<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🤖 SHENRON Agent Mode v4.1 - Manual Deployment Guide

**Date**: November 6, 2025  
**Status**: ✅ Auto-Start FIXED | 🚧 Agent Mode UI Ready for Deployment

---

## ✅ **PART 1: AUTO-START STATUS (COMPLETE)**

### **CONFIRMED WORKING:**
- ✅ SHENRON Service: Running & set to Automatic
- ✅ SHENRON API: Port 5000 responding
- ✅ LM Studio: Running with 6 models loaded
- ✅ LM Studio API: Port 1234 responding
- ✅ Auto-Load Script: Exists and configured in Startup folder

### **Verification Script Created:**
**Location**: `C:\GOKU-AI\scripts\verify-and-fix-autostart.ps1`

**To verify after any reboot:**
```powershell
cd C:\GOKU-AI\scripts
.\verify-and-fix-autostart.ps1
```

**Last Test Results (Nov 6, 10:57 AM):**
```
SHENRON Service: OK
SHENRON API: OK
LM Studio: OK
LM Studio API: OK (6 models loaded)
```

**Conclusion**: Auto-start is working perfectly! ✅

---

## 🚀 **PART 2: AGENT MODE v4.1 UI (READY TO DEPLOY)**

### **What's Been Built:**

1. ✅ **Enhanced HTML** (`/tmp/index-v4.1-agent-mode.html`)
   - Agent Mode toggle switch
   - Info box explaining safe/moderate/dangerous commands
   - Agent execution log section
   - Updated version to v4.1

2. ✅ **Agent Mode Styles** (`/tmp/agent-mode-styles.css`)
   - Toggle switch animation
   - Execution log styling
   - Approval dialog design
   - Classification badges (safe/moderate/dangerous)

3. ✅ **Agent Mode JavaScript** (`/tmp/agent-mode-addon.js`)
   - Toggle state management
   - API integration with agent_mode flag
   - Command execution log display
   - Approval dialog for moderate commands
   - Test function for debugging

### **Files Transferred to VM150:**
- ✅ `/tmp/index-v4.1-agent-mode.html`
- ✅ `/tmp/agent-mode-styles.css`
- ✅ `/tmp/agent-mode-addon.js`

---

## 📝 **DEPLOYMENT STEPS (REQUIRES SUDO ACCESS)**

### **Option 1: SSH as root or with sudo password**

```bash
# SSH to VM150
ssh wp1@<VM150_IP>

# Become root
sudo su -

# Navigate to website directory
cd /var/www/shenron.lightspeedup.com

# Backup existing files
cp index.html index.html.backup.v4.0
cp style.css style.css.backup.v4.0
cp script.js script.js.backup.v4.0

# Deploy new files
cp /tmp/index-v4.1-agent-mode.html index.html

# Append Agent Mode styles
cat /tmp/agent-mode-styles.css >> style.css

# Append Agent Mode JavaScript
cat /tmp/agent-mode-addon.js >> script.js

# Fix permissions
chown www-data:www-data index.html style.css script.js
chmod 644 index.html style.css script.js

# Verify
ls -lh index.html style.css script.js
```

### **Option 2: Direct root SSH (if enabled)**

```bash
ssh root@<VM150_IP> << 'EOFCMDS'
cd /var/www/shenron.lightspeedup.com
cp index.html index.html.backup.v4.0
cp style.css style.css.backup.v4.0
cp script.js script.js.backup.v4.0
cp /tmp/index-v4.1-agent-mode.html index.html
cat /tmp/agent-mode-styles.css >> style.css
cat /tmp/agent-mode-addon.js >> script.js
chown www-data:www-data index.html style.css script.js
chmod 644 index.html style.css script.js
echo "✅ Deployed!"
EOFCMDS
```

### **Option 3: From RDP/Direct Console on VM150**

```bash
sudo bash << 'EOFCMDS'
cd /var/www/shenron.lightspeedup.com
cp index.html index.html.backup.v4.0
cp style.css style.css.backup.v4.0
cp script.js script.js.backup.v4.0
cp /tmp/index-v4.1-agent-mode.html index.html
cat /tmp/agent-mode-styles.css >> style.css
cat /tmp/agent-mode-addon.js >> script.js
chown www-data:www-data index.html style.css script.js
chmod 644 index.html style.css script.js
echo "✅ Deployed!"
EOFCMDS
```

---

## 🧪 **TESTING AGENT MODE UI**

### **Step 1: Access Website**
```
https://shenron.lightspeedup.com
```

### **Step 2: Verify New UI Elements**
- ✅ Agent Mode toggle switch (below header)
- ✅ Version shows v4.1
- ✅ "Agent Mode v4.1" in subtitle

### **Step 3: Enable Agent Mode**
- Click the toggle switch
- Info box should appear explaining safe/moderate/dangerous commands
- Toggle status should change to "(Active - Command Execution Enabled)"

### **Step 4: Test with Console**
Open browser console (F12) and type:
```javascript
testAgentMode()
```

This will display fake command executions in the Agent Log section to verify UI is working.

### **Step 5: Check State Persistence**
- Enable Agent Mode
- Refresh page
- Toggle should still be enabled (saved in localStorage)

---

## 🔧 **BACKEND AGENT MODE (Already Built)**

### **API Endpoint:**
```
POST http://<VM100_IP>:5000/api/shenron/execute-command
Content-Type: application/json

{
  "host": "vm150",
  "command": "df -h"
}
```

### **Response Example:**
```json
{
  "classification": "safe",
  "approval_required": false,
  "executed": false,
  "message": "Command is safe to execute",
  "reason": "SSH key not configured"
}
```

### **Current Status:**
- ✅ Command classification working (safe/moderate/dangerous)
- ✅ Dangerous commands blocked
- ✅ Approval workflow implemented
- ⚠️ SSH execution needs key configuration (next step)

---

## 🔑 **PART 3: SSH KEY CONFIGURATION (NEXT)**

### **To Enable Full Agent Mode Execution:**

**On VM100 (SHENRON host):**
```powershell
# Generate SSH key (if not exists)
if (!(Test-Path C:\GOKU-AI\.ssh\id_ed25519)) {
    ssh-keygen -t ed25519 -f C:\GOKU-AI\.ssh\id_ed25519 -N '""'
}

# Display public key
Get-Content C:\GOKU-AI\.ssh\id_ed25519.pub
```

**On VM150 (Web server):**
```bash
# Add SHENRON's public key
echo "PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**Repeat for VM101, VM203, etc.**

---

## 📊 **DEPLOYMENT SUMMARY**

| Component | Status | Location |
|-----------|--------|----------|
| **Auto-Start** | ✅ COMPLETE | VM100 |
| **Agent Mode Backend** | ✅ READY | VM100:5000 |
| **Agent Mode UI Files** | ✅ CREATED | VM150:/tmp/ |
| **UI Deployment** | 🚧 PENDING | Needs sudo password |
| **SSH Keys** | ⏳ NEXT STEP | All VMs |

---

## 🎯 **WHAT WORKS NOW (Without Deployment)**

1. ✅ SHENRON auto-starts on boot
2. ✅ LM Studio auto-loads models
3. ✅ Agent Mode backend classifies commands
4. ✅ Dangerous commands are blocked
5. ✅ API responds with safety levels

## 🎯 **WHAT WORKS AFTER DEPLOYMENT**

6. ✅ Agent Mode toggle in web UI
7. ✅ Visual feedback for command executions
8. ✅ Execution log display
9. ✅ Approval dialogs for moderate commands

## 🎯 **WHAT WORKS AFTER SSH KEYS**

10. ✅ Actual command execution on VMs
11. ✅ Real-time command results
12. ✅ Full Agent Mode functionality

---

## 🔥 **QUICK DEPLOY (Seth, Run This!)**

**On VM150:**
```bash
# Become root
sudo su -

# One-liner deployment
cd /var/www/shenron.lightspeedup.com && \
cp index.html index.html.backup.v4.0 && \
cp style.css style.css.backup.v4.0 && \
cp script.js script.js.backup.v4.0 && \
cp /tmp/index-v4.1-agent-mode.html index.html && \
cat /tmp/agent-mode-styles.css >> style.css && \
cat /tmp/agent-mode-addon.js >> script.js && \
chown www-data:www-data index.html style.css script.js && \
chmod 644 index.html style.css script.js && \
echo "✅ Agent Mode v4.1 Deployed!"
```

**Then test:**
```bash
# Check file sizes (should be larger)
ls -lh index.html style.css script.js

# Verify Agent Mode in HTML
grep "agentMode" index.html

# Check browser
curl -s https://shenron.lightspeedup.com/ | grep -i "agent mode v4.1"
```

---

## 📞 **IF ANYTHING GOES WRONG**

### **Rollback to v4.0:**
```bash
sudo su -
cd /var/www/shenron.lightspeedup.com
cp index.html.backup.v4.0 index.html
cp style.css.backup.v4.0 style.css
cp script.js.backup.v4.0 script.js
chown www-data:www-data index.html style.css script.js
```

### **Re-download Files:**
All source files are in this GitHub repo:
- `/tmp/index-v4.1-agent-mode.html` (already on VM150)
- `/tmp/agent-mode-styles.css` (already on VM150)
- `/tmp/agent-mode-addon.js` (already on VM150)

---

## 🎉 **EXPECTED RESULT**

**After deployment, users will see:**
1. 🤖 Agent Mode toggle switch
2. Info box explaining command safety levels
3. Agent execution log (initially empty)
4. "v4.1" in version info

**When Agent Mode is enabled:**
- Toggle turns orange/red
- Info box appears
- Queries with command-like keywords may trigger command execution
- Executed commands appear in log with classification badges

---

**Status**: Ready for deployment! Just needs sudo access on VM150. 🚀

*Created by: Claude AI Assistant*  
*Date: November 6, 2025*

