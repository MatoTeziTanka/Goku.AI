<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔌 VM101 Code-Server Port Selection Guide

**Issue:** Reverse proxy (VM120) may handle ports 80, 443, 8080, 8443  
**Goal:** Find a safe port NOT handled by reverse proxy for code-server

---

## 🔍 Step 1: Check Reverse Proxy Configuration

### **On VM120 (Reverse Proxy):**

**✅ VERIFIED: Nginx is listening on:**
- Port 80 (HTTP) - IPv4 and IPv6
- Port 443 (HTTPS) - IPv4 only

**Check for Apache and other ports:**
```bash
# SSH to VM120
ssh proxy1@<VM120_IP>

# Check if Apache is installed/running
dpkg -l | grep apache
sudo systemctl status apache2
sudo ss -tlnp | grep apache

# Check all listening ports
sudo ss -tlnp | grep -E ":(80|443|8080|8443|8000|8001|9000|9001|10000)"

# Check Nginx config for any other ports
sudo grep -r "listen" /etc/nginx/ | grep -v "#"

# Check Apache config (if Apache is installed)
sudo grep -r "Listen\|<VirtualHost" /etc/apache2/ 2>/dev/null | grep -v "#"
```

**See:** `VM120-REVERSE-PROXY-PORT-CHECK.md` for detailed results

### **On VM101 (Current System):**

**Check what ports are in use:**
```bash
# Check listening ports
sudo ss -tlnp | grep LISTEN

# Check firewall rules
sudo ufw status verbose

# Check what's using specific ports
sudo lsof -i :8080
sudo lsof -i :8443
sudo lsof -i :8001
```

---

## 🎯 Step 2: Port Selection Strategy

### **Ports to AVOID (Common/Reverse Proxy):**
- ❌ **80** - HTTP (standard)
- ❌ **443** - HTTPS (standard)
- ❌ **8080** - Common alternative HTTP
- ❌ **8443** - Common alternative HTTPS
- ❌ **3000** - Common dev server
- ❌ **5000** - Common Flask default
- ❌ **8000** - Common alternative

### **Safe Port Ranges (Less Scanned):**

**High Range Ports (Recommended):**
- ✅ **9001-9010** - High range, less common
- ✅ **8444-8450** - Alternative HTTPS-like
- ✅ **10000-10010** - Very high range
- ✅ **20000-20010** - Very high range

**Specific Recommendations:**
- ✅ **9001** - Simple, high range
- ✅ **9002** - Alternative
- ✅ **8444** - If 8443 is taken
- ✅ **10000** - Very high, unlikely conflict
- ✅ **20000** - Very high, unlikely conflict

---

## 🛠️ Step 3: Verify Port Availability

### **On VM101:**

**Test if port is available:**
```bash
# Test port 9001
sudo ss -tlnp | grep :9001
# If empty, port is available

# Test port 10000
sudo ss -tlnp | grep :10000
# If empty, port is available
```

**Test if port is accessible from network:**
```bash
# Start temporary listener
nc -l 9001 &
# Test from another machine
# Then kill: killall nc
```

---

## 📋 Step 4: Recommended Ports (Priority Order)

### **Option 1: Port 9001 (Recommended)**
- ✅ High range (less scanned)
- ✅ Simple number
- ✅ Unlikely to conflict
- ✅ Not standard web port

**Setup:**
```bash
# Edit code-server config
nano ~/.config/code-server/config.yaml
# Set: bind-addr: 0.0.0.0:9001

# Update firewall
sudo ufw allow 9001/tcp comment "code-server"
```

### **Option 2: Port 10000 (Alternative)**
- ✅ Very high range
- ✅ Unlikely any service uses it
- ✅ Not in common port ranges

**Setup:**
```bash
# Edit code-server config
nano ~/.config/code-server/config.yaml
# Set: bind-addr: 0.0.0.0:10000

# Update firewall
sudo ufw allow 10000/tcp comment "code-server"
```

### **Option 3: Port 8444 (If 8443 is taken)**
- ✅ Similar to 8443 but different
- ✅ HTTPS-like port
- ✅ Less common than 8443

**Setup:**
```bash
# Edit code-server config
nano ~/.config/code-server/config.yaml
# Set: bind-addr: 0.0.0.0:8444

# Update firewall
sudo ufw allow 8444/tcp comment "code-server"
```

---

## 🔧 Step 5: Complete Setup Script

**Create `setup-code-server-safe-port.sh`:**
```bash
#!/bin/bash
# Setup code-server on a safe port (not handled by reverse proxy)

# Default to 9001, but can override
PORT=${1:-9001}

echo "🔌 Setting up code-server on port ${PORT}..."

# Check if port is in use
if sudo ss -tlnp | grep -q ":${PORT} "; then
    echo "❌ Port ${PORT} is already in use!"
    echo "   Try: ./setup-code-server-safe-port.sh 10000"
    exit 1
fi

# Create config directory
mkdir -p ~/.config/code-server

# Generate random password
PASSWORD=$(openssl rand -base64 12)

# Create config
cat > ~/.config/code-server/config.yaml << EOF
bind-addr: 0.0.0.0:${PORT}
auth: password
password: ${PASSWORD}
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

echo ""
echo "✅ Code-server configured on port ${PORT}"
echo "   Password: ${PASSWORD}"
echo "   Access: http://<VM101_IP>:${PORT}"
echo ""
echo "📋 Next steps:"
echo "   1. Test: curl http://<VM101_IP>:${PORT}"
echo "   2. Check status: sudo systemctl status code-server"
echo "   3. View logs: sudo journalctl -u code-server -f"
```

**Usage:**
```bash
chmod +x setup-code-server-safe-port.sh

# Use default port 9001
./setup-code-server-safe-port.sh

# Or specify custom port
./setup-code-server-safe-port.sh 10000
```

---

## 🔍 Verification Commands

**After setup, verify:**
```bash
# Check if code-server is running
sudo systemctl status code-server

# Check if port is listening
sudo ss -tlnp | grep :9001

# Test from localhost
curl http://localhost:9001

# Test from network
curl http://<VM101_IP>:9001
```

---

## 📋 Port Selection Checklist

- [ ] Check reverse proxy (VM120) for port usage
- [ ] Check VM101 for ports in use
- [ ] Select safe port (9001, 10000, or 8444)
- [ ] Verify port is not in use
- [ ] Configure code-server on selected port
- [ ] Update firewall rules
- [ ] Test access from network
- [ ] Document port in configuration

---

## 🎯 Recommended Action

**Before configuring code-server:**

1. **Check reverse proxy ports:**
   ```bash
   ssh proxy1@<VM120_IP> "sudo grep -r 'listen' /etc/nginx/ /etc/apache2/ 2>/dev/null | grep -E ':(80|443|8080|8443)'"
   ```

2. **Check VM101 ports:**
   ```bash
   sudo ss -tlnp | grep -E ":(80|443|8080|8443|9001|10000)"
   ```

3. **Select safe port:**
   - If reverse proxy uses 80, 443, 8080, 8443 → Use **9001** or **10000**
   - If port 9001 is free → Use **9001**
   - If port 10000 is free → Use **10000**

4. **Configure code-server:**
   ```bash
   ./setup-code-server-safe-port.sh 9001
   ```

---

**Select a port NOT in the reverse proxy configuration!** 🔐

