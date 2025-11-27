<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔍 VM101 Verification Commands

**Purpose:** Commands to verify and correct the flagged items in VM101-MIGRATION-SUMMARY.md  
**Run these via SSH on VM101**

---

## 1️⃣ Verify Secondary IP Address (<EDGEROUTER_IP>81)

### **Check Current Network Configuration**
```bash
# View all IP addresses
ip -4 addr show

# Check network configuration files
cat /etc/netplan/*.yaml
# or
cat /etc/network/interfaces

# Check if secondary IP is intentional
ip route show
```

### **Check Network Interface Details**
```bash
# Detailed interface info
ip addr show enp6s18

# Check for DHCP leases
cat /var/lib/dhcp/dhclient.leases | grep -A 10 "<EDGEROUTER_IP>81"

# Check systemd network configuration
networkctl status enp6s18
```

### **If Secondary IP Should Be Removed**
```bash
# Check what's using it
sudo ip addr del <EDGEROUTER_IP>81/24 dev enp6s18

# Or remove from netplan config
sudo nano /etc/netplan/*.yaml
# Remove the secondary IP, then:
sudo netplan apply
```

---

## 2️⃣ Check code-server Service Status

### **Check Service Status**
```bash
# Check user services
systemctl --user list-units --type=service --state=running | grep code-server

# Check if code-server process is running
ps aux | grep code-server | grep -v grep

# Check code-server status directly
systemctl --user status code-server@mgmt1

# Check if service is enabled
systemctl --user is-enabled code-server@mgmt1
```

### **Check code-server Configuration**
```bash
# Check config file
cat ~/.config/code-server/config.yaml

# Check if port 8080 is listening
sudo ss -tulnp | grep 8080

# Test if code-server is accessible
curl -I http://localhost:8080 2>/dev/null || echo "code-server not responding"
```

### **Start code-server if Not Running**
```bash
# Start the service
systemctl --user start code-server@mgmt1

# Enable auto-start
systemctl --user enable code-server@mgmt1

# Check status again
systemctl --user status code-server@mgmt1
```

### **Check code-server Logs**
```bash
# View service logs
journalctl --user -u code-server@mgmt1 -n 50

# Or check if running manually
code-server --version
```

---

## 3️⃣ Check Docker Containers

### **Check Docker Service**
```bash
# Check Docker service status
sudo systemctl status docker

# Check if Docker is running
docker ps

# Check Docker info
docker info | head -20
```

### **List All Containers**
```bash
# Running containers
docker ps

# All containers (including stopped)
docker ps -a

# Container sizes
docker ps -s
```

### **Check Docker Images**
```bash
# List images
docker images

# Check image sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

### **Check Docker Networks**
```bash
# List networks
docker network ls

# Inspect default network
docker network inspect bridge
```

### **Check Docker Compose Files**
```bash
# Find docker-compose files
find ~/GitHub -name "docker-compose.yml" -o -name "docker-compose.yaml" 2>/dev/null

# Check if any are in use
for file in $(find ~/GitHub -name "docker-compose.yml" -o -name "docker-compose.yaml" 2>/dev/null); do
  echo "=== $file ==="
  head -10 "$file"
done
```

---

## 4️⃣ Additional Verification Commands

### **Check Management Scripts**
```bash
# List management scripts
ls -la ~/management-scripts/ 2>/dev/null

# Check if scripts exist and are executable
find ~/management-scripts -name "*.sh" -type f 2>/dev/null
```

### **Verify SSH Access to Other VMs**
```bash
# Test SSH to each VM
echo "Testing SSH access to VMs..."
for vm in "proxy1@<VM120_IP>:VM120" "wp1@<VM150_IP>:VM150" "dbs1@<VM160_IP>:VM160" "gsh1@<VM170_IP>:VM170" "apis1@<VM180_IP>:VM180"; do
  IFS=':' read -r userhost name <<< "$vm"
  IFS='@' read -r user host <<< "$userhost"
  echo -n "Testing $name ($user@$host)... "
  timeout 3 ssh -o ConnectTimeout=2 -o BatchMode=yes "$userhost" "hostname" 2>/dev/null && echo "✅ OK" || echo "❌ FAILED"
done
```

### **Check Cron Jobs**
```bash
# User cron jobs
crontab -l 2>/dev/null || echo "No user cron jobs"

# Root cron jobs
sudo crontab -l 2>/dev/null || echo "No root cron jobs"

# System cron directories
ls -la /etc/cron.d/ 2>/dev/null
ls -la /etc/cron.daily/ 2>/dev/null
ls -la /etc/cron.weekly/ 2>/dev/null
ls -la /etc/cron.monthly/ 2>/dev/null
```

### **Check System Resources**
```bash
# Memory usage
free -h

