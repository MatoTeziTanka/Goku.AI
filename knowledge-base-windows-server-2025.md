<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Windows Server 2025 Administration Guide for Proxmox VMs
## Complete Documentation for Windows Server 2025 Datacenter & Standard

**Last Updated**: November 6, 2025  
**Editions**: Datacenter, Standard  
**Platform**: Dell R730 + Proxmox VE  
**Use Case**: Domain Controller, Application Server, AI Host (LM Studio)

---

## 🖥️ **WINDOWS SERVER 2025 OVERVIEW**

### **What's New in Windows Server 2025?**
Windows Server 2025 is the latest server operating system from Microsoft, released in late 2024:

**Key Features**:
- ✅ **Enhanced Security**: Advanced threat protection, credential guard improvements
- ✅ **Hybrid Cloud**: Better Azure integration, Azure Arc support
- ✅ **Storage Spaces Direct**: Improved software-defined storage
- ✅ **Hyper-V Enhancements**: Nested virtualization improvements
- ✅ **Active Directory**: New Group Policy features, improved replication
- ✅ **Containers**: Windows Server Core containers, Kubernetes support
- ✅ **PowerShell 7.4+**: Modern scripting with cross-platform support
- ✅ **Windows Admin Center**: Web-based management interface

**Release Date**: Q4 2024  
**Support**: 5 years mainstream + 5 years extended (through 2034)  
**Kernel**: Windows NT 10.0 (Build 26xxx)

---

## 📊 **EDITIONS COMPARISON**

| Feature | **Datacenter** | **Standard** |
|---------|----------------|--------------|
| **VM Rights** | Unlimited VMs | 2 VMs per license |
| **Hyper-V** | Full (unlimited VMs) | Limited (2 VMs) |
| **Storage Spaces Direct** | ✅ Yes | ❌ No |
| **Shielded VMs** | ✅ Yes | ❌ No |
| **Storage Replica** | ✅ Yes | ❌ Limited |
| **Network Controller** | ✅ Yes | ❌ No |
| **Software-Defined Networking** | ✅ Full | ❌ Limited |
| **Clustering** | ✅ Unlimited nodes | ✅ Up to 64 nodes |
| **Price (Retail 2025)** | ~$6,155 | ~$1,069 |

**Recommendation for Your Setup**:
- **Datacenter**: If running many VMs, need Storage Spaces Direct
- **Standard**: If running 1-2 VMs, basic server needs

---

## 💻 **YOUR CURRENT SETUP (VM100)**

### **VM Configuration**
| Attribute | Value |
|-----------|-------|
| **VM ID** | 100 |
| **IP Address** | <VM100_IP> |
| **Role** | Domain Controller + AI Host (LM Studio) |
| **Edition** | Windows Server 2025 Datacenter (assumed) |
| **CPU** | 6-8 cores (from E5-2698 v3) |
| **RAM** | 192 GB (allocated from 480 GB total) |
| **Storage** | Multiple virtual disks (Proxmox) |
| **Network** | Bridged to physical NICs |
| **Domain** | Active Directory Domain Services (ADDS) |
| **Hostname** | VM100 (or custom) |

### **Services Running**
- ✅ Active Directory Domain Services (Domain Controller)
- ✅ DNS Server
- ✅ LM Studio (hosting 6 AI models - DBZ-Warriors)
- ✅ SHENRON Orchestrator (Python Flask API)
- ✅ RAG System (ChromaDB)

---

## 🚀 **INSTALLATION IN PROXMOX**

### **Step 1: Download Windows Server 2025 ISO**

**From Microsoft**:
1. Go to: https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2025
2. Download Evaluation ISO (180-day trial) OR use your license ISO
3. Save to Proxmox: Upload to `local` storage

**From Your License** (if you have access):
- Use ISO from Microsoft Evaluation Center
- OR: Download from your organization's Volume Licensing Service Center (VLSC)

### **Step 2: Create VM in Proxmox**

