<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🚀 VM100 BEAST MODE UPGRADE - November 6, 2025

**Status:** ✅ COMPLETE  
**Upgraded By:** Seth Schultz  
**Reason:** Maximize AI performance before customer onboarding

---

## 📊 UPGRADE SUMMARY

### **BEFORE (Original Config):**
- **CPU**: 1 socket, 20 cores = **20 vCPUs**
- **RAM**: 81,920 MiB (**80 GB**)
- **Purpose**: Basic AI workload

### **AFTER (Beast Mode):**
- **CPU**: 2 sockets, 26 cores = **26 vCPUs** (+6 cores, +30%)
- **RAM**: 196,608 MiB (**192 GB**) (+112 GB, +140%)
- **Purpose**: Maximum AI performance with full context lengths

---

## 🎯 CONFIGURATION DETAILS

### **Hardware Allocation:**
```bash
VM ID: 100
Name: VM100-GOKU-AI-DC
Sockets: 2
Cores per socket: 13
Total vCPUs: 26 (out of 28 physical cores)
Memory: 196608 MiB (192 GB)
Host Reserved: 2 cores, 64 GB RAM
```

### **Proxmox Command Used:**
```bash
qm stop 100
qm set 100 -memory 196608
qm set 100 -sockets 2
qm set 100 -cores 13
qm start 100
```

---

## 🐉 AI MODEL CONFIGURATION

### **All 6 Warriors - Full Power Settings:**

| Warrior | Model | Context Length | Max Tokens | Est. RAM |
|---------|-------|----------------|------------|----------|
| 🥋 GOKU | DeepSeek-Coder-V2-Lite 16B | **163,840** | 8,192 | ~25 GB |
| 👑 VEGETA | Llama 3.2 3B | **32,768** | 4,096 | ~4 GB |
| 🧠 PICCOLO | Qwen2.5-Coder 7B | **32,768** | 4,096 | ~7 GB |
| ⚠️ GOHAN | Mistral 7B v0.3 | **32,768** | 4,096 | ~7 GB |
| 🔧 KRILLIN | Phi-3-Mini 128K | **128,000** | 2,048 | ~10 GB |
| 😈 FRIEZA | Phi-3-Mini 128K | **128,000** | 2,048 | ~10 GB |

**Total AI RAM Usage**: ~63 GB  
**Remaining for System**: ~129 GB

---

## 💡 RATIONALE

### **Why 192GB RAM?**
1. ✅ Run all 6 AI models at **full native context lengths**
2. ✅ GOKU can use its full 163K context (was limited to 32K before)
3. ✅ KRILLIN & FRIEZA can use full 128K context (4x increase)
4. ✅ Massive headroom for ChromaDB vector operations
5. ✅ Can load additional models for testing (Mixtral, Llama 70B)
6. ✅ Easy to scale back when customers arrive

### **Why 26 vCPUs (2 sockets)?**
1. ✅ Better NUMA performance (each socket has dedicated memory channels)
2. ✅ 4+ cores per AI model for parallel inference
3. ✅ Faster response times for complex queries
4. ✅ Can handle multiple simultaneous requests
5. ✅ Leaves 2 physical cores for Proxmox host

---

## 📈 PERFORMANCE IMPROVEMENTS

### **Expected Benefits:**
- **Context Processing**: 4-5x faster (163K vs 32K for GOKU)
- **Parallel Inference**: 30% faster with 26 vs 20 cores
- **Memory Headroom**: Can cache more model layers in RAM
- **Simultaneous Queries**: Can handle 3-5 concurrent web requests
- **RAG Operations**: ChromaDB can load larger vector databases

### **Real-World Impact:**
- **Before**: GOKU limited to ~30 pages of code context
- **After**: GOKU can process **~150 pages** of code context
- **Before**: KRILLIN/FRIEZA limited to ~30K tokens
- **After**: KRILLIN/FRIEZA can handle **128K tokens** (entire codebases)

---

## ⚠️ SCALING STRATEGY

### **When Customers Arrive:**

