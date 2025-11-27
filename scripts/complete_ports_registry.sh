#!/bin/bash
# Complete Ports Registry with known ports
# Run this on VM101 to update the Ports Registry

cd ~/GitHub/Goku.AI

PORTS_FILE="docs/infrastructure/PORTS_REGISTRY.md"

echo "======================================================================"
echo "COMPLETING PORTS REGISTRY"
echo "======================================================================"
echo

# Backup existing file
if [ -f "$PORTS_FILE" ]; then
    cp "$PORTS_FILE" "${PORTS_FILE}.backup"
    echo "✅ Created backup: ${PORTS_FILE}.backup"
fi

# Create updated ports registry
cat > "$PORTS_FILE" << 'EOF'
# 🚢 Master Ports Registry

> **CRITICAL RESOURCE:** This document tracks ALL network ports used across the infrastructure to prevent conflicts.
> **Rule:** Do NOT start a new service without checking this table first.

## 🟢 VM100 (Inference Node / LM Studio)
**IP Address:** 192.168.12.100

| Service Name       | Internal Port | External Port | Protocol | Status | Notes |
|-------------------|---------------|---------------|----------|--------|-------|
| LM Studio Server  | 1234          | 1234          | TCP      | Active | Main LLM Engine - http://192.168.12.100:1234 |

## 🔵 VM101 (Control Node / Goku.AI)
**IP Address:** 192.168.12.101

| Service Name       | Internal Port | External Port | Protocol | Status | Notes |
|-------------------|---------------|---------------|----------|--------|-------|
| SHENRON API       | 5000          | 5000          | TCP      | Active | Core Agent API - http://192.168.12.101:5000 |
| Code Server       | 9001          | 9001          | TCP      | Active | VS Code in Browser - http://192.168.12.101:9001 |
| Shenron Dashboard | 8501          | 8501          | TCP      | Planned| Streamlit UI |
| Vector DB (Chroma)| 8000          | 8000          | TCP      | Planned| Knowledge Base |

## 🟡 VM120 (Reverse Proxy / Cloudflare Tunnel)
**IP Address:** 192.168.12.120

| Service Name       | Internal Port | External Port | Protocol | Status | Notes |
|-------------------|---------------|---------------|----------|--------|-------|
| Nginx HTTP        | 80            | 80            | TCP      | Active | Reverse Proxy |
| Nginx HTTPS       | 443           | 443           | TCP      | Active | SSL Termination |
| Cloudflare Tunnel | -             | -             | TCP      | Active | Cloudflare Tunnel Service |
| SSH               | 22            | 22            | TCP      | Active | Admin Access |

## 🟠 VM150 (WordPress / HTML Frontend)
**IP Address:** 192.168.12.150

| Service Name       | Internal Port | External Port | Protocol | Status | Notes |
|-------------------|---------------|---------------|----------|--------|-------|
| Apache HTTP        | 80            | 80            | TCP      | Active | WordPress / HTML Frontend |
| Apache HTTPS       | 443           | 443           | TCP      | Active | SSL (via Cloudflare) |
| SSH                | 22            | 22            | TCP      | Active | Admin Access |

## 🟠 Reserved / Common

| Service           | Port  | Notes |
|-------------------|-------|-------|
| SSH               | 22    | Admin Access (All VMs) |
| RDP               | 3389  | Windows Remote Desktop |
| HTTP/HTTPS        | 80/443| Web Traffic |
| MySQL             | 3306  | Database (if used) |
| PostgreSQL        | 5432  | Database (if used) |

## 📋 Port Allocation Rules

1. **Check this file FIRST** before assigning any port
2. **Register immediately** when assigning a new port
3. **Update status** when services start/stop
4. **Document conflicts** if a port is already in use
5. **Use next available** if preferred port is taken

## 🔍 How to Check Port Availability

```bash
# On Linux
sudo ss -tlnp | grep :PORT_NUMBER

# On Windows
netstat -ano | findstr :PORT_NUMBER
```

## ⚠️ Port Conflicts

If you encounter a port conflict:
1. Check this registry
2. Identify the conflicting service
3. Choose next available port
4. Update this registry immediately
5. Update service configuration
EOF

echo "✅ Updated: $PORTS_FILE"
echo
echo "======================================================================"
echo "PORTS REGISTRY COMPLETE"
echo "======================================================================"
echo
echo "Registered ports:"
echo "  - VM100: 1234 (LM Studio)"
echo "  - VM101: 5000 (API), 9001 (Code Server)"
echo "  - VM120: 80, 443 (Reverse Proxy)"
echo "  - VM150: 80, 443 (WordPress/HTML)"
echo
echo "Next: Review and add any missing ports manually"
echo

