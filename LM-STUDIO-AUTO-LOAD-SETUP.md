# 🤖 LM STUDIO AUTO-LOAD MODELS AT STARTUP

**Problem:** LM Studio starts automatically on boot, but models are NOT loaded automatically, requiring manual intervention after every reboot.

**Solution:** Automated PowerShell script that runs at startup, waits for LM Studio to initialize, and attempts to trigger model loading.

---

## 📋 QUICK SETUP (Run on VM100)

### **Step 1: Copy Scripts to Desktop**
The scripts should already be on your Desktop:
- `Auto-Load-LMStudio-Models.ps1`
- `Setup-LMStudio-AutoLoad.ps1`

### **Step 2: Run Setup (ONE TIME)**
```powershell
# Open PowerShell as Administrator
cd C:\Users\Administrator\Desktop
.\Setup-LMStudio-AutoLoad.ps1
```

This will:
- ✅ Copy the auto-load script to `C:\GOKU-AI\scripts\`
- ✅ Create a Windows Scheduled Task
- ✅ Configure it to run 2 minutes after startup

### **Step 3: Test It Now**
```powershell
# Trigger the task manually to test
Start-ScheduledTask -TaskName "LMStudio-AutoLoad-Models"

# Check task status
Get-ScheduledTaskInfo -TaskName "LMStudio-AutoLoad-Models"
```

---

## 🔍 HOW IT WORKS

### **Startup Sequence:**
1. **Windows boots** → LM Studio auto-starts (already configured in Registry)
2. **2 minutes later** → Auto-load script runs
3. **Script waits** for LM Studio process to be detected
4. **Script checks** if LM Studio API is responding
5. **Script verifies** how many models are loaded
6. **If 0 models** → Script brings LM Studio window to foreground (triggers session restore)
7. **Script rechecks** after 20 seconds to confirm models loaded

### **Expected Behavior:**
- ✅ **If LM Studio has "Restore Session" enabled:** Models load automatically
- ⚠️  **If not:** Script will activate the window, which may trigger loading
- ❌ **If that fails:** Manual intervention required (one-time model loading)

---

## 🧪 TESTING

### **Test 1: Reboot VM100**
```powershell
Restart-Computer
```

Wait 5 minutes, then check:
```powershell
# Check if models are loaded
Invoke-RestMethod http://localhost:1234/v1/models

# Should show 6 models
```

### **Test 2: Manual Trigger**
```powershell
# Run the auto-load script manually
C:\GOKU-AI\scripts\Auto-Load-LMStudio-Models.ps1
```

---

## 📊 TROUBLESHOOTING

### **Problem: 0 models after reboot**
```powershell
# Check if task ran
Get-ScheduledTaskInfo -TaskName "LMStudio-AutoLoad-Models"

# Check task history
Get-WinEvent -LogName "Microsoft-Windows-TaskScheduler/Operational" | 
    Where-Object {$_.Message -like "*LMStudio-AutoLoad*"} | 
    Select-Object -First 5
```

### **Problem: LM Studio doesn't have session restore**

**Option A: Manual workaround (recommended)**
1. Load all 6 models in LM Studio
2. Keep LM Studio window open (minimized is OK)
3. Models will stay loaded until LM Studio is closed

**Option B: Check LM Studio settings**
1. Open LM Studio
2. Go to Settings → General or Advanced
3. Look for options like:
   - "Restore previous session"
   - "Auto-load last models"
   - "Remember loaded models"

**Option C: Use LM Studio CLI (if available)**
```powershell
# Check for CLI
ls "C:\Users\Administrator\AppData\Local\Programs\LM Studio" -Filter *.exe
```

---

## 🎯 LM STUDIO SESSION RESTORE CHECK

### **Check if LM Studio saves loaded models:**

```powershell
# Check UI state files
Get-Content "C:\Users\Administrator\.lmstudio\.internal\ui-state\global.json" | ConvertFrom-Json

# Check backend preferences
Get-Content "C:\Users\Administrator\.lmstudio\.internal\backend-preferences-v1.json" | ConvertFrom-Json

# Look for any "loadedModels", "activeModels", or "sessionState" keys
```

If you find config options for session restore, you can enable them manually or via script.

---

## 📝 ALTERNATIVE SOLUTION: NSSM SERVICE FOR MODELS

If LM Studio doesn't support session restore, you could:

1. **Create a wrapper script** that:
   - Starts LM Studio
   - Waits for API to be ready
   - Calls a model-loading API (if it exists)

2. **Use Windows Task Scheduler** (current solution)

3. **Keep LM Studio running 24/7** (simplest!)
   - Models stay loaded as long as LM Studio doesn't close
   - Just minimize it, don't close it

---

## 🔧 SCRIPT LOCATIONS

| File | Location |
|------|----------|
| Auto-load script | `C:\GOKU-AI\scripts\Auto-Load-LMStudio-Models.ps1` |
| Setup script | Desktop (can be deleted after setup) |
| Task name | `LMStudio-AutoLoad-Models` |
| Trigger | At startup + 2 minute delay |

---

## ⚡ QUICK COMMANDS

```powershell
# View task details
Get-ScheduledTask -TaskName "LMStudio-AutoLoad-Models"

# Trigger manually
Start-ScheduledTask -TaskName "LMStudio-AutoLoad-Models"

# Disable auto-load
Disable-ScheduledTask -TaskName "LMStudio-AutoLoad-Models"

# Enable auto-load
Enable-ScheduledTask -TaskName "LMStudio-AutoLoad-Models"

# Remove completely
Unregister-ScheduledTask -TaskName "LMStudio-AutoLoad-Models" -Confirm:$false
```

---

## 📚 RELATED DOCUMENTATION

- [SHENRON v4.0 Deployment Complete](./SHENRON-v4-DEPLOYMENT-COMPLETE.md)
- [SHENRON Full Access Setup](./SHENRON-FULL-ACCESS-SETUP.md)

---

## 🎯 RECOMMENDED WORKFLOW

**For now, until we verify LM Studio session restore works:**

1. ✅ Load all 6 models in LM Studio **once**
2. ✅ Keep LM Studio running (minimized)
3. ✅ Models stay loaded
4. ✅ Only restart LM Studio if absolutely necessary
5. ✅ If you reboot, run the auto-load script or load models manually

**Future enhancement:**
- If LM Studio adds model auto-load API, update script to use it
- If LM Studio session restore is confirmed working, document the setting

---

**Status:** ⚠️ WORKAROUND SOLUTION (testing required)  
**Next Steps:** Test after reboot and verify model loading behavior

🐉 **Shenron's models should now load automatically (or with minimal intervention)!**

