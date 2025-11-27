<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🐛 SHENRON Built-In Debugger Design

**Date:** November 7, 2025  
**Purpose:** Add real-time debugging capabilities to SHENRON  
**Goal:** Monitor, troubleshoot, and optimize AI performance

---

## 🎯 **WHAT IS A DEBUGGER FOR AI?**

**Traditional Software Debugger:**
- Sets breakpoints in code
- Steps through execution line-by-line
- Inspects variable values
- Traces function calls

**AI System Debugger:**
- Monitors model queries in real-time
- Tracks response times per warrior
- Logs token usage and context
- Records consensus decisions
- Captures errors and warnings
- Analyzes performance bottlenecks
- **Enables live troubleshooting**

---

## 🔍 **SHENRON DEBUGGER FEATURES**

### **1. Real-Time Query Monitor**

**Shows:**
- Current query being processed
- Which warriors are responding
- Live progress (0-100%)
- Time elapsed per warrior
- Estimated time remaining

**Example Display:**
```
═══════════════════════════════════════════════════════════
🐉 SHENRON LIVE DEBUG - Query in Progress
═══════════════════════════════════════════════════════════
Query: "What is 2+2?"
Started: 2025-11-07 20:30:15
Elapsed: 12.5s

Warrior Status:
[✅] GOKU    (deepseek-coder-v2-lite)  12.3s  COMPLETE
[✅] VEGETA  (llama-3.2-3b)             3.2s  COMPLETE
[⏳] PICCOLO (qwen2.5-coder-7b)         5.1s  IN PROGRESS...
[⏳] GOHAN   (mistral-7b)               4.8s  IN PROGRESS...
[⏳] KRILLIN (phi-3-mini-128k)          2.9s  IN PROGRESS...
[⏳] FRIEZA  (phi-3-mini-128k:2)        1.5s  IN PROGRESS...

Progress: ████████░░░░░░░░░░░░ 33% (2/6 complete)
ETA: 18 seconds remaining
═══════════════════════════════════════════════════════════
```

---

### **2. Performance Profiler**

**Tracks:**
- Time per warrior (min/max/avg)
- Slowest warrior per query
- Token usage per model
- Context window utilization
- RAM usage during query
- CPU utilization per model

**Example Report:**
```
═══════════════════════════════════════════════════════════
📊 PERFORMANCE PROFILE - Last 10 Queries
═══════════════════════════════════════════════════════════

Warrior Performance (Average Response Time):
  1. PICCOLO: 4.2s  ⚡ FASTEST
  2. KRILLIN: 5.1s  
  3. VEGETA:  9.5s  
  4. FRIEZA:  9.8s  
  5. GOHAN:   11.2s 
  6. GOKU:    37.1s  🐌 SLOWEST

Bottleneck: GOKU (deepseek-coder-v2-lite)
- Average: 37.1s (4x slower than PICCOLO)
- Max: 45.3s
- Min: 29.8s
- Recommendation: Investigate model loading or context size

Token Usage (Last Query):
  GOKU:    1,234 tokens (163K context, 0.75% used)
  VEGETA:  512 tokens   (32K context, 1.6% used)
  PICCOLO: 678 tokens   (32K context, 2.1% used)
  GOHAN:   834 tokens   (32K context, 2.6% used)
  KRILLIN: 456 tokens   (128K context, 0.36% used)
  FRIEZA:  923 tokens   (32K context, 2.9% used)

RAM Usage During Query: 148 GB / 192 GB (77%)
CPU Usage Peak: 89%
═══════════════════════════════════════════════════════════
```

---

### **3. Consensus Debugger**

**Shows:**
- How consensus was calculated
- Which warriors agreed/disagreed
- Confidence scores per warrior
- Why consensus level was chosen

**Example:**
```
═══════════════════════════════════════════════════════════
🤝 CONSENSUS ANALYSIS
═══════════════════════════════════════════════════════════
Query: "Should I upgrade server RAM?"

Warrior Positions:
  ✅ GOKU:    "Yes, upgrade" (Confidence: 0.8)
  ✅ PICCOLO: "Yes, upgrade" (Confidence: 0.7)
  ❌ VEGETA:  "Check motherboard first" (Confidence: 0.6)
  ❌ GOHAN:   "Risk: May not need it" (Confidence: 0.9)
  ⚠️  KRILLIN: "Test with current first" (Confidence: 0.5)
  ❌ FRIEZA:  "What if you waste $2000?" (Confidence: 0.7)

Agreement Matrix:
  GOKU + PICCOLO:        AGREE (upgrade)
  VEGETA + GOHAN + FRIEZA: DISAGREE (wait/test)
  KRILLIN:               NEUTRAL

Consensus: WEAK (3 for, 3 against)
Type: Split decision
Recommendation: SHENRON must synthesize middle ground

SHENRON's Decision:
"Test workload at current RAM first. If hitting limits, 
upgrade. Otherwise, defer to avoid unnecessary expense."

Rationale: Balanced approach considering both sides
═══════════════════════════════════════════════════════════
```

