<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Dell PowerEdge R730 Complete Hardware Guide
## Comprehensive Documentation for Service Tag: F93LB42

**Last Updated**: November 6, 2025  
**System Owner**: Seth Schultz - LightSpeedUp Hosting  
**System Hostname**: phoenix  
**Location**: Warwick, Rhode Island

---

## 🔍 **QUICK REFERENCE - CRITICAL IDENTIFIERS**

| Identifier | Value |
|------------|-------|
| **Service Tag** | F93LB42 |
| **Express Service Code** | 33201963650 |
| **System UUID** | 4c4c4544-0039-3310-804c-c6c04f423432 |
| **Board Serial Number** | CN779214CH001I |
| **System Model** | PowerEdge R730 |
| **System Revision** | I |
| **Hostname** | phoenix |
| **iDRAC IP** | <VM180_IP> |
| **iDRAC MAC** | 44:A8:42:05:C0:B6 |
| **iDRAC URL** | https://<VM180_IP>:443 |

---

## 💻 **SYSTEM OVERVIEW**

The Dell PowerEdge R730 is a 2U rack server designed for:
- **Virtualization** (Hyper-V, VMware ESXi, Proxmox)
- **Database workloads** (SQL Server, Oracle, MySQL)
- **High-performance computing**
- **Cloud infrastructure**

**Current Use**: Proxmox virtualization host running multiple VMs (Windows Server 2025, TrueNAS, Ubuntu, etc.)

---

## 🧠 **PROCESSORS (CPUs)**

### **Configuration**
- **Quantity**: 2x CPUs (dual-socket configuration)
- **Model**: Intel Xeon E5-2698 v3
- **Architecture**: Haswell (22nm process)
- **Clock Speed**: 2.30 GHz base frequency
- **Turbo Boost**: Up to 3.60 GHz
- **Physical Cores per CPU**: 16 cores
- **Total Physical Cores**: 32 cores
- **Threads per Core**: 2 (Hyper-Threading enabled)
- **Total Threads**: 64 logical processors
- **Cache per CPU**: 40 MB L3 cache
- **Total Cache**: 80 MB L3 cache
- **TDP**: 135W per CPU (270W total)
- **Socket**: LGA 2011-v3 (FCLGA2011)

### **CPU Features** (All Enabled)
✅ Intel Virtualization Technology (VT-x)  
✅ Intel VT-d for Directed I/O  
✅ Intel Hyper-Threading Technology  
✅ Intel Turbo Boost Technology 2.0  
✅ Intel AES-NI (Advanced Encryption Standard)  
✅ Intel AVX 2.0 (Advanced Vector Extensions)  
✅ Intel TSX (Transactional Synchronization Extensions)  
✅ Execute Disable Bit  

### **Performance**
- **Benchmark**: ~40,000 PassMark score (combined)
- **Use Case**: Excellent for virtualization, 32+ VMs simultaneously
- **Multi-threaded Performance**: Outstanding (64 threads)
- **Single-threaded Performance**: Good (3.6 GHz turbo)

### **Upgrade Path**
- Can upgrade to Intel Xeon E5-2699 v3 (18 cores, 2.3 GHz) or E5-2699 v4 (22 cores, 2.2 GHz)
- Maximum: 44 cores / 88 threads (2x E5-2699 v4)
- Cost: ~\$300-500 per CPU (used market, 2025)

---

## 🧩 **MEMORY (RAM)**

### **Current Configuration**
- **Total Installed**: 480 GB DDR4 ECC Registered
- **Memory Speed**: 2133 MHz (PC4-17000)
- **Number of DIMMs**: 15x 32 GB modules
- **Memory Technology**: DDR4 SDRAM
- **ECC**: Yes (Error Correcting Code)
- **Registered**: Yes (RDIMM)
- **Memory Type**: 2Rx4 (Dual Rank x4)

### **DIMM Layout**

