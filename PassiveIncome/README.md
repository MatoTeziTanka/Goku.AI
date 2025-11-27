# 💰 Passive Income Projects

**Repository**: https://github.com/MatoTeziTanka/PassiveIncome  
**Owner**: MatoTeziTanka  
**Purpose**: Documentation and AI collaboration hub for passive income infrastructure

---

## 🎯 Mission

This repository documents and coordinates multiple passive income projects running on a Dell PowerEdge server with Proxmox virtualization. Each project is designed to generate recurring revenue through subscriptions, hosting services, or API access.

**Revenue Goal**: $500+/month by Q1 2026

---

## 📁 Project Structure

```
PassiveIncome/
├── WordPress-VM/              ✅ Production (Test Mode)
│   ├── AI-COLLABORATION.md    → Primary AI coordination document
│   ├── vm-150-wordpress-config.md
│   ├── wordpress-production-hardening.md
│   └── wordpress-stripe-integration-complete.md
│
├── Discord-Bot-Services/      🔄 Planning Phase
│   └── AI-COLLABORATION.md    → Primary AI coordination document
│
├── Game-Server-Hosting/       🔄 Planning Phase
│   └── AI-COLLABORATION.md    → Primary AI coordination document
│
├── API-Services/              🔄 Planning Phase
│   └── AI-COLLABORATION.md    → Primary AI coordination document
│
├── INFRASTRUCTURE.md          → Server, network, and VM details
├── PORT-ALLOCATION.md         → Port mapping reference
└── README.md                  → This file
```

---

## 🚀 Active Projects

### 1. WordPress VM (VM150) - ✅ Production
**Status**: Live in test mode  
**URL**: https://wp.lightspeedup.com  
**Revenue Model**: Subscription-based infrastructure services ($9-$29/mo)

**Current Features**:
- Three enterprise-focused homepage variants (Lightspeed Enterprise, Vector Edge, Nova Scale)
- Stripe payment integration (test mode)
- Cloudflare Tunnel with HTTPS
- Nginx reverse proxy with security headers
- WordPress + Blocksy theme
- 9 active plugins (Security, SEO, Caching, Payments)

**Next Steps**:
- Test Stripe transaction with test card
- Add logo and branding
- Automated backups
- Transition to live Stripe keys

📄 **AI Collaboration Document**: `WordPress-VM/AI-COLLABORATION.md`

---

### 2. Discord Bot Services (VM160) - 🔄 Planning
**Status**: Planning phase  
**Revenue Model**: Premium bot subscriptions, custom features

**Potential Bots**:
- Server management and moderation
- Custom economy systems
- 24/7 music streaming
- Ticket support systems
- Verification and captcha

**Next Steps**:
- Define bot feature set
- Choose framework (Discord.js or discord.py)
- Design revenue tiers
- Set up development environment

📄 **AI Collaboration Document**: `Discord-Bot-Services/AI-COLLABORATION.md`

---

### 3. Game Server Hosting (VM170) - 🔄 Planning
**Status**: Planning phase  
**Revenue Model**: Per-slot or per-server pricing

**Potential Games**:
- Minecraft (Java/Bedrock, modpacks)
- Rust
- ARK: Survival Evolved
- Valheim
- Terraria
- 7 Days to Die

**Next Steps**:
- Choose first game to host (recommend Minecraft)
- Install control panel (Pterodactyl or AMP)
- Configure backup automation
- Design hosting packages

📄 **AI Collaboration Document**: `Game-Server-Hosting/AI-COLLABORATION.md`

---

### 4. API Services (VM180) - 🔄 Planning
**Status**: Planning phase  
**Revenue Model**: Tiered API access (requests/day or features)

**Potential APIs**:
- Data transformation (JSON, XML, CSV)
- Image processing (resize, compress, watermark)
- Webhook relay and transformation
- QR code generation
- Text processing (sentiment, summarization)
- URL shortener with analytics

