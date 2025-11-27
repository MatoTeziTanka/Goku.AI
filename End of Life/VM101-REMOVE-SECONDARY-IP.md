<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🌐 VM101 Secondary IP Address Removal Guide

**Issue:** Secondary IP address `<EDGEROUTER_IP>81` is dynamically assigned via DHCP  
**Goal:** VM101 should only have ONE IP address: `<VM101_IP>`  
**Exception:** Only keep if `.181` is intended as a fallback

---

## 🔍 Current Network Configuration

**From netplan:**
```yaml
# /etc/netplan/00-installer-config.yaml
network:
  version: 2
  ethernets:
    enp6s18:
      dhcp4: false
      dhcp6: false
      addresses:
        - <VM101_IP>/24
      gateway4: <EDGEROUTER_IP>
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]

# /etc/netplan/50-cloud-init.yaml
network:
  version: 2
  ethernets:
    enp6s18:
      dhcp4: true  # ← THIS IS THE PROBLEM
```

**Problem:**
- Primary IP (<VM101_IP>) is static (correct)
- Secondary IP (<EDGEROUTER_IP>81) is from DHCP (unwanted)
- Cloud-init is enabling DHCP even though static IP is configured

---

## 🎯 Solution: Disable DHCP in Cloud-Init

### **Option 1: Disable Cloud-Init Network (Recommended)**

**Edit cloud-init config:**
```bash
sudo nano /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
```

**Add:**
```yaml
network:
  config: disabled
```

**Or create the file:**
```bash
sudo tee /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg > /dev/null << 'EOF'
network:
  config: disabled
EOF
```

### **Option 2: Override Netplan Config**

**Edit cloud-init netplan:**
```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```

**Change:**
```yaml
network:
  version: 2
  ethernets:
    enp6s18:
      dhcp4: false  # ← Change from true to false
      dhcp6: false
```

### **Option 3: Remove Cloud-Init Netplan (If Not Needed)**

**If you don't need cloud-init network management:**
```bash
sudo rm /etc/netplan/50-cloud-init.yaml
```

---

## 🛠️ Step-by-Step Fix

### **Step 1: Check Current IPs**

```bash
ip -4 addr show enp6s18
```

**Should show:**
- `<VM101_IP>/24` (static, primary)
- `<EDGEROUTER_IP>81/24` (dynamic, secondary) ← Remove this

### **Step 2: Disable Cloud-Init DHCP**

```bash
# Create cloud-init override
sudo tee /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg > /dev/null << 'EOF'
network:
  config: disabled
EOF

# Or edit netplan directly
sudo nano /etc/netplan/50-cloud-init.yaml
# Change dhcp4: true to dhcp4: false
```

### **Step 3: Apply Netplan Changes**

```bash
# Test netplan config
sudo netplan try

# If test succeeds, apply permanently
sudo netplan apply
```

### **Step 4: Release DHCP Lease**

```bash
# Release the DHCP lease
sudo dhclient -r enp6s18

# Or if using NetworkManager
sudo nmcli connection down enp6s18
sudo nmcli connection up enp6s18
```

### **Step 5: Verify Single IP**

```bash
# Check IP addresses
ip -4 addr show enp6s18

# Should only show:
# inet <VM101_IP>/24 scope global enp6s18
```

### **Step 6: Restart Network (If Needed)**

```bash
# Restart networking
sudo systemctl restart networking

# Or reboot (if changes don't take effect)
sudo reboot
```

---

## 🔍 Verification Commands

```bash
# Check IPs
ip -4 addr show enp6s18 | grep inet

# Check netplan
sudo netplan get

# Check cloud-init
cat /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg

# Check DHCP leases
cat /var/lib/dhcp/dhclient.leases | grep -A 10 enp6s18
```

---

## 🚨 If .181 is Intended as Fallback

**If you want to keep `.181` as a fallback IP:**

### **Option 1: Static Secondary IP**

**Edit netplan:**
```yaml
network:
  version: 2
  ethernets:
    enp6s18:
      dhcp4: false
      dhcp6: false
      addresses:
        - <VM101_IP>/24
        - <EDGEROUTER_IP>81/24  # Static secondary
      gateway4: <EDGEROUTER_IP>
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

**Apply:**
```bash
sudo netplan apply
```

### **Option 2: Keep DHCP for Fallback**

**If you want DHCP as fallback:**
- Keep current config
- Document that `.181` is a fallback IP
- Monitor which IP is used

**⚠️ Note:** Having two IPs can cause routing issues. Only use if you have a specific need.

---

## 📋 Recommended Configuration

**Final netplan config (`/etc/netplan/00-installer-config.yaml`):**
```yaml
network:
  version: 2
  ethernets:
    enp6s18:
      dhcp4: false
      dhcp6: false
      addresses:
        - <VM101_IP>/24
      gateway4: <EDGEROUTER_IP>
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

**Cloud-init override (`/etc/cloud/cloud.cfg.d/99-disable-network-config.cfg`):**
```yaml
network:
  config: disabled
```

**Or remove cloud-init netplan:**
```bash
sudo rm /etc/netplan/50-cloud-init.yaml
```

---

## 🛠️ Quick Fix Script

**Create `remove-secondary-ip.sh`:**
```bash
#!/bin/bash
# Remove secondary DHCP IP from VM101

set -e

echo "🔧 Removing secondary IP address (<EDGEROUTER_IP>81)..."

# Step 1: Disable cloud-init network
echo "1. Disabling cloud-init network..."
sudo tee /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg > /dev/null << 'EOF'
network:
  config: disabled
EOF

# Step 2: Disable DHCP in cloud-init netplan
echo "2. Disabling DHCP in cloud-init netplan..."
if [ -f /etc/netplan/50-cloud-init.yaml ]; then
    sudo sed -i 's/dhcp4: true/dhcp4: false/g' /etc/netplan/50-cloud-init.yaml
    sudo sed -i 's/dhcp6: true/dhcp6: false/g' /etc/netplan/50-cloud-init.yaml
fi

# Step 3: Release DHCP lease
echo "3. Releasing DHCP lease..."
sudo dhclient -r enp6s18 2>/dev/null || true

# Step 4: Apply netplan
echo "4. Applying netplan..."
sudo netplan apply

# Step 5: Verify
echo "5. Verifying IP addresses..."
ip -4 addr show enp6s18 | grep inet

echo ""
echo "✅ Done! VM101 should now only have <VM101_IP>"
echo "   If secondary IP still appears, reboot: sudo reboot"
```

**Run:**
```bash
chmod +x remove-secondary-ip.sh
./remove-secondary-ip.sh
```

---

## ✅ Expected Result

**Before:**
```
2: enp6s18: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    inet <VM101_IP>/24 brd 192.168.12.255 scope global enp6s18
    inet <EDGEROUTER_IP>81/24 metric 100 brd 192.168.12.255 scope global secondary dynamic enp6s18
```

**After:**
```
2: enp6s18: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    inet <VM101_IP>/24 brd 192.168.12.255 scope global enp6s18
```

---

**VM101 should only have ONE IP: <VM101_IP>** 🌐




