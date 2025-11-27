<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Port Allocation Reference

**Last Updated**: October 31, 2025

This document tracks all port allocations across the passive income infrastructure to prevent conflicts and ensure proper firewall configuration.

---

## 🌐 Standard Ports (All VMs)

| Port | Protocol | Service | Access |
|------|----------|---------|--------|
| 22 | TCP | SSH | LAN Only |

---

## 🖥️ VM-Specific Port Allocations

### VM101 - Management & AI Assistant
| Port | Service | Status | Notes |
|------|---------|--------|-------|
| 22 | SSH | ✅ Active | Key-based auth |

### VM120 - Reverse Proxy & Cloudflare Tunnel
| Port | Service | Status | Notes |
|------|---------|--------|-------|
| 22 | SSH | ✅ Active | Key-based auth |
| 80 | Nginx (HTTP) | ✅ Active | Proxies to backend VMs |
| 443 | Nginx (HTTPS) | 🔒 Internal | Cloudflare Tunnel handles external HTTPS |

### VM150 - WordPress Server
| Port | Service | Status | Notes |
|------|---------|--------|-------|
| 22 | SSH | ✅ Active | Key-based auth |
| 80 | Apache (HTTP) | ✅ Active | Behind Nginx reverse proxy |
| 3306 | MySQL | 🔒 Internal | Database (localhost only) |
| 6379 | Redis | 🔒 Internal | Object cache (localhost only) |

---

## 🎮 Game Server Ports (Planned - VM170)

### Minecraft Servers
| Port | Service | Status | Notes |
|------|---------|--------|-------|
| 25565 | Minecraft Java | ⏭️ Planned | Default Minecraft port |
| 25566 | Minecraft Java #2 | ⏭️ Planned | Additional server |
| 19132 | Minecraft Bedrock | ⏭️ Planned | Bedrock Edition (UDP) |

### Other Game Servers
| Port | Service | Status | Notes |
|------|---------|--------|-------|
| 7777-7778 | ARK: Survival Evolved | ⏭️ Planned | Game + Query ports |
| 27015-27016 | Steam/ARK | ⏭️ Planned | Steam query ports |
| 2456-2458 | Valheim | ⏭️ Planned | Game ports (UDP) |
| 28015-28016 | Rust | ⏭️ Planned | Game + RCON |
| 7000-7001 | Terraria | ⏭️ Planned | Game port |
| 26900 | 7 Days to Die | ⏭️ Planned | Game port |

---

## 🤖 Discord Bot Ports (Planned - VM160)

| Port | Service | Status | Notes |
|------|---------|--------|-------|
| 22 | SSH | ⏭️ Planned | Management access |
| 3000 | Bot Dashboard | ⏭️ Planned | Web interface (internal) |
| 5432 | PostgreSQL | ⏭️ Planned | Bot database (internal) |

**Note**: Discord bots connect outbound to Discord API (no inbound ports needed)

---

## 🔌 API Service Ports (Planned - VM180)

| Port Range | Service | Status | Notes |
|------------|---------|--------|-------|
| 22 | SSH | ⏭️ Planned | Management access |
| 3000 | API Service #1 | ⏭️ Planned | Behind Nginx reverse proxy |
| 3001 | API Service #2 | ⏭️ Planned | Behind Nginx reverse proxy |
| 3002 | API Service #3 | ⏭️ Planned | Behind Nginx reverse proxy |
| 5432 | PostgreSQL | ⏭️ Planned | API database (internal) |
| 6379 | Redis | ⏭️ Planned | Rate limiting cache (internal) |

---

## 🌍 Cloudflare Tunnel Routes

All external HTTP/HTTPS traffic flows through Cloudflare Tunnel on VM120.

### Active Routes
| Hostname | Backend Service | Target VM | Port | Status |
|----------|----------------|-----------|------|--------|
| wp.lightspeedup.com | WordPress | VM150 | 80 | ✅ Active |

