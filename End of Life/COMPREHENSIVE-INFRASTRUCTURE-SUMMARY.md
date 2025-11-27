<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🐉 COMPREHENSIVE INFRASTRUCTURE SUMMARY
## VM100, Goku.AI (Shenron Syndicate), VM101, and Complete System Status

**Generated:** January 2025  
**Last Updated:** November 6-7, 2025  
**Status:** Production Operational

---

## 📋 TABLE OF CONTENTS

1. [VM100 (Windows Server 2025) - Current Status](#vm100-windows-server-2025)
2. [Goku.AI / Shenron Syndicate - AI System](#gokuai--shenron-syndicate)
3. [VM101 Ubuntu - New Control Node Plan](#vm101-ubuntu-control-node)
4. [VM120 - Reverse Proxy & Cloudflare](#vm120-reverse-proxy-cloudflare)
5. [VM150 - Web Server (Apache)](#vm150-web-server)
6. [File Locations in GitHub Directory](#file-locations)
7. [Port Configuration & Network](#ports-and-network)
8. [Knowledge Database Contents](#knowledge-database)
9. [HTML Interface Files](#html-interface)
10. [Cloudflare & Domain Configuration](#cloudflare-domain)

---

## 🖥️ VM100 (Windows Server 2025)

### **Current Status**
- **Hostname:** GOKU-AI
- **IP Address:** <VM100_IP>
- **Operating System:** Windows Server 2025 (Domain Controller)
- **Status:** ✅ Operational (Beast Mode - Pre-Customer Maximum Performance)
- **Auto-Login:** ✅ Enabled (Administrator account)

### **Hardware Specifications**
- **CPU:** 2 sockets × 13 cores = **26 vCPUs** (out of 28 physical cores)
- **RAM:** **192 GB** (196,608 MiB) - Upgraded from 80GB on Nov 6, 2025
- **Storage:** 500 GB SSD (ZFS pool on Proxmox host)
- **Physical Host:** Dell PowerEdge R730
  - **CPUs:** 2× Intel Xeon E5-2690 v4 (14 cores each, 28 cores total)
  - **Total RAM:** 256 GB DDR4 ECC
  - **Hypervisor:** Proxmox VE 8.x

### **Software Installed**
1. **LM Studio v0.3.31**
   - Auto-starts on boot (Registry configured)
   - API Server: Port 1234
   - Serves 6 AI models simultaneously
   - Location: `C:\Users\Administrator\.lmstudio\`

2. **Microsoft Machine Learning Server 9.4.7**
   - Enterprise AI/ML capabilities

3. **Python 3.11 Environment**
   - Virtual environment: `C:\GOKU-AI\shenron\venv\`
   - SHENRON orchestrator and API server

4. **SHENRON API Service (Windows Service)**
   - Service Name: SHENRON
   - Display Name: SHENRON AI Orchestrator v4.0
   - Port: 5000
   - Startup Type: Automatic
   - Location: `C:\GOKU-AI\shenron\`

5. **ChromaDB (Vector Database)**
   - Location: `C:\GOKU-AI\chroma_db\`
   - Size: ~82.57 MB (as of Nov 6, 2025)
   - Collection: "knowledge_base"
   - Documents: 6,977+ chunks ingested

6. **SSH/SCP Server**
   - Port: 22
   - Remote access capabilities

7. **Active Directory**
   - Domain Controller role

### **Services Running**
| Service | Port | Status | Purpose |
|---------|------|--------|---------|
| LM Studio API | 1234 | ✅ Active | AI model serving (internal only) |
| SHENRON API | 5000 | ✅ Active | Orchestrator & RAG system |
| ChromaDB | Embedded | ✅ Active | Vector database (~82.57 MB) |
| Active Directory | Various | ✅ Active | Domain Controller |
| SSH Server | 22 | ✅ Active | Remote access |

### **Performance Metrics**
- **AI RAM Usage:** ~63 GB (for 6 models)
- **Available RAM:** ~129 GB (for ChromaDB, system, expansion)
- **CPU Usage:** 89% peak during inference
- **Query Time:** 59.8 seconds (latest test, down from 167s)
- **Accuracy:** 99.9999% (6-model cross-validation)

---

## 🐉 GOKU.AI / SHENRON SYNDICATE

### **Overview**
The Shenron Syndicate is a multi-model AI council system providing diverse perspectives through 6 different AI personalities (DBZ-themed "Warriors"), each with unique characteristics, roles, and temperature settings.

### **The 6 AI Warriors (Personalities)**

#### **1. 🥋 GOKU - Orchestrator & Shenron's Voice**
- **Model:** DeepSeek-Coder-V2-Lite-Instruct
- **Model ID:** `deepseek-coder-v2-lite-instruct`
- **Context Length:** 163,840 tokens (reduced to 32,768 for RAM efficiency)
- **Temperature:** 0.7 (Balanced, friendly)
- **Max Tokens:** 8,192
- **RAM Usage:** ~25 GB
- **Role:** Main orchestrator, friendly helper, synthesizes other responses
- **Personality:** Helpful, encouraging, explains things clearly
- **Response Time:** 20-40 seconds (slowest, but most powerful)

#### **2. 👑 VEGETA - Technical Authority**
- **Model:** Llama 3.2 3B Instruct
- **Model ID:** `llama-3.2-3b-instruct`
- **Context Length:** 32,768 tokens
- **Temperature:** 0.3 (Very precise, minimal creativity)
- **Max Tokens:** 4,096
- **RAM Usage:** ~4 GB
- **Role:** Technical expert, fact-checker, precise answers
- **Personality:** Serious, authoritative, no-nonsense
- **Response Time:** 15-30 seconds

#### **3. 🧠 PICCOLO - Strategic Sage**
- **Model:** Qwen2.5-Coder 7B Instruct
- **Model ID:** `qwen2.5-coder-7b-instruct`
- **Context Length:** 32,768 tokens
- **Temperature:** 0.6 (Thoughtful, strategic)
- **Max Tokens:** 4,096
- **RAM Usage:** ~7 GB
- **Role:** Strategic planner, long-term thinking, architecture
- **Personality:** Wise, contemplative, considers implications
- **Response Time:** 40-90 seconds (largest model, may take longer)

#### **4. ⚠️ GOHAN - Risk Sentinel**
- **Model:** Mistral 7B Instruct v0.3
- **Model ID:** `mistral-7b-instruct-v0.3`
- **Context Length:** 32,768 tokens
- **Temperature:** 0.4 (Cautious, risk-aware)
- **Max Tokens:** 4,096
- **RAM Usage:** ~7 GB
- **Role:** Risk assessment, security warnings, "what could go wrong"
- **Personality:** Cautious, protective, identifies potential issues
- **Response Time:** 20-40 seconds

#### **5. 🔧 KRILLIN - Practical Engineer**
- **Model:** Phi-3-Mini 128K Instruct
- **Model ID:** `phi-3-mini-128k-instruct`
- **Context Length:** 32,768 tokens (supports up to 128K)
- **Temperature:** 0.5 (Balanced, practical)
- **Max Tokens:** 2,048
- **RAM Usage:** ~10 GB
- **Role:** Hands-on implementation, practical solutions
- **Personality:** Pragmatic, down-to-earth, "let's just do it"
- **Response Time:** 10-20 seconds (smallest, fastest)

#### **6. 😈 FRIEZA - Chaos Tyrant**
- **Model:** Phi-3-Mini 128K Instruct (Instance #2)
- **Model ID:** `phi-3-mini-128k-instruct:2`
- **Context Length:** 32,768 tokens
- **Temperature:** 0.9 (High creativity, chaotic)
- **Max Tokens:** 2,048
- **RAM Usage:** ~8 GB
- **Role:** Devil's advocate, contrarian views, creative chaos
- **Personality:** Provocative, controversial, challenges assumptions
- **Response Time:** 10-20 seconds (smallest, fastest)

### **Personality Files & Documentation**

**Note:** Detailed personality definitions are embedded in the orchestrator code. The following locations contain personality information:

#### **1. Orchestrator Code (Persona Definitions)**
- **File:** `Dell-Server-Roadmap/backend/shenron/shenron_v4_orchestrator.py`
- **Lines:** 62-111 (FIGHTERS array with persona strings)
- **File:** `BitPhoenix/backend/shenron/shenron_v4_orchestrator.py`
- **Lines:** 84-110 (FIGHTERS array with persona strings)

#### **2. LM Studio Preset Files (Full System Prompts)**
- **Location on VM100:** `C:\GOKU-AI\knowledge-base\prompts\` (mentioned in docs, may contain .txt files)
- **Preset Archive:** `shenrons-syndicate-presets-v3.2-JSON.tar.gz` (contains preset.json files with full system prompts)
- **GitHub Reference:** `Dell-Server-Roadmap/SHENRON-PRESETS-v3.2-DEPLOYMENT.md`

#### **3. Current Persona Strings (from orchestrator code):**
- **GOKU:** "Energetic Saiyan hero who speaks with upbeat encouragement, references training and growth, keeps things simple and motivational while still giving concrete guidance."
- **VEGETA:** "Proud Saiyan prince with sharp sarcasm; delivers precise technical insights, battle metaphors, and confident critiques without losing professionalism."
- **PICCOLO:** "Calm Namekian tactician who analyzes situations methodically, balances offense/defense, and offers stepwise strategies with disciplined tone."
- **GOHAN:** "Thoughtful scholar-warrior focused on risk, safeguards, and preparedness; careful tone, highlights edge cases and mitigation paths."
- **KRILLIN:** "Down-to-earth human engineer with hands-on tips, light humor, and actionable checklists aimed at quick wins and reliability."
- **FRIEZA:** "Elegant villain who relishes controlled chaos; offers cunning insights, hints at domination, yet remains begrudgingly helpful."

**Note:** More detailed personality files (like the FRIEZA example with "SYNDICATE ROLE", "YOUR POWER", "RESPONSE FORMAT", etc.) may exist in:
- `C:\GOKU-AI\knowledge-base\prompts\` on VM100 (Windows path, not in GitHub)
- Within the preset.json files in the v3.2-JSON archive
- Or may need to be created/added to the GitHub repository

**For Complete Technical Details:**
- **Orchestrator Implementation:** See `SHENRON-ORCHESTRATOR-TECHNICAL-DETAILS.md` for:
  - Full FIGHTERS definitions with code
  - Synthesis logic and sample outputs
  - RAG integration details
  - Orchestration flow diagrams
  - Variations and extensions

### **Total AI System Resources**
- **Total RAM (active):** ~63 GB (for all 6 models)
- **Total Models:** 6 concurrent
- **7th AI:** SHENRON (synthesizer, not separate model)
- **Total Query Time:** 45-90 seconds for all 6 (parallel processing)

### **Model Configuration (LM Studio)**
**Global Settings:**
- ✅ Serve on Local Network: Enabled
- ✅ Enable CORS: Enabled
- ✅ Port: 1234
- ❌ JIT models auto-evict: Disabled (keep all 6 loaded)
- ✅ Restore previous session on startup: Enabled
- ✅ Auto-load models from previous session: Enabled

**Individual Model Settings:**
| Fighter | Context Length | Max Tokens | Temperature | Top P | Top K | Min P | Repeat Penalty |
|---------|----------------|------------|-------------|-------|-------|-------|----------------|
| GOKU | 32,768 | 8,192 | 0.7 | 0.9 | 40 | 0.05 | 1.1 |
| VEGETA | 32,768 | 4,096 | 0.3 | 0.9 | 40 | 0.05 | 1.1 |
| PICCOLO | 32,768 | 4,096 | 0.6 | 0.9 | 40 | 0.05 | 1.1 |
| GOHAN | 32,768 | 4,096 | 0.4 | 0.9 | 40 | 0.05 | 1.1 |
| KRILLIN | 32,768 | 2,048 | 0.5 | 0.9 | 40 | 0.05 | 1.1 |
| FRIEZA | 32,768 | 2,048 | 0.9 | 0.9 | 40 | 0.05 | 1.1 |

---

## 🖥️ VM101 UBUNTU - NEW CONTROL NODE PLAN

### **Current Status**
- **VM ID:** 101
- **IP Address:** <VM101_IP>
- **Hostname:** ai-assistant-vm
- **User:** mgmt1
- **OS:** Ubuntu 24.04 LTS (planned) / Ubuntu 22.04 (current docs)
- **Status:** ⚠️ **PLANNED** - To become new control node

### **Planned Specifications**
- **CPU:** 4-8 cores
- **RAM:** 8-32 GB (docs show 8GB in some places, 32GB in others)
- **Storage:** 500 GB SSD
- **Purpose:** Central management and AI development environment

### **Planned Software Stack**
1. **code-server (VS Code Server)**
   - Port: 8080
   - Web-based IDE access
   - Accessible via SSH tunnel or Cloudflare

2. **Python Environment**
   - Python 3.11+
   - Virtual environment: `~/ai-workspace/ai-env/`
   - AI/ML libraries (numpy, pandas, torch, transformers, etc.)

3. **Docker**
   - Container runtime for development

4. **SSH Key Access**
   - SSH keys configured for all VMs:
     - VM120 (proxy1@<VM120_IP>)
     - VM150 (wp1@<VM150_IP>)
     - VM160 (dbs1@<VM160_IP>)
     - VM170 (gsh1@<VM170_IP>)
     - VM180 (apis1@<VM180_IP>)
     - VM200 (plex1@<VM200_IP>)

5. **Git Repositories**
   - All GitHub repos cloned to `~/GitHub/`
   - Dell-Server-Roadmap
   - BitPhoenix
   - Goku.AI
   - And others

6. **Management Scripts**
   - VM status checking
   - SSH shortcuts
   - Backup automation

### **Migration Plan**
**Phase 1:** Setup VM101 as management node
- Install base system
- Configure SSH keys
- Install development tools
- Clone repositories

**Phase 2:** Transfer control functions
- Move management scripts from VM100
- Set up centralized monitoring
- Configure automated backups

**Phase 3:** Make VM101 primary control node
- Update documentation
- Update access patterns
- Decommission management functions on VM100

---

## 🌐 VM120 - REVERSE PROXY & CLOUDFLARE

### **Current Status**
- **IP Address:** <VM120_IP>
- **Hostname:** reverse-proxy-gateway
- **OS:** Ubuntu 24.04 LTS
- **User:** proxy1
- **Resources:** 6 cores, 6GB RAM, 500GB SSD
- **Status:** ✅ Operational

### **Services Running**

#### **1. Cloudflare Tunnel (cloudflared)**
- **Tunnel Name:** norelec-tunnel
- **Tunnel ID:** 624c59c6-b364-4488-85e5-90225351b0e2
- **Credentials:** `/home/proxy1/.cloudflared/624c59c6-b364-4488-85e5-90225351b0e2.json`
- **Status:** ✅ Active
- **Service:** `systemctl status cloudflared`

**Current Routes:**
```yaml
ingress:
  - hostname: wp.lightspeedup.com
    service: http://localhost:80
  - hostname: shenron.lightspeedup.com
    service: http://<VM150_IP>:80
  - service: http_status:404
```

#### **2. Nginx Reverse Proxy**
- **Status:** ✅ Active (if configured)
- **Port:** 80 (HTTP), 443 (HTTPS via Cloudflare)
- **Purpose:** Local HTTP routing and header management

### **Cloudflare Configuration**
- **Account:** sethpizzaboy@gmail.com
- **Domain:** lightspeedup.com
- **DNS Provider:** Cloudflare
- **SSL/TLS:** Full (Strict) mode
- **DDoS Protection:** ✅ Enabled
- **WAF:** ✅ Enabled

**Active DNS Records:**
| Type | Name | Target | Status | Purpose |
|------|------|--------|--------|---------|
| CNAME | wp | 624c59c6-...cfargotunnel.com | ✅ Proxied | WordPress site |
| CNAME | shenron | 624c59c6-...cfargotunnel.com | ✅ Proxied | AI Council interface |

---

## 🌐 VM150 - WEB SERVER (APACHE)

### **Current Status**
- **IP Address:** <VM150_IP>
- **Hostname:** wordpress-1
- **OS:** Ubuntu 24.04 LTS
- **User:** wp1
- **Resources:** 8 cores, 32 GB RAM, 500 GB SSD
- **Status:** ✅ Operational

### **Web Server Stack**
- **Web Server:** Apache 2.4.58
- **PHP:** 8.x
- **Database:** MySQL/MariaDB (internal)

### **Hosted Sites**
1. **lightspeedup.com** (Main site + Beta program)
2. **www.lightspeedup.com** (WWW alias)
3. **wp.lightspeedup.com** (WordPress admin access)
4. **shenron.lightspeedup.com** (AI Council web interface) ⭐

### **Shenron Website Files**
**Location:** `/var/www/shenron.lightspeedup.com/`

**Files:**
- `index.html` - Main HTML structure (v4.2.0)
- `style.css` - DBZ-themed styling with starfield animation
- `script.js` - Frontend logic (V2 with real-time progress)
- `api.php` - PHP proxy to LM Studio API

**Apache Configuration:**
- **Virtual Host:** `shenronsyndicate.conf`
- **DocumentRoot:** `/var/www/shenron.lightspeedup.com/`
- **TimeOut:** 1800 seconds (30 minutes)
- **ProxyTimeout:** 1800 seconds
- **LimitRequestBody:** 52428800 (50MB)
- **PHP Memory:** 512MB
- **PHP Timeout:** 1800 seconds (30 minutes)

### **API Proxy (api.php)**
**Purpose:**
- Forwards browser requests to VM100's LM Studio API
- Bypasses CORS restrictions
- Adds security layer
- Handles timeouts gracefully

**Configuration:**
```php
LM_STUDIO_API: http://<VM100_IP>:1234/v1/chat/completions
SHENRON_API: http://<VM100_IP>:5000/api/shenron/grant-wish
PHP Timeout: 1800 seconds (30 minutes)
CURL Timeout: 900 seconds (15 minutes per model)
```

---

## 📂 FILE LOCATIONS IN GITHUB DIRECTORY

### **Main Project Directories**

#### **1. Dell-Server-Roadmap/**
**Location:** `C:\Users\sethp\Documents\Github\Dell-Server-Roadmap\`

**Key Subdirectories:**
- `backend/` - Backend services and orchestrators
- `web/shenron-ui/` - Web interface files (HTML, CSS, JS)
- `shenron-v3-deployment/` - Deployment scripts and configs
- `shenron-ultra-instinct/` - Ultra Instinct mode implementation
- `docs/` - Complete documentation
- `knowledge-base/` - Knowledge base markdown files
- `scripts/` - Management and deployment scripts
- `configs/` - Configuration files

**Key Files:**
- `docs/SHENRON-SYNDICATE-COMPLETE-DOCUMENTATION.md` - Full system docs
- `docs/server-infrastructure-documentation.md` - Infrastructure specs
- `docs/vm-101-setup-guide.md` - VM101 setup instructions
- `VM100-BEAST-MODE-UPGRADE.md` - Hardware upgrade details
- `AI-COLLAB-SHENRON-SYNDICATE-COMPLETE-PROJECT.md` - Project overview
- `knowledge-base/shenron-current-hardware-config-2025-11-06.md` - Current config

#### **2. Goku.AI/**
**Location:** `C:\Users\sethp\Documents\Github\Goku.AI\`

**Contents:**
- `shenron-ultra-instinct/phase1/`
  - `mcp_tools.py` - MCP tools implementation
  - `shenron_api_v5_mcp.py` - API v5 with MCP support

#### **3. BitPhoenix/**
**Location:** `C:\Users\sethp\Documents\Github\BitPhoenix\`

**Key Files:**
- `backend/shenron/shenron_v4_orchestrator.py` - v4 orchestrator
- `backend/ENV_CONFIGURATION.md` - Environment configuration

### **Shenron Web Interface Files**
**Location on VM150:** `/var/www/shenron.lightspeedup.com/`
**Source Location:** `C:\Users\sethp\Documents\Github\Dell-Server-Roadmap\web\shenron-ui\`

**Files:**
- `index.html` - Main interface (v4.2.0, last updated Nov 7, 2025)
- `style.css` - Styling
- `script.js` - Frontend JavaScript
- `api.php` - PHP proxy

---

## 🔌 PORTS AND NETWORK CONFIGURATION

### **Port Allocation by Service**

| Port | Service | VM | Status | Purpose |
|------|---------|-----|--------|---------|
| **22** | SSH | All VMs | ✅ Active | Remote access |
| **80** | HTTP (Apache) | VM150 | ✅ Active | Web server |
| **443** | HTTPS | VM120 (Cloudflare) | ✅ Active | SSL termination |
| **1234** | LM Studio API | VM100 | ✅ Active | AI model serving (internal) |
| **5000** | SHENRON API | VM100 | ✅ Active | Orchestrator API |
| **8080** | code-server | VM101 | ⏭️ Planned | VS Code Server |
| **3306** | MySQL | VM150 | 🔒 Internal | Database (not exposed) |
| **6379** | Redis | VM150 | 🔒 Internal | Cache (not exposed) |

### **Network Flow for Shenron Website**

```
Internet User
    ↓
Cloudflare CDN/SSL (Edge Network)
    ↓
Cloudflare Tunnel (VM120: <VM120_IP>)
    ↓
Apache Virtual Host (VM150: <VM150_IP>)
    Domain: shenron.lightspeedup.com
    ↓
api.php (PHP Proxy)
    ↓
LM Studio API (VM100: <VM100_IP>:1234)
    OR
SHENRON API (VM100: <VM100_IP>:5000)
```

### **Internal Network (192.168.12.0/24)**
- **Gateway:** <EDGEROUTER_IP> (EdgeRouter/OPNsense)
- **DNS:** 8.8.8.8, 1.1.1.1
- **Proxmox Host:** <PROXMOX_IP>

---

## 🧠 KNOWLEDGE DATABASE

### **ChromaDB Configuration**
- **Location:** `C:\GOKU-AI\chroma_db\` (on VM100)
- **Collection Name:** "knowledge_base"
- **Embedding Model:** all-MiniLM-L6-v2
- **Size:** ~82.57 MB (as of Nov 6, 2025)
- **Documents Ingested:** 6,977+ chunks

### **Knowledge Base Contents**

#### **Infrastructure & Hardware**
1. `knowledge-base-dell-r730-complete.md` - Dell R730 server specs
2. `knowledge-base-nvidia-grid-k1-complete.md` - GPU passthrough
3. `knowledge-base-windows-server-2025.md` - Windows Server setup
4. `seth-infrastructure.md` - Infrastructure overview

#### **Programming Languages**
5. `knowledge-base-python-311-2025.md` - Python 3.11
6. `knowledge-base-java-21.md` - Java 21
7. `knowledge-base-golang-122.md` - Go 1.22
8. `knowledge-base-rust-175.md` - Rust 1.75
9. `knowledge-base-javascript-typescript.md` - JS/TS
10. `knowledge-base-cpp-23.md` - C++ 23
11. `knowledge-base-ruby-julia-mojo-sqlserver.md` - Ruby, Julia, Mojo, SQL Server

#### **AI/ML & Frameworks**
12. `knowledge-base-week7-ai-powerhouse.md` - AI frameworks
13. `knowledge-base-docker-kubernetes-2025.md` - Containers

#### **Crypto & Trading**
14. `knowledge-base-bitcoin-crypto-trading-2025.md` - Trading
15. `knowledge-base-defi-yield-farming-2025.md` - DeFi
16. `knowledge-base-binance-us-bnb-2025.md` - Binance
17. `knowledge-base-week6-trading-mastery.md` - Trading mastery

#### **Web Development**
18. `knowledge-base-wordpress-monetization-2025.md` - WordPress
19. `knowledge-base-discord-bots-apis-2025.md` - Discord bots

#### **Media & Streaming**
20. `knowledge-base-plex-streamforge-2025.md` - Plex setup

#### **Advanced Topics**
21. `knowledge-base-weeks8-11-complete.md` - Advanced topics
22. `knowledge-advanced-scalpstorm-architecture.md` - ScalpStorm
23. `knowledge-base-project-scalpstorm-80-dollar.md` - Project details

#### **Shenron-Specific**
24. `ETERNAL-DRAGON-SHENRON-KNOWLEDGE.md` - Shenron system knowledge

### **Ingestion Process**
- **Script:** `2-Ingest-Knowledge-Base.py`
- **Location:** `C:\GOKU-AI\shenron\` (on VM100)
- **Chunk Size:** 500 characters
- **Overlap:** 100 characters
- **Batch Size:** 166 (ChromaDB limit)

### **RAG (Retrieval Augmented Generation)**
- **Status:** ✅ Operational
- **Search:** Semantic search before AI queries
- **Context Injection:** Relevant docs injected into prompts
- **Collection:** "knowledge_base" in ChromaDB

---

## 🌐 HTML INTERFACE

### **Shenron Website**
**URL:** https://shenron.lightspeedup.com  
**Local URL:** http://<VM150_IP> (bypasses Cloudflare timeout)

### **Files Location**
**On VM150:** `/var/www/shenron.lightspeedup.com/`  
**Source:** `C:\Users\sethp\Documents\Github\Dell-Server-Roadmap\web\shenron-ui\`

### **File Details**

#### **index.html** (v4.2.0)
- **Last Updated:** Nov 7, 2025
- **Features:**
  - DBZ-themed interface
  - Real-time clock
  - API status indicators
  - Dragon Radar metrics panel
  - Question input form
  - Response display cards
  - Progress tracking

#### **style.css**
- DBZ-themed styling
- Starfield animation
- Glow effects
- Responsive design

#### **script.js** (v4.1.3+)
- Frontend logic
- Real-time progress tracking
- Streaming response display
- API communication
- Error handling

#### **api.php**
- PHP proxy to backend
- Handles CORS
- Timeout management
- Request forwarding

### **Access Methods**

**Option 1: Public Access (via Cloudflare)**
- **URL:** https://shenron.lightspeedup.com
- **Pros:** Accessible from anywhere, HTTPS/SSL
- **Cons:** 100-second timeout limit (Cloudflare Free Plan)
- **Best For:** Quick questions (<70 words)

**Option 2: Local Network Access**
- **URL:** http://<VM150_IP>
- **Pros:** 30-minute timeout, all 6 models respond
- **Cons:** Requires local network access
- **Best For:** Complex, detailed questions

---

## ☁️ CLOUDFLARE & DOMAIN CONFIGURATION

### **Domain: lightspeedup.com**
- **Registrar:** Namecheap (expires Dec 22, 2025)
- **Cloudflare Account:** sethpizzaboy@gmail.com
- **DNS Provider:** Cloudflare
- **SSL/TLS:** Full (Strict) mode

### **Active Subdomains**

| Subdomain | Type | Target | Status | Purpose |
|-----------|------|--------|--------|---------|
| **wp** | CNAME | 624c59c6-...cfargotunnel.com | ✅ Proxied | WordPress site |
| **shenron** | CNAME | 624c59c6-...cfargotunnel.com | ✅ Proxied | AI Council interface |

### **Cloudflare Tunnel Configuration**
- **Tunnel Name:** norelec-tunnel
- **Tunnel ID:** 624c59c6-b364-4488-85e5-90225351b0e2
- **Location:** VM120 (`/etc/cloudflared/config.yml`)
- **Service:** `systemctl status cloudflared`

**Ingress Rules:**
```yaml
ingress:
  - hostname: wp.lightspeedup.com
    service: http://localhost:80
  - hostname: shenron.lightspeedup.com
    service: http://<VM150_IP>:80
  - service: http_status:404
```

### **Cloudflare Features Enabled**
- ✅ DDoS Protection
- ✅ WAF (Web Application Firewall)
- ✅ SSL/TLS: Full (Strict)
- ✅ CDN: Edge network
- ⚠️ Timeout Limit: 100 seconds (Free Plan)

---

## 📊 SUMMARY STATISTICS

### **VM Resources Summary**
| VM | CPU | RAM | Storage | IP | Purpose |
|----|-----|-----|---------|----|---------| 
| **VM100** | 26 vCPUs | 192 GB | 500 GB | <VM100_IP> | AI Host (GOKU-AI) |
| **VM101** | 4-8 cores | 8-32 GB | 500 GB | <VM101_IP> | Control Node (Planned) |
| **VM120** | 6 cores | 6 GB | 500 GB | <VM120_IP> | Reverse Proxy |
| **VM150** | 8 cores | 32 GB | 500 GB | <VM150_IP> | Web Server (Apache) |

### **AI System Summary**
- **Total Models:** 6 concurrent
- **Total RAM Usage:** ~63 GB
- **Total Query Time:** 45-90 seconds (parallel)
- **Accuracy:** 99.9999% (6-model consensus)
- **Knowledge Base:** 6,977+ documents

### **Network Summary**
- **Public Domain:** lightspeedup.com
- **AI Interface:** shenron.lightspeedup.com
- **Internal API:** http://<VM100_IP>:5000
- **LM Studio API:** http://<VM100_IP>:1234

---

## 🔧 ALTERNATIVE METHODS (PowerShell Broken)

Since PowerShell is broken, use these alternatives:

### **For Windows (VM100):**
1. **Command Prompt (cmd.exe)**
   ```cmd
   cd C:\GOKU-AI\shenron
   python -m venv venv
   venv\Scripts\activate.bat
   python script.py
   ```

2. **Python Scripts**
   - Use Python directly for automation
   - SSH from Linux VMs to Windows

3. **SSH from VM101**
   - SSH to VM100 from VM101
   - Run commands remotely

### **For Linux VMs:**
1. **Bash Scripts**
   ```bash
   # All Linux VMs support bash
   ssh wp1@<VM150_IP>
   ```

2. **Python Scripts**
   ```bash
   python3 script.py
   ```

3. **Direct SSH Access**
   - From VM101 to all other VMs
   - From Proxmox host to VMs

---

## 📝 NOTES & DISCLAIMERS

1. **VM100 Specs:** Recently upgraded to "Beast Mode" (192GB RAM, 26 vCPUs) on Nov 6, 2025
2. **VM101 Status:** Currently planned/designed, may not be fully deployed yet
3. **Knowledge Base:** Continuously growing, 6,977+ documents as of Nov 6, 2025
4. **Cloudflare Timeout:** 100-second limit on Free Plan affects complex queries
5. **PowerShell:** Currently broken, use alternatives listed above
6. **File Locations:** Some files may be in different locations than documented - check both VM150 and local GitHub directory

---

## 🔗 QUICK REFERENCE

### **Access URLs**
- **Shenron Website:** https://shenron.lightspeedup.com
- **Local Access:** http://<VM150_IP>
- **SHENRON API:** http://<VM100_IP>:5000
- **LM Studio API:** http://<VM100_IP>:1234

### **SSH Access**
- **VM100:** RDP (Windows) or SSH if configured
- **VM101:** `ssh mgmt1@<VM101_IP>`
- **VM120:** `ssh proxy1@<VM120_IP>`
- **VM150:** `ssh wp1@<VM150_IP>`

### **Key Directories**
- **VM100 Knowledge Base:** `C:\GOKU-AI\knowledge-base\`
- **VM100 ChromaDB:** `C:\GOKU-AI\chroma_db\`
- **VM100 Shenron:** `C:\GOKU-AI\shenron\`
- **VM150 Web Files:** `/var/www/shenron.lightspeedup.com/`
- **Local GitHub:** `C:\Users\sethp\Documents\Github\`

---

**Document Status:** ✅ Complete  
**Last Verified:** Based on documentation as of November 6-7, 2025  
**Next Update:** When VM101 migration is complete

