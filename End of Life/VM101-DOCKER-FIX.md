# 🔧 VM101 Docker Fix - Missing dockerd Binary

**Error:** `exec: dockerd: not found`  
**Cause:** Only `docker-ce-rootless-extras` installed, missing main Docker CE package  
**Solution:** Install full Docker CE, then reinstall rootless

---

## 🚀 Quick Fix (Recommended)

### **Option 1: Install Full Docker CE (Then Rootless)**

```bash
# Step 1: Install prerequisites
sudo apt-get update
sudo apt-get install -y ca-certificates curl

# Step 2: Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Step 3: Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Step 4: Install Docker CE
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Step 5: Reinstall rootless Docker
dockerd-rootless-setuptool.sh install

# Step 6: Start Docker
systemctl --user start docker
systemctl --user enable docker

# Step 7: Verify
docker --version
docker ps
```

---

## 🎯 Alternative: Use Regular Docker (Simpler)

**If you don't need rootless Docker, use regular Docker:**

```bash
# Install regular Docker (simpler)
sudo apt-get update
sudo apt-get install -y docker.io

# Add user to docker group
sudo usermod -aG docker $USER

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Log out and back in for group changes to take effect
# Then test:
docker --version
docker ps
```

**Note:** Regular Docker requires `sudo` for most commands (or being in docker group), but is simpler to set up.

---

## 🔍 Verify Current Docker Packages

```bash
# Check what Docker packages are installed
dpkg -l | grep docker

# Check if dockerd exists
which dockerd
find /usr -name dockerd 2>/dev/null
```

---

## 📋 All-in-One Script (Full Docker CE + Rootless)

```bash
#!/bin/bash
# Complete Docker CE + Rootless setup

# Install prerequisites
sudo apt-get update
sudo apt-get install -y ca-certificates curl uidmap

# Add Docker GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker CE
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras

# Initialize rootless Docker
dockerd-rootless-setuptool.sh install

# Start Docker
systemctl --user start docker
systemctl --user enable docker

# Verify
echo "Docker version:"
docker --version
echo ""
echo "Docker containers:"
docker ps
```

---

## ✅ Expected Result

After installation:
- `dockerd` binary will exist at `/usr/bin/dockerd`
- Rootless Docker will be able to start
- `docker --version` will work
- `docker ps` will show containers

---

## 🎯 Recommendation

**For VM101 control node, I recommend regular Docker (Option 2):**
- Simpler setup
- No rootless complexity
- Works fine for control/orchestration tasks
- Can still run containers as non-root user (via docker group)

**Rootless Docker is only needed if:**
- You can't use sudo
- You need true rootless operation
- Security requirements mandate it

---

**Run Option 1 (Full Docker CE) or Option 2 (Regular Docker) - both will work!**




