<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🎯 Dell R730 Hardware Inventory - Quick Reference

**Generated**: November 6, 2025  
**Service Tag**: F93LB42  
**Express Service Code**: 33201963650  
**System Name**: phoenix

---

## 🚀 QUICK STATS

| Component | Summary |
|-----------|---------|
| **CPUs** | 2x Intel Xeon E5-2698 v3 (32 cores / 64 threads) |
| **Memory** | 480 GB DDR4-2133 ECC (15 of 24 slots used) |
| **Storage** | 55.84 TB total (2x 240GB boot + 4x 3.84TB SSD + 4x 10TB HDD) |
| **Network** | 4x 1GbE Intel I350-t ports |
| **GPUs** | 5 total (1x Matrox + 4x NVIDIA GRID K1) |
| **Power** | 2x 1100W PSUs (redundant) |
| **Status** | ✅ ALL SYSTEMS OPERATIONAL |

---

## 💰 HARDWARE VALUE & SPECS

### **Total Computing Power**
- **64 logical processors** (32 physical cores)
- **128 MB total CPU cache** (L1 + L2 + L3)
- **Base Clock**: 2.3 GHz, **Turbo**: up to 4.0 GHz
- **480 GB RAM** with ECC protection
- **~$15,000-20,000** original server value (2015 pricing)
- **~$2,000-3,000** current used/refurbished value

### **Storage Breakdown**
- **Boot**: 480 GB total (2x 240GB BOSS-S1 mirrored)
- **Fast Storage**: 15.36 TB (4x Samsung 3.84TB SSDs)
- **Bulk Storage**: 40 TB (4x HGST 10TB HDDs)
- **Total Raw**: 55.84 TB

### **Expansion Capacity**
- **Memory**: Can expand to 3 TB (9 more DIMMs)
- **PCIe Slots**: 4 of 7 empty (room for 10GbE NIC, more GPUs, NVMe)
- **Storage Bays**: 2 rear 2.5" bays likely available

---

## 🔧 CRITICAL IDENTIFIERS

### **For Dell Support**
| Identifier | Value |
|------------|-------|
| **Service Tag** | F93LB42 |
| **Express Service Code** | 33201963650 *(call Dell support)* |
| **System UUID** | 4c4c4544-0039-3310-804c-c6c04f423432 |
| **Board Serial** | CN779214CH001I |

### **For Firmware Updates**
| Component | Current Version |
|-----------|-----------------|
| **BIOS** | 2.19.0 (Dec 12, 2023) |
| **iDRAC** | 2.82.82.82 (Enterprise) |
| **Lifecycle Controller** | 2.82.82.82 |
| **BOSS-S1 Firmware** | 2.5.13.3022 |

---

## 🌐 NETWORK INTERFACES

| Port | MAC Address | Speed | Status |
|------|-------------|-------|--------|
| **NIC 1** | EC:F4:BB:D6:D5:08 | 1 Gbps | ✅ Active |
| **NIC 2** | EC:F4:BB:D6:D5:09 | 1 Gbps | ✅ Active |
| **NIC 3** | EC:F4:BB:D6:D5:0A | 1 Gbps | ✅ Active |
| **NIC 4** | EC:F4:BB:D6:D5:0B | 1 Gbps | ✅ Active |
| **iDRAC** | 44:a8:42:05:c0:b6 | - | https://<VM180_IP> |

---

## 💾 STORAGE INVENTORY

### **Boot Drives (BOSS-S1 RAID)**
```
Disk 0: Intel 240GB SSD (S/N: PHYH929100AU240J) - Ready
Disk 1: Intel 240GB SSD (S/N: PHYH011402BP240J) - Ready
Status: Both drives ready, can be mirrored for redundant boot
```

### **Data SSDs (Samsung 3.84TB)**
```
Slot 0: S/N S456NY0M405636 - 3.84 TB - Non-RAID
Slot 1: S/N S456NY0M405622 - 3.84 TB - Non-RAID
Slot 2: S/N S456NY0M405617 - 3.84 TB - Non-RAID
Slot 3: S/N S456NY0M405620 - 3.84 TB - Non-RAID
Total: 15.36 TB SSD (likely Proxmox VM storage)
```

### **Bulk HDDs (HGST 10TB)**
```
Slot 4: S/N 7JHU9ENC - 10 TB - Non-RAID
Slot 5: S/N 7JHR0XVC - 10 TB - Non-RAID
Slot 6: S/N 7PK8R6BC - 10 TB - Non-RAID
Slot 7: S/N 7JHX8YTK - 10 TB - Non-RAID
Total: 40 TB HDD (likely TrueNAS ZFS pool)
```

---

## ⚡ POWER & THERMAL

### **Power Supplies**
```
PSU 1: Dell/Liteon 1100W (S/N: CN7161549F0755) - Firmware 00.24.35
PSU 2: Dell/Delta 1100W (S/N: CNDED0082A0JNY) - Firmware 00.1D.7D
Config: N+1 Redundancy (can lose one PSU)
Input: 118V AC per PSU
Max Draw: 2464W input, 2200W output
```

### **Cooling**
```
6 Fans @ ~43% PWM speed (8160-8400 RPM)
Exhaust Temp: 27°C
Airflow: 65 CFM
Status: All fans fully redundant, variable speed
```

---

## 🎮 GRAPHICS/GPU

```
Embedded: Matrox G200eR2 (bus 10)
Slot 4:    NVIDIA GRID K1 Card (4x GK107 GPUs)
  - GPU 1: Bus 132
  - GPU 2: Bus 133
  - GPU 3: Bus 134
  - GPU 4: Bus 135
Total: 5 video controllers (1 management + 4 GPU passthrough)
```

---

