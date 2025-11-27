<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🚨 CRITICAL FIXES - November 6, 2025

**Issues Identified:**
1. ❌ Web UI header broken (my v4.1.1 deployment failed)
2. ❌ LM Studio not auto-loading 6 models on boot
3. ❌ SHENRON API may not be starting automatically  
4. ❌ Quest Manager maxing out CPU/RAM (stuck at attempt #9)
5. ❌ Auto-start sequence unreliable

---

## ✅ **FIX 1: WEB UI RESTORED** (COMPLETED)

**Problem:** My v4.1.1 changes broke the header layout

**Solution:** Rolled back to v4.0 (working version)

**Status:** ✅ **FIXED** - Site should now look correct

**Verify:** Visit https://shenron.lightspeedup.com

---

## ✅ **FIX 2: MASTER STARTUP SCRIPT** (DEPLOYED)

**Problem:** Too many moving parts at boot - Task Scheduler, VBScript, PowerShell scripts all competing

**Solution:** Created ONE master script to rule them all

**File:** `C:\GOKU-AI\START-SHENRON.ps1`

**What it does:**
1. ✅ Stops any existing LM Studio/Python processes (clean start)
2. ✅ Starts LM Studio and waits for it to be ready
3. ✅ Prompts you to manually load the 6 models (with list)
4. ✅ Verifies models are loaded
5. ✅ Starts SHENRON API server
6. ✅ Verifies everything is operational
7. ✅ Creates detailed log file

**How to use:**

### **Option A: Manual Start (Recommended for now)**
```powershell
# On VM100, open PowerShell as Administrator
cd C:\GOKU-AI
.\START-SHENRON.ps1
```

### **Option B: Desktop Shortcut**
1. Right-click desktop → New → Shortcut
2. Location: `powershell.exe -ExecutionPolicy Bypass -File "C:\GOKU-AI\START-SHENRON.ps1"`
3. Name: "🐉 Start SHENRON"
4. Right-click shortcut → Properties → Run as administrator

### **Option C: Auto-start on Boot**
```powershell
# Create scheduled task (run as Administrator)
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File C:\GOKU-AI\START-SHENRON.ps1"
$trigger = New-ScheduledTaskTrigger -AtLogOn
$principal = New-ScheduledTaskPrincipal -UserId "Administrator" -LogonType Interactive -RunLevel Highest
Register-ScheduledTask -TaskName "SHENRON-Startup" -Action $action -Trigger $trigger -Principal $principal -Description "Start SHENRON Syndicate on login"
```

---

## ❌ **FIX 3: QUEST MANAGER CPU/RAM ISSUE** (CRITICAL)

**Problem:** Quest Manager is maxing out 52 CPUs and 192GB RAM, stuck at attempt #9

**Root Cause:** Likely querying SHENRON which is querying 6 models which aren't loaded

**IMMEDIATE ACTION REQUIRED:**

```powershell
# On VM100, STOP Quest Manager NOW
Get-Process python | Where-Object {$_.CommandLine -like "*quest_manager*"} | Stop-Process -Force

# OR just reboot VM100
Restart-Computer
```

**DON'T run Quest Manager until:**
1. LM Studio is running
2. All 6 models are loaded
3. SHENRON API is responding
4. You've tested SHENRON with a simple query first

**Test SHENRON first:**
```powershell
# Simple health check
Invoke-RestMethod -Uri "http://localhost:5000/health"

# Simple query (should take 30-60 seconds)
Invoke-RestMethod -Uri "http://localhost:5000/api/shenron/grant-wish" -Method POST -Body (@{query="What is 2+2?"} | ConvertTo-Json) -ContentType "application/json"
```

**Only after SHENRON works, then try Quest Manager**

---

## 🔧 **FIX 4: MODEL AUTO-LOADING** (NOT POSSIBLE)

**Bad News:** LM Studio does NOT have a command-line interface for loading models

**Options:**

### **Option A: Manual Loading (Current best option)**
1. Start LM Studio (via master script or manually)
2. Go to "My Models" tab
3. Load these 6 models (click the load icon for each):
   - `qwen2.5-coder-72b-instruct` (GOKU)
   - `qwen2.5-32b-instruct` (VEGETA)
   - `qwen2.5-coder-14b-instruct` (PICCOLO)
   - `deepseek-coder-v2-lite-instruct` (GOHAN)
   - `mistral-7b-instruct-v0.3` (TRUNKS)
   - `llama-3.2-3b-instruct` (FRIEZA)

**The master script will pause and wait for you to do this**

### **Option B: Save Session (Experimental)**
LM Studio *might* restore your last session if you:
1. Load all 6 models
2. Let them stay loaded for 5+ minutes
3. Close LM Studio normally (not force-quit)
4. Next time it starts, it *might* restore them

**Not reliable though**

### **Option C: API-based Loading (Future)**
Write a script that uses LM Studio's API to load models, but this is complex and may not work reliably.

---

## 📋 **RECOMMENDED STARTUP PROCEDURE**

**Every time you reboot VM100:**

1. **Wait for Windows to fully load** (2-3 minutes)

2. **Open PowerShell as Administrator**

3. **Run master script:**
   ```powershell
   cd C:\GOKU-AI
   .\START-SHENRON.ps1
   ```

4. **Script will:**
   - Start LM Studio automatically
   - Wait for LM Studio API to be ready
   - **PAUSE and ask you to load models**

5. **You manually load the 6 models in LM Studio**

6. **Press Enter in PowerShell to continue**

7. **Script will:**
   - Verify models are loaded
   - Start SHENRON API
   - Verify everything works

8. **Total time:** 5-10 minutes (mostly waiting for model loading)

---

## ❌ **THINGS TO STOP DOING**

### **DON'T run Quest Manager directly**
```powershell
# DON'T DO THIS (causes CPU/RAM maxing):
cd C:\GOKU-AI\shenron
python quest_manager.py run 1
```

**Instead:**
1. Make sure SHENRON is fully operational first
2. Test with simple query
3. THEN run Quest Manager with careful monitoring

### **DON'T rely on auto-start (yet)**
The Task Scheduler / VBScript / multiple scripts are competing and unreliable.

**Use the master script manually for now until we perfect it**

---

## 🧪 **TESTING PROCEDURE**

**After running master script:**

### **Test 1: SHENRON Health**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/health"
# Should return: {"status": "operational"}
```

### **Test 2: Simple Query**
```powershell
$body = @{query="What is the capital of France?"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/api/shenron/grant-wish" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 120
```

**This should:**
- Take 30-60 seconds
- Return a response from all 6 warriors
- Show consensus level

**If this works, SHENRON is fully operational!**

### **Test 3: Web UI**
Visit: https://shenron.lightspeedup.com

Try a simple query through the web interface

### **Test 4: Quest Manager (Optional)**
**ONLY if Tests 1-3 pass:**
```powershell
cd C:\GOKU-AI\shenron
python quest_manager.py status 1
# Should show quest stats
```

**DON'T run `quest_manager.py run 1` yet!**

---

## 📊 **WHAT WENT WRONG**

### **Web UI (My fault)**
- I made changes to add API status indicator and password protection
- The CSS broke the header layout
- **Fixed:** Rolled back to v4.0

### **Auto-start (Architecture issue)**
- Too many components:
  - Task Scheduler trying to start LM Studio
  - VBScript wrapper trying to start LM Studio
  - PowerShell script trying to load models (but LM Studio not ready)
  - SHENRON service trying to start (but models not loaded)
  - Everything competing, nothing coordinated

**Fixed:** Master script does everything in order

### **Quest Manager (User error + my incomplete testing)**
- Ran without SHENRON being ready
- SHENRON tried to query 6 models that weren't loaded
- Caused timeouts, retries, CPU/RAM maxing

**Fix:** Always verify SHENRON first

---

## 🎯 **ACTION ITEMS FOR YOU**

### **RIGHT NOW:**

1. ✅ **Verify web UI is fixed** - Visit site, should look normal
2. ✅ **Stop Quest Manager if running**
   ```powershell
   Get-Process python | Stop-Process -Force
   ```
3. ✅ **Reboot VM100** (clean slate)
   ```powershell
   Restart-Computer
   ```

### **AFTER REBOOT:**

4. ✅ **Run master startup script**
   ```powershell
   cd C:\GOKU-AI
   .\START-SHENRON.ps1
   ```

5. ✅ **Load 6 models manually when prompted**

6. ✅ **Test SHENRON with simple query**

7. ✅ **Verify everything works**

### **LATER (When everything is stable):**

8. ⏳ **Create desktop shortcut** (for easy starting)

9. ⏳ **Consider scheduled task** (for auto-start)

10. ⏳ **Test Quest Manager** (with monitoring)

---

## 🔒 **ABOUT AGENT MODE & PASSWORD**

**I haven't re-implemented the password protection yet** because the web UI broke.

**For now:**
- Agent Mode is accessible to anyone visiting the site
- This is a security risk if the site is public
- **Recommendation:** Keep it OFF unless you're using it

**I'll re-implement properly once we have stable startup**

---

## 📝 **FILES CREATED/MODIFIED**

### **New Files:**
1. `C:\GOKU-AI\START-SHENRON.ps1` - Master startup script
2. `C:\GOKU-AI\startup-YYYYMMDD-HHMMSS.log` - Logs (created each run)

### **Restored Files:**
1. `/var/www/shenron.lightspeedup.com/index.html` - Back to v4.0
2. `/var/www/shenron.lightspeedup.com/script.js` - Back to v4.0
3. `/var/www/shenron.lightspeedup.com/style.css` - Back to v4.0

### **Unchanged (Still working):**
1. `C:\GOKU-AI\shenron\quest_manager.py` - Quest Manager code
2. `C:\GOKU-AI\shenron\shenron_v4_orchestrator.py` - SHENRON API
3. `C:\GOKU-AI\knowledge-base\*.md` - All knowledge files

---

## 🎓 **LESSONS LEARNED**

1. **Don't deploy untested web UI changes** - I should have tested locally first
2. **Coordinated startup is critical** - Master script approach is better
3. **LM Studio model loading is manual** - No way around it (yet)
4. **Quest Manager needs SHENRON ready** - Must verify before running
5. **Auto-start is complex** - Need proper orchestration

---

## 🚀 **NEXT STEPS (My TODO)**

1. ⏳ Create safer web UI updates (test locally first)
2. ⏳ Add proper API status indicator (without breaking layout)
3. ⏳ Implement password protection (without breaking site)
4. ⏳ Research LM Studio session restore
5. ⏳ Add Quest Manager safety checks (verify SHENRON first)
6. ⏳ Create monitoring dashboard

---

## 📞 **IF SOMETHING BREAKS**

### **Web UI broken:**
```bash
ssh wp1@<VM150_IP>
cd /var/www/shenron.lightspeedup.com
echo "<VM_PASSWORD>"  # See credentials.json | sudo -S cp index.html.backup.v4.0 index.html
echo "<VM_PASSWORD>"  # See credentials.json | sudo -S cp script.js.backup.v4.0 script.js
echo "<VM_PASSWORD>"  # See credentials.json | sudo -S cp style.css.backup.v4.0 style.css
```

### **VM100 unresponsive:**
- Reboot via Proxmox web UI
- Or SSH to Proxmox host: `qm reboot 100`

### **SHENRON not responding:**
```powershell
# Restart everything
cd C:\GOKU-AI
.\START-SHENRON.ps1
```

---

**Status:** Web UI fixed, Master script deployed  
**Next:** You need to run the master script manually  
**Goal:** Get to stable, reliable startup procedure  

**I apologize for the web UI breakage - that was my mistake!** 🙏

