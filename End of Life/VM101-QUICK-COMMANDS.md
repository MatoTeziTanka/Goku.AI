<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🚀 VM101 Quick Information Gathering Commands

**Purpose:** Quick reference commands to gather VM101 information for migration summary  
**Usage:** Run these commands via SSH on VM101

---

## 📋 Quick Command Reference

### **1. OS Version & System Info**
```bash
lsb_release -a
cat /etc/os-release
hostnamectl
uname -a
```

### **2. Installed Packages**
```bash
dpkg -l | grep -E "python3|docker|code-server|git|curl|wget|vim|nano|build-essential|ufw|jq|openssh"
python3 --version
docker --version 2>/dev/null || echo "Docker not installed"
code-server --version 2>/dev/null || echo "code-server not installed"
```

### **3. Disk Usage**
```bash
df -h
du -sh ~/GitHub/* 2>/dev/null
du -sh ~/ai-workspace/* 2>/dev/null
du -sh ~
```

### **4. Python Environment**
```bash
python3 --version
ls -la ~/ai-workspace/ 2>/dev/null
ls -la ~/ai-workspace/ai-env/ 2>/dev/null
~/ai-workspace/ai-env/bin/python --version 2>/dev/null
~/ai-workspace/ai-env/bin/pip list 2>/dev/null
```

### **5. SSH Keys**
```bash
ls -la ~/.ssh/
cat ~/.ssh/id_ed25519.pub 2>/dev/null || cat ~/.ssh/id_rsa.pub 2>/dev/null
file ~/.ssh/id_* 2>/dev/null
```

### **6. Git Repositories**
```bash
ls -la ~/GitHub/ 2>/dev/null
cd ~/GitHub && for repo in */; do echo "=== $repo ==="; cd "$repo" && git remote get-url origin 2>/dev/null && git branch --show-current 2>/dev/null && cd ..; done
```

### **7. Docker**
```bash
docker --version 2>/dev/null || echo "Docker not installed"
docker ps -a 2>/dev/null
docker images 2>/dev/null
docker network ls 2>/dev/null
systemctl status docker 2>/dev/null
```

### **8. Network Configuration**
```bash
ip -4 addr show
ip route show
cat /etc/resolv.conf
sudo ss -tulnp | head -20
```

### **9. Firewall**
```bash
sudo ufw status verbose
sudo ufw status numbered
```

### **10. Services & Cron**
```bash
systemctl list-units --type=service --state=running | head -20
systemctl --user status code-server@$USER 2>/dev/null
crontab -l 2>/dev/null || echo "No user cron jobs"
sudo crontab -l 2>/dev/null || echo "No root cron jobs"
```

### **11. Management Scripts**
```bash
ls -la ~/management-scripts/ 2>/dev/null
find ~ -maxdepth 2 -name "*.sh" -type f 2>/dev/null
```

### **12. Additional Info**
```bash
free -h
lscpu | grep -E "Model name|CPU\(s\)|Thread|Core"
ls -la ~/
cat ~/.config/code-server/config.yaml 2>/dev/null || echo "code-server config not found"
```

---

## 🎯 Automated Script Method

**Option 1: Run the automated script (recommended)**

```bash
# On your local machine, upload the script
scp VM101-INFO-GATHERING-COMMANDS.sh mgmt1@<VM101_IP>:~/info-gather.sh

# SSH to VM101
ssh mgmt1@<VM101_IP>

# Make executable and run
chmod +x ~/info-gather.sh
~/info-gather.sh

# Download results
# (from local machine)
scp -r mgmt1@<VM101_IP>:~/vm101-info/ ./vm101-info/
```

**Option 2: Copy-paste commands manually**

Run each section above individually and save output.

---

## 📤 Output Collection

**To save all output to files:**

```bash
# Create output directory
mkdir -p ~/vm101-info

# Run commands and save output
{
  echo "=== OS VERSION ==="
  lsb_release -a
  cat /etc/os-release
  echo ""
  echo "=== PACKAGES ==="
  dpkg -l | grep -E "python3|docker|code-server|git"
  echo ""
  echo "=== DISK USAGE ==="
  df -h
  du -sh ~/GitHub/* 2>/dev/null
  echo ""
  echo "=== SSH KEYS ==="
  ls -la ~/.ssh/
  echo ""
  echo "=== GIT REPOS ==="
  ls -la ~/GitHub/ 2>/dev/null
  echo ""
  echo "=== NETWORK ==="
  ip -4 addr show
  echo ""
  echo "=== FIREWALL ==="
  sudo ufw status verbose
} > ~/vm101-info/quick-info.txt 2>&1

# View results
cat ~/vm101-info/quick-info.txt
```

---

## 🔍 One-Liner Comprehensive Check

**Quick comprehensive check (all in one):**

```bash
echo "=== VM101 SYSTEM INFO ===" && \
echo "OS:" && lsb_release -d && \
echo "Packages:" && dpkg -l | grep -c "^ii" && \
echo "Disk:" && df -h / | tail -1 && \
echo "Python:" && python3 --version && \
echo "Docker:" && docker --version 2>/dev/null || echo "Not installed" && \
echo "Git Repos:" && ls -d ~/GitHub/*/ 2>/dev/null | wc -l && \
echo "SSH Keys:" && ls ~/.ssh/*.pub 2>/dev/null | wc -l && \
echo "Network:" && ip -4 addr show | grep "inet " | grep -v "127.0.0.1"
```

---

## 📝 What to Look For

After running commands, check for:

1. **OS Version:** Should be Ubuntu 22.04 or 24.04 LTS
2. **Python:** Should be 3.10+ or 3.11+
3. **Git Repos:** Check if Dell-Server-Roadmap is cloned
4. **SSH Keys:** Should have id_ed25519 or id_rsa
5. **Disk Space:** Check if ~/GitHub has space
6. **Services:** Check if code-server, docker are running
7. **Network:** Verify IP is <VM101_IP>
8. **Firewall:** Check UFW rules

---

## 🚨 Common Issues

**If commands fail:**
- Use `sudo` for system commands
- Some commands may need `2>/dev/null` to suppress errors
- Check if directories exist before listing

**If SSH keys missing:**
- Generate new key: `ssh-keygen -t ed25519 -C "vm101-mgmt1" -f ~/.ssh/id_ed25519 -N ""`

**If Git repos missing:**
- Clone them: `cd ~/GitHub && git clone https://github.com/MatoTeziTanka/Dell-Server-Roadmap.git`




