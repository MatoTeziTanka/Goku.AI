<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔄 VM101 ↔ VM100 Communication Architecture

**Created:** November 23, 2025  
**Purpose:** Clarify how VM100 (LM Studio) and VM101 (Control Node) communicate  
**Status:** ✅ Architecture Document

---

## 🎯 KEY POINT: **HTTP/API Communication, NOT SSH**

**VM100 and VM101 communicate via HTTP/HTTPS APIs, NOT SSH.**

- **SSH** = Management/Deployment (one-way: VM101 → VM100)
- **HTTP/API** = Service Communication (bidirectional: VM101 ↔ VM100)

---

## 📡 COMMUNICATION FLOWS

### **1. API Communication (HTTP - Ports 1234 & 5000)**

**VM101 → VM100: HTTP Requests**
```
VM101 (Control Node)
    ↓ HTTP Request
    ↓ http://<VM100_IP>:1234/v1/chat/completions
    ↓ http://<VM100_IP>:5000/api/shenron/grant-wish
VM100 (LM Studio + SHENRON API)
    ↓ HTTP Response (automatic)
    ↓ JSON response with AI results
VM101 (Control Node)
```

**How it works:**
1. VM101 makes HTTP POST requests to VM100's APIs
2. VM100 processes the request (LM Studio generates response)
3. VM100 sends HTTP response back to VM101
4. **No SSH needed** - this is standard HTTP request/response

**Ports Used:**
- **Port 1234:** LM Studio API (`http://<VM100_IP>:1234/v1/`)
- **Port 5000:** SHENRON API (`http://<VM100_IP>:5000/api/`)

**Example Request (from VM101):**
```python
# VM101 makes HTTP request to VM100
import requests

response = requests.post(
    "http://<VM100_IP>:1234/v1/chat/completions",
    json={
        "model": "deepseek-coder-v2-lite-instruct",
        "messages": [{"role": "user", "content": "Hello"}]
    }
)
# VM100 responds automatically via HTTP (no SSH needed)
```

---

### **2. SSH Communication (Management Only - One-Way)**

**VM101 → VM100: SSH (Management)**
```
VM101 (Control Node)
    ↓ SSH Connection
    ↓ ssh Administrator@<VM100_IP>
VM100 (AI Host)
    ↓ SSH Session
    ↓ Execute commands, deploy code, manage services
VM101 (Control Node)
```

**Purpose:**
- Deploy code updates
- Manage services (start/stop/restart)
- View logs
- System administration

**One-Way Trust:**
- ✅ VM101 CAN SSH to VM100 (for management)
- ❌ VM100 CANNOT SSH to VM101 (security isolation)

**Why this is secure:**
- VM100 doesn't need to SSH to VM101
- VM100 just needs to accept incoming HTTP requests (which it does)
- If VM100 is compromised, attacker can't SSH to VM101

---

## 🔍 DETAILED COMMUNICATION PATTERNS

### **Pattern 1: SHENRON Orchestrator → LM Studio**

**Location:** `Dell-Server-Roadmap/backend/shenron/shenron_v4_orchestrator.py`

```python
# Configuration
LM_STUDIO_API = "http://<VM100_IP>:1234/v1"

# HTTP Request (not SSH!)
response = requests.post(
    f"{LM_STUDIO_API}/chat/completions",
    json={
        "model": "deepseek-coder-v2-lite-instruct",
        "messages": [...],
        "temperature": 0.7
    },
    timeout=120
)
```

**Flow:**
1. VM101's SHENRON orchestrator makes HTTP POST to `http://<VM100_IP>:1234/v1/chat/completions`
2. VM100's LM Studio receives HTTP request
3. LM Studio processes with AI model
4. VM100 sends HTTP response back to VM101
5. **No SSH involved!**

---

### **Pattern 2: Web UI → SHENRON API**

**Location:** `Dell-Server-Roadmap/web/shenron-ui/api.php`

```php
// Web UI (on VM120 or VM150) makes HTTP request
$backendBase = 'http://<VM100_IP>:5000';
$response = http_json_request('POST', "$backendBase/api/shenron/grant-wish", $payload);
```

**Flow:**
1. User submits query via web UI
2. Web UI makes HTTP POST to `http://<VM100_IP>:5000/api/shenron/grant-wish`
3. VM100's SHENRON API processes request
4. SHENRON API makes HTTP requests to LM Studio (port 1234)
5. VM100 sends HTTP response back to web UI
6. **No SSH involved!**

---

### **Pattern 3: VM101 Management → VM100 (SSH)**

**Purpose:** Code deployment, service management

```bash
# On VM101
scp -i ~/.ssh/vm-keys/vm100_key \
    shenron_v4_orchestrator.py \
    Administrator@<VM100_IP>:C:/GOKU-AI/shenron/

ssh -i ~/.ssh/vm-keys/vm100_key \
    Administrator@<VM100_IP> \
    "powershell -Command 'Restart-Service SHENRON'"
```