**Via Proxmox Web GUI**:
```
1. Click "Create VM"
2. General:
   - Node: Select your Proxmox host
   - VM ID: 100 (or your choice)
   - Name: VM100-WinServer2025

3. OS:
   - ISO Image: Select Windows Server 2025 ISO
   - Guest OS Type: Microsoft Windows
   - Version: 11/2022/2025

4. System:
   - Graphic card: Default
   - Machine: q35
   - BIOS: OVMF (UEFI) ← RECOMMENDED
   - Add EFI Disk: Yes
   - Storage: local-lvm
   - SCSI Controller: VirtIO SCSI single
   - Qemu Agent: ✅ Enabled (install later)

5. Disks:
   - Bus/Device: SCSI 0
   - Storage: local-lvm (or your SSD storage)
   - Disk size: 100 GB minimum (200-500 GB recommended)
   - Cache: Write back
   - Discard: ✅ Enabled (for SSD TRIM)
   - SSD emulation: ✅ Enabled

6. CPU:
   - Sockets: 1
   - Cores: 6-8 (for AI workloads, use 8+)
   - Type: host (best performance)

7. Memory:
   - RAM: 16384 MB (16 GB minimum)
   - For AI/LM Studio: 196608 MB (192 GB) ← Your current setup

8. Network:
   - Bridge: vmbr0 (or your bridge)
   - Model: VirtIO (paravirtualized)
   - VLAN Tag: (leave blank unless using VLANs)
   - Firewall: ✅ Enabled (optional)

9. Confirm: Review and click "Finish"
```

**Via Command Line** (faster for advanced users):
```bash
# SSH to Proxmox host
ssh root@<VM200_IP>

# Create VM
qm create 100 \
  --name VM100-WinServer2025 \
  --machine q35 \
  --bios ovmf \
  --cpu host \
  --cores 8 \
  --memory 196608 \
  --scsihw virtio-scsi-single \
  --scsi0 local-lvm:200,cache=writeback,discard=on,ssd=1 \
  --net0 virtio,bridge=vmbr0,firewall=1 \
  --ostype win11 \
  --efidisk0 local-lvm:1,format=raw,efitype=4m,pre-enrolled-keys=0

# Attach Windows Server 2025 ISO
qm set 100 --ide2 local:iso/windows-server-2025.iso,media=cdrom

# Attach VirtIO drivers ISO (required for Windows)
qm set 100 --ide0 local:iso/virtio-win-0.1.240.iso,media=cdrom

# Enable Qemu Agent
qm set 100 --agent enabled=1

# Start VM
qm start 100
```

### **Step 3: Install Windows Server 2025**

**3.1: Boot VM and Start Installation**
```
1. Access VM console (Proxmox Web GUI → VM100 → Console)
2. VM boots from Windows Server 2025 ISO
3. Select language, time, keyboard → Next
4. Click "Install now"
```

**3.2: Choose Edition**
```
Select:
- Windows Server 2025 Datacenter (Desktop Experience)
  OR
- Windows Server 2025 Standard (Desktop Experience)

Note: "Desktop Experience" = GUI
      "Server Core" = Command-line only (advanced)
```

**3.3: Accept License Terms**
```
✅ I accept the Microsoft Software License Terms
Click "Next"
```

**3.4: Installation Type**
```
Select: "Custom: Install Microsoft Server Operating System only (advanced)"
```

**3.5: Load VirtIO Drivers** ⚠️ **CRITICAL STEP**
```
Problem: Windows installer won't see Proxmox virtual disk
Solution: Load VirtIO drivers from second ISO

1. Click "Load driver"
2. Click "Browse"
3. Navigate to E:\ (VirtIO drivers ISO)
4. Select: E:\viostor\2k25\amd64\ (for Windows Server 2025)
5. Click "OK"
6. Select "Red Hat VirtIO SCSI controller"
7. Click "Next"

Now you'll see "Drive 0 Unallocated Space" (200 GB or your size)
```

**3.6: Partition and Install**
```
1. Select "Drive 0 Unallocated Space"
2. Click "New" → "Apply" (creates system partitions automatically)
3. Select primary partition (largest)
4. Click "Next"
5. Installation begins (10-20 minutes)
6. VM will reboot automatically
```

**3.7: Set Administrator Password**
```
After reboot:
1. Enter Administrator password (STRONG password!)
2. Confirm password
3. Click "Finish"
4. Press Ctrl+Alt+Delete to log in (or use "Send CtrlAltDel" button in console)
```

---

## ⚙️ **POST-INSTALLATION CONFIGURATION**

### **Step 1: Install VirtIO Drivers (Additional)**

Windows Server 2025 is now running, but needs additional VirtIO drivers:

```powershell
# In VM, open File Explorer
# Navigate to D:\ (VirtIO drivers ISO)

# Install drivers:
1. Run: D:\virtio-win-guest-tools.exe
2. Install all drivers (network, balloon, serial, etc.)
3. Reboot VM

# Verify drivers installed:
Get-PnpDevice | Where-Object {$_.FriendlyName -like "*VirtIO*"}
```

