<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔧 **DELL/PROXMOX SYSTEM ADMIN GUIDE - LightSpeedUp Hosting**

**Last Updated:** November 4, 2025  
**Server:** Dell PowerEdge R730 (LightSpeedUp)  
**Hypervisor:** Proxmox VE 8.x  
**Network:** Ubiquiti EdgeRouter-10X 3.0.0  
**Status:** Production Ready for Beta Launch

---

## 📋 **EXECUTIVE SUMMARY**

This guide contains the **finalized infrastructure architecture** for LightSpeedUp's Beta hosting launch. The architecture has been **simplified from the original 4-tier physical NIC plan** to a more scalable, software-defined approach.

### **Key Decision:**
✅ **Keep current 4-NIC allocation** (no reconfiguration needed)  
✅ **All customer VMs on vmbr0** (Community Shared Network)  
✅ **Isolated Network tier uses Proxmox internal bridges** (software-defined)  
✅ **Personal/management infrastructure remains untouched** (eno2-4)

---

## 🏗️ **FINAL NETWORK ARCHITECTURE**

### **Physical NIC Allocation (UNCHANGING)**

```
┌─────────────────────────────────────────────────────────────┐
│         EdgeRouter-10X 3.0.0 (4 independent ports)          │
│     Port 1    Port 2    Port 3    Port 4                    │
└────┬──────────┬─────────┬─────────┬─────────────────────────┘
     │          │         │         │
     eno1      eno2      eno3      eno4
     │          │         │         │
   vmbr0      vmbr1     vmbr2     vmbr3
     │          │         │         │
  (Customer)  (Personal) (Mgmt)  (Storage)
  ALL VMs     NOT SALE   NOT SALE NOT SALE
```

### **Network Purposes:**

**vmbr0 (eno1) - Customer Production Network**
- **IP:** <PROXMOX_IP>/24
- **Purpose:** ALL customer VMs (Community Shared + base for Isolated)
- **Bandwidth:** 1 Gbps shared
- **Capacity:** 20-50+ customers
- **Current VMs:** VM150 (WordPress-Hosting-1)
- **Status:** ✅ ACTIVE

**vmbr1 (eno2) - Personal Services**
- **IP:** 192.168.12.71/24
- **Purpose:** Seth's personal projects (bots, games, APIs)
- **Bandwidth:** 1 Gbps dedicated
- **Current VMs:** VM100, VM160, VM170, VM180, VM190, VM191
- **Status:** ✅ ACTIVE - **NOT FOR SALE**

**vmbr2 (eno3) - Management Network**
- **IP:** 192.168.12.72/24
- **Purpose:** Proxmox Web UI, monitoring, infrastructure
- **Bandwidth:** 1 Gbps dedicated
- **Current VMs:** VM101 (pending migration), VM120, VM122
- **Status:** ✅ ACTIVE - **NOT FOR SALE**

**vmbr3 (eno4) - Storage/Media Network**
- **IP:** 192.168.12.73/24
- **Purpose:** Plex Media Server, backups
- **Bandwidth:** 1 Gbps dedicated
- **Current VMs:** VM200 (SethFlix), VM201 (StreamForge)
- **Status:** ⚠️ NO-CARRIER (cable needed) - **NOT FOR SALE**

---

## 💰 **CUSTOMER PRICING MODEL**

### **Resource Packages (Base Pricing):**

| Package | CPU | RAM | Storage | Beta Price | Regular Price |
|---------|-----|-----|---------|------------|---------------|
| **Starter** | 2 cores | 4 GB | 30 GB | **$14.50/mo** | $29/mo |
| **Business** | 6 cores | 16 GB | 120 GB | **$44.50/mo** | $89/mo |
| **Enterprise** | 12 cores | 32 GB | 300 GB | **$99.50/mo** | $199/mo |

### **Network Tier Options (Add-On):**

