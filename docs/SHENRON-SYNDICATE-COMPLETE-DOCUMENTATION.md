<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🐉 THE SHENRON SYNDICATE - Complete Documentation

**Last Updated:** November 6, 2025  
**Version:** 2.1  
**Status:** ✅ PRODUCTION - Fully Operational (Long-Form Queries Supported)

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [AI Council Members](#ai-council-members)
4. [Infrastructure](#infrastructure)
5. [Web Interface](#web-interface)
6. [API Configuration](#api-configuration)
7. [Model Configuration](#model-configuration)
8. [Deployment History](#deployment-history)
9. [Access Methods](#access-methods)
10. [Long-Form Query Support](#long-form-query-support)
11. [Troubleshooting](#troubleshooting)
12. [Test Results](#test-results)
13. [Future Enhancements (RAG)](#future-enhancements-rag)

---

## 🎯 OVERVIEW

The **Shenron Syndicate** is a multi-model AI council system that provides diverse perspectives through 6 different AI personalities (DBZ-Fighters), each with unique characteristics, roles, and temperature settings.

### Purpose
- **Multi-Model Consensus**: Combine strengths of different LLMs
- **Diverse Perspectives**: From ultra-precise technical (VEGETA) to creative chaos (FRIEZA)
- **Infrastructure Knowledge**: Upcoming RAG integration for server awareness
- **Devil's Advocate**: FRIEZA provides contrarian viewpoints
- **Public Access**: Available at https://shenron.lightspeedup.com

### Key Features
- ✅ 6 specialized AI personalities
- ✅ Parallel query processing (all 6 respond simultaneously)
- ✅ Real-time progress tracking with countdown timer
- ✅ Streaming responses (appear as each fighter completes)
- ✅ Temperature-based personality variation
- ✅ Web GUI with DBZ theming
- ✅ PHP proxy to bypass CORS issues
- ✅ Cloudflare SSL integration

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                         INTERNET USER                            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
                    ┌───────────────────────┐
                    │   Cloudflare CDN/SSL  │
                    │   (Edge Network)      │
                    └───────────┬───────────┘
                                │
                                ↓
        ┌───────────────────────────────────────────┐
        │  Cloudflare Tunnel (norelec-tunnel)      │
        │  VM 120: <VM120_IP>                  │
        │  Service: cloudflared                     │
        └───────────────┬───────────────────────────┘
                        │
                        ↓
        ┌───────────────────────────────────────────┐
        │  Apache Virtual Host                      │
        │  VM 150: <VM150_IP>                  │
        │  Domain: shenron.lightspeedup.com│
        │  DocumentRoot: /var/www/shenronsyndicate/ │
        └───────────────┬───────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ↓                               ↓
┌───────────────┐             ┌──────────────────┐
│  Static Files │             │    api.php       │
│  - index.html │             │  (PHP Proxy)     │
│  - script.js  │             └────────┬─────────┘
│  - style.css  │                      │
└───────────────┘                      ↓
                        ┌───────────────────────────┐
                        │  LM Studio API Server     │
                        │  VM 100: <VM100_IP>   │
                        │  Port: 1234               │
                        │  6 Models Running         │
                        └───────────────────────────┘
```

---

## 🥋 AI COUNCIL MEMBERS

### **1. 🥋 GOKU - Orchestrator & Shenron's Voice**
- **Model**: DeepSeek-Coder-V2-Lite-Instruct
- **Model ID**: `deepseek-coder-v2-lite-instruct`
- **Context Length**: 163,840 tokens (reduced to 32,768 for RAM)
- **Temperature**: 0.7 (Balanced, friendly)
- **Max Tokens**: 8,192
- **Role**: Main orchestrator, friendly helper, synthesizes other responses
- **Personality**: Helpful, encouraging, explains things clearly

### **2. 👑 VEGETA - Technical Authority**
- **Model**: Llama 3.2 3B Instruct
- **Model ID**: `llama-3.2-3b-instruct`
- **Context Length**: 32,768 tokens
- **Temperature**: 0.3 (Very precise, minimal creativity)
- **Max Tokens**: 4,096
- **Role**: Technical expert, fact-checker, precise answers
- **Personality**: Serious, authoritative, no-nonsense

### **3. 🧠 PICCOLO - Strategic Sage**
- **Model**: Qwen2.5-Coder 7B Instruct
- **Model ID**: `qwen2.5-coder-7b-instruct`
- **Context Length**: 32,768 tokens
- **Temperature**: 0.6 (Thoughtful, strategic)
- **Max Tokens**: 4,096
- **Role**: Strategic planner, long-term thinking, architecture
- **Personality**: Wise, contemplative, considers implications
- **Note**: Largest model (7B), may take longer to respond

### **4. ⚠️ GOHAN - Risk Sentinel**
- **Model**: Mistral 7B Instruct v0.3
- **Model ID**: `mistral-7b-instruct-v0.3`
- **Context Length**: 32,768 tokens
- **Temperature**: 0.4 (Cautious, risk-aware)
- **Max Tokens**: 4,096
- **Role**: Risk assessment, security warnings, "what could go wrong"
- **Personality**: Cautious, protective, identifies potential issues

### **5. 🔧 KRILLIN - Practical Engineer**
- **Model**: Phi-3-Mini 128K Instruct
- **Model ID**: `phi-3-mini-128k-instruct`
- **Context Length**: 32,768 tokens (supports up to 128K)
- **Temperature**: 0.5 (Balanced, practical)
- **Max Tokens**: 2,048
- **Role**: Hands-on implementation, practical solutions
- **Personality**: Pragmatic, down-to-earth, "let's just do it"

### **6. 😈 FRIEZA - Chaos Tyrant**
- **Model**: Phi-3-Mini 128K Instruct (Instance #2)
- **Model ID**: `phi-3-mini-128k-instruct:2`
- **Context Length**: 32,768 tokens
- **Temperature**: 0.9 (High creativity, chaotic)
- **Max Tokens**: 2,048
- **Role**: Devil's advocate, contrarian views, creative chaos
- **Personality**: Provocative, controversial, challenges assumptions

---

## 🖥️ INFRASTRUCTURE

### **VM 100 - GOKU-AI Host**

| Specification | Value |
|---------------|-------|
| **Hostname** | GOKU-AI |
| **OS** | Windows Server 2025 |
| **IP Address** | <VM100_IP> |
| **CPU** | 16 cores (Xeon E5-2698 v3) |
| **RAM** | 65 GB DDR4 ECC |
| **Storage** | 500 GB SSD |
| **Auto-Login** | ✅ Enabled (Administrator) |
| **LM Studio** | v0.3.31 (auto-start on boot) |

### **Software Stack**
- **LM Studio**: Local LLM runtime and API server
- **Microsoft ML Server 9.4.7**: Enterprise AI/ML capabilities
- **Python 3.11**: Automation and scripting
- **PowerShell**: System management
- **SSH/SCP**: Remote access capabilities

### **Network Configuration**
- **Port 1234**: LM Studio API (internal only, not exposed)
- **DNS**: 8.8.8.8, 1.1.1.1
- **Gateway**: <EDGEROUTER_IP> (OPNsense)

### **VM 150 - WordPress Host (Web Interface)**

| Specification | Value |
|---------------|-------|
| **Hostname** | wordpress-1 |
| **OS** | Ubuntu 24.04 LTS |
| **IP Address** | <VM150_IP> |
| **CPU** | 8 cores |
| **RAM** | 32 GB |
| **Storage** | 500 GB SSD |
| **Web Server** | Apache 2.4.58 |
| **PHP** | 8.x |

### **VM 120 - Reverse Proxy (Cloudflare Tunnel)**

| Specification | Value |
|---------------|-------|
| **Hostname** | reverse-proxy-gateway |
| **OS** | Ubuntu 24.04 LTS |
| **IP Address** | <VM120_IP> |
| **Service** | cloudflared (Cloudflare Tunnel) |
| **Tunnel ID** | norelec-tunnel |

---

## 🌐 WEB INTERFACE

### **Access**
- **Public URL**: https://shenron.lightspeedup.com
- **SSL**: Cloudflare Flexible SSL (automatic)
- **CDN**: Cloudflare edge network

### **Files**
```
/var/www/shenron.lightspeedup.com/
├── index.html     # Main HTML structure
├── style.css      # DBZ-themed styling with starfield animation
├── script.js      # Frontend logic (V2 with real-time progress)
└── api.php        # PHP proxy to LM Studio API
```

### **Features**
1. **Question Input**: Textarea for user questions
2. **Summon Button**: Triggers parallel AI queries
3. **Progress Bar**: Real-time tracking with percentage and countdown
4. **Status Indicators**: Live status for each DBZ-Fighter
5. **Response Cards**: Styled cards with fighter emoji, name, role, and response
6. **Streaming Display**: Responses appear immediately as each fighter completes

### **Progress Bar V2**
- **Format**: `"3/6 Fighters Responded | 50% Complete | EST: 18s remaining"`
- **Updates**: Every 1 second
- **Calculation**: Dynamic ETA based on average response time
- **Animation**: Smooth 0% → 100% progress fill
- **Auto-hide**: 2 seconds after completion

---

## 🔌 API CONFIGURATION

### **api.php Proxy**

**Location**: `/var/www/shenron.lightspeedup.com/api.php`

**Purpose**:
- Forwards browser requests to VM100's LM Studio API
- Bypasses CORS restrictions
- Adds security layer
- Handles timeouts gracefully

**Configuration**:
```php
// LM Studio API endpoint
define('LM_STUDIO_API', 'http://<VM100_IP>:1234/v1/chat/completions');

// Timeouts
set_time_limit(600);                     // 10 minute PHP execution
curl_setopt($ch, CURLOPT_TIMEOUT, 120); // 2 minute per model
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10); // 10 second connection
```

**Headers**:
```php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
```

### **Request Format**
```json
{
  "model": "deepseek-coder-v2-lite-instruct",
  "messages": [
    {
      "role": "user",
      "content": "What are the specs of VM100?"
    }
  ],
  "max_tokens": 8192,
  "temperature": 0.7,
  "top_p": 0.9,
  "stream": false
}
```

### **Response Format**
```json
{
  "id": "chatcmpl-xxxxx",
  "object": "chat.completion",
  "created": 1762341677,
  "model": "deepseek-coder-v2-lite-instruct",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "VM100 is running Windows Server 2025...",
        "reasoning_content": "",
        "tool_calls": []
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 123,
    "total_tokens": 138
  }
}
```

---

## ⚙️ MODEL CONFIGURATION

### **LM Studio Settings**

**Path**: `C:\Users\Administrator\.lmstudio\` (on VM100)

**Global Settings**:
- ✅ **Serve on Local Network**: Enabled
- ✅ **Enable CORS**: Enabled
- ✅ **Port**: 1234
- ❌ **JIT models auto-evict**: Disabled (keep all 6 loaded)
- ✅ **Restore previous session on startup**: Enabled
- ✅ **Auto-load models from previous session**: Enabled
- ❌ **When selecting a model to load, first unload any currently loaded ones**: Disabled
- ✅ **Enable model load configuration support in presets**: Enabled

### **Individual Model Settings**

Each model has its own chat in LM Studio with specific settings:

| Fighter | Context Length | Max Tokens | Temperature | Top P | Top K | Min P | Repeat Penalty |
|---------|----------------|------------|-------------|-------|-------|-------|----------------|
| GOKU | 32,768 | 8,192 | 0.7 | 0.9 | 40 | 0.05 | 1.1 |
| VEGETA | 32,768 | 4,096 | 0.3 | 0.9 | 40 | 0.05 | 1.1 |
| PICCOLO | 32,768 | 4,096 | 0.6 | 0.9 | 40 | 0.05 | 1.1 |
| GOHAN | 32,768 | 4,096 | 0.4 | 0.9 | 40 | 0.05 | 1.1 |
| KRILLIN | 32,768 | 2,048 | 0.5 | 0.9 | 40 | 0.05 | 1.1 |
| FRIEZA | 32,768 | 2,048 | 0.9 | 0.9 | 40 | 0.05 | 1.1 |

**Note**: Context Length was reduced from DeepSeek's max (163,840) to 32,768 to ensure all 6 models can run simultaneously within 65GB RAM.

### **System Prompts** (Future)

System prompts are stored at:
`C:\GOKU-AI\knowledge-base\prompts\`

Each fighter has a `.txt` file with their personality definition.

---

## 📜 DEPLOYMENT HISTORY

### **Version 1.0 (November 5, 2025)**
- ✅ Initial deployment
- ✅ 6 AI models configured
- ✅ Web interface created
- ✅ PHP proxy implemented
- ✅ Cloudflare Tunnel integration
- ❌ Issue: HTTP 400 errors (wrong model names with prefixes)
- ❌ Issue: HTTP 524 timeouts (models took too long)

### **Version 1.1 (November 5, 2025 - Hotfix)**
- ✅ Fixed model names (removed `deepseek-ai/`, `meta-llama/`, etc. prefixes)
- ✅ Changed API endpoint from direct LM Studio to `/api.php` proxy
- ✅ 5/6 fighters responding (PICCOLO timeout)
- ❌ Issue: Progress bar didn't reset
- ❌ Issue: All responses showed at once (not streaming)
- ❌ Issue: No time estimate

### **Version 2.0 (November 5, 2025 - Major Update)**
- ✅ Real-time progress bar with percentage display
- ✅ Live countdown timer with dynamic ETA calculation
- ✅ Streaming responses (appear immediately as each completes)
- ✅ Increased PHP timeout: 300s → 600s (10 minutes)
- ✅ Optimized per-model timeout: 300s → 120s (2 minutes)
- ✅ Added connection timeout: 10 seconds
- ✅ Smooth fade-in animations for response cards
- ✅ Progress bar resets to 0% on each new query
- ✅ All 6 fighters responding successfully
- ✅ No more 524 timeouts (parallel processing)

---

## 🔧 TROUBLESHOOTING

### **HTTP 524 (Cloudflare Timeout)**
**Symptom**: All fighters show "HTTP 524" error  
**Cause**: Cloudflare has 100-second timeout, sequential queries exceed this  
**Solution**: V2 runs queries in parallel, each with 2-minute max  

### **HTTP 400 (Bad Request)**
**Symptom**: Specific fighters show "HTTP 400"  
**Cause**: Model name mismatch (e.g., `deepseek-ai/` prefix)  
**Solution**: Use exact model IDs from LM Studio `/v1/models` endpoint  

### **"Failed to fetch"**
**Symptom**: JavaScript console shows "Failed to fetch"  
**Cause**: Browser trying to reach VM100 directly (CORS issue)  
**Solution**: Ensure `API_BASE = "/api.php"` in script.js  

### **Progress bar stuck at 0%**
**Symptom**: Progress doesn't update  
**Cause**: JavaScript `updateProgress()` not being called  
**Solution**: V2 uses `setInterval()` to update every second  

### **Responses don't appear**
**Symptom**: Progress completes but no response cards  
**Cause**: `displaySingleResponse()` not being called  
**Solution**: Each fighter's promise calls display immediately after completion  

### **Out of Memory in LM Studio**
**Symptom**: "Failed to allocate compute pp buffers"  
**Cause**: Context length too high for available RAM  
**Solution**: Reduce context length to 32,768 for all models  

### **Models not auto-loading on boot**
**Symptom**: LM Studio opens but no models loaded  
**Fix**: Enable "Restore previous session" and "Auto-load models" in settings  

---

## 🌐 ACCESS METHODS

The Shenron Syndicate can be accessed in two ways, each with different capabilities:

### **Option 1: Public Access (via Cloudflare)**

**URL**: `https://shenron.lightspeedup.com`

**Pros**:
- ✅ Accessible from anywhere with internet
- ✅ HTTPS/SSL encryption via Cloudflare
- ✅ No VPN or local network required
- ✅ Professional domain name

**Cons**:
- ⚠️ **100-second timeout limit** (Cloudflare Free Plan)
- ⚠️ Complex queries may timeout (returns HTTP 524)
- ⚠️ Only KRILLIN/FRIEZA respond to long questions

**Best For**:
- Quick questions (<70 words)
- Simple technical queries
- Testing the interface
- Public demonstrations

---

### **Option 2: Local Network Access (No Cloudflare)**

**URL**: `http://<VM150_IP>`

**Pros**:
- ✅ **30-minute timeout** (full backend capability)
- ✅ ALL 6 DBZ-Fighters respond to complex questions
- ✅ 50MB POST limit (5000+ line code/output)
- ✅ No external dependencies
- ✅ Faster response times (local network)

**Cons**:
- ❌ Requires local network access (192.168.12.x subnet)
- ❌ No SSL encryption
- ❌ Not accessible from internet

**Best For**:
- Complex, detailed questions
- Long-form analyses
- Large code/output sharing (5000+ lines)
- Testing all 6 models simultaneously
- Internal use

---

### **Comparison Table**

| Feature | Public (Cloudflare) | Local Network |
|---------|---------------------|---------------|
| **URL** | https://shenron.lightspeedup.com | http://<VM150_IP> |
| **Timeout** | 100 seconds | 30 minutes (1800s) |
| **Models Responding** | 1-2 (KRILLIN/FRIEZA) | All 6 |
| **POST Limit** | ~100KB | 50MB |
| **Access From** | Anywhere | Local network only |
| **SSL** | ✅ Yes | ❌ No |
| **Complex Queries** | ⚠️ May timeout | ✅ Fully supported |

---

## ⚡ LONG-FORM QUERY SUPPORT

### **What Changed (v2.1 - November 6, 2025)**

The backend was upgraded to support complex, long-form queries with massive inputs:

**Backend Capabilities**:
- ✅ **PHP Timeout**: 30 minutes (1800 seconds)
- ✅ **Apache Timeout**: 30 minutes (1800 seconds)
- ✅ **CURL Timeout**: 15 minutes per model (900 seconds)
- ✅ **POST Body Size**: 50MB (LimitRequestBody 52428800)
- ✅ **PHP Memory**: 512MB
- ✅ **Apache Proxy**: mod_proxy, mod_proxy_http enabled

**Input Capacity**:
- Each model: **32,768 token context window**
- ~130,000 characters total (input + output)
- ~**5,000-10,000 lines of code** per query
- Complex multi-part questions supported

**Files Changed**:
```bash
# PHP Proxy (VM150)
/var/www/shenron.lightspeedup.com/api.php
  - set_time_limit(1800)
  - CURLOPT_TIMEOUT: 900
  - CURLOPT_CONNECTTIMEOUT: 30

# Apache Configuration (VM150)
/etc/apache2/sites-available/shenronsyndicate.conf
  - TimeOut 1800
  - ProxyTimeout 1800
  - LimitRequestBody 52428800

# PHP Configuration (VM150)
/etc/php/8.3/apache2/php.ini
  - max_execution_time = 1800
  - memory_limit = 512M
  - post_max_size = 50M
  - upload_max_filesize = 50M
```

### **Why Cloudflare Still Times Out**

Cloudflare Free Plan has a **hard 100-second limit** for HTTP connections. This cannot be changed without upgrading to Cloudflare Pro ($20/month).

**What Happens**:
1. User asks complex question via `https://shenron.lightspeedup.com`
2. Request goes: Browser → Cloudflare → Cloudflare Tunnel (VM120) → Apache (VM150) → LM Studio (VM100)
3. Small models (KRILLIN/FRIEZA) respond in <100s ✅
4. Large models (DeepSeek/Llama/Qwen/Mistral) take >100s ❌
5. Cloudflare cuts connection after 100s (HTTP 524)
6. Backend continues processing, but browser never receives response

**Workarounds**:
1. **Use local access**: `http://<VM150_IP>` (no Cloudflare)
2. **Break up questions**: Ask 3-4 shorter questions instead of 1 long one
3. **Upgrade Cloudflare**: Pro plan ($20/month) extends timeouts
4. **Implement streaming**: Server-Sent Events (SSE) bypass timeout (future enhancement)

---

## 🧪 TEST RESULTS

### **Test #1: Complex Long-Form Query (November 6, 2025)**

**Question Asked**:
> "What is your name, Purpose, and what are the below Settings you are running along with your model type, version Author. Quantization Temperature Top P Max Tokens Context Length Min P 0.05 Top K 40 Repeat Penalty Also Please include the time it took you to respond, the time it took for the printout to complete, and and Ideas to improve yourself with system performance specs."

**Access Method**: Local (`http://<VM150_IP>`)

**Results**:

| Fighter | Model Identified | Response Time | Status |
|---------|-----------------|---------------|---------|
| 🥋 GOKU | DeepSeek Coder V2 Lite | ~instant | ✅ Success |
| 👑 VEGETA | Llama 3.2 3B | 100-200ms | ✅ Success |
| 🧠 PICCOLO | Qwen 2.5 Coder 7B | 0.1s | ✅ Success |
| ⚠️ GOHAN | "Model-3" (Mistral 7B) | 0.2s | ✅ Success |
| 🔧 KRILLIN | Phi-3 Mini (Microsoft) | Instant | ✅ Success |
| 😈 FRIEZA | Phi-3 Mini (Microsoft) | 0.5s | ⚠️ Duplicate? |

**Key Findings**:
1. ✅ **All 6 models responded** to complex question
2. ✅ **No HTTP 524 errors** (local access bypassed Cloudflare)
3. ✅ **30-minute timeout worked perfectly**
4. ⚠️ **KRILLIN & FRIEZA both identified as "Phi-3 Mini"** (possible duplicate)
5. ⚠️ **Some models don't self-identify correctly** (GOHAN said "Model-3" instead of "Mistral")

**Model Specs Reported**:

**GOKU (DeepSeek)**:
- Version: 1.0
- Author: DeepSeek (China)
- Response: "~instant"

**VEGETA (Llama)**:
- Version: 2022-02-01
- Quantization: 16-bit float
- Temperature: 1.0
- Max Tokens: 2048
- Context: 512 tokens

**PICCOLO (Qwen)**:
- Author: Alibaba Cloud
- Temperature: 0.7
- Max Tokens: 512
- Context: 4096 tokens
- Hardware: Intel Xeon + Tesla P100 (reported by model)

**GOHAN (Mistral)**:
- Identified as "Model-3"
- Response: 0.2 seconds
- Did not self-identify as Mistral

**KRILLIN (Phi-3)**:
- Author: Microsoft
- Response: Instantaneous

**FRIEZA (Phi-3)**:
- Author: Microsoft (same as KRILLIN!)
- Response: 0.5 seconds

### **TODO: Verify Model Configuration**

**Action Required**:
- Check LM Studio on VM100 to verify FRIEZA is using a different model
- Expected: FRIEZA should use a larger creative model (e.g., Mixtral, GPT-4-style)
- Current: Both KRILLIN and FRIEZA report as "Phi-3 Mini"

**How to Check**:
1. RDP to VM100 (<VM100_IP>)
2. Open LM Studio
3. Check loaded models/chats
4. Verify each chat uses a distinct model

---

## 🚀 FUTURE ENHANCEMENTS (RAG)

### **Planned: RAG (Retrieval Augmented Generation)**

**Goal**: Give the Shenron Syndicate knowledge about your Dell R730 infrastructure.

**Components**:
1. **Vector Database**: ChromaDB for document embeddings
2. **Embedding Model**: sentence-transformers
3. **Knowledge Base**: Infrastructure docs, VM configs, ZFS status
4. **Semantic Search**: Query docs before asking AI
5. **Context Injection**: Inject relevant docs into prompts

**Knowledge Base Files**:
```
C:\GOKU-AI\knowledge-base\
├── infrastructure.md          # Proxmox, VMs, network
├── system-instructions.md     # GOKU-AI operational guidelines
├── marketing-guidelines.md    # Brand voice, messaging
├── project-vision.md          # Mission, roadmap
├── freelancer-fiverr.md      # Service catalog
├── website-rules.md           # lightspeedup.com requirements
├── shenron-syndicate.md      # AI council config
├── self-learning-protocol.md # How GOKU learns
└── learned-behaviors.md      # Auto-updated learnings
```

**Example RAG Query**:
```
User: "What VMs are running?"
→ RAG searches knowledge-base/infrastructure.md
→ Finds VM list with IPs and purposes
→ Injects into prompt: "Based on this infrastructure doc: [...]"
→ AI responds with accurate, current info
```

**TODO**:
- [ ] Install ChromaDB on VM100
- [ ] Create embedding service
- [ ] Build ingestion script for knowledge base
- [ ] Update api.php to do semantic search before AI query
- [ ] Test RAG with sample infrastructure questions

---

## 📊 PERFORMANCE METRICS

### **Response Times** (Approximate)
- **GOKU (DeepSeek)**: 20-40 seconds
- **VEGETA (Llama 3.2)**: 15-30 seconds
- **PICCOLO (Qwen 7B)**: 40-90 seconds (largest model)
- **GOHAN (Mistral)**: 20-40 seconds
- **KRILLIN (Phi-3)**: 10-20 seconds (smallest)
- **FRIEZA (Phi-3)**: 10-20 seconds (smallest)

**Total Time**: 45-90 seconds for all 6 (parallel processing)

### **Resource Usage** (VM100)
- **RAM**: ~50-60 GB (6 models loaded)
- **CPU**: Burst to 80-100% during inference
- **Disk I/O**: Minimal (models loaded in RAM)
- **Network**: ~1-5 Mbps (API requests/responses)

---

## 🎓 LESSONS LEARNED

1. **Model Naming**: LM Studio uses simple names, not full HuggingFace paths
2. **Context Length**: Balance between capability and RAM usage
3. **Parallel Processing**: Essential for web UX, avoids timeouts
4. **PHP Proxy**: Simplest CORS solution, better than Nginx config
5. **Temperature Matters**: 0.3 (VEGETA) vs 0.9 (FRIEZA) = night and day
6. **Progress Feedback**: Users need to see something happening
7. **Auto-Login/Start**: Critical for VM reboots after power loss

---

## 📝 MAINTENANCE NOTES

### **Weekly**
- [ ] Check LM Studio is running on VM100
- [ ] Verify all 6 models are loaded
- [ ] Test web interface accessibility
- [ ] Review Apache error logs on VM150

### **Monthly**
- [ ] Update LM Studio to latest version
- [ ] Check for model updates (new quantizations)
- [ ] Review VM100 disk space
- [ ] Backup knowledge base files

### **After Proxmox Reboot**
- [ ] Verify VM100 auto-login worked
- [ ] Verify LM Studio auto-started
- [ ] Verify all 6 chats are loaded
- [ ] Test Cloudflare Tunnel on VM120

---

## 🔗 RELATED DOCUMENTATION

- **VM100 Setup Guide**: `/tmp/VM100-SETUP-GUIDE.md`
- **LM Studio Config**: `C:\GOKU-AI\knowledge-base\shenron-syndicate.md`
- **Web Interface Source**: `/tmp/shenron-syndicate-web/`
- **Deployment Scripts**: `/tmp/DEPLOY-SHENRON-*.sh`
- **PowerShell Helpers**: `C:\GOKU-AI\scripts\`

---

## 📞 SUPPORT

**Issues?** Check:
1. Browser console (F12) for JavaScript errors
2. Apache logs: `/var/log/apache2/shenron-error.log` (VM150)
3. LM Studio logs: Check LM Studio console (VM100)
4. Cloudflare Tunnel logs: `journalctl -u cloudflared` (VM120)

**Contact**: Built by Seth (Marine Corps veteran, infrastructure owner)

---

**THE SHENRON SYNDICATE IS OPERATIONAL! 🐉⚡**