---

### **4. Error Tracker**

**Logs:**
- Model timeout errors
- API connection failures
- JSON parsing errors
- Memory errors
- Context overflow warnings

**Example:**
```
═══════════════════════════════════════════════════════════
⚠️  ERROR LOG - Last 24 Hours
═══════════════════════════════════════════════════════════

[2025-11-07 18:23:45] ERROR - FRIEZA
  Type: InsufficientMemory
  Message: "Model requires 58.71 GB, only 47 GB available"
  Context: 128K context requested, 32K used instead
  Resolution: Reduced context to 32K ✅
  Impact: None (model loaded successfully with 32K)

[2025-11-07 19:45:12] WARNING - GOKU
  Type: SlowResponse
  Message: "Model took 45.3s (expected <40s)"
  Context: Cold start after service restart
  Resolution: Subsequent queries faster (37s avg) ✅
  Impact: Minor (first query only)

[2025-11-07 20:10:33] ERROR - LM Studio API
  Type: ConnectionTimeout
  Message: "Connection to localhost:1234 timed out"
  Context: LM Studio not responding
  Resolution: Restarted LM Studio service ✅
  Impact: 2 minutes downtime

Total Errors: 3
Critical: 0
Warnings: 1
Resolved: 3/3 (100%)
═══════════════════════════════════════════════════════════
```

---

### **5. Live Query Inspector**

**Allows:**
- View RAG search results
- See exact prompt sent to each warrior
- Inspect raw model responses
- View SHENRON's synthesis logic
- Export full query data as JSON

**Example:**
```
═══════════════════════════════════════════════════════════
🔍 QUERY INSPECTOR - Query #42
═══════════════════════════════════════════════════════════

[1] User Query:
"What is 2+2?"

[2] RAG Search:
Searching knowledge base: "2+2 arithmetic addition mathematics"
Results: 0 relevant docs (simple math, no RAG needed)

[3] Prompt to GOKU:
───────────────────────────────────────────────────────────
You are GOKU, an Adaptive Warrior & Growth Catalyst.
User query: "What is 2+2?"
Context: (none)
Temperature: 0.7
Max tokens: 8192

Provide a helpful, accurate response.
───────────────────────────────────────────────────────────

[4] GOKU's Raw Response:
───────────────────────────────────────────────────────────
{
  "model": "deepseek-coder-v2-lite-instruct",
  "response": " The answer to \"what is 2 plus 2?\" is 4.",
  "tokens_used": 23,
  "response_time": 37.541555404663086
}
───────────────────────────────────────────────────────────

[5] All Warrior Responses:
  GOKU:    "4" (37.5s)
  VEGETA:  "4" (9.8s)
  PICCOLO: "4" (4.4s)
  GOHAN:   "4" (11.5s)
  KRILLIN: "4" (5.1s)
  FRIEZA:  "4" (9.8s)

[6] Consensus Analysis:
Type: UNANIMOUS
Confidence: 1.0 (100%)
All warriors agree: Answer is 4

[7] SHENRON's Synthesis:
───────────────────────────────────────────────────────────
The answer to the simple mathematical question "2 plus 2" 
is indeed 4. Each of the warriors, while expressing the 
result in their unique manner, all concur that the sum of 
2 and 2 equals 4...
───────────────────────────────────────────────────────────

[8] Final Response:
Status: SUCCESS
Total Time: 59.8s
Warriors: 6/6 responded
Consensus: UNANIMOUS
Wish Granted: ✅

[Export as JSON] [Download Log] [View in Browser]
═══════════════════════════════════════════════════════════
```

---

## 🚀 **IMPLEMENTATION OPTIONS**

### **Option A: Web-Based Debug UI (Recommended)**

**Access via:** `http://<VM100_IP>:5001/debug`

**Features:**
- Live query monitoring dashboard
- Real-time warrior status updates
- Performance graphs (Chart.js)
- Error log viewer
- Query history
- Export debug data

**Tech Stack:**
- Flask route: `/debug`
- WebSocket for live updates
- Chart.js for graphs
- Bootstrap for UI

**Example Route:**
```python
@app.route('/debug')
def debug_dashboard():
    """Debug dashboard for SHENRON"""
    return render_template('debug.html')

@app.route('/debug/live')
def debug_live():
    """WebSocket endpoint for live updates"""
    # Stream live query data
    pass
```

---

### **Option B: Terminal-Based Debug (Simple)**

**Enable via:** Environment variable or config flag

