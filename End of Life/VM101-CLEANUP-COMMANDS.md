<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🧹 VM101 Cleanup & Configuration Commands

**Purpose:** Handle secondary IP and port 8080 configuration  
**Run these on VM101 via SSH**

---

## 1️⃣ Test SSH Access to All VMs

### **Quick Test (One-liner)**
```bash
# Test SSH to all VMs
for vm in "Administrator@<VM100_IP>:VM100" "proxy1@<VM120_IP>:VM120" "wp1@<VM150_IP>:VM150" "dbs1@<VM160_IP>:VM160" "gsh1@<VM170_IP>:VM170" "apis1@<VM180_IP>:VM180" "Administrator@<VM200_IP>:VM200"; do
  IFS=':' read -r userhost name <<< "$vm"
  IFS='@' read -r user host <<< "$userhost"
  echo -n "Testing $name ($user@$host)... "
  timeout 5 ssh -o ConnectTimeout=3 -o BatchMode=yes $userhost "hostname" 2>/dev/null && echo "✅ OK" || echo "❌ FAILED"
done
```

### **Detailed Test Script**
```bash
# Upload and run the test script
# Or run commands individually:

# VM100
ssh -o ConnectTimeout=3 Administrator@<VM100_IP> "hostname" && echo "✅ VM100 OK" || echo "❌ VM100 FAILED"

# VM120
ssh -o ConnectTimeout=3 proxy1@<VM120_IP> "hostname" && echo "✅ VM120 OK" || echo "❌ VM120 FAILED"

# VM150
ssh -o ConnectTimeout=3 wp1@<VM150_IP> "hostname" && echo "✅ VM150 OK" || echo "❌ VM150 FAILED"

# VM160
ssh -o ConnectTimeout=3 dbs1@<VM160_IP> "hostname" && echo "✅ VM160 OK" || echo "❌ VM160 FAILED"

# VM170
ssh -o ConnectTimeout=3 gsh1@<VM170_IP> "hostname" && echo "✅ VM170 OK" || echo "❌ VM170 FAILED"

# VM180
ssh -o ConnectTimeout=3 apis1@<VM180_IP> "hostname" && echo "✅ VM180 OK" || echo "❌ VM180 FAILED"

# VM200
ssh -o ConnectTimeout=3 Administrator@<VM200_IP> "hostname" && echo "✅ VM200 OK" || echo "❌ VM200 FAILED"
```

### **Save Results**
```bash
{
  echo "=== SSH Access Test Results ==="
  echo "Date: $(date)"
  echo ""
  for vm in "Administrator@<VM100_IP>:VM100" "proxy1@<VM120_IP>:VM120" "wp1@<VM150_IP>:VM150" "dbs1@<VM160_IP>:VM160" "gsh1@<VM170_IP>:VM170" "apis1@<VM180_IP>:VM180" "Administrator@<VM200_IP>:VM200"; do
    IFS=':' read -r userhost name <<< "$vm"
    IFS='@' read -r user host <<< "$userhost"
    echo -n "$name ($user@$host): "
    timeout 5 ssh -o ConnectTimeout=3 -o BatchMode=yes $userhost "hostname" 2>/dev/null && echo "✅ OK" || echo "❌ FAILED"
  done
} > ~/vm101-ssh-test-results.txt

cat ~/vm101-ssh-test-results.txt
```

---

## 2️⃣ Handle Secondary IP (<EDGEROUTER_IP>81)

### **Option A: Remove Secondary IP (Recommended if not needed)**

```bash
# Check current IPs
ip -4 addr show enp6s18

# Remove secondary IP
sudo ip addr del <EDGEROUTER_IP>81/24 dev enp6s18

# Verify it's removed
ip -4 addr show enp6s18

# Make permanent (disable DHCP in cloud-init)
sudo nano /etc/netplan/50-cloud-init.yaml
# Change: dhcp4: true
# To:     dhcp4: false
# Then apply:
sudo netplan apply
```

### **Option B: Keep Secondary IP (If it's needed)**