**Phase 1: Light Customer Load (1-5 VMs)**
- Keep VM100 at 192GB RAM
- Reduce to 160GB if needed (still plenty for AI)

**Phase 2: Medium Customer Load (6-15 VMs)**
- Reduce VM100 to **128GB RAM** (still 1.5x original!)
- Keep 26 vCPUs
- Reduce AI context lengths slightly:
  - GOKU: 163K → 128K
  - KRILLIN/FRIEZA: 128K → 64K

**Phase 3: Heavy Customer Load (16+ VMs)**
- Reduce VM100 to **96GB RAM** (still more than original 80GB)
- Reduce to 20 vCPUs
- Use conservative context lengths:
  - GOKU: 128K → 64K
  - KRILLIN/FRIEZA: 64K → 32K

### **Monitoring Commands:**
```bash
# Check Proxmox host RAM usage
free -h

# Check VM100 RAM usage
ssh Administrator@<VM100_IP> 'systeminfo | findstr "Available Physical Memory"'

# Check LM Studio RAM usage
ssh Administrator@<VM100_IP> 'tasklist /FI "IMAGENAME eq LM Studio.exe" /FO TABLE'
```

---

## 🎯 NEXT STEPS

### **Immediate (Done):**
- ✅ Upgraded VM100 to 26 vCPUs, 192GB RAM
- ✅ All 6 AI models loaded with full context lengths
- ✅ LM Studio configured for maximum performance

### **Knowledge Injection (Next):**
- [ ] Inject this upgrade documentation into Shenron
- [ ] Update SHENRON with current hardware specs
- [ ] Inject scaling strategy for when customers arrive
- [ ] Document model context length configurations

### **Future Enhancements:**
- [ ] Load additional large models (Mixtral 8x22B, Llama 70B) for testing
- [ ] Benchmark performance improvements
- [ ] Set up automated monitoring alerts
- [ ] Create customer onboarding playbook with auto-scaling

---

## 📝 TECHNICAL NOTES

### **NUMA Configuration:**
- 2-socket config = each socket has dedicated memory channels
- Better memory bandwidth for AI inference
- Windows Server 2025 automatically handles NUMA optimization

### **Hyper-Threading:**
- Physical cores: 28 (14 per socket)
- VM100 uses: 26 physical cores
- Proxmox host: 2 physical cores + 56 logical threads via HT
- Customer VMs can use logical threads when needed

### **Memory Layout:**
- Total Server RAM: 256 GB
- VM100: 192 GB (75%)
- Proxmox Host: ~8 GB
- Available for Customers: ~56 GB (can run 5-10 VMs)

---

## 🔧 ROLLBACK PROCEDURE

If needed, revert to original config:

```bash
ssh root@<PROXMOX_IP>
qm stop 100
qm set 100 -memory 81920
qm set 100 -sockets 1
qm set 100 -cores 20
qm start 100
```

---

## 📊 VERIFICATION

### **Confirm New Settings:**
```powershell
# On VM100
systeminfo | findstr /C:"Total Physical Memory"
# Should show: ~196 GB

$env:NUMBER_OF_PROCESSORS
# Should show: 26

Get-WmiObject Win32_ComputerSystem | Select-Object NumberOfProcessors, NumberOfLogicalProcessors
# Processors: 2, Logical: 26
```

### **LM Studio Health Check:**
```powershell
# Check models loaded
Invoke-RestMethod http://localhost:1234/v1/models

# Should show 6 models with their context lengths
```

---

## 🎉 OUTCOME

**VM100 is now an AI POWERHOUSE!**
- ✅ 2.4x more RAM
- ✅ 30% more CPU cores
- ✅ 5x larger context windows for GOKU
- ✅ 4x larger context for KRILLIN/FRIEZA
- ✅ Ready for production AI workloads
- ✅ Can scale back gracefully when needed

**Status**: OPERATIONAL - BEAST MODE ENGAGED 🐉⚡

---

*For questions or scaling adjustments, refer to the scaling strategy above or contact Seth.*

