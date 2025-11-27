<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🐉⚡ ULTRA INSTINCT MODE - Monitoring Guide

**Version:** v1762539231  
**Updated:** November 7, 2025, 1:13 PM EST

---

## ⏱️ **TIMEOUT SETTINGS**

### **NEW Extended Timeouts:**
| Mode | Timeout | Use Case |
|------|---------|----------|
| ⚡ **LIGHTNING** | 2 minutes | Quick queries |
| 🔥 **COUNCIL** | 5 minutes | Standard analysis |
| 🐉 **ULTRA INSTINCT** | **30 minutes** | Deep puzzle solving |

**What happens if it times out?**
- You'll see: "⏱️ The summoning timed out after X minutes"
- The query is stopped
- You can try again with a shorter/simpler query

---

## 👀 **HOW TO MONITOR ULTRA INSTINCT MODE**

### **❌ NO Pop-ups or New Tabs**
- Everything happens **in the same page**
- You monitor progress in the **browser window**
- Console log shows detailed progress

### **✅ What You'll See:**

#### **1. While Processing:**
```
🐉 SHENRON is awakening...

[Progress bar moving]
0% → 10% → 20% ... → 100%
Estimated: Calculating...

[Warrior Status Updates:]
🥋 GOKU: Consulting... → ✓ Complete
👑 VEGETA: Consulting... → ✓ Complete
🧠 PICCOLO: Consulting... → ✓ Complete
⚠️ GOHAN: Consulting... → ✓ Complete
🔧 KRILLIN: Consulting... → ✓ Complete
😈 FRIEZA: Consulting... → ✓ Complete
```

#### **2. When Complete:**
```
🐉 SHENRON'S UNIFIED RESPONSE:

[The synthesized answer appears here]

📊 COUNCIL CONSENSUS: [Agreement level]

✨ So be it. Your wish has been granted! ✨

[View Individual Warrior Responses] ← Click to see all 6 responses
```

---

## 🖥️ **BROWSER CONSOLE MONITORING (Advanced)**

### **To Open Console:**
- **Chrome/Edge:** Press `F12` or `Ctrl+Shift+J`
- **Firefox:** Press `F12` or `Ctrl+Shift+K`

### **What You'll See in Console:**

```javascript
// When you click Summon:
🔍 callShenronAPI called with: {query: "...", agentMode: true, powerMode: "ultra"}
⏱️ API timeout set to 30 minutes for ULTRA mode
🔍 Request body: {"query":"...","power_mode":"ultra","agent_mode":true}

// While processing:
🔍 Response received: 200 OK
🔍 Response data: {...}

// When complete:
🐉 Wish granted in 142.3 seconds
✨ Displaying results...
```

### **If Something Goes Wrong:**
```javascript
// Timeout:
⏱️ The summoning timed out after 30 minutes

// Network error:
❌ Error: Failed to fetch

// API error:
❌ Error: HTTP error! status: 500
```

---

## 📊 **BACKEND MONITORING (Advanced)**

### **Monitor SHENRON API Logs (VM100):**

**Via SSH:**
```powershell
# Watch API output in real-time
ssh Administrator@<VM100_IP>
powershell
cd C:\GOKU-AI\shenron\logs
Get-Content shenron-startup.log -Tail 50 -Wait
```

**What You'll See:**
```
🔥 COUNCIL MODE: Analyze the GSMG.IO Bitcoin puzzle...
📚 Searching knowledge base...
✅ Found relevant context (523 chars)
⚡ Querying 6 fighters in parallel...

[Goku-deepseek-coder-v2] Generating response...
[Vegeta-llama-3.2-3b] Generating response...
[Piccolo-qwen2.5-coder-7b] Generating response...
[Gohan-mistral-7b] Generating response...
[Krillin-phi-3-mini] Generating response...
[Frieza-phi-3-mini] Generating response...

✅ All 6 responded (87.4s total)
🧠 Synthesizing final answer...
✅ Synthesis complete (14.2s)
```

---

## 🔍 **WHAT'S HAPPENING DURING ULTRA INSTINCT?**

### **Phase 1: RAG Search (0-10s)**
- SHENRON searches the knowledge base
- Looking for relevant context about your query
- Console: `📚 Searching knowledge base...`

### **Phase 2: Warrior Consultation (10s-2min)**
- All 6 warriors analyze the query in parallel
- Each warrior uses their unique perspective
- Console: `⚡ Querying 6 fighters in parallel...`
- **UI:** Warriors change from "Ready" → "Consulting..." → "✓ Complete"

### **Phase 3: Consensus Analysis (2-3min)**
- SHENRON analyzes all 6 responses
- Detects agreements and conflicts
- Determines consensus strength
- Console: `🧠 Analyzing consensus...`

### **Phase 4: TRUE Synthesis (3-5min)**
- **7th AI call** synthesizes the final answer
- Combines the best insights from all warriors
- Creates a coherent, unified response
- Console: `🧠 Synthesizing final answer...`

### **Phase 5 (ULTRA INSTINCT ONLY): Multi-Pass Debate (5-30min)**
- If consensus is weak, run **Pass 2**
- Warriors debate the disagreements
- New synthesis incorporating all viewpoints
- Console: `🐉 Detected split consensus - initiating second pass...`

---

## ⚡ **REAL-TIME STATUS INDICATORS**

### **Progress Bar:**
- Moves from 0% to 100%
- Updates as warriors complete
- Shows estimated time remaining