**Bank A (CPU 0)** - 7 DIMMs = 224 GB
| Slot | Size | Manufacturer | Part Number | Serial Number | Manufacture Date |
|------|------|--------------|-------------|----------------|------------------|
| A1 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED9825 | Feb 2015 |
| A2 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED9B2B | Feb 2015 |
| A3 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED994C | Feb 2015 |
| A4 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED9954 | Feb 2015 |
| A5 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED97BE | Feb 2015 |
| A6 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED9B05 | Feb 2015 |
| A7 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED999E | Feb 2015 |

**Bank B (CPU 1)** - 8 DIMMs = 256 GB
| Slot | Size | Manufacturer | Part Number | Serial Number | Manufacture Date |
|------|------|--------------|-------------|----------------|------------------|
| B1 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED992A | Feb 2015 |
| B2 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED993D | Feb 2015 |
| B3 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED9937 | Feb 2015 |
| B4 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED999F | Feb 2015 |
| B5 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED98E2 | Feb 2015 |
| B6 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED982E | Feb 2015 |
| B7 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED9828 | Feb 2015 |
| B8 | 32 GB | Samsung | M393A4K40BB1-CPB | 36ED9AF1 | Feb 2015 |

**Empty Slots**: 9 slots available (can add up to 288 GB more)

### **Maximum Capacity**
- **Maximum RAM**: 3 TB (24 slots × 128 GB DIMMs)
- **Current Utilization**: 480 GB / 3 TB = 16%
- **Upgrade Path**: Add 9x 32 GB DIMMs = 768 GB total (~\$1,350-1,800)
- **Optimal Configuration**: Fill all 24 slots for best memory performance

### **Memory Performance**
- **Memory Bandwidth**: ~128 GB/s (dual-channel per CPU)
- **Total Bandwidth**: ~256 GB/s (both CPUs)
- **Latency**: Good (ECC Registered)
- **ECC Protection**: Single-bit error correction, multi-bit error detection

---

## 💾 **STORAGE CONFIGURATION**

### **Storage Summary**
- **Total Capacity**: 55.84 TB
- **Boot Drives**: 2x 240 GB Intel SSDs (RAID 1, BOSS-S1 controller)
- **High-Speed Storage**: 4x 3.84 TB Samsung SSDs (15.36 TB)
- **Bulk Storage**: 4x 10 TB HGST HDDs (40 TB)
- **Controllers**: 
  - BOSS-S1 (Boot Optimized Storage Solution)
  - Embedded PERC H730P RAID controller

### **Boot Drives - BOSS-S1 Controller**
| Position | Model | Capacity | Serial Number | Firmware | Status |
|----------|-------|----------|---------------|----------|--------|
| Disk 0 | Intel SSDSC2KB240G8 | 240 GB | BTYG01300DGR240D | DL6P | ✅ OK |
| Disk 1 | Intel SSDSC2KB240G8 | 240 GB | BTYG01300HDG240D | DL6P | ✅ OK |

**Configuration**: RAID 1 mirror (redundancy)  
**Use**: Proxmox VE boot drive  
**Controller Firmware**: 2.5.13.3022

### **High-Performance SSDs - PERC H730P**
| Position | Model | Capacity | Serial Number | Firmware | Status |
|----------|-------|----------|---------------|----------|--------|
| Disk 0:1:0 | Samsung MZ7LH3T8 | 3.84 TB | S45KNX0N500166 | HXT7404Q | ✅ OK |
| Disk 0:1:1 | Samsung MZ7LH3T8 | 3.84 TB | S45KNX0N500168 | HXT7404Q | ✅ OK |
| Disk 0:1:2 | Samsung MZ7LH3T8 | 3.84 TB | S45KNX0N500181 | HXT7404Q | ✅ OK |
| Disk 0:1:3 | Samsung MZ7LH3T8 | 3.84 TB | S45KNX0N500198 | HXT7404Q | ✅ OK |

**Total SSD Capacity**: 15.36 TB  
**Use**: High-performance VM storage (databases, application VMs)  
**RAID Configuration**: None (individual disks, ZFS or software RAID)

