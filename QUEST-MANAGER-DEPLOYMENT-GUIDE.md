# 🐉 SHENRON ETERNAL QUEST MANAGER - Deployment Guide

**Version:** 1.0 (Phase 1)  
**Date:** November 6, 2025  
**Status:** Ready for Deployment

---

## 🎯 **WHAT IS THIS?**

The **SHENRON Eternal Quest Manager** is an autonomous background agent that:
- ✅ Runs continuously in the background
- ✅ Takes complex problems and tries solutions non-stop
- ✅ Learns from successes and failures
- ✅ Uses all 6 AI warriors (via SHENRON orchestrator)
- ✅ Saves progress so it can run for days/weeks
- ✅ Notifies you when it finds solutions

**Perfect for:** Crypto puzzles, optimization problems, research tasks, any complex challenge that needs persistent exploration.

---

## 📦 **PHASE 1 FEATURES**

### **Core System**
- ✅ Quest database (SQLite)
- ✅ Quest Manager service (Windows background)
- ✅ Autonomous attempt loop
- ✅ Learning from past attempts
- ✅ Integration with SHENRON orchestrator
- ✅ Progress tracking

### **API Endpoints**
- ✅ Create/Start/Pause/Stop quests
- ✅ Get quest status
- ✅ View attempt history
- ✅ Statistics dashboard

### **Not in Phase 1** (Coming in Phase 2)
- Web UI (manual API calls for now)
- Notifications (email/Discord)
- Multi-step workflows
- Actual solution testing (Phase 1 uses AI consensus)

---

## 🚀 **QUICK START DEPLOYMENT**

### **Step 1: Download Files from GitHub**

```powershell
# On VM100
cd C:\GOKU-AI\shenron

# Download from GitHub (or copy from repo)
# Files needed:
#   - quest_manager.py
#   - quest_api.py
#   - deploy-quest-manager.ps1
```

### **Step 2: Run Deployment Script**

```powershell
cd C:\GOKU-AI\shenron
.\deploy-quest-manager.ps1
```

**This will:**
1. Copy files to correct locations
2. Initialize SQLite database
3. Install Windows service (SHENRON-QUESTS)
4. Start the service

### **Step 3: Verify Deployment**

```powershell
# Check service status
Get-Service SHENRON-QUESTS

# Check database
dir C:\GOKU-AI\quests.db

# Check logs
Get-Content C:\GOKU-AI\quest-service.log -Tail 20
```

---

## 📝 **MANUAL DEPLOYMENT (If Script Fails)**

### **1. Copy Files**

```powershell
# Create directory if needed
New-Item -Path C:\GOKU-AI\shenron -ItemType Directory -Force

# Copy Python files
Copy-Item quest_manager.py C:\GOKU-AI\shenron\
Copy-Item quest_api.py C:\GOKU-AI\shenron\
```

### **2. Initialize Database**

```powershell
cd C:\GOKU-AI\shenron
C:\GOKU-AI\venv\Scripts\python.exe -c "from quest_manager import QuestDatabase; db = QuestDatabase(); print('Database initialized'); db.close()"
```

### **3. Create Service Wrapper**

Create `C:\GOKU-AI\shenron\quest_service.py`:

```python
import sys
sys.path.insert(0, 'C:/GOKU-AI/shenron')
from quest_manager import QuestManager
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('C:/GOKU-AI/quest-service.log'),
        logging.StreamHandler()
    ]
)

if __name__ == '__main__':
    manager = QuestManager()
    print('SHENRON Quest Manager Service starting...')
    try:
        manager.run_manager_loop(delay_seconds=60)
    except KeyboardInterrupt:
        print('Service stopped')
    finally:
        manager.stop()
```

### **4. Install Windows Service**

