<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Discord Bot Services - Version Control & Change Log

**Project**: Discord Bot Services for Passive Income  
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
| New AI collaboration session complete | MAJOR (v1.0.0) | First bot deployed and earning | After completing a full objective |
| AI makes significant changes | MINOR (v0.2.0) | Bot framework chosen, dev env setup | After each AI response |
| Human makes small fix | PATCH (v0.1.1) | Fixed typo in config | Quick corrections |
| Critical hotfix | PATCH (v0.1.1) | Bot crashed, quick fix | Emergency fixes |

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
- ✅ Revenue target set: $300-600/mo
- ✅ Two bot concepts identified:
  1. ServerGuard Pro - Moderation bot ($4.99/server/mo)
  2. EconoBot - Virtual economy bot ($9.99/server/mo)
- ✅ Technical stack proposed: Discord.js (Node.js) or discord.py (Python)

**Files Created**:
- `/home/mgmt1/GitHub/PassiveIncome/Discord-Bot-Services/AI-COLLABORATION.md`
- `/home/mgmt1/GitHub/PassiveIncome/Discord-Bot-Services/VERSION-CONTROL.md`

**Infrastructure Status**:
- ❌ No VM allocated yet (likely VM160)
- ❌ No Discord application created
- ❌ No bot tokens generated
- ❌ No development environment set up
- ❌ No database configured

**Revenue Status**:
- Target: $300-600/mo
- Current: $0/mo
- Pricing: $4.99-9.99/server/month

**Testing Status**:
- ⚠️ No bots created yet
- ⚠️ No test Discord server set up
- ⚠️ No code written

**Known Issues**:
- None (project not started)

**Next Phase**: Framework selection and MVP development (v1.0.0)

---

## 🎯 Version Roadmap

### **v1.0.0** - MVP Bot #1: ServerGuard Pro (Target: Week 2-3)
**Objective**: Build and deploy first Discord bot with basic moderation features

**Planned Changes**:
- [ ] Choose framework: Discord.js vs discord.py
- [ ] Create Discord application and bot user
- [ ] Allocate VM160 (or use existing VM)
- [ ] Set up development environment (Node.js or Python)
- [ ] Install dependencies (Discord library, database driver)
- [ ] Create bot structure (commands, events, handlers)
- [ ] Implement basic commands:
  - `/kick [user]` - Kick user from server
  - `/ban [user]` - Ban user from server
  - `/warn [user] [reason]` - Warn user
  - `/mute [user] [duration]` - Mute user
  - `/purge [count]` - Delete messages
- [ ] Implement anti-spam detection
- [ ] Create SQLite database for warnings/logs
- [ ] Add bot configuration system
- [ ] Test in development Discord server
- [ ] Create bot listing page (top.gg)
- [ ] Deploy to production
- [ ] Launch free tier (basic moderation)

**Files to Create**:
```
Discord-Bot-Services/
├── ServerGuardPro/
│   ├── bot.js (or bot.py)
│   ├── config.json
│   ├── commands/
│   │   ├── kick.js
│   │   ├── ban.js
│   │   ├── warn.js
│   │   ├── mute.js
│   │   └── purge.js
│   ├── events/
│   │   ├── messageCreate.js
│   │   └── guildMemberAdd.js
│   ├── utils/
│   │   ├── database.js
│   │   └── permissions.js
│   └── package.json (or requirements.txt)
```

**Infrastructure to Set Up**:
- VM160 (Ubuntu 24.04 LTS, 2GB RAM, 2 CPU cores)
- Node.js 20.x or Python 3.11
- SQLite3 or PostgreSQL
- PM2 process manager (for Node.js) or systemd (for Python)
- UFW firewall (SSH only)

**Scripts to Execute**:
```bash
# Create Discord application
# (Manual step in Discord Developer Portal)

# Set up VM160
ssh root@<PROXMOX_IP>  # Proxmox
qm create 160 --name discord-bot-1 --memory 2048 --cores 2

# SSH to VM160 and install dependencies
ssh bot1@<VM160_IP>
sudo apt update && sudo apt upgrade -y

# Option A: Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
npm install discord.js

# Option B: Python
sudo apt install -y python3 python3-pip
pip3 install discord.py

# Install PM2 (Node.js)
sudo npm install -g pm2
pm2 start bot.js --name serverguard-pro
pm2 save
pm2 startup
```

**Success Criteria**:
- ✅ Bot online in test Discord server
- ✅ Basic moderation commands work
- ✅ Anti-spam detection functional
- ✅ Warnings logged to database
- ✅ Free tier available on bot listing sites
- ✅ Ready for premium tier ($4.99/mo)

**Revenue Target**: $0-100/mo (10-20 free tier servers, attract first premium users)

**Target Date**: November 10-15, 2025