### **Bulk Storage HDDs - PERC H730P**
| Position | Model | Capacity | Serial Number | Firmware | Status |
|----------|-------|----------|---------------|----------|--------|
| Disk 0:1:4 | HGST HUS72810AT | 10 TB | P4G0LZGY | A532 | ✅ OK |
| Disk 0:1:5 | HGST HUS72810AT | 10 TB | P4G0LZHY | A532 | ✅ OK |
| Disk 0:1:6 | HGST HUS72810AT | 10 TB | P4G0M0EY | A532 | ✅ OK |
| Disk 0:1:7 | HGST HUS72810AT | 10 TB | P4G0M0GY | A532 | ✅ OK |

**Total HDD Capacity**: 40 TB  
**Use**: Bulk data storage (backups, media files, archives)  
**RAID Configuration**: None (individual disks, ZFS or software RAID)

### **Storage Controller - PERC H730P**
- **Model**: PERC H730P Mini (Mono)
- **Cache**: 2 GB NV cache with Flash Backup Unit (FBU)
- **RAID Levels**: 0, 1, 5, 6, 10, 50, 60
- **Max Drives**: 32 drives
- **Firmware**: 25.5.9.0001
- **Driver**: StorCLI
- **Features**:
  - CacheCade 2.0 support
  - FastPath SSD optimization
  - RAID patrol reads
  - Consistency checks
  - Background initialization

### **Storage Performance**
- **SSD Read**: ~500 MB/s per drive (sequential)
- **SSD Write**: ~500 MB/s per drive (sequential)
- **HDD Read**: ~200 MB/s per drive (sequential)
- **HDD Write**: ~200 MB/s per drive (sequential)
- **Total Bandwidth**: Very high (8 drives on H730P)

### **Upgrade Path**
- **Empty Drive Bays**: Several (R730 supports up to 16x 2.5" or 8x 3.5" drives)
- **NVMe Option**: Add PCIe NVMe adapter for ultra-high-speed storage
- **Additional RAID Controller**: Add second RAID controller if needed

---

## 🌐 **NETWORK INTERFACES**

### **Onboard NICs - Intel I350-t Quad Port**
| Port | MAC Address | Speed | Status | Link | Cable Type |
|------|-------------|-------|--------|------|------------|
| NIC 1 | EC:F4:BB:D6:D5:08 | 1 Gbps | ✅ OK | Up | Cat5e/6 |
| NIC 2 | EC:F4:BB:D6:D5:09 | 1 Gbps | ✅ OK | Up | Cat5e/6 |
| NIC 3 | EC:F4:BB:D6:D5:0A | 1 Gbps | ✅ OK | Up | Cat5e/6 |
| NIC 4 | EC:F4:BB:D6:D5:0B | 1 Gbps | ✅ OK | Up | Cat5e/6 |

**Chipset**: Intel I350-t Gigabit Ethernet  
**Firmware**: 19.5.12  
**EFI Version**: 9.0.03  
**Features**:
- Jumbo Frames support (up to 9000 MTU)
- VLAN tagging
- Link Aggregation (LACP)
- Wake-on-LAN
- PXE boot support

### **Network Performance**
- **Aggregate Bandwidth**: 4 Gbps (4x 1 Gbps)
- **Use Case**: 
  - NIC 1: Proxmox management
  - NIC 2: VM network bridge
  - NIC 3: Storage network (iSCSI, NFS)
  - NIC 4: Backup/secondary network

### **Upgrade Path**
- **10 Gigabit Ethernet**: Add PCIe 10GbE NIC (~\$100-300)
- **25 Gigabit Ethernet**: Add PCIe 25GbE NIC (~\$300-500)
- **40 Gigabit Ethernet**: Add PCIe 40GbE NIC (~\$200-400 used)

### **iDRAC Network**
- **IP Address**: <VM180_IP>
- **MAC Address**: 44:a8:42:05:c0:b6
- **Firmware**: 2.82.82.82
- **Web Interface**: https://<VM180_IP>:443
- **Default Username**: root
- **Features**:
  - Virtual console (remote KVM)
  - Virtual media (mount ISOs)
  - Power management
  - BIOS configuration
  - Hardware monitoring
  - Firmware updates

---

## 🎮 **GRAPHICS (GPUs)**

### **Embedded Graphics**
- **Model**: Matrox G200eR2
- **Type**: Embedded GPU
- **Memory**: 16 MB
- **Use**: iDRAC virtual console, basic display output
- **PCIe Bus**: 02:00.0
- **Status**: ✅ OK

