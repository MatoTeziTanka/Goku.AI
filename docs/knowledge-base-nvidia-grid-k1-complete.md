<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# NVIDIA GRID K1 Complete GPU Guide for Proxmox & Dell R730
## Comprehensive Documentation for GPU Passthrough & Virtualization

**Last Updated**: November 6, 2025  
**System**: Dell PowerEdge R730 (Service Tag: F93LB42)  
**GPU**: 4x NVIDIA GRID K1 (GK107GL) in PCIe Slot 4  
**Use Case**: GPU passthrough to VMs in Proxmox VE

---

## 🎮 **NVIDIA GRID K1 OVERVIEW**

### **What is NVIDIA GRID K1?**
The NVIDIA GRID K1 is a **professional virtualization GPU** designed for:
- **Virtual Desktop Infrastructure (VDI)** - Multiple virtual desktops per GPU
- **GPU-accelerated applications** - CAD, video editing, graphics workloads
- **GPU passthrough** - Dedicate GPU to specific VMs
- **vGPU technology** - Share GPU among multiple VMs (requires vGPU license)

**Not ideal for**: Modern AI/ML workloads (Kepler architecture, older generation)

---

## 📊 **TECHNICAL SPECIFICATIONS**

### **GPU Architecture**
| Specification | Value |
|---------------|-------|
| **Architecture** | Kepler (GK107GL) |
| **Manufacturing Process** | 28nm |
| **Release Date** | 2013 |
| **Form Factor** | PCIe Full-height, dual-slot |
| **PCIe Interface** | PCIe 3.0 x16 |
| **TDP** | 130W (total card) |

### **GPU Configuration (Per Card)**
| Specification | Value |
|---------------|-------|
| **GPUs per Card** | 4 (quad-GPU design) |
| **GPU Model** | GK107 (Kepler) |
| **CUDA Cores per GPU** | 192 |
| **Total CUDA Cores** | 768 (4 × 192) |
| **Base Clock** | 850 MHz |
| **Boost Clock** | 875 MHz |
| **Memory per GPU** | 4 GB GDDR5 |
| **Total Memory** | 16 GB GDDR5 (4 × 4 GB) |
| **Memory Interface** | 128-bit per GPU |
| **Memory Bandwidth** | 40 GB/s per GPU (160 GB/s total) |
| **Memory Clock** | 1250 MHz (5.0 Gbps effective) |

### **Compute Capabilities**
| Feature | Value |
|---------|-------|
| **CUDA Compute Capability** | 3.5 |
| **DirectX** | 11.2 |
| **OpenGL** | 4.6 |
| **Vulkan** | 1.3 (with latest drivers) |
| **OpenCL** | 1.2 / 3.0 (with latest drivers) |
| **CUDA SDK** | Up to CUDA 11.x (limited support) |
| **Shader Model** | 5.1 |

### **Video Encoding/Decoding (NVENC/NVDEC)**
- **H.264 Encode**: Yes (1st gen NVENC)
- **H.264 Decode**: Yes (NVDEC)
- **H.265/HEVC**: Limited support (encode only with driver updates)
- **Max Streams**: 2-4 simultaneous encode streams per GPU
- **Use Case**: Video transcoding, streaming, recording

### **Display Outputs**
- **Outputs**: None (headless design for VDI)
- **Max Virtual Displays**: Up to 16 per card (vGPU mode)

---

## 🖥️ **YOUR CONFIGURATION (Dell R730)**

### **Current Setup**
| Attribute | Value |
|-----------|-------|
| **Server Model** | Dell PowerEdge R730 |
| **PCIe Slot** | Slot 4 (x16, PCIe 3.0) |
| **Number of GPUs** | 4 (on single card) |
| **Total CUDA Cores** | 768 |
| **Total VRAM** | 16 GB GDDR5 |
| **Power Draw** | 130W |
| **Status** | ✅ Installed, ❌ Not configured for passthrough |

