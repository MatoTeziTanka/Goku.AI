<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🐉 ETERNAL DRAGON: SHENRON KNOWLEDGE
## Complete Infrastructure Knowledge Base for RAG Injection & Emergency Reference

**Owner**: Seth Schultz (Marine Corps Veteran)  
**Location**: Warwick, Rhode Island  
**Company**: LightSpeedUp Hosting  
**Purpose**: "I Got Hit by a Bus" Emergency Documentation + SHENRON AI Knowledge Base

**Last Updated**: November 6, 2025  
**Status**: ✅ CURRENT AND OPERATIONAL  
**Auto-Update**: This document should be updated whenever ANY infrastructure change occurs

---

## 📋 TABLE OF CONTENTS

1. [CRITICAL EMERGENCY INFO](#critical-emergency-info)
2. [OWNER IDENTITY & MISSION](#owner-identity--mission)
3. [COMPLETE INFRASTRUCTURE OVERVIEW](#complete-infrastructure-overview)
4. [HARDWARE SPECIFICATIONS](#hardware-specifications)
5. [NETWORK ARCHITECTURE](#network-architecture)
6. [VIRTUAL MACHINES - COMPLETE](#virtual-machines---complete)
7. [SHENRON AI SYNDICATE](#shenron-ai-syndicate)
8. [SERVICES & WEBSITES](#services--websites)
9. [ACCESS CREDENTIALS](#access-credentials)
10. [PASSWORDS & KEYS](#passwords--keys)
11. [KNOWN ISSUES & ROADMAP](#known-issues--roadmap)
12. [EMERGENCY PROCEDURES](#emergency-procedures)
13. [CONTACT INFORMATION](#contact-information)

---

## 🚨 CRITICAL EMERGENCY INFO

### **IF SETH IS INCAPACITATED:**

**Primary Contact**: [TO BE ADDED]  
**Emergency Server Access**: See [Passwords & Keys](#passwords--keys) section  
**Critical Services**: See [Services Status](#services--websites)

### **Immediate Actions Required:**
1. ✅ Check server status: https://<PROXMOX_IP>:8006 (Proxmox)
2. ✅ Verify all VMs are running (see VM list below)
3. ✅ Check website: https://lightspeedup.com
4. ✅ Verify SHENRON: http://<VM150_IP> or https://shenron.lightspeedup.com

### **Critical Passwords Location:**
- **This Document**: See [Passwords & Keys](#passwords--keys)
- **Physical Location**: [TO BE ADDED - where are password backups?]
- **GitHub**: This repository (Dell-Server-Roadmap)

---

## 👤 OWNER IDENTITY & MISSION

### **Personal Information**
- **Name**: Seth Schultz
- **Nickname**: sethpizzaboy
- **Email**: sethpizzaboy@gmail.com
- **Background**: United States Marine Corps Veteran
- **Location**: Warwick, Rhode Island
- **GitHub**: MatoTeziTanka
- **Company**: LightSpeedUp Hosting

### **Mission Statement**
To provide affordable, enterprise-grade hosting services while showcasing technical expertise and infrastructure capabilities. LightSpeedUp Hosting uses professional Dell PowerEdge hardware to offer high-performance hosting at competitive prices, demonstrating that quality doesn't require enterprise pricing.

### **Company Services**
1. **Web Hosting** - WordPress, static sites, custom applications
2. **Virtual Private Servers** - Full root access Linux/Windows VMs
3. **Domain Management** - Registration, DNS, email
4. **Professional Email** - Business email hosting
5. **AI Consultation** - SHENRON Syndicate multi-model AI council

### **Core Values**
- **Quality Over Profit**: Using enterprise hardware for affordable hosting
- **Transparency**: Open about infrastructure and capabilities
- **Support**: Responsive, knowledgeable customer service
- **Innovation**: Unique AI consultation platform (SHENRON Syndicate)
- **Military Precision**: Attention to detail, reliability, discipline

---

## 🏗️ COMPLETE INFRASTRUCTURE OVERVIEW

### **Architecture Diagram**

```
Internet (Public IP: 70.188.182.126)
    ↓
Cox Router (192.168.11.1)
    ↓
Deeper Network Mini (Security)
    ↓
EdgeRouter 10X (<EDGEROUTER_IP>) - Gateway
    ↓
Dell PowerEdge R730 - Proxmox Host (<PROXMOX_IP>)
    ↓
┌───────────────────────────────────────────────────────┐
│  VIRTUAL MACHINES (13 Active, 1 Template)            │
├───────────────────────────────────────────────────────┤
│  VM 100: GOKU-AI (Windows, AI Models)                │
│  VM 120: Reverse Proxy (Nginx, Cloudflare Tunnel)    │
│  VM 150: WordPress (Apache, Main Website)            │
│  VM 160: Database Services (MySQL/MariaDB)           │
│  VM 170: Game Servers (Minecraft, CS2, etc.)         │
│  VM 180: API Services (Microservices)                │
│  VM 190: Legacy Reverse Proxy (Deprecated)           │
│  VM 192: Atlantis Pinball (React + API)              │
│  VM 200: Plex Media Server (Windows, GPU)            │
│  VM 201: StreamForge Dev (Windows, GPU, VS)          │
│  VM 202: Windows Template (Template, Not Running)     │
│  VM 203: Development Server (Ubuntu)                 │
└───────────────────────────────────────────────────────┘
```

### **Current Status**
- **Infrastructure**: ✅ 100% Complete and Operational
- **Network**: ✅ 4-tier segmentation implemented
- **Storage**: ✅ ZFS RAID-Z2 (SSD + HDD pools)
- **Backups**: ⚠️ Manual (automated backups pending)
- **Security**: ✅ Multi-layer firewall, SSH keys
- **Monitoring**: ⚠️ health.php exists, needs updates

---

## 🖥️ HARDWARE SPECIFICATIONS

### **Dell PowerEdge R730 - Primary Server**

| Component | Specification | Notes |
|-----------|---------------|-------|
| **Model** | Dell PowerEdge R730 Rack Server | Enterprise-grade |
| **System Revision** | I | Hardware revision |
| **System Hostname** | phoenix | Internal hostname |
| **Form Factor** | 2U Rackmount | |
| **Service Tag** | F93LB42 | CRITICAL - For Dell support |
| **Express Service Code** | 33201963650 | For Dell support calls |
| **Purchase Date** | [TO BE ADDED] | |
| **Location** | Home Lab, Warwick, RI | |

### **CPU Configuration**
| Property | Value |
|----------|-------|
| **Processor** | 2x Intel Xeon E5-2698 v3 @ 2.30GHz |
| **Cores per CPU** | 16 cores (32 threads) |
| **Total Cores** | 32 cores / 64 threads |
| **Architecture** | Haswell (Broadwell refresh) |
| **Cache** | 40MB L3 Cache per CPU |
| **TDP** | 135W per CPU |

### **Memory Configuration**
| Property | Value |
|----------|-------|
| **Total RAM** | 480 GB DDR4 ECC |
| **Configuration** | 15x 32GB DIMMs |
| **Speed** | 2133 MHz (DDR4-2133) |
| **Type** | ECC Registered (RDIMM) |
| **Slots Used** | 15 of 24 slots |
| **Expansion Available** | 9 empty slots (288 GB max additional) |

### **Storage Configuration**

#### **SSD Pool (VM Storage)**
- **Type**: ZFS RAID-Z2
- **Drives**: 4x Samsung PM883 3.84TB Enterprise SSDs
- **Total Raw**: 15.36 TB
- **Usable Space**: ~10 TB (after RAID-Z2 parity)
- **Current Usage**: 6.1 TB available
- **Performance**: ~2000 MB/s read, ~1500 MB/s write
- **Purpose**: VM storage (SSD_VMs pool)

#### **HDD Pool (Media Storage)**
- **Type**: ZFS RAID-Z2
- **Drives**: 4x 3.5TB 7200 RPM HDDs
- **Total Raw**: 14 TB
- **Usable Space**: ~9 TB (after RAID-Z2 parity)
- **Current Usage**: 11.6 TB available (Plex pool)
- **Purpose**: Media storage for Plex

#### **OS Drives**
- **Type**: RAID 1 (Hardware RAID)
- **Drives**: 2x 240GB SSDs
- **Purpose**: Proxmox OS installation
- **Usable**: ~130 GB (local-lvm)

### **Network Interfaces**
| NIC | Bridge | IP | Purpose |
|-----|--------|-----|---------|
| **eno1** | vmbr0 | <PROXMOX_IP> | Customer Production (ALL customer VMs) |
| **eno2** | vmbr1 | 192.168.12.71 | Personal Services (Internal use) |
| **eno3** | vmbr2 | 192.168.12.72 | Management (Infrastructure) |
| **eno4** | vmbr3 | 192.168.12.73 | Storage/Media (Plex) |

**Capacity**: 4x 1 GbE = 4 Gbps aggregate bandwidth

### **GPU Configuration**
| GPU | Slot | Passthrough | VM Assignment |
|-----|------|-------------|---------------|
| **NVIDIA GRID K1** (GPU 0) | PCIe 84:00.0 | ✅ Yes | VM 200 (Plex) |
| **NVIDIA GRID K1** (GPU 1) | PCIe 85:00.0 | ✅ Yes | VM 201 (StreamForge) |

**Note**: GRID K1 has 4 GPUs per card, currently using 2

### **Power & Cooling**
- **PSU**: Dual 1100W Redundant Power Supplies
  - PSU 1 Firmware: 00.24.35
  - PSU 2 Firmware: 00.1D.7D
- **Cooling**: 6x Hot-swap fans (redundant)
- **Power Consumption**: ~400W idle, ~800W under load
- **Current Power State**: ON
- **UPS**: [TO BE ADDED - UPS model and capacity]

### **Remote Management**
- **iDRAC**: Version 2.82.82.82 (iDRAC 8)
- **iDRAC IP**: <VM180_IP>
- **iDRAC MAC**: 44:A8:42:05:C0:B6
- **iDRAC Access**: https://<VM180_IP>
- **Lifecycle Controller**: 2.82.82.82
- **BIOS Version**: 2.19.0
- **Features**: Remote KVM, Virtual Media, Power Control
- **License**: Enterprise

---

## 🌐 NETWORK ARCHITECTURE

### **External Network**
| Component | Value | Notes |
|-----------|-------|-------|
| **Public IP** | 70.188.182.126 | Cox Communications |
| **ISP** | Cox Cable | Gigabit plan |
| **External DNS** | Cloudflare | DNS + CDN |
| **Tunnel** | norelec-tunnel | Cloudflare Tunnel on VM 120 |

### **Internal Network (192.168.12.0/24)**
| Component | IP | MAC | Purpose |
|-----------|-----|-----|---------|
| **Gateway** | <EDGEROUTER_IP> | - | EdgeRouter 10X |
| **Proxmox Host** | <PROXMOX_IP> | - | Dell R730 |
| **Cox Router** | 192.168.11.1 | - | Upstream (NAT) |

### **Network Segmentation Strategy**

#### **vmbr0 (Customer Production) - <PROXMOX_IP>**
- **Purpose**: ALL customer VMs
- **VMs**: VM150 (WordPress)
- **Isolation**: Customer VMs isolated from each other
- **Security**: Strict firewall rules between VMs
- **For Sale**: YES - used for hosting services

#### **vmbr1 (Personal Services) - 192.168.12.71**
- **Purpose**: Seth's personal services
- **VMs**: VM160, VM170, VM180, VM192
- **Isolation**: Separate from customer network
- **For Sale**: NO - not for customers

#### **vmbr2 (Management) - 192.168.12.72**
- **Purpose**: Infrastructure management
- **VMs**: VM120 (Reverse Proxy)
- **Isolation**: Separate from production
- **For Sale**: NO - infrastructure only

#### **vmbr3 (Storage/Media) - 192.168.12.73**
- **Purpose**: Media streaming (Plex)
- **VMs**: VM200 (Plex Server)
- **Isolation**: Separate media network
- **For Sale**: NO - personal use

### **Port Forwarding (EdgeRouter)**
| External Port | Internal IP | Internal Port | Service |
|---------------|-------------|---------------|---------|
| 32400 | <VM200_IP> | 32400 | Plex Media Server |
| 80 | <VM120_IP> | 80 | HTTP (Cloudflare Tunnel) |
| 443 | <VM120_IP> | 443 | HTTPS (Cloudflare Tunnel) |

### **DNS Configuration**
| Domain | Type | Points To | Notes |
|--------|------|-----------|-------|
| lightspeedup.com | A | Cloudflare Tunnel | Main website |
| www.lightspeedup.com | CNAME | lightspeedup.com | Alias |
| wp.lightspeedup.com | CNAME | lightspeedup.com | WordPress admin |
| shenron.lightspeedup.com | A | Cloudflare Tunnel | AI Council |
| pinball.lightspeedup.com | A | Cloudflare Tunnel | Atlantis Pinball |

---

## 🖥️ VIRTUAL MACHINES - COMPLETE

### **VM 100 - GOKU-AI (Windows Server 2025)**

| Property | Value |
|----------|-------|
| **VM ID** | 100 |
| **Hostname** | GOKU-AI |
| **OS** | Windows Server 2025 Datacenter |
| **IP Address** | <VM100_IP> |
| **MAC Address** | BC:24:11:D5:FE:35 |
| **CPU** | 16 cores (host passthrough) |
| **RAM** | 65 GB |
| **Storage** | 500 GB (SSD_VMs) |
| **Network** | vmbr0 (Customer Production) |
| **Status** | ✅ RUNNING |

**Purpose**: AI Council / SHENRON Syndicate  
**Access**: Windows RDP (auto-login as Administrator)  
**Username**: Administrator  
**Password**: Norelec7!

**Software**:
- LM Studio 0.3.31 (auto-start on boot)
- Microsoft Machine Learning Server 9.4.7
- Python 3.11 (C:\GOKU-AI\venv)
- SHENRON v4.0 API Server (port 5000)
- ChromaDB (RAG knowledge base)

**AI Models Loaded** (LM Studio API on port 1234):
1. **GOKU** 🥋 - deepseek-coder-v2-lite-instruct (temp 0.7)
2. **VEGETA** 👑 - llama-3.2-3b-instruct (temp 0.3)
3. **PICCOLO** 🧠 - qwen2.5-coder-7b-instruct (temp 0.5)
4. **GOHAN** ⚠️ - mistral-7b-instruct-v0.3 (temp 0.4)
5. **KRILLIN** 🔧 - phi-3-mini-128k-instruct (temp 0.6)
6. **FRIEZA** 😈 - phi-3-mini-128k-instruct:2 (temp 0.9)

**SHENRON v4.0 Features**:
- TRUE synthesis (7th AI call)
- Agent mode (SSH command execution with safety guardrails)
- RAG (Retrieval Augmented Generation) with persistent memory
- Consensus detection (Unanimous/Strong/Majority/Weak)

---

### **VM 120 - Reverse Proxy Gateway (Ubuntu 24.04 LTS)**

| Property | Value |
|----------|-------|
| **VM ID** | 120 |
| **Hostname** | reverse-proxy-gateway |
| **OS** | Ubuntu 24.04 LTS |
| **IP Address** | <VM120_IP> |
| **MAC Address** | BC:24:11:87:19:86 |
| **CPU** | 6 cores |
| **RAM** | 6 GB |
| **Storage** | 500 GB (SSD_VMs) |
| **Network** | vmbr2 (Management) |
| **Status** | ✅ RUNNING |

**Purpose**: Reverse Proxy, SSL Termination, Cloudflare Tunnel  
**Access**: SSH (ssh proxy1@<VM120_IP>)  
**Username**: proxy1  
**Password**: Norelec7!

**Software**:
- Nginx (reverse proxy)
- Cloudflare Tunnel (norelec-tunnel)
- SSL/TLS termination

**Proxied Sites**:
- lightspeedup.com → VM 150
- shenron.lightspeedup.com → VM 150
- pinball.lightspeedup.com → VM 192

---

### **VM 150 - WordPress Hosting (Ubuntu 24.04 LTS)**

| Property | Value |
|----------|-------|
| **VM ID** | 150 |
| **Hostname** | wordpress-1 |
| **OS** | Ubuntu 24.04 LTS |
| **IP Address** | <VM150_IP> |
| **MAC Address** | BC:24:11:D3:D0:A6 |
| **CPU** | 8 cores |
| **RAM** | 32 GB |
| **Storage** | 500 GB (SSD_VMs, can be reduced to 100 GB) |
| **Network** | vmbr0 (Customer Production) |
| **Status** | ✅ RUNNING |

**Purpose**: WordPress Hosting, Main Website, SHENRON Web GUI  
**Access**: SSH (ssh wp1@<VM150_IP>)  
**Username**: wp1  
**Password**: Norelec7!

**Software**:
- Apache 2.4.58
- PHP 8.x
- MySQL/MariaDB client
- WordPress (lightspeedup.com)

**Hosted Sites** (Apache VirtualHosts):
- lightspeedup.com → /var/www/wordpress
- www.lightspeedup.com → Alias of lightspeedup.com
- wp.lightspeedup.com → WordPress admin
- shenron.lightspeedup.com → /var/www/shenron.lightspeedup.com
- <VM150_IP> (direct IP) → Syndicate (internal access)

**SHENRON Syndicate Files** (/var/www/shenron.lightspeedup.com/):
- index.html (v3.2)
- script.js (v3.2.1 - needs status animation fix)
- style.css (v3.2)
- api.php (proxy to SHENRON API on VM100:5000)

**Known Issues**:
- ⚠️ Warrior status animations don't turn green individually (flashing orange only)
- ⚠️ Missing live clock
- ⚠️ Missing version/date info

---

### **VM 160 - Database Services (Ubuntu 24.04 LTS)**

| Property | Value |
|----------|-------|
| **VM ID** | 160 |
| **Hostname** | dbs-1 |
| **OS** | Ubuntu 24.04 LTS |
| **IP Address** | <VM160_IP> |
| **MAC Address** | BC:24:11:76:05:13 |
| **CPU** | 8 cores |
| **RAM** | 32 GB |
| **Storage** | 500 GB (can be reduced to 100 GB) |
| **Network** | vmbr1 (Personal Services) |
| **Status** | ✅ RUNNING |

**Purpose**: Database hosting (MySQL/MariaDB)  
**Access**: SSH (ssh dbs1@<VM160_IP>)  
**Username**: dbs1  
**Password**: Norelec7!

**Software**:
- MySQL 8.0 / MariaDB
- phpMyAdmin (optional)

---

### **VM 170 - Game Server Hosting (Ubuntu 24.04 LTS)**

| Property | Value |
|----------|-------|
| **VM ID** | 170 |
| **Hostname** | gsh-1 |
| **OS** | Ubuntu 24.04 LTS |
| **IP Address** | <VM170_IP> |
| **MAC Address** | BC:24:11:7E:93:38 |
| **CPU** | 12 cores |
| **RAM** | 48 GB |
| **Storage** | 500 GB (can be reduced to 200 GB) |
| **Network** | vmbr1 (Personal Services) |
| **Status** | ✅ RUNNING |

**Purpose**: Game server hosting (Minecraft, CS2, etc.)  
**Access**: SSH (ssh gsh1@<VM170_IP>)  
**Username**: gsh1  
**Password**: Norelec7!

---

### **VM 180 - API Services (Ubuntu 24.04 LTS)**

| Property | Value |
|----------|-------|
| **VM ID** | 180 |
| **Hostname** | apis-1 |
| **OS** | Ubuntu 24.04 LTS |
| **IP Address** | <VM180_IP> |
| **MAC Address** | BC:24:11:F6:7A:33 |
| **CPU** | 8 cores |
| **RAM** | 32 GB |
| **Storage** | 500 GB (can be reduced to 100 GB) |
| **Network** | vmbr1 (Personal Services) |
| **Status** | ✅ RUNNING |

**Purpose**: API services, microservices, webhooks  
**Access**: SSH (ssh apis1@<VM180_IP>)  
**Username**: apis1  
**Password**: Norelec7!

---

### **VM 192 - Atlantis Pinball (Ubuntu 24.04 LTS)**

| Property | Value |
|----------|-------|
| **VM ID** | 192 |
| **Hostname** | atlantis-pinball |
| **OS** | Ubuntu 24.04 LTS |
| **IP Address** | <VM192_IP> |
| **CPU** | 6 cores |
| **RAM** | 16 GB |
| **Storage** | 250 GB |
| **Network** | vmbr1 (Personal Services) |
| **Status** | ✅ RUNNING |

**Purpose**: Atlantis Pinball Leaderboard (React + FastAPI)  
**Access**: SSH  
**Ports**:
- 3000: Frontend (React)
- 8000: Backend API (FastAPI)

**External Access**: https://pinball.lightspeedup.com (via VM 120 proxy)

---

### **VM 200 - Plex Media Server (Windows Server 2025)**

| Property | Value |
|----------|-------|
| **VM ID** | 200 |
| **Hostname** | SethFlix-Media-Server-2025 |
| **OS** | Windows Server 2025 Datacenter |
| **IP Address** | <VM200_IP> |
| **CPU** | 8 cores |
| **RAM** | 32 GB |
| **Storage** | 250 GB (OS) + Plex pool (11.6 TB) |
| **GPU** | NVIDIA GRID K1 (PCIe 84:00.0) passthrough |
| **Network** | vmbr3 (Storage/Media) |
| **Status** | ✅ RUNNING |

**Purpose**: Plex Media Server  
**Access**: Windows RDP  
**Username**: Administrator  
**Password**: Norelec7!  
**External Access**: http://70.188.182.126:32400

**Software**:
- Plex Media Server
- GPU encoding/transcoding enabled

---

### **VM 201 - StreamForge Development (Windows Server 2025)**

| Property | Value |
|----------|-------|
| **VM ID** | 201 |
| **Hostname** | StreamForge-Development-2025 |
| **OS** | Windows Server 2025 Datacenter |
| **IP Address** | 192.168.12.201 |
| **CPU** | 16 cores |
| **RAM** | 64 GB |
| **Storage** | 250 GB |
| **GPU** | NVIDIA GRID K1 (PCIe 85:00.0) passthrough |
| **Network** | vmbr1 (Personal Services) |
| **Status** | ✅ RUNNING |

**Purpose**: StreamForge Development, Visual Studio Enterprise  
**Access**: Windows RDP  
**Username**: Administrator  
**Password**: Norelec7!

**Software**:
- Visual Studio Enterprise 2022
- GPU development tools
- StreamForge project files

---

### **VM 202 - Windows Server 2025 Template**

| Property | Value |
|----------|-------|
| **VM ID** | 202 |
| **Hostname** | Windows-Server-2025-Template |
| **OS** | Windows Server 2025 Datacenter |
| **CPU** | 16 cores |
| **RAM** | 16 GB |
| **Storage** | 250 GB |
| **Status** | ⏸️ TEMPLATE (Not Running) |

**Purpose**: Template for cloning new Windows VMs  
**Product Key**: GTX9N-9KYM3-BWYDK-8PKVT-RRKXQ (ECPI license)

---

### **VM 203 - Development Server (Ubuntu 24.04 LTS)**

| Property | Value |
|----------|-------|
| **VM ID** | 203 |
| **OS** | Ubuntu 24.04 LTS |
| **IP Address** | 192.168.12.203 |
| **CPU** | 8 cores |
| **RAM** | 16 GB |
| **Storage** | 100 GB |
| **Network** | vmbr1 (Personal Services) |
| **Status** | ✅ RUNNING |

**Purpose**: Development and testing  
**Access**: SSH

---

## 🐉 SHENRON AI SYNDICATE

### **Overview**
The SHENRON Syndicate is a unique multi-model AI council that provides diverse perspectives through 6 different AI personalities (DBZ-Warriors), coordinated by SHENRON, the orchestrator.

### **Architecture**
```
User → Web GUI (VM150) → api.php Proxy → SHENRON API (VM100:5000) → RAG Search (ChromaDB)
                                                ↓
                                    LM Studio API (VM100:1234)
                                                ↓
                        ┌───────────────────────┴───────────────────────┐
                        ↓           ↓           ↓           ↓           ↓
                     GOKU      VEGETA      PICCOLO      GOHAN      KRILLIN      FRIEZA
                   (6 parallel queries)
                        ↓           ↓           ↓           ↓           ↓
                        └───────────────────────┬───────────────────────┘
                                                ↓
                                    SHENRON Synthesis (7th AI call)
                                                ↓
                                        Unified Response
```

### **Version History**
- **v2.1** (Nov 5, 2025): Original parallel query system
- **v3.0** (Nov 5, 2025): Added RAG + orchestrator
- **v3.1** (Nov 6, 2025): Fixed status bar design
- **v3.2** (Nov 6, 2025): Enhanced response layout
- **v3.2.1** (Nov 6, 2025): Status animations (needs fix)
- **v4.0** (Nov 6, 2025): TRUE synthesis + Agent mode

### **Current Status (v4.0)**
- ✅ TRUE synthesis working (7th AI call confirmed)
- ✅ Agent mode safety guardrails operational
- ⚠️ SSH execution needs key configuration
- ⚠️ Web GUI status animations need fix
- ⚠️ Missing live clock and version info

### **AI Warriors Configuration**

| Warrior | Emoji | Role | Model | Temp | Purpose |
|---------|-------|------|-------|------|---------|
| **GOKU** | 🥋 | Adaptive Warrior & Growth Catalyst | deepseek-coder-v2-lite-instruct | 0.7 | Creative, adaptive, learns from challenges |
| **VEGETA** | 👑 | Technical Authority | llama-3.2-3b-instruct | 0.3 | Precise, technical, no compromises |
| **PICCOLO** | 🧠 | Strategic Sage | qwen2.5-coder-7b-instruct | 0.5 | Long-term planning, wisdom |
| **GOHAN** | ⚠️ | Risk Sentinel | mistral-7b-instruct-v0.3 | 0.4 | Risk assessment, cautious |
| **KRILLIN** | 🔧 | Practical Engineer | phi-3-mini-128k-instruct | 0.6 | Hands-on, pragmatic |
| **FRIEZA** | 😈 | Chaos Tyrant | phi-3-mini-128k-instruct:2 | 0.9 | Devil's advocate, creative chaos |

### **Performance**
- **v3.2.1**: ~5-6s (6 parallel calls, placeholder synthesis)
- **v4.0**: ~27s (7 calls: 6 warriors + TRUE synthesis)
- **Trade-off**: +22s for massive quality improvement

### **Access**
- **Internal**: http://<VM150_IP>
- **External**: https://shenron.lightspeedup.com
- **API**: http://<VM100_IP>:5000

---

## 🌐 SERVICES & WEBSITES

### **Production Websites**

| Domain | VM | Path | Status |
|--------|-----|------|--------|
| lightspeedup.com | VM150 | /var/www/wordpress | ✅ LIVE |
| www.lightspeedup.com | VM150 | Alias | ✅ LIVE |
| wp.lightspeedup.com | VM150 | WordPress admin | ✅ LIVE |
| shenron.lightspeedup.com | VM150 | /var/www/shenron.lightspeedup.com | ✅ LIVE |
| pinball.lightspeedup.com | VM192 | React app (port 3000) | ✅ LIVE |

### **Internal Services**

| Service | VM | Port | Access |
|---------|-----|------|--------|
| Proxmox Web UI | Host | 8006 | https://<PROXMOX_IP>:8006 |
| LM Studio API | VM100 | 1234 | http://<VM100_IP>:1234 |
| SHENRON API | VM100 | 5000 | http://<VM100_IP>:5000 |
| Plex | VM200 | 32400 | http://<VM200_IP>:32400 |

### **Service Status Dashboard**
- ⚠️ **Needs Implementation**: health.php monitoring dashboard
- **Location**: TBD
- **Should Monitor**: All VMs, services, disk space, uptime

---

## 🔑 ACCESS CREDENTIALS

### **Proxmox Host**
- **IP**: <PROXMOX_IP>
- **Web UI**: https://<PROXMOX_IP>:8006
- **SSH**: `ssh root@<PROXMOX_IP>`
- **Username**: root
- **Password**: [REDACTED - see secure location]
- **SSH Key**: /root/.ssh/id_ed25519

### **GitHub**
- **Username**: MatoTeziTanka
- **Repository**: Dell-Server-Roadmap
- **SSH Key**: /root/.ssh/id_ed25519
- **Public Key**: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAHzO/boElPfcY/WPcCBT2B7YHgUZj9b7uWkrCxj4vuN

### **All VMs - Standard Credentials**
**Default Password for ALL VMs**: Norelec7!

| VM | IP | Username | Access Method |
|----|-----|----------|---------------|
| VM100 | <VM100_IP> | Administrator | RDP |
| VM120 | <VM120_IP> | proxy1 | SSH |
| VM150 | <VM150_IP> | wp1 | SSH |
| VM160 | <VM160_IP> | dbs1 | SSH |
| VM170 | <VM170_IP> | gsh1 | SSH |
| VM180 | <VM180_IP> | apis1 | SSH |
| VM192 | <VM192_IP> | [TBD] | SSH |
| VM200 | <VM200_IP> | Administrator | RDP |
| VM201 | 192.168.12.201 | Administrator | RDP |
| VM203 | 192.168.12.203 | [TBD] | SSH |

---

## 🔐 PASSWORDS & KEYS

### **Universal Password**
**Password**: Norelec7!  
**Used For**: All VMs, services, WordPress admin, databases

### **Windows Server Product Keys**
- **VM 100, 200, 201, 202**: GTX9N-9KYM3-BWYDK-8PKVT-RRKXQ (ECPI license)

### **SSH Keys Location**
- **Proxmox Host**: /root/.ssh/id_ed25519 (private), id_ed25519.pub (public)
- **GitHub**: Same key used for GitHub authentication

### **External Services**
- **Cloudflare**: [Email + password TBD]
- **Domain Registrar**: [TBD]
- **Cox Communications**: [Account info TBD]

### **Database Credentials**
- **MySQL Root**: Norelec7!
- **WordPress DB User**: [TBD]
- **WordPress DB Password**: [TBD]

---

## ⚠️ KNOWN ISSUES & ROADMAP

### **Critical Issues**
1. ⚠️ **Automated Backups**: Not implemented yet
2. ⚠️ **Monitoring Dashboard**: health.php needs updates
3. ⚠️ **UPS Configuration**: No UPS documentation

### **SHENRON Syndicate Issues**
1. ⚠️ **Status Animations**: Warriors don't turn green individually (v3.2.1 bug)
2. ⚠️ **Missing Features**: No live clock, no version info
3. ⚠️ **Agent Mode**: SSH keys not configured for command execution
4. ⚠️ **Easter Eggs**: Limited DBZ references

### **Infrastructure Issues**
1. ⚠️ **VM Disk Sizes**: Several VMs over-provisioned (500 GB → can be 100 GB)
2. ⚠️ **SSH Windows**: Windows DC blocks SSH password auth (known limitation)
3. ⚠️ **iDRAC**: Configuration not documented

### **Roadmap (v4.1+)**
1. Fix warrior status animations
2. Add live clock to Syndicate
3. Add version/date info to Syndicate
4. Add more DBZ easter eggs
5. Configure SSH keys for agent mode
6. Implement multi-step workflows
7. Add command feedback loops
8. Update web GUI for v4.0 features
9. Implement automated backups
10. Create monitoring dashboard

---

## 🚨 EMERGENCY PROCEDURES

### **If Server is Down**
1. Check physical server (power, network cables)
2. Access iDRAC: [iDRAC IP TBD]
3. Check EdgeRouter: https://<EDGEROUTER_IP>
4. Power cycle if necessary (last resort)

### **If Website is Down**
1. Check VM150 status: Proxmox → VM 150
2. Check Apache: `ssh wp1@<VM150_IP> "sudo systemctl status apache2"`
3. Check Cloudflare Tunnel: VM120 cloudflared service
4. Check DNS: Cloudflare dashboard

### **If SHENRON is Down**
1. Check VM100 status: RDP to <VM100_IP>
2. Check LM Studio is running (should auto-start)
3. Check SHENRON API: `python C:\GOKU-AI\shenron\shenron-v4-api-server.py`
4. Check if all 6 models are loaded in LM Studio

### **Data Recovery**
- **VM Snapshots**: Proxmox has snapshot capability (check if enabled)
- **ZFS Snapshots**: `zfs list -t snapshot` on Proxmox
- **Off-site Backups**: [TBD - where are off-site backups?]

---

## 📞 CONTACT INFORMATION

### **Owner**
- **Name**: Seth Schultz
- **Nickname**: sethpizzaboy
- **Email**: sethpizzaboy@gmail.com
- **Phone**: [TO BE ADDED - Seth should add this]
- **Location**: Warwick, Rhode Island

### **Emergency Contacts**
- **Primary**: [TO BE ADDED - family member or trusted friend]
- **Technical**: [TO BE ADDED - IT professional if Seth is unavailable]
- **Legal**: [TO BE ADDED - attorney for business matters]
- **NOTE**: Seth should add physical emergency contact card with this info

### **Service Providers**
- **ISP**: Cox Communications
  - Account #: [TO BE ADDED]
  - Public IP: 70.188.182.126
  - Service: Gigabit cable internet
- **Cloudflare**: 
  - Email: [TO BE ADDED - likely sethpizzaboy@gmail.com]
  - Used for: DNS, CDN, Tunnel (norelec-tunnel)
- **Domain Registrar**: [TO BE ADDED - check domain registrar for lightspeedup.com]

### **Community Support**
- **GitHub**: https://github.com/MatoTeziTanka/Dell-Server-Roadmap
- **Reddit**: sethpizzaboy (active on r/veterans, r/homelabsales)
- **Discord**: [TO BE ADDED if applicable]
- **Twitter**: [TO BE ADDED if applicable]

---

## 📚 DOCUMENT MAINTENANCE

### **Update Policy**
This document MUST be updated whenever:
- ✅ New VM is created
- ✅ VM configuration changes
- ✅ Service is added/removed
- ✅ Password is changed
- ✅ Network configuration changes
- ✅ SHENRON version updates
- ✅ Infrastructure issues discovered

### **Version Control**
- **Location**: /home/mgmt1/GitHub/Dell-Server-Roadmap/ETERNAL-DRAGON-SHENRON-KNOWLEDGE.md
- **Git**: Tracked in Dell-Server-Roadmap repository
- **Backups**: Automatic via GitHub

### **RAG Injection**
This document is designed to be ingested into SHENRON's RAG knowledge base:
1. Save as markdown in `C:\GOKU-AI\knowledge-base\eternal-dragon-complete.md`
2. Run ingestion: `python C:\GOKU-AI\shenron\2-Ingest-Knowledge-Base.py`
3. Restart SHENRON API server
4. SHENRON will now have complete infrastructure knowledge

---

**Document Created**: November 6, 2025  
**Last Updated**: November 6, 2025  
**Maintained By**: Seth Schultz (with AI assistance)  
**Status**: ✅ CURRENT

---

*"So be it. Your wish has been granted!"* ✨  
**— SHENRON, The Eternal Dragon**

