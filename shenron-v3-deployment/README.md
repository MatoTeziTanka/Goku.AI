# 🐉 SHENRON v3.0 - Deployment Package

**Version:** 3.0  
**Release Date:** November 6, 2025  
**Status:** Production Ready

---

## 📋 WHAT'S IN THIS PACKAGE

This directory contains the complete SHENRON v3.0 deployment:

| File | Purpose | Platform |
|------|---------|----------|
| `1-Install-Python-Packages.ps1` | Install dependencies | VM100 (Windows) |
| `2-Ingest-Knowledge-Base.py` | Create vector embeddings | VM100 (Windows) |
| `3-shenron-orchestrator.py` | Test SHENRON locally | VM100 (Windows) |
| `4-shenron-api-server.py` | Start Flask API server | VM100 (Windows) |
| `shenron_orchestrator.py` | Importable Python module | VM100 (Windows) |
| `api-v3.php` | Web proxy to SHENRON API | VM150 (Linux) |
| `DEPLOY-SHENRON-V3.md` | **Complete deployment guide** | Documentation |
| `SHENRON-V3-READY.md` | Quick start summary | Documentation |
| `README.md` | This file | Documentation |

---

## 🚀 QUICK START

### **Prerequisites**

**VM100 (Windows Server 2025):**
- Python 3.11+ installed
- LM Studio running with 6 models loaded
- Knowledge base files in `C:\GOKU-AI\knowledge-base\`

**VM150 (Ubuntu):**
- Apache2 with PHP 8.3
- Site configured at `/var/www/shenron.lightspeedup.com`

---

### **Deployment Steps**

1. **Copy files to VM100:**
   ```powershell
   New-Item -Path "C:\GOKU-AI\shenron" -ItemType Directory -Force
   # Copy all files to this directory
   ```

2. **Install dependencies (10 min):**
   ```powershell
   cd C:\GOKU-AI\shenron
   .\1-Install-Python-Packages.ps1
   ```

3. **Ingest knowledge base (5 min):**
   ```powershell
   C:\GOKU-AI\venv\Scripts\Activate.ps1
   python 2-Ingest-Knowledge-Base.py
   ```

4. **Test orchestrator (2 min):**
   ```powershell
   python 3-shenron-orchestrator.py
   ```

5. **Start API server (keep running):**
   ```powershell
   pip install flask-cors
   python 4-shenron-api-server.py
   ```

6. **Update VM150:**
   ```bash
   sudo cp api-v3.php /var/www/shenron.lightspeedup.com/api.php
   sudo chown www-data:www-data /var/www/shenron.lightspeedup.com/api.php
   ```

7. **Test:** `http://192.168.12.150` → Ask "What is my name?"

---

## 🎯 WHAT SHENRON v3.0 DOES

### **The Problem (v2.1)**

```
User: "What is my name and mission?"

🥋 GOKU: "I don't know, you haven't told me."
👑 VEGETA: "I don't know, you haven't told me."
🧠 PICCOLO: "I don't know, you haven't told me."
⚠️ GOHAN: "I don't know, you haven't told me."
🔧 KRILLIN: "I don't know, you haven't told me."
😈 FRIEZA: "I don't know, you haven't told me."

Result: 6 unhelpful responses
```

### **The Solution (v3.0)**

```
User: "What is my name and mission?"

🐉 SHENRON: "Consulting the council..."
   📚 Searching knowledge base...
   ✅ Found relevant context (523 chars)
   ⚡ Querying 6 fighters in parallel...
      ✅ All 6 responded (18.4s total)

🐉 SHENRON'S UNIFIED RESPONSE:

Your name is Seth, a Marine Corps veteran from Warwick, RI. 
You own LightSpeedUp Hosting and operate a Dell R730 server 
with 480GB RAM, dual E5-2697v4 CPUs, and ZFS storage. Your 
mission is to provide affordable, high-performance hosting 
while showcasing your infrastructure and DevOps expertise.

📊 COUNCIL CONSENSUS: UNANIMOUS (6/6 fighters agree)

✨ So be it. Your wish has been granted! ✨

[▼ Show Individual Fighter Responses]
```

---

## 🏗️ ARCHITECTURE

```
User Browser
    ↓
Web UI (VM150)
    ↓
api.php (routes to SHENRON API)
    ↓
SHENRON API Server (VM100:5000)
    ↓
SHENRON Orchestrator
    ├─ RAG: Search knowledge base (ChromaDB)
    └─ Query 6 fighters in parallel (LM Studio)
        ├─ GOKU (DeepSeek)
        ├─ VEGETA (Llama)
        ├─ PICCOLO (Qwen)
        ├─ GOHAN (Mistral)
        ├─ KRILLIN (Phi-3)
        └─ FRIEZA (Phi-3)
    ↓
Analyze consensus + Synthesize response
    ↓
Return unified answer to user
```

---

## ✨ KEY FEATURES