### **PCIe Device Information**
```bash
# From Proxmox host
lspci | grep -i nvidia

# Expected output (example):
# 83:00.0 VGA compatible controller: NVIDIA Corporation GK107GL [GRID K1] (rev a1)
# 84:00.0 VGA compatible controller: NVIDIA Corporation GK107GL [GRID K1] (rev a1)
# 85:00.0 VGA compatible controller: NVIDIA Corporation GK107GL [GRID K1] (rev a1)
# 86:00.0 VGA compatible controller: NVIDIA Corporation GK107GL [GRID K1] (rev a1)
```

**Device IDs**: 10de:0ff2 (NVIDIA GK107GL GRID K1)

---

## 🚀 **GPU PASSTHROUGH STRATEGIES**

### **Strategy 1: Full GPU Passthrough (Recommended for Proxmox)**
**What it does**: Passes entire GPU to a single VM (exclusive access)  
**Best for**: Windows VMs, Linux VMs, GPU-intensive applications  
**Pros**: 
- ✅ No licensing required
- ✅ Full GPU performance
- ✅ Easier to configure
- ✅ Works with open-source drivers

**Cons**:
- ❌ 1 GPU = 1 VM (not shared)
- ❌ VM must be stopped to reclaim GPU

**Use Case**: Your Windows Server 2025 or Ubuntu VMs can get dedicated GPU

### **Strategy 2: vGPU (Virtual GPU Sharing)**
**What it does**: Splits GPU into multiple virtual GPUs (shared among VMs)  
**Best for**: VDI deployments, multiple light GPU workloads  
**Pros**:
- ✅ Multiple VMs per GPU (4-16 VMs per K1 card)
- ✅ Dynamic allocation
- ✅ Ideal for VDI

**Cons**:
- ❌ Requires NVIDIA vGPU license ($$$)
- ❌ Requires NVIDIA vGPU Manager software
- ❌ More complex setup
- ❌ Not available in Proxmox (VMware/Citrix/Nutanix only)

**Use Case**: Not recommended for your setup (licensing cost)

### **Strategy 3: GPU Compute Passthrough (MIG-like)**
**What it does**: Pass GPU for compute only (no display)  
**Best for**: CUDA workloads, ML training (legacy), video encoding  
**Use Case**: Your GPUs for video transcoding in Plex/Jellyfin VM

---

## 🛠️ **PROXMOX GPU PASSTHROUGH SETUP (STEP-BY-STEP)**

### **PREREQUISITES**

1. **BIOS Settings on Dell R730** ✅
   - Intel VT-x: Enabled (already enabled)
   - Intel VT-d: Enabled (check in BIOS)
   - SR-IOV: Enabled (optional, for advanced features)
   - Access: iDRAC → BIOS Configuration → Virtualization Settings

2. **Proxmox VE Installed** ✅
   - Version: 8.x or later recommended
   - Already running on your Dell R730

3. **Backup VMs** ⚠️
   - Always backup VMs before major configuration changes

---

### **STEP 1: Enable IOMMU in Proxmox**

**1.1: Edit GRUB Configuration**
```bash
# SSH to Proxmox host (<VM200_IP>)
ssh root@<VM200_IP>

# Edit GRUB config
nano /etc/default/grub

# Find this line:
GRUB_CMDLINE_LINUX_DEFAULT="quiet"

# Change to:
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt"

# For some systems, you may also need:
# GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt pcie_acs_override=downstream,multifunction"

# Save and exit (Ctrl+X, Y, Enter)

# Update GRUB
update-grub

# Reboot Proxmox host
reboot
```

**1.2: Verify IOMMU is Enabled**
```bash
# After reboot, check IOMMU status
dmesg | grep -e DMAR -e IOMMU

# Expected output:
# DMAR: IOMMU enabled
# DMAR: Intel(R) Virtualization Technology for Directed I/O

# Check IOMMU groups
find /sys/kernel/iommu_groups/ -type l

# Should show multiple IOMMU groups (one per device)
```

