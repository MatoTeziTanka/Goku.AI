<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
#!/bin/bash
# VM 101 Complete Setup Script
# This script sets up VM 101 as the AI Assistant & Cursor AI management VM

set -e

echo "========================================="
echo "VM 101 - Complete Setup Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as mgmt1 user
if [ "$USER" != "mgmt1" ]; then
    echo -e "${RED}Error: This script must be run as mgmt1 user${NC}"
    exit 1
fi

# Step 1: Update System
echo -e "${GREEN}[1/10] Updating system...${NC}"
sudo apt update && sudo apt upgrade -y

# Step 2: Install Essential Tools
echo -e "${GREEN}[2/10] Installing essential tools...${NC}"
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
  tree \
  openssl

# Step 3: Configure Firewall
echo -e "${GREEN}[3/10] Configuring firewall...${NC}"
sudo ufw --force enable
sudo ufw allow 22/tcp
sudo ufw allow 8080/tcp
sudo ufw reload

# Step 4: Setup SSH Keys
echo -e "${GREEN}[4/10] Setting up SSH keys...${NC}"
mkdir -p ~/.ssh
chmod 700 ~/.ssh

if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "Generating SSH key..."
    ssh-keygen -t ed25519 -C "vm101-mgmt1" -f ~/.ssh/id_ed25519 -N ""
fi

# Display public key for manual addition to VMs
echo -e "${YELLOW}Public SSH Key (add to authorized_keys on other VMs):${NC}"
cat ~/.ssh/id_ed25519.pub
echo ""

# Step 5: Python Environment
echo -e "${GREEN}[5/10] Setting up Python environment...${NC}"
sudo apt install -y python3 python3-pip python3-venv python3-dev

mkdir -p ~/ai-workspace
cd ~/ai-workspace

if [ ! -d "ai-env" ]; then
    python3 -m venv ai-env
fi

source ai-env/bin/activate
pip install --upgrade pip setuptools wheel

# Install core AI libraries
echo "Installing AI/ML libraries (this may take a few minutes)..."
pip install \
  numpy \
  pandas \
  matplotlib \
  seaborn \
  scikit-learn \
  jupyter \
  jupyterlab \
  openai \
  langchain

# Step 6: Docker Setup
echo -e "${GREEN}[6/10] Installing Docker...${NC}"
if ! command -v docker &> /dev/null; then
    # Add Docker repository
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    echo -e "${YELLOW}Note: Log out and back in for Docker group changes to take effect${NC}"
else
    echo "Docker already installed"
fi

# Step 7: VS Code Server
echo -e "${GREEN}[7/10] Installing code-server...${NC}"
if ! command -v code-server &> /dev/null; then
    curl -fsSL https://code-server.dev/install.sh | sh
else
    echo "code-server already installed"
fi

# Configure code-server
mkdir -p ~/.config/code-server

# Generate secure password
CODE_SERVER_PASSWORD=$(openssl rand -base64 32)

cat > ~/.config/code-server/config.yaml << EOF
bind-addr: 0.0.0.0:8080
auth: password
password: $CODE_SERVER_PASSWORD
cert: false
EOF

chmod 600 ~/.config/code-server/config.yaml

# Enable and start code-server
systemctl --user enable code-server@$USER || true
systemctl --user daemon-reload
systemctl --user start code-server@$USER || systemctl --user restart code-server@$USER

echo -e "${YELLOW}Code-server password: $CODE_SERVER_PASSWORD${NC}"
echo -e "${YELLOW}Save this password! It's also in ~/.config/code-server/config.yaml${NC}"

# Step 8: Create Directories
echo -e "${GREEN}[8/10] Creating workspace directories...${NC}"
mkdir -p ~/repos
mkdir -p ~/management-scripts
mkdir -p ~/workspace

# Step 9: Git Configuration
echo -e "${GREEN}[9/10] Configuring Git...${NC}"
if [ -z "$(git config --global user.name)" ]; then
    echo "Git not configured. Please run:"
    echo "  git config --global user.name 'Your Name'"
    echo "  git config --global user.email 'your.email@example.com'"
fi

# Step 10: Create Management Scripts
echo -e "${GREEN}[10/10] Creating management scripts...${NC}"

# VM Status Script
cat > ~/management-scripts/manage-vms.sh << 'EOF'
#!/bin/bash
# VM Management Script