# CPU info
lscpu | grep -E "Model name|CPU\(s\)|Thread|Core"

# Disk usage details
df -h
du -sh ~/* 2>/dev/null | sort -h | tail -10
```

### **Check Listening Ports**
```bash
# All listening ports
sudo ss -tulnp | grep LISTEN

# Specific ports
sudo ss -tulnp | grep -E ":22|:8080|:8000|:8001"
```

### **Check System Services**
```bash
# All running services
systemctl list-units --type=service --state=running | head -20

# Failed services
systemctl --failed

# User services
systemctl --user list-units --type=service
```

### **Verify Git Repository Status**
```bash
# Check Dell-Server-Roadmap repo status
cd ~/GitHub/Dell-Server-Roadmap && git status
git remote -v
git branch --show-current

# Check if repo is up to date
git fetch --dry-run
```

### **Check Python Environment**
```bash
# Activate and check venv
source ~/ai-workspace/ai-env/bin/activate
python --version
pip list | head -20
deactivate
```

### **Check Firewall Rules in Detail**
```bash
# UFW status with numbers
sudo ufw status numbered

# Check iptables (if UFW is using it)
sudo iptables -L -n -v | head -30
```

---

## 🎯 One-Liner Comprehensive Check

**Run this to check everything at once:**

```bash
echo "=== VM101 COMPREHENSIVE CHECK ===" && \
echo "" && \
echo "1. Network:" && \
ip -4 addr show | grep "inet " && \
echo "" && \
echo "2. code-server:" && \
(systemctl --user status code-server@mgmt1 --no-pager -l 2>/dev/null | head -5 || echo "Service not found") && \
(ps aux | grep -E "code-server" | grep -v grep || echo "Process not running") && \
echo "" && \
echo "3. Docker:" && \
(systemctl is-active docker 2>/dev/null && echo "✅ Docker active" || echo "❌ Docker inactive") && \
(docker ps -a --format "table {{.Names}}\t{{.Status}}" 2>/dev/null | head -10 || echo "No containers") && \
echo "" && \
echo "4. SSH Keys:" && \
ls ~/.ssh/*.pub 2>/dev/null | wc -l && \
echo "keys found" && \
echo "" && \
echo "5. Git Repos:" && \
ls -d ~/GitHub/*/ 2>/dev/null | wc -l && \
echo "repositories" && \
echo "" && \
echo "6. Disk:" && \
df -h / | tail -1 && \
echo "" && \
echo "7. Services:" && \
systemctl list-units --type=service --state=running --no-pager | grep -E "docker|code" | head -5
```

---

## 📋 Quick Fix Commands

### **If code-server Not Running:**
```bash
# Start code-server
systemctl --user start code-server@mgmt1
systemctl --user enable code-server@mgmt1
systemctl --user status code-server@mgmt1
```

### **If Docker Not Running:**
```bash
# Start Docker
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl status docker
```

### **If Secondary IP Should Be Removed:**
```bash
# Remove secondary IP
sudo ip addr del <EDGEROUTER_IP>81/24 dev enp6s18

# Verify it's gone
ip -4 addr show enp6s18
```

### **If SSH Access Fails to Other VMs:**
```bash
# Test connection
ssh -v proxy1@<VM120_IP> "hostname"

# Check SSH config
cat ~/.ssh/config 2>/dev/null || echo "No SSH config"

# Display public key for manual addition
cat ~/.ssh/id_ed25519.pub
```

---

## 📤 Save All Output

**To save all verification output to a file:**

```bash
{
  echo "=== VM101 VERIFICATION REPORT ==="
  echo "Date: $(date)"
  echo ""
  echo "=== NETWORK ==="
  ip -4 addr show
  echo ""
  echo "=== CODE-SERVER ==="
  systemctl --user status code-server@mgmt1 --no-pager -l 2>&1
  ps aux | grep code-server | grep -v grep
  echo ""
  echo "=== DOCKER ==="
  systemctl status docker --no-pager -l 2>&1
  docker ps -a 2>&1
  docker images 2>&1
  echo ""
  echo "=== SERVICES ==="
  systemctl list-units --type=service --state=running --no-pager | head -20
  echo ""
  echo "=== CRON JOBS ==="
  crontab -l 2>&1
  echo ""
  echo "=== LISTENING PORTS ==="
  sudo ss -tulnp | grep LISTEN
} > ~/vm101-verification-$(date +%Y%m%d-%H%M%S).txt 2>&1

echo "Report saved to: ~/vm101-verification-*.txt"
```

---

**After running these commands, share the output and I'll update the VM101-MIGRATION-SUMMARY.md file with the verified information!**




