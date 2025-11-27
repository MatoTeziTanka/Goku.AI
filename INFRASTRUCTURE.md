<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Passive Income Infrastructure Overview

**Last Updated**: October 31, 2025  
**Repository**: https://github.com/MatoTeziTanka/PassiveIncome

---

## 🏗️ Physical Infrastructure

### Dell PowerEdge Server
- **Model**: Dell PowerEdge (Specific model TBD)
- **Location**: Home Lab
- **Hypervisor**: Proxmox VE
- **Management IP**: <PROXMOX_IP>
- **Purpose**: Host all passive income VMs

### Network Configuration
- **LAN**: 192.168.12.0/24
- **Gateway**: <EDGEROUTER_IP>
- **Router**: EdgeRouter (admin / SethNorelec7!)
- **Additional Hardware**: Deeper Connect Mini (admin / NoReLeC7!7!)
- **DNS**: Cloudflare (1.1.1.1, 1.0.0.1) + Google (8.8.8.8, 8.8.4.4)

---

## 🖥️ Virtual Machine Inventory

### VM101 - Management & AI Assistant
- **IP**: <VM101_IP>
- **OS**: Ubuntu 24.04 LTS
- **Purpose**: AI assistant workspace, Git repositories, management scripts
- **User**: mgmt1
- **Status**: ✅ Active

### VM120 - Reverse Proxy & Tunnel
- **IP**: <VM120_IP>
- **OS**: Ubuntu
- **Purpose**: Nginx reverse proxy, Cloudflare Tunnel, SSL termination
- **User**: proxy1
- **Services**: Nginx, Cloudflared, UFW
- **Cloudflare Tunnel**: norelec-tunnel (624c59c6-b364-4488-85e5-90225351b0e2)
- **Status**: ✅ Active