| Network Tier | Description | Beta Add-On | Regular Add-On |
|--------------|-------------|-------------|----------------|
| **Community Shared** | Default - All VMs on vmbr0 | Included | Included |
| **Isolated Network** | Private internal bridge (vmbr10-99) | **+$5/mo** | +$10/mo |

---

## 🌐 **NETWORK TIER DETAILS**

### **1. COMMUNITY SHARED NETWORK (Default - 90% of customers)**

**Technical Implementation:**
```
All customer VMs → vmbr0 (eno1)

Example:
├─ VM150 (Customer A - Starter + Community Shared)
├─ VM151 (Customer B - Business + Community Shared)
├─ VM152 (Customer C - Enterprise + Community Shared)
└─ VM153 (Customer D - Starter + Community Shared)
```

**Specifications:**
- **Bridge:** vmbr0 (connected to physical eno1)
- **IP Range:** 192.168.12.0/24 (DHCP or static IPs)
- **Bandwidth:** 1 Gbps **shared** uplink (eno1)
- **Internal Communication:** 10 Gbps (Proxmox virtual networking between VMs on same bridge)
- **Isolation Level:** VM-level only (separate VMs, same network bridge)
- **Firewall:** Standard iptables rules between VMs
- **Capacity:** **20-50+ customers** (bandwidth-limited, not hardware-limited)