### Planned Routes
| Hostname | Backend Service | Target VM | Port | Status |
|----------|----------------|-----------|------|--------|
| api.lightspeedup.com | API Gateway | VM180 | 3000 | ⏭️ Planned |
| game.lightspeedup.com | Game Panel | VM170 | 8080 | ⏭️ Planned |
| bot.lightspeedup.com | Bot Dashboard | VM160 | 3000 | ⏭️ Planned |

---

## 🔒 Internal-Only Ports (Never Exposed)

These ports should **NEVER** be exposed to the internet or included in UFW allow rules:

| Port | Service | Reason |
|------|---------|--------|
| 3306 | MySQL/MariaDB | Database should only accept localhost connections |
| 5432 | PostgreSQL | Database should only accept localhost connections |
| 6379 | Redis | Cache should only accept localhost connections |
| 27017 | MongoDB | Database should only accept localhost connections |

---

## 🛡️ Port Forwarding (EdgeRouter)

### Current Port Forwards
- **None** - All HTTP/HTTPS traffic uses Cloudflare Tunnel

### Future Port Forwards (If Needed)
Some services may require direct port forwarding if Cloudflare Tunnel doesn't support them:

| External Port | Internal IP | Internal Port | Service | Status |
|---------------|-------------|---------------|---------|--------|
| 25565 | <VM170_IP> | 25565 | Minecraft Java | ⏭️ If needed |
| 19132 | <VM170_IP> | 19132 | Minecraft Bedrock (UDP) | ⏭️ If needed |

**Note**: Prefer Cloudflare Tunnel or Cloudflare Spectrum (for UDP/TCP) over direct port forwarding when possible.

---

## 📝 Port Allocation Guidelines

### When Adding New Services

1. **Check this document** to ensure the port isn't already allocated
2. **Choose appropriate port range**:
   - 80, 443: Reserved for web servers
   - 3000-3999: Node.js/API services
   - 5000-5999: Python Flask/FastAPI services
   - 8000-8999: Alternative web services
   - 9000-9999: Misc. services
   - 25000-28000: Game servers
3. **Update this document** with the new allocation
4. **Configure UFW** on the target VM:
   ```bash
   sudo ufw allow PORT/tcp
   # or
   sudo ufw allow PORT/udp
   ```
5. **Update Nginx reverse proxy** (if applicable)
6. **Test connectivity** before marking as active

---

## 🔍 Checking Port Usage

### On a Specific VM
```bash
# Check listening ports
sudo ss -tulnp

# Check specific port
sudo lsof -i :PORT

# Check all open ports
sudo netstat -tulnp | grep LISTEN
```

### Network-Wide Scan
```bash
# Scan all VMs from VM101
nmap -p- <VM101_IP>-199
```

---

## ⚠️ Port Conflict Resolution

If you encounter a port conflict:

1. **Identify the conflicting service**:
   ```bash
   sudo lsof -i :PORT
   ```

2. **Options**:
   - Change the new service to use a different port
   - Stop and disable the conflicting service (if unused)
   - Reconfigure the existing service to use a different port

3. **Update this document** with the resolution

---

## 🔐 Security Best Practices

### ✅ DO:
- Use non-standard ports for SSH if exposing to internet (e.g., 2222 instead of 22)
- Keep databases on internal-only ports
- Use Cloudflare Tunnel for HTTP/HTTPS services
- Document every port allocation in this file
- Use UFW to restrict access to necessary ports only

### ❌ DON'T:
- Expose database ports (3306, 5432, etc.) to the internet
- Use well-known ports for custom services
- Forget to update UFW rules when adding ports
- Reuse ports across different VMs for different services (causes confusion)

---

**Maintained By**: AI Infrastructure Team  
**Project Owner**: MatoTeziTanka  
**Repository**: https://github.com/MatoTeziTanka/PassiveIncome