---

### **STEP 2: Load VFIO Modules**

**2.1: Add VFIO Modules to Load at Boot**
```bash
# Edit modules file
nano /etc/modules

# Add these lines:
vfio
vfio_iommu_type1
vfio_pci
vfio_virqfd

# Save and exit
```

**2.2: Blacklist NVIDIA Drivers (Prevent Host from Using GPU)**
```bash
# Create blacklist file
nano /etc/modprobe.d/blacklist-nvidia.conf

# Add these lines:
blacklist nouveau
blacklist nvidia
blacklist nvidiafb
blacklist nvidia_drm
blacklist nvidia_modeset

# Save and exit
```

**2.3: Configure VFIO for NVIDIA GRID K1**
```bash
# Create VFIO config file
nano /etc/modprobe.d/vfio.conf

# Add this line (NVIDIA GRID K1 device ID):
options vfio-pci ids=10de:0ff2

# Save and exit

# Update initramfs
update-initramfs -u -k all

# Reboot
reboot
```

**2.4: Verify VFIO Loaded**
```bash
# After reboot, verify VFIO is using the GPU
lspci -nnk | grep -A 3 NVIDIA

# Expected output should show:
# Kernel driver in use: vfio-pci
# (NOT nouveau or nvidia)
```

---

### **STEP 3: Identify GPU PCIe Address**

**3.1: Find GPU PCIe IDs**
```bash
# List all NVIDIA GPUs with PCIe addresses
lspci | grep -i nvidia

# Example output:
# 83:00.0 VGA compatible controller: NVIDIA Corporation GK107GL [GRID K1] (rev a1)
# 84:00.0 VGA compatible controller: NVIDIA Corporation GK107GL [GRID K1] (rev a1)
# 85:00.0 VGA compatible controller: NVIDIA Corporation GK107GL [GRID K1] (rev a1)
# 86:00.0 VGA compatible controller: NVIDIA Corporation GK107GL [GRID K1] (rev a1)

# PCIe addresses: 83:00.0, 84:00.0, 85:00.0, 86:00.0
```

**3.2: Check IOMMU Groups**
```bash
# Check which IOMMU group each GPU is in
for d in $(find /sys/kernel/iommu_groups/ -type l | sort -n -t / -k 5); do
    n=${d#*/iommu_groups/*}; n=${n%%/*}
    printf 'IOMMU group %s ' "$n"
    lspci -nns "${d##*/}"
done | grep NVIDIA

# Ideally, each GPU should be in its own IOMMU group
# If multiple devices share a group, you may need ACS override patch
```

---

### **STEP 4: Passthrough GPU to VM (Proxmox Web GUI)**

**4.1: Shutdown Target VM**
```bash
# Example: VM 100 (Windows Server 2025)
qm stop 100
```

**4.2: Add GPU to VM via Command Line**
```bash
# Add GPU 1 (PCIe 83:00.0) to VM 100
qm set 100 -hostpci0 83:00.0,pcie=1,rombar=0

# Add GPU 2 (PCIe 84:00.0) to VM 101 (if you have another VM)
# qm set 101 -hostpci0 84:00.0,pcie=1,rombar=0

# Parameters:
# -hostpci0: First PCIe passthrough device (use hostpci1, hostpci2 for more)
# pcie=1: Enable PCIe passthrough
# rombar=0: Disable ROM BAR (fixes some GPU passthrough issues)
```

**4.3: Verify GPU Added to VM**
```bash
# Check VM config
qm config 100 | grep hostpci

# Expected output:
# hostpci0: 83:00.0,pcie=1,rombar=0
```

---

### **STEP 5: Configure VM Settings for GPU**