**Security:**
- ✅ Separate VM per customer (cannot access other VMs' disks/memory)
- ✅ Dedicated CPU/RAM/storage (guaranteed resources)
- ✅ Firewall rules between VMs
- ✅ AppArmor/SELinux policies
- ⚠️ Same network bridge (can see other VMs' network traffic if compromised)
- ⚠️ Potential for network-level attacks (ARP spoofing, MAC flooding)

**Suitable For:**
- Personal blogs, portfolio sites
- Small business websites
- Non-sensitive applications
- Budget-conscious customers
- 90% of Beta customers

**Provisioning Command:**
```bash
qm create <VMID> \
  --name "customer-name-starter" \
  --cores 2 \
  --memory 4096 \
  --net0 virtio,bridge=vmbr0,firewall=1 \
  --scsi0 SSD_VMs:30,format=raw \
  --ostype l26 \
  --boot order=scsi0
```

---

### **2. ISOLATED NETWORK (+$5/mo Beta - 10% of customers)**

**Technical Implementation:**
```
Each customer gets unique Proxmox internal bridge:

vmbr10 (Customer A's private network)
└─ VM150 (Customer A only)

vmbr11 (Customer B's private network)
├─ VM151 (Customer B - web server)
└─ VM152 (Customer B - database server)

vmbr12 (Customer C's private network)
└─ VM153 (Customer C only)
```

**Specifications:**
- **Bridge:** vmbr[10-99] (unique per customer, Proxmox internal bridge - NO physical NIC)
- **IP Range:** 10.0.X.0/24 (where X = bridge number - 10)
  - vmbr10 → 10.0.0.0/24
  - vmbr11 → 10.0.1.0/24
  - vmbr12 → 10.0.2.0/24
- **Internal Bandwidth:** **10 Gbps** (Proxmox virtual networking - VM-to-VM on same bridge)
- **External Bandwidth:** 1 Gbps (routed through VM120 reverse proxy to vmbr0/eno1)
- **Isolation Level:** **Network-level** (complete separation from all other customers)
- **Firewall:** Custom rules per customer bridge
- **Capacity:** **Unlimited** (software-defined, no hardware limit)

**Architecture Diagram:**
```
Customer VM (vmbr10) → VM120 (Reverse Proxy) → vmbr0 (eno1) → Internet
                       ↑
                       NAT + Firewall Rules
```

**Security:**
- ✅ Private internal bridge (vmbr[X])
- ✅ Cannot see other customers' network traffic
- ✅ Cannot perform network-level attacks on other customers
- ✅ Custom firewall rules per customer
- ✅ NAT routing through reverse proxy (additional security layer)
- ✅ Perfect for compliance requirements (PCI DSS, HIPAA)

**Performance Advantage:**
- **Internal VM-to-VM:** 10 Gbps (perfect for web + database architecture)
- **External internet:** 1 Gbps (shared via reverse proxy)

**Suitable For:**
- E-commerce sites (payment processing, PCI DSS)
- SaaS applications (sensitive customer data)
- Healthcare applications (HIPAA compliance)
- Financial services
- Multi-VM architectures (web + database + cache)
- Customers who value privacy/security
- 10% of Beta customers

**Provisioning Commands:**

**Step 1: Create internal bridge for customer**
```bash
# Create bridge vmbr10 for first Isolated Network customer
cat >> /etc/network/interfaces << EOF

# Customer: [Customer Name] - Isolated Network
auto vmbr10
iface vmbr10 inet static
        address 10.0.0.1/24
        bridge-ports none
        bridge-stp off
        bridge-fd 0
        # Internal bridge - no physical NIC
EOF

# Reload networking
ifreload -a
```

**Step 2: Create VM on isolated bridge**
```bash
qm create <VMID> \
  --name "customer-name-isolated" \
  --cores 2 \
  --memory 4096 \
  --net0 virtio,bridge=vmbr10,firewall=1 \
  --scsi0 SSD_VMs:30,format=raw \
  --ostype l26 \
  --boot order=scsi0
```

**Step 3: Configure NAT routing through VM120**
```bash
# On VM120 (Reverse Proxy VM)
# Add NAT rule for customer's internal bridge

iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth1 -o eth0 -s 10.0.0.0/24 -j ACCEPT
iptables -A FORWARD -i eth0 -o eth1 -d 10.0.0.0/24 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Save rules
iptables-save > /etc/iptables/rules.v4
```

**Step 4: Configure reverse proxy (Nginx on VM120)**
```bash
# Create Nginx virtual host for customer domain
cat > /etc/nginx/sites-available/customer-domain.com << EOF
upstream customer_backend {
    server 10.0.0.10:80;  # Customer's VM on vmbr10
}

server {
    listen 80;
    server_name customer-domain.com www.customer-domain.com;
    
    location / {
        proxy_pass http://customer_backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/customer-domain.com /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

---

## 📊 **CAPACITY PLANNING**

### **Current Capacity Analysis:**

| Resource | Total Available | Currently Used | Available for Beta | Notes |
|----------|----------------|----------------|-------------------|-------|
| **CPU Cores** | 64 threads | ~20 threads (personal VMs) | **~44 threads** | Can allocate 2-12 cores per customer |
| **RAM** | 480 GB | ~250 GB (personal VMs) | **~230 GB** | Can allocate 4-32 GB per customer |
| **Storage** | 14 TB (SSD_VMs) | ~300 GB used | **~13.7 TB** | Can allocate 30-300 GB per customer |
| **Network (vmbr0)** | 1 Gbps | ~50 Mbps (VM150) | **~950 Mbps** | Shared across all Community customers |
| **Internal Bridges** | Unlimited (vmbr10-99) | 0 created | **Unlimited** | Software-defined, no hardware limit |

### **Beta Goal: 15-20 Customers**

**Expected Resource Allocation:**

| Package Mix | Count | CPU Total | RAM Total | Storage Total | Monthly Revenue (Beta) |
|-------------|-------|-----------|-----------|---------------|------------------------|
| **Starter** | 8 customers | 16 cores | 32 GB | 240 GB | $116 (8 × $14.50) |
| **Business** | 6 customers | 36 cores | 96 GB | 720 GB | $267 (6 × $44.50) |
| **Enterprise** | 2 customers | 24 cores | 64 GB | 600 GB | $199 (2 × $99.50) |
| **Isolated (+$5)** | 4 customers | - | - | - | $20 (4 × $5) |
| **TOTAL** | **16 customers** | **76 cores** | **192 GB** | **1.56 TB** | **$602/month** |

**Capacity Remaining After Beta:**
- **CPU:** 64 - 76 = ❌ **OVERSUBSCRIBED** by 12 threads
- **RAM:** 480 - 192 - 250 (personal) = **38 GB** remaining
- **Storage:** 14 TB - 1.56 TB - 0.3 TB (personal) = **12.14 TB** remaining
- **Network:** 1 Gbps - (16 customers × ~10-50 Mbps avg) = **~400-700 Mbps** remaining

**⚠️ CPU OVERSUBSCRIPTION NOTE:**
- Proxmox allows CPU oversubscription (common practice)
- Most VMs don't use 100% CPU constantly
- 2:1 oversubscription ratio is safe (64 cores → 128 vCPUs allocated)
- Monitor CPU usage and adjust if needed

---

## 🛠️ **PROVISIONING SCRIPTS NEEDED**

### **Script 1: `provision-customer-vm.sh`**

**Purpose:** Automate VM creation for Beta customers

**Location:** `/root/scripts/provision-customer-vm.sh`

**Inputs:**
- Customer name
- Package (starter/business/enterprise)
- Network tier (community/isolated)
- VMID (auto-assign or manual)

**Outputs:**
- Created VM with correct resources
- Assigned to correct network bridge
- SSH keys configured
- Firewall rules applied
- Backup schedule configured

**Script Outline:**
```bash
#!/bin/bash
# Usage: ./provision-customer-vm.sh <customer_name> <package> <network_tier> <vmid>

CUSTOMER_NAME=$1
PACKAGE=$2  # starter, business, enterprise
NETWORK=$3  # community, isolated
VMID=$4

# Set resources based on package
case $PACKAGE in
    starter)
        CORES=2
        RAM=4096
        STORAGE=30
        ;;
    business)
        CORES=6
        RAM=16384
        STORAGE=120
        ;;
    enterprise)
        CORES=12
        RAM=32768
        STORAGE=300
        ;;