```powershell
# Install service using NSSM
C:\ProgramData\nssm\nssm.exe install "SHENRON-QUESTS" `
    "C:\GOKU-AI\venv\Scripts\python.exe" `
    "C:\GOKU-AI\shenron\quest_service.py"

# Configure service
C:\ProgramData\nssm\nssm.exe set "SHENRON-QUESTS" DisplayName "SHENRON Quest Manager"
C:\ProgramData\nssm\nssm.exe set "SHENRON-QUESTS" Description "SHENRON Eternal Quest Manager - Autonomous Problem Solving"
C:\ProgramData\nssm\nssm.exe set "SHENRON-QUESTS" Start SERVICE_AUTO_START
C:\ProgramData\nssm\nssm.exe set "SHENRON-QUESTS" AppDirectory "C:\GOKU-AI\shenron"

# Start service
Start-Service -Name "SHENRON-QUESTS"
```

---

## 🎮 **USING THE QUEST MANAGER**

### **Option 1: Command Line**

```powershell
cd C:\GOKU-AI\shenron

# Create a quest
C:\GOKU-AI\venv\Scripts\python.exe quest_manager.py create "Find the optimal Apache configuration for 10000 users"

# Output: Quest created: ID=1

# Start the quest
C:\GOKU-AI\venv\Scripts\python.exe quest_manager.py start 1

# Check status
C:\GOKU-AI\venv\Scripts\python.exe quest_manager.py status 1

# Run quest manually (for testing)
C:\GOKU-AI\venv\Scripts\python.exe quest_manager.py run 1
```

### **Option 2: Python API**

```python
from quest_manager import QuestManager

manager = QuestManager()

# Create quest
quest_id = manager.create_quest(
    goal="Solve the crypto puzzle from GSMG.IO repository",
    strategy="adaptive",
    priority=10,
    max_attempts=1000,
    timeout_minutes=10080  # 1 week
)

# Start quest
manager.start_quest(quest_id)

# Check status
status = manager.get_quest_status(quest_id)
print(status)
```

### **Option 3: REST API** (Start API first)

```powershell
# Start Quest API server (separate terminal)
cd C:\GOKU-AI\shenron
C:\GOKU-AI\venv\Scripts\python.exe quest_api.py
```

Then use curl or PowerShell:

```powershell
# Create quest
$body = @{
    goal = "Optimize Plex transcoding for 4K 60fps"
    strategy = "adaptive"
    priority = 8
    max_attempts = 100
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5001/api/quest/create" `
    -Method Post -Body $body -ContentType "application/json"

# List quests
Invoke-RestMethod -Uri "http://localhost:5001/api/quest/list"

# Get quest details
Invoke-RestMethod -Uri "http://localhost:5001/api/quest/1"

# Start quest
Invoke-RestMethod -Uri "http://localhost:5001/api/quest/1/start" -Method Post

# Get stats
Invoke-RestMethod -Uri "http://localhost:5001/api/quest/stats"
```

---

## 💡 **EXAMPLE USE CASES**

### **1. Crypto Puzzle Solving**

```python
manager.create_quest(
    goal="Solve Bitcoin puzzle #64 from privatekeys.pw",
    strategy="exhaustive",
    max_attempts=-1,  # No limit
    timeout_minutes=43200  # 30 days
)
```

**What happens:**
- Quest runs 24/7
- Tries different approaches (brute force, pattern recognition, math analysis)
- Learns what doesn't work
- Keeps trying until solved or you stop it

### **2. Server Optimization**

```python
manager.create_quest(
    goal="Find Apache config that handles 10,000 concurrent users with <100ms response time",
    strategy="adaptive",
    max_attempts=500
)
```

**What happens:**
- Tries different configurations
- Tests each approach (Phase 2 will actually test, Phase 1 evaluates via AI)
- Learns from failures
- Finds optimal solution

### **3. Research Task**

```python
manager.create_quest(
    goal="Research and summarize all NVIDIA GRID K1 GPU passthrough solutions for Proxmox 8.x",
    strategy="comprehensive",
    max_attempts=50
)
```

---

## 📊 **MONITORING QUESTS**

### **Check Service Status**

```powershell
Get-Service SHENRON-QUESTS

# Should show: Running
```

### **View Logs**

```powershell
# Service log
Get-Content C:\GOKU-AI\quest-service.log -Tail 50 -Wait