### **Warrior Status Colors:**
| Color | Status | Meaning |
|-------|--------|---------|
| **Gray** | "Ready" | Not started |
| **Yellow** | "Consulting..." | Currently working |
| **Green** | "✓ Complete" | Finished |

### **API Status Light (Top Right):**
| Color | Status | Meaning |
|-------|--------|---------|
| 🟢 **Green** | "Online" | API responding |
| 🔴 **Red** | "Not responding" | API offline |
| 🟡 **Yellow** | "Checking..." | Testing connection |

---

## 🐛 **TROUBLESHOOTING**

### **Problem: "Warriors stuck on 'Consulting...' forever"**
**Cause:** LM Studio models not loaded  
**Fix:**
```powershell
# Check LM Studio on VM100
curl http://<VM100_IP>:1234/v1/models
# Should show 6 models loaded
```

### **Problem: "Timeout after 30 minutes"**
**Cause:** Query too complex or models slow  
**Fix:**
- Break query into smaller parts
- Use COUNCIL mode instead of ULTRA
- Check VM100 CPU/RAM usage

### **Problem: "No response received"**
**Cause:** Backend error or field mismatch  
**Fix:**
- Check browser console for errors
- Verify API is running: `curl http://<VM100_IP>:5000/health`

### **Problem: "Page frozen/unresponsive"**
**Cause:** Browser tab backgrounded or system sleep  
**Fix:**
- Keep tab active and visible
- Disable screen sleep during long queries
- Use `caffeinate` on Mac or PowerToys Awake on Windows

---

## 📋 **MONITORING CHECKLIST**

### **Before Starting:**
- [ ] LM Studio running on VM100 (6 models loaded)
- [ ] SHENRON API running (check API status light = green)
- [ ] Browser console open (F12)
- [ ] Screen sleep disabled
- [ ] Query prepared and tested

### **During Execution:**
- [ ] Watch warrior status (turning green one by one)
- [ ] Monitor progress bar (0% → 100%)
- [ ] Check console for errors
- [ ] Estimated time updating

### **After Completion:**
- [ ] Read synthesized answer
- [ ] Check consensus level (unanimous? split?)
- [ ] View individual warrior responses
- [ ] Save/copy important results
- [ ] Check total time in console

---

## 💡 **PRO TIPS**

### **Tip #1: Use Console for Detailed Progress**
```javascript
// See exactly what's happening:
console.log = (function(old) {
    return function() {
        // Logs appear in console with timestamp
        old.apply(console, arguments);
    };
})(console.log);
```

### **Tip #2: Save Long Responses**
- Click "View Individual Warrior Responses"
- Right-click → Inspect → Copy HTML
- Or use Ctrl+A, Ctrl+C to copy all text

### **Tip #3: Monitor VM100 Performance**
```powershell
# Watch CPU/RAM usage while SHENRON runs
ssh Administrator@<VM100_IP>
powershell
while ($true) {
    $cpu = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue
    $ram = (Get-Counter '\Memory\Available MBytes').CounterSamples.CookedValue
    Write-Host "CPU: $([math]::Round($cpu,2))% | RAM Free: $ram MB"
    Start-Sleep -Seconds 5
}
```

### **Tip #4: Background Monitoring**
Keep the SHENRON tab **ACTIVE** and **VISIBLE**:
- Background tabs may throttle JavaScript
- Page updates might pause
- Animations may freeze

---

## 🎯 **EXPECTED TIMINGS**

### **GSMG.IO Puzzle Query (96 words):**

| Phase | COUNCIL Mode | ULTRA INSTINCT Mode |
|-------|--------------|---------------------|
| **RAG Search** | 5-10s | 5-10s |
| **6 Warriors** | 60-120s | 60-120s |
| **Consensus** | 10-20s | 20-40s |
| **Synthesis** | 15-30s | 30-60s |
| **Pass 2** | N/A | +60-180s (if needed) |
| **TOTAL** | 2-3 minutes | **3-7 minutes** |

### **Ultra Complex Query:**
- Simple consensus: 3-5 minutes
- Weak consensus (Pass 2): 7-15 minutes
- High conflict (Pass 3+): 15-30 minutes

---

## 🔔 **NOTIFICATIONS (Optional Setup)**

### **Desktop Notification When Complete:**
Add this to your browser console:
```javascript
// Notify when SHENRON completes
const originalShowResults = showResults;
window.showResults = function() {
    originalShowResults.apply(this, arguments);
    new Notification('🐉 SHENRON', {
        body: 'Your wish has been granted!',
        icon: 'data:image/svg+xml,<svg>...</svg>'
    });
};

// Request permission first
Notification.requestPermission();
```

---

## 📊 **SUMMARY**

**What You See:**
- ✅ Same browser window (no popups)
- ✅ Real-time warrior status updates
- ✅ Progress bar showing completion
- ✅ Estimated time remaining
- ✅ Final synthesized answer

**Timeouts:**
- ⚡ Lightning: 2 minutes
- 🔥 Council: 5 minutes
- 🐉 Ultra Instinct: **30 minutes**

**Monitoring:**
- 👁️ Visual: Watch warriors turn green
- 📊 Progress: Check progress bar
- 🖥️ Console: See detailed logs (F12)
- 🔧 Backend: SSH to VM100 for API logs

---

**🐉 Ready to monitor Ultra Instinct Mode!**

**Access:** `http://shenron.lightspeedup.com`  
**Power Level:** OVER 9000!  
**Timeout:** 30 minutes  
**Let the dragon solve your puzzle!** 💰⚡

