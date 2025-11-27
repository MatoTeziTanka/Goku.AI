<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Game Server Hosting - Version Control & Change Log

**Project**: Game Server Hosting for Passive Income  
**Repository**: https://github.com/MatoTeziTanka/PassiveIncome  
**Current Version**: v0.1.0  
**Last Updated**: October 31, 2025  
**Status**: Planning Phase - Not Yet Started

---

## 📌 Version Numbering System

### Semantic Versioning: `vMAJOR.MINOR.PATCH`

- **MAJOR** (v1.0.0, v2.0.0): Complete AI collaboration session finished, ready for next major phase
- **MINOR** (v0.1.0, v0.2.0): After each AI assistant response with significant changes
- **PATCH** (v0.1.1, v0.1.2): Small corrections, typo fixes, minor tweaks (no AI collab needed)

### Version Incrementing Rules

| Change Type | Version Bump | Example | When to Use |
|-------------|--------------|---------|-------------|
| New AI collaboration session complete | MAJOR (v1.0.0) | First game server deployed | After completing a full objective |
| AI makes significant changes | MINOR (v0.2.0) | Control panel installed | After each AI response |
| Human makes small fix | PATCH (v0.1.1) | Fixed server config | Quick corrections |
| Critical hotfix | PATCH (v0.1.1) | Server crashed, emergency fix | Emergency fixes |

---

## 📚 Current Version: v0.1.0

### Version History

#### **v0.1.0** - Project Initialization (Oct 31, 2025)
**Status**: Planning phase  
**AI Session**: Dell Server Roadmap → PassiveIncome migration  
**Objective**: Create project structure and documentation framework

**Changes**:
- ✅ Project folder created in PassiveIncome repository
- ✅ AI-COLLABORATION.md created with project guidelines
- ✅ VERSION-CONTROL.md created (this file)
- ✅ Revenue target set: $400-800/mo
- ✅ Primary game identified: Minecraft (Java Edition)
- ✅ Control panel proposed: Pterodactyl Panel
- ✅ Hosting tiers defined: Bronze, Silver, Gold, Diamond

**Files Created**:
- `/home/mgmt1/GitHub/PassiveIncome/Game-Server-Hosting/AI-COLLABORATION.md`
- `/home/mgmt1/GitHub/PassiveIncome/Game-Server-Hosting/VERSION-CONTROL.md`

**Infrastructure Status**:
- ❌ No VM allocated yet (likely VM170)
- ❌ No control panel installed
- ❌ No game servers deployed
- ❌ No backup system configured
- ❌ No customer portal set up

**Revenue Status**:
- Target: $400-800/mo
- Current: $0/mo
- Pricing: $12-96/mo per Minecraft server

**Testing Status**:
- ⚠️ No servers created yet
- ⚠️ No control panel tested
- ⚠️ No backups tested

**Known Issues**:
- None (project not started)

**Next Phase**: Control panel installation and first Minecraft server (v1.0.0)

---

## 🎯 Version Roadmap

### **v1.0.0** - Pterodactyl Panel + First Minecraft Server (Target: Week 2-3)
**Objective**: Install control panel and deploy first Minecraft server

**Planned Changes**:
- [ ] Allocate VM170 (Ubuntu 24.04 LTS, 16GB RAM, 6 CPU cores, 200GB SSD)
- [ ] Install Pterodactyl Panel (control panel for game servers)
- [ ] Configure Pterodactyl:
  - Web interface
  - Wings (server daemon)
  - MySQL database
  - Redis cache
  - Nginx reverse proxy
- [ ] Create first Minecraft server (Bronze tier):
  - Paper 1.20.1 (optimized Minecraft server)
  - 2GB RAM allocation
  - 10 player slots
  - Daily backups
- [ ] Set up automatic backups (rsnapshot or Restic)
- [ ] Configure UFW firewall (25565 for Minecraft, 80/443 for panel)
- [ ] Create server templates for easy deployment
- [ ] Test server performance and stability
- [ ] Document server creation process