case "$1" in
    "status")
        echo "=== VM Status Check ==="
        for vm in "101:AI Assistant" "120:Reverse Proxy" "150:WordPress" "160:Database" "170:Game Servers" "180:API Services" "200:Plex"; do
            IFS=':' read -r ip desc <<< "$vm"
            if [ "$ip" = "101" ]; then
                status="UP (THIS VM)"
            else
                status=$(ping -c 1 -W 1 192.168.12.$ip > /dev/null 2>&1 && echo "UP" || echo "DOWN")
            fi
            printf "VM $ip (%s): %s\n" "$desc" "$status"
        done
        ;;
    "ssh")
        if [ -z "$2" ]; then
            echo "Usage: $0 ssh <vm-number>"
            echo "Available VMs:"
            echo "  120 - Reverse Proxy (proxy1)"
            echo "  150 - WordPress (wp1)"
            echo "  160 - Database (dbs1)"
            echo "  170 - Game Servers (gsh1)"
            echo "  180 - API Services (apis1)"
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
    "check")
        echo "=== VM 101 Status ==="
        echo "Uptime: $(uptime -p)"
        echo "Memory: $(free -h | grep Mem | awk '{print $3 "/" $2}')"
        echo "Disk: $(df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 " used)"}')"
        echo ""
        echo "=== Services ==="
        echo "code-server: $(systemctl --user is-active code-server@mgmt1 2>/dev/null || echo 'not running')"
        echo "Docker: $(systemctl is-active docker 2>/dev/null || echo 'not running')"
        echo ""
        echo "=== Network ==="
        ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | grep -v "127.0.0.1"
        ;;
    *)
        echo "VM Management Script"
        echo "Usage: $0 {status|ssh|check}"
        echo ""
        echo "Commands:"
        echo "  status  - Check status of all VMs"
        echo "  ssh     - SSH to specific VM"
        echo "  check   - Check VM 101 status"
        ;;
esac
EOF

chmod +x ~/management-scripts/manage-vms.sh

# SSH Key Distribution Helper
cat > ~/management-scripts/distribute-ssh-keys.sh << 'EOF'
#!/bin/bash
# Helper script to distribute SSH keys to VMs
# Note: You'll need to manually add the key to each VM or provide passwords

KEY_FILE="$HOME/.ssh/id_ed25519.pub"

if [ ! -f "$KEY_FILE" ]; then
    echo "Error: SSH public key not found at $KEY_FILE"
    exit 1
fi

VMs=(
  "proxy1@<VM120_IP>:Reverse Proxy"
  "wp1@<VM150_IP>:WordPress"
  "dbs1@<VM160_IP>:Database"
  "gsh1@<VM170_IP>:Game Servers"
  "apis1@<VM180_IP>:API Services"
)

echo "SSH Public Key:"
cat $KEY_FILE
echo ""
echo "To add this key to each VM, run on each VM:"
echo "  mkdir -p ~/.ssh"
echo "  echo '$(cat $KEY_FILE)' >> ~/.ssh/authorized_keys"
echo "  chmod 700 ~/.ssh"
echo "  chmod 600 ~/.ssh/authorized_keys"
EOF

chmod +x ~/management-scripts/distribute-ssh-keys.sh

# Add aliases to .bashrc
if ! grep -q "VM Management Aliases" ~/.bashrc; then
    cat >> ~/.bashrc << 'EOF'

# VM Management Aliases
alias vm-status="~/management-scripts/manage-vms.sh status"
alias vm-ssh="~/management-scripts/manage-vms.sh ssh"
alias vm-check="~/management-scripts/manage-vms.sh check"

# AI Workspace Environment
alias ai-env="source ~/ai-workspace/ai-env/bin/activate"
export PATH=$PATH:/home/mgmt1/.local/bin
export PYTHONPATH=$PYTHONPATH:/home/mgmt1/ai-workspace
EOF
fi

echo ""
echo "========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "========================================="
echo ""
echo "Next Steps:"
echo "1. Add SSH key to other VMs (see ~/management-scripts/distribute-ssh-keys.sh)"
echo "2. Clone repositories: cd ~/repos && git clone <repo-url>"
echo "3. Access code-server:"
echo "   - SSH tunnel: ssh -L 8080:localhost:8080 mgmt1@<VM101_IP>"
echo "   - Then visit: http://localhost:8080"
echo "   - Password: $CODE_SERVER_PASSWORD"
echo ""
echo "4. Test commands:"
echo "   - vm-status  (check all VMs)"
echo "   - vm-check   (check VM 101)"
echo "   - vm-ssh 150 (SSH to WordPress VM)"
echo ""

