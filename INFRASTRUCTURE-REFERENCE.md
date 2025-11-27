<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Infrastructure Reference - Quick Access

**Last Updated**: October 31, 2025  
📌 **READ THIS** before starting Discord, Game, or API projects!

---

## 🔑 Universal Credentials & Access

### SSH Access Pattern
All VMs follow this pattern:
```bash
# Standard user password for all VMs
password: "<VM_PASSWORD>"  # See credentials.json

# Sudo usage
echo "<VM_PASSWORD>"  # See credentials.json | sudo -S command

# Key-based SSH is configured (ED25519)
```

### Network Configuration (All VMs)
```yaml
LAN: 192.168.12.0/24
Gateway: <EDGEROUTER_IP>
DNS: 8.8.8.8, 8.8.4.4 (or 1.1.1.1, 1.0.0.1)
```

### Proxmox Host
```bash
# Access Proxmox to create new VMs
ssh root@<PROXMOX_IP>
# Web UI: https://<PROXMOX_IP>:8006
```

---

## 🖥️ Existing VM Infrastructure

### VM101 - Management & AI Assistant ✅
- **IP**: <VM101_IP>
- **User**: mgmt1
- **Purpose**: Git repos, AI workspace, management scripts
- **Status**: Active
- **OS**: Ubuntu 24.04 LTS
- **Password**: Norelec7!

### VM120 - Reverse Proxy & Cloudflare Tunnel ✅
- **IP**: <VM120_IP>
- **User**: proxy1
- **Purpose**: Nginx reverse proxy, Cloudflare Tunnel, SSL termination
- **Services**: Nginx, Cloudflared
- **Status**: Active
- **Password**: Norelec7!
- **Cloudflare Tunnel**: norelec-tunnel (624c59c6-b364-4488-85e5-90225351b0e2)

**YOU WILL USE THIS VM FOR**:
- Adding new subdomains (bot.lightspeedup.com, game.lightspeedup.com, api.lightspeedup.com)
- Configuring Nginx reverse proxy for your services
- Setting up Cloudflare Tunnel routes

### VM150 - WordPress (Production) ✅
- **IP**: <VM150_IP>
- **User**: wp1
- **Purpose**: WordPress revenue site
- **Status**: Production
- **Password**: Norelec7!
- **Site**: https://wp.lightspeedup.com

**NOT FOR YOUR USE** - WordPress project only

---

## 🆕 VMs You Will Create

### VM160 - Discord Bot Services (You create this)
- **IP**: <VM160_IP> (suggested)
- **User**: bot1 (suggested)
- **Purpose**: Discord bot hosting
- **RAM**: 2GB
- **CPU**: 2 cores
- **Disk**: 25GB SSD
- **Status**: ⏭️ Not created yet

**Create with**:
```bash
ssh root@<PROXMOX_IP>
qm create 160 --name discord-bot-1 --memory 2048 --cores 2
```

### VM170 - Game Server Hosting (You create this)
- **IP**: <VM170_IP> (suggested)
- **User**: gamehost1 (suggested)
- **Purpose**: Pterodactyl + game servers
- **RAM**: 16GB (for multiple game servers)
- **CPU**: 6 cores
- **Disk**: 200GB SSD
- **Status**: ⏭️ Not created yet

**Create with**:
```bash
ssh root@<PROXMOX_IP>
qm create 170 --name game-server-1 --memory 16384 --cores 6
```

### VM180 - API Services (You create this)
- **IP**: <VM180_IP> (suggested)
- **User**: apihost1 (suggested)
- **Purpose**: API hosting (Express.js or FastAPI)
- **RAM**: 4GB
- **CPU**: 2 cores
- **Disk**: 50GB SSD
- **Status**: ⏭️ Not created yet

**Create with**:
```bash
ssh root@<PROXMOX_IP>
qm create 180 --name api-services-1 --memory 4096 --cores 2
```

---

## 🌐 Domain & DNS (Shared)

### Domain: lightspeedup.com
- **Registrar**: GoDaddy
- **DNS Provider**: Cloudflare
- **Expires**: December 22, 2025 ($21.99/yr)
- **Cloudflare Account**: sethpizzaboy@gmail.com
- **API Token**: Already configured (has Tunnel + DNS edit permissions)

### Cloudflare API Token
**Token Name**: Cloudflare-Infra-Tunnel-DNS  
**Permissions**:
- Account: Cloudflare Tunnel - Read/Edit
- Zone: DNS - Edit
- Zone: Zone - Read
- Zone Settings: Read
- Zone: Cache Purge
- Zone: Firewall Services - Edit