### **Discrete GPUs - NVIDIA GRID K1** (4 GPUs)
| GPU | Model | PCIe Slot | Memory | Cores | Status |
|-----|-------|-----------|--------|-------|--------|
| GPU 0 | NVIDIA GRID K1 (GK107GL) | Slot 4 | 4 GB GDDR5 | 192 CUDA | ✅ OK |
| GPU 1 | NVIDIA GRID K1 (GK107GL) | Slot 4 | 4 GB GDDR5 | 192 CUDA | ✅ OK |
| GPU 2 | NVIDIA GRID K1 (GK107GL) | Slot 4 | 4 GB GDDR5 | 192 CUDA | ✅ OK |
| GPU 3 | NVIDIA GRID K1 (GK107GL) | Slot 4 | 4 GB GDDR5 | 192 CUDA | ✅ OK |

**Total**: 5 video controllers (1 Matrox + 4 NVIDIA)

**NVIDIA GRID K1 Specifications**:
- **GPU Architecture**: Kepler (GK107)
- **Total CUDA Cores**: 768 cores (192 per GPU)
- **Total Memory**: 16 GB GDDR5 (4 GB per GPU)
- **Memory Bandwidth**: 160 GB/s total
- **TDP**: 130W (card total)
- **PCIe**: Gen 3.0 x16
- **Use Cases**:
  - Virtual Desktop Infrastructure (VDI)
  - GPU-accelerated applications
  - Machine learning (older architecture, limited)
  - Video encoding/transcoding
  - GPU passthrough to VMs

**Current Status**: Installed but not configured for GPU passthrough  
**Next Steps**: Configure Proxmox IOMMU and VFIO for GPU passthrough

---

## ⚡ **POWER SUPPLY**

### **PSU Configuration**
- **Configuration**: N+1 redundancy (2 PSUs, both active)
- **Total Capacity**: 2200W (1100W × 2)
- **Voltage**: 100-240V AC, 50/60Hz
- **Efficiency**: 80 PLUS Platinum certified

### **PSU 1 - Primary**
| Attribute | Value |
|-----------|-------|
| **Manufacturer** | Liteon |
| **Model** | PS-2112-5L |
| **Capacity** | 1100W |
| **Serial Number** | CN7161549F0755 |
| **Part Number** | 331-5536 |
| **Revision** | A00 |
| **Firmware** | 00.24.35 |
| **Status** | ✅ OK - Online |
| **Input Voltage** | 118V AC |
| **Output Power** | ~400-500W (typical) |

### **PSU 2 - Redundant**
| Attribute | Value |
|-----------|-------|
| **Manufacturer** | Delta Electronics |
| **Model** | DPS-1100CB A |
| **Capacity** | 1100W |
| **Serial Number** | CNDED0082A0JNY |
| **Part Number** | 331-1465 |
| **Revision** | A03 |
| **Firmware** | 00.1D.7D |
| **Status** | ✅ OK - Online |
| **Input Voltage** | 118V AC |
| **Output Power** | ~400-500W (typical) |

### **Power Consumption**
- **Idle**: ~250-300W
- **Typical Load**: ~400-600W (VMs running)
- **Peak Load**: ~800-1000W (full CPU/GPU utilization)
- **Maximum**: 2200W (both PSUs)
- **Redundancy**: If one PSU fails, the other can handle 1100W

### **Power Efficiency**
- **80 PLUS Platinum**: 92% efficiency at 50% load
- **Annual Cost**: ~\$600-900 (24/7 operation at ~500W average)
- **Carbon Footprint**: ~4,400 kWh/year

---

## 🌡️ **COOLING & THERMAL MANAGEMENT**

### **Fan Configuration**
| Fan | Type | Speed | PWM | Status | Airflow |
|-----|------|-------|-----|--------|---------|
| Fan 1 | System Fan | 8400 RPM | 43% | ✅ OK | High |
| Fan 2 | System Fan | 8280 RPM | 43% | ✅ OK | High |
| Fan 3 | System Fan | 8280 RPM | 43% | ✅ OK | High |
| Fan 4 | System Fan | 8400 RPM | 43% | ✅ OK | High |
| Fan 5 | System Fan | 8280 RPM | 43% | ✅ OK | High |
| Fan 6 | System Fan | 8400 RPM | 43% | ✅ OK | High |