# Quest Manager log
Get-Content C:\GOKU-AI\quest-manager.log -Tail 50 -Wait
```

### **Database Queries**

```powershell
# Install SQLite tools if needed
# Then query database directly
sqlite3 C:\GOKU-AI\quests.db "SELECT * FROM quests"
sqlite3 C:\GOKU-AI\quests.db "SELECT * FROM attempts ORDER BY timestamp DESC LIMIT 10"
```

---

## 🔧 **CONFIGURATION**

### **Quest Parameters**

| Parameter | Description | Default |
|-----------|-------------|---------|
| `goal` | What you want to solve | Required |
| `strategy` | `adaptive`, `exhaustive`, `comprehensive` | `adaptive` |
| `priority` | 1-10 (higher = more important) | 5 |
| `max_attempts` | Max attempts before stopping (-1 = unlimited) | -1 |
| `timeout_minutes` | Max time before stopping (-1 = unlimited) | -1 |
| `metadata` | Custom data (JSON) | {} |

### **Service Configuration**

Edit timing in `quest_service.py`:

```python
manager.run_manager_loop(delay_seconds=60)  # 60 = 1 minute between attempts
```

**Recommendations:**
- Fast testing: 10-30 seconds
- Normal use: 60-120 seconds
- Resource-intensive: 300-600 seconds (5-10 min)

---

## 🐛 **TROUBLESHOOTING**

### **Service Won't Start**

```powershell
# Check if Python path is correct
C:\GOKU-AI\venv\Scripts\python.exe --version

# Check if SHENRON API is running
Invoke-RestMethod http://localhost:5000/health

# View service error log
Get-Content C:\GOKU-AI\quest-service-stderr.log
```

### **Database Errors**

```powershell
# Reinitialize database
Remove-Item C:\GOKU-AI\quests.db
cd C:\GOKU-AI\shenron
C:\GOKU-AI\venv\Scripts\python.exe -c "from quest_manager import QuestDatabase; QuestDatabase()"
```

### **Quest Not Making Progress**

```powershell
# Check quest status
C:\GOKU-AI\venv\Scripts\python.exe quest_manager.py status <quest_id>

# Check if SHENRON is responding
Invoke-RestMethod -Uri "http://localhost:5000/api/shenron/grant-wish" `
    -Method Post -Body '{"query":"test","use_rag":false}' `
    -ContentType "application/json"

# Check recent attempts
sqlite3 C:\GOKU-AI\quests.db "SELECT * FROM attempts WHERE quest_id=<id> ORDER BY timestamp DESC LIMIT 5"
```

---

## 🚀 **NEXT STEPS (Phase 2)**

After Phase 1 is working, we'll add:
- ✅ Web UI dashboard
- ✅ Real-time notifications (Discord, email)
- ✅ Actual solution testing (not just AI evaluation)
- ✅ Multi-step workflows
- ✅ Cross-quest learning
- ✅ Resource limits (CPU/RAM)
- ✅ Quest templates
- ✅ Export/import quests

---

## 📞 **SUPPORT**

**Files:**
- `quest_manager.py` - Core quest system
- `quest_api.py` - REST API server
- `quest_service.py` - Windows service wrapper
- `deploy-quest-manager.ps1` - Deployment script

**Logs:**
- `C:\GOKU-AI\quest-manager.log` - Quest Manager log
- `C:\GOKU-AI\quest-service.log` - Service log
- `C:\GOKU-AI\quest-service-stdout.log` - Service stdout
- `C:\GOKU-AI\quest-service-stderr.log` - Service errors

**Database:**
- `C:\GOKU-AI\quests.db` - SQLite database

---

## ✅ **SUCCESS CRITERIA**

**You'll know it's working when:**
1. ✅ Service shows "Running"
2. ✅ Database file exists
3. ✅ Can create quests via CLI
4. ✅ Quest attempts appear in logs
5. ✅ Quest status updates over time

---

**Ready to solve problems autonomously! 🐉🧠⚡**

*SHENRON Eternal Quest Manager v1.0 - Never Give Up, Never Surrender*

