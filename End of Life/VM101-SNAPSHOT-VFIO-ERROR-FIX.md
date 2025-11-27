<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔧 VM101 Snapshot VFIO Error - Fix Guide

**Error:** `VFIO migration is not supported in kernel`  
**Cause:** VM101 has PCI passthrough (VFIO) device that cannot be snapshotted  
**Date:** November 23, 2025

---

## 🚨 PROBLEM

**Error Message:**
```
TASK ERROR: VM 101 qmp command 'savevm-start' failed - 
0000:86:00.0: VFIO migration is not supported in kernel
```

**What this means:**
- VM101 has a PCI device passed through directly to the VM (VFIO)
- Device: `0000:86:00.0` (PCI address)
- VFIO devices cannot be snapshotted because they're hardware-attached
- Proxmox cannot save the state of directly-attached hardware

---

## ✅ SOLUTION OPTIONS

### **Option 1: Use Backup Instead of Snapshot (RECOMMENDED)**

**Backups work with VFIO devices** - they copy disk data, not VM state.

**Via Proxmox Web UI:**
1. Go to: **VM 101** → **Backup**
2. Click: **Backup now**
3. Storage: Choose your backup storage
4. Mode: **Stop mode** (safest) or **Snapshot mode** (faster, but may skip VFIO)
5. Compression: `gzip` (recommended)
6. Click: **Backup**

**Via SSH (Command Line):**
```bash
# SSH to Proxmox host
ssh root@<PROXMOX_IP>

# Create backup (stop mode - safest)
vzdump 101 \
    --mode stop \
    --storage local \
    --compress gzip \
    --remove 0

# Or snapshot mode (faster, but may have issues with VFIO)
vzdump 101 \
    --mode snapshot \
    --storage local \
    --compress gzip \
    --remove 0
```

**Expected Output:**
```
INFO: starting new backup job: vzdump 101 --mode stop --storage local --compress gzip
INFO: Starting Backup of VM 101 (qemu)
INFO: status = stopped
INFO: backup mode: stop
INFO: ionice priority: 7
INFO: creating archive '/var/lib/vz/dump/vzdump-qemu-101-2025_11_23-XX_XX_XX.vma.gz'
INFO: starting kvm to execute backup task
INFO:   Logical volume "vm-101-disk-0" created.
...
INFO: Finished Backup of VM 101 (00:XX:XX)
INFO: Backup job finished successfully
```

**✅ Advantages:**
- Works with VFIO devices
- Full disk backup (can restore entire VM)
- Can be stored externally
- More reliable than snapshots

**⏱️ Time:** 5-15 minutes (depending on disk size)

---

### **Option 2: Identify and Temporarily Remove VFIO Device**

**Check what VFIO device is attached:**
```bash
# SSH to Proxmox host
ssh root@<PROXMOX_IP>

# Check VM101 configuration
qm config 101 | grep -i vfio

# Or check all hardware
qm config 101
```

**Look for lines like:**
```
hostpci0: 0000:86:00.0,pcie=1
```

**Temporarily remove VFIO device:**
```bash
# Remove VFIO device
qm set 101 --delete hostpci0

# Create snapshot
qm snapshot 101 vm101-pre-migration-$(date +%Y%m%d)

# Re-add VFIO device (if needed)
qm set 101 --hostpci0 0000:86:00.0,pcie=1
```

**⚠️ Warning:**
- VM will lose access to the passthrough device
- May need to restart VM
- Only do this if the device is not critical

---

### **Option 3: Use Disk-Only Snapshot (If Supported)**

**Some VFIO configurations allow disk snapshots:**
```bash
# Try disk snapshot only (may work)
qm snapshot 101 vm101-pre-migration-$(date +%Y%m%d) --description "Pre-migration disk snapshot"
```

**Note:** This may still fail if VFIO device prevents any snapshot operation.

---

## 🔍 IDENTIFY THE VFIO DEVICE

**Check what device is using VFIO:**
```bash
# On Proxmox host
ssh root@<PROXMOX_IP>

# Check VM101 config
qm config 101

# Look for hostpci lines
# Example output:
# hostpci0: 0000:86:00.0,pcie=1

# Identify the device
lspci -s 86:00.0

# Or check all PCI devices
lspci | grep -i "86:00"
```

**Common VFIO devices:**
- GPU (for passthrough)
- Network card (for direct access)
- Storage controller (for direct disk access)

**Question to ask:**
- Is this device critical for VM101's operation?
- Can VM101 function without it temporarily?
- Is it needed for the migration?

---

## 📋 RECOMMENDED APPROACH

**For Migration Safety:**

1. **Use Backup (Option 1)** - Most reliable
   ```bash
   vzdump 101 --mode stop --storage local --compress gzip
   ```

2. **Verify Backup:**
   ```bash
   # List backups
   ls -lh /var/lib/vz/dump/vzdump-qemu-101-*.vma.gz
   
   # Check backup size (should be reasonable)
   du -sh /var/lib/vz/dump/vzdump-qemu-101-*.vma.gz
   ```

3. **Proceed with Migration:**
   - Backup is your restore point
   - Can restore entire VM if needed
   - More reliable than snapshot for VFIO VMs

---

## 🔄 RESTORE FROM BACKUP (If Needed)

**Via Proxmox Web UI:**
1. Go to: **Datacenter** → **Backup**
2. Find: `vzdump-qemu-101-YYYY_MM_DD-XX_XX_XX.vma.gz`
3. Click: **Restore**
4. Choose: Target VM (101) or new VM ID
5. Click: **Restore**

**Via SSH:**
```bash
# Restore backup
qmrestore /var/lib/vz/dump/vzdump-qemu-101-YYYY_MM_DD-XX_XX_XX.vma.gz 101

# Or restore to new VM
qmrestore /var/lib/vz/dump/vzdump-qemu-101-YYYY_MM_DD-XX_XX_XX.vma.gz 999 --storage local
```

---

## ✅ VERIFICATION

**After creating backup:**
```bash
# Check backup exists
ls -lh /var/lib/vz/dump/vzdump-qemu-101-*.vma.gz

# Check backup integrity (optional)
vzdump --verify /var/lib/vz/dump/vzdump-qemu-101-YYYY_MM_DD-XX_XX_XX.vma.gz
```

**Expected:**
- Backup file exists
- File size is reasonable (not 0 bytes)
- Backup verification passes (if checked)

---

## 🎯 NEXT STEPS

**After successful backup:**

1. ✅ **Backup created** - You have a restore point
2. ✅ **Proceed with Step 2** - Generate SSH keys
3. ✅ **Continue migration** - Follow `VM101-MIGRATION-EXECUTION-GUIDE.md`

**The backup serves the same purpose as a snapshot:**
- Full VM restore capability
- Pre-migration safety net
- Can rollback if needed

---

## 📝 NOTES

**Why VFIO prevents snapshots:**
- VFIO = Virtual Function I/O (PCI passthrough)
- Device is directly attached to VM (bypasses hypervisor)
- Hypervisor cannot save/restore hardware state
- Snapshot requires full VM state capture (impossible with direct hardware)

**Why backups work:**
- Backups copy disk data, not hardware state
- VFIO device configuration is saved in VM config
- On restore, VM config is restored (including VFIO)
- Device reattaches on VM start

---

**Last Updated:** November 23, 2025  
**Status:** ✅ Solution Documented




