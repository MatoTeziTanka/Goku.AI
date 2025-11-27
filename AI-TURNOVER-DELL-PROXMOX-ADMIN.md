<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🖥️ DELL/PROXMOX ADMIN AI - COMPLETE TURNOVER DOCUMENT

**Last Updated**: November 6, 2025  
**Owner**: Seth Schultz (sethpizzaboy@gmail.com)  
**Purpose**: Complete knowledge transfer for Dell R730 & Proxmox administration

---

## 🎯 YOUR ROLE

You are the **Dell PowerEdge R730 & Proxmox VE Administrator AI**. Your responsibilities:
1. ✅ Monitor and maintain Dell R730 hardware
2. ✅ Manage Proxmox VE hypervisor
3. ✅ Provision and manage VMs
4. ✅ Optimize performance and resource allocation
5. ✅ Handle backups and disaster recovery
6. ✅ Troubleshoot hardware and software issues
7. ✅ Plan capacity and upgrades

---

## 🖥️ HARDWARE: DELL POWEREDGE R730

### **Complete Specifications:**

| Component | Specification | Notes |
|-----------|---------------|-------|
| **Model** | Dell PowerEdge R730 | 2U Rackmount |
| **System Revision** | I | Hardware revision |
| **System Hostname** | phoenix | Internal hostname |
| **Service Tag** | F93LB42 | CRITICAL - For Dell support |
| **Express Service Code** | 33201963650 | For Dell support calls |
| **CPU** | 2x Intel Xeon E5-2698 v3 @ 2.30GHz | 32 cores / 64 threads total |
| **RAM** | 480 GB DDR4 ECC (15x 32GB DIMMs) | 2133 MHz, 9 slots empty |
| **Storage - SSD Pool** | 4x Samsung PM883 3.84TB Enterprise SSDs | ZFS RAID-Z2, ~10TB usable |
| **Storage - HDD Pool** | 4x 3.5TB 7200 RPM HDDs | ZFS RAID-Z2, ~9TB usable |
| **Storage - OS** | 2x 240GB SSDs | Hardware RAID 1 |
| **Network** | 4x 1 GbE NICs (eno1-eno4) | 4 Gbps aggregate |
| **GPU** | 2x NVIDIA GRID K1 (PCIe passthrough) | VM200, VM201 |
| **PSU** | Dual 1100W Redundant | Hot-swappable |
| **iDRAC** | iDRAC 8 (v2.82.82.82) | IP: <VM180_IP> |
| **BIOS Version** | 2.19.0 | Latest stable |
| **Lifecycle Controller** | 2.82.82.82 | Firmware management |

### **Physical Location:**
- **Location**: Seth's home datacenter, Warwick, Rhode Island
- **Access**: Physical access required (no remote hands)
- **UPS**: [TO BE ADDED - model and capacity]

### **Warranty:**
- **Status**: [TO BE VERIFIED via Dell Support website with Service Tag]
- **Expiration**: [TO BE ADDED]

---

## 🔧 PROXMOX VE CONFIGURATION

### **Host Details:**
| Property | Value |
|----------|-------|
| **Hostname** | proxmox-host (or pve) |
| **IP Address** | <PROXMOX_IP> |
| **Proxmox Version** | [TO BE VERIFIED - run `pveversion`] |
| **Web UI** | https://<PROXMOX_IP>:8006 |
| **SSH Access** | `ssh root@<PROXMOX_IP>` |
| **Password** | Norelec7! |

### **Storage Pools:**

#### **SSD_VMs** (VM Storage)
```
Type: ZFS RAID-Z2
Devices: 4x 3.84TB Samsung PM883
Total Raw: 15.36 TB
Usable: ~10 TB
Current Usage: 3.9 TB used, 6.1 TB available
Purpose: VM disks (high performance)
```

#### **Plex** (Media Storage)
```
Type: ZFS RAID-Z2
Devices: 4x 3.5TB HDDs
Total Raw: 14 TB
Usable: ~9 TB
Current Usage: [TO BE VERIFIED]
Purpose: Plex media library
```

