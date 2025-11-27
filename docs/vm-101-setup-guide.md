<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# VM 101 - AI Assistant & Cursor AI Setup Guide

## 🎯 Purpose
VM 101 serves as the central management and AI development environment, running Cursor AI with SSH access to all VMs.

## 📋 VM Specifications
- **VM ID**: 101
- **IP Address**: <VM101_IP>
- **Hostname**: ai-assistant-vm
- **User**: mgmt1
- **OS**: Ubuntu 24.04 LTS
- **Resources**: 8 cores, 32GB RAM, 500GB SSD

## 🔑 Prerequisites
- VM 101 created and running
- Static IP configured: <VM101_IP>
- User `mgmt1` created with sudo access
- SSH access from Proxmox host working

---

## 📦 Step 1: Base System Setup

### Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### Install Essential Tools
```bash
sudo apt install -y \
  git \
  curl \
  wget \
  vim \
  nano \
  build-essential \
  software-properties-common \
  apt-transport-https \
  ca-certificates \
  gnupg \
  lsb-release \
  openssh-client \
  htop \
  net-tools \
  ufw \
  jq \
  unzip \
  zip \
  tree
```

---

## 🔐 Step 2: SSH Key Setup for VM Access

### Generate SSH Key Pair (if not exists)
```bash
# Check if key exists
ls -la ~/.ssh/id_ed25519

# If not, generate new key
ssh-keygen -t ed25519 -C "vm101-mgmt1" -f ~/.ssh/id_ed25519 -N ""
```

### Copy SSH Key to All VMs
```bash
# Create script to copy key to all VMs
cat > ~/copy-ssh-keys.sh << 'EOF'
#!/bin/bash
KEY_FILE="$HOME/.ssh/id_ed25519.pub"
KEY_CONTENT=$(cat $KEY_FILE)

VMs=(
  "proxy1@<VM120_IP>:Reverse Proxy"
  "wp1@<VM150_IP>:WordPress"
  "dbs1@<VM160_IP>:Database"
  "gsh1@<VM170_IP>:Game Servers"
  "apis1@<VM180_IP>:API Services"
)

for vm in "${VMs[@]}"; do
  IFS=':' read -r userhost desc <<< "$vm"
  IFS='@' read -r user host <<< "$userhost"
  
  echo "Adding key to $desc ($user@$host)..."
  ssh-copy-id -i $KEY_FILE $user@$host || echo "Failed to add key to $user@$host (might need manual setup)"
done

echo "SSH key distribution complete!"
EOF

chmod +x ~/copy-ssh-keys.sh
```

### Test SSH Access
```bash
# Test SSH to each VM
ssh proxy1@<VM120_IP> "hostname && whoami"
ssh wp1@<VM150_IP> "hostname && whoami"
ssh dbs1@<VM160_IP> "hostname && whoami"
ssh gsh1@<VM170_IP> "hostname && whoami"
ssh apis1@<VM180_IP> "hostname && whoami"
```

---

## 🐍 Step 3: Python Environment Setup

### Install Python and Pip
```bash
sudo apt install -y python3 python3-pip python3-venv python3-dev
```

### Create AI Workspace with Virtual Environment
```bash
mkdir -p ~/ai-workspace
cd ~/ai-workspace
python3 -m venv ai-env
source ai-env/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Install AI/ML Libraries
```bash
pip install \
  numpy \
  pandas \
  matplotlib \
  seaborn \
  scikit-learn \
  jupyter \
  jupyterlab \
  openai \
  langchain \
  transformers \
  torch \
  tensorflow
```

### Add to .bashrc
```bash
cat >> ~/.bashrc << 'EOF'

# AI Workspace Environment
alias ai-env="source ~/ai-workspace/ai-env/bin/activate"
export PATH=$PATH:/home/mgmt1/.local/bin
export PYTHONPATH=$PYTHONPATH:/home/mgmt1/ai-workspace
EOF

source ~/.bashrc
```

---

## 🐳 Step 4: Docker Setup

### Install Docker
```bash
# Add Docker repository
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
```

### Verify Docker
```bash
# Log out and back in, then:
docker --version
docker run hello-world
```

---

## 💻 Step 5: VS Code Server (code-server) Setup

### Install code-server
```bash
curl -fsSL https://code-server.dev/install.sh | sh

# Enable and start service
sudo systemctl enable --now code-server@$USER
```

### Configure code-server
```bash
mkdir -p ~/.config/code-server

cat > ~/.config/code-server/config.yaml << 'EOF'
bind-addr: 0.0.0.0:8080
auth: password
password: YOUR_SECURE_PASSWORD_HERE
cert: false
EOF

# Set a secure password
# Generate password: openssl rand -base64 32
PASSWORD=$(openssl rand -base64 32)
sed -i "s/YOUR_SECURE_PASSWORD_HERE/$PASSWORD/" ~/.config/code-server/config.yaml
echo "Code-server password saved to config file"
echo "Password: $PASSWORD"

# Restart code-server
sudo systemctl restart code-server@$USER
```

### Configure Firewall
```bash
sudo ufw allow 8080/tcp
sudo ufw reload
```

---

## 🔗 Step 6: Access code-server via Reverse Proxy

### Option A: SSH Tunnel (Simple)
From your PC:
```bash
ssh -L 8080:localhost:8080 mgmt1@<VM101_IP>
```
Then access: `http://localhost:8080`

### Option B: Cloudflare Tunnel (Recommended for Remote)
Add to VM 120 reverse proxy nginx config:
```nginx
location /code-server/ {
    proxy_pass http://<VM101_IP>:8080/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # WebSocket support
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

---

## 📂 Step 7: Repository Setup

### Clone All Repositories
```bash
mkdir -p ~/repos
cd ~/repos