```powershell
# Enable debug mode
$env:SHENRON_DEBUG = "true"
Restart-Service SHENRON
```

**Output:**
```
[DEBUG] [20:30:15] Starting query: "What is 2+2?"
[DEBUG] [20:30:15] RAG search: 0 results
[DEBUG] [20:30:15] Querying GOKU (deepseek-coder-v2-lite)...
[DEBUG] [20:30:15] Querying VEGETA (llama-3.2-3b)...
[DEBUG] [20:30:15] Querying PICCOLO (qwen2.5-coder-7b)...
[DEBUG] [20:30:15] Querying GOHAN (mistral-7b)...
[DEBUG] [20:30:15] Querying KRILLIN (phi-3-mini-128k)...
[DEBUG] [20:30:15] Querying FRIEZA (phi-3-mini-128k:2)...
[DEBUG] [20:30:19] PICCOLO responded (4.4s): "4"
[DEBUG] [20:30:20] KRILLIN responded (5.1s): "4"
[DEBUG] [20:30:25] VEGETA responded (9.8s): "4"
[DEBUG] [20:30:25] FRIEZA responded (9.8s): "4"
[DEBUG] [20:30:27] GOHAN responded (11.5s): "4"
[DEBUG] [20:30:52] GOKU responded (37.5s): "4"
[DEBUG] [20:30:52] Consensus: UNANIMOUS (6/6 agree)
[DEBUG] [20:30:52] Generating synthesis...
[DEBUG] [20:31:15] Synthesis complete (23s)
[DEBUG] [20:31:15] Total time: 59.8s
[DEBUG] [20:31:15] Query complete ✅
```

---

### **Option C: Log File Debug (Permanent Record)**

**Log to:** `C:\GOKU-AI\logs\shenron-debug.log`

**Rotation:** Daily logs, keep 30 days

**Format:**
```
2025-11-07 20:30:15.123 [INFO] Query started: "What is 2+2?"
2025-11-07 20:30:15.234 [DEBUG] RAG search returned 0 results
2025-11-07 20:30:15.345 [DEBUG] GOKU query started
2025-11-07 20:30:15.456 [DEBUG] VEGETA query started
...
2025-11-07 20:31:15.789 [INFO] Query complete (59.8s)
2025-11-07 20:31:15.890 [PERF] GOKU: 37.5s (SLOW)
2025-11-07 20:31:15.901 [PERF] PICCOLO: 4.4s (FAST)
```

**Python Implementation:**
```python
import logging
from logging.handlers import TimedRotatingFileHandler

# Setup logger
logger = logging.getLogger('shenron')
logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)

# File handler (rotates daily)
handler = TimedRotatingFileHandler(
    'C:/GOKU-AI/logs/shenron-debug.log',
    when='midnight',
    interval=1,
    backupCount=30
)
handler.setFormatter(logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s'
))
logger.addHandler(handler)

# Usage
logger.debug(f"Querying {fighter.name}...")
logger.info(f"Query complete ({elapsed}s)")
logger.warning(f"{fighter.name} slow response: {time}s")
logger.error(f"{fighter.name} failed: {error}")
```

---

## 🎯 **RECOMMENDED IMPLEMENTATION: HYBRID**

### **Phase 1: Add Logging (Week 1)**

**Immediate benefit:**
- Permanent record of all queries
- Performance tracking
- Error logging
- No UI needed yet

**Implementation:**
```python
# Add to shenron_v4_orchestrator.py
import logging
logger = logging.getLogger('shenron')

def consult_council(self, query):
    logger.info(f"Query: {query}")
    start_time = time.time()
    
    # Query warriors
    for fighter in FIGHTERS:
        logger.debug(f"Querying {fighter.name}...")
        response = self.query_fighter(fighter, query)
        logger.debug(f"{fighter.name} responded ({response.time}s)")
    
    elapsed = time.time() - start_time
    logger.info(f"Query complete ({elapsed}s)")
```

---

### **Phase 2: Add Web UI (Week 2-3)**

**Features:**
- Live query monitor
- Performance dashboard
- Error log viewer
- Query history

**Access:** `http://<VM100_IP>:5001/debug`

---

### **Phase 3: Add WebSocket (Week 4)**

**Real-time updates:**
- Live warrior status
- Progress bar
- ETA display
- No page refresh needed

---

## 📊 **DEBUG MODES**

### **1. MINIMAL (Production)**

**Logs:** Errors only  
**Performance:** No impact  
**Use case:** Normal operation

```python
SHENRON_DEBUG_LEVEL = "ERROR"
```

---

### **2. STANDARD (Default)**

**Logs:** Info + Errors + Warnings  
**Performance:** Minimal impact (<1%)  
**Use case:** Normal operation with basic monitoring

```python
SHENRON_DEBUG_LEVEL = "INFO"
```

---