### **Step 2: Install Qemu Guest Agent**

Enables Proxmox to communicate with VM (shutdown, IP display, etc.):

```powershell
# Still using VirtIO drivers ISO (D:\)
# Navigate to: D:\guest-agent\
# Run: qemu-ga-x86_64.msi
# Install with default options
# Service starts automatically

# Verify agent running:
Get-Service QEMU-GA
# Status should be: Running
```

**After agent install, Proxmox will show VM IP address in summary!**

### **Step 3: Set Static IP Address**

```powershell
# Open PowerShell as Administrator

# View current network adapters
Get-NetAdapter

# Set static IP (example: <VM100_IP>)
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress <VM100_IP> -PrefixLength 24 -DefaultGateway <EDGEROUTER_IP>

# Set DNS servers
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses <EDGEROUTER_IP>,8.8.8.8

# Verify configuration
Get-NetIPConfiguration
```

### **Step 4: Rename Computer**

```powershell
# Rename from generic name to VM100
Rename-Computer -NewName "VM100" -Restart

# VM will reboot automatically
```

### **Step 5: Windows Updates**

```powershell
# Install Windows Update Module
Install-Module PSWindowsUpdate -Force

# Check for updates
Get-WindowsUpdate

# Install all updates
Install-WindowsUpdate -AcceptAll -AutoReboot

# This may take 30-60 minutes and multiple reboots
```

---

## 🏢 **ACTIVE DIRECTORY DOMAIN SERVICES (ADDS)**

### **Installing Domain Controller Role**

**Your VM100 is currently a Domain Controller.** Here's how it was set up:

```powershell
# Install AD DS role
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools

# Promote to Domain Controller (creates new forest)
Install-ADDSForest `
  -DomainName "yourdomain.local" `
  -DomainNetBIOSName "YOURDOMAIN" `
  -ForestMode "WinThreshold" `
  -DomainMode "WinThreshold" `
  -InstallDNS `
  -DatabasePath "C:\Windows\NTDS" `
  -LogPath "C:\Windows\NTDS" `
  -SysvolPath "C:\Windows\SYSVOL" `
  -NoRebootOnCompletion:$false `
  -Force

# VM reboots automatically
# After reboot, VM100 is now a Domain Controller!
```

### **DNS Server Configuration**

Domain Controller automatically installs DNS:

```powershell
# Verify DNS role installed
Get-WindowsFeature | Where-Object {$_.Name -like "*DNS*"}

# View DNS zones
Get-DnsServerZone

# Add forwarders (for external DNS resolution)
Add-DnsServerForwarder -IPAddress 8.8.8.8,1.1.1.1

# Test DNS
nslookup google.com
nslookup VM100.yourdomain.local
```

---

## 🖥️ **REMOTE DESKTOP (RDP) CONFIGURATION**

### **Enable Remote Desktop**

```powershell
# Enable Remote Desktop
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -name "fDenyTSConnections" -value 0

# Enable Remote Desktop through firewall
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"

# For Network Level Authentication (NLA) - more secure
# NLA is enabled by default, to disable (less secure but more compatible):
# Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -name "UserAuthentication" -value 0
```

### **Connect via RDP**

**From Windows**:
```
1. Open Remote Desktop Connection (mstsc.exe)
2. Computer: <VM100_IP>
3. Username: YOURDOMAIN\Administrator (or .\Administrator for local)
4. Password: [your administrator password]
5. Click "Connect"
```

**From Linux/Mac**:
```bash
# Install Remmina or use xfreerdp
xfreerdp /v:<VM100_IP> /u:Administrator /p:YourPassword /cert:ignore /dynamic-resolution

# OR use Remmina GUI (recommended)
remmina
```

---

## 🔒 **SECURITY HARDENING**

### **Windows Firewall**

```powershell
# View firewall status
Get-NetFirewallProfile

# Enable firewall for all profiles
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# Allow specific ports (example: Flask API port 5000)
New-NetFirewallRule -DisplayName "SHENRON API Server" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow

# Allow LM Studio port 1234
New-NetFirewallRule -DisplayName "LM Studio API" -Direction Inbound -LocalPort 1234 -Protocol TCP -Action Allow
```

### **Windows Defender**