**Files to Create**:
```
Game-Server-Hosting/
├── pterodactyl/
│   ├── panel-setup.sh         # Installation script
│   ├── wings-setup.sh          # Wings daemon setup
│   └── config/
│       ├── panel.conf          # Nginx config
│       └── wings.yml           # Wings config
├── minecraft/
│   ├── paper-1.20.1.jar        # Server JAR
│   ├── server.properties       # Default config
│   ├── spigot.yml              # Spigot settings
│   └── paper.yml               # Paper settings
├── backups/
│   └── backup-script.sh        # Automated backup
└── docs/
    └── server-creation-guide.md
```

**Infrastructure to Set Up**:
- **VM170 Specifications**:
  - OS: Ubuntu 24.04 LTS
  - RAM: 16GB (support multiple game servers)
  - CPU: 6 cores
  - Disk: 200GB SSD
  - IP: <VM170_IP>
  - User: gamehost1

**Scripts to Execute**:
```bash
# Create VM170 on Proxmox
ssh root@<PROXMOX_IP>
qm create 170 --name game-server-1 --memory 16384 --cores 6 --scsihw virtio-scsi-pci

# Install Pterodactyl Panel
ssh gamehost1@<VM170_IP>
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y software-properties-common curl apt-transport-https ca-certificates gnupg
sudo add-apt-repository -y ppa:ondrej/php
curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash

# Install packages
sudo apt install -y php8.1 php8.1-{cli,gd,mysql,pdo,mbstring,tokenizer,bcmath,xml,fpm,curl,zip} mariadb-server nginx tar unzip git redis-server

# Install Composer
curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer

# Download and install Pterodactyl Panel
cd /var/www
sudo curl -Lo panel.tar.gz https://github.com/pterodactyl/panel/releases/latest/download/panel.tar.gz
sudo tar -xzvf panel.tar.gz
sudo chmod -R 755 storage/* bootstrap/cache/

# Configure database
sudo mysql -u root -p
CREATE DATABASE panel;
CREATE USER 'pterodactyl'@'127.0.0.1' IDENTIFIED BY 'SECURE_PASSWORD';
GRANT ALL PRIVILEGES ON panel.* TO 'pterodactyl'@'127.0.0.1' WITH GRANT OPTION;
exit

# Install Panel
cd /var/www/pterodactyl
sudo composer install --no-dev --optimize-autoloader
sudo php artisan key:generate --force
sudo php artisan p:environment:setup
sudo php artisan p:environment:database
sudo php artisan migrate --seed --force
sudo php artisan p:user:make  # Create admin user

# Install Wings (server daemon)
curl -sSL https://get.docker.com/ | CHANNEL=stable bash
sudo systemctl enable --now docker

sudo mkdir -p /etc/pterodactyl
curl -L -o /usr/local/bin/wings "https://github.com/pterodactyl/wings/releases/latest/download/wings_linux_$([[ "$(uname -m)" == "x86_64" ]] && echo "amd64" || echo "arm64")"
sudo chmod u+x /usr/local/bin/wings

# Create first Minecraft server
# (Done through Pterodactyl web interface)
```

**Success Criteria**:
- ✅ Pterodactyl Panel accessible at https://game.lightspeedup.com
- ✅ Wings daemon running and connected
- ✅ First Minecraft server created and online
- ✅ Players can connect to server
- ✅ Backups running daily
- ✅ Server performance acceptable (TPS > 19)

**Revenue Target**: $0/mo (test server, not for sale yet)

**Target Date**: November 10-15, 2025

---

### **v2.0.0** - Launch Bronze/Silver/Gold Tiers + Stripe Integration (Target: Week 3-4)
**Objective**: Create hosting packages and integrate payment processing

**Planned Changes**:
- [ ] Create hosting tier templates in Pterodactyl:
  - **Bronze**: 2GB RAM, 10 slots, $12/mo
  - **Silver**: 4GB RAM, 25 slots, $24/mo
  - **Gold**: 8GB RAM, 50 slots, $48/mo
  - **Diamond**: 16GB RAM, 100 slots, $96/mo
