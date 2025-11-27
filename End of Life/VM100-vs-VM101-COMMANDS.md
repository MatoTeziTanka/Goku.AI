<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🖥️ VM100 vs VM101 - Command Reference

**Purpose:** Clarify which commands run on which VM  
**Last Updated:** January 2025

---

## 📋 QUICK REFERENCE

| Service/Component | VM | OS | Access Method |
|-------------------|----|----|---------------|
| **LM Studio** | VM100 | Windows Server 2025 | RDP or SSH |
| **SHENRON API** | VM100 | Windows Server 2025 | Port 5000 (HTTP) |
| **ChromaDB** | VM100 | Windows Server 2025 | Local file system |
| **Knowledge Base** | VM100 | Windows Server 2025 | Local file system |
| **code-server** | VM101 | Ubuntu 24.04 | Port 8080/8081 (HTTP) |
| **Multi-Agent System** | VM101 | Ubuntu 24.04 | Port 8001 (HTTP) |
| **Docker** | VM101 | Ubuntu 24.04 | Rootless mode |
| **Git Repositories** | VM101 | Ubuntu 24.04 | Local file system |

---

## 🖥️ VM100 (Windows Server 2025) - AI Services

**IP:** <VM100_IP>  
**Hostname:** GOKU-AI  
**User:** Administrator  
**Access:** RDP (port 3389) or SSH (port 22)

### **Services Running on VM100:**

1. **LM Studio** (Port 1234)
   ```powershell
   # Check LM Studio status
   Invoke-RestMethod http://localhost:1234/v1/models
   
   # Check if running
   Get-Process | Where-Object {$_.ProcessName -like "*lmstudio*"}
   ```

2. **SHENRON API** (Port 5000)
   ```powershell
   # Check SHENRON API health
   Invoke-RestMethod http://localhost:5000/health
   
   # Check service status
   Get-Service SHENRON
   ```

3. **ChromaDB** (Local)
   ```powershell
   # Check ChromaDB location
   Test-Path C:\GOKU-AI\chroma_db\
   
   # Check size
   Get-ChildItem C:\GOKU-AI\chroma_db\ -Recurse | Measure-Object -Property Length -Sum
   ```

4. **Knowledge Base** (Local)
   ```powershell
   # List knowledge base files
   Get-ChildItem C:\GOKU-AI\knowledge-base\ -Filter *.md
   ```

### **Commands for VM100:**

**Via SSH (from VM101):**
```bash
# SSH to VM100
ssh Administrator@<VM100_IP>

# Run PowerShell commands remotely
ssh Administrator@<VM100_IP> "powershell -Command 'Get-Service SHENRON'"
```

**Via RDP:**
- Connect to <VM100_IP>:3389
- Login as Administrator
- Use PowerShell or Command Prompt

**Note:** PowerShell is broken on VM100, so use alternative methods or fix PowerShell first.

---

## 🐧 VM101 (Ubuntu 24.04) - Control Node

**IP:** <VM101_IP> (primary), <EDGEROUTER_IP>81 (secondary)  
**Hostname:** Goku  
**User:** mgmt1  
**Access:** SSH (port 22)

### **Services Running on VM101:**

1. **code-server** (Port 8080 or 8081)
   ```bash
   # Check if running
   ps aux | grep code-server
   sudo ss -tulnp | grep 8080
   
   # Start code-server
   code-server --bind-addr 0.0.0.0:8080
   ```

2. **Multi-Agent System** (Port 8001)
   ```bash
   # Check status
   ps aux | grep uvicorn
   curl http://localhost:8001/health 2>/dev/null
   
   # Location
   ls -la ~/multi-agent-system/backend/
   ```

3. **Docker** (Rootless)
   ```bash
   # Check if rootless Docker is initialized
   ls -la ~/.docker/run/docker.sock
   
   # Initialize rootless Docker (if needed)
   dockerd-rootless-setuptool.sh install
   
   # Add to PATH (if needed)
   export PATH=$PATH:/usr/bin
   ```

4. **Git Repositories**
   ```bash
   # List repositories
   ls -la ~/GitHub/
   
   # Sync repositories
   cd ~/GitHub/Dell-Server-Roadmap
   git pull
   ```

