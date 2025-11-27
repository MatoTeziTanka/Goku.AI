<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Dell R730 Server Infrastructure Documentation

## 🏗️ **Network Architecture Overview**

```
Internet → Cox Router (192.168.11.1) → Deeper Network Mini → EdgeRouter (<EDGEROUTER_IP>) → Proxmox Host (<PROXMOX_IP>)
                                                                                            ↓
                                                                                    Virtual Machines
```

## 🌐 **Network Configuration**

### **External Access**
- **Public IP**: 70.188.182.126
- **External Port Forwarding**: Cox Router → EdgeRouter → Services

### **Internal Network (192.168.12.0/24)**
- **Gateway**: <EDGEROUTER_IP> (EdgeRouter)
- **DNS**: 8.8.8.8, 8.8.4.4
- **Proxmox Host**: <PROXMOX_IP>

## 🖥️ **Proxmox Host Configuration**

### **Hardware Specifications**
- **Model**: Dell PowerEdge R730
- **CPU**: Dual Intel Xeon E5-2620 v4 (2.1GHz, 8 cores each)
- **RAM**: 128GB DDR4 ECC
- **Storage**: 
  - SSD Pool: 4x Samsung 3.84TB SSDs (ZFS RAID-Z2)
  - HDD Pool: 4x 3.5TB HDDs (ZFS RAID-Z2)
  - OS Drive: 2x 240GB SSDs (RAID 1)

### **Storage Pools**
- **SSD_VMs**: 6.1TB available (ZFS RAID-Z2)
- **Plex**: 11.6TB available (ZFS RAID-Z2)
- **local-lvm**: 130GB available (LVM thin)

### **Proxmox Access**
- **Web Interface**: https://<PROXMOX_IP>:8006
- **SSH Access**: root@<PROXMOX_IP>
- **SSH Key**: /root/.ssh/id_ed25519 (GitHub key)

## 🖥️ **Virtual Machines Configuration**

### **VM 100 - GOKU-AI / Shenron Syndicate**
- **Status**: Running (Windows Server 2025)
- **IP**: <VM100_IP>
- **MAC**: BC:24:11:D5:FE:35
- **Resources**: 16 cores, 65GB RAM, 500GB SSD
- **Computer Name**: GOKU-AI
- **Purpose**: AI Council / Multi-Model LLM System
- **Access**: Windows RDP (auto-login enabled)
- **Software**: 
  - LM Studio 0.3.31 (auto-start on boot)
  - Microsoft Machine Learning Server 9.4.7
  - Python 3.11 environment
  - SSH/SCP capabilities
- **Loaded Models**:
  - GOKU: DeepSeek-Coder-V2-Lite (163B context, temp 0.7)
  - VEGETA: Llama 3.2 3B (32K context, temp 0.3)
  - PICCOLO: Qwen2.5-Coder 7B (32K context, temp 0.6)
  - GOHAN: Mistral 7B (32K context, temp 0.4)
  - KRILLIN: Phi-3-Mini (32K context, temp 0.5)
  - FRIEZA: Phi-3-Mini:2 (32K context, temp 0.9)

### **VM 120 - Reverse Proxy Gateway**
- **Status**: Running (Ubuntu 24.04 LTS)
- **IP**: <VM120_IP> (nginx, reverse proxy for all public services)
- **MAC**: BC:24:11:87:19:86
- **Resources**: 6 cores, 6GB RAM, 500GB SSD
- **Purpose**: Reverse proxy, SSL termination, load balancing
- **User**: proxy1
- **Hostname**: reverse-proxy-gateway

### **VM 150 - WordPress Hosting**
- **Status**: Running (Ubuntu 24.04 LTS)
- **IP**: <VM150_IP>
- **MAC**: BC:24:11:D3:D0:A6
- **Resources**: 8 cores, 32GB RAM, 500GB SSD
- **Purpose**: WordPress hosting, web development
- **User**: wp1
- **Hostname**: wordpress-1
- **Hosted Sites**:
  - https://lightspeedup.com (Main site + Beta program)
  - https://www.lightspeedup.com (WWW alias)
  - https://wp.lightspeedup.com (WordPress admin access)
  - https://shenron.lightspeedup.com (AI Council web interface)
- **Special Configuration**:
  - Apache 2.4.58 (Virtual hosts for multiple domains)
  - PHP 8.x with increased timeouts for AI responses
  - api.php proxy to VM100's LM Studio API (bypasses CORS)

### **VM 160 - Database Services**
- **Status**: Running (Ubuntu 24.04 LTS)
- **IP**: <VM160_IP>
- **MAC**: BC:24:11:76:05:13
- **Resources**: 8 cores, 32GB RAM, 500GB SSD
- **Purpose**: Database hosting, data services
- **User**: dbs1
- **Hostname**: dbs-1