---

### **v2.0.0** - Premium Features & Stripe Integration (Target: Week 3-4)
**Objective**: Add premium features and payment processing for ServerGuard Pro

**Planned Changes**:
- [ ] Integrate Stripe payment processing
- [ ] Create premium tier ($4.99/server/mo)
- [ ] Add premium features:
  - Custom automod rules
  - Raid protection
  - Backup/restore server settings
  - Advanced logging dashboard
  - Custom welcome messages
  - Role rewards system
- [ ] Create web dashboard for bot configuration
- [ ] Implement license key system (tie Discord server to Stripe subscription)
- [ ] Add `/premium` command to show upgrade benefits
- [ ] Create customer portal (Stripe Customer Portal)
- [ ] Set up webhook for subscription events
- [ ] Test full payment flow

**Files to Create**:
```
Discord-Bot-Services/
├── ServerGuardPro/
│   ├── premium/
│   │   ├── stripe.js
│   │   ├── licenses.js
│   │   └── webhooks.js
│   ├── dashboard/
│   │   ├── index.html
│   │   ├── app.js
│   │   └── styles.css
│   └── database/
│       └── schema.sql (add premium tables)
```

**Stripe Configuration**:
- Create Stripe product: "ServerGuard Pro Premium"
- Price: $4.99/month recurring
- Webhook URL: `https://bot.lightspeedup.com/webhook/stripe`
- Test with sandbox keys first
- Switch to live keys after testing

**Success Criteria**:
- ✅ Payment flow works (test and live)
- ✅ Premium features locked behind paywall
- ✅ License keys generated and validated
- ✅ Webhooks handle subscription events
- ✅ First paying customer acquired
- ✅ Dashboard accessible and functional

**Revenue Target**: $100-300/mo (20-60 premium servers @ $4.99/mo)

**Target Date**: November 20-25, 2025

---

### **v3.0.0** - Bot #2: EconoBot MVP (Target: Month 2)
**Objective**: Launch second bot for virtual economy and games

**Planned Changes**:
- [ ] Create second Discord application
- [ ] Build EconoBot with basic economy features:
  - `/balance` - Check virtual currency
  - `/daily` - Claim daily reward
  - `/work` - Earn currency by working
  - `/shop` - View items for sale
  - `/buy [item]` - Purchase item
  - `/inventory` - View owned items
  - `/give [user] [amount]` - Send currency
  - `/leaderboard` - Top richest users
- [ ] Add mini-games:
  - Coin flip (gambling)
  - Dice roll
  - Rock paper scissors
- [ ] Create database for economy (user balances, items, transactions)
- [ ] Launch free tier
- [ ] Deploy to production

**Files to Create**:
```
Discord-Bot-Services/
├── EconoBot/
│   ├── bot.js
│   ├── config.json
│   ├── commands/
│   │   ├── balance.js
│   │   ├── daily.js
│   │   ├── work.js
│   │   ├── shop.js
│   │   └── games/
│   │       ├── coinflip.js
│   │       └── dice.js
│   ├── database/
│   │   └── economy.db (SQLite)
│   └── package.json
```

**Success Criteria**:
- ✅ Bot online and functional
- ✅ Economy system working
- ✅ Mini-games entertaining
- ✅ Free tier on bot listing sites
- ✅ 50+ servers using free tier

**Revenue Target**: $0-100/mo (building user base, no premium yet)

**Target Date**: December 2025

---

### **v4.0.0** - EconoBot Premium & Scale (Target: Month 3)
**Objective**: Add premium features to EconoBot and scale both bots

**Planned Changes**:
- [ ] EconoBot premium tier ($9.99/server/mo):
  - Custom shop items
  - Role rewards for milestones
  - Advanced statistics dashboard
  - Custom currency name
  - Event scheduling
  - API access for integration
- [ ] ServerGuard Pro marketing push
- [ ] Cross-promote bots (suggest EconoBot in ServerGuard, vice versa)
- [ ] Add custom bot development offering ($299-999 one-time)
- [ ] Scale infrastructure if needed

**Success Criteria**:
- ✅ ServerGuard Pro: 60+ premium servers ($300/mo)
- ✅ EconoBot: 40+ premium servers ($400/mo)
- ✅ Total: 100+ premium servers ($700/mo)
- ✅ 1-2 custom bot projects ($299-999 one-time)

**Revenue Target**: $600-900/mo recurring + $300-2,000 one-time

**Target Date**: January 2026

---

### **v5.0.0** - Hit $1K/mo MRR (Target: Month 4)
**Objective**: Scale to $1,000+/mo monthly recurring revenue

