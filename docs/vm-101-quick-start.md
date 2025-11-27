<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# VM 101 Quick Start - Run This Now

## 🚀 Quick Setup Instructions

### Step 1: SSH to VM 101
From your Proxmox host (or PC with SSH access):
```bash
ssh mgmt1@<VM101_IP>
```

### Step 2: Clone the Setup Script
```bash
# Create repos directory
mkdir -p ~/repos
cd ~/repos

# Clone the repository (if you have SSH key set up) OR
git clone https://github.com/MatoTeziTanka/Dell-Server-Roadmap.git

# OR copy the script directly
```

### Step 3: Download and Run the Setup Script
```bash
# Download the setup script
cd ~
wget https://raw.githubusercontent.com/MatoTeziTanka/Dell-Server-Roadmap/master/scripts/vm-101-complete-setup.sh

# Make it executable
chmod +x vm-101-complete-setup.sh

# Run it
./vm-101-complete-setup.sh
```

**OR** if the script is already there:
```bash
cd ~/repos/Dell-Server-Roadmap
chmod +x scripts/vm-101-complete-setup.sh
~/repos/Dell-Server-Roadmap/scripts/vm-101-complete-setup.sh
```

### Step 4: Save Your Code-Server Password
The script will output a password for code-server. **SAVE IT** - you'll need it to access VS Code Server.

### Step 5: Add SSH Key to Other VMs
After setup, run:
```bash
~/management-scripts/distribute-ssh-keys.sh
```

Then manually add the SSH public key to each VM's `~/.ssh/authorized_keys` file.

### Step 6: Access code-server
From your PC, create SSH tunnel:
```bash
ssh -L 8080:localhost:8080 mgmt1@<VM101_IP>
```

Then open browser: `http://localhost:8080`

Enter the password from Step 4.

---

## 📋 Post-Setup Checklist

- [ ] Setup script completed successfully
- [ ] SSH key copied to all VMs (120, 150, 160, 170, 180)
- [ ] Test SSH access: `vm-ssh 150` (should connect to WordPress VM)
- [ ] Code-server accessible via SSH tunnel
- [ ] Clone all repositories to `~/repos/`
- [ ] Python environment working: `ai-env` then `python --version`
- [ ] Docker working: `docker run hello-world`

---

## 🔧 Common Issues

### Script fails on Docker install
```bash
# Try installing Docker manually
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and back in
```

### code-server not starting
```bash
# Check status
systemctl --user status code-server@mgmt1

# View logs
journalctl --user -u code-server@mgmt1

# Restart
systemctl --user restart code-server@mgmt1
```

### Can't access code-server via SSH tunnel
1. Make sure SSH tunnel is active: `ssh -L 8080:localhost:8080 mgmt1@<VM101_IP>`
2. Check code-server is running: `systemctl --user status code-server@mgmt1`
3. Try accessing: `http://127.0.0.1:8080` instead of `localhost:8080`

---

## 📞 Need Help?

See the full guide: `docs/vm-101-setup-guide.md`