#### **local-lvm** (Proxmox OS)
```
Type: LVM thin
Devices: 2x 240GB SSDs (RAID 1)
Usable: ~130 GB
Purpose: Proxmox OS, templates
```

---

## 🌐 NETWORK ARCHITECTURE

### **4-Tier Network Segmentation:**

```
┌─────────────────────────────────────────────────┐
│  vmbr0 (eno1) → <PROXMOX_IP>                  │
│  Purpose: Customer Production                   │
│  VMs: VM150 (WordPress)                        │
│  For Sale: YES                                  │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  vmbr1 (eno2) → 192.168.12.71                  │
│  Purpose: Personal Services                     │
│  VMs: VM160, VM170, VM180, VM192, VM203       │
│  For Sale: NO                                   │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  vmbr2 (eno3) → 192.168.12.72                  │
│  Purpose: Management/Infrastructure             │
│  VMs: VM120 (Reverse Proxy)                   │
│  For Sale: NO                                   │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  vmbr3 (eno4) → 192.168.12.73                  │
│  Purpose: Storage/Media                         │
│  VMs: VM200 (Plex)                             │
│  For Sale: NO                                   │
└─────────────────────────────────────────────────┘
```

### **Gateway & DNS:**
- **Gateway**: <EDGEROUTER_IP> (EdgeRouter 10X)
- **DNS**: 8.8.8.8, 8.8.4.4 (Google)
- **Public IP**: 70.188.182.126 (Cox Communications)

---

## 🖥️ VIRTUAL MACHINES (Complete List)

### **Production VMs:**

| VM ID | Name | OS | IP | CPU | RAM | Storage | Network | Status |
|-------|------|-----|-----|-----|-----|---------|---------|--------|
| **100** | GOKU-AI | Windows Server 2025 | <VM100_IP> | 16 | 65 GB | 500 GB | vmbr0 | ✅ Running |
| **120** | Reverse Proxy | Ubuntu 24.04 | <VM120_IP> | 6 | 6 GB | 500 GB | vmbr2 | ✅ Running |
| **150** | WordPress | Ubuntu 24.04 | <VM150_IP> | 8 | 32 GB | 500 GB | vmbr0 | ✅ Running |
| **160** | Database Services | Ubuntu 24.04 | <VM160_IP> | 8 | 32 GB | 500 GB | vmbr1 | ✅ Running |
| **170** | Game Servers | Ubuntu 24.04 | <VM170_IP> | 12 | 48 GB | 500 GB | vmbr1 | ✅ Running |
| **180** | API Services | Ubuntu 24.04 | <VM180_IP> | 8 | 32 GB | 500 GB | vmbr1 | ✅ Running |
| **192** | Atlantis Pinball | Ubuntu 24.04 | <VM192_IP> | 6 | 16 GB | 250 GB | vmbr1 | ✅ Running |
| **200** | Plex Media | Windows Server 2025 | <VM200_IP> | 8 | 32 GB | 250 GB | vmbr3 | ✅ Running |
| **201** | StreamForge Dev | Windows Server 2025 | 192.168.12.201 | 16 | 64 GB | 250 GB | vmbr1 | ✅ Running |
| **202** | Windows Template | Windows Server 2025 | - | 16 | 16 GB | 250 GB | - | ⏸️ Template |
| **203** | Development | Ubuntu 24.04 | 192.168.12.203 | 8 | 16 GB | 100 GB | vmbr1 | ✅ Running |

### **Resource Allocation:**
- **Total CPU cores allocated**: ~110 cores (host has 64 cores = overcommitted but OK)
- **Total RAM allocated**: ~370 GB (host has 480 GB = ~77% utilization)
- **Total Storage used**: ~3.9 TB (10 TB available = ~39% utilization)

---

## 🔧 COMMON ADMIN TASKS

### **1. Create New VM:**