**Next Steps**:
- Define API use cases
- Choose framework (Express.js, FastAPI, Flask)
- Design authentication and rate limiting
- Create API documentation (Swagger)

📄 **AI Collaboration Document**: `API-Services/AI-COLLABORATION.md`

---

## 🏗️ Infrastructure

### Physical Server
- **Dell PowerEdge** running Proxmox VE
- **Hypervisor**: <PROXMOX_IP> (See credentials.json)
- **Network**: <LOCAL_NETWORK_CIDR> (See credentials.json)

### Virtual Machines
| VM ID | Name | IP | Purpose | Status |
|-------|------|-----|---------|--------|
| VM101 | management-ai-assistant-1 | <VM101_IP> (See credentials.json) | AI workspace, Git repos | ✅ Active |
| VM120 | reverse-proxy-1 | <VM120_IP> (See credentials.json) | Nginx, Cloudflare Tunnel | ✅ Active |
| VM150 | wordpress-1 | <VM150_IP> (See credentials.json) | WordPress passive income | ✅ Production |
| VM160 | discord-bot-1 (planned) | TBD | Discord bot services | ⏭️ Planned |
| VM170 | game-server-1 (planned) | TBD | Game server hosting | ⏭️ Planned |
| VM180 | api-services-1 (planned) | TBD | API services | ⏭️ Planned |

### Domain & DNS
- **Primary Domain**: lightspeedup.com (Cloudflare DNS)
- **Active Subdomains**: wp.lightspeedup.com
- **SSL/HTTPS**: Cloudflare Tunnel

### Security
- Cloudflare DDoS protection and WAF
- Nginx reverse proxy with security headers
- UFW firewall on all VMs
- SSH key-based authentication
- Wordfence security suite (WordPress)

📄 **Full Details**: `INFRASTRUCTURE.md`

---

## 💳 Payment Processing

### Stripe Integration
- **Account**: sethpizzaboy@gmail.com
- **Current Mode**: TEST (Sandbox)
- **Active Integration**: WordPress Stripe Payments plugin

### Current Pricing (WordPress VM)
- **Starter Plan**: $9/month
- **Business Plan**: $29/month

### Test Card
```
Card: 4242 4242 4242 4242
Expiry: 12/26
CVC: 123
ZIP: 12345
```

---

## 🤖 AI Collaboration System

### Purpose
Each project folder contains an `AI-COLLABORATION.md` document that serves as the **central knowledge base** for AI assistants working on that project.

### What's in an AI Collaboration Document?
1. **Project Mission** - Clear goals and revenue model
2. **Current Status** - What's live, what's planned
3. **Technical Architecture** - Infrastructure, frameworks, services
4. **Security Configuration** - Authentication, rate limiting, best practices
5. **Common AI Tasks** - Code examples and commands
6. **Priority Checklist** - What needs to be done next
7. **Change Log** - History of major updates

### How AI Assistants Should Use These Documents

#### ✅ DO:
- **Read the AI-COLLABORATION.md FIRST** before making any changes
- **Update the document** after completing work
- **Document new configurations** (plugins, services, credentials)
- **Add to the change log** with dates
- **Follow the security best practices** outlined
- **Test changes before deploying** to production

#### ❌ DON'T:
- Make changes without reading current status
- Forget to update the document after work
- Commit sensitive credentials to git
- Break production services without backups
- Ignore security warnings in the document

### Example AI Workflow
```
1. User: "Add a new feature to WordPress"
2. AI reads: WordPress-VM/AI-COLLABORATION.md
3. AI checks: Current status, active plugins, priorities
4. AI implements: The feature using documented patterns
5. AI updates: The AI-COLLABORATION.md with changes
6. AI commits: Changes to git with clear message
7. AI verifies: Site still works correctly
```

---

## 📊 Revenue Tracking