esac

# Set network bridge
if [ "$NETWORK" == "community" ]; then
    BRIDGE="vmbr0"
else
    # Find next available internal bridge number
    BRIDGE="vmbr10"  # Logic to find next available
fi

# Create VM
qm create $VMID \
  --name "${CUSTOMER_NAME}-${PACKAGE}" \
  --cores $CORES \
  --memory $RAM \
  --net0 virtio,bridge=$BRIDGE,firewall=1 \
  --scsi0 SSD_VMs:$STORAGE,format=raw \
  --ostype l26 \
  --boot order=scsi0

echo "VM $VMID created for $CUSTOMER_NAME ($PACKAGE package, $NETWORK network)"
```

---

### **Script 2: `create-isolated-bridge.sh`**

**Purpose:** Create new Proxmox internal bridge for Isolated Network customers

**Location:** `/root/scripts/create-isolated-bridge.sh`

**Inputs:**
- Customer name
- Bridge ID (vmbr10-99, or auto-assign next available)

**Outputs:**
- Created internal bridge (vmbr[X])
- Configured IP range (10.0.X.0/24)
- Added to `/etc/network/interfaces`
- Network reloaded

**Script Outline:**
```bash
#!/bin/bash
# Usage: ./create-isolated-bridge.sh <customer_name> [bridge_id]

CUSTOMER_NAME=$1
BRIDGE_ID=${2:-10}  # Default to vmbr10 if not specified
BRIDGE="vmbr${BRIDGE_ID}"
SUBNET_OCTET=$((BRIDGE_ID - 10))  # vmbr10 → 10.0.0.0, vmbr11 → 10.0.1.0
IP="10.0.${SUBNET_OCTET}.1/24"

# Add bridge to /etc/network/interfaces
cat >> /etc/network/interfaces << EOF