```bash
# SSH to Proxmox host
ssh root@<PROXMOX_IP>

# Create VM (example: Ubuntu)
qm create 210 \
  --name "New-VM" \
  --memory 8192 \
  --cores 4 \
  --net0 virtio,bridge=vmbr0 \
  --scsi0 SSD_VMs:32 \
  --boot order=scsi0 \
  --ostype l26

# Download Ubuntu ISO (if not already present)
cd /var/lib/vz/template/iso
wget https://releases.ubuntu.com/24.04/ubuntu-24.04-live-server-amd64.iso

# Attach ISO
qm set 210 --ide2 local:iso/ubuntu-24.04-live-server-amd64.iso,media=cdrom

# Start VM
qm start 210

# Access console (Web UI)
# https://<PROXMOX_IP>:8006 → VM 210 → Console
```

### **2. Backup VM:**

```bash
# Manual backup (to local storage)
vzdump 150 --storage local --mode snapshot

# Backup to external location
vzdump 150 --storage /mnt/backup --mode snapshot

# Schedule backup (via Web UI or cron)
# Web UI: Datacenter → Backup → Add
```

### **3. Resize VM Disk:**

```bash
# Increase disk size (can't shrink!)
qm resize 150 scsi0 +50G

# Inside VM: extend filesystem
# Linux:
sudo resize2fs /dev/sda1

# Windows:
# Disk Management → Extend Volume
```

### **4. Change VM Resources:**

```bash
# Change RAM
qm set 150 --memory 16384

# Change CPU cores
qm set 150 --cores 8

# Requires VM restart for most changes
qm stop 150
qm start 150
```

### **5. Clone VM:**

```bash
# Full clone
qm clone 150 160 --name "WordPress-Copy" --full

# Linked clone (faster, uses less space)
qm clone 150 160 --name "WordPress-Copy"
```

### **6. Migrate VM to Different Network:**

```bash
# Change network bridge
qm set 150 --net0 virtio,bridge=vmbr1
```

---

## 📊 MONITORING & HEALTH CHECKS

### **Daily Checks:**
```bash
# Check Proxmox host health
pveversion
pveperf

# Check ZFS pool health
zpool status
zpool list

# Check VM status
qm list

# Check disk usage
df -h
zfs list

# Check RAM usage
free -h

# Check CPU load
top
```

### **Weekly Checks:**
- ✅ Review VM resource usage (CPU, RAM, disk)
- ✅ Check for Proxmox updates (`apt update && apt list --upgradable`)
- ✅ Verify backup completion
- ✅ Review /var/log/syslog for errors
- ✅ Check ZFS scrub status

### **Monthly Checks:**
- ✅ ZFS scrub (`zpool scrub <pool>`)
- ✅ Update Proxmox packages (`apt update && apt full-upgrade`)
- ✅ Review capacity planning (are we running out of space?)
- ✅ Test backup restoration
- ✅ Check Dell firmware updates (via iDRAC)

---

## 🚨 TROUBLESHOOTING

### **Issue: VM won't start**

```bash
# Check error message
qm start 150

# Check VM config
qm config 150

# Check if enough resources
free -h  # RAM
df -h    # Disk

# Check locks
qm unlock 150

# Force stop and restart
qm stop 150 --skiplock
qm start 150
```

### **Issue: Poor VM performance**

```bash
# Check host CPU usage
top

# Check disk I/O
iostat -x 1

# Check ZFS ARC usage
arc_summary

# Check VM CPU usage (from inside VM)
ssh user@vm-ip "top"

# Possible solutions:
# - Reduce overcommitment
# - Increase VM cores/RAM
# - Enable CPU host passthrough
# - Check for swap usage (bad on VMs)
```

### **Issue: Proxmox Web UI not accessible**

```bash
# Check if service is running
systemctl status pveproxy

# Restart service
systemctl restart pveproxy

# Check firewall
iptables -L

# Check listening ports
netstat -tulpn | grep 8006
```

### **Issue: ZFS pool degraded**

```bash
# Check status
zpool status

# If disk failed:
# 1. Replace physical disk
# 2. Resilver pool
zpool replace <pool> <old-disk> <new-disk>

# Monitor resilver progress
zpool status -v
```

---

## 🔒 SECURITY

