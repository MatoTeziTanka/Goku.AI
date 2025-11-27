<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🐉 SHENRON v3.0 - Complete Deployment Guide

**Version:** 3.0  
**Date:** November 6, 2025  
**Status:** Ready for Deployment

---

## 📋 OVERVIEW

SHENRON v3.0 introduces:
- ✅ **RAG (Retrieval Augmented Generation)** - Knowledge base integration
- ✅ **Orchestrator Pattern** - SHENRON coordinates all 6 fighters
- ✅ **Consensus Detection** - Analyzes agreement/conflicts
- ✅ **Unified Response** - One synthesized answer
- ✅ **API Server** - Flask endpoint for web integration
- ✅ **Easter Egg** - "Your wish has been granted! ✨"

---

## 🎯 ARCHITECTURE

```
User → Web UI (VM150)
         ↓
     api.php (proxy)
         ↓
     SHENRON API Server (VM100:5000)
         ↓
     SHENRON Orchestrator
         ├── RAG Search (ChromaDB)
         └── Query 6 Fighters (LM Studio:1234)
             ├── GOKU (DeepSeek)
             ├── VEGETA (Llama)
             ├── PICCOLO (Qwen)
             ├── GOHAN (Mistral)
             ├── KRILLIN (Phi-3)
             └── FRIEZA (Phi-3)
         ↓
     Synthesize Consensus
         ↓
     User receives unified answer
```

---

## 📦 DEPLOYMENT STEPS

### **PHASE 1: Install Dependencies (VM100)**

#### **Step 1: Copy Deployment Files**

Via RDP to VM100, copy all files from `/tmp/shenron-deployment/` to `C:\GOKU-AI\shenron\`:

```powershell
# On VM100 (Windows)
New-Item -Path "C:\GOKU-AI\shenron" -ItemType Directory -Force
# Copy all files from your Linux machine to this directory
```

Or download from GitHub after pushing.

#### **Step 2: Install Python Packages**

Open PowerShell as Administrator on VM100:

```powershell
cd C:\GOKU-AI\shenron
.\1-Install-Python-Packages.ps1
```

**Expected time:** 5-10 minutes  
**Downloads:** ~500MB of packages

**What this installs:**
- ChromaDB (vector database)
- sentence-transformers (embedding model)
- requests, flask, numpy, tiktoken, paramiko

---

### **PHASE 2: Ingest Knowledge Base (VM100)**

Activate the virtual environment and run ingestion:

```powershell
cd C:\GOKU-AI\shenron
C:\GOKU-AI\venv\Scripts\Activate.ps1
python 2-Ingest-Knowledge-Base.py
```

**Expected time:** 2-5 minutes  
**What this does:**
- Reads all `.md` files from `C:\GOKU-AI\knowledge-base\`
- Splits into chunks (500 words, 100 overlap)
- Creates vector embeddings
- Stores in ChromaDB at `C:\GOKU-AI\chroma_db\`

**Expected output:**
```
✅ KNOWLEDGE BASE INGESTION COMPLETE!
   - Files processed: 8
   - Total chunks: 150+
   - Database location: C:\GOKU-AI\chroma_db
```

---

### **PHASE 3: Test SHENRON Orchestrator (VM100)**

Test SHENRON locally before exposing via API:

```powershell
cd C:\GOKU-AI\shenron
C:\GOKU-AI\venv\Scripts\Activate.ps1
python 3-shenron-orchestrator.py
```

**Expected output:**
```
🐉 SHENRON: Consulting the council...
   📚 Searching knowledge base...
   ✅ Found relevant context (523 chars)
   ⚡ Querying 6 fighters in parallel...
      ✅ 🥋 GOKU responded (12.3s)
      ✅ 👑 VEGETA responded (8.1s)
      ✅ 🧠 PICCOLO responded (15.7s)
      ✅ ⚠️ GOHAN responded (10.4s)
      ✅ 🔧 KRILLIN responded (5.2s)
      ✅ 😈 FRIEZA responded (6.8s)

🐉 SHENRON'S RESPONSE:
   📊 Consensus: UNANIMOUS
      All 6 fighters agree.
   ⏱️ Total Time: 18.4 seconds
   📚 RAG Used: Yes

✨ So be it. Your wish has been granted! ✨
```

---

### **PHASE 4: Start SHENRON API Server (VM100)**

Start the Flask API server that will receive requests from VM150:

```powershell
cd C:\GOKU-AI\shenron
C:\GOKU-AI\venv\Scripts\Activate.ps1

# Install flask-cors (if not already installed)
pip install flask-cors

# Start the API server
python 4-shenron-api-server.py
```

**Expected output:**
```
🐉 SHENRON API SERVER v3.0 - Starting...
📡 API ENDPOINTS:
   GET  /health                       - Health check
   POST /api/shenron/grant-wish       - Grant a wish (main)
   POST /api/shenron/search-knowledge - Search knowledge base
   GET  /api/shenron/fighters         - List all fighters

🌐 Server will be available at:
   http://localhost:5000
   http://<VM100_IP>:5000