**5.1: Set Machine Type (Important!)**
```bash
# Set machine type to q35 (required for PCIe passthrough)
qm set 100 -machine q35

# Verify
qm config 100 | grep machine
# Output: machine: q35
```

**5.2: Set BIOS to OVMF (UEFI) - Recommended**
```bash
# For UEFI boot (better GPU support)
qm set 100 -bios ovmf

# Add EFI disk if not already present
qm set 100 -efidisk0 local-lvm:1,format=raw,efitype=4m,pre-enrolled-keys=0

# Note: You may need to reinstall OS or convert existing VM to UEFI
```

**5.3: Increase VM RAM (GPU needs RAM)**
```bash
# GRID K1 has 4 GB VRAM, give VM at least 8-16 GB RAM
qm set 100 -memory 16384

# Verify
qm config 100 | grep memory
```

**5.4: Set CPU Type (Host for Best Performance)**
```bash
# Use host CPU passthrough for best performance
qm set 100 -cpu host

# Verify
qm config 100 | grep cpu
```

---

### **STEP 6: Start VM and Install GPU Drivers**

**6.1: Start VM**
```bash
# Start VM
qm start 100

# Access VM console (Proxmox Web GUI or noVNC)
```

**6.2: Install NVIDIA Drivers (Windows)**

**For Windows Server 2025 / Windows 11:**
1. Boot into Windows
2. Open Device Manager → Should see "Microsoft Basic Display Adapter" or "Unknown Device"
3. Download NVIDIA GRID K1 drivers:
   - Go to: https://www.nvidia.com/Download/index.aspx
   - Product Type: GRID
   - Product Series: GRID K-Series
   - Product: GRID K1
   - Operating System: Windows Server 2025 / Windows 11
   - Download Type: Production Branch
   - Click "Search"
4. Install driver (typical installation)
5. Reboot VM
6. Verify: `nvidia-smi` in PowerShell should show GPU

**6.3: Install NVIDIA Drivers (Ubuntu/Linux)**

**For Ubuntu 22.04 / 24.04:**
```bash
# SSH into Ubuntu VM or use console

# Update package list
sudo apt update

# Install NVIDIA driver (proprietary)
sudo apt install nvidia-driver-535 -y
# Or use nvidia-driver-470 for older GRID K1

# Reboot VM
sudo reboot

# After reboot, verify GPU
nvidia-smi

# Expected output:
# +-----------------------------------------------------------------------------+
# | NVIDIA-SMI 535.xx.xx    Driver Version: 535.xx.xx    CUDA Version: 12.x   |
# |-------------------------------+----------------------+----------------------+
# | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
# | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
# |===============================+======================+======================|
# |   0  GRID K1             Off  | 00000000:06:00.0 Off |                  N/A |
# | N/A   35C    P0    10W / 31W  |      0MiB /  4096MiB |      0%      Default |
# +-------------------------------+----------------------+----------------------+
```

---

### **STEP 7: Test GPU Performance**

**7.1: Test CUDA (Linux)**
```bash
# Install CUDA toolkit
sudo apt install nvidia-cuda-toolkit -y

# Test CUDA
cuda-samples/bin/x86_64/linux/release/deviceQuery

# Should show GRID K1 specs
```

**7.2: Test Video Encoding (NVENC)**
```bash
# Install ffmpeg with NVIDIA support
sudo apt install ffmpeg -y

# Test H.264 encoding
ffmpeg -i input.mp4 -c:v h264_nvenc -preset fast output.mp4

# Monitor GPU usage
watch -n 1 nvidia-smi
```

**7.3: Test DirectX/OpenGL (Windows)**
```powershell
# Install GPU-Z
# Download: https://www.techpowerup.com/gpuz/

# Run GPU-Z
# Should show: NVIDIA GRID K1, 4 GB VRAM, Kepler architecture

# Run 3DMark or Unigine Heaven benchmark
# Should see GPU rendering graphics
```

---