### **VM 170 - Game Server Hosting**
- **Status**: Running (Ubuntu 24.04 LTS)
- **IP**: <VM170_IP>
- **MAC**: BC:24:11:7E:93:38
- **Resources**: 12 cores, 48GB RAM, 500GB SSD
- **Purpose**: Game server hosting (Minecraft, CS2, etc.)
- **User**: gsh1
- **Hostname**: gsh-1

### **VM 180 - API Services**
- **Status**: Running (Ubuntu 24.04 LTS)
- **IP**: <VM180_IP>
- **MAC**: BC:24:11:F6:7A:33
- **Resources**: 8 cores, 32GB RAM, 500GB SSD
- **Purpose**: API services, microservices, webhooks
- **User**: apis1
- **Hostname**: apis-1

### **VM 200 - Plex Media Server**
- **Status**: Running (Windows Server 2025)
- **IP**: <VM200_IP>
- **MAC**: BC:24:11:D5:FE:35
- **Resources**: 8 cores, 32GB RAM, 500GB SSD
- **Purpose**: Media streaming server
- **Access**: Windows RDP
- **External Access**: http://70.188.182.126:32400

## 🔑 **SSH Key Configuration**

### **GitHub SSH Key**
- **Private Key**: /root/.ssh/id_ed25519
- **Public Key**: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAHzO/boElPfcY/WPcCBT2B7YHgUZj9b7uWkrCxj4vuN MatoTeziTanka@github/134341580
- **GitHub Username**: MatoTeziTanka

### **SSH Access Pattern**
All VMs use the same SSH key for access:
```bash
ssh -i /root/.ssh/id_ed25519 [username]@[vm_ip]
```

## 🌐 **Port Forwarding Configuration**

### **Cox Router → EdgeRouter**
- **External Port**: 32400
- **Internal IP**: EdgeRouter IP on Cox network
- **Internal Port**: 32400

### **EdgeRouter → Services**
- **Port 32400**: Plex Media Server (<VM200_IP>)
- **Port 80/443**: Reverse Proxy (<EDGEROUTER_IP>90) - Configured
  - wp.lightspeedup.com → VM 150 (WordPress)
  - pinball.lightspeedup.com → VM 192 (Atlantis Pinball)
- **Port 22**: SSH access to all VMs
- **Port 3000**: VM 192 - Atlantis Pinball Frontend (internal)
- **Port 8000**: VM 192 - Atlantis Pinball Backend API (internal)

## 🛡️ **Security Configuration**

### **Firewall Status**
- **EdgeRouter**: Default firewall enabled
- **Proxmox**: VM-level firewalls enabled
- **VMs**: UFW enabled on all Ubuntu VMs

### **User Management**
- **Proxmox**: root user with SSH key
- **VMs**: Dedicated users with sudo privileges
- **SSH**: Key-based authentication enabled

## 📊 **Resource Allocation Summary**

| VM ID | Service | CPU | RAM | Storage | IP Address |
|-------|---------|-----|-----|---------|------------|
| 100 | AI Assistant | 8 cores | 32GB | 500GB | <VM100_IP> |
| 120 | Reverse Proxy | 6 cores | 6GB | 500GB | <EDGEROUTER_IP>90 |
| 150 | WordPress | 8 cores | 32GB | 500GB | <VM150_IP> |
| 160 | Database | 8 cores | 32GB | 500GB | <VM160_IP> |
| 170 | Game Servers | 12 cores | 48GB | 500GB | <VM170_IP> |
| 180 | API Services | 8 cores | 32GB | 500GB | <VM180_IP> |
| 192 | Atlantis Pinball | 4 cores | 8GB | 100GB | <VM192_IP> |
| 200 | Plex Server | 8 cores | 32GB | 500GB | <VM200_IP> |

**Total Resources**: 62 cores, 222GB RAM, 3.6TB storage

## 🚀 **Revenue Generation Services Ready**

### **WordPress Hosting** (VM 150)
- **Status**: Ready for deployment
- **Potential Revenue**: $50-200/month per site

### **Game Server Hosting** (VM 170)
- **Status**: Ready for deployment
- **Potential Revenue**: $30-150/month per server

### **API Services** (VM 180)
- **Status**: Ready for deployment
- **Potential Revenue**: $100-500/month per API

### **Database Services** (VM 160)
- **Status**: Ready for deployment
- **Potential Revenue**: $50-300/month per database

## 🔧 **Next Steps**

1. **Configure Reverse Proxy** (VM 120) - Install Nginx + Let's Encrypt
2. **Deploy First Revenue Service** - Choose WordPress, Game Servers, or APIs
3. **Set up SSL Certificates** - Automatic SSL for all services
4. **Configure Monitoring** - Set up monitoring and logging
5. **Launch Services** - Begin revenue generation

## 📝 **Important Notes**

- **Backup Strategy**: ZFS snapshots enabled on all storage pools
- **Network Security**: Deeper Network Mini provides additional protection
- **Scalability**: Easy to add more VMs or resize existing ones
- **Professional Setup**: Enterprise-grade infrastructure ready for commercial use

---

**Last Updated**: October 23, 2025
**Documentation Version**: 1.0

