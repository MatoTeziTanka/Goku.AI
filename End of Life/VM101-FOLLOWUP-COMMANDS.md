<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔧 VM101 Follow-Up Commands

**Based on verification results, run these commands to investigate and fix issues**

---

## 1️⃣ Investigate Secondary IP (<EDGEROUTER_IP>81)

### **Check Why Secondary IP Exists**
```bash
# Check netplan configuration
sudo cat /etc/netplan/*.yaml

# Check DHCP leases
cat /var/lib/dhcp/dhclient.leases | grep -A 5 "<EDGEROUTER_IP>81"

# Check network manager (if using)
nmcli connection show

# Check systemd-networkd
networkctl status enp6s18
```

### **Check What's Using the Secondary IP**
```bash
# Check routing table
ip route show

# Check if any services are bound to specific IP
sudo ss -tulnp | grep <EDGEROUTER_IP>81

# Check ARP table
arp -a | grep <EDGEROUTER_IP>81
```

### **Remove Secondary IP (if not needed)**
```bash
# Remove the secondary IP
sudo ip addr del <EDGEROUTER_IP>81/24 dev enp6s18

# Verify it's removed
ip -4 addr show enp6s18

# Make permanent (if in netplan)
sudo nano /etc/netplan/*.yaml
# Remove the secondary IP configuration, then:
sudo netplan apply
```

---

## 2️⃣ Fix code-server Service

### **Identify What's Running on Port 8080**
```bash
# Check what process is using port 8080
sudo lsof -i :8080
ps aux | grep 430042

# Check if it's actually code-server
sudo netstat -tulnp | grep 8080
curl -I http://localhost:8080
```

### **Set Up code-server as Systemd Service**
```bash
# Check if code-server binary exists
which code-server
code-server --version

# Create systemd user service
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

# Reload systemd
systemctl --user daemon-reload

# Stop manual process first (if it's code-server)
kill 430042 2>/dev/null

# Start service
systemctl --user start code-server.service
systemctl --user enable code-server.service

# Check status
systemctl --user status code-server.service
```

### **Or Keep Manual Process (if preferred)**
```bash
# Just document that it's running manually
# Check startup script or cron job
grep -r "code-server\|8080" ~/.bashrc ~/.profile ~/.bash_profile 2>/dev/null
crontab -l | grep -i code
```

---

## 3️⃣ Start Docker Service

### **Start and Enable Docker**
```bash
# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Check status
sudo systemctl status docker

# Verify Docker is working
docker ps
docker info | head -10
```

### **Check Why Docker Wasn't Running**
```bash
# Check Docker service logs
sudo journalctl -u docker -n 50

# Check if Docker socket exists
ls -la /var/run/docker.sock

# Check Docker group membership
groups | grep docker
# If not in docker group:
sudo usermod -aG docker $USER
# Then log out and back in
```

---

## 4️⃣ Identify Service on Port 8001

### **Find What's Running on Port 8001**
```bash
# Check process details
ps aux | grep 1681540
sudo lsof -i :8001
sudo ss -tulnp | grep 8001

# Check what the process is doing
sudo netstat -tulnp | grep 8001
curl -I http://localhost:8001 2>/dev/null

# Check process tree
pstree -p 1681540

# Check process working directory
sudo ls -la /proc/1681540/cwd
sudo cat /proc/1681540/cmdline | tr '\0' ' '
```

### **Check if It's a Known Service**
```bash
# Check if it's a Python web server
curl http://localhost:8001 2>/dev/null | head -20

# Check systemd services
systemctl list-units --type=service --state=running | grep -i python

# Check user services
systemctl --user list-units --type=service | grep -i python
```

---

## 5️⃣ Complete System Check

### **Run Full Verification**
```bash
{
  echo "=== VM101 COMPLETE VERIFICATION ==="
  echo "Date: $(date)"
  echo ""
  
  echo "=== NETWORK ==="
  ip -4 addr show
  echo ""
  sudo cat /etc/netplan/*.yaml 2>/dev/null
  echo ""
  
  echo "=== CODE-SERVER (Port 8080) ==="
  sudo lsof -i :8080
  ps aux | grep 430042 | grep -v grep
  echo ""
  
  echo "=== UNKNOWN SERVICE (Port 8001) ==="
  sudo lsof -i :8001
  ps aux | grep 1681540 | grep -v grep
  sudo cat /proc/1681540/cmdline 2>/dev/null | tr '\0' ' '
  echo ""
  
  echo "=== DOCKER ==="
  sudo systemctl status docker --no-pager -l 2>&1
  docker ps -a 2>&1
  echo ""
  
  echo "=== ALL LISTENING PORTS ==="
  sudo ss -tulnp | grep LISTEN
  echo ""
  
  echo "=== RUNNING SERVICES ==="
  systemctl list-units --type=service --state=running --no-pager | head -15
  echo ""
  
  echo "=== USER SERVICES ==="
  systemctl --user list-units --type=service --state=running --no-pager
  echo ""
  
  echo "=== CRON JOBS ==="
  crontab -l 2>&1
  echo ""
  
  echo "=== PROCESSES ON PORTS 8080, 8000, 8001 ==="
  for port in 8080 8000 8001; do
    echo "Port $port:"
    sudo lsof -i :$port 2>/dev/null || echo "  No process found"
  done
  
} > ~/vm101-complete-check-$(date +%Y%m%d-%H%M%S).txt 2>&1

echo "Complete check saved. View with:"
echo "cat ~/vm101-complete-check-*.txt"
```

---

## 🎯 Quick Fix Commands

### **Fix All Issues at Once**
```bash
# 1. Start Docker
sudo systemctl start docker && sudo systemctl enable docker && echo "✅ Docker started"

# 2. Identify port 8001 service
echo "Port 8001 process:" && sudo lsof -i :8001

# 3. Check code-server on 8080
echo "Port 8080 process:" && sudo lsof -i :8080

# 4. Check secondary IP
echo "Secondary IP source:" && cat /etc/netplan/*.yaml | grep -A 5 "<EDGEROUTER_IP>81" || echo "Not in netplan (likely DHCP)"
```

---

## 📋 Summary of Actions Needed

1. **✅ Docker:** Start service (`sudo systemctl start docker && sudo systemctl enable docker`)
2. **⚠️ code-server:** Either set up as systemd service or document manual startup
3. **⚠️ Port 8001:** Identify what service is running
4. **⚠️ Secondary IP:** Verify if <EDGEROUTER_IP>81 is needed (likely DHCP, can be removed if not needed)

---

**Run the complete verification command above and share the output for final documentation update!**