### **3. VERBOSE (Troubleshooting)**

**Logs:** Everything (DEBUG)  
**Performance:** Minor impact (~5%)  
**Use case:** Troubleshooting issues

```python
SHENRON_DEBUG_LEVEL = "DEBUG"
```

---

### **4. FULL DEBUG (Development)**

**Logs:** Everything + RAW responses  
**Performance:** Moderate impact (~10%)  
**Use case:** Development, testing new features

```python
SHENRON_DEBUG_LEVEL = "TRACE"
SHENRON_LOG_RAW_RESPONSES = True
```

---

## 🔧 **ENABLE DEBUG MODE**

### **Method 1: Environment Variable**

```powershell
# Set debug level
$env:SHENRON_DEBUG = "DEBUG"

# Restart service
Restart-Service SHENRON
```

---

### **Method 2: Config File**

**File:** `C:\GOKU-AI\shenron\config.json`

```json
{
  "debug": {
    "enabled": true,
    "level": "DEBUG",
    "log_file": "C:/GOKU-AI/logs/shenron-debug.log",
    "log_raw_responses": true,
    "performance_profiling": true
  }
}
```

---

### **Method 3: API Endpoint**

```powershell
# Enable debug via API
Invoke-RestMethod -Uri "http://localhost:5000/debug/enable" -Method POST

# Disable debug
Invoke-RestMethod -Uri "http://localhost:5000/debug/disable" -Method POST

# Get debug status
Invoke-RestMethod -Uri "http://localhost:5000/debug/status"
```

---

## 📈 **PERFORMANCE IMPACT**

| Debug Level | Log File Size | Performance Impact | Disk I/O |
|-------------|---------------|-------------------|----------|
| ERROR | ~1 MB/day | 0% | Negligible |
| INFO | ~10 MB/day | <1% | Low |
| DEBUG | ~50 MB/day | ~5% | Moderate |
| TRACE | ~200 MB/day | ~10% | High |

**Recommendation:** Use INFO for normal operation, DEBUG only when troubleshooting.

---

## 🎯 **USE CASES**

### **Use Case 1: Find Bottleneck**

**Problem:** Queries take 60 seconds, need to identify slowest warrior

**Solution:**
1. Enable DEBUG mode
2. Run test queries
3. Check performance profile
4. Identify slowest warrior (GOKU: 37.5s)
5. Investigate why (context size? model loading?)

---

### **Use Case 2: Diagnose Error**

**Problem:** SHENRON returns empty response

**Solution:**
1. Enable DEBUG mode
2. Check error log
3. Find property name mismatch
4. Fix and verify

---

### **Use Case 3: Optimize Performance**

**Problem:** Want to improve response time

**Solution:**
1. Enable performance profiling
2. Identify patterns:
   - GOKU always slow (37s)
   - PICCOLO always fast (4s)
3. Deploy Ultra Instinct mode (GOKU only for simple queries)
4. Measure improvement (60s → 2s)

---

## 🚀 **QUICK START: ADD BASIC DEBUGGING**

### **Step 1: Add to orchestrator (5 minutes)**

```python
import logging
import time

# Setup logger
logging.basicConfig(
    filename='C:/GOKU-AI/logs/shenron.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger('shenron')

# Add to consult_council method
def consult_council(self, query):
    logger.info(f"Query: '{query}'")
    start_time = time.time()
    
    # ... existing code ...
    
    for fighter in FIGHTERS:
        fighter_start = time.time()
        response = self.query_fighter(fighter, query)
        fighter_time = time.time() - fighter_start
        logger.info(f"{fighter.name}: {fighter_time:.2f}s")
    
    total_time = time.time() - start_time
    logger.info(f"Total: {total_time:.2f}s, Consensus: {consensus}")
```

---

### **Step 2: Restart SHENRON**

```powershell
Restart-Service SHENRON
```

---

### **Step 3: View Logs**

```powershell
Get-Content C:\GOKU-AI\logs\shenron.log -Tail 50 -Wait
```

---

## 📝 **SUMMARY**

**Debugger Benefits:**
- ✅ Monitor real-time query progress
- ✅ Identify performance bottlenecks
- ✅ Track errors and warnings
- ✅ Optimize warrior performance
- ✅ Troubleshoot issues faster
- ✅ Understand consensus decisions

**Implementation:**
- **Phase 1:** Basic logging (5 min)
- **Phase 2:** Web UI (1-2 weeks)
- **Phase 3:** Live updates (1 week)

**Recommendation:**
Start with basic logging NOW (Phase 1), then add web UI later when needed.

---

**Status:** Design complete  
**Complexity:** LOW (basic), MEDIUM (web UI)  
**Time:** 5 minutes (logging), 1-2 weeks (full UI)  
**Next:** Add basic logging to orchestrator

