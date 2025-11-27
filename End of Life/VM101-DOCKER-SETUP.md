# 🐳 VM101 Docker Rootless Setup

**Issue:** Rootless Docker requires `uidmap` package  
**Solution:** Install requirements, then initialize Docker

---

## 🔧 Setup Commands

### **Step 1: Install Required Package**
```bash
# Install uidmap (required for rootless Docker)
sudo apt-get install -y uidmap
```

### **Step 2: Initialize Rootless Docker**
```bash
# Run the setup tool again
dockerd-rootless-setuptool.sh install
```

### **Step 3: Start Rootless Docker**
```bash
# Start the rootless Docker daemon
systemctl --user start docker

# Enable auto-start
systemctl --user enable docker

# Check status
systemctl --user status docker
```

### **Step 4: Verify Docker Works**
```bash
# Check Docker version
docker --version

# List containers
docker ps

# Check Docker info
docker info
```

---

## 🚨 If Docker Command Still Not Found

### **Add Docker to PATH**
```bash
# Check where Docker is installed
which dockerd-rootless.sh
ls -la $(which dockerd-rootless.sh)

# Add to PATH in .bashrc
echo 'export PATH=$PATH:/usr/bin' >> ~/.bashrc
source ~/.bashrc

# Or add Docker bin directory
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

### **Check Docker Context**
```bash
# List Docker contexts
docker context ls

# Use rootless context (if available)
docker context use rootless
```

---

## 📋 Complete Setup Script

**Run this all at once:**

```bash
# Install requirements
sudo apt-get install -y uidmap

# Initialize rootless Docker
dockerd-rootless-setuptool.sh install

# Start Docker service
systemctl --user start docker
systemctl --user enable docker

# Verify
docker --version
docker ps
```

---

## ✅ Expected Output

After successful setup:
- `~/.docker/run/docker.sock` should exist
- `docker --version` should work
- `docker ps` should show empty list (or existing containers)
- `systemctl --user status docker` should show "active (running)"

---

## 🔍 Troubleshooting

**If setup still fails:**
```bash
# Check if user is in docker group (not needed for rootless, but check anyway)
groups | grep docker

# Check systemd user services
systemctl --user list-units | grep docker

# Check Docker logs
journalctl --user -u docker -n 50
```

**If Docker socket doesn't exist:**
```bash
# Manually start rootless Docker daemon
dockerd-rootless.sh &

# Check if socket is created
ls -la ~/.docker/run/docker.sock
```

---

**After setup, Docker commands will work on VM101!**