**Test Token**:
```bash
curl "https://api.cloudflare.com/client/v4/accounts/1b7e6de8d8a093cedf14784989dff6d1/tokens/verify" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Suggested Subdomains for Your Projects
```
Discord Bots:    bot.lightspeedup.com
Game Servers:    game.lightspeedup.com
API Services:    api.lightspeedup.com
```

---

## 🔒 Firewall Rules (UFW Standard)

### Standard UFW Setup (All VMs)
```bash
# Install UFW
sudo apt install -y ufw

# Default policy
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (ALWAYS DO THIS FIRST!)
sudo ufw allow 22/tcp

# Allow your service port (varies by project)
sudo ufw allow PORT/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status verbose
```

### Ports Already in Use
See `PORT-ALLOCATION.md` for complete list:

**Reserved**:
- 22: SSH (all VMs)
- 80: HTTP (VM120, VM150)
- 3306: MySQL (internal only)
- 6379: Redis (internal only)
- 25565: Minecraft (planned for VM170)

---

## 🚇 Cloudflare Tunnel Setup (VM120)

### Existing Tunnel
- **Name**: norelec-tunnel
- **ID**: 624c59c6-b364-4488-85e5-90225351b0e2
- **Credentials**: `/home/proxy1/.cloudflared/624c59c6-b364-4488-85e5-90225351b0e2.json`

### Current Routes
```yaml
ingress:
  - hostname: wp.lightspeedup.com
    service: http://localhost:80
  - service: http_status:404
```

### To Add Your Service
```bash
# SSH to VM120
ssh proxy1@<VM120_IP>

# Edit tunnel config
sudo nano /etc/cloudflared/config.yml

# Add your route BEFORE the 404 line:
#  - hostname: YOUR-SUBDOMAIN.lightspeedup.com
#    service: http://YOUR-VM-IP:YOUR-PORT

# Example for Discord bot dashboard:
#  - hostname: bot.lightspeedup.com
#    service: http://<VM160_IP>:3000

# Restart tunnel
sudo systemctl restart cloudflared

# Check status
sudo systemctl status cloudflared
```

### Add DNS Record in Cloudflare
```bash
# Create CNAME for your subdomain
# Use Cloudflare API or dashboard
# Point to: 624c59c6-b364-4488-85e5-90225351b0e2.cfargotunnel.com
```

---

## 🛡️ Nginx Reverse Proxy (VM120)

### To Add Your Service to Nginx
```bash
# SSH to VM120
ssh proxy1@<VM120_IP>

# Create config file
sudo nano /etc/nginx/sites-available/YOUR-SUBDOMAIN.lightspeedup.com.conf