# Customer: ${CUSTOMER_NAME} - Isolated Network
auto ${BRIDGE}
iface ${BRIDGE} inet static
        address ${IP}
        bridge-ports none
        bridge-stp off
        bridge-fd 0
        # Internal bridge - no physical NIC attached
EOF

# Reload networking
ifreload -a

echo "Created ${BRIDGE} for ${CUSTOMER_NAME} with IP ${IP}"
```

---

### **Script 3: `configure-reverse-proxy.sh`**

**Purpose:** Configure VM120 (reverse proxy) to route Isolated Network VMs to internet

**Location:** `/root/scripts/configure-reverse-proxy.sh`

**Inputs:**
- Customer domain (e.g., customer-site.com)
- Internal VM IP (on vmbr[X])
- SSL certificate option (letsencrypt/custom)

**Outputs:**
- Nginx virtual host configured
- SSL certificate installed (Let's Encrypt)
- NAT rules configured (iptables)
- Firewall rules added

**Script Outline:**
```bash
#!/bin/bash
# Usage: ./configure-reverse-proxy.sh <domain> <internal_ip> <ssl_option>

DOMAIN=$1
INTERNAL_IP=$2
SSL_OPTION=${3:-letsencrypt}

# Create Nginx virtual host
cat > /etc/nginx/sites-available/${DOMAIN} << EOF
upstream ${DOMAIN//./_}_backend {
    server ${INTERNAL_IP}:80;
}

