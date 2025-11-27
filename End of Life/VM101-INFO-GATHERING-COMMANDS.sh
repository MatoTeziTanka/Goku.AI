<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
#!/bin/bash
# VM101 Information Gathering Script
# Run these commands on VM101 via SSH to gather current system state
# Output will be saved to files for easy review

echo "========================================="
echo "VM101 Information Gathering"
echo "========================================="
echo ""
echo "This script will gather all information needed for VM101 migration summary"
echo "Output files will be saved to ~/vm101-info/"
echo ""

# Create output directory
mkdir -p ~/vm101-info
cd ~/vm101-info

echo "[1/12] Gathering OS Version & System Info..."
echo "=========================================" > 01-os-version.txt
lsb_release -a >> 01-os-version.txt 2>&1
echo "" >> 01-os-version.txt
echo "--- /etc/os-release ---" >> 01-os-version.txt
cat /etc/os-release >> 01-os-version.txt
echo "" >> 01-os-version.txt
echo "--- hostnamectl ---" >> 01-os-version.txt
hostnamectl >> 01-os-version.txt
echo "" >> 01-os-version.txt
echo "--- uname -a ---" >> 01-os-version.txt
uname -a >> 01-os-version.txt
echo "✅ Saved to 01-os-version.txt"

echo ""
echo "[2/12] Gathering Installed Packages..."
echo "=========================================" > 02-packages.txt
echo "--- All Installed Packages ---" >> 02-packages.txt
dpkg -l >> 02-packages.txt 2>&1
echo "" >> 02-packages.txt
echo "--- Key Packages Check ---" >> 02-packages.txt
dpkg -l | grep -E "python3|docker|code-server|git|curl|wget|vim|nano|build-essential|ufw|jq|openssh" >> 02-packages.txt
echo "" >> 02-packages.txt
echo "--- Python Version ---" >> 02-packages.txt
python3 --version >> 02-packages.txt 2>&1
echo "" >> 02-packages.txt
echo "--- Docker Version ---" >> 02-packages.txt
docker --version >> 02-packages.txt 2>&1
echo "" >> 02-packages.txt
echo "--- code-server Version ---" >> 02-packages.txt
code-server --version >> 02-packages.txt 2>&1
echo "✅ Saved to 02-packages.txt"

