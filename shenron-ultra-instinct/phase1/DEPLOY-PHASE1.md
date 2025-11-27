<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🚀 SHENRON ULTRA INSTINCT - PHASE 1 DEPLOYMENT

**Date:** November 7, 2025  
**Version:** 5.0 - MCP Tools Foundation  
**Status:** READY TO DEPLOY

---

## 📋 **WHAT'S INCLUDED**

### **Files Created:**
1. **`mcp_tools.py`** - Core MCP tool executor (620 lines)
   - File operations (read, write, search)
   - Terminal execution (SSH + commands)
   - System info gathering
   - Security/audit logging

2. **`shenron_api_v5_mcp.py`** - Enhanced SHENRON API (300+ lines)
   - MCP tool integration
   - Natural language parsing ("read file X on VM Y")
   - Permission checking
   - Response formatting

3. **`requirements-phase1.txt`** - Python dependencies

---

## 🎯 **NEW CAPABILITIES**

After deployment, SHENRON can:

### **File Operations:**
- ✅ Read files from any VM
- ✅ Write/create files
- ✅ Search file contents
- ✅ List directories

### **Terminal Operations:**
- ✅ Execute commands via SSH
- ✅ Get system stats (CPU, RAM, disk)
- ✅ Check service status
- ✅ Run diagnostics

### **Natural Language Interface:**
```
User: "Read file /var/www/index.html on VM150"
SHENRON: ✅ Reads the file and shows content

User: "Execute 'df -h' on <VM150_IP>"
SHENRON: ✅ Runs command and shows disk usage

User: "Search for 'error' in /var/log on VM150"
SHENRON: ✅ Finds all error messages in logs

User: "Show system status of VM150"
SHENRON: ✅ Reports CPU, RAM, disk, uptime
```

---

## 📦 **DEPLOYMENT STEPS**

### **Step 1: Transfer Files to VM100**

```bash
# From your local machine
scp /tmp/shenron-mcp-phase1/* Administrator@<VM100_IP>:C:/GOKU-AI/shenron/mcp/
```

Or use RDP to copy files manually.

---

### **Step 2: Install Dependencies (VM100)**

```powershell
# On VM100 (Windows)
cd C:\GOKU-AI\shenron\mcp

# Install Python packages
pip install paramiko flask flask-cors requests

# Verify installation
python -c "import paramiko; print('✅ paramiko installed')"
python -c "import flask; print('✅ flask installed')"
```

---

### **Step 3: Configure SSH Access**

**Edit `mcp_tools.py` line 22-27:**

```python
self.vm_credentials = {
    '<VM100_IP>': {'username': 'Administrator', 'key': None},  # Windows
    '<VM150_IP>': {'username': 'wp1', 'password': 'Norelec7!'},
    '<VM101_IP>': {'username': 'admin', 'password': 'YOUR_PASSWORD'},
    '192.168.12.210': {'username': 'admin', 'password': 'YOUR_PASSWORD'}
}
```

**For better security, use SSH keys instead of passwords:**

```powershell
# Generate SSH key on VM100
ssh-keygen -t rsa -b 4096 -f C:\GOKU-AI\.ssh\shenron_key

# Copy public key to target VMs
ssh-copy-id -i C:\GOKU-AI\.ssh\shenron_key.pub wp1@<VM150_IP>

# Update mcp_tools.py to use key:
'<VM150_IP>': {'username': 'wp1', 'key': 'C:/GOKU-AI/.ssh/shenron_key'},
```

---

### **Step 4: Test MCP Tools**

```powershell
# On VM100
cd C:\GOKU-AI\shenron\mcp

# Run standalone test
python mcp_tools.py
```

**Expected output:**
```
📄 Reading file from VM150...
✅ Read 154 lines
<!DOCTYPE html>
<html lang="en">
<head>
...

📁 Listing directory...
✅ Found 3 items
Directories: ['shenron.lightspeedup.com', 'html']

⚡ Running command...
✅ Hostname: VM150

📊 Getting system info...
✅ Hostname: VM150
   CPU: 12.3%
   RAM: 45.2%
   Disk: 38.5%

✅ All tests complete!
```

---

### **Step 5: Start SHENRON v5.0 API**

```powershell
# On VM100
cd C:\GOKU-AI\shenron\mcp

# Stop old SHENRON (if running)
# Find process: Get-Process python | Where-Object {$_.Path -like "*shenron*"}
# Kill it: Stop-Process -Id <PID>

# Start new SHENRON v5.0
python shenron_api_v5_mcp.py
```