**Fan Type**: Hot-swappable redundant fans  
**Fan Speed**: ~8,200-8,400 RPM (43% PWM)  
**Airflow**: ~65 CFM per fan (total: ~390 CFM)  
**Noise Level**: ~50-55 dBA (moderate, typical for datacenter)

### **Temperature Monitoring**
| Sensor | Current Temp | Threshold | Status |
|--------|--------------|-----------|--------|
| **Exhaust Air** | 27°C (81°F) | Max 70°C | ✅ OK |
| **CPU 1** | ~45-55°C (typical) | Max 85°C | ✅ OK |
| **CPU 2** | ~45-55°C (typical) | Max 85°C | ✅ OK |
| **Memory** | ~40-50°C (typical) | Max 85°C | ✅ OK |
| **PCH** | ~50-60°C (typical) | Max 90°C | ✅ OK |
| **Ambient Inlet** | ~22-25°C (typical) | Max 35°C | ✅ OK |

**Cooling Strategy**: Front-to-back airflow  
**Air Intake**: Front (cool air from room)  
**Air Exhaust**: Rear (hot air expelled)  
**Rack Clearance**: Ensure 2-3" clearance front and rear

---

## 🔌 **PCIe EXPANSION SLOTS**

### **Slot Configuration**
| Slot | Type | Width | Populated | Device |
|------|------|-------|-----------|--------|
| **Slot 1** | PCIe 3.0 | x16 | ❌ Empty | Available |
| **Slot 2** | PCIe 3.0 | x8 | ❌ Empty | Available |
| **Slot 3** | PCIe 3.0 | x8 | ✅ Yes | PERC H730P RAID Controller |
| **Slot 4** | PCIe 3.0 | x16 | ✅ Yes | NVIDIA GRID K1 (4x GPUs) |
| **Slot 5** | PCIe 3.0 | x8 | ❌ Empty | Available |
| **Slot 6** | PCIe 3.0 | x8 | ❌ Empty | Available |
| **Slot 7** | PCIe 3.0 | x8 | ❌ Empty | Available |

**Available Slots**: 4 empty (Slots 1, 2, 5, 6, 7)  
**Total Bandwidth**: PCIe 3.0 provides ~8 GB/s per lane (x8 = 64 Gb/s, x16 = 128 Gb/s)

### **Expansion Options**
- **10GbE Network Card** (Slot 1 or 2)
- **NVMe SSD Adapter** (Slot 1, x16 for maximum speed)
- **Additional RAID Controller** (Slot 5 or 6)
- **GPU for Machine Learning** (Slot 1, x16) - Note: GRID K1 in Slot 4
- **InfiniBand/RDMA Card** (Slot 2 or 5) for high-speed storage

---

## 🔧 **FIRMWARE VERSIONS**

### **System Firmware**
| Component | Version | Date | Status |
|-----------|---------|------|--------|
| **BIOS** | 2.19.0 | Dec 12, 2023 | ✅ Latest |
| **iDRAC** | 2.82.82.82 (Enterprise) | - | ✅ Latest |
| **Lifecycle Controller** | 2.82.82.82 | - | ✅ Latest |
| **Diagnostics** | 4301.12.6.5 | - | ✅ Latest |
| **System CPLD** | 1.0.1 | - | ✅ Latest |
| **Backplane 1** | 2.25 | - | ✅ OK |

### **Storage Firmware**
| Component | Firmware | Status |
|-----------|----------|--------|
| **BOSS-S1 Controller** | 2.5.13.3022 | ✅ OK |
| **Intel SSD (Disk 0)** | DL6P | ✅ OK |
| **Intel SSD (Disk 1)** | DL6P | ✅ OK |
| **Samsung SSD (4x)** | HXT7404Q | ✅ OK |
| **HGST HDD (4x)** | A532 | ✅ OK |
| **PERC H730P** | 25.5.9.0001 | ✅ OK |