**Flow:**
1. VM101 initiates SSH connection to VM100
2. VM100 accepts SSH (one-way trust)
3. VM101 executes commands or transfers files
4. **This is for management, NOT API communication**

---

## 🔒 SECURITY MODEL

### **One-Way Trust (SSH)**

```
VM101 → VM100: ✅ ALLOWED (SSH for management)
VM100 → VM101: ❌ BLOCKED (Security isolation)
```

**Why this works:**
- VM100 doesn't need to SSH to VM101
- VM100 just needs to accept HTTP requests (which it does by default)
- If VM100 is compromised, attacker can't SSH to VM101

### **Bidirectional HTTP (API)**

```
VM101 → VM100: ✅ HTTP requests (port 1234, 5000)
VM100 → VM101: ✅ HTTP responses (automatic, part of HTTP)
```

**Why this works:**
- HTTP is request/response protocol
- VM100 responds to HTTP requests automatically
- No SSH needed for API communication
- Firewall allows HTTP traffic (ports 1234, 5000)

---

## 🌐 NETWORK FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                    VM101 (Control Node)                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  SHENRON Orchestrator                                │  │
│  │  - Makes HTTP requests to VM100                      │  │
│  │  - Receives HTTP responses from VM100               │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Management Scripts                                  │  │
│  │  - SSH to VM100 (one-way)                            │  │
│  │  - Deploy code, manage services                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                    │                    │
                    │                    │
        HTTP/API    │                    │    SSH
        (1234,5000) │                    │    (22)
                    │                    │
                    ↓                    ↓
┌─────────────────────────────────────────────────────────────┐
│                    VM100 (AI Host)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  LM Studio API (Port 1234)                           │  │
│  │  - Accepts HTTP requests                              │  │
│  │  - Returns HTTP responses                             │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  SHENRON API (Port 5000)                              │  │
│  │  - Accepts HTTP requests                              │  │
│  │  - Returns HTTP responses                             │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  SSH Server (Port 22)                                 │  │
│  │  - Accepts SSH from VM101 only                       │  │
│  │  - Rejects SSH from VM100 to VM101                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ VERIFICATION

### **Test HTTP API Communication (No SSH Needed):**

**From VM101:**
```bash
# Test LM Studio API (HTTP)
curl http://<VM100_IP>:1234/v1/models

# Test SHENRON API (HTTP)
curl http://<VM100_IP>:5000/health

# These work WITHOUT SSH!
```

**Expected Output:**
```json
# LM Studio response
{
  "data": [
    {
      "id": "deepseek-coder-v2-lite-instruct",
      "object": "model",
      ...
    }
  ]
}

# SHENRON API response
{
  "status": "healthy",
  "version": "4.0"
}
```

### **Test SSH (Management Only):**

**From VM101:**
```bash
# This works (VM101 → VM100)
ssh -i ~/.ssh/vm-keys/vm100_key Administrator@<VM100_IP> "hostname"
# Expected: GOKU-AI
```

**From VM100:**
```bash
# This should FAIL (VM100 → VM101)
ssh mgmt1@<VM101_IP> "hostname"
# Expected: Permission denied (publickey)
```

---

## 📋 SUMMARY

| Communication Type | Protocol | Direction | Purpose | SSH Needed? |
|-------------------|----------|-----------|---------|-------------|
| **API Calls** | HTTP | VM101 ↔ VM100 | LM Studio & SHENRON API | ❌ NO |
| **Management** | SSH | VM101 → VM100 | Code deployment, service management | ✅ YES (one-way) |
| **Responses** | HTTP | VM100 → VM101 | Automatic HTTP responses | ❌ NO |

**Key Points:**
1. ✅ **API communication uses HTTP** (ports 1234, 5000) - no SSH needed
2. ✅ **SSH is only for management** (one-way: VM101 → VM100)
3. ✅ **VM100 doesn't need SSH to VM101** - it just responds to HTTP requests
4. ✅ **One-way trust is correct** - VM100 can't SSH to VM101, but APIs still work

---

## 🔧 FIREWALL CONFIGURATION

**VM100 (Windows Firewall):**
- ✅ Allow inbound HTTP on port 1234 (LM Studio)
- ✅ Allow inbound HTTP on port 5000 (SHENRON API)
- ✅ Allow inbound SSH on port 22 (from VM101 only)
- ❌ Block outbound SSH to VM101 (one-way trust)

**VM101 (UFW):**
- ✅ Allow outbound HTTP to VM100 (ports 1234, 5000)
- ✅ Allow outbound SSH to VM100 (port 22)
- ✅ Block inbound SSH from VM100 (one-way trust)

---

**Last Updated:** November 23, 2025  
**Status:** ✅ Architecture Documented