### **Commands for VM101:**

**All commands run on VM101 via SSH:**
```bash
# SSH to VM101
ssh mgmt1@<VM101_IP>

# Run commands directly
```

---

## 🔄 Commands That Connect Between VMs

### **From VM101 to VM100:**

```bash
# Test SSH connection
ssh Administrator@<VM100_IP> "hostname"

# Check SHENRON API from VM101
curl http://<VM100_IP>:5000/health

# Check LM Studio from VM101
curl http://<VM100_IP>:1234/v1/models

# Copy files from VM100 to VM101
scp Administrator@<VM100_IP>:C:/GOKU-AI/chroma_db/* ~/backups/chroma_db/

# Copy files from VM101 to VM100
scp ~/GitHub/Dell-Server-Roadmap/backend/shenron/* Administrator@<VM100_IP>:C:/GOKU-AI/shenron/
```

### **From VM100 to VM101:**

```powershell
# Test connection (if PowerShell works)
Test-NetConnection -ComputerName <VM101_IP> -Port 22

# Or via SSH (if SSH client installed)
ssh mgmt1@<VM101_IP> "hostname"
```

---

## 🎯 Common Tasks

### **Deploy SHENRON Updates (VM101 → VM100)**

```bash
# On VM101
cd ~/GitHub/Dell-Server-Roadmap/backend/shenron

# Copy orchestrator to VM100
scp shenron_v4_orchestrator.py Administrator@<VM100_IP>:C:/GOKU-AI/shenron/

# Restart SHENRON service on VM100
ssh Administrator@<VM100_IP> "powershell -Command 'Restart-Service SHENRON'"
```

### **Backup ChromaDB (VM100 → VM101)**

```bash
# On VM101
mkdir -p ~/backups/chroma_db_$(date +%Y%m%d)
scp -r Administrator@<VM100_IP>:C:/GOKU-AI/chroma_db/ ~/backups/chroma_db_$(date +%Y%m%d)/
```

### **Update Knowledge Base (VM100)**

```powershell
# On VM100 (via RDP or SSH)
cd C:\GOKU-AI\shenron
C:\GOKU-AI\venv\Scripts\python.exe 2-Ingest-Knowledge-Base.py
```

### **Check All Services Status (From VM101)**

```bash
# On VM101 - Check all services
echo "=== VM100 Services ==="
curl -s http://<VM100_IP>:5000/health | jq . || echo "SHENRON API down"
curl -s http://<VM100_IP>:1234/v1/models | jq '.data[].id' | head -3 || echo "LM Studio down"

echo ""
echo "=== VM101 Services ==="
ps aux | grep -E "code-server|uvicorn" | grep -v grep
sudo ss -tulnp | grep -E ":8080|:8001"
```

---

## ⚠️ Important Notes

1. **PowerShell is broken on VM100** - Use alternative methods:
   - RDP and use Command Prompt
   - SSH and use `cmd.exe` commands
   - Fix PowerShell first

2. **Docker on VM101** - Rootless mode:
   - May need initialization: `dockerd-rootless-setuptool.sh install`
   - Check PATH: `which docker` or `docker --version`
   - Socket location: `~/.docker/run/docker.sock`

3. **code-server on VM101** - Now working:
   - Port 8080: Available (HTTP server stopped)
   - Port 8081: Alternative option
   - **Security:** Authentication is disabled - consider enabling

4. **Network Access:**
   - VM101 can access VM100 services (ports 1234, 5000)
   - VM100 can access VM101 services (ports 8080, 8001)
   - Firewall rules allow these connections

---

## 📝 Quick Command Cheat Sheet

**VM100 (Windows):**
- LM Studio: `http://<VM100_IP>:1234`
- SHENRON API: `http://<VM100_IP>:5000`
- SSH: `ssh Administrator@<VM100_IP>`

**VM101 (Ubuntu):**
- code-server: `http://<VM101_IP>:8080` or `:8081`
- Multi-Agent: `http://<VM101_IP>:8001`
- SSH: `ssh mgmt1@<VM101_IP>`

---

**Summary:** Most commands you ran are correct for VM101. Docker just needs PATH setup or rootless initialization. VM100 commands are for Windows/PowerShell and access LM Studio/SHENRON services.




