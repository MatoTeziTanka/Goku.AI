# 🔧 VM101 Docker Rootless Troubleshooting

**Issue:** Docker rootless service failed to start  
**Status:** Setup completed but service won't start

---

## 🔍 Step 1: Check Error Logs

```bash
# Check Docker service status
systemctl --user status docker.service

# Check detailed error logs
journalctl --user -xeu docker.service -n 50

# Or shorter version
journalctl --user -n 20 --no-pager --unit docker.service
```

---

## 🔧 Common Fixes

### **Fix 1: Check System Requirements**

```bash
# Verify uidmap is properly installed
dpkg -l | grep uidmap

# Check if user namespaces are enabled
cat /proc/sys/user/max_user_namespaces

# Should be > 0 (typically 10000 or higher)
# If 0, enable it:
sudo sysctl kernel.unprivileged_userns_clone=1
```

### **Fix 2: Check Permissions**

```bash
# Check if user has proper permissions
id

# Check Docker directories
ls -la ~/.local/share/docker
ls -la ~/.config/systemd/user/docker.service
```

### **Fix 3: Reinstall Rootless Docker**

```bash
# Uninstall current setup (as suggested by error)
/usr/bin/dockerd-rootless-setuptool.sh uninstall -f
/usr/bin/rootlesskit rm -rf /home/mgmt1/.local/share/docker

# Reinstall
dockerd-rootless-setuptool.sh install

# Try starting again
systemctl --user start docker.service
```

### **Fix 4: Manual Start (Test)**

```bash
# Try starting Docker daemon manually to see error
dockerd-rootless.sh

# Or with verbose output
dockerd-rootless.sh --debug
```

### **Fix 5: Check PATH**

```bash
# Find Docker binary
which docker
find /usr -name docker 2>/dev/null

# Add to PATH if needed
export PATH=$PATH:/usr/bin
docker --version
```

---

## 🎯 Complete Diagnostic Script

**Run this to gather all diagnostic info:**

```bash
{
  echo "=== DOCKER ROOTLESS DIAGNOSTICS ==="
  echo ""
  echo "1. Service Status:"
  systemctl --user status docker.service --no-pager -l
  echo ""
  echo "2. Error Logs:"
  journalctl --user -n 30 --no-pager --unit docker.service
  echo ""
  echo "3. System Requirements:"
  echo "  uidmap installed:" && dpkg -l | grep uidmap
  echo "  user namespaces:" && cat /proc/sys/user/max_user_namespaces
  echo ""
  echo "4. Docker Directories:"
  ls -la ~/.local/share/docker 2>/dev/null || echo "  Directory doesn't exist"
  ls -la ~/.config/systemd/user/docker.service 2>/dev/null || echo "  Service file doesn't exist"
  echo ""
  echo "5. Docker Binary:"
  which docker || echo "  docker not in PATH"
  which dockerd-rootless.sh || echo "  dockerd-rootless.sh not found"
  echo ""
  echo "6. User Info:"
  id
  echo ""
  echo "7. Systemd User Services:"
  systemctl --user list-units --type=service | grep docker
} > ~/docker-diagnostics.txt 2>&1

cat ~/docker-diagnostics.txt
```

---

## 🚀 Alternative: Use Regular Docker (Not Rootless)

**If rootless Docker continues to fail, consider regular Docker:**

```bash
# Install regular Docker (requires sudo)
sudo apt-get install -y docker.io

# Add user to docker group
sudo usermod -aG docker $USER

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Log out and back in for group changes
# Then test:
docker --version
docker ps
```

---

## 📋 Quick Fix Attempt

**Try these in order:**

```bash
# 1. Check logs first
journalctl --user -n 20 --no-pager --unit docker.service

# 2. If it's a namespace issue:
sudo sysctl kernel.unprivileged_userns_clone=1

# 3. Try manual start to see error
dockerd-rootless.sh

# 4. If manual start works, check service file
cat ~/.config/systemd/user/docker.service

# 5. Restart service
systemctl --user daemon-reload
systemctl --user restart docker.service
```

---

**Share the output of the diagnostic script and I'll help identify the specific issue!**