```bash
# Just document it - no action needed
# The secondary IP is harmless and auto-renews
echo "Secondary IP <EDGEROUTER_IP>81 is from cloud-init DHCP and is harmless"
```

### **Check What's Using Secondary IP**
```bash
# Check if any services are bound to it
sudo ss -tulnp | grep <EDGEROUTER_IP>81

# Check routing
ip route show | grep <EDGEROUTER_IP>81
```

---

## 3️⃣ Handle Port 8080 (Python HTTP Server)

### **Option A: Stop HTTP Server and Use code-server on 8080**

```bash
# Find the HTTP server process
ps aux | grep "http.server 8080" | grep -v grep

# Stop it (PID 430042)
kill 430042

# Verify it's stopped
sudo ss -tulnp | grep 8080

# Start code-server on 8080
code-server --bind-addr 0.0.0.0:8080

# Or set up as systemd service
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/code-server.service << 'EOF'
[Unit]
Description=code-server
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/code-server --bind-addr 0.0.0.0:8080
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user start code-server.service
systemctl --user enable code-server.service
```

### **Option B: Keep HTTP Server, Use code-server on 8081**

```bash
# Keep HTTP server running on 8080
# Use code-server on 8081 (already tested and working)

# Set up code-server on 8081 as systemd service
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/code-server.service << 'EOF'
[Unit]
Description=code-server
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/code-server --bind-addr 0.0.0.0:8081
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user start code-server.service
systemctl --user enable code-server.service

# Verify
systemctl --user status code-server.service
sudo ss -tulnp | grep 8081
```

### **Option C: Document HTTP Server Purpose**

```bash
# If HTTP server is intentional, just document it
# Check what directory it's serving
ps aux | grep 430042
# Check process working directory
sudo ls -la /proc/430042/cwd
```

---

## 🎯 All-in-One Cleanup Script

```bash
#!/bin/bash
# VM101 Complete Cleanup and Configuration

echo "=== VM101 Cleanup & Configuration ==="
echo ""

# 1. Test SSH access
echo "1. Testing SSH access..."
./VM101-SSH-TEST-COMMANDS.sh  # Or run inline commands

# 2. Handle secondary IP (Option: Remove)
echo ""
echo "2. Handling secondary IP..."
read -p "Remove secondary IP <EDGEROUTER_IP>81? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo ip addr del <EDGEROUTER_IP>81/24 dev enp6s18
    echo "✅ Secondary IP removed"
    echo "⚠️  To make permanent, edit /etc/netplan/50-cloud-init.yaml and set dhcp4: false"
else
    echo "ℹ️  Keeping secondary IP (harmless)"
fi

# 3. Handle port 8080 (Option: Stop HTTP server, use code-server)
echo ""
echo "3. Handling port 8080..."
read -p "Stop HTTP server and use code-server on 8080? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    kill 430042 2>/dev/null
    echo "✅ HTTP server stopped"
    echo "⚠️  Start code-server manually or set up systemd service"
else
    echo "ℹ️  Keeping HTTP server on 8080, use code-server on 8081"
fi

echo ""
echo "=== Cleanup Complete ==="
```

---

## 📋 Quick Commands Summary

**Test SSH:**
```bash
for vm in "Administrator@<VM100_IP>" "proxy1@<VM120_IP>" "wp1@<VM150_IP>" "dbs1@<VM160_IP>" "gsh1@<VM170_IP>" "apis1@<VM180_IP>" "Administrator@<VM200_IP>"; do
  timeout 5 ssh -o ConnectTimeout=3 -o BatchMode=yes $vm "hostname" 2>/dev/null && echo "$vm ✅" || echo "$vm ❌"
done
```

**Remove Secondary IP:**
```bash
sudo ip addr del <EDGEROUTER_IP>81/24 dev enp6s18 && ip -4 addr show enp6s18
```

**Stop HTTP Server:**
```bash
kill 430042 && sudo ss -tulnp | grep 8080
```

---

**Run the SSH test first, then decide on secondary IP and port 8080 based on your needs!**




