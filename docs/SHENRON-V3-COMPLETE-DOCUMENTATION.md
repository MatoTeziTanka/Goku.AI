<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🐉 THE SHENRON SYNDICATE v3.0-v3.3 - Complete Documentation

**Last Updated:** November 6, 2025  
**Version:** 3.3 (v4.0 backend operational)  
**Status:** ✅ PRODUCTION - Fully Operational with RAG + Orchestration + TRUE Synthesis

---

## 📋 TABLE OF CONTENTS

1. [Version History](#version-history)
2. [Architecture Overview](#architecture-overview)
3. [Major Changes from v2.1](#major-changes-from-v21)
4. [Backend Components](#backend-components)
5. [Frontend Components](#frontend-components)
6. [AI Council Warriors](#ai-council-warriors)
7. [Deployment Guide](#deployment-guide)
8. [API Endpoints](#api-endpoints)
9. [Configuration](#configuration)
10. [Testing](#testing)
11. [Known Issues](#known-issues)
12. [Roadmap (v4.0)](#roadmap-v40)

---

## 📅 VERSION HISTORY

### **v3.3** (November 6, 2025) - Current
- ✅ Fixed warrior status animations (turn green individually during consultation)
- ✅ Live clock with user location detection (top info bar)
- ✅ Version info and last update date display
- ✅ Enhanced DBZ easter eggs (10+ new animations and effects)
- ✅ Improved visual polish and user experience
- 🔧 Backend: v4.0 operational (TRUE synthesis + Agent mode ready)

### **v3.2.1** (November 6, 2025)
- ✅ Fixed warrior status animations (turn green individually as they complete)
- ✅ Updated GOKU's role to "Adaptive Warrior & Growth Catalyst"
- ✅ Added dramatic wish prompt: "Why have you summoned me? Tell me Your Wish Now."
- ✅ Failure easter egg: "Your wish cannot be granted because the Guardian of Earth created me..."
- ✅ Changed "DBZ-Fighters" to "DBZ-Warriors" throughout
- ✅ Title text stroke for better visibility
- ✅ SHENRON's voice appears FIRST in responses
- ⚠️ Known issue: SHENRON's synthesis is placeholder (shows GOKU's response)

### **v3.2** (November 6, 2025)
- ✅ Redesigned response layout with SHENRON's unified voice at top
- ✅ Individual warrior responses moved to expandable section
- ✅ Enhanced visual design with status bars at top of cards
- ✅ "Your wish has been granted!" animated success message
- ✅ Improved consensus badges

### **v3.1** (November 6, 2025)
- ✅ Fixed status bar design (moved to top of cards)
- ✅ Proper color scheme: Gray (Ready) → Orange (Consulting) → Green (Complete)
- ✅ No more overlapping text or visibility issues

### **v3.0** (November 5-6, 2025) - Major Upgrade
- ✅ **RAG System**: ChromaDB + sentence-transformers for knowledge base
- ✅ **SHENRON Orchestrator**: Python-based agent that coordinates all warriors
- ✅ **Parallel Queries**: All 6 warriors consulted simultaneously
- ✅ **Consensus Detection**: Unanimous/Strong/Majority/Weak analysis
- ✅ **Flask API Server**: Port 5000 on VM100
- ✅ **Knowledge Base**: Persistent memory about Seth and infrastructure
- ✅ **Updated PHP Proxy**: Routes to SHENRON API instead of individual models

---

## 🏗️ ARCHITECTURE OVERVIEW

### **High-Level Flow**

```
User Browser (http://<VM150_IP>)
    ↓
Web GUI (HTML/JS/CSS on VM150)
    ↓
api.php (PHP Proxy on VM150)
    ↓
SHENRON API Server (Flask on VM100:5000)
    ↓
    ├→ RAG Search (ChromaDB)
    └→ LM Studio API (VM100:1234)
        ↓
        6 AI Models (Parallel Queries)
```

### **Component Distribution**

| Component | Location | Port | Purpose |
|-----------|----------|------|---------|
| **Web GUI** | VM150 | 80 | User interface |
| **PHP Proxy** | VM150 | 80 | CORS bypass, request forwarding |
| **SHENRON API** | VM100 | 5000 | Orchestration, RAG, synthesis |
| **LM Studio** | VM100 | 1234 | AI model hosting |
| **ChromaDB** | VM100 | - | Vector database for RAG |

---

## 🆕 MAJOR CHANGES FROM V2.1

### **Backend Transformation**

| Feature | v2.1 | v3.0+ |
|---------|------|-------|
| **Query Method** | Sequential (one-by-one) | Parallel (all 6 simultaneously) |
| **Knowledge** | None (stateless) | RAG with persistent memory |
| **Response Time** | 6x slower | ~5-6 seconds total |
| **Orchestration** | None (direct queries) | SHENRON agent coordinates |
| **Consensus** | None | Detected and displayed |
| **Memory** | None | Knows about Seth, infrastructure, services |

### **Frontend Improvements**

| Feature | v2.1 | v3.2 |
|---------|------|------|
| **Layout** | Individual responses only | SHENRON's voice + expandable warriors |
| **Status Updates** | Basic dot indicators | Animated status bars (Ready/Consulting/Complete) |
| **Design** | Simple cards | Status bars at top, clean hierarchy |
| **Easter Eggs** | None | "Wish granted" + "Cannot grant" messages |
| **Visibility** | Plain text | Text stroke on title, enhanced shadows |

---

## 🔧 BACKEND COMPONENTS

### **1. RAG System** (`C:\GOKU-AI\knowledge-base\`)

**Purpose**: Provide persistent memory and context to AI models

**Components**:
- **Knowledge Base Files**: Markdown files with Seth's info, infrastructure details, services
- **ChromaDB**: Vector database for semantic search
- **Sentence-Transformers**: Embedding model (`all-MiniLM-L6-v2`)

**Location**: 
- Knowledge Base: `C:\GOKU-AI\knowledge-base\seth-infrastructure.md`
- Vector DB: `C:\GOKU-AI\chroma_db\`
- Ingestion Script: `C:\GOKU-AI\shenron\2-Ingest-Knowledge-Base.py`

**Capabilities**:
- Semantic search over knowledge base
- Returns top 3 relevant chunks for any query
- Injected into prompts before querying warriors

### **2. SHENRON Orchestrator** (`C:\GOKU-AI\shenron\`)

**Purpose**: Central coordination agent that manages the entire AI council

**Main Files**:
```
C:\GOKU-AI\shenron\
├── shenron_orchestrator.py      # Core orchestrator module
├── 3-shenron-orchestrator.py    # Standalone test script
├── 4-shenron-api-server.py      # Flask API server
└── 2-Ingest-Knowledge-Base.py   # RAG ingestion
```

**Key Functions**:

**`ShenronOrchestrator` Class**:
- `search_knowledge_base(query, n_results=3)` - RAG search
- `query_fighter(fighter, user_query, context)` - Query single warrior
- `consult_council(user_query, use_rag=True)` - Query all 6 in parallel
- `analyze_consensus(responses)` - Detect agreement levels
- `synthesize_response(council_result)` - Combine responses
- `grant_wish(user_query, use_rag=True)` - Main entry point

**Warrior Configuration**:
```python
FIGHTERS = [
    Fighter("GOKU", "🥋", "Adaptive Warrior & Growth Catalyst", 
            "deepseek-coder-v2-lite-instruct", 0.7),
    Fighter("VEGETA", "👑", "Technical Authority", 
            "llama-3.2-3b-instruct", 0.3),
    Fighter("PICCOLO", "🧠", "Strategic Sage", 
            "qwen2.5-coder-7b-instruct", 0.5),
    Fighter("GOHAN", "⚠️", "Risk Sentinel", 
            "mistral-7b-instruct-v0.3", 0.4),
    Fighter("KRILLIN", "🔧", "Practical Engineer", 
            "phi-3-mini-128k-instruct", 0.6),
    Fighter("FRIEZA", "😈", "Chaos Tyrant", 
            "phi-3-mini-128k-instruct:2", 0.9),
]
```

**Consensus Detection**:
- **UNANIMOUS** (100%): All 6 warriors respond successfully
- **STRONG** (75-99%): 5 warriors respond
- **MAJORITY** (50-74%): 3-4 warriors respond
- **WEAK** (<50%): 1-2 warriors respond

### **3. Flask API Server** (Port 5000)

**Purpose**: Expose SHENRON's capabilities via HTTP

**Endpoints**:

#### `GET /health`
Health check endpoint.

**Response**:
```json
{
    "status": "operational",
    "service": "SHENRON v3.0",
    "dragon_awakened": true
}
```

#### `POST /api/shenron/grant-wish`
Main endpoint for granting wishes.

**Request**:
```json
{
    "query": "What is my name and mission?",
    "use_rag": true
}
```

**Response**:
```json
{
    "query": "What is my name and mission?",
    "rag_used": true,
    "consensus": {
        "type": "unanimous",
        "message": "All 6 fighters agree.",
        "consensus_level": 1.0,
        "successful_fighters": ["GOKU", "VEGETA", "PICCOLO", "GOHAN", "KRILLIN", "FRIEZA"],
        "failed_fighters": []
    },
    "synthesized_answer": "...",
    "individual_responses": [
        {
            "fighter": "GOKU",
            "emoji": "🥋",
            "role": "Adaptive Warrior & Growth Catalyst",
            "answer": "Your name is Seth.",
            "success": true,
            "response_time": 4.08,
            "temperature": 0.7,
            "model": "deepseek-coder-v2-lite-instruct"
        },
        // ... 5 more warriors
    ],
    "total_time": 5.02,
    "wish_granted": true
}
```

#### `POST /api/shenron/search-knowledge`
Direct knowledge base search.

#### `GET /api/shenron/fighters`
List all warriors and their configurations.

---

## 💻 FRONTEND COMPONENTS

### **Files** (`/var/www/shenron.lightspeedup.com/`)

```
/var/www/shenron.lightspeedup.com/
├── index.html      # Main HTML structure (v3.2)
├── script.js       # Frontend logic (v3.2.1)
├── style.css       # DBZ-themed styling with v3.2 enhancements
└── api.php         # PHP proxy to SHENRON API (v3.0)
```

### **Key Features**

#### **HTML Structure (v3.2)**
- Warrior cards with status bars at top
- Dramatic wish prompt
- SHENRON's unified response section
- Expandable individual warrior insights
- Success/failure easter eggs

#### **JavaScript (v3.2.1)**
- `summonShenron()` - Main query function
- `animateWarriorCompletions()` - NEW: Turn warriors green individually
- `showResults()` - Display SHENRON's response
- `createUnifiedResponse()` - Format synthesized answer
- `toggleFighterResponses()` - Show/hide warrior details

**Status Animation Logic**:
```javascript
// Warriors complete at different times based on response_time
sorted.forEach(warrior => {
    const delay = warrior.response_time * 1000;
    setTimeout(() => {
        updateWarriorStatus(key, 'done', '✓ Complete');
    }, delay);
});
```

#### **CSS Styling (v3.2)**
- **Title**: Black text stroke for visibility
- **Status Bars**: Positioned at top of cards
  - Gray (Ready) → Orange (Consulting, animated pulse) → Green (Complete)
- **SHENRON's Voice**: Centered with green glow
- **Success Message**: Animated shimmer + glow
- **Failure Message**: Red pulse with yellow border
- **Dragon Divider**: Gradient line separator

### **PHP Proxy (v3.0)**

**Location**: `/var/www/shenron.lightspeedup.com/api.php`

**Purpose**: Forward requests from web GUI to SHENRON API

**Key Changes from v2.1**:
- Endpoint changed from LM Studio (`:1234`) to SHENRON (`:5000`)
- Now calls `/api/shenron/grant-wish` instead of direct model queries
- Passes `query` and `use_rag` parameters
- Increased timeout to 30 minutes (1800s)

**Configuration**:
```php
$SHENRON_API = "http://<VM100_IP>:5000/api/shenron/grant-wish";
set_time_limit(1800);
curl_setopt($ch, CURLOPT_TIMEOUT, 1800);
```

---

## 🥋 AI COUNCIL WARRIORS

### **1. 🥋 GOKU - Adaptive Warrior & Growth Catalyst**
- **Model**: deepseek-coder-v2-lite-instruct
- **Temperature**: 0.7 (Creative but focused)
- **Role**: Learns through challenges, pushes limits, never gives up
- **Personality**: Like the Marine Corps - resilient, adaptive, growth-minded
- **Context**: 163B tokens
- **Max Tokens**: 8192

### **2. 👑 VEGETA - Technical Authority**
- **Model**: llama-3.2-3b-instruct
- **Temperature**: 0.3 (Ultra-precise, technical)
- **Role**: Commands technical excellence, no compromises
- **Personality**: Pride in precision, demands perfection
- **Context**: 32K tokens
- **Max Tokens**: 4096

### **3. 🧠 PICCOLO - Strategic Sage**
- **Model**: qwen2.5-coder-7b-instruct
- **Temperature**: 0.5 (Balanced wisdom)
- **Role**: Long-term planning, strategic thinking
- **Personality**: Wise mentor, sees the bigger picture
- **Context**: 32K tokens
- **Max Tokens**: 4096

### **4. ⚠️ GOHAN - Risk Sentinel**
- **Model**: mistral-7b-instruct-v0.3
- **Temperature**: 0.4 (Cautious, thorough)
- **Role**: Identifies risks, warns of dangers
- **Personality**: Protective scholar, thorough analyst
- **Context**: 32K tokens
- **Max Tokens**: 4096

### **5. 🔧 KRILLIN - Practical Engineer**
- **Model**: phi-3-mini-128k-instruct
- **Temperature**: 0.5 (Pragmatic)
- **Role**: Hands-on solutions, practical implementations
- **Personality**: Gets it done, workaround master
- **Context**: 128K tokens
- **Max Tokens**: 2048

### **6. 😈 FRIEZA - Chaos Tyrant**
- **Model**: phi-3-mini-128k-instruct:2
- **Temperature**: 0.9 (Maximum chaos/creativity)
- **Role**: Devil's advocate, challenges assumptions
- **Personality**: Ruthless contrarian, finds weaknesses
- **Context**: 128K tokens
- **Max Tokens**: 2048

**Temperature Philosophy**:
- **Low (0.3-0.4)**: Precise, technical, risk-aware
- **Medium (0.5-0.6)**: Balanced, practical
- **High (0.7-0.9)**: Creative, adaptive, chaotic

---

## 🚀 DEPLOYMENT GUIDE

### **Prerequisites**

**VM100 (Windows Server 2025):**
- Python 3.11+
- Virtual environment: `C:\GOKU-AI\venv`
- LM Studio 0.3.31 with 6 models loaded
- Firewall: Port 5000 open

**VM150 (Ubuntu 24.04 LTS):**
- Apache 2.4.58
- PHP 8.x
- Document root: `/var/www/shenron.lightspeedup.com/`

### **Backend Deployment (VM100)**

#### **Step 1: Install Python Dependencies**

```powershell
cd C:\GOKU-AI\shenron
.\venv\Scripts\Activate.ps1

pip install chromadb sentence-transformers flask flask-cors requests numpy tiktoken
```

**Installed Packages**:
- `chromadb` - Vector database
- `sentence-transformers` - Embedding model
- `flask` - Web framework
- `flask-cors` - CORS support
- `requests` - HTTP client
- `numpy` - Numerical computing
- `tiktoken` - Token counting

#### **Step 2: Create Knowledge Base**

Create `C:\GOKU-AI\knowledge-base\seth-infrastructure.md` with:
- Your name, background, location
- Infrastructure details (VMs, services, hardware)
- Company info (LightSpeedUp Hosting)
- Services offered
- Network configuration

#### **Step 3: Ingest Knowledge Base**

```powershell
cd C:\GOKU-AI\shenron
python 2-Ingest-Knowledge-Base.py
```

**Expected Output**:
```
✅ Knowledge Base Ingestion Complete!
📊 Files processed: 1
   Total chunks: 50-100 (depends on content size)
   Database location: C:\GOKU-AI\chroma_db
```

#### **Step 4: Test Orchestrator**

```powershell
python 3-shenron-orchestrator.py
```

**Expected**: Full response from all 6 warriors with RAG context.

#### **Step 5: Start API Server**

```powershell
python 4-shenron-api-server.py
```

**Expected Output**:
```
🐉 SHENRON API SERVER v3.0 - Starting...
✅ SHENRON is ready to grant wishes!

 * Running on http://127.0.0.1:5000
 * Running on http://<VM100_IP>:5000
```

**Keep this running!**

#### **Step 6: Open Firewall**

```powershell
New-NetFirewallRule -DisplayName "SHENRON API Server" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

### **Frontend Deployment (VM150)**

#### **Files to Deploy**:

Upload to `/var/www/shenron.lightspeedup.com/`:
- `index.html` (v3.2)
- `script.js` (v3.2.1)
- `style.css` (v3.2)
- `api.php` (v3.0)

#### **Deploy Script**:

```bash
# Backup current files
sudo cp /var/www/shenron.lightspeedup.com/index.html /var/www/shenron.lightspeedup.com/index.html.backup
sudo cp /var/www/shenron.lightspeedup.com/script.js /var/www/shenron.lightspeedup.com/script.js.backup
sudo cp /var/www/shenron.lightspeedup.com/style.css /var/www/shenron.lightspeedup.com/style.css.backup

# Deploy new files
sudo cp /tmp/index.html.v3.2 /var/www/shenron.lightspeedup.com/index.html
sudo cp /tmp/script.js.v3.2.1 /var/www/shenron.lightspeedup.com/script.js
sudo cp /tmp/style.css.v3.2 /var/www/shenron.lightspeedup.com/style.css

# Set permissions
sudo chown www-data:www-data /var/www/shenron.lightspeedup.com/{index.html,script.js,style.css}
```

#### **Verify Deployment**:

```bash
ls -lh /var/www/shenron.lightspeedup.com/
curl http://localhost/api.php -X POST -H "Content-Type: application/json" -d '{"query":"test","use_rag":true}'
```

---

## 🧪 TESTING

### **Backend Tests**

#### **Test 1: RAG Search**
```bash
curl http://<VM100_IP>:5000/api/shenron/search-knowledge \
  -H "Content-Type: application/json" \
  -d '{"query": "What is my name?", "n_results": 3}'
```

**Expected**: Relevant knowledge base chunks mentioning "Seth"

#### **Test 2: Grant Wish**
```bash
curl http://<VM100_IP>:5000/api/shenron/grant-wish \
  -H "Content-Type: application/json" \
  -d '{"query": "What is my name?", "use_rag": true}'
```

**Expected**: Full JSON response with all 6 warriors

#### **Test 3: List Warriors**
```bash
curl http://<VM100_IP>:5000/api/shenron/fighters
```

**Expected**: Array of 6 warrior configurations

### **Frontend Tests**

#### **Test 1: Load Web GUI**
- Navigate to `http://<VM150_IP>`
- Verify 6 warrior cards display with "Ready" status
- Check title has visible text stroke

#### **Test 2: Simple Query**
- Enter: "What is my name?"
- Click "SUMMON SHENRON"
- Expected:
  - All warriors turn orange "Consulting..."
  - Warriors turn green "✓ Complete" individually (fastest first)
  - SHENRON's response appears at top
  - "✨ So be it. Your wish has been granted! ✨" shows
  - Individual warrior responses hidden until expanded

#### **Test 3: Consensus Types**
- **UNANIMOUS**: Ask any normal question
- **WEAK**: Stop 4-5 models in LM Studio, then query
- Verify consensus badge shows correct type and color

### **Performance Benchmarks**

| Metric | v2.1 | v3.0-v3.2 | Improvement |
|--------|------|-----------|-------------|
| **Total Response Time** | ~180s (sequential) | ~5-6s | **30x faster** |
| **Fastest Warrior** | N/A | ~2.8s (VEGETA) | - |
| **Slowest Warrior** | N/A | ~4.7s (GOHAN) | - |
| **RAG Lookup** | N/A | <1s | - |
| **Knowledge Retention** | None | Persistent | ∞ |

---

## ⚠️ KNOWN ISSUES

### **1. SHENRON's Synthesis is Placeholder** (v3.2.1)

**Issue**: SHENRON's "unified response" currently just displays GOKU's response, not a true synthesis.

**Code**:
```javascript
const firstResponse = successfulResponses[0]; // Just GOKU!
```

**Workaround**: Expand "View Individual DBZ-Warrior Insights" to see all responses.

**Fix**: Planned for v4.0 - Add 7th AI call to truly synthesize responses.

### **2. SSH Authentication on Windows DC**

**Issue**: Windows Server 2025 Domain Controller blocks SSH password auth by design.

**Status**: Deferred to v4.0 (will use PowerShell remoting instead for agent mode).

### **3. Status Updates Appear All at Once** (FIXED in v3.2.1)

**Issue**: Warriors turned green all at once after all completed.

**Fix**: v3.2.1 now animates completions based on `response_time` data.

---

## 🚀 ROADMAP (V4.0)

### **Planned Features**

#### **1. True AI Synthesis**
- Add 7th API call to synthesize all responses
- Use GOKU or dedicated synthesis model
- Prompt: "Read these 6 responses and create ONE unified answer"
- Result: SHENRON's actual voice, not just GOKU's

#### **2. SSH Command Execution (Agent Mode)**
- Add `paramiko` SSH execution
- Action detection: "advice" vs "execute"
- Safety guardrails:
  - **Safe** (auto-execute): `df -h`, `uptime`, `systemctl status`
  - **Moderate** (require approval): `systemctl restart`, `apt update`
  - **Dangerous** (blocked): `rm -rf`, `dd`, `shutdown`
- Multi-step workflows
- Feedback loops (learn from command results)

#### **3. Enhanced RAG**
- Multi-document support
- Real-time knowledge base updates
- Query history and learning
- Semantic deduplication

#### **4. Streaming Responses**
- Server-sent events (SSE) for real-time updates
- True live status as warriors complete
- No fake animations needed

#### **5. Multi-User Support**
- Session management
- User-specific context
- Request queuing

---

## 📝 MAINTENANCE

### **Update Knowledge Base**

1. Edit `C:\GOKU-AI\knowledge-base\seth-infrastructure.md`
2. Re-run ingestion:
```powershell
cd C:\GOKU-AI\shenron
python 2-Ingest-Knowledge-Base.py
```
3. Restart API server

### **Update Warrior Roles**

Edit `C:\GOKU-AI\shenron\shenron_orchestrator.py`:
```python
Fighter("GOKU", "🥋", "NEW ROLE HERE", "model", 0.7)
```

Restart API server.

### **Backup Strategy**

**Critical Files**:
- `C:\GOKU-AI\knowledge-base\` - Knowledge base source
- `C:\GOKU-AI\chroma_db\` - Vector database
- `C:\GOKU-AI\shenron\*.py` - Orchestrator code
- `/var/www/shenron.lightspeedup.com/` - Web GUI

**Backup Command**:
```bash
tar -czf shenron-backup-$(date +%Y%m%d).tar.gz \
  /var/www/shenron.lightspeedup.com/
```

---

## 🎓 LESSONS LEARNED

### **What Worked Well**
1. ✅ Parallel queries dramatically improved speed (30x faster)
2. ✅ RAG integration provided persistent memory without retraining
3. ✅ Flask API provided clean separation of concerns
4. ✅ Status animations enhanced user experience
5. ✅ Consensus detection added transparency

### **Challenges Encountered**
1. ⚠️ Windows Server 2025 DC SSH issues (security policies)
2. ⚠️ Unicode encoding issues with emojis in PowerShell
3. ⚠️ Missing Visual C++ redistributable for PyTorch
4. ⚠️ Firewall configuration for port 5000
5. ⚠️ True response synthesis more complex than expected

### **Best Practices**
1. ✅ Always use virtual environments for Python
2. ✅ Test backend independently before frontend integration
3. ✅ Version control everything (backups before deployment)
4. ✅ Document configuration changes immediately
5. ✅ Use meaningful variable names and comments

---

## 📞 SUPPORT

### **Troubleshooting**

**Warriors not responding?**
- Check LM Studio is running on VM100
- Verify all 6 models are loaded
- Test direct API: `curl http://<VM100_IP>:1234/v1/models`

**RAG not working?**
- Verify ChromaDB exists: `ls C:\GOKU-AI\chroma_db`
- Re-run ingestion script
- Check knowledge base file exists

**API server won't start?**
- Check port 5000 not in use: `netstat -ano | findstr 5000`
- Verify firewall rule exists
- Check Python virtual environment is activated

**Status animations not working?**
- Hard refresh browser (Ctrl+F5)
- Check `script.js` version is v3.2.1
- Verify no JavaScript errors in browser console

---

## 📚 REFERENCES

### **Documentation**
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Sentence-Transformers](https://www.sbert.net/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [LM Studio](https://lmstudio.ai/)

### **Related Files**
- `/docs/SHENRON-SYNDICATE-COMPLETE-DOCUMENTATION.md` - v2.1 docs
- `/docs/server-infrastructure-documentation.md` - Infrastructure overview
- `/shenron-v3-deployment/` - Deployment scripts

---

**Maintained by**: Seth (Marine Corps Veteran, LightSpeedUp Hosting)  
**Location**: Warwick, Rhode Island  
**Infrastructure**: Dell PowerEdge R730, 480GB RAM, Proxmox Virtualization

---

*"So be it. Your wish has been granted!"* ✨