- [ ] Integrate Stripe payment processing:
  - Create Stripe products for each tier
  - Build customer signup flow
  - Auto-provision servers after payment
  - Handle subscription renewals
  - Manage cancellations (grace period + deletion)
- [ ] Create customer portal:
  - View server status
  - Start/stop/restart server
  - Access console
  - View backups
  - Upgrade/downgrade plan
  - Manage billing
- [ ] Set up automated provisioning (API integration)
- [ ] Configure email notifications (server ready, payment due, etc.)
- [ ] Create landing page showcasing plans
- [ ] Test full customer journey (signup → payment → server → usage)

**Files to Create**:
```
Game-Server-Hosting/
├── website/
│   ├── index.html              # Landing page
│   ├── pricing.html            # Pricing tiers
│   ├── signup.php              # Customer signup
│   └── portal/
│       ├── dashboard.php       # Customer portal
│       └── billing.php         # Billing management
├── provisioning/
│   ├── stripe-webhook.php      # Handle Stripe events
│   ├── create-server.php       # Auto-provision server
│   └── delete-server.php       # Handle cancellations
└── email-templates/
    ├── server-ready.html
    ├── payment-reminder.html
    └── cancellation.html
```

**Stripe Configuration**:
```bash
# Create Stripe products
# Bronze: $12/mo (product_bronze)
# Silver: $24/mo (product_silver)
# Gold: $48/mo (product_gold)
# Diamond: $96/mo (product_diamond)

# Webhook URL: https://game.lightspeedup.com/webhook/stripe
# Events to listen:
# - customer.subscription.created
# - customer.subscription.updated
# - customer.subscription.deleted
# - invoice.payment_succeeded
# - invoice.payment_failed
```

**Success Criteria**:
- ✅ All four tiers available for purchase
- ✅ Payment flow works (test and live)
- ✅ Servers auto-provision after payment
- ✅ Customer portal functional
- ✅ First paying customer acquired
- ✅ Subscription renewals handled automatically

**Revenue Target**: $100-400/mo (5-15 servers @ $12-48/mo)

**Target Date**: November 20-30, 2025

---

### **v3.0.0** - Modpack Hosting + Scale (Target: Month 2)
**Objective**: Add modpack support and scale to 20+ customers

**Planned Changes**:
- [ ] Add modpack support:
  - All The Mods 9 (ATM9)
  - Feed The Beast (FTB)
  - Vault Hunters
  - SkyFactory
  - RLCraft