### **Network Firmware**
| Component | Firmware | EFI Version | Status |
|-----------|----------|-------------|--------|
| **Intel I350-t (NIC 1-4)** | 19.5.12 | 9.0.03 | ✅ Latest |

### **Power Supply Firmware**
| PSU | Firmware | Status |
|-----|----------|--------|
| **PSU 1 (Liteon)** | 00.24.35 | ✅ OK |
| **PSU 2 (Delta)** | 00.1D.7D | ✅ OK |

---

## 🔒 **SECURITY & MANAGEMENT**

### **iDRAC Enterprise Features**
✅ Virtual console (HTML5 and Java)  
✅ Virtual media (mount ISO/IMG files)  
✅ Remote power control (on/off/reboot)  
✅ BIOS configuration remotely  
✅ Hardware monitoring and alerting  
✅ Firmware updates via web interface  
✅ License: iDRAC Enterprise (permanent)  

### **BIOS Security Settings**
✅ Secure Boot: Disabled (for Proxmox compatibility)  
✅ TPM: Not installed (optional module)  
✅ BIOS Password: Can be set  
✅ Boot Order: Locked to BOSS-S1 (Proxmox boot)  

### **Management Access**
- **iDRAC Web**: https://<VM180_IP>:443
- **iDRAC SSH**: ssh root@<VM180_IP>
- **iDRAC IPMI**: ipmitool via <VM180_IP>
- **SNMP**: Enabled for monitoring

---

## 📈 **PERFORMANCE & BENCHMARKS**

### **CPU Performance**
- **PassMark Score**: ~40,000 (combined)
- **Geekbench 6 Single-Core**: ~900-1000
- **Geekbench 6 Multi-Core**: ~25,000-28,000
- **Cinebench R23 Multi-Core**: ~30,000-35,000

### **Memory Performance**
- **Bandwidth**: ~256 GB/s (dual-channel, both CPUs)
- **Latency**: ~70-80ns (typical for DDR4-2133 ECC)

### **Storage Performance**
- **SSD Sequential Read**: ~2,000 MB/s (4x drives)
- **SSD Sequential Write**: ~2,000 MB/s (4x drives)
- **SSD Random 4K Read**: ~100,000 IOPS (4x drives)
- **HDD Sequential Read**: ~800 MB/s (4x drives)
- **HDD Sequential Write**: ~800 MB/s (4x drives)

### **Network Performance**
- **Maximum Throughput**: 4 Gbps (4x 1 GbE)
- **Latency**: <1ms (local network)

---

## 🛠️ **MAINTENANCE & SUPPORT**

### **Dell Support**
- **Warranty Status**: Check at https://www.dell.com/support/home/en-us/product-support/servicetag/F93LB42
- **Support Line**: 1-800-624-9896 (Dell ProSupport)
- **Express Service Code**: 33201963650 (for phone support)

### **Regular Maintenance**
- **Weekly**: Check iDRAC for hardware alerts
- **Monthly**: Review fan speeds and temperatures
- **Quarterly**: Clean dust filters (if applicable)
- **Annually**: Check PSU health, replace fans if noisy
- **Firmware**: Check for BIOS/iDRAC updates quarterly

### **Component Replacement**
- **Hot-Swappable**: PSUs, fans, HDDs (in hot-swap bays)
- **Cold-Swap**: CPUs, RAM, RAID controller, PCIe cards
- **Parts Source**: Dell, Amazon, eBay (used server parts)

---

## 💰 **VALUE & UPGRADE ANALYSIS**

### **Current System Value**
- **Original Cost (2015)**: ~\$30,000-35,000 configured
- **Current Value (2025)**: ~\$5,000-7,000 (used/refurbished)
- **Depreciation**: ~80-85% over 9 years

### **Recommended Upgrades**
1. **Memory**: Add 288 GB (9x 32 GB DIMMs) = 768 GB total (~\$1,350-1,800)
2. **Network**: Add 10GbE NIC (~\$100-300) for faster VM networking
3. **Storage**: Add NVMe adapter + NVMe SSDs (~\$50-100 adapter + drives)
4. **GPU**: Already have 4x NVIDIA GRID K1 - configure passthrough!