### Current Status (October 31, 2025)
| Project | Status | Monthly Revenue | Target Revenue |
|---------|--------|----------------|----------------|
| WordPress VM | ✅ Production (Test) | $0 | $100+ |
| Discord Bots | 🔄 Planning | $0 | $150+ |
| Game Servers | 🔄 Planning | $0 | $200+ |
| API Services | 🔄 Planning | $0 | $100+ |
| **TOTAL** | | **$0** | **$550+** |

### Revenue Milestones
- [x] Set up first revenue stream infrastructure (WordPress)
- [ ] Complete first real transaction ($1+)
- [ ] Reach $10/month recurring revenue
- [ ] Reach $100/month recurring revenue
- [ ] Reach $500/month recurring revenue
- [ ] Launch second revenue stream (Discord/Game/API)
- [ ] Reach $1000/month recurring revenue

---

## 🔧 Quick Start for AI Assistants

### Working on WordPress VM
```bash
# Read the collaboration document
cat WordPress-VM/AI-COLLABORATION.md

# SSH to WordPress VM
ssh wp1@<VM150_IP>  # See credentials.json for actual IP

# Common commands documented in the collaboration file
```

### Working on Other Projects
```bash
# Read the collaboration document for that project
cat Discord-Bot-Services/AI-COLLABORATION.md
cat Game-Server-Hosting/AI-COLLABORATION.md
cat API-Services/AI-COLLABORATION.md

# Follow the documented setup and deployment steps
```

### Updating Documentation
```bash
# Make changes to relevant files
nano WordPress-VM/AI-COLLABORATION.md

# Commit with clear message
git add .
git commit -m "Updated WordPress status after deploying new feature"
git push origin main
```

---

## 📚 Important Documents

### Infrastructure References
- `INFRASTRUCTURE.md` - Complete server, VM, and network details
- `PORT-ALLOCATION.md` - Port mapping and firewall rules

### Project-Specific Documentation
- `WordPress-VM/AI-COLLABORATION.md` - WordPress project coordination
- `WordPress-VM/wordpress-stripe-integration-complete.md` - Full Stripe setup guide
- `Discord-Bot-Services/AI-COLLABORATION.md` - Discord bot coordination
- `Game-Server-Hosting/AI-COLLABORATION.md` - Game server coordination
- `API-Services/AI-COLLABORATION.md` - API services coordination

---

## 🆘 Getting Help

### For AI Assistants
1. Read the relevant `AI-COLLABORATION.md` document
2. Check `INFRASTRUCTURE.md` for server/network details
3. Review recent git commits for context
4. Check the project's current status section

### For Humans
1. Review this README for project overview
2. Check individual project folders for details
3. Refer to `INFRASTRUCTURE.md` for technical specs
4. Contact: MatoTeziTanka (GitHub)

---

## 🔐 Security Notes

### Never Commit to Git:
- Real API keys (Stripe, Cloudflare, etc.)
- Database passwords
- SSH private keys
- Real customer data

### Use Instead:
- Test/sandbox API keys in documentation
- Environment variables for production secrets
- SSH keys stored locally on VMs
- Placeholder data for examples

---

## 📈 Success Metrics

### Technical KPIs
- Uptime: 99.9%+ for all production services
- Response Time: <500ms for web pages
- Backup Success Rate: 100%
- Security Incidents: 0

### Business KPIs
- Monthly Recurring Revenue (MRR): $500+ target
- Customer Acquisition Cost (CAC): <$20
- Customer Lifetime Value (CLV): >$100
- Churn Rate: <5% monthly

---

## 📝 Contributing

This is a private repository for passive income projects. All contributions should:
1. Update relevant AI-COLLABORATION.md documents
2. Follow security best practices
3. Include clear commit messages
4. Test changes before committing
5. Document new features or configurations

---

## 📅 Last Updated

**Date**: October 31, 2025  
**By**: AI Infrastructure Team  
**Major Changes**: 
- Created repository structure
- Moved WordPress project from Dell-Server-Roadmap
- Created AI collaboration documents for all projects
- Documented infrastructure and port allocations

---

**Let's build passive income together! 🚀💰**