## 🎯 **USE CASES FOR YOUR GRID K1 GPUS**

### **Use Case 1: Windows Desktop VM with GPU Acceleration**
**Configuration**:
- VM: Windows 11 or Windows Server 2025
- GPU: 1x GRID K1 GPU (83:00.0)
- Use: Remote desktop, CAD software, video editing

**Benefits**:
- Smooth RDP/remote desktop experience
- Hardware-accelerated applications
- GPU-accelerated video playback

### **Use Case 2: Plex/Jellyfin Media Server with Hardware Transcoding**
**Configuration**:
- VM: Ubuntu 22.04/24.04 or Windows
- GPU: 1x GRID K1 GPU (84:00.0)
- Use: Hardware-accelerated video transcoding (NVENC)

**Benefits**:
- 2-4 simultaneous 1080p transcodes per GPU
- Offloads CPU from transcoding
- Faster transcoding speeds

**Setup**:
```bash
# Ubuntu VM with Plex
# Enable hardware transcoding in Plex settings
# Settings → Transcoder → Use hardware acceleration when available
```

### **Use Case 3: GPU Compute for Legacy ML Workloads**
**Configuration**:
- VM: Ubuntu 22.04 with CUDA
- GPU: 1x GRID K1 GPU (85:00.0)
- Use: Older TensorFlow/PyTorch models (CUDA 3.5 compute capability)

**Limitations**:
- GRID K1 is Kepler (2013), not ideal for modern AI/ML
- For modern ML, consider upgrading to RTX 4000 Ada or A4000

### **Use Case 4: Multiple VDI Desktops (with vGPU License)**
**Configuration** (if you purchase vGPU license):
- Multiple Windows VMs
- vGPU profiles: K140Q, K160Q, K180Q, K1 Passthrough
- Use: Virtual desktop infrastructure (VDI)

**Profiles**:
- K140Q: 1 GB VRAM, up to 4 VMs per GPU
- K160Q: 2 GB VRAM, up to 2 VMs per GPU
- K180Q: 4 GB VRAM, 1 VM per GPU
- K1 Passthrough: Full 4 GB, 1 VM per GPU

**Licensing**:
- NVIDIA vGPU license required (~$100-300/year per GPU)
- Not recommended unless you need VDI

---

## ⚠️ **TROUBLESHOOTING COMMON ISSUES**

### **Issue 1: VM Won't Start After Adding GPU**
**Symptoms**: VM fails to start, error in Proxmox logs  
**Causes**:
- IOMMU not enabled
- VFIO not loaded
- IOMMU group conflicts

**Solutions**:
```bash
# Check IOMMU enabled
dmesg | grep IOMMU

# Check VFIO loaded
lsmod | grep vfio

# Check IOMMU groups
for d in $(find /sys/kernel/iommu_groups/ -type l); do
    n=${d#*/iommu_groups/*}; n=${n%%/*}
    printf 'IOMMU group %s ' "$n"
    lspci -nns "${d##*/}"
done | grep "83:00.0"

# If IOMMU group has multiple devices, add ACS override:
# Edit /etc/default/grub
# GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt pcie_acs_override=downstream,multifunction"
# update-grub && reboot
```

### **Issue 2: GPU Not Detected in VM**
**Symptoms**: VM starts but GPU not in Device Manager/lspci  
**Causes**:
- Machine type not q35
- BIOS not OVMF (UEFI)
- PCIe passthrough not properly configured

**Solutions**:
```bash
# Verify VM config
qm config 100

# Should have:
# machine: q35
# bios: ovmf
# hostpci0: 83:00.0,pcie=1,rombar=0

# If missing, add:
qm set 100 -machine q35
qm set 100 -bios ovmf
```

### **Issue 3: NVIDIA Driver Won't Install in VM**
**Symptoms**: Driver installation fails, "Code 43" error  
**Causes**:
- VM detection (NVIDIA drivers detect virtualization)
- Missing ROM BAR
- KVM hidden features not enabled