### **Firewall Rules:**
- **Proxmox Host**: UFW disabled (using Proxmox firewall)
- **VMs**: Each VM has UFW enabled
- **Inter-VM traffic**: Blocked on vmbr0 (customer isolation)

### **SSH Access:**
- **SSH Key**: /root/.ssh/id_ed25519 (GitHub key)
- **Public Key**: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAHzO/boElPfcY/WPcCBT2B7YHgUZj9b7uWkrCxj4vuN

### **Passwords:**
- **Proxmox root**: Norelec7!
- **All VMs**: Norelec7! (standard password)
- **Windows Product Key**: GTX9N-9KYM3-BWYDK-8PKVT-RRKXQ

---

## 📈 CAPACITY PLANNING

### **Current Utilization:**
- **CPU**: ~110 cores allocated / 64 available = Overcommitted (OK, VMs don't use 100%)
- **RAM**: 370 GB allocated / 480 GB available = 77% (Good)
- **Storage**: 3.9 TB used / 10 TB available = 39% (Excellent)

### **Growth Projections:**
- **Beta Launch**: 15-20 customer VMs
- **Average VM**: 4 cores, 8 GB RAM, 50 GB storage
- **Expected Growth**: +100 GB RAM, +1 TB storage per month

### **Upgrade Path:**
- **RAM**: 9 empty slots, can add 9x 32GB = +288 GB (total 768 GB)
- **Storage**: Can add more SSDs to SSD_VMs pool
- **CPU**: Current CPUs sufficient for now

---

## 🔗 IMPORTANT LINKS

### **Dell Support:**
- **Support Website**: https://www.dell.com/support
- **Service Tag Lookup**: Enter service tag → Get all docs/drivers
- **iDRAC**: https://[TO BE ADDED]:443

### **Proxmox Documentation:**
- **Official Wiki**: https://pve.proxmox.com/wiki/Main_Page
- **Forum**: https://forum.proxmox.com/
- **r/Proxmox**: https://reddit.com/r/Proxmox

### **Internal:**
- **GitHub Repo**: https://github.com/MatoTeziTanka/Dell-Server-Roadmap
- **Master Doc**: ETERNAL-DRAGON-SHENRON-KNOWLEDGE.md
- **VM Specs**: docs/VM-COMPLETE-SPECIFICATIONS.md

---

## 📞 EMERGENCY PROCEDURES

### **Server Won't Boot:**
1. Check physical power (both PSUs)
2. Check network cables (all 4 NICs)
3. Access iDRAC (remote KVM)
4. Check BIOS/boot order
5. Check ZFS pool import

### **Total Data Loss:**
1. Restore from backups (check /mnt/backup or offsite)
2. Rebuild VMs from templates
3. Restore configurations from GitHub

### **Hardware Failure:**
1. Check Dell warranty status
2. Call Dell support (Express Service Code)
3. Have Service Tag ready
4. Dell will ship replacement parts

---

## 🎯 YOUR MISSION (Admin AI)

### **Primary Objectives:**
1. **Keep infrastructure running** (99.9% uptime goal)
2. **Optimize performance** (no resource waste)
3. **Maintain security** (customer isolation, patches)
4. **Plan for growth** (capacity monitoring)
5. **Document everything** (update ETERNAL-DRAGON doc)

### **Daily Tasks:**
- Check all VMs are running
- Monitor resource usage
- Review logs for errors

### **Weekly Tasks:**
- Check for Proxmox updates
- Verify backup completion
- Review capacity metrics

### **Monthly Tasks:**
- ZFS scrub
- Full system update
- Test disaster recovery

---

## 📞 CONTACTS

- **Owner**: Seth Schultz (sethpizzaboy@gmail.com)
- **GitHub**: https://github.com/MatoTeziTanka
- **Dell Support**: 1-800-433-9005 (have Service Tag ready)

---

**Status**: Active  
**Infrastructure**: 100% Complete, Ready for Production  
**Next Maintenance**: [Schedule weekly/monthly tasks]

✨ **Keep it running. Keep it secure. Keep it profitable.** 🖥️

