# 🔌 VM101 Port Configuration Guide

**Requirement:** Avoid common ports (like 8080) for security

---

## 📋 Current Port Usage

**Verified Ports:**
- **Port 22:** SSH (standard, required)
- **Port 8001:** Multi-Agent System Backend (FastAPI/Uvicorn)
- **Port 8080:** ⚠️ Currently empty (was Python HTTP server, now stopped)
- **Port 8000:** Allowed in firewall (not in use)

---

## 🎯 Recommended Port Allocation

### **Non-Standard Ports for Services:**

**Code-Server (VS Code in Browser):**
- **Current:** Not running as service
- **Recommended Port:** `8443` (HTTPS-like, non-standard)
- **Alternative Ports:** `8444`, `8445`, `9001`, `9002`
- **Why:** Avoids common ports (8080, 3000, 5000)

**Multi-Agent System Backend:**
- **Current:** Port 8001
- **Status:** ✅ Already non-standard (good)
- **Keep:** Port 8001 is fine

**Other Services:**
- **SSH:** Port 22 (standard, keep)
- **Docker:** Uses dynamic ports (no conflict)

---

## 🛠️ Code-Server Port Configuration

### **Option 1: Port 8443 (Recommended)**

**Edit code-server config:**
```bash
nano ~/.config/code-server/config.yaml
```

**Set:**
```yaml
bind-addr: 0.0.0.0:8443
auth: password
password: YOUR_SECURE_PASSWORD
cert: false
```

**Update firewall:**
```bash
sudo ufw allow 8443/tcp
sudo ufw reload
```

**Start code-server:**
```bash
code-server
# Or as service (see below)
```

### **Option 2: Port 8444 (Alternative)**

```yaml
bind-addr: 0.0.0.0:8444
```

### **Option 3: Port 9001 (Alternative)**

```yaml
bind-addr: 0.0.0.0:9001
```

---

## 🔧 Setup Code-Server as Systemd Service

**Create service file:**
```bash
sudo nano /etc/systemd/system/code-server.service
```

**Content:**
```ini
[Unit]
Description=Code Server (VS Code in Browser)
After=network.target

[Service]
Type=simple
User=mgmt1
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/code-server --bind-addr 0.0.0.0:8443 --auth password
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable code-server
sudo systemctl start code-server
sudo systemctl status code-server
```

**Update firewall:**
```bash
sudo ufw allow 8443/tcp
sudo ufw reload
```

---

## 🔍 Port Security Best Practices

### **1. Use Non-Standard Ports**

**Avoid:**
- ❌ 8080 (common web server)
- ❌ 3000 (common dev server)
- ❌ 5000 (common Flask default)
- ❌ 8000 (common alternative)

**Use:**
- ✅ 8443, 8444 (HTTPS-like, non-standard)
- ✅ 9001, 9002 (high range, less scanned)
- ✅ 8001+ (already using, good)

### **2. Firewall Rules**

**Only allow necessary ports:**
```bash
# Check current rules
sudo ufw status verbose

# Remove unnecessary rules
sudo ufw delete allow 8080/tcp  # If not needed
sudo ufw delete allow 8000/tcp   # If not needed

# Add specific port
sudo ufw allow 8443/tcp comment "code-server"
```

### **3. Port Scanning Protection**

**Use fail2ban (optional):**
```bash
sudo apt-get install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 📋 Port Allocation Summary

| Service | Current Port | Recommended Port | Status |
|---------|-------------|------------------|---------|
| SSH | 22 | 22 (keep) | ✅ Standard |
| Multi-Agent Backend | 8001 | 8001 (keep) | ✅ Non-standard |
| Code-Server | Not running | 8443 | ⚠️ Needs setup |
| Docker | Dynamic | Dynamic | ✅ No conflict |

---

## 🚀 Quick Setup Script

**Create `setup-code-server-port.sh`:**
```bash
#!/bin/bash
# Setup code-server on non-standard port 8443

PORT=8443

# Update config
mkdir -p ~/.config/code-server
cat > ~/.config/code-server/config.yaml << EOF
bind-addr: 0.0.0.0:${PORT}
auth: password
password: $(openssl rand -base64 12)
cert: false
EOF

# Update firewall
sudo ufw allow ${PORT}/tcp comment "code-server"

# Create systemd service
sudo tee /etc/systemd/system/code-server.service > /dev/null << EOF
[Unit]
Description=Code Server (VS Code in Browser)
After=network.target

[Service]
Type=simple
User=mgmt1
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/code-server --bind-addr 0.0.0.0:${PORT} --auth password
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable code-server
sudo systemctl start code-server

echo "✅ Code-server configured on port ${PORT}"
echo "Password: $(grep password ~/.config/code-server/config.yaml | awk '{print $2}')"
```

**Run:**
```bash
chmod +x setup-code-server-port.sh
./setup-code-server-port.sh
```

---

**Use port 8443 (or 8444, 9001) instead of 8080 for better security!** 🔐