```powershell
# Check Windows Defender status
Get-MpComputerStatus

# Update definitions
Update-MpSignature

# Perform full scan
Start-MpScan -ScanType FullScan

# Exclude folders (for performance, e.g., AI models)
Add-MpPreference -ExclusionPath "C:\GOKU-AI"
```

### **User Account Control (UAC)**

```powershell
# Check UAC status (should be enabled for security)
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "EnableLUA"

# UAC is enabled by default (good)
# Only disable if absolutely necessary (NOT RECOMMENDED)
```

---

## 🛠️ **POWERSHELL 7.4+ ADMINISTRATION**

### **Install PowerShell 7.4+**

Windows Server 2025 includes PowerShell 5.1 by default. Install PowerShell 7.4+ for modern features:

```powershell
# Download and install PowerShell 7.4+
winget install --id Microsoft.PowerShell --source winget

# OR via Invoke-WebRequest
$url = "https://github.com/PowerShell/PowerShell/releases/latest/download/PowerShell-7.4.0-win-x64.msi"
Invoke-WebRequest -Uri $url -OutFile "$env:TEMP\PowerShell-7.4.0.msi"
Start-Process msiexec.exe -ArgumentList "/i $env:TEMP\PowerShell-7.4.0.msi /quiet" -Wait

# Launch PowerShell 7
pwsh
```

### **Useful PowerShell Commands**

```powershell
# System information
Get-ComputerInfo

# Disk usage
Get-Volume

# Network configuration
Get-NetIPConfiguration

# Services
Get-Service | Where-Object {$_.Status -eq "Running"}

# Processes
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# Event logs (errors in last 24 hours)
Get-EventLog -LogName System -EntryType Error -After (Get-Date).AddDays(-1)

# Windows updates
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10
```

---

## 📦 **SOFTWARE INSTALLATION**

### **Package Managers**

**Winget** (built-in Windows Package Manager):
```powershell
# Search for package
winget search python

# Install package
winget install Python.Python.3.11

# Upgrade all packages
winget upgrade --all
```

**Chocolatey** (community package manager):
```powershell
# Install Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install packages
choco install git python vscode 7zip -y

# Upgrade all packages
choco upgrade all -y
```

### **Common Software for Your Setup**

```powershell
# Python 3.11 (for SHENRON, LM Studio)
winget install Python.Python.3.11

# Git
winget install Git.Git

# Visual Studio Code
winget install Microsoft.VisualStudioCode

# 7-Zip
winget install 7zip.7zip

# Google Chrome
winget install Google.Chrome

# Notepad++
winget install Notepad++.Notepad++
```

---

## 🤖 **AI WORKLOADS (LM STUDIO & SHENRON)**

### **Your Current AI Setup**

**LM Studio** (hosting 6 AI models):
- Runs on VM100
- Port: 1234 (LM Studio API)
- Models: deepseek-coder, llama, qwen, mistral, phi-3 (6 total)

**SHENRON Orchestrator**:
- Python Flask API
- Port: 5000 (SHENRON API)
- RAG: ChromaDB
- Location: C:\GOKU-AI\shenron\

### **Python Environment Setup**

```powershell
# Navigate to SHENRON directory
cd C:\GOKU-AI\shenron

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install flask chromadb sentence-transformers paramiko

# Run SHENRON API server
python shenron-v4-api-server.py
```

### **Managing AI Services**

```powershell
# Check if LM Studio is running
Get-Process | Where-Object {$_.ProcessName -like "*LM*"}

# Check if SHENRON API is running (Python)
Get-Process | Where-Object {$_.ProcessName -eq "python"}

# Test LM Studio API
Invoke-WebRequest -Uri "http://localhost:1234/v1/models" | Select-Object -Expand Content

# Test SHENRON API
Invoke-WebRequest -Uri "http://localhost:5000/health" | Select-Object -Expand Content
```

---

## 💾 **STORAGE MANAGEMENT**

### **Disk Management**

```powershell
# View disks
Get-Disk

# View partitions
Get-Partition

# View volumes
Get-Volume

# Extend C: drive (if you added more space in Proxmox)
# First, extend disk in Proxmox, then:
$MaxSize = (Get-PartitionSupportedSize -DriveLetter C).SizeMax
Resize-Partition -DriveLetter C -Size $MaxSize
```

### **Storage Spaces**

```powershell
# View storage pools (if using Storage Spaces)
Get-StoragePool

# View virtual disks
Get-VirtualDisk
```

---