- [ ] Create modpack tier pricing ($36-60/mo, higher RAM requirements)
- [ ] Optimize server performance (aikar's flags, configs)
- [ ] Add plugin support (Essentials, WorldEdit, GriefPrevention)
- [ ] Create one-click modpack installer
- [ ] Market to modded Minecraft communities (r/feedthebeast, r/ATM9)
- [ ] Partner with 1-2 Minecraft YouTubers (free server for review)

**Success Criteria**:
- ✅ 5+ modpacks available
- ✅ Modpack servers perform well
- ✅ 10+ modpack customers acquired
- ✅ 20-25 total customers
- ✅ $400-600/mo MRR

**Revenue Target**: $400-600/mo (20-25 servers, mix of vanilla and modded)

**Target Date**: December 2025

---

### **v4.0.0** - Multi-Game Support (Target: Month 3)
**Objective**: Add Rust, ARK, Valheim support to diversify offerings

**Planned Changes**:
- [ ] Add Rust server support:
  - Install Rust egg in Pterodactyl
  - Create Rust hosting tiers ($48-96/mo)
  - Configure Rust-specific features (wipes, blueprints, etc.)
- [ ] Add ARK: Survival Evolved support:
  - Install ARK egg in Pterodactyl
  - Create ARK hosting tiers ($48-96/mo)
  - Support mods and custom maps
- [ ] Add Valheim support:
  - Install Valheim egg
  - Create Valheim hosting tiers ($24-48/mo)
  - Support world saves and backups
- [ ] Expand marketing to multi-game communities
- [ ] Create game-specific landing pages

**Success Criteria**:
- ✅ 3 games supported (Minecraft, Rust, ARK/Valheim)
- ✅ 5+ customers on non-Minecraft games
- ✅ 30-40 total customers
- ✅ $800-1,200/mo MRR

**Revenue Target**: $800-1,200/mo

**Target Date**: January 2026

---

### **v5.0.0** - Hit $1.5K/mo MRR (Target: Month 4)
**Objective**: Scale to $1,500/mo monthly recurring revenue

**Planned Changes**:
- [ ] Scale Minecraft hosting to 30-35 servers ($500-800/mo)
- [ ] Scale Rust hosting to 10-15 servers ($500-700/mo)
- [ ] Scale ARK/Valheim to 5-10 servers ($200-400/mo)
- [ ] Add dedicated server option ($200-500/mo)
- [ ] Implement referral program (1 month free)
- [ ] Create affiliate program (20% commission)
- [ ] Optimize churn (improve support, add features)

**Success Criteria**:
- ✅ $1,500+/mo MRR from game hosting
- ✅ 50-60 total customers
- ✅ <5% monthly churn
- ✅ 95%+ uptime across all servers

**Revenue Target**: $1,500-2,000/mo

**Target Date**: February 2026

---

## 📋 Change Log Template

Use this template when creating version updates:

```markdown
### **vX.Y.Z** - [Title] ([Date])
**Status**: [In Progress / Completed / Failed]  
**AI Session**: [Session description]  
**Objective**: [What are we trying to accomplish?]

**Changes**:
- ✅ [Completed change 1]
- ✅ [Completed change 2]
- ⚠️ [Partial change 3]
- ❌ [Failed change 4]

**Files Created**:
- [path/to/new/file1.ext]

**Files Modified**:
- [path/to/modified/file1.ext]

**Scripts Executed**:
```bash
# Script description
command here
```

**Issues Resolved**:
- ❌ [Issue] → [Solution]

**Issues Encountered**:
- ⚠️ [Issue] → [Workaround]

**Testing Status**:
- ✅ [Test 1]: Passed
- ⚠️ [Test 2]: Needs verification

**Revenue Impact**:
- Previous MRR: $X
- Current MRR: $Y
- Change: +$Z (+X%)

**Next Phase**: [What comes next]
```

---

## 🔍 How to Use This Document

### For AI Assistants:
1. **Read current version section first** (currently v0.1.0 - Planning)
2. **Check "Version Roadmap"** to see infrastructure requirements
3. **Review "Planned Changes"** for v1.0.0 (Pterodactyl + first server)
4. **Execute tasks** systematically
5. **Update this document** after completing work:
   - Increment version number
   - Add new version section
   - Document all changes
   - Update revenue tracking
6. **Commit changes** with version number in message

### For Humans:
1. **Check current version** (v0.1.0 = Planning)
2. **Review roadmap** to understand path to $800/mo
3. **Start new AI chat** with: "Read Game-Server-Hosting/VERSION-CONTROL.md and let's build v1.0.0"
4. **Update after each milestone**

---

## 📊 Progress Tracker

### Overall Project Status

| Phase | Version | Status | Completion | Revenue | Target Date |
|-------|---------|--------|------------|---------|-------------|
| Planning | v0.1.0 | ✅ Complete | 100% | $0 | Oct 31, 2025 |
| Control Panel + First Server | v1.0.0 | ⏭️ Pending | 0% | $0 | Nov 10-15, 2025 |
| Hosting Tiers + Stripe | v2.0.0 | ⏭️ Planned | 0% | $100-400 | Nov 20-30, 2025 |
| Modpack Support | v3.0.0 | ⏭️ Planned | 0% | $400-600 | Dec 2025 |
| Multi-Game Support | v4.0.0 | ⏭️ Planned | 0% | $800-1,200 | Jan 2026 |
| Hit $1.5K/mo | v5.0.0 | ⏭️ Planned | 0% | $1,500+ | Feb 2026 |

### Current Sprint (v0.1.0 → v1.0.0)

| Task | Priority | Status | Assignee | Estimated Time |
|------|----------|--------|----------|----------------|
| Allocate VM170 (16GB RAM) | ⚡ Critical | ⏭️ Pending | AI | 30 min |
| Install Pterodactyl Panel | ⚡ Critical | ⏭️ Pending | AI | 2-3 hours |
| Install Wings daemon | ⚡ Critical | ⏭️ Pending | AI | 1 hour |
| Configure Nginx reverse proxy | 📋 High | ⏭️ Pending | AI | 30 min |
| Create first Minecraft server | 📋 High | ⏭️ Pending | AI | 1 hour |
| Set up automated backups | 📋 High | ⏭️ Pending | AI | 1 hour |
| Configure UFW firewall | 📋 High | ⏭️ Pending | AI | 30 min |
| Test server performance | 📋 Medium | ⏭️ Pending | Human | 1 hour |
| Document process | 📋 Medium | ⏭️ Pending | AI | 1 hour |

**Total Estimated Time**: 8-10 hours of focused work

---

## 🐛 Issues & Tickets

### Open Issues

#### Issue #001 - Control Panel Choice: Pterodactyl vs Alternatives
**Priority**: ⚡ Critical  
**Status**: Open  
**Created**: Oct 31, 2025  
**Assignee**: AI + Human

**Description**:
Need to confirm Pterodactyl Panel as the control panel choice.

**Alternatives Considered**:
1. **Pterodactyl Panel** (Recommended)
   - Pros: Free, modern UI, Docker-based, active development
   - Cons: Requires learning curve, Docker dependency
2. **AMP (CubeCoders)**
   - Pros: Very user-friendly, great support
   - Cons: Paid license ($10/month), less flexible
3. **Multicraft**
   - Pros: Mature, stable
   - Cons: Dated UI, less feature-rich

**Recommendation**: Pterodactyl Panel (free, modern, scalable)

**Resolution Plan**:
- User confirms or AI proceeds with Pterodactyl
- Document in v1.0.0

---

#### Issue #002 - Server Resource Allocation
**Priority**: 📋 Medium  
**Status**: Open  
**Created**: Oct 31, 2025  
**Assignee**: AI

**Description**:
VM170 needs 16GB RAM to support multiple game servers. Confirm Dell server has capacity.

**Current Proxmox Allocation**:
- VM101: 4GB RAM
- VM120: 2GB RAM
- VM150: 4GB RAM
- VM160 (planned Discord): 2GB RAM
- VM170 (planned Games): 16GB RAM
- **Total**: 28GB RAM

**Dell Server Capacity**: Unknown (need to verify)

**Options if Insufficient RAM**:
1. Upgrade Dell server RAM
2. Reduce VM170 to 12GB (support fewer servers)
3. Use external VPS for game hosting (defeats purpose)

**Resolution Plan**:
- Check Dell server specs
- Allocate appropriate RAM
- Document in INFRASTRUCTURE.md

---

### Closed Issues

None yet (project not started)

---

## 💡 Ideas & Future Enhancements

### High-Priority Ideas
- [ ] **Dedicated Servers** - Full dedicated box for $200-500/mo
- [ ] **DDoS Protection** - Partner with OVH or Cloudflare Spectrum
- [ ] **Control Panel White-Label** - Rebrand Pterodactyl for agencies
- [ ] **Managed Services** - Full server management for premium
- [ ] **Server Migration Service** - Import from other hosts ($49 fee)

### Medium-Priority Ideas
- [ ] **Custom JARs** - Spigot, Paper, Purpur, Fabric, Forge
- [ ] **Automatic Plugin Installer** - One-click popular plugins
- [ ] **Performance Monitoring** - TPS tracking, lag detection
- [ ] **Server Templates** - Pre-configured servers (PvP, Survival, etc.)
- [ ] **Discord Integration** - Bot for server management

### Low-Priority Ideas
- [ ] **Mobile App** - Manage servers from phone
- [ ] **API Access** - Programmatic server management
- [ ] **Reseller Program** - Let others resell your hosting
- [ ] **Free Trial** - 24-hour free server trial
- [ ] **Seasonal Promotions** - Black Friday, holiday deals

---

## 💰 Revenue Tracking

### Revenue Milestones

- [ ] Pterodactyl Panel installed
- [ ] First Minecraft server created
- [ ] First test player connects
- [ ] First paying customer ($12/mo)
- [ ] 5 paying customers ($60-200/mo)
- [ ] 10 paying customers ($120-400/mo)
- [ ] $500/mo MRR
- [ ] 20 paying customers ($400-600/mo)
- [ ] $800/mo MRR (Primary goal)
- [ ] $1,000/mo MRR
- [ ] $1,500/mo MRR (Stretch goal)

### Target Pricing

**Minecraft (Vanilla/Paper)**:
- Bronze: $12/mo (2GB, 10 slots) → 15 customers = $180/mo
- Silver: $24/mo (4GB, 25 slots) → 10 customers = $240/mo
- Gold: $48/mo (8GB, 50 slots) → 5 customers = $240/mo
- Diamond: $96/mo (16GB, 100 slots) → 2 customers = $192/mo

**Minecraft (Modpacks)**:
- Modded Bronze: $36/mo (6GB) → 5 customers = $180/mo
- Modded Silver: $60/mo (10GB) → 3 customers = $180/mo

**Other Games**:
- Rust: $48/mo → 2 customers = $96/mo
- ARK: $48/mo → 2 customers = $96/mo
- Valheim: $24/mo → 2 customers = $48/mo

**Total Target**: $1,452/mo from 46 game servers

---

## 🔗 Related Documentation

### In This Repository
- `AI-COLLABORATION.md` - Main AI coordination document
- `VERSION-CONTROL.md` - This file

### Parent Repository
- `../REVENUE-STRATEGY.md` - Overall $2K/mo strategy
- `../INFRASTRUCTURE.md` - Server details
- `../PORT-ALLOCATION.md` - Port mapping
- `../README.md` - Project overview

### External Resources
- [Pterodactyl Documentation](https://pterodactyl.io/project/introduction.html)
- [Paper Minecraft Server](https://papermc.io/)
- [Aikar's Flags (Performance)](https://aikar.co/2018/07/02/tuning-the-jvm-g1gc-garbage-collector-flags-for-minecraft/)
- [Minecraft Server Optimization](https://github.com/YouHaveTrouble/minecraft-optimization)

---

## 🚀 Quick Start Guide

### Starting Your Game Server Hosting Chat

**Opening Message**:
```
I want to build game server hosting for passive income.

Current version: v0.1.0 (Planning complete)
Next milestone: v1.0.0 (Install Pterodactyl + first Minecraft server)

Read: /home/mgmt1/GitHub/PassiveIncome/Game-Server-Hosting/VERSION-CONTROL.md

Help me set up VM170 with Pterodactyl Panel and deploy first Minecraft server.
Revenue goal: $800+/mo within 3-4 months.

Let's start!
```

### What AI Will Do
1. Read VERSION-CONTROL.md
2. See project is in planning (v0.1.0)
3. Understand goal: Minecraft hosting, $800/mo target
4. Allocate VM170 (16GB RAM)
5. Install Pterodactyl Panel
6. Deploy first Minecraft server (v1.0.0)

---

**Last Updated**: October 31, 2025  
**Current Version**: v0.1.0 (Planning Complete)  
**Next Version**: v1.0.0 (Pterodactyl + First Server - Week 2-3)  
**Maintained By**: AI Infrastructure Team + Human Owner  
**Repository**: https://github.com/MatoTeziTanka/PassiveIncome