### VM150 - WordPress (Passive Income Project #1)
- **IP**: <VM150_IP>
- **OS**: Ubuntu 24.04.3 LTS
- **Purpose**: WordPress revenue site (https://wp.lightspeedup.com)
- **User**: wp1
- **Stack**: LAMP (Apache, MySQL, PHP)
- **Services**: WordPress, Redis, Apache
- **Status**: ✅ Production

### Future VMs (Planned)
- **VM160** - Discord Bot Server (TBD)
- **VM170** - Game Server Hosting (TBD)
- **VM180** - API Services (TBD)
- **VM190** - Additional services as needed

---

## 🌐 Domain & DNS Configuration

### Primary Domain: lightspeedup.com
- **Registrar**: GoDaddy
- **DNS Provider**: Cloudflare
- **Expires**: December 22, 2025 ($21.99/yr renewal)
- **Cloudflare Account**: sethpizzaboy@gmail.com

### Active Subdomains
| Subdomain | Type | Target | Purpose |
|-----------|------|--------|---------|
| wp.lightspeedup.com | CNAME | 624c59c6-...cfargotunnel.com | WordPress site |

### DNS Configuration Notes
- **DuckDNS**: ❌ Removed (was interfering with Cloudflare)
- **Cloudflare Tunnel**: ✅ Active for all HTTP/HTTPS services
- **Port Forwarding**: Only used for services that can't use tunnels (e.g., Plex)

---

## 🔒 Security Architecture

### Firewall Rules (UFW)
All VMs use UFW with default deny and explicit allow rules:
- Port 22 (SSH): Allowed from LAN only
- Port 80 (HTTP): Allowed on web servers
- Port 443 (HTTPS): Handled by Cloudflare Tunnel

### Cloudflare Protection
- **DDoS Protection**: ✅ Enabled
- **WAF**: ✅ Enabled
- **SSL/TLS**: Full (Strict) mode
- **Rate Limiting**: Custom rules per service

### Authentication
- **SSH**: Key-based authentication (ED25519 keys)
- **VM Passwords**: Norelec7! (change for production)
- **WordPress Admin**: Secure password stored separately
- **API Keys**: Environment variables, never committed to git

---

## 🔌 Port Allocation

### Reserved Ports by Service

| Port Range | Service | VM | Status |
|------------|---------|-----|--------|
| 22 | SSH | All VMs | ✅ Active |
| 80 | HTTP (Apache) | VM150 | ✅ Active |
| 3306 | MySQL | VM150 | 🔒 Internal |
| 6379 | Redis | VM150 | 🔒 Internal |
| 8080 | Nginx Proxy | VM120 | 🔒 Internal |
| 25565 | Minecraft (Future) | VM170 | ⏭️ Planned |
| 27015 | ARK/Steam (Future) | VM170 | ⏭️ Planned |
| 3000-3100 | API Services (Future) | VM180 | ⏭️ Planned |

### Cloudflare Tunnel Routing
All HTTP/HTTPS traffic routes through Cloudflare Tunnel on VM120:
```
Internet → Cloudflare → VM120 (Tunnel) → Nginx → Backend VMs
```

---

## 💳 Payment Processing

### Stripe Configuration
- **Account**: sethpizzaboy@gmail.com (or business account)
- **Mode**: Currently TEST mode (sandbox)
- **Integration**: WordPress Stripe Payments plugin
- **Webhook URL**: https://wp.lightspeedup.com/?asp_action=ipn

### Revenue Tracking
- **WordPress**: $9/mo Starter, $29/mo Business plans
- **Discord Bots**: TBD
- **Game Servers**: TBD
- **API Services**: TBD

---

## 📦 Backup Strategy

### Current Backups
- **WordPress (VM150)**: Manual backups (automated solution pending)
- **Git Repositories**: GitHub (MatoTeziTanka/PassiveIncome)
- **Proxmox Snapshots**: Available but not automated

### Planned Backup Solution
```bash
# Daily automated backups to external storage
- WordPress database dumps (MySQL)
- WordPress files (/var/www/wordpress)
- VM configuration files
- Retention: 7 daily, 4 weekly, 12 monthly
```

---

## 📊 Monitoring & Logging

### Current Monitoring
- **WordPress**: Activity Log plugin (audit trail)
- **Wordfence**: Security monitoring, malware scans
- **Manual Checks**: SSH-based server health checks

### Planned Monitoring
- [ ] UptimeRobot or Pingdom for uptime monitoring
- [ ] Grafana + Prometheus for system metrics
- [ ] Log aggregation (Loki or ELK stack)
- [ ] Alerting via email/Discord/Slack

---

## 🚀 Project Status Overview

| Project | Status | Revenue | VM | URL |
|---------|--------|---------|-----|-----|
| WordPress Site | ✅ Production (Test Mode) | $0 (Testing) | VM150 | https://wp.lightspeedup.com |
| Discord Bots | 🔄 Planning | $0 | TBD | N/A |
| Game Servers | 🔄 Planning | $0 | TBD | N/A |
| API Services | 🔄 Planning | $0 | TBD | N/A |

**Total Monthly Revenue**: $0 (Test mode)  
**Target Monthly Revenue**: $500+ (Goal for Q1 2026)

---

## 📁 Repository Structure

```
PassiveIncome/
├── WordPress-VM/
│   ├── AI-COLLABORATION.md
│   ├── vm-150-wordpress-config.md
│   ├── wordpress-production-hardening.md
│   └── wordpress-stripe-integration-complete.md
├── Discord-Bot-Services/
│   └── AI-COLLABORATION.md
├── Game-Server-Hosting/
│   └── AI-COLLABORATION.md
├── API-Services/
│   └── AI-COLLABORATION.md
├── INFRASTRUCTURE.md (this file)
├── PORT-ALLOCATION.md
└── README.md
```

---

## 🔧 Common Infrastructure Tasks

### Add New VM to Proxmox
```bash
# SSH to Proxmox host
ssh root@<PROXMOX_IP>

# Create new VM (example)
qm create 160 --name discord-bot-1 --memory 4096 --cores 2 --net0 virtio,bridge=vmbr0

# Clone from template if available
qm clone 150 160 --name discord-bot-1
```

### Configure New VM for Passive Income
```bash
# Set static IP
sudo nano /etc/netplan/00-installer-config.yaml

# Apply network config
sudo netplan apply

# Enable firewall
sudo ufw enable
sudo ufw allow 22/tcp

# Update system
sudo apt update && sudo apt upgrade -y
```

### Add New Cloudflare Tunnel Route
```bash
# SSH to VM120
ssh proxy1@<VM120_IP>

# Edit tunnel config
sudo nano /etc/cloudflared/config.yml

# Add new ingress rule
# - hostname: newservice.lightspeedup.com
#   service: http://192.168.12.XXX:PORT

# Restart tunnel
sudo systemctl restart cloudflared
```

---

## 🆘 Emergency Procedures

### WordPress Site Down
1. Check VM150 status: `ssh wp1@<VM150_IP>`
2. Restart Apache: `sudo systemctl restart apache2`
3. Check VM120 tunnel: `ssh proxy1@<VM120_IP> && sudo systemctl status cloudflared`
4. Verify Cloudflare DNS records
5. Check site: https://wp.lightspeedup.com

### Cloudflare Tunnel Down
1. SSH to VM120: `ssh proxy1@<VM120_IP>`
2. Check tunnel status: `sudo systemctl status cloudflared`
3. Restart tunnel: `sudo systemctl restart cloudflared`
4. Check logs: `sudo journalctl -u cloudflared -f`

### Complete Network Outage
1. Check physical Dell server status
2. Access Proxmox web UI: https://<PROXMOX_IP>:8006
3. Check EdgeRouter: `ssh admin@<EDGEROUTER_IP>`
4. Verify internet connection
5. Check Deeper Connect Mini status

---

## 📞 Contact & Support

### Key Accounts
- **GitHub**: MatoTeziTanka
- **Cloudflare**: sethpizzaboy@gmail.com
- **GoDaddy**: (domain registrar)
- **Stripe**: sethpizzaboy@gmail.com (or business account)

### Important Credentials
- **VM SSH**: Stored in ~/.ssh/ on VM101
- **WordPress Admin**: See WordPress-VM/AI-COLLABORATION.md
- **Cloudflare API Token**: Stored securely (not in git)
- **Stripe API Keys**: Stored in WordPress wp-config.php (test mode)

---

## ✅ Infrastructure Health Checklist

### Daily Checks
- [ ] All VMs online and responsive
- [ ] WordPress site accessible (https://wp.lightspeedup.com)
- [ ] Cloudflare Tunnel status: Healthy
- [ ] No critical security alerts (Wordfence)

### Weekly Checks
- [ ] System updates on all VMs
- [ ] Backup verification (restore test)
- [ ] Review Activity Log for suspicious behavior
- [ ] Check disk space usage on all VMs

### Monthly Checks
- [ ] Review Stripe revenue and payouts
- [ ] Update WordPress core and plugins
- [ ] Rotate SSH keys if needed
- [ ] Review and optimize VM resource allocation
- [ ] Check domain renewal dates

---

**Maintained By**: AI Infrastructure Team  
**Project Owner**: MatoTeziTanka  
**Repository**: https://github.com/MatoTeziTanka/PassiveIncome