## 🧠 MEMORY DETAIL

### **Bank A (7 DIMMs - 224 GB)**
```
A1: 32GB Samsung M386A4G40DM0-CPB (S/N: 4010323C) - Feb 2015
A2: 32GB Samsung M386A4G40DM0-CPB (S/N: 40103128) - Feb 2015
A3: 32GB Samsung M386A4G40DM0-CPB (S/N: 401267C5) - Feb 2015
A4: 32GB Samsung M386A4G40DM0-CPB (S/N: 40126BB9) - Feb 2015
A5: 32GB Samsung M386A4G40DM0-CPB (S/N: 4010331D) - Feb 2015
A6: 32GB Samsung M386A4G40DM0-CPB (S/N: 40103226) - Feb 2015
A7: 32GB Samsung M386A4G40DM0-CPB (S/N: 40103225) - Feb 2015
```

### **Bank B (8 DIMMs - 256 GB)**
```
B1: 32GB Samsung M386A4G40DM0-CPB (S/N: 40126BA4) - Feb 2015
B2: 32GB Samsung M386A4G40DM0-CPB (S/N: 401268DF) - Feb 2015
B3: 32GB Samsung M386A4G40DM0-CPB (S/N: 40126BC3) - Feb 2015
B4: 32GB Samsung M386A4G40DM0-CPB (S/N: 40126BA3) - Feb 2015
B5: 32GB Samsung M386A4G40DM0-CPB (S/N: 40126919) - Feb 2015
B6: 32GB Samsung M386A4G40DM0-CPB (S/N: 4012675E) - Feb 2015
B7: 32GB Samsung M386A4G40DM0-CPB (S/N: 40126918) - Feb 2015
B8: 32GB Samsung M386A4G40DM0-CPB (S/N: 40126C42) - Feb 2015
```

**All DIMMs**: DDR4-2133, ECC, Quad Rank, Feb 2015 manufacturing date

---

## 📊 SYSTEM HEALTH (ALL GREEN)

```
✅ Overall System:           OK
✅ CPUs (both):              OK
✅ Memory (all 15 DIMMs):    OK
✅ Storage (all 10 disks):   OK
✅ Power Supplies (both):    OK
✅ Fans (all 6):             OK
✅ Temperatures:             OK
✅ Voltages:                 OK
✅ Intrusion:                OK
✅ Battery:                  OK
✅ SD Card Module:           OK
✅ Licensing:                OK
```

**No warnings, no errors, full redundancy operational**

---

## 🔗 USEFUL LINKS

### **Dell Support**
- **Service Tag Lookup**: https://www.dell.com/support/home/en-us/product-support/servicetag/F93LB42
- **Driver Downloads**: Same URL as above
- **iDRAC Access**: https://<VM180_IP>:443
- **Express Service Code**: 33201963650 (for phone support)

### **Documentation**
- **Full Hardware Inventory**: `DELL-R730-COMPLETE-HARDWARE-INVENTORY.md` (682 lines, comprehensive)
- **Master Knowledge Base**: `ETERNAL-DRAGON-SHENRON-KNOWLEDGE.md` (1100+ lines)
- **Admin Turnover Doc**: `AI-TURNOVER-DELL-PROXMOX-ADMIN.md`

---

## 💡 KEY TAKEAWAYS

### **Strengths**
- ✅ **64 threads** - excellent for virtualization/containerization
- ✅ **480 GB ECC RAM** - stable, reliable, room to grow
- ✅ **55+ TB storage** - huge capacity (SSDs for speed, HDDs for bulk)
- ✅ **Fully redundant** - dual PSUs, N+1 fan config
- ✅ **4 GPUs available** - NVIDIA GRID K1 for GPU passthrough
- ✅ **Enterprise-grade** - Dell PowerEdge reliability
- ✅ **All systems healthy** - no hardware issues

### **Opportunities**
- 💰 **Memory**: Can add 288 GB more (current ~$1500 for 9x 32GB DIMMs)
- 🌐 **10GbE**: Add 10 Gigabit Ethernet card (4 empty PCIe slots)
- 🚀 **NVMe**: Add NVMe adapter for ultra-fast storage
- 🎮 **More GPUs**: 4 empty slots for additional GPU passthrough

### **Maintenance Notes**
- 🔄 **BIOS**: Current 2.19.0 is recent (Dec 2023)
- 🔄 **iDRAC**: 2.82.82.82 is latest for iDRAC8 Enterprise
- ⚠️ **DIMMs**: 10 years old (Feb 2015) - consider testing/replacement if errors occur
- ⚠️ **CMOS Battery**: Check/replace every 3-5 years (server age: 9+ years)

---

## 📞 EMERGENCY HARDWARE SUPPORT

### **If Hardware Fails**
1. **Check iDRAC**: https://<VM180_IP>
2. **Review alerts**: System → Alerts
3. **Check logs**: iDRAC → Logs → Hardware Logs
4. **Dell Support**: Call 1-800-456-3355 with Express Service Code: **33201963650**

### **Component Replacement**
- **Dell Warranty**: Check status at dell.com/support using Service Tag F93LB42
- **Memory**: Samsung M386A4G40DM0-CPB or compatible DDR4-2133 ECC RDIMM
- **PSU**: Dell 1100W Hot-Plug (part numbers: 0TFR9VA01 or 0Y26KXA02)
- **Fans**: Dell R730 fan modules (hot-swappable)

---

**Last Updated**: November 6, 2025  
**Next Review**: Quarterly (February 2026)  
**Inventory Source**: iDRAC XML export  
**Service Tag**: F93LB42  
**Owner**: Seth Schultz - LightSpeedUp Hosting

✨ **Status: ALL SYSTEMS OPERATIONAL** ✨

