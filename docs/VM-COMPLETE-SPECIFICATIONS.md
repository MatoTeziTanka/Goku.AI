<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🖥️ **COMPLETE VM SPECIFICATIONS - PRODUCTION VMs**

**Created:** November 4, 2025  
**Purpose:** Complete rebuild specifications for production VMs  
**VMs Documented:** VM150, VM160, VM170, VM180  
**Use Case:** Use this document to rebuild VMs with exact specifications  

---

## 📋 **TABLE OF CONTENTS**

1. [VM150 - WordPress Hosting](#vm150---wordpress-hosting)
2. [VM160 - Database Services](#vm160---database-services)
3. [VM170 - Game Server Hosting](#vm170---game-server-hosting)
4. [VM180 - API Services](#vm180---api-services)
5. [Quick Rebuild Commands](#quick-rebuild-commands)

---

# VM150 - WordPress Hosting

## 🔑 **Authentication & Access**

| Property | Value |
|----------|-------|
| **VM ID** | 150 |
| **Hostname** | WordPress-Hosting-1 |
| **IP Address** | <VM150_IP>/24 |
| **Gateway** | <EDGEROUTER_IP> |
| **DNS** | 8.8.8.8, 8.8.4.4 |
| **Username** | wp1 |
| **Password** | Norelec7! |
| **SSH Access** | `ssh wp1@<VM150_IP>` |
| **Sudo Access** | `echo "<VM_PASSWORD>"  # See credentials.json \| sudo -S <command>` |

---

## 💻 **Hardware Configuration**

### **CPU & Memory**
| Property | Value | Notes |
|----------|-------|-------|
| **CPU Cores** | 8 | Host passthrough |
| **CPU Type** | host | Maximum performance |
| **Sockets** | 1 | Single socket |
| **Memory (RAM)** | 32768 MB (32 GB) | Fixed allocation |
| **Balloon** | 0 (disabled) | No memory ballooning |
| **NUMA** | 1 (enabled) | Optimized for multi-core |

### **Storage Configuration**
| Device | Type | Size | Storage Pool | Options |
|--------|------|------|--------------|---------|
| **scsi0** | Hard Disk | 500G | SSD_VMs | cache=writeback, discard=on, iothread=1, ssd=1 |
| **efidisk0** | EFI Disk | 1M | SSD_VMs | efitype=4m, pre-enrolled-keys=1 |
| **ide2** | CD/DVD | ISO | local | ubuntu-24.04.3-live-server-amd64.iso |

**SCSI Controller:** virtio-scsi-single

**Note:** Current disk is 500 GB but only using ~12 GB. Recommended rebuild size: **100 GB**

### **Network Configuration**
| Property | Value | Notes |
|----------|-------|-------|
| **Interface** | net0 | Primary network |
| **Type** | virtio | High performance |
| **MAC Address** | BC:24:11:D3:D0:A6 | Static assignment |
| **Bridge** | vmbr0 | Client Production Network (eno1) |
| **Firewall** | 1 (enabled) | VM firewall active |

### **System Configuration**
| Property | Value | Notes |
|----------|-------|-------|
| **Machine Type** | q35 | Modern chipset |
| **BIOS** | ovmf (UEFI) | Required for modern OSes |
| **OS Type** | l26 (Linux 2.6+) | Ubuntu 24.04 LTS |
| **VGA** | std | Standard VGA |
| **QEMU Guest Agent** | 1 (enabled) | For better VM management |
| **Auto-Start** | 1 (enabled) | Starts on Proxmox boot |
| **Boot Order** | scsi0 | Boot from primary disk |

### **Identifiers**
| Property | Value |
|----------|-------|
| **SMBIOS UUID** | 559f7e10-7554-47f0-bd9b-a0f51a735bc7 |
| **VM Generation ID** | da513792-45e2-404a-b247-813115a8d768 |
| **Creation Date** | October 22, 2025 (Unix: 1761099905) |
| **QEMU Version** | 9.2.0 |

---

## 🔧 **Cloud-Init Configuration**

| Property | Value |
|----------|-------|
| **Cloud-Init User** | wp1 |
| **Cloud-Init Password** | (Set via cipassword) |
| **IP Config** | ip=<VM150_IP>/24,gw=<EDGEROUTER_IP> |

---

## 📝 **Complete Proxmox Config**

```bash
agent: 1
balloon: 0
bios: ovmf
boot: order=scsi0
cipassword: **********
ciuser: wp1
cores: 8
cpu: host
efidisk0: SSD_VMs:vm-150-disk-1,efitype=4m,pre-enrolled-keys=1,size=1M
ide2: local:iso/ubuntu-24.04.3-live-server-amd64.iso,media=cdrom,size=3226020K
ipconfig0: ip=<VM150_IP>/24,gw=<EDGEROUTER_IP>
machine: q35
memory: 32768
meta: creation-qemu=9.2.0,ctime=1761099905
name: WordPress-Hosting-1
net0: virtio=BC:24:11:D3:D0:A6,bridge=vmbr0,firewall=1
numa: 1
onboot: 1
ostype: l26
scsi0: SSD_VMs:vm-150-disk-2,cache=writeback,discard=on,iothread=1,replicate=0,size=500G,ssd=1
scsihw: virtio-scsi-single
smbios1: uuid=559f7e10-7554-47f0-bd9b-a0f51a735bc7
sockets: 1
vga: std
vmgenid: da513792-45e2-404a-b247-813115a8d768
```

---

## 🔄 **Rebuild Command (Recommended Size)**

```bash
# Create VM with proper 100 GB disk
qm create 150 \
  --name "WordPress-Hosting-1" \
  --cores 8 \
  --sockets 1 \
  --cpu host \
  --memory 32768 \
  --balloon 0 \
  --numa 1 \
  --machine q35 \
  --bios ovmf \
  --ostype l26 \
  --agent 1 \
  --onboot 1 \
  --net0 virtio=BC:24:11:D3:D0:A6,bridge=vmbr0,firewall=1 \
  --scsihw virtio-scsi-single \
  --scsi0 SSD_VMs:100,cache=writeback,discard=on,iothread=1,ssd=1 \
  --efidisk0 SSD_VMs:1,efitype=4m,pre-enrolled-keys=1 \
  --ide2 local:iso/ubuntu-24.04.3-live-server-amd64.iso,media=cdrom \
  --boot order=scsi0 \
  --vga std \
  --ciuser wp1 \
  --cipassword "<VM_PASSWORD>"  # See credentials.json \
  --ipconfig0 ip=<VM150_IP>/24,gw=<EDGEROUTER_IP> \
  --nameserver 8.8.8.8 \
  --nameserver 8.8.4.4
```

---
---

# VM160 - Database Services

## 🔑 **Authentication & Access**

| Property | Value |
|----------|-------|
| **VM ID** | 160 |
| **Hostname** | Discord-Bot-Services-1 |
| **IP Address** | <VM160_IP>/24 |
| **Gateway** | <EDGEROUTER_IP> |
| **DNS** | 8.8.8.8, 8.8.4.4 |
| **Username** | dbs1 |
| **Password** | Norelec7! |
| **SSH Access** | `ssh dbs1@<VM160_IP>` |
| **Sudo Access** | `echo "<VM_PASSWORD>"  # See credentials.json \| sudo -S <command>` |

**⚠️ NOTE:** Proxmox config shows `ciuser: wp1` but actual username is `dbs1`

---

## 💻 **Hardware Configuration**

### **CPU & Memory**
| Property | Value | Notes |
|----------|-------|-------|
| **CPU Cores** | 4 | ⚠️ Documentation says 8 cores |
| **CPU Type** | host | Maximum performance |
| **Sockets** | 1 | Single socket |
| **Memory (RAM)** | 16384 MB (16 GB) | ⚠️ Documentation says 32 GB |
| **Balloon** | 0 (disabled) | No memory ballooning |
| **NUMA** | 1 (enabled) | Optimized for multi-core |

**Recommendation:** If rebuilding, consider using 8 cores / 32 GB as per original specs

### **Storage Configuration**
| Device | Type | Size | Storage Pool | Options |
|--------|------|------|--------------|---------|
| **scsi0** | Hard Disk | 500G | SSD_VMs | cache=writeback, discard=on, iothread=1, ssd=1 |
| **efidisk0** | EFI Disk | 1M | SSD_VMs | efitype=4m, pre-enrolled-keys=1 |
| **ide2** | CD/DVD | ISO | local | ubuntu-24.04.3-live-server-amd64.iso |

**SCSI Controller:** virtio-scsi-single

**Note:** Current disk is 500 GB but only using ~11 GB. Recommended rebuild size: **100 GB**

### **Network Configuration**
| Property | Value | Notes |
|----------|-------|-------|
| **Interface** | net0 | Primary network |
| **Type** | virtio | High performance |
| **MAC Address** | BC:24:11:B3:23:48 | Static assignment |
| **Bridge** | vmbr1 | Personal Services Network (eno2) |
| **Firewall** | 1 (enabled) | VM firewall active |

### **System Configuration**
| Property | Value | Notes |
|----------|-------|-------|
| **Machine Type** | q35 | Modern chipset |
| **BIOS** | ovmf (UEFI) | Required for modern OSes |
| **OS Type** | l26 (Linux 2.6+) | Ubuntu 24.04 LTS |
| **VGA** | std | Standard VGA |
| **QEMU Guest Agent** | 1 (enabled) | For better VM management |
| **Auto-Start** | 1 (enabled) | Starts on Proxmox boot |
| **Boot Order** | scsi0 | Boot from primary disk |

### **Identifiers**
| Property | Value |
|----------|-------|
| **SMBIOS UUID** | 0b584c7b-283c-41ec-a2b6-c31acecac290 |
| **VM Generation ID** | 363dbc89-a423-47d2-b53b-e4b1f882dab5 |
| **Creation Date** | October 22, 2025 (Unix: 1761099905) |
| **QEMU Version** | 9.2.0 |

---

## 📝 **Complete Proxmox Config**

```bash
agent: 1
balloon: 0
bios: ovmf
boot: order=scsi0
cipassword: **********
ciuser: wp1
cores: 4
cpu: host
efidisk0: SSD_VMs:vm-160-disk-0,efitype=4m,pre-enrolled-keys=1,size=1M
ide2: local:iso/ubuntu-24.04.3-live-server-amd64.iso,media=cdrom,size=3226020K
ipconfig0: ip=<VM160_IP>/24,gw=<EDGEROUTER_IP>
machine: q35
memory: 16384
meta: creation-qemu=9.2.0,ctime=1761099905
name: Discord-Bot-Services-1
net0: virtio=BC:24:11:B3:23:48,bridge=vmbr1,firewall=1
numa: 1
onboot: 1
ostype: l26
scsi0: SSD_VMs:vm-160-disk-1,cache=writeback,discard=on,iothread=1,replicate=0,size=500G,ssd=1
scsihw: virtio-scsi-single
smbios1: uuid=0b584c7b-283c-41ec-a2b6-c31acecac290
sockets: 1
vga: std
vmgenid: 363dbc89-a423-47d2-b53b-e4b1f882dab5
```

---

## 🔄 **Rebuild Command (Recommended Size & Specs)**

```bash
# Create VM with proper 100 GB disk and upgraded CPU/RAM
qm create 160 \
  --name "Database-Services-1" \
  --cores 8 \
  --sockets 1 \
  --cpu host \
  --memory 32768 \
  --balloon 0 \
  --numa 1 \
  --machine q35 \
  --bios ovmf \
  --ostype l26 \
  --agent 1 \
  --onboot 1 \
  --net0 virtio=BC:24:11:B3:23:48,bridge=vmbr1,firewall=1 \
  --scsihw virtio-scsi-single \
  --scsi0 SSD_VMs:100,cache=writeback,discard=on,iothread=1,ssd=1 \
  --efidisk0 SSD_VMs:1,efitype=4m,pre-enrolled-keys=1 \
  --ide2 local:iso/ubuntu-24.04.3-live-server-amd64.iso,media=cdrom \
  --boot order=scsi0 \
  --vga std \
  --ciuser dbs1 \
  --cipassword "<VM_PASSWORD>"  # See credentials.json \
  --ipconfig0 ip=<VM160_IP>/24,gw=<EDGEROUTER_IP> \
  --nameserver 8.8.8.8 \
  --nameserver 8.8.4.4
```

---
---

# VM170 - Game Server Hosting

## 🔑 **Authentication & Access**

| Property | Value |
|----------|-------|
| **VM ID** | 170 |
| **Hostname** | Game-Server-Hosting-1 |
| **IP Address** | <VM170_IP>/24 |
| **Gateway** | <EDGEROUTER_IP> |
| **DNS** | 8.8.8.8, 8.8.4.4 |
| **Username** | gsh1 |
| **Password** | Norelec7! |
| **SSH Access** | `ssh gsh1@<VM170_IP>` |
| **Sudo Access** | `echo "<VM_PASSWORD>"  # See credentials.json \| sudo -S <command>` |

**⚠️ NOTE:** Proxmox config shows `ciuser: wp1` but actual username is `gsh1`

---

## 💻 **Hardware Configuration**

### **CPU & Memory**
| Property | Value | Notes |
|----------|-------|-------|
| **CPU Cores** | 12 | High performance for game servers |
| **CPU Type** | host | Maximum performance |
| **Sockets** | 1 | Single socket |
| **Memory (RAM)** | 49152 MB (48 GB) | Large allocation for multiple servers |
| **Balloon** | 0 (disabled) | No memory ballooning |
| **NUMA** | 1 (enabled) | Optimized for multi-core |

### **Storage Configuration**
| Device | Type | Size | Storage Pool | Options |
|--------|------|------|--------------|---------|
| **scsi0** | Hard Disk | 500G | SSD_VMs | cache=writeback, discard=on, iothread=1, ssd=1 |
| **efidisk0** | EFI Disk | 1M | SSD_VMs | efitype=4m, pre-enrolled-keys=1 |
| **ide2** | CD/DVD | ISO | local | ubuntu-24.04.3-live-server-amd64.iso |

**SCSI Controller:** virtio-scsi-single

**Note:** Current disk is 500 GB but only using ~11 GB. Recommended rebuild size: **200 GB**

### **Network Configuration**
| Property | Value | Notes |
|----------|-------|-------|
| **Interface** | net0 | Primary network |
| **Type** | virtio | High performance |
| **MAC Address** | BC:24:11:5F:10:F4 | Static assignment |
| **Bridge** | vmbr1 | Personal Services Network (eno2) |
| **Firewall** | 1 (enabled) | VM firewall active |

### **System Configuration**
| Property | Value | Notes |
|----------|-------|-------|
| **Machine Type** | q35 | Modern chipset |
| **BIOS** | ovmf (UEFI) | Required for modern OSes |
| **OS Type** | l26 (Linux 2.6+) | Ubuntu 24.04 LTS |
| **VGA** | std | Standard VGA |
| **QEMU Guest Agent** | 1 (enabled) | For better VM management |
| **Auto-Start** | 1 (enabled) | Starts on Proxmox boot |
| **Boot Order** | scsi0 | Boot from primary disk |

### **Identifiers**
| Property | Value |
|----------|-------|
| **SMBIOS UUID** | fd525d1f-42c5-48d6-ad20-33b85ec47bf8 |
| **VM Generation ID** | a2bdc501-bac4-4a48-940f-f020b0533f0c |
| **Creation Date** | October 22, 2025 (Unix: 1761099905) |
| **QEMU Version** | 9.2.0 |

---

## 📝 **Complete Proxmox Config**

```bash
agent: 1
balloon: 0
bios: ovmf
boot: order=scsi0
cipassword: **********
ciuser: wp1
cores: 12
cpu: host
efidisk0: SSD_VMs:vm-170-disk-0,efitype=4m,pre-enrolled-keys=1,size=1M
ide2: local:iso/ubuntu-24.04.3-live-server-amd64.iso,media=cdrom,size=3226020K
ipconfig0: ip=<VM170_IP>/24,gw=<EDGEROUTER_IP>
machine: q35
memory: 49152
meta: creation-qemu=9.2.0,ctime=1761099905
name: Game-Server-Hosting-1
net0: virtio=BC:24:11:5F:10:F4,bridge=vmbr1,firewall=1
numa: 1
onboot: 1
ostype: l26
scsi0: SSD_VMs:vm-170-disk-1,cache=writeback,discard=on,iothread=1,replicate=0,size=500G,ssd=1
scsihw: virtio-scsi-single
smbios1: uuid=fd525d1f-42c5-48d6-ad20-33b85ec47bf8
sockets: 1
vga: std
vmgenid: a2bdc501-bac4-4a48-940f-f020b0533f0c
```

---

## 🔄 **Rebuild Command (Recommended Size)**

```bash
# Create VM with proper 200 GB disk for game servers
qm create 170 \
  --name "Game-Server-Hosting-1" \
  --cores 12 \
  --sockets 1 \
  --cpu host \
  --memory 49152 \
  --balloon 0 \
  --numa 1 \
  --machine q35 \
  --bios ovmf \
  --ostype l26 \
  --agent 1 \
  --onboot 1 \
  --net0 virtio=BC:24:11:5F:10:F4,bridge=vmbr1,firewall=1 \
  --scsihw virtio-scsi-single \
  --scsi0 SSD_VMs:200,cache=writeback,discard=on,iothread=1,ssd=1 \
  --efidisk0 SSD_VMs:1,efitype=4m,pre-enrolled-keys=1 \
  --ide2 local:iso/ubuntu-24.04.3-live-server-amd64.iso,media=cdrom \
  --boot order=scsi0 \
  --vga std \
  --ciuser gsh1 \
  --cipassword "<VM_PASSWORD>"  # See credentials.json \
  --ipconfig0 ip=<VM170_IP>/24,gw=<EDGEROUTER_IP> \
  --nameserver 8.8.8.8 \
  --nameserver 8.8.4.4
```

---
---

# VM180 - API Services

## 🔑 **Authentication & Access**

| Property | Value |
|----------|-------|
| **VM ID** | 180 |
| **Hostname** | API-Services-1 |
| **IP Address** | <VM180_IP>/24 |
| **Gateway** | <EDGEROUTER_IP> |
| **DNS** | 8.8.8.8, 8.8.4.4 |
| **Username** | apis1 |
| **Password** | Norelec7! |
| **SSH Access** | `ssh apis1@<VM180_IP>` |
| **Sudo Access** | `echo "<VM_PASSWORD>"  # See credentials.json \| sudo -S <command>` |

**⚠️ NOTE:** Proxmox config shows `ciuser: wp1` but actual username is `apis1`

---

## 💻 **Hardware Configuration**

### **CPU & Memory**
| Property | Value | Notes |
|----------|-------|-------|
| **CPU Cores** | 6 | Medium performance |
| **CPU Type** | host | Maximum performance |
| **Sockets** | 1 | Single socket |
| **Memory (RAM)** | 24576 MB (24 GB) | Medium allocation |
| **Balloon** | 0 (disabled) | No memory ballooning |
| **NUMA** | 1 (enabled) | Optimized for multi-core |

### **Storage Configuration**
| Device | Type | Size | Storage Pool | Options |
|--------|------|------|--------------|---------|
| **scsi0** | Hard Disk | 500G | SSD_VMs | cache=writeback, discard=on, iothread=1, ssd=1 |
| **efidisk0** | EFI Disk | 1M | SSD_VMs | efitype=4m, pre-enrolled-keys=1 |
| **ide2** | CD/DVD | ISO | local | ubuntu-24.04.3-live-server-amd64.iso |

**SCSI Controller:** virtio-scsi-single

**Note:** Current disk is 500 GB. Recommended rebuild size: **100 GB**

### **Network Configuration**
| Property | Value | Notes |
|----------|-------|-------|
| **Interface** | net0 | Primary network |
| **Type** | virtio | High performance |
| **MAC Address** | BC:24:11:69:20:FD | Static assignment |
| **Bridge** | vmbr1 | Personal Services Network (eno2) |
| **Firewall** | 1 (enabled) | VM firewall active |

### **System Configuration**
| Property | Value | Notes |
|----------|-------|-------|
| **Machine Type** | q35 | Modern chipset |
| **BIOS** | ovmf (UEFI) | Required for modern OSes |
| **OS Type** | l26 (Linux 2.6+) | Ubuntu 24.04 LTS |
| **VGA** | std | Standard VGA |
| **QEMU Guest Agent** | 1 (enabled) | For better VM management |
| **Auto-Start** | 1 (enabled) | Starts on Proxmox boot |
| **Boot Order** | scsi0 | Boot from primary disk |

### **Identifiers**
| Property | Value |
|----------|-------|
| **SMBIOS UUID** | 691385b9-fc05-48c8-ada4-7e1c312f98ec |
| **VM Generation ID** | a7b6d6ee-3750-489c-a351-8cfcb4e7e14d |
| **Creation Date** | October 22, 2025 (Unix: 1761099905) |
| **QEMU Version** | 9.2.0 |

---

## 📝 **Complete Proxmox Config**

```bash
agent: 1
balloon: 0
bios: ovmf
boot: order=scsi0
cipassword: **********
ciuser: wp1
cores: 6
cpu: host
efidisk0: SSD_VMs:vm-180-disk-0,efitype=4m,pre-enrolled-keys=1,size=1M
ide2: local:iso/ubuntu-24.04.3-live-server-amd64.iso,media=cdrom,size=3226020K
ipconfig0: ip=<VM180_IP>/24,gw=<EDGEROUTER_IP>
machine: q35
memory: 24576
meta: creation-qemu=9.2.0,ctime=1761099905
name: API-Services-1
net0: virtio=BC:24:11:69:20:FD,bridge=vmbr1,firewall=1
numa: 1
onboot: 1
ostype: l26
scsi0: SSD_VMs:vm-180-disk-1,cache=writeback,discard=on,iothread=1,replicate=0,size=500G,ssd=1
scsihw: virtio-scsi-single
smbios1: uuid=691385b9-fc05-48c8-ada4-7e1c312f98ec
sockets: 1
vga: std
vmgenid: a7b6d6ee-3750-489c-a351-8cfcb4e7e14d
```

---

## 🔄 **Rebuild Command (Recommended Size)**

```bash
# Create VM with proper 100 GB disk
qm create 180 \
  --name "API-Services-1" \
  --cores 6 \
  --sockets 1 \
  --cpu host \
  --memory 24576 \
  --balloon 0 \
  --numa 1 \
  --machine q35 \
  --bios ovmf \
  --ostype l26 \
  --agent 1 \
  --onboot 1 \
  --net0 virtio=BC:24:11:69:20:FD,bridge=vmbr1,firewall=1 \
  --scsihw virtio-scsi-single \
  --scsi0 SSD_VMs:100,cache=writeback,discard=on,iothread=1,ssd=1 \
  --efidisk0 SSD_VMs:1,efitype=4m,pre-enrolled-keys=1 \
  --ide2 local:iso/ubuntu-24.04.3-live-server-amd64.iso,media=cdrom \
  --boot order=scsi0 \
  --vga std \
  --ciuser apis1 \
  --cipassword "<VM_PASSWORD>"  # See credentials.json \
  --ipconfig0 ip=<VM180_IP>/24,gw=<EDGEROUTER_IP> \
  --nameserver 8.8.8.8 \
  --nameserver 8.8.4.4
```

---
---

# Quick Rebuild Commands

## 📋 **Rebuild All 4 VMs with Proper Disk Sizes**

**⚠️ WARNING:** This will DELETE existing VMs and create new ones. Backup data first!

```bash
# SSH into Proxmox host
ssh root@<PROXMOX_IP>

# Backup VMs first (recommended)
vzdump 150 --mode snapshot --compress gzip --storage local
vzdump 160 --mode snapshot --compress gzip --storage local
vzdump 170 --mode snapshot --compress gzip --storage local
vzdump 180 --mode snapshot --compress gzip --storage local

# Stop and destroy old VMs
qm stop 150 && qm destroy 150
qm stop 160 && qm destroy 160
qm stop 170 && qm destroy 170
qm stop 180 && qm destroy 180

# Rebuild VM150 (WordPress) - 100 GB
qm create 150 \
  --name "WordPress-Hosting-1" \
  --cores 8 --sockets 1 --cpu host \
  --memory 32768 --balloon 0 --numa 1 \
  --machine q35 --bios ovmf --ostype l26 \
  --agent 1 --onboot 1 \
  --net0 virtio=BC:24:11:D3:D0:A6,bridge=vmbr0,firewall=1 \
  --scsihw virtio-scsi-single \
  --scsi0 SSD_VMs:100,cache=writeback,discard=on,iothread=1,ssd=1 \
  --efidisk0 SSD_VMs:1,efitype=4m,pre-enrolled-keys=1 \
  --ide2 local:iso/ubuntu-24.04.3-live-server-amd64.iso,media=cdrom \
  --boot order=scsi0 --vga std \
  --ciuser wp1 --cipassword "<VM_PASSWORD>"  # See credentials.json \
  --ipconfig0 ip=<VM150_IP>/24,gw=<EDGEROUTER_IP> \
  --nameserver 8.8.8.8 --nameserver 8.8.4.4

# Rebuild VM160 (Database) - 100 GB with upgraded CPU/RAM
qm create 160 \
  --name "Database-Services-1" \
  --cores 8 --sockets 1 --cpu host \
  --memory 32768 --balloon 0 --numa 1 \
  --machine q35 --bios ovmf --ostype l26 \
  --agent 1 --onboot 1 \
  --net0 virtio=BC:24:11:B3:23:48,bridge=vmbr1,firewall=1 \
  --scsihw virtio-scsi-single \
  --scsi0 SSD_VMs:100,cache=writeback,discard=on,iothread=1,ssd=1 \
  --efidisk0 SSD_VMs:1,efitype=4m,pre-enrolled-keys=1 \
  --ide2 local:iso/ubuntu-24.04.3-live-server-amd64.iso,media=cdrom \
  --boot order=scsi0 --vga std \
  --ciuser dbs1 --cipassword "<VM_PASSWORD>"  # See credentials.json \
  --ipconfig0 ip=<VM160_IP>/24,gw=<EDGEROUTER_IP> \
  --nameserver 8.8.8.8 --nameserver 8.8.4.4

# Rebuild VM170 (Game Servers) - 200 GB
qm create 170 \
  --name "Game-Server-Hosting-1" \
  --cores 12 --sockets 1 --cpu host \
  --memory 49152 --balloon 0 --numa 1 \
  --machine q35 --bios ovmf --ostype l26 \
  --agent 1 --onboot 1 \
  --net0 virtio=BC:24:11:5F:10:F4,bridge=vmbr1,firewall=1 \
  --scsihw virtio-scsi-single \
  --scsi0 SSD_VMs:200,cache=writeback,discard=on,iothread=1,ssd=1 \
  --efidisk0 SSD_VMs:1,efitype=4m,pre-enrolled-keys=1 \
  --ide2 local:iso/ubuntu-24.04.3-live-server-amd64.iso,media=cdrom \
  --boot order=scsi0 --vga std \
  --ciuser gsh1 --cipassword "<VM_PASSWORD>"  # See credentials.json \
  --ipconfig0 ip=<VM170_IP>/24,gw=<EDGEROUTER_IP> \
  --nameserver 8.8.8.8 --nameserver 8.8.4.4

# Rebuild VM180 (API Services) - 100 GB
qm create 180 \
  --name "API-Services-1" \
  --cores 6 --sockets 1 --cpu host \
  --memory 24576 --balloon 0 --numa 1 \
  --machine q35 --bios ovmf --ostype l26 \
  --agent 1 --onboot 1 \
  --net0 virtio=BC:24:11:69:20:FD,bridge=vmbr1,firewall=1 \
  --scsihw virtio-scsi-single \
  --scsi0 SSD_VMs:100,cache=writeback,discard=on,iothread=1,ssd=1 \
  --efidisk0 SSD_VMs:1,efitype=4m,pre-enrolled-keys=1 \
  --ide2 local:iso/ubuntu-24.04.3-live-server-amd64.iso,media=cdrom \
  --boot order=scsi0 --vga std \
  --ciuser apis1 --cipassword "<VM_PASSWORD>"  # See credentials.json \
  --ipconfig0 ip=<VM180_IP>/24,gw=<EDGEROUTER_IP> \
  --nameserver 8.8.8.8 --nameserver 8.8.4.4

# Start all VMs
qm start 150
qm start 160
qm start 170
qm start 180

# Wait for cloud-init to complete (2-3 minutes)
sleep 180

# Verify SSH access
ssh wp1@<VM150_IP> "hostname && df -h /"
ssh dbs1@<VM160_IP> "hostname && df -h /"
ssh gsh1@<VM170_IP> "hostname && df -h /"
ssh apis1@<VM180_IP> "hostname && df -h /"
```

---

## 📊 **Disk Space Comparison**

| VM | Current Allocation | Actual Usage | Recommended | Space Saved |
|----|-------------------|--------------|-------------|-------------|
| VM150 | 500 GB | 12 GB | 100 GB | 400 GB |
| VM160 | 500 GB | 11 GB | 100 GB | 400 GB |
| VM170 | 500 GB | 11 GB | 200 GB | 300 GB |
| VM180 | 500 GB | - | 100 GB | 400 GB |
| **TOTAL** | **2,000 GB** | **~34 GB** | **500 GB** | **1,500 GB** |

**Total Space Reclaimed:** ~1.5 TB

---

## 🎯 **Key Differences from Current Config**

### **VM150 (WordPress):**
- ✅ No changes to CPU/RAM (8 cores, 32 GB is correct)
- ✅ Disk reduced: 500 GB → 100 GB
- ✅ Network correct: vmbr0 (Client Production)

### **VM160 (Database):**
- ⬆️ **CPU upgraded:** 4 cores → 8 cores (as per docs)
- ⬆️ **RAM upgraded:** 16 GB → 32 GB (as per docs)
- ✅ Disk reduced: 500 GB → 100 GB
- ✅ Network correct: vmbr1 (Personal Services)
- 🔧 **Username fixed:** ciuser changed to `dbs1` (was incorrectly `wp1`)

### **VM170 (Game Servers):**
- ✅ No changes to CPU/RAM (12 cores, 48 GB is correct)
- ✅ Disk reduced: 500 GB → 200 GB (larger for game server data)
- ✅ Network correct: vmbr1 (Personal Services)
- 🔧 **Username fixed:** ciuser changed to `gsh1` (was incorrectly `wp1`)

### **VM180 (API Services):**
- ✅ No changes to CPU/RAM (6 cores, 24 GB is appropriate)
- ✅ Disk reduced: 500 GB → 100 GB
- ✅ Network correct: vmbr1 (Personal Services)
- 🔧 **Username fixed:** ciuser changed to `apis1` (was incorrectly `wp1`)

---

## ⚠️ **CRITICAL NOTES**

### **Cloud-Init Username Issue:**
All VMs except VM150 have `ciuser: wp1` in Proxmox config, but the actual usernames are different:
- VM150: `wp1` ✅ (correct)
- VM160: Should be `dbs1` ❌ (incorrect in Proxmox)
- VM170: Should be `gsh1` ❌ (incorrect in Proxmox)
- VM180: Should be `apis1` ❌ (incorrect in Proxmox)

**This is likely why SSH deployment failed for some VMs!**

### **When to Rebuild:**
- ✅ **DO NOT rebuild before Beta launch** (Nov 5, 2025)
- ✅ **Plan for post-Beta maintenance window** (December 2025)
- ✅ **Test rebuild on one VM first** (suggest VM180 since it needs reprovisioning anyway)

---

## 📝 **Post-Rebuild Checklist**

After rebuilding each VM:
1. ✅ Verify SSH access: `ssh <user>@<ip>`
2. ✅ Check disk size: `df -h /`
3. ✅ Verify network connectivity: `ping 8.8.8.8`
4. ✅ Update packages: `sudo apt update && sudo apt upgrade -y`
5. ✅ Install essential packages: `sudo apt install -y curl wget git vim ufw`
6. ✅ Configure UFW firewall
7. ✅ Add VM101 SSH key: `echo "ssh-rsa AAAAB3Nza..." >> ~/.ssh/authorized_keys`
8. ✅ Restore application data from backup
9. ✅ Verify services are running
10. ✅ Update documentation

---

**Document Location:** `/home/mgmt1/GitHub/Dell-Server-Roadmap/docs/VM-COMPLETE-SPECIFICATIONS.md`  
**Created:** November 4, 2025  
**Use Case:** Complete VM rebuild reference with all specifications  

**Related Documents:**
- `/home/mgmt1/VM-DISK-SIZE-AUDIT.md` - Disk size analysis
- `/home/mgmt1/GitHub/Dell-Server-Roadmap/docs/SSH-KEYS-BACKUP.md` - SSH key inventory
- `/home/mgmt1/FINAL-STATUS-REPORT.md` - Current infrastructure status