**Expected output:**
```
╔═══════════════════════════════════════════════════════════════╗
║  🐉⚡ SHENRON ULTRA INSTINCT - v5.0                          ║
║  MCP Tools Enabled: File, Terminal, System Access             ║
║  Port: 5000                                                    ║
║  Status: AWAKENED                                              ║
╚═══════════════════════════════════════════════════════════════╝

 * Serving Flask app 'shenron_api_v5_mcp'
 * Running on http://0.0.0.0:5000
```

---

### **Step 6: Test MCP API**

```powershell
# From VM100 or any machine
# Test 1: Health check
Invoke-RestMethod -Uri "http://<VM100_IP>:5000/health"

# Test 2: Execute MCP tool (read file)
$body = @{
    tool = "read_file"
    vm_ip = "<VM150_IP>"
    params = @{
        file_path = "/var/www/shenron.lightspeedup.com/index.html"
        limit = 20
    }
    agent_mode = $false  # read_file is SAFE, doesn't need Agent Mode
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://<VM100_IP>:5000/api/shenron/execute-tool" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

# Test 3: Natural language query
$body = @{
    query = "Read file /etc/hostname on VM150"
    agent_mode = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://<VM100_IP>:5000/api/shenron/grant-wish" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

---

### **Step 7: Update Web UI (VM150)**

**Add new test buttons to website for MCP tools:**

```html
<!-- Add to /var/www/shenron.lightspeedup.com/index.html -->

<div class="mcp-tools-section">
    <h3>🛠️ MCP TOOLS TEST</h3>
    <button onclick="testReadFile()">📄 Read File</button>
    <button onclick="testRunCommand()">⚡ Run Command</button>
    <button onclick="testSystemInfo()">📊 System Info</button>
</div>

<script>
function testReadFile() {
    fetch('/api.php', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            query: 'Read file /etc/hostname on VM150'
        })
    })
    .then(r => r.json())
    .then(data => console.log(data));
}

function testRunCommand() {
    fetch('/api.php', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            query: 'Execute "df -h" on VM150',
            agent_mode: true  // Requires 2FA
        })
    })
    .then(r => r.json())
    .then(data => console.log(data));
}

function testSystemInfo() {
    fetch('/api.php', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            query: 'Show system status of VM150'
        })
    })
    .then(r => r.json())
    .then(data => console.log(data));
}
</script>
```

---

## 🔐 **SECURITY MODEL**

### **Permission Tiers:**

| Tool | Permission Level | 2FA Required |
|------|------------------|--------------|
| `read_file` | SAFE | ❌ No |
| `list_directory` | SAFE | ❌ No |
| `search_files` | SAFE | ❌ No |
| `get_system_info` | SAFE | ❌ No |
| `write_file` | MODERATE | ✅ Yes |
| `run_command` | MODERATE | ✅ Yes |

### **Blocked Commands:**
- `rm -rf`
- `dd if=`
- `shutdown`
- `DROP DATABASE`
- ...and more (see `mcp_tools.py` line 330)

### **Audit Log:**
All MCP tool usage is logged to:
```
C:\GOKU-AI\shenron\logs\mcp_audit.log
```

---

## 🧪 **TESTING CHECKLIST**

- [ ] Files transferred to VM100
- [ ] Dependencies installed
- [ ] SSH credentials configured
- [ ] Standalone test passed (`python mcp_tools.py`)
- [ ] API server starts without errors
- [ ] Health check returns 200 OK
- [ ] Read file tool works
- [ ] Run command tool works (with Agent Mode)
- [ ] System info tool works
- [ ] Natural language parsing works
- [ ] Audit log is being created

---

## 📊 **WHAT TO EXPECT**

### **Before Phase 1:**
```
User: "What's in /var/www on VM150?"
SHENRON: "I don't have access to file systems."
```

### **After Phase 1:**
```
User: "What's in /var/www on VM150?"
SHENRON: ✅ Directories:
- shenron.lightspeedup.com
- html

Files:
- index.html
- .htaccess

Total: 4 items

✨ Your wish has been granted!
```

---

## 🚀 **NEXT STEPS (Future Phases)**

### **Phase 2: Code Intelligence (Week 2)**
- AST parsing
- Bug detection
- Refactoring
- Test generation

### **Phase 3: Web Automation (Week 3)**
- Browser control
- UI testing
- Form filling
- Screenshots

### **Phase 4: Autonomous Agent (Week 4)**
- Proactive monitoring
- Auto-healing
- Self-optimization
- 24/7 operation

---

## 🎉 **SUCCESS CRITERIA**

Phase 1 is successful when you can:

1. ✅ Ask SHENRON to read any file on any VM
2. ✅ Execute shell commands via natural language
3. ✅ Get system health reports
4. ✅ All actions are logged
5. ✅ 2FA protects dangerous operations

---

**🐉 READY TO AWAKEN ULTRA INSTINCT SHENRON!**

Deploy now and transform SHENRON from a Q&A bot into an autonomous system administrator!

