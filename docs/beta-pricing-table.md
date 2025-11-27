# 💰 LightSpeedUp Beta Pricing - Quick Reference

**Launch:** November 5, 2025 | **Beta Discount:** 50% off for 75 days

---

## 📊 COMPLETE PRICING TABLE

| Package + Network | Regular Price | Beta Price (50% off) | CPU | RAM | Storage | Network |
|-------------------|---------------|----------------------|-----|-----|---------|---------|
| **Starter + Community** | $29/mo | **$14.50/mo** | 2 cores | 4GB | 30GB | Shared vmbr0 |
| **Starter + Isolated** | $39/mo | **$19.50/mo** | 2 cores | 4GB | 30GB | Private bridge (10 Gbps) |
| **Business + Community** | $89/mo | **$44.50/mo** | 6 cores | 16GB | 120GB | Shared vmbr0 |
| **Business + Isolated** | $99/mo | **$49.50/mo** | 6 cores | 16GB | 120GB | Private bridge (10 Gbps) |
| **Enterprise + Community** | $199/mo | **$99.50/mo** | 12 cores | 32GB | 300GB | Shared vmbr0 |
| **Enterprise + Isolated** | $209/mo | **$104.50/mo** | 12 cores | 32GB | 300GB | Private bridge (10 Gbps) |

---

## 🎯 RECOMMENDED CONFIGURATIONS

### **Most Popular (90% of customers):**
- **Business + Community:** $44.50/mo (Beta)
  - Perfect for: Small businesses, e-commerce, growing sites

### **For E-Commerce / Security:**
- **Business + Isolated:** $49.50/mo (Beta)
  - Perfect for: WooCommerce, payment processing, PCI compliance

### **For SaaS / Multi-VM:**
- **Enterprise + Isolated:** $104.50/mo (Beta)
  - Perfect for: Web + Database separation, 10 Gbps internal VM speed

---

## 🔧 NETWORK TIER BREAKDOWN

### **🌐 Community Shared (Included)**
- **Cost:** Included with all packages
- **Network:** Shared vmbr0 (connected to physical eno1)
- **Bandwidth:** 1 Gbps shared uplink
- **Isolation:** VM-level only
- **Best for:** Personal sites, blogs, small business

### **🔒 Isolated Network (+$5 Beta, +$10 Regular)**
- **Cost:** +$5/mo (Beta), +$10/mo (Regular)
- **Network:** Private internal bridge (vmbr[X])
- **Internal:** 10 Gbps between your VMs
- **External:** 1 Gbps uplink (routed)
- **Isolation:** Network-level (complete separation)
- **Best for:** E-commerce, SaaS, compliance apps, multi-VM setups

---

## 📈 CAPACITY PLANNING

### **Current Physical NICs:**
```
eno1 (vmbr0) → Community Shared Network
├─ Capacity: 20-50 customers (unlimited technically)
├─ All Starter/Business/Enterprise default packages
└─ Shared 1 Gbps uplink

eno2 (vmbr1) → Your Personal Services
├─ VM100, VM160, VM170, VM180, VM190, VM191
└─ Not for sale

eno3 (vmbr2) → Management Network
├─ VM101, VM120, VM122, Proxmox Web UI
└─ Not for sale

eno4 (vmbr3) → Media/Storage Network
├─ VM200 (Plex), VM201 (StreamForge)
└─ Not for sale
```

### **Proxmox Internal Bridges (Isolated Network):**
```
vmbr10 → Customer A (Isolated)
vmbr11 → Customer B (Isolated)
vmbr12 → Customer C (Isolated)
...
vmbr99 → Customer N (Isolated)

Capacity: Unlimited (software-defined)
Speed: 10 Gbps internal, 1 Gbps external uplink
```

---

## 💰 REVENUE PROJECTIONS

### **Scenario 1: Conservative (20 Beta customers)**
```
15 customers × $44.50 (Business + Community) = $667.50/mo
5 customers × $49.50 (Business + Isolated) = $247.50/mo
────────────────────────────────────────────────────
Total Beta Revenue: $915/month
After Beta (with 10% founder discount): $1,646/month
```

### **Scenario 2: Realistic (20 Beta customers, mixed tiers)**
```
8 customers × $14.50 (Starter + Community) = $116/mo
6 customers × $44.50 (Business + Community) = $267/mo
4 customers × $49.50 (Business + Isolated) = $198/mo
2 customers × $104.50 (Enterprise + Isolated) = $209/mo
────────────────────────────────────────────────────
Total Beta Revenue: $790/month
After Beta (with 10% founder discount): $1,422/month
```

### **Scenario 3: Optimistic (20 Beta customers, higher tiers)**
```
4 customers × $14.50 (Starter + Community) = $58/mo
10 customers × $49.50 (Business + Isolated) = $495/mo
4 customers × $99.50 (Enterprise + Community) = $398/mo
2 customers × $104.50 (Enterprise + Isolated) = $209/mo
────────────────────────────────────────────────────
Total Beta Revenue: $1,160/month
After Beta (with 10% founder discount): $2,088/month
```

---

## 🎖️ VETERAN DISCOUNT

**Stacks with Beta pricing!**

### **Example: Business + Isolated**
```
Regular Price: $99/month
Beta Price (50% off): $49.50/month
Veteran Discount (15% off Beta): -$7.42
─────────────────────────────────────
Final Price: $42.08/month
Total Savings: 57.5%
```

### **Veteran Pricing Table:**

| Package + Network | Regular | Beta | Veteran Beta |
|-------------------|---------|------|--------------|
| Starter + Community | $29 | $14.50 | **$12.32** |
| Starter + Isolated | $39 | $19.50 | **$16.57** |
| Business + Community | $89 | $44.50 | **$37.82** |
| Business + Isolated | $99 | $49.50 | **$42.08** |
| Enterprise + Community | $199 | $99.50 | **$84.58** |
| Enterprise + Isolated | $209 | $104.50 | **$88.82** |

---

## ✅ WHAT'S INCLUDED (ALL PACKAGES)

### **Infrastructure:**
- ✅ Dell PowerEdge R730 hardware
- ✅ 480 GB ECC RAM server
- ✅ 64-thread Xeon processors
- ✅ ZFS RAID-Z2 storage
- ✅ 6-layer security stack
- ✅ Rhode Island, USA location

### **Features:**
- ✅ Free SSL certificates (Let's Encrypt)
- ✅ Daily automated backups
- ✅ Cloudflare CDN integration
- ✅ ZFS snapshots
- ✅ 24/7 uptime monitoring
- ✅ Real-time health dashboard

### **Support:**
- ✅ Direct founder support (Beta)
- ✅ Discord community access
- ✅ Email support (24h response Starter, 4h Business/Enterprise)
- ✅ Free migration assistance

### **Beta Bonuses:**
- ✅ 50% off for 75 days
- ✅ Founding member status
- ✅ Lifetime 10% discount after Beta
- ✅ Priority support for life
- ✅ Shape product roadmap
- ✅ 7-day money-back guarantee

---

## 🚀 NEXT STEPS

1. **Review pricing** - Choose package + network tier
2. **Check health.php** - See live infrastructure: https://lightspeedup.com/health.php
3. **Apply for Beta** - https://lightspeedup.com/beta.php
4. **Join Discord** - Get direct support from Seth
5. **Go live** - 24-48 hour setup after payment

---

**Questions?** Email hosting@lightspeedup.com  
**Last Updated:** November 4, 2025