server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};
    
    location / {
        proxy_pass http://${DOMAIN//./_}_backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/${DOMAIN} /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# Install SSL certificate
if [ "$SSL_OPTION" == "letsencrypt" ]; then
    certbot --nginx -d ${DOMAIN} -d www.${DOMAIN} --non-interactive --agree-tos -m admin@lightspeedup.com
fi

echo "Configured reverse proxy for ${DOMAIN} → ${INTERNAL_IP}"
```

---

## 🔐 **SECURITY CONFIGURATION**

### **Firewall Rules for Customer Isolation**

**Goal:** Prevent Community Shared customers from accessing each other

**Implementation (on Proxmox host):**

```bash
# Block inter-VM traffic on vmbr0 (except necessary services)
iptables -A FORWARD -i vmbr0 -o vmbr0 -p tcp --dport 22 -j DROP    # Block SSH between VMs
iptables -A FORWARD -i vmbr0 -o vmbr0 -p tcp --dport 3306 -j DROP  # Block MySQL between VMs
iptables -A FORWARD -i vmbr0 -o vmbr0 -p tcp --dport 5432 -j DROP  # Block PostgreSQL between VMs

# Allow web traffic (reverse proxy needs this)
iptables -A FORWARD -i vmbr0 -o vmbr0 -p tcp --dport 80 -j ACCEPT
iptables -A FORWARD -i vmbr0 -o vmbr0 -p tcp --dport 443 -j ACCEPT

# Log dropped packets for security monitoring
iptables -A FORWARD -i vmbr0 -o vmbr0 -j LOG --log-prefix "INTER-VM-BLOCKED: "
iptables -A FORWARD -i vmbr0 -o vmbr0 -j DROP

# Save rules
iptables-save > /etc/iptables/rules.v4
```

**Block Customer VMs from accessing management network:**

```bash
# Block customer VMs (vmbr0) from accessing management network (vmbr2)
iptables -A FORWARD -i vmbr0 -o vmbr2 -j DROP
iptables -A FORWARD -i vmbr2 -o vmbr0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Block customer VMs from accessing personal network (vmbr1)
iptables -A FORWARD -i vmbr0 -o vmbr1 -j DROP

# Block customer VMs from accessing storage network (vmbr3)
iptables -A FORWARD -i vmbr0 -o vmbr3 -j DROP

# Save rules
iptables-save > /etc/iptables/rules.v4
```

---

## 📊 **MONITORING REQUIREMENTS**

### **Metrics to Track (Add to health.php):**

**Per-VM Metrics:**
- CPU usage (%)
- RAM usage (MB / %)
- Disk usage (GB / %)
- Network bandwidth (in/out Mbps)
- Disk I/O (IOPS)
- Uptime

**Per-Network Metrics:**
- **vmbr0 (Community Shared):** Total bandwidth usage, VM count
- **vmbr10-99 (Isolated Networks):** Bandwidth per bridge, VM count per bridge
- Firewall rule hits
- Failed connection attempts

**Customer-Facing Stats:**
- Total customer VMs
- Community Shared VMs count
- Isolated Network VMs count
- Average resource usage per tier
- System uptime

**Commands for Monitoring:**

```bash
# Get all VM stats
pvesh get /cluster/resources --type vm

# Get specific VM stats
qm status <VMID>
pvesh get /nodes/LightSpeedUp/qemu/<VMID>/status/current

# Get network bandwidth per bridge
grep vmbr /proc/net/dev

# Get CPU usage per VM
top -b -n 1 | grep qemu

# Get memory usage per VM
free -m && ps aux | grep qemu
```

---

## 🚨 **WHAT WE'RE NOT OFFERING (IMPORTANT)**

### **Dedicated Physical NICs - NOT Available During Beta**

**Why:**
- Only 4 physical NICs total on Dell R730
- 3 already allocated to personal/management/storage infrastructure
- Not worth reorganizing for Beta (15-20 customers)

**If Customer Asks:**
*"We can provide dedicated physical network infrastructure for enterprise customers with high-traffic requirements. This requires custom infrastructure reconfiguration and starts at $299/month with a 6-month commitment. Would you like a custom quote?"*

**When to Consider:**
- Customer commits to $299+/month for 6+ months
- High-value, long-term relationship
- Requires moving personal infrastructure off eno2 or eno3

---

## 🎯 **IMMEDIATE ACTION ITEMS (Before Beta Launch)**

### **Priority 1 (Must Complete Today - Nov 4):**
- [ ] ⚠️ Connect eno4 cable to EdgeRouter Port 4 (for vmbr3/Plex)
- [ ] Create `provision-customer-vm.sh` script
- [ ] Create `create-isolated-bridge.sh` script
- [ ] Create `configure-reverse-proxy.sh` script
- [ ] Test provisioning on staging VM (use VM190 or create test VM)

### **Priority 2 (Before First Customer - Nov 5-10):**
- [ ] Configure firewall rules for customer isolation
- [ ] Set up automated daily backups for customer VMs
- [ ] Update health.php to display customer VM stats
- [ ] Create customer onboarding documentation
- [ ] Test Isolated Network provisioning end-to-end

### **Priority 3 (Nice to Have - Nov 11-30):**
- [ ] Create customer self-service portal (view VM stats, backups)
- [ ] Set up Stripe webhook integration (auto-provision on payment)
- [ ] Automated SSL certificate provisioning (Let's Encrypt)
- [ ] Per-VM bandwidth monitoring and alerts
- [ ] Automated daily reports (resource usage, alerts)

---

## 📞 **ADMIN AI QUESTIONS & ANSWERS**

### **Q1: Should we pre-create vmbr10-20 or create on-demand?**

**A:** Create on-demand (recommended)
- Less clutter in `/etc/network/interfaces`
- Only create what you need
- Easy to track which customer has which bridge
- Document in customer database: "Customer X = vmbr15"

---

### **Q2: What's the best IP range for internal bridges?**

**A:** Use `10.0.X.0/24` pattern (recommended)
- `vmbr10` → `10.0.0.0/24` (gateway: 10.0.0.1)
- `vmbr11` → `10.0.1.0/24` (gateway: 10.0.1.1)
- `vmbr12` → `10.0.2.0/24` (gateway: 10.0.2.1)

**Why 10.0.x.x instead of 192.168.x.x:**
- Won't conflict with existing 192.168.12.0/24 network
- RFC1918 private address space
- Easy to remember pattern (bridge 10 = subnet 0, bridge 11 = subnet 1)

---

### **Q3: How to handle DNS for customer domains?**

**A:** Cloudflare API automation (recommended for scale)

**Phase 1 (Beta - Manual):**
- Customer provides domain
- Manually create A record pointing to <PROXMOX_IP>
- Configure Nginx virtual host on VM120

**Phase 2 (Post-Beta - Automated):**
```bash
# Cloudflare API to create DNS A record
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"customer1.lightspeedup.com","content":"<PROXMOX_IP>","proxied":true}'
```

**Alternative:** Use Cloudflare CNAME to `hosting.lightspeedup.com` (simpler)

---

### **Q4: What monitoring solution should we use?**

**A:** Progressive approach (recommended)

**Phase 1 (Beta - Weeks 1-4):**
- Update health.php with basic per-VM stats
- Manual monitoring via Proxmox Web UI
- Daily check-ins on resource usage

**Phase 2 (Post-Beta - Month 2+):**
- Install Prometheus + Grafana
- Per-customer dashboards
- Automated alerts (email/Discord)
- Historical data retention

**Commands for health.php:**
```bash
# Get VM stats
pvesh get /cluster/resources --type vm --output-format json