🐉 SHENRON is ready to grant wishes!
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://<VM100_IP>:5000
```

**Keep this running!** Leave the PowerShell window open.

---

### **PHASE 5: Update api.php (VM150)**

SSH to VM150 and update the PHP proxy to use SHENRON API:

```bash
ssh wp1@<VM150_IP>
```

Create new `api.php`:

```php
<?php
// SHENRON v3.0 - API Proxy
// Routes requests to SHENRON API Server on VM100

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Configuration
$SHENRON_API = "http://<VM100_IP>:5000/api/shenron/grant-wish";

// Set timeouts
set_time_limit(1800); // 30 minutes
ini_set('max_execution_time', '1800');

// Get request body
$requestBody = file_get_contents('php://input');
$requestData = json_decode($requestBody, true);

if (!isset($requestData['query'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing query field']);
    exit;
}

// Forward to SHENRON API
$ch = curl_init($SHENRON_API);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $requestBody);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_TIMEOUT, 1800); // 30 minutes
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 30);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if (curl_errno($ch)) {
    http_response_code(500);
    echo json_encode(['error' => 'SHENRON API error: ' . curl_error($ch)]);
    curl_close($ch);
    exit;
}

curl_close($ch);

// Return SHENRON's response
http_response_code($httpCode);
echo $response;
?>
```

Deploy it:

```bash
sudo cp /path/to/new/api.php /var/www/shenron.lightspeedup.com/api.php
sudo chown www-data:www-data /var/www/shenron.lightspeedup.com/api.php
```

---

### **PHASE 6: Update Web UI (VM150)**

Update `script.js` to handle SHENRON's unified response format.

The new response format:

```json
{
  "query": "What is my name?",
  "rag_used": true,
  "consensus": {
    "type": "unanimous",
    "message": "All 6 fighters agree.",
    "consensus_level": 1.0
  },
  "synthesized_answer": "...",
  "individual_responses": [...],
  "total_time": 18.4,
  "wish_granted": true
}
```

Update JavaScript to:
1. Show "🐉 SHENRON is consulting the council..."
2. Display unified response in main card
3. Show "✨ Your wish has been granted! ✨" when successful
4. Make individual responses expandable

---

### **PHASE 7: Test Complete Flow**

1. Open browser: `http://<VM150_IP>`
2. Ask: "What is my name and mission?"
3. Expected:
   - Progress bar shows "Consulting council..."
   - Unified SHENRON response appears
   - "Your wish has been granted! ✨"
   - Individual responses expandable

---

## 🔧 AUTO-START CONFIGURATION

### **Make SHENRON Start on VM100 Boot**

Create startup script:

```powershell
# C:\GOKU-AI\shenron\Start-Shenron.bat
@echo off
timeout /t 30 /nobreak
cd C:\GOKU-AI\shenron
call C:\GOKU-AI\venv\Scripts\activate.bat
python 4-shenron-api-server.py
```

Add to Startup folder:

```powershell
$startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
Copy-Item "C:\GOKU-AI\shenron\Start-Shenron.bat" -Destination $startupPath
```

---

## 📊 TESTING CHECKLIST

- [ ] Python packages installed
- [ ] Knowledge base ingested (150+ chunks)
- [ ] SHENRON orchestrator test successful
- [ ] API server running on port 5000
- [ ] api.php updated on VM150
- [ ] Web UI updated
- [ ] Test query returns unified response
- [ ] "Wish granted" message appears
- [ ] Individual responses expandable
- [ ] Auto-start configured

---

## 🐛 TROUBLESHOOTING

### **"Module not found" errors**
```powershell
# Ensure venv is activated
C:\GOKU-AI\venv\Scripts\Activate.ps1
pip list  # Verify packages installed
```

### **ChromaDB errors**
```powershell
# Delete and re-ingest
Remove-Item -Recurse -Force C:\GOKU-AI\chroma_db
python 2-Ingest-Knowledge-Base.py
```

### **API server won't start**
```powershell
# Check if port 5000 is in use
netstat -ano | findstr :5000
# Kill process if needed
taskkill /PID <PID> /F
```

### **Fighters timeout**
- Check LM Studio is running
- Verify all 6 models are loaded
- Check `http://<VM100_IP>:1234/v1/models`

---

## 📝 MAINTENANCE

### **Weekly**
- [ ] Check SHENRON API is running
- [ ] Test knowledge base queries
- [ ] Verify all 6 fighters respond

### **After Adding Knowledge**
```powershell
cd C:\GOKU-AI\shenron
C:\GOKU-AI\venv\Scripts\Activate.ps1
python 2-Ingest-Knowledge-Base.py
```

---

## 🎓 LESSONS LEARNED

1. **RAG is Essential** - Models need context
2. **Orchestration > Direct Queries** - Better UX
3. **Consensus Matters** - Users trust unified answers
4. **Easter Eggs Work** - "Wish granted" adds personality
5. **Flask is Simple** - Easy Python API server

---

## 🚀 FUTURE ENHANCEMENTS (v4.0)

- [ ] True AI synthesis (use another AI to combine responses)
- [ ] Iterative refinement (SHENRON asks follow-ups)
- [ ] SSH command execution
- [ ] Streaming responses (SSE)
- [ ] Web search integration
- [ ] Memory across sessions

---

**🐉 THE ETERNAL DRAGON AWAITS YOUR COMMAND! ⚡**