echo ""
echo "[3/12] Gathering Disk Usage..."
echo "=========================================" > 03-disk-usage.txt
echo "--- Overall Disk Usage ---" >> 03-disk-usage.txt
df -h >> 03-disk-usage.txt
echo "" >> 03-disk-usage.txt
echo "--- GitHub Directory Sizes ---" >> 03-disk-usage.txt
if [ -d ~/GitHub ]; then
    du -sh ~/GitHub/* 2>/dev/null >> 03-disk-usage.txt
else
    echo "~/GitHub directory does not exist" >> 03-disk-usage.txt
fi
echo "" >> 03-disk-usage.txt
echo "--- Python Environment Sizes ---" >> 03-disk-usage.txt
if [ -d ~/ai-workspace ]; then
    du -sh ~/ai-workspace/* 2>/dev/null >> 03-disk-usage.txt
else
    echo "~/ai-workspace directory does not exist" >> 03-disk-usage.txt
fi
echo "" >> 03-disk-usage.txt
echo "--- Home Directory Total Size ---" >> 03-disk-usage.txt
du -sh ~ >> 03-disk-usage.txt
echo "" >> 03-disk-usage.txt
echo "--- Top 10 Largest Directories in Home ---" >> 03-disk-usage.txt
du -h ~ 2>/dev/null | sort -rh | head -10 >> 03-disk-usage.txt
echo "✅ Saved to 03-disk-usage.txt"

echo ""
echo "[4/12] Gathering Python Environment Info..."
echo "=========================================" > 04-python-env.txt
echo "--- Python Version ---" >> 04-python-env.txt
python3 --version >> 04-python-env.txt
echo "" >> 04-python-env.txt
echo "--- Python3 Path ---" >> 04-python-env.txt
which python3 >> 04-python-env.txt
echo "" >> 04-python-env.txt
echo "--- Virtual Environments ---" >> 04-python-env.txt
if [ -d ~/ai-workspace ]; then
    ls -la ~/ai-workspace/ >> 04-python-env.txt
    echo "" >> 04-python-env.txt
    echo "--- ai-env Contents ---" >> 04-python-env.txt
    if [ -d ~/ai-workspace/ai-env ]; then
        ls -la ~/ai-workspace/ai-env/ >> 04-python-env.txt
        echo "" >> 04-python-env.txt
        echo "--- Python Version in venv ---" >> 04-python-env.txt
        ~/ai-workspace/ai-env/bin/python --version >> 04-python-env.txt 2>&1
        echo "" >> 04-python-env.txt
        echo "--- Installed Packages in venv ---" >> 04-python-env.txt
        ~/ai-workspace/ai-env/bin/pip list >> 04-python-env.txt 2>&1
    else
        echo "ai-env directory does not exist" >> 04-python-env.txt
    fi
else
    echo "~/ai-workspace directory does not exist" >> 04-python-env.txt
fi
echo "" >> 04-python-env.txt
echo "--- Other Python Environments ---" >> 04-python-env.txt
find ~ -type d -name "venv" -o -name ".venv" -o -name "env" 2>/dev/null >> 04-python-env.txt
echo "✅ Saved to 04-python-env.txt"

echo ""
echo "[5/12] Gathering SSH Key Info..."
echo "=========================================" > 05-ssh-keys.txt
echo "--- SSH Directory Contents ---" >> 05-ssh-keys.txt
if [ -d ~/.ssh ]; then
    ls -la ~/.ssh/ >> 05-ssh-keys.txt
    echo "" >> 05-ssh-keys.txt
    echo "--- SSH Key Types ---" >> 05-ssh-keys.txt
    for key in ~/.ssh/id_*; do
        if [ -f "$key" ] && [ ! -f "${key}.pub" ]; then
            echo "Private key: $key" >> 05-ssh-keys.txt
            file "$key" >> 05-ssh-keys.txt
        fi
    done
    echo "" >> 05-ssh-keys.txt
    echo "--- Public Keys (for distribution) ---" >> 05-ssh-keys.txt
    for pubkey in ~/.ssh/*.pub; do
        if [ -f "$pubkey" ]; then
            echo "File: $pubkey" >> 05-ssh-keys.txt
            cat "$pubkey" >> 05-ssh-keys.txt
            echo "" >> 05-ssh-keys.txt
        fi
    done
else
    echo "~/.ssh directory does not exist" >> 05-ssh-keys.txt
fi
echo "" >> 05-ssh-keys.txt
echo "--- SSH Config ---" >> 05-ssh-keys.txt
if [ -f ~/.ssh/config ]; then
    cat ~/.ssh/config >> 05-ssh-keys.txt
else
    echo "No SSH config file" >> 05-ssh-keys.txt
fi
echo "✅ Saved to 05-ssh-keys.txt"

echo ""
echo "[6/12] Gathering Git Repository Info..."
echo "=========================================" > 06-git-repos.txt
echo "--- GitHub Directory Structure ---" >> 06-git-repos.txt
if [ -d ~/GitHub ]; then
    ls -la ~/GitHub/ >> 06-git-repos.txt
    echo "" >> 06-git-repos.txt
    echo "--- Repository Status ---" >> 06-git-repos.txt
    for repo in ~/GitHub/*; do
        if [ -d "$repo/.git" ]; then
            echo "" >> 06-git-repos.txt
            echo "Repository: $(basename $repo)" >> 06-git-repos.txt
            cd "$repo"
            echo "  Branch: $(git branch --show-current 2>/dev/null)" >> ~/vm101-info/06-git-repos.txt
            echo "  Remote: $(git remote get-url origin 2>/dev/null)" >> ~/vm101-info/06-git-repos.txt
            echo "  Status: $(git status --short 2>/dev/null | head -5)" >> ~/vm101-info/06-git-repos.txt
            cd - > /dev/null
        fi
    done
else
    echo "~/GitHub directory does not exist" >> 06-git-repos.txt
fi
echo "" >> 06-git-repos.txt
echo "--- Git Configuration ---" >> 06-git-repos.txt
git config --global --list >> 06-git-repos.txt 2>&1
echo "✅ Saved to 06-git-repos.txt"

echo ""
echo "[7/12] Gathering Docker Info..."
echo "=========================================" > 07-docker.txt
echo "--- Docker Version ---" >> 07-docker.txt
docker --version >> 07-docker.txt 2>&1
echo "" >> 07-docker.txt
echo "--- Docker Info ---" >> 07-docker.txt
docker info >> 07-docker.txt 2>&1
echo "" >> 07-docker.txt
echo "--- Docker Containers ---" >> 07-docker.txt
docker ps -a >> 07-docker.txt 2>&1
echo "" >> 07-docker.txt
echo "--- Docker Images ---" >> 07-docker.txt
docker images >> 07-docker.txt 2>&1
echo "" >> 07-docker.txt
echo "--- Docker Networks ---" >> 07-docker.txt
docker network ls >> 07-docker.txt 2>&1
echo "" >> 07-docker.txt
echo "--- Docker Compose Files ---" >> 07-docker.txt
find ~ -name "docker-compose.yml" -o -name "docker-compose.yaml" 2>/dev/null >> 07-docker.txt
echo "" >> 07-docker.txt
echo "--- Docker Service Status ---" >> 07-docker.txt
systemctl status docker >> 07-docker.txt 2>&1
echo "✅ Saved to 07-docker.txt"

echo ""
echo "[8/12] Gathering Network Configuration..."
echo "=========================================" > 08-network.txt
echo "--- IP Addresses ---" >> 08-network.txt
ip -4 addr show >> 08-network.txt
echo "" >> 08-network.txt
echo "--- Network Interfaces ---" >> 08-network.txt
ip link show >> 08-network.txt
echo "" >> 08-network.txt
echo "--- Routing Table ---" >> 08-network.txt
ip route show >> 08-network.txt
echo "" >> 08-network.txt
echo "--- DNS Configuration ---" >> 08-network.txt
cat /etc/resolv.conf >> 08-network.txt
echo "" >> 08-network.txt
echo "--- Listening Ports ---" >> 08-network.txt
sudo ss -tulnp >> 08-network.txt 2>&1
echo "" >> 08-network.txt
echo "--- Network Connections ---" >> 08-network.txt
netstat -tuln >> 08-network.txt 2>&1
echo "✅ Saved to 08-network.txt"

echo ""
echo "[9/12] Gathering Firewall Rules..."
echo "=========================================" > 09-firewall.txt
echo "--- UFW Status ---" >> 09-firewall.txt
sudo ufw status verbose >> 09-firewall.txt 2>&1
echo "" >> 09-firewall.txt
echo "--- UFW Rules (numbered) ---" >> 09-firewall.txt
sudo ufw status numbered >> 09-firewall.txt 2>&1
echo "" >> 09-firewall.txt
echo "--- iptables Rules ---" >> 09-firewall.txt
sudo iptables -L -n -v >> 09-firewall.txt 2>&1
echo "✅ Saved to 09-firewall.txt"

echo ""
echo "[10/12] Gathering Services & Cron Jobs..."
echo "=========================================" > 10-services.txt
echo "--- System Services ---" >> 10-services.txt
systemctl list-units --type=service --state=running >> 10-services.txt
echo "" >> 10-services.txt
echo "--- User Services ---" >> 10-services.txt
systemctl --user list-units --type=service --state=running >> 10-services.txt 2>&1
echo "" >> 10-services.txt
echo "--- code-server Status ---" >> 10-services.txt
systemctl --user status code-server@$USER >> 10-services.txt 2>&1
echo "" >> 10-services.txt
echo "--- Docker Service Status ---" >> 10-services.txt
systemctl status docker >> 10-services.txt 2>&1
echo "" >> 10-services.txt
echo "--- User Cron Jobs ---" >> 10-services.txt
crontab -l >> 10-services.txt 2>&1
echo "" >> 10-services.txt
echo "--- Root Cron Jobs ---" >> 10-services.txt
sudo crontab -l >> 10-services.txt 2>&1
echo "" >> 10-services.txt
echo "--- System Cron Directories ---" >> 10-services.txt
ls -la /etc/cron.d/ >> 10-services.txt 2>&1
ls -la /etc/cron.daily/ >> 10-services.txt 2>&1
ls -la /etc/cron.weekly/ >> 10-services.txt 2>&1
echo "✅ Saved to 10-services.txt"

echo ""
echo "[11/12] Gathering Management Scripts..."
echo "=========================================" > 11-scripts.txt
echo "--- Management Scripts Directory ---" >> 11-scripts.txt
if [ -d ~/management-scripts ]; then
    ls -la ~/management-scripts/ >> 11-scripts.txt
    echo "" >> 11-scripts.txt
    echo "--- Script Contents ---" >> 11-scripts.txt
    for script in ~/management-scripts/*.sh; do
        if [ -f "$script" ]; then
            echo "" >> 11-scripts.txt
            echo "=== $(basename $script) ===" >> 11-scripts.txt
            head -20 "$script" >> 11-scripts.txt
        fi
    done
else
    echo "~/management-scripts directory does not exist" >> 11-scripts.txt
fi
echo "" >> 11-scripts.txt
echo "--- Other Scripts in Home ---" >> 11-scripts.txt
find ~ -maxdepth 2 -name "*.sh" -type f 2>/dev/null >> 11-scripts.txt
echo "✅ Saved to 11-scripts.txt"

echo ""
echo "[12/12] Gathering Additional Info..."
echo "=========================================" > 12-additional.txt
echo "--- Environment Variables ---" >> 12-additional.txt
env | sort >> 12-additional.txt
echo "" >> 12-additional.txt
echo "--- PATH ---" >> 12-additional.txt
echo $PATH >> 12-additional.txt
echo "" >> 12-additional.txt
echo "--- Shell Configuration ---" >> 12-additional.txt
echo "Shell: $SHELL" >> 12-additional.txt
echo "" >> 12-additional.txt
echo "--- .bashrc Aliases ---" >> 12-additional.txt
grep -E "^alias|^export" ~/.bashrc 2>/dev/null >> 12-additional.txt
echo "" >> 12-additional.txt
echo "--- VS Code Server Config ---" >> 12-additional.txt
if [ -f ~/.config/code-server/config.yaml ]; then
    cat ~/.config/code-server/config.yaml >> 12-additional.txt
else
    echo "code-server config not found" >> 12-additional.txt
fi
echo "" >> 12-additional.txt
echo "--- Workspace Directories ---" >> 12-additional.txt
ls -la ~/ | grep -E "^d" >> 12-additional.txt
echo "" >> 12-additional.txt
echo "--- Memory Info ---" >> 12-additional.txt
free -h >> 12-additional.txt
echo "" >> 12-additional.txt
echo "--- CPU Info ---" >> 12-additional.txt
lscpu >> 12-additional.txt
echo "✅ Saved to 12-additional.txt"

echo ""
echo "========================================="
echo "Information Gathering Complete!"
echo "========================================="
echo ""
echo "All information saved to: ~/vm101-info/"
echo ""
echo "Files created:"
ls -lh ~/vm101-info/
echo ""
echo "To view a file:"
echo "  cat ~/vm101-info/01-os-version.txt"
echo ""
echo "To download all files to local machine:"
echo "  scp -r mgmt1@<VM101_IP>:~/vm101-info/ ./vm101-info/"
echo ""