# Get node stats
pvesh get /nodes/LightSpeedUp/status --output-format json

# Get storage stats
pvesm status --output-format json
```

---

### **Q5: How to handle backups for customer VMs?**

**A:** Proxmox built-in backup (vzdump)

**Backup Strategy:**
- **Starter:** Daily backups, 7-day retention
- **Business:** Daily backups, 14-day retention
- **Enterprise:** Hourly backups, 30-day retention

**Backup Script:**
```bash
#!/bin/bash
# /root/scripts/backup-customer-vms.sh

# Backup all customer VMs (150-199 range)
for VMID in {150..199}; do
    if qm status $VMID > /dev/null 2>&1; then
        vzdump $VMID \
          --storage local \
          --mode snapshot \
          --compress zstd \
          --mailnotification always \
          --mailto admin@lightspeedup.com
    fi
done
```

**Add to crontab:**
```bash
# Daily backups at 2 AM
0 2 * * * /root/scripts/backup-customer-vms.sh
```

---

## ✅ **FINAL SUMMARY FOR ADMIN AI**

### **Infrastructure Status:**
- ✅ 4-NIC network segmentation complete (Stages 1-3)
- ✅ vmbr0 (eno1) ready for customer VMs
- ✅ vmbr1-3 (eno2-4) allocated to personal/management/storage
- ⚠️ Stage 4 pending: Migrate VM101/120/122 to vmbr2, connect eno4 cable

### **Customer Provisioning:**
- ✅ Architecture finalized (Community Shared + Isolated Network)
- ⏳ Need 3 provisioning scripts
- ⏳ Need firewall rules configured
- ⏳ Need backup automation

### **Beta Launch Ready:**
- ✅ Pricing finalized (Starter/Business/Enterprise + Isolated add-on)
- ✅ Capacity calculated (can handle 15-20 customers)
- ✅ Network architecture scalable (unlimited software-defined bridges)
- ⏳ Need scripts + security before onboarding first customer

### **No Changes to Existing Infrastructure:**
- ✅ Personal VMs stay on vmbr1 (eno2)
- ✅ Management VMs stay on vmbr2 (eno3)
- ✅ Plex/media VMs stay on vmbr3 (eno4)
- ✅ All customer VMs use vmbr0 (eno1) or internal bridges (vmbr10-99)

---

**Status:** Ready for script creation and security configuration  
**Next Steps:** Create 3 provisioning scripts, configure firewall rules, test provisioning  
**Launch Date:** November 5, 2025 (pending script completion)

---

**Last Updated:** November 4, 2025  
**Maintained by:** Seth Schultz (sethpizzaboy)  
**For:** Dell/Proxmox System Admin AI