**Solutions**:
```bash
# Hide KVM from VM (edit VM config file)
nano /etc/pve/qemu-server/100.conf

# Add to cpu line:
cpu: host,hidden=1,flags=+pcid

# Add vendor_id:
args: -cpu host,kvm=off,hv_vendor_id=proxmox

# Save and restart VM
qm stop 100 && qm start 100
```

### **Issue 4: Poor GPU Performance**
**Symptoms**: Low FPS, stuttering, slow rendering  
**Causes**:
- CPU not set to host
- Insufficient RAM
- PCIe lanes not full x16

**Solutions**:
```bash
# Set CPU to host
qm set 100 -cpu host

# Increase RAM
qm set 100 -memory 16384

# Verify PCIe passthrough
qm config 100 | grep hostpci
# Should have: pcie=1
```

### **Issue 5: "nvidia-smi" Shows No GPUs**
**Symptoms**: nvidia-smi returns "No devices found" in VM  
**Causes**:
- Driver not installed correctly
- GPU not passed through
- NVIDIA kernel module not loaded

**Solutions (Ubuntu)**:
```bash
# Check if GPU is present
lspci | grep -i nvidia

# If present but no nvidia-smi:
# Reinstall driver
sudo apt purge nvidia-* -y
sudo apt autoremove -y
sudo apt install nvidia-driver-535 -y
sudo reboot

# Check kernel module loaded
lsmod | grep nvidia
```

---

## 🔧 **ADVANCED CONFIGURATION**

### **GPU ROM Extraction (If Passthrough Fails)**
Sometimes GPU passthrough requires extracting and providing the GPU ROM:

```bash
# On Proxmox host, extract ROM from GPU
cd /sys/bus/pci/devices/0000:83:00.0/
echo 1 > rom
cat rom > /usr/share/kvm/vbios-grid-k1.bin
echo 0 > rom

# Add ROM to VM
qm set 100 -hostpci0 83:00.0,pcie=1,romfile=vbios-grid-k1.bin
```

### **Multiple GPUs to Single VM**
Pass multiple GRID K1 GPUs to one VM:

```bash
# Add 2 GPUs to VM 100
qm set 100 -hostpci0 83:00.0,pcie=1,rombar=0
qm set 100 -hostpci1 84:00.0,pcie=1,rombar=0

# VM will see 2 separate GPUs (8 GB VRAM total, 384 CUDA cores)
```

### **GPU Passthrough with OVMF Secure Boot**
For Windows 11 VMs requiring Secure Boot:

```bash
# Create VM with OVMF and Secure Boot
qm create 105 --memory 16384 --cores 4 --cpu host --machine q35 --bios ovmf
qm set 105 -efidisk0 local-lvm:1,format=raw,efitype=4m,pre-enrolled-keys=1
qm set 105 -hostpci0 85:00.0,pcie=1,rombar=0

# Install Windows 11, drivers should work with Secure Boot
```

---

## 📚 **DRIVER DOWNLOADS & RESOURCES**

### **Official NVIDIA Resources**
- **GRID K1 Product Page**: https://www.nvidia.com/en-us/design-visualization/grid-vpgpu/
- **Driver Downloads**: https://www.nvidia.com/Download/index.aspx (Product: GRID K-Series → GRID K1)
- **GRID vGPU Software**: https://www.nvidia.com/en-us/data-center/virtual-solutions/ (requires account)
- **GRID vGPU User Guide**: https://docs.nvidia.com/grid/ (comprehensive documentation)

### **Linux Driver Versions (Ubuntu)**
- **Production Branch**: nvidia-driver-535 (recommended for Ubuntu 22.04/24.04)
- **Legacy Branch**: nvidia-driver-470 (for older kernels)
- **Open-source**: nouveau (not recommended, poor performance)