**Planned Changes**:
- [ ] Scale ServerGuard Pro to 100 premium servers ($500/mo)
- [ ] Scale EconoBot to 60 premium servers ($600/mo)
- [ ] Launch third bot or add-on features
- [ ] Implement referral program (1 month free for referrals)
- [ ] Create video tutorials for YouTube
- [ ] Partner with Discord server list sites
- [ ] Optimize conversion (free → premium)

**Success Criteria**:
- ✅ $1,000+/mo MRR from Discord bots
- ✅ 150+ premium servers total
- ✅ <5% monthly churn
- ✅ Positive ROI on marketing spend

**Revenue Target**: $1,000-1,200/mo

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
- [path/to/new/file2.ext]

**Files Modified**:
- [path/to/modified/file1.ext]

**Scripts Executed**:
```bash
# Script 1 description
command here
```

**Issues Resolved**:
- ❌ [Issue description] → [Solution]

**Issues Encountered**:
- ⚠️ [New issue] → [Workaround]

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
2. **Check "Version Roadmap"** to see what needs to be built
3. **Review "Planned Changes"** for v1.0.0 (first bot MVP)
4. **Execute tasks** systematically
5. **Update this document** after completing work:
   - Increment version number (MINOR for AI work, MAJOR for milestones)
   - Add new version section using template
   - Document files created/modified
   - Update revenue tracking
6. **Commit changes** with version number in commit message

### For Humans:
1. **Check current version** (v0.1.0 = Planning)
2. **Review roadmap** to understand path to $600/mo
3. **Start new AI chat** with: "Read Discord-Bot-Services/VERSION-CONTROL.md and let's build v1.0.0"
4. **Update this document** after each milestone

---

## 📊 Progress Tracker

### Overall Project Status

| Phase | Version | Status | Completion | Revenue | Target Date |
|-------|---------|--------|------------|---------|-------------|
| Planning | v0.1.0 | ✅ Complete | 100% | $0 | Oct 31, 2025 |
| Bot #1 MVP | v1.0.0 | ⏭️ Pending | 0% | $0 | Nov 10-15, 2025 |
| Premium Features | v2.0.0 | ⏭️ Planned | 0% | $100-300 | Nov 20-25, 2025 |
| Bot #2 MVP | v3.0.0 | ⏭️ Planned | 0% | $100-400 | Dec 2025 |
| Scale Both Bots | v4.0.0 | ⏭️ Planned | 0% | $600-900 | Jan 2026 |
| Hit $1K/mo | v5.0.0 | ⏭️ Planned | 0% | $1,000+ | Feb 2026 |

### Current Sprint (v0.1.0 → v1.0.0)

| Task | Priority | Status | Assignee | Estimated Time |
|------|----------|--------|----------|----------------|
| Choose framework (Discord.js vs discord.py) | ⚡ Critical | ⏭️ Pending | AI + Human | 30 min |
| Create Discord application | ⚡ Critical | ⏭️ Pending | Human | 15 min |
| Allocate VM160 | ⚡ Critical | ⏭️ Pending | AI | 30 min |
| Set up development environment | ⚡ Critical | ⏭️ Pending | AI | 1 hour |
| Build basic bot structure | 📋 High | ⏭️ Pending | AI | 2-3 hours |
| Implement moderation commands | 📋 High | ⏭️ Pending | AI | 3-4 hours |
| Add anti-spam detection | 📋 Medium | ⏭️ Pending | AI | 2 hours |
| Create database schema | 📋 Medium | ⏭️ Pending | AI | 1 hour |
| Test in Discord server | 📋 High | ⏭️ Pending | Human | 1 hour |
| Deploy to production | 📋 High | ⏭️ Pending | AI | 1 hour |

**Total Estimated Time**: 12-15 hours of focused work

---

## 🐛 Issues & Tickets

### Open Issues

#### Issue #001 - Framework Selection: Discord.js vs discord.py
**Priority**: ⚡ Critical  
**Status**: Open  
**Created**: Oct 31, 2025  
**Assignee**: AI + Human

**Description**:
Need to choose between Discord.js (Node.js) and discord.py (Python) for bot development.

**Pros - Discord.js**:
- ✅ JavaScript (same as potential web dashboard)
- ✅ Large community and documentation
- ✅ PM2 for easy process management
- ✅ Great async/await support

**Pros - discord.py**:
- ✅ Python (easier for beginners)
- ✅ Great documentation
- ✅ Strong community
- ✅ Good for AI/ML features later

**Decision Criteria**:
- What language are you more comfortable with?
- Do you want to learn Node.js or Python?
- Will you integrate AI features? (Python advantage)

**Resolution Plan**:
- User decides or AI recommends based on goals
- Document decision and proceed with v1.0.0

---

#### Issue #002 - VM Allocation Strategy
**Priority**: 📋 Medium  
**Status**: Open  
**Created**: Oct 31, 2025  
**Assignee**: AI