# Basic proxy template:
server {
    listen 80;
    server_name YOUR-SUBDOMAIN.lightspeedup.com;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    location / {
        proxy_pass http://YOUR-VM-IP:YOUR-PORT;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/YOUR-SUBDOMAIN.lightspeedup.com.conf /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Reload
sudo systemctl reload nginx
```

---

## 💳 Stripe Integration (Shared)

### Stripe Account
- **Email**: sethpizzaboy@gmail.com (or business account)
- **Current Status**: WordPress using test mode
- **Dashboard**: https://dashboard.stripe.com/

### Test Keys (Shared - Safe to Use)
```
Publishable: pk_test_51SNeqpJbRpPPse0TBcAvUAjuilPOVLxnCqEjJjwHHKxUua9uWl1EyrsPG46Lse9nIpZ845tectsJhVv5WzEFhKmO00BrPFBJUi

Secret: <STRIPE_TEST_SECRET_KEY>  # See credentials.json
```

### Test Card
```
Card: 4242 4242 4242 4242
Expiry: 12/26 (any future date)
CVC: 123 (any 3 digits)
ZIP: 12345 (any 5 digits)
```

### When Creating Your Products
- Create separate products for your service
- Use consistent naming: "[Service Name] - [Plan]"
- Configure webhook URL: `https://YOUR-SUBDOMAIN.lightspeedup.com/webhook/stripe`

---

## 🔧 Common Setup Commands

### Create New Ubuntu VM
```bash
# On Proxmox host
ssh root@<PROXMOX_IP>

# Create VM (adjust memory/cores/disk as needed)
qm create VM-ID --name vm-name --memory RAM-MB --cores NUM-CORES

# Set up networking, storage, etc. through Proxmox web UI
```

### Initial VM Setup (After Install)
```bash
# SSH to new VM
ssh USER@192.168.12.VM-ID

# Update system
sudo apt update && sudo apt upgrade -y

# Install essentials
sudo apt install -y curl wget git nano htop net-tools ufw

# Configure UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw enable

# Set static IP (if needed)
sudo nano /etc/netplan/00-installer-config.yaml
# Set IP, gateway, DNS
sudo netplan apply

# Create user if needed
sudo adduser USERNAME
sudo usermod -aG sudo USERNAME
```

### Install Node.js (Discord/API projects)
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node --version
npm --version
```

### Install Python (API/Discord projects)
```bash
sudo apt install -y python3 python3-pip python3-venv
python3 --version
pip3 --version
```

### Install PostgreSQL (API/Discord projects)
```bash
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable postgresql
sudo -u postgres psql
# CREATE DATABASE your_db;
# CREATE USER your_user WITH PASSWORD 'password';
# GRANT ALL PRIVILEGES ON DATABASE your_db TO your_user;
```

### Install Redis (API projects)
```bash
sudo apt install -y redis-server
sudo systemctl enable redis-server
redis-cli ping
# PONG
```

---

## 📊 Resource Allocation (Current)

| VM | Purpose | RAM | CPU | Disk | Status |
|----|---------|-----|-----|------|--------|
| VM101 | Management | 4GB | 2 | 50GB | ✅ Active |
| VM120 | Reverse Proxy | 2GB | 1 | 25GB | ✅ Active |
| VM150 | WordPress | 4GB | 2 | 50GB | ✅ Active |
| VM160 | Discord Bots | 2GB | 2 | 25GB | ⏭️ Create |
| VM170 | Game Servers | 16GB | 6 | 200GB | ⏭️ Create |
| VM180 | API Services | 4GB | 2 | 50GB | ⏭️ Create |
| **Total** | | **32GB** | **15** | **400GB** | |

**Check Dell server capacity before creating VMs!**

---

## 🔗 Documentation Links

### Your Project Docs
- `Discord-Bot-Services/VERSION-CONTROL.md`
- `Game-Server-Hosting/VERSION-CONTROL.md`
- `API-Services/VERSION-CONTROL.md`

### Shared Infrastructure
- `../INFRASTRUCTURE.md` - Detailed infrastructure overview
- `../PORT-ALLOCATION.md` - Complete port mapping
- `../REVENUE-STRATEGY.md` - Overall revenue plan
- `../README.md` - Project overview

### WordPress (For Reference)
- `WordPress-VM/CURRENT-STATE.md` - Complete VM150 state
- `WordPress-VM/VERSION-CONTROL.md` - WordPress version history

---

## 🚨 Important Notes

### DO:
- ✅ Check `PORT-ALLOCATION.md` before opening ports
- ✅ Use VM120 for all HTTP/HTTPS services (via Cloudflare Tunnel)
- ✅ Follow UFW firewall best practices
- ✅ Update `INFRASTRUCTURE.md` when you create new VMs
- ✅ Use test Stripe keys first, then switch to live
- ✅ Document all credentials (except in git!)

### DON'T:
- ❌ Expose database ports (3306, 5432, etc.) to internet
- ❌ Skip firewall configuration
- ❌ Use VM150 for your projects (WordPress only!)
- ❌ Commit real passwords/API keys to git
- ❌ Forget to update DNS records when adding services
- ❌ Create VMs without checking available resources

---

## 📞 Getting Help

### If VM120 (Reverse Proxy) Isn't Working:
```bash
ssh proxy1@<VM120_IP>
sudo systemctl status nginx cloudflared
sudo nginx -t  # Test config
journalctl -u cloudflared -f  # Check tunnel logs
```

### If You Can't Create New VM:
- Check Proxmox web UI: https://<PROXMOX_IP>:8006
- Verify available resources
- Check existing VMs: `qm list`

### If Domain/DNS Not Working:
- Check Cloudflare dashboard
- Verify DNS CNAME points to tunnel
- Check tunnel config includes your hostname
- Test from command line: `nslookup YOUR-SUBDOMAIN.lightspeedup.com`

---

## ✅ Pre-Flight Checklist (Before Starting Your Project)

- [ ] Read this INFRASTRUCTURE-REFERENCE.md
- [ ] Read your project's VERSION-CONTROL.md
- [ ] Check `PORT-ALLOCATION.md` for available ports
- [ ] Verify Dell server has RAM for your VM
- [ ] Understand VM120 reverse proxy setup
- [ ] Have Cloudflare credentials ready
- [ ] Know how to create VMs in Proxmox
- [ ] UFW firewall commands memorized
- [ ] Stripe test keys ready

---

**Last Updated**: October 31, 2025  
**For Questions**: Check project-specific AI-COLLABORATION.md files  
**Need Infrastructure Changes**: Update `../INFRASTRUCTURE.md`




