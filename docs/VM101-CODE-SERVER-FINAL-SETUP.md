<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# ✅ VM101 Code-Server Final Setup Guide

**Status:** Port verification complete - Ready to setup  
**Recommended Port:** 9001  
**Date:** November 23, 2025

---

## ✅ Port Verification Results

### **VM120 (Reverse Proxy) - VERIFIED:**
- ✅ **Port 80:** Nginx HTTP (in use)
- ✅ **Port 443:** Nginx HTTPS (in use)
- ✅ **Apache:** NOT installed
- ✅ **Port 8080:** FREE
- ✅ **Port 8443:** FREE
- ✅ **Port 9001:** FREE ⭐ **RECOMMENDED**
- ✅ **Port 10000:** FREE (alternative)

### **VM101 (Control Node) - Current:**
- ✅ **Port 22:** SSH (in use)
- ✅ **Port 8001:** Multi-Agent System Backend (in use)
- ✅ **Port 9001:** FREE ⭐ **SAFE TO USE**

---

## 🚀 Quick Setup (Recommended)

### **Option 1: Automated Script (Easiest)**

**On VM101:**
```bash
# Make script executable
chmod +x VM101-CODE-SERVER-SETUP-9001.sh

# Run setup
./VM101-CODE-SERVER-SETUP-9001.sh
```

**The script will:**
- ✅ Check if port 9001 is available
- ✅ Create code-server config with password auth
- ✅ Add firewall rule for port 9001
- ✅ Create systemd service
- ✅ Start code-server automatically
- ✅ Display password and access URL

---

## 🛠️ Manual Setup (Alternative)

### **Step 1: Create Configuration**

```bash
# Create config directory
mkdir -p ~/.config/code-server

# Generate random password
PASSWORD=$(openssl rand -base64 12)

# Create config file
cat > ~/.config/code-server/config.yaml << EOF
bind-addr: 0.0.0.0:9001
auth: password
password: ${PASSWORD}
cert: false
EOF

echo "Password: ${PASSWORD}"
```

### **Step 2: Update Firewall**

```bash
sudo ufw allow 9001/tcp comment "code-server"
sudo ufw reload
```

### **Step 3: Create Systemd Service**

```bash
sudo tee /etc/systemd/system/code-server.service > /dev/null << EOF
[Unit]
Description=Code Server (VS Code in Browser)
After=network.target

[Service]
Type=simple
User=mgmt1
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/code-server --bind-addr 0.0.0.0:9001 --auth password
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

### **Step 4: Enable and Start**

```bash
sudo systemctl daemon-reload
sudo systemctl enable code-server
sudo systemctl start code-server
sudo systemctl status code-server
```

---

## 🔍 Verification

### **Check Service Status**

```bash
# Check if service is running
sudo systemctl status code-server

# Check if port is listening
sudo ss -tlnp | grep :9001

# Check logs
sudo journalctl -u code-server -f
```

### **Test Access**

```bash
# Test from localhost
curl http://localhost:9001

# Test from network
curl http://<VM101_IP>:9001
```

### **Access in Browser**

```
http://<VM101_IP>:9001
```

**Login with the password shown during setup.**

---

## 📋 Configuration Details

### **Config File Location:**
```
~/.config/code-server/config.yaml
```

### **Service File Location:**
```
/etc/systemd/system/code-server.service
```

### **Logs Location:**
```
sudo journalctl -u code-server
```

---

## 🔧 Management Commands

### **Start/Stop/Restart**

```bash
# Start
sudo systemctl start code-server

# Stop
sudo systemctl stop code-server

# Restart
sudo systemctl restart code-server

# Status
sudo systemctl status code-server
```

### **View Logs**

```bash
# Follow logs
sudo journalctl -u code-server -f

# Last 50 lines
sudo journalctl -u code-server -n 50

# Since boot
sudo journalctl -u code-server -b
```

### **Change Password**

```bash
# Edit config
nano ~/.config/code-server/config.yaml

# Change password line, then restart
sudo systemctl restart code-server
```

---

## 🔐 Security Notes

- ✅ **Password authentication enabled** (secure)
- ✅ **Firewall rule added** (port 9001 allowed)
- ✅ **Service auto-starts on boot** (persistent)
- ✅ **Port 9001 is safe** (not used by reverse proxy)
- ⚠️ **Consider:** Adding IP restrictions if needed
- ⚠️ **Consider:** Using HTTPS with reverse proxy (future)

---

## 🎯 Summary

**Port Selection:** ✅ **9001** (verified safe)  
**Setup Method:** Automated script or manual  
**Access:** `http://<VM101_IP>:9001`  
**Authentication:** Password (generated during setup)

**Ready to setup!** 🚀