**Description**:
Should Discord bots get dedicated VM160 or share with existing VMs?

**Options**:
1. **Dedicated VM160** (Recommended)
   - Pros: Isolation, easier to scale, dedicated resources
   - Cons: Another VM to manage
2. **Share with VM150** (WordPress)
   - Pros: Resource efficient
   - Cons: Risk to WordPress if bot crashes
3. **Share with VM101** (Management)
   - Pros: Already set up
   - Cons: Management VM should stay clean

**Recommendation**: Dedicated VM160 (2GB RAM, 2 CPU cores)

**Resolution Plan**:
- Create VM160 in v1.0.0
- Document in INFRASTRUCTURE.md
- Add to PORT-ALLOCATION.md

---

### Closed Issues

None yet (project not started)

---

## 💡 Ideas & Future Enhancements

### High-Priority Ideas
- [ ] **Bot Bundle** - Both bots together at discount ($12/mo vs $15)
- [ ] **White-Label Bots** - Rebrand for server owners ($49/mo)
- [ ] **Dashboard Analytics** - Show server owners detailed stats
- [ ] **Multi-Language Support** - Spanish, French, German for global market
- [ ] **Mobile App** - Manage bot settings from phone

### Medium-Priority Ideas
- [ ] **Music Bot** - 24/7 music streaming (premium feature)
- [ ] **Ticket System Bot** - Support ticket management
- [ ] **Verification Bot** - Captcha and phone verification
- [ ] **Giveaway Bot** - Automated giveaways for engagement
- [ ] **Leveling System** - XP and levels with role rewards

### Low-Priority Ideas
- [ ] **NFT Integration** - Crypto rewards (if market recovers)
- [ ] **Voice Features** - Voice channel management
- [ ] **Bot Hosting Service** - Host custom bots for others
- [ ] **Plugin System** - Let users add custom features
- [ ] **Marketplace** - Third-party add-ons

---

## 💰 Revenue Tracking

### Revenue Milestones

- [ ] First Discord application created
- [ ] First bot online in test server
- [ ] First free tier user
- [ ] 10 free tier users
- [ ] 50 free tier users
- [ ] First premium subscriber ($4.99/mo)
- [ ] $100/mo MRR
- [ ] $300/mo MRR
- [ ] $600/mo MRR (Primary goal)
- [ ] $1,000/mo MRR (Stretch goal)

### Target Pricing

**ServerGuard Pro**:
- Free tier: Basic moderation
- Premium: $4.99/server/month
  - 60 servers = $299/mo

**EconoBot**:
- Free tier: Basic economy
- Premium: $9.99/server/month
  - 40 servers = $400/mo

**Custom Development**:
- One-time: $299-999/bot
- Maintenance: $49-149/mo
- 1 project/month = $299-999 one-time

**Total Target**: $600-900/mo recurring + $300-1,000/mo one-time

---

## 🔗 Related Documentation

### In This Repository
- `AI-COLLABORATION.md` - Main AI coordination document (read this first!)
- `VERSION-CONTROL.md` - This file (version tracking and roadmap)

### Parent Repository
- `../REVENUE-STRATEGY.md` - Overall $2K/mo strategy
- `../INFRASTRUCTURE.md` - Server and network details
- `../PORT-ALLOCATION.md` - Port mapping reference
- `../README.md` - Passive Income project overview

### External Resources
- [Discord.js Guide](https://discordjs.guide/)
- [discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs)
- [Discord Bot Best Practices](https://discord.com/developers/docs/topics/community-resources)
- [top.gg Bot List](https://top.gg/)
- [discordbotlist.com](https://discordbotlist.com/)

---

## 🚀 Quick Start Guide

### Starting Your First Discord Bot Chat

**Opening Message**:
```
I want to build Discord bots for passive income.

Current version: v0.1.0 (Planning complete)
Next milestone: v1.0.0 (Build ServerGuard Pro MVP)

Read: /home/mgmt1/GitHub/PassiveIncome/Discord-Bot-Services/VERSION-CONTROL.md

Help me choose framework (Discord.js or discord.py) and build first bot.
Revenue goal: $300-600/mo within 2-3 months.

Let's start!
```

### What AI Will Do
1. Read VERSION-CONTROL.md
2. See project is in planning (v0.1.0)
3. Understand goal: 2 bots, $600/mo target
4. Help choose framework
5. Set up VM160
6. Build ServerGuard Pro MVP (v1.0.0)

---

**Last Updated**: October 31, 2025  
**Current Version**: v0.1.0 (Planning Complete)  
**Next Version**: v1.0.0 (ServerGuard Pro MVP - Week 2-3)  
**Maintained By**: AI Infrastructure Team + Human Owner  
**Repository**: https://github.com/MatoTeziTanka/PassiveIncome




