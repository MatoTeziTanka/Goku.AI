<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# SHENRON Current Hardware Configuration - November 6, 2025

## VM100 - GOKU-AI Domain Controller (Beast Mode)

**Last Updated**: November 6, 2025  
**Status**: AI Beast Mode (Pre-Customer Maximum Performance)

### Hardware Allocation
- **CPU**: 2 sockets × 13 cores = **26 vCPUs**
- **RAM**: **192 GB** (196,608 MiB)
- **Storage**: ZFS pool (details in infrastructure docs)
- **Network**: <VM100_IP> (static)

### Physical Host
- **Server**: Dell PowerEdge R730
- **CPUs**: 2× Intel Xeon E5-2690 v4 (14 cores each, 28 cores total)
- **Total RAM**: 256 GB DDR4 ECC
- **Hypervisor**: Proxmox VE 8.x

### AI Models Running
1. **GOKU** (DeepSeek-Coder-V2-Lite 16B): 163,840 context, 8,192 max tokens
2. **VEGETA** (Llama 3.2 3B): 32,768 context, 4,096 max tokens
3. **PICCOLO** (Qwen2.5-Coder 7B): 32,768 context, 4,096 max tokens
4. **GOHAN** (Mistral 7B v0.3): 32,768 context, 4,096 max tokens
5. **KRILLIN** (Phi-3-Mini 128K): 128,000 context, 2,048 max tokens
6. **FRIEZA** (Phi-3-Mini 128K): 128,000 context, 2,048 max tokens

**Total AI RAM Usage**: ~63 GB  
**Available RAM**: ~129 GB for ChromaDB, system, and future expansion

### Scaling Plan
- **Current**: 192GB RAM (75% of server total) - Pre-customer maximum
- **Light Load**: Can maintain 192GB with 1-5 customer VMs
- **Medium Load**: Scale to 128-160GB when 6-15 customer VMs active
- **Heavy Load**: Scale to 96GB when 16+ customer VMs active

### Performance Capabilities
- Can process **~150 pages** of code in single context (GOKU)
- Can handle **entire codebases** up to 128K tokens (KRILLIN/FRIEZA)
- Supports 3-5 simultaneous web UI queries
- Fast parallel inference with 26 CPU cores
- Large vector database operations via ChromaDB

### Services Running
- **LM Studio**: Port 1234 (AI model serving)
- **SHENRON API**: Port 5000 (orchestrator)
- **ChromaDB**: Embedded vector database (~82.57 MB)
- **Active Directory**: Domain Controller
- **SSH Server**: Port 22

### Auto-Start Configuration
- ✅ LM Studio: Auto-starts via Registry
- ✅ SHENRON Service: Auto-starts via NSSM (Windows Service)
- ⚠️ AI Models: Manual load required after reboot (no session restore)
- ✅ Model Auto-Loader: Startup script attempts to restore session

### Current Status (as of Nov 6, 2025)
- Operating System: Windows Server 2025 (Domain Controller)
- Uptime: Recently rebooted for hardware upgrade
- All services: Operational
- AI Models: 6/6 loaded and responding
- Knowledge Base: 6,977 documents ingested

### Notes
This is a **pre-customer configuration** optimized for maximum AI performance. As LightSpeedUp acquires customers, VM100 will be scaled back to allocate resources to revenue-generating customer VMs. See VM100-BEAST-MODE-UPGRADE.md for detailed scaling strategy.