### **Windows Driver Versions**
- **Latest**: R535 branch (525.xx.xx - 535.xx.xx)
- **Stable**: R470 branch (470.xx.xx)
- **Download**: NVIDIA website → Drivers → GRID K1

### **CUDA Support**
- **Compute Capability**: 3.5
- **Maximum CUDA Version**: 11.8 (limited support)
- **Recommended CUDA**: 10.2 or 11.2 for best compatibility
- **TensorFlow**: Up to TensorFlow 2.10 (CUDA 11.2)
- **PyTorch**: Up to PyTorch 1.13 (CUDA 11.7)

---

## 🆚 **GRID K1 vs Newer GPUs (Upgrade Path)**

| Feature | GRID K1 (2013) | RTX A4000 (2021) | RTX 4000 Ada (2024) |
|---------|----------------|------------------|---------------------|
| **Architecture** | Kepler (GK107) | Ampere | Ada Lovelace |
| **CUDA Cores** | 768 (4×192) | 6144 | 6144 |
| **VRAM** | 16 GB (4×4GB) | 16 GB GDDR6 | 20 GB GDDR6 |
| **TDP** | 130W | 140W | 130W |
| **PCIe** | 3.0 x16 | 4.0 x16 | 4.0 x16 |
| **Compute** | 3.5 | 8.6 | 8.9 |
| **Tensor Cores** | ❌ None | ✅ 192 | ✅ 192 Gen 4 |
| **RT Cores** | ❌ None | ✅ 48 Gen 2 | ✅ 48 Gen 3 |
| **NVENC** | 1st gen | 7th gen (3 encoders) | 8th gen (2 encoders) |
| **Modern AI/ML** | ❌ Poor | ✅ Excellent | ✅ Best |
| **VDI** | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| **Gaming** | ❌ Weak | ✅ Good | ✅ Excellent |
| **Price (2025)** | $100-200 used | $800-1000 used | $1500-1800 new |

**Recommendation**: 
- Keep GRID K1 for VDI, video transcoding, legacy GPU workloads
- Upgrade to RTX A4000 or RTX 4000 Ada if you need modern AI/ML, ray tracing, or high-end gaming VMs

---

## 💰 **VALUE & PERFORMANCE EXPECTATIONS**

### **GRID K1 Value in 2025**
- **Original Price (2013)**: ~$3,000-4,000
- **Current Value (2025)**: ~$100-250 (used market)
- **Depreciation**: ~95% over 11 years

### **Performance Expectations**
**Good For**:
- ✅ Virtual Desktop Infrastructure (VDI) - designed purpose
- ✅ Video transcoding (NVENC H.264)
- ✅ Legacy CUDA applications (Compute 3.5)
- ✅ GPU-accelerated RDP/remote desktop
- ✅ CAD software (older versions)
- ✅ Multiple light GPU workloads

**Not Good For**:
- ❌ Modern AI/ML training (too old, no Tensor Cores)
- ❌ Modern gaming (Kepler = 2013, DirectX 11.2)
- ❌ Ray tracing (no RT cores)
- ❌ H.265/AV1 encoding (1st gen NVENC)

### **Your 4x GRID K1 Setup**
**Total Capability**:
- 768 CUDA cores
- 16 GB VRAM
- 4 separate GPUs (can assign to 4 different VMs)

**Recommended Allocation**:
1. **VM 100 (Windows Server 2025)**: 1x GPU → AI model hosting, RDP
2. **VM 150 (Ubuntu)**: 1x GPU → Plex/Jellyfin transcoding
3. **VM 102 (Windows 11 Desktop)**: 1x GPU → GPU-accelerated desktop
4. **VM 103 (Ubuntu)**: 1x GPU → Legacy ML experiments, CUDA dev

---

## ✅ **QUICK REFERENCE: COMMANDS CHEAT SHEET**