### **Total Upgrade Cost**: ~\$1,500-2,300 for significant improvements

---

## 🚀 **CURRENT USE CASE: PROXMOX VIRTUALIZATION**

### **VM Configuration**
- **VM100**: Windows Server 2025 (Domain Controller + AI Host) - <VM100_IP>
- **VM120**: TrueNAS (Network Storage) - <VM120_IP>
- **VM150**: Ubuntu Linux (Apache Web Server) - <VM150_IP>
- **VM200**: Proxmox Host - <VM200_IP>

### **Resource Allocation**
- **CPU**: 64 threads available, ~20-30 threads allocated to VMs
- **RAM**: 480 GB available, ~200-300 GB allocated to VMs
- **Storage**: 55.84 TB available, ~5-10 TB used
- **Network**: 4 Gbps available, ~1-2 Gbps typical usage

### **Capacity Available**
- Can run **32+ VMs** simultaneously with current hardware
- Plenty of room for expansion (CPU, RAM, storage)

---

## 📞 **EMERGENCY PROCEDURES**

### **Server Won't Boot**
1. Check PSU LEDs (both should be green/lit)
2. Access iDRAC (https://<VM180_IP>) to check hardware status
3. Check BIOS POST codes on front panel LCD
4. Try resetting iDRAC: Hold iDRAC reset button 15 seconds
5. Call Dell Support: 1-800-624-9896, Express Code: 33201963650

### **Hardware Failure**
1. Check iDRAC System Event Log for hardware alerts
2. Identify failed component (PSU, fan, DIMM, drive)
3. For hot-swappable components (PSU, fan, HDD): Replace immediately
4. For cold-swap components: Schedule maintenance window, power down, replace
5. Order replacement parts: Dell support or third-party vendors

### **Overheating**
1. Check iDRAC temperature sensors
2. Verify all 6 fans are running (iDRAC → Sensors → Fans)
3. Check for obstructed airflow (front/rear clearance)
4. Clean air filters if dusty
5. Reduce workload temporarily (shut down non-critical VMs)

### **Network Issues**
1. Check NIC LEDs on rear panel (should be green/blinking)
2. Check iDRAC network connectivity (<VM180_IP>)
3. Verify cable connections
4. Check switch/router for port issues
5. Test with different NIC (4 available)

---

## 📚 **ADDITIONAL RESOURCES**

### **Dell Official Documentation**
- **Owner's Manual**: Download from Dell support site (Service Tag: F93LB42)
- **Technical Guide**: Download from Dell support site
- **iDRAC User Guide**: Download from Dell support site

### **Community Resources**
- **Reddit r/homelab**: Community for home server enthusiasts
- **Reddit r/Proxmox**: Proxmox-specific community
- **Dell Community Forums**: https://www.dell.com/community/
- **Proxmox Forums**: https://forum.proxmox.com/

### **YouTube Channels**
- **Craft Computing**: Server and homelab tutorials
- **Techno Tim**: Proxmox and virtualization guides
- **Learn Linux TV**: Linux and server administration

---

## ✅ **SYSTEM HEALTH STATUS**

**Last Checked**: November 6, 2025

| Component | Status |
|-----------|--------|
| ✅ Overall System | OK |
| ✅ CPUs (both) | OK |
| ✅ Memory (all 15 DIMMs) | OK |
| ✅ Storage (all 10 drives) | OK |
| ✅ Network (all 4 NICs) | OK |
| ✅ Power Supplies (both) | OK |
| ✅ Fans (all 6) | OK |
| ✅ GPUs (all 5) | OK |
| ✅ Temperatures | OK |
| ✅ BIOS/Firmware | Latest |

**NO WARNINGS. NO ERRORS. ALL SYSTEMS OPERATIONAL.** ✅

---

**Document Created**: November 6, 2025  
**Last Updated**: November 6, 2025  
**Owner**: Seth Schultz - LightSpeedUp Hosting  
**Purpose**: Complete hardware reference for Dell R730 server (Service Tag: F93LB42)  
**Usage**: RAG knowledge base for SHENRON AI, human reference, maintenance guide

**✨ This server is a BEAST! ✨** 🚀