# Clone Dell-Server-Roadmap
git clone git@github.com:MatoTeziTanka/Dell-Server-Roadmap.git

# Add other repositories as needed
# git clone git@github.com:username/repo-name.git
```

### Configure Git
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 📝 Step 8: VM Management Scripts

### Create Management Script
```bash
mkdir -p ~/management-scripts

cat > ~/management-scripts/manage-vms.sh << 'EOF'
#!/bin/bash
# VM Management Script

case "$1" in
    "status")
        echo "=== VM Status Check ==="
        echo "VM 101 (AI Assistant): $(ping -c 1 <VM101_IP> > /dev/null 2>&1 && echo 'UP' || echo 'DOWN')"
        echo "VM 120 (Reverse Proxy): $(ping -c 1 <VM120_IP> > /dev/null 2>&1 && echo 'UP' || echo 'DOWN')"
        echo "VM 150 (WordPress): $(ping -c 1 <VM150_IP> > /dev/null 2>&1 && echo 'UP' || echo 'DOWN')"
        echo "VM 160 (Database): $(ping -c 1 <VM160_IP> > /dev/null 2>&1 && echo 'UP' || echo 'DOWN')"
        echo "VM 170 (Game Servers): $(ping -c 1 <VM170_IP> > /dev/null 2>&1 && echo 'UP' || echo 'DOWN')"
        echo "VM 180 (API Services): $(ping -c 1 <VM180_IP> > /dev/null 2>&1 && echo 'UP' || echo 'DOWN')"
        echo "VM 200 (Plex): $(ping -c 1 <VM200_IP> > /dev/null 2>&1 && echo 'UP' || echo 'DOWN')"
        ;;
    "ssh")
        if [ -z "$2" ]; then
            echo "Usage: $0 ssh <vm-number>"
            echo "Available VMs:"
            echo "  120 - Reverse Proxy"
            echo "  150 - WordPress"
            echo "  160 - Database"
            echo "  170 - Game Servers"
            echo "  180 - API Services"
        else
            case "$2" in
                120) ssh proxy1@<VM120_IP> ;;
                150) ssh wp1@<VM150_IP> ;;
                160) ssh dbs1@<VM160_IP> ;;
                170) ssh gsh1@<VM170_IP> ;;
                180) ssh apis1@<VM180_IP> ;;
                *) echo "Unknown VM: $2" ;;
            esac
        fi
        ;;
    "backup")
        echo "Starting backup process..."
        # Add backup logic here
        ;;
    *)
        echo "VM Management Script"
        echo "Usage: $0 {status|ssh|backup}"
        echo ""
        echo "Commands:"
        echo "  status  - Check status of all VMs"
        echo "  ssh     - SSH to specific VM"
        echo "  backup  - Start backup process"
        ;;
esac
EOF

chmod +x ~/management-scripts/manage-vms.sh

# Add aliases
cat >> ~/.bashrc << 'EOF'

# VM Management Aliases
alias vm-status="~/management-scripts/manage-vms.sh status"
alias vm-ssh="~/management-scripts/manage-vms.sh ssh"
EOF

source ~/.bashrc
```

---

## 🚀 Step 9: Cursor AI Installation

### Install Cursor (Binary)
```bash
cd /tmp

# Download Cursor (check latest version)
wget https://download.cursor.sh/linux/cursor-latest-amd64.deb

# Install
sudo dpkg -i cursor-latest-amd64.deb || sudo apt install -f -y
```

### Alternative: Use code-server with Cursor Extension
Since Cursor is primarily a desktop app, you can:
1. Use code-server (already installed) and install Cursor-compatible extensions
2. Or use SSH + X11 forwarding for GUI apps

---

## 📊 Step 10: Monitoring and Status

### Create Status Check Script
```bash
cat > ~/management-scripts/check-status.sh << 'EOF'
#!/bin/bash
echo "=== VM 101 Status ==="
echo "Uptime: $(uptime)"
echo "Memory: $(free -h | grep Mem | awk '{print $3 "/" $2}')"
echo "Disk: $(df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 " used)"}')"
echo ""
echo "=== Services ==="
echo "code-server: $(systemctl --user is-active code-server@mgmt1)"
echo "Docker: $(systemctl is-active docker)"
echo ""
echo "=== Network ==="
ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | grep -v "127.0.0.1"
EOF

chmod +x ~/management-scripts/check-status.sh
```

---

## ✅ Verification Checklist

- [ ] System updated and essential tools installed
- [ ] SSH keys configured for all VMs
- [ ] Python environment and AI libraries installed
- [ ] Docker installed and working
- [ ] code-server installed and accessible
- [ ] All repositories cloned
- [ ] Management scripts created and working
- [ ] Firewall configured
- [ ] SSH access tested to all VMs

---

## 🔧 Troubleshooting

### code-server not accessible
1. Check service: `systemctl --user status code-server@mgmt1`
2. Check firewall: `sudo ufw status`
3. Check bind address in config: `cat ~/.config/code-server/config.yaml`

### SSH to VMs failing
1. Test connectivity: `ping <VM120_IP>`
2. Check SSH key: `cat ~/.ssh/id_ed25519.pub`
3. Manually add key: `ssh-copy-id user@vm-ip`

### Docker permission denied
1. Add user to group: `sudo usermod -aG docker $USER`
2. Log out and back in
3. Test: `docker run hello-world`

---

**Last Updated**: 2025-10-29