1. **RAG (Retrieval Augmented Generation)**
   - Semantic search of knowledge base
   - Context injection into prompts
   - No more "I don't know" responses

2. **Orchestration Pattern**
   - SHENRON coordinates all fighters
   - Parallel query execution
   - Unified response synthesis

3. **Consensus Detection**
   - Analyzes agreement/disagreement
   - Shows consensus level (unanimous/strong/majority/weak)
   - Highlights conflicts

4. **Better UX**
   - One unified answer (not 6 separate ones)
   - "Your wish has been granted!" easter egg
   - Expandable individual responses

5. **Production Ready**
   - 30-minute timeout support
   - Flask API server with CORS
   - Auto-start scripts included

---

## 📊 PERFORMANCE

**Expected Response Times:**
- Knowledge base search: < 1 second
- Fighter queries (parallel): 15-90 seconds (depends on model/query)
- Total: ~20-120 seconds for complex queries

**Resource Usage (VM100):**
- RAM: +2GB for ChromaDB + embeddings
- CPU: Minimal (only during ingestion/search)
- Disk: +500MB for vector database

---

## 🔧 MAINTENANCE

### **Weekly Tasks**
- Check SHENRON API is running
- Test knowledge base queries
- Verify all 6 fighters respond

### **Adding New Knowledge**
```powershell
cd C:\GOKU-AI\shenron
C:\GOKU-AI\venv\Scripts\Activate.ps1
python 2-Ingest-Knowledge-Base.py
```
This re-ingests all knowledge base files (overwrites old embeddings).

### **Restarting SHENRON**
```powershell
# Kill existing server
taskkill /F /IM python.exe

# Restart
cd C:\GOKU-AI\shenron
C:\GOKU-AI\venv\Scripts\Activate.ps1
python 4-shenron-api-server.py
```

---

## 🐛 TROUBLESHOOTING

See `DEPLOY-SHENRON-V3.md` for comprehensive troubleshooting.

**Common Issues:**

| Problem | Solution |
|---------|----------|
| "Module not found" | Activate venv: `C:\GOKU-AI\venv\Scripts\Activate.ps1` |
| ChromaDB errors | Delete `C:\GOKU-AI\chroma_db` and re-ingest |
| API won't start | Check port 5000: `netstat -ano \| findstr :5000` |
| Fighters timeout | Verify LM Studio is running with all 6 models loaded |
| "No context found" | Re-run ingestion script |

---

## 🚧 FUTURE ENHANCEMENTS (v4.0)

These are deferred but can be added later:

- [ ] SSH command execution (paramiko is installed)
- [ ] True AI synthesis (use another AI to combine responses)
- [ ] Iterative refinement (multi-round discussions)
- [ ] Server-Sent Events (streaming responses)
- [ ] Web search integration
- [ ] Session memory across queries

---

## 📝 CHANGELOG

### **v3.0 (November 6, 2025)**
- ✅ RAG system with ChromaDB
- ✅ SHENRON orchestrator pattern
- ✅ Consensus detection
- ✅ Unified response synthesis
- ✅ Flask API server
- ✅ "Your wish has been granted!" easter egg

### **v2.1 (November 6, 2025)**
- Long-form query support (30-minute timeout)
- Local network access (http://192.168.12.150)
- 50MB POST limit

### **v2.0 (November 5, 2025)**
- Initial multi-model council (6 fighters)
- Parallel query processing
- Real-time progress bar

---

## 📞 SUPPORT

**Documentation:**
- Complete guide: `DEPLOY-SHENRON-V3.md`
- Quick start: `SHENRON-V3-READY.md`

**GitHub:**
- Repository: `Dell-Server-Roadmap`
- Directory: `shenron-v3-deployment/`

**Related Documentation:**
- Main docs: `/docs/SHENRON-SYNDICATE-COMPLETE-DOCUMENTATION.md`
- VM100 setup: `/docs/server-infrastructure-documentation.md`

---

## 🎓 TECHNICAL DETAILS

**Python Dependencies:**
- `chromadb` - Vector database
- `sentence-transformers` - Embedding model
- `flask` - API server
- `requests` - HTTP client
- `numpy` - Numerical computing
- `tiktoken` - Token counting
- `paramiko` - SSH client (for future use)
- `flask-cors` - CORS support

**Embedding Model:**
- `all-MiniLM-L6-v2` (384 dimensions)
- Fast, efficient, good quality
- ~90MB download

**Database:**
- ChromaDB (persistent storage)
- Location: `C:\GOKU-AI\chroma_db`
- ~500MB disk space

---

## ⚡ ONE-LINER SUMMARY

**SHENRON v3.0 = RAG + Orchestration + Consensus + Easter Egg**

---

**🐉 THE ETERNAL DRAGON AWAITS YOUR COMMAND! ⚡**

*Built by Seth (Marine Corps veteran) for the LightSpeedUp infrastructure*  
*Running on Dell R730 server in Warwick, RI*