## 🌐 **NETWORKING**

### **Network Adapter Configuration**

```powershell
# View adapters
Get-NetAdapter

# View IP configuration
Get-NetIPConfiguration

# Set static IP (if needed)
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress <VM100_IP> -PrefixLength 24 -DefaultGateway <EDGEROUTER_IP>

# Set DNS
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses <VM100_IP>,8.8.8.8

# Test connectivity
Test-NetConnection <EDGEROUTER_IP>
Test-NetConnection google.com -Port 443
```

### **Hyper-V Virtual Switch** (if using Hyper-V inside VM)

```powershell
# Enable nested virtualization (must be done on Proxmox host first)
# On Proxmox host: qm set 100 -cpu host,flags=+vmx

# Create virtual switch
New-VMSwitch -Name "InternalSwitch" -SwitchType Internal
```

---

## 📊 **MONITORING & PERFORMANCE**

### **Performance Monitor**

```powershell
# Open Performance Monitor GUI
perfmon

# View CPU usage
Get-Counter '\Processor(_Total)\% Processor Time'

# View Memory usage
Get-Counter '\Memory\Available MBytes'

# View Disk usage
Get-Counter '\PhysicalDisk(_Total)\% Disk Time'

# View Network usage
Get-Counter '\Network Interface(*)\Bytes Total/sec'
```

### **Resource Monitor**

```powershell
# Open Resource Monitor GUI
resmon

# View top CPU consumers
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, CPU, WS

# View memory usage
Get-Process | Sort-Object WS -Descending | Select-Object -First 10 Name, WS
```

---

## 🔄 **BACKUP & RECOVERY**

### **Proxmox VM Backup**

Best practice: Backup from Proxmox host, not inside VM

```bash
# On Proxmox host
# Backup VM 100
vzdump 100 --storage local --mode snapshot --compress gzip

# Scheduled backups (via Proxmox GUI)
# Datacenter → Backup → Add
# Schedule: Daily at 2 AM
# Storage: local or network storage
```

### **Windows Server Backup** (inside VM)

```powershell
# Install Windows Server Backup feature
Install-WindowsFeature Windows-Server-Backup

# Create backup
wbadmin start backup -backupTarget:D: -include:C: -allCritical -quiet

# View backups
wbadmin get versions
```

---

## 📚 **LEARNING RESOURCES**

### **Official Microsoft Documentation**
- **Windows Server 2025**: https://learn.microsoft.com/en-us/windows-server/
- **Active Directory**: https://learn.microsoft.com/en-us/windows-server/identity/
- **PowerShell**: https://learn.microsoft.com/en-us/powershell/
- **Hyper-V**: https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/

### **Community Resources**
- **Reddit r/sysadmin**: https://www.reddit.com/r/sysadmin/
- **Reddit r/WindowsServer**: https://www.reddit.com/r/WindowsServer/
- **Server Fault**: https://serverfault.com/

---

## ✅ **QUICK REFERENCE: COMMON TASKS**

### **System Administration**
```powershell
# Restart VM
Restart-Computer -Force

# Shutdown VM
Stop-Computer -Force

# Check uptime
(Get-Date) - (gcim Win32_OperatingSystem).LastBootUpTime

# View installed features
Get-WindowsFeature | Where-Object {$_.InstallState -eq "Installed"}

# Install feature
Install-WindowsFeature -Name Web-Server -IncludeManagementTools

# Remove feature
Uninstall-WindowsFeature -Name Web-Server
```

### **User Management** (Domain Controller)
```powershell
# Create new user
New-ADUser -Name "John Doe" -SamAccountName "jdoe" -UserPrincipalName "jdoe@yourdomain.local" -Path "CN=Users,DC=yourdomain,DC=local" -AccountPassword (ConvertTo-SecureString "P@ssw0rd!" -AsPlainText -Force) -Enabled $true

# Add user to group
Add-ADGroupMember -Identity "Domain Admins" -Members "jdoe"

# View users
Get-ADUser -Filter *

# View groups
Get-ADGroup -Filter *
```

---

**Document Created**: November 6, 2025  
**Last Updated**: November 6, 2025  
**Owner**: Seth Schultz - LightSpeedUp Hosting  
**Purpose**: Complete Windows Server 2025 administration guide for Proxmox VMs  
**Usage**: RAG knowledge base for SHENRON AI, human reference, VM configuration guide

**✨ Windows Server 2025 knowledge complete! ✨** 🖥️

