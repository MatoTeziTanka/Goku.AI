# 🚀 Building $2K/mo Passive Income with Self-Hosted Services

**Status**: Building in Public 🔨  
**Current MRR**: $0 → Target: $2,000+/mo  
**Timeline**: Q4 2025 - Q1 2026  
**Last Updated**: November 1, 2025

[![Building in Public](https://img.shields.io/badge/Building-In%20Public-blue)](https://github.com/MatoTeziTanka/PassiveIncome)
[![Server Status](https://img.shields.io/badge/Server-Online-success)](.)
[![Revenue](https://img.shields.io/badge/MRR-$0%20%E2%86%92%20$2K-orange)](.)

---

## 👋 What is This?

I'm building 4 passive income services on a **Dell PowerEdge home server** and documenting everything publicly:

1. **WordPress Hosting** - Enterprise features at fair prices ($29-199/mo)
2. **Discord Bots** - Moderation & automation ($4.99-9.99/mo)
3. **Game Server Hosting** - Minecraft, Rust, ARK ($12-96/mo)
4. **API Services** - Screenshot, PDF, image optimization ($9-199/mo)

**Why share this?** Because the internet helped me learn - time to give back. This repo contains my infrastructure, documentation, lessons learned, and real revenue numbers.

---

## 📊 Current Status (November 2025)

| Service | Status | MRR | Progress |
|---------|--------|-----|----------|
| WordPress Hosting | ✅ Test Mode | $0 | 90% complete |
| Discord Bots | 🔄 Development | $0 | 40% complete |
| Game Servers | 🔄 Planning | $0 | 20% complete |
| API Services | 🔄 Planning | $0 | 15% complete |
| **TOTAL** | | **$0** | **Target: $2K/mo by Q1 2026** |

---

## 🏗️ Infrastructure

### Physical Setup
- **Server**: Dell PowerEdge (bare metal, no cloud!)
- **Virtualization**: Proxmox VE
- **Network**: 192.168.X.X (internal)
- **Public Access**: Cloudflare Tunnel (no port forwarding needed)
- **Domain**: lightspeedup.com

### Active VMs
| VM | Purpose | RAM | Status |
|----|---------|-----|--------|
| VM101 | Management & AI workspace | 8GB | ✅ Active |
| VM120 | Nginx reverse proxy | 4GB | ✅ Active |
| VM150 | WordPress production | 8GB | ✅ Test Mode |
| VM160 | Discord bots (planned) | 4GB | 🔄 Planned |
| VM170 | Game servers (planned) | 16GB | 🔄 Planned |
| VM180 | API services (planned) | 8GB | 🔄 Planned |

### Tech Stack
- **Web**: Nginx, Cloudflare, WordPress
- **Database**: MySQL 8.0
- **Caching**: Redis
- **Security**: Wordfence, UFW, Cloudflare WAF
- **Monitoring**: 24/7 uptime checks
- **Backups**: Automated daily backups

---

## 📁 Repository Structure

```
PassiveIncome/
├── WordPress-VM/              ✅ In Production (Test Mode)
│   ├── AI-COLLABORATION.md    → Primary documentation
│   ├── STRIPE-SETUP-GUIDE.md  → Payment integration
│   └── VERSION-CONTROL.md     → Change tracking
│
├── Discord-Bot-Services/      🔄 In Development
│   └── AI-COLLABORATION.md    → Bot architecture plans
│
├── Game-Server-Hosting/       🔄 Planning Phase
│   └── AI-COLLABORATION.md    → Infrastructure design
│
├── API-Services/              🔄 Planning Phase
│   └── AI-COLLABORATION.md    → API specifications
│
├── INFRASTRUCTURE.md          → Server & network details
├── PORT-ALLOCATION.md         → Port mapping reference
├── REVENUE-STRATEGY.md        → Business model & pricing
└── README.md                  → This file
```

---

## 💰 Business Model

### Revenue Streams

**1. WordPress Hosting**
- **Starter**: $29/mo (5 projects, 50GB)
- **Business**: $79/mo (25 projects, 250GB)
- **Enterprise**: $199/mo (unlimited, 1TB)
- **Target**: $500/mo MRR

**2. Discord Bots**
- **Free**: Basic moderation
- **Premium**: $4.99/mo per server
- **Enterprise**: Custom pricing
- **Target**: $600/mo MRR

**3. Game Server Hosting**
- **Minecraft Bronze**: $12/mo (2GB, 10 slots)
- **Minecraft Silver**: $24/mo (4GB, 25 slots)
- **Minecraft Gold**: $48/mo (8GB, 50 slots)
- **Other Games**: $24-96/mo
- **Target**: $800/mo MRR

**4. API Services**
- **Free**: 100 requests/day
- **Hobby**: $9/mo (5K requests/day)
- **Business**: $49/mo (50K requests/day)
- **Enterprise**: $199/mo (unlimited)
- **Target**: $400/mo MRR

**Total Target**: $2,300/mo MRR by Q1 2026

---

## 🎯 Why This Will Work

### Competitive Advantages
1. **Lower Costs**: Bare metal = no cloud markup (60-80% cheaper)
2. **Better Performance**: Dedicated hardware vs shared hosting
3. **Transparent Pricing**: No hidden fees or gotchas
4. **Personal Touch**: Direct support from the builder
5. **Public Documentation**: Learn from my setup for free

### Market Validation
- WordPress hosting: $50B+ market
- Discord bots: 350M+ Discord users
- Minecraft hosting: $1B+ market
- API services: $10B+ market

**I'm not creating demand - I'm capturing existing demand with better value.**

---

## 📈 Milestones

### ✅ Completed
- [x] Dell PowerEdge server setup
- [x] Proxmox virtualization configured
- [x] Cloudflare Tunnel (HTTPS without port forwarding)
- [x] WordPress VM in production (test mode)
- [x] Stripe payment integration (test mode)
- [x] Security hardening (Wordfence, UFW, SSL)
- [x] Automated backups configured
- [x] Revenue strategy documented

### 🔄 In Progress (November 2025)
- [ ] Test Stripe transaction with test card
- [ ] Add branding and logo
- [ ] Transition to live Stripe keys
- [ ] Discord bot MVP development
- [ ] Game server control panel setup
- [ ] API service architecture

### ⏭️ Next Up (December 2025)
- [ ] First real customer ($1+)
- [ ] Launch Discord bot beta
- [ ] Set up Minecraft hosting
- [ ] Build screenshot API
- [ ] Marketing content creation
- [ ] Community building

### 🎯 Goals (Q1 2026)
- [ ] $100/mo MRR
- [ ] $500/mo MRR
- [ ] $1,000/mo MRR
- [ ] $2,000/mo MRR ✨

---

## 🧪 What's Working / What's Not

### ✅ What's Working
- **Cloudflare Tunnel**: No port forwarding, free SSL - amazing!
- **Proxmox**: Super stable, easy VM management
- **WordPress + Stripe**: Integration was smoother than expected
- **Documentation**: AI-assisted docs keep me organized

### ⚠️ Challenges
- **Time**: Building 4 services simultaneously is ambitious
- **Marketing**: Need to drive traffic once live
- **Support**: Will need good docs to scale
- **Pricing**: Still testing what market will pay

### 💡 Lessons Learned
1. **Document everything** - Future you will thank you
2. **Start with one service** - Get one profitable before expanding
3. **Security matters** - Spent extra time hardening, worth it
4. **Community first** - Build audience before asking for money

---

## 📖 Learn From My Setup

### Key Documentation
- [Infrastructure Setup Guide](INFRASTRUCTURE.md) - Complete server setup
- [WordPress Production Guide](WordPress-VM/AI-COLLABORATION.md) - From zero to production
- [Stripe Integration](WordPress-VM/STRIPE-SETUP-GUIDE.md) - Payment processing
- [Security Hardening](WordPress-VM/wordpress-production-hardening.md) - Lock it down
- [Revenue Strategy](REVENUE-STRATEGY.md) - Business model & pricing

### Helpful Configs
- Nginx reverse proxy setup
- Cloudflare Tunnel configuration
- WordPress optimization settings
- Security headers and firewalls
- Automated backup scripts

**Note**: All sensitive info (IPs, passwords, API keys) has been sanitized for public sharing.

---

## 🤝 Building in Public

### Monthly Updates
I'll share progress updates including:
- ✅ What shipped
- 💰 Revenue numbers (real MRR)
- 📊 Traffic and conversion metrics
- 🐛 Problems encountered
- 💡 Lessons learned
- 🎯 Next month's goals

**Subscribe for updates**: (Waitlist page coming soon!)

### Why I'm Sharing This
1. **Accountability** - Public goals = higher completion rate
2. **Learning** - Teaching forces deeper understanding
3. **Community** - Get feedback and advice
4. **Giving Back** - Internet taught me everything
5. **Marketing** - Builds trust before asking for money

---

## 🔐 Security & Privacy

### What's Public
✅ Architecture and design decisions  
✅ Tech stack and tools used  
✅ Revenue goals and progress  
✅ Lessons learned and mistakes  
✅ Configuration patterns (sanitized)

### What's Private
❌ Real IP addresses (shown as 192.168.X.X)  
❌ API keys and credentials  
❌ Customer data  
❌ Real domain names (if private)  
❌ Proprietary business logic

---

## 💬 FAQ

**Q: Why self-host instead of using cloud?**  
A: 60-80% cost savings + I control everything. Cloud markup is insane for what I need.

**Q: Isn't this risky on one server?**  
A: For now, yes. If it works, I'll add redundancy. Crawl → Walk → Run.

**Q: When can I use your services?**  
A: WordPress hosting is in test mode now. Full launch targeted for January 2026. Join waitlist for early access!

**Q: Can I copy your setup?**  
A: **YES!** That's why this is public. Fork, modify, build. I'd love to see what you create!

**Q: How do I follow along?**  
A: Star this repo, check back monthly for updates. Waitlist page coming soon.

**Q: Are you looking for investors?**  
A: Nope! Bootstrapped and proud. Want to own 100%.

---

## 📊 Revenue Tracking

### Current Status (November 1, 2025)
```
WordPress VM:    $0 (test mode)
Discord Bots:    $0 (not launched)
Game Servers:    $0 (not launched)
API Services:    $0 (not launched)
────────────────────────────────
TOTAL:           $0
TARGET:          $2,000+/mo
```

**First Dollar Goal**: December 2025 🎯

---

## 🚀 Get Involved

### Star This Repo
If you find this interesting or helpful, star it! Helps me know people care.

### Ask Questions
Open an issue or discussion. I'll answer everything I can.

### Share Your Journey
Building something similar? I'd love to hear about it!

### Join the Waitlist
Want early access to services? (Waitlist page coming soon!)

---

## 🙏 Acknowledgments

Built with help from:
- **r/selfhosted** - Best community for home server nerds
- **r/homelab** - Inspiration and troubleshooting
- **Stack Overflow** - Saved me countless hours
- **YouTube tutorials** - Visual learning FTW
- **Claude (AI)** - Documentation assistance

---

## 📅 Update Schedule

- **Weekly**: GitHub commits with progress
- **Monthly**: Detailed revenue and progress report
- **Quarterly**: Major milestone announcements

**Next Update**: December 1, 2025

---

## 📞 Contact

- **GitHub**: [@MatoTeziTanka](https://github.com/MatoTeziTanka)
- **Email**: (Coming soon - setting up)
- **Discord**: (Community server coming soon)
- **Website**: lightspeedup.com (under construction)

---

## 📝 License

This documentation is shared under MIT License. Code and configurations are provided as-is for educational purposes.

**Note**: If you use this to build your own business, drop me a line - I'd love to hear about it!

---

**Building in public since November 2025** 🚀

**Current Status**: Infrastructure ready, services launching soon!

**Star this repo to follow the journey from $0 to $2K/mo MRR** ⭐

---

*Last Updated: November 1, 2025*  
*Next Milestone: First paying customer 🎯*