### **Proxmox Host Commands**
```bash
# Check IOMMU enabled
dmesg | grep IOMMU

# List NVIDIA GPUs
lspci | grep -i nvidia

# Check VFIO loaded
lsmod | grep vfio

# Check GPU driver (should be vfio-pci)
lspci -nnk | grep -A 3 NVIDIA

# Add GPU to VM
qm set <VMID> -hostpci0 <PCIe_ADDRESS>,pcie=1,rombar=0

# Remove GPU from VM
qm set <VMID> -delete hostpci0

# View VM config
qm config <VMID>
```

### **Inside Windows VM**
```powershell
# Check GPU in Device Manager
devmgmt.msc

# Check NVIDIA GPU via nvidia-smi
nvidia-smi

# Install driver
# Download from NVIDIA website and run installer
```

### **Inside Ubuntu VM**
```bash
# Check GPU present
lspci | grep -i nvidia

# Install NVIDIA driver
sudo apt install nvidia-driver-535 -y
sudo reboot

# Check driver loaded
nvidia-smi

# Check CUDA
nvcc --version

# Monitor GPU usage
watch -n 1 nvidia-smi
```

---

## 🎓 **LEARNING RESOURCES**

### **Proxmox GPU Passthrough Guides**
- **Official Proxmox Wiki**: https://pve.proxmox.com/wiki/PCI(e)_Passthrough
- **Reddit r/Proxmox**: https://www.reddit.com/r/Proxmox/ (search "GPU passthrough")
- **Proxmox Forum**: https://forum.proxmox.com/ (GPU passthrough section)

### **YouTube Tutorials**
- **Craft Computing**: "Proxmox GPU Passthrough Tutorial"
- **Techno Tim**: "GPU Passthrough with Proxmox"
- **Learn Linux TV**: "Proxmox GPU Passthrough Step-by-Step"

### **NVIDIA GRID Documentation**
- **GRID User Guide**: https://docs.nvidia.com/grid/
- **GRID Release Notes**: https://docs.nvidia.com/grid/latest/grid-software-quick-start-guide/
- **GRID Licensing Guide**: https://docs.nvidia.com/grid/latest/grid-licensing-user-guide/

---

## 📞 **SUPPORT & TROUBLESHOOTING**

### **NVIDIA Support**
- **Enterprise Support**: https://www.nvidia.com/en-us/support/
- **GRID Forum**: https://forums.developer.nvidia.com/c/professional-graphics/grid-vgpu/
- **Driver Support**: https://www.nvidia.com/Download/Find.aspx

### **Proxmox Community**
- **Proxmox Forum**: https://forum.proxmox.com/
- **Reddit r/Proxmox**: https://www.reddit.com/r/Proxmox/
- **IRC**: #proxmox on irc.oftc.net

### **Dell R730 GPU Compatibility**
- **Dell Community**: https://www.dell.com/community/
- **Dell Support**: 1-800-624-9896 (Express Code: 33201963650)

---

## ✨ **SUMMARY: YOUR NEXT STEPS**

1. **Enable IOMMU in Proxmox** (Step 1)
2. **Load VFIO modules** (Step 2)
3. **Identify GPU PCIe addresses** (Step 3)
4. **Passthrough GPU to VM** (Step 4-5)
5. **Install NVIDIA drivers in VM** (Step 6)
6. **Test GPU performance** (Step 7)
7. **Configure use cases** (Plex, RDP, etc.)

**Estimated Time**: 2-3 hours (first time), 30 minutes (subsequent VMs)

---

**Document Created**: November 6, 2025  
**Last Updated**: November 6, 2025  
**Owner**: Seth Schultz - LightSpeedUp Hosting  
**Purpose**: Complete GPU passthrough guide for NVIDIA GRID K1 in Proxmox on Dell R730  
**Usage**: RAG knowledge base for SHENRON AI, human reference, GPU configuration guide

**✨ Let's put those 4 GPUs to work! ✨** 🎮

