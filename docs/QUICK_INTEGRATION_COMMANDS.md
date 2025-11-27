# 🚀 Quick Integration Commands for v3.0.0

**For:** Copy/paste into SSH session on VM101  
**Location:** Run from `~/GitHub/Goku.AI`

---

## ⚡ One-Command Integration (Recommended)

```bash
cd ~/GitHub/Goku.AI && chmod +x scripts/complete_v3_integration.sh && bash scripts/complete_v3_integration.sh
```

This runs all three steps automatically.

---

## 📋 Step-by-Step Commands

### **Step 1: Integrate Master Prompt**

```bash
cd ~/GitHub/Goku.AI
python3 scripts/integrate_master_prompt_v3.py
```

**What it does:**
- Adds Master Prompt loading to API
- Adds operational mode functions
- Updates warrior query to use Master Prompt
- Creates backup of original file

---

### **Step 2: Create Warrior State Machines**

```bash
cd ~/GitHub/Goku.AI
python3 scripts/create_warrior_states.py
```

**What it does:**
- Creates `src/services/warrior_states.py`
- Creates `src/services/warrior_states.json`
- Implements state tracking for all 6 warriors

---

### **Step 3: Complete Ports Registry**

```bash
cd ~/GitHub/Goku.AI
chmod +x scripts/complete_ports_registry.sh
bash scripts/complete_ports_registry.sh
```

**What it does:**
- Updates `docs/infrastructure/PORTS_REGISTRY.md`
- Adds all known ports (VM100, VM101, VM120, VM150)
- Creates backup of original file

---

## ✅ Verification Commands

After running integration, verify:

```bash
# Check Master Prompt integration
grep -n "MASTER_PROMPT" src/api/shenron_api_v5_mcp.py

# Check state machines exist
ls -la src/services/warrior_states.*

# Check ports registry updated
grep -A 5 "VM120" docs/infrastructure/PORTS_REGISTRY.md

# Test API syntax
python3 -m py_compile src/api/shenron_api_v5_mcp.py
```

---

## 🔧 Manual Integration (If Scripts Fail)

### **1. Add Master Prompt to API**

Edit `src/api/shenron_api_v5_mcp.py` and add after imports:

```python
from pathlib import Path as PathLib

# Load Master Prompt
MASTER_PROMPT_PATH = PathLib(__file__).parent.parent.parent.parent / "MASTER_PROMPT_PRODUCTION.md"
MASTER_PROMPT = MASTER_PROMPT_PATH.read_text(encoding='utf-8') if MASTER_PROMPT_PATH.exists() else "# Master Prompt v3.0.0"

def get_system_message(mode: str = "coder") -> str:
    modes = {
        "coder": "CODER MODE (Goku/Vegeta): Strict v3.0.0 adherence.",
        "debug": "DEBUG MODE (Shenron): Root cause analysis.",
        "architect": "ARCHITECT MODE: Pure system design.",
        "strategy": "STRATEGY MODE (Frieza): Business logic.",
        "teaching": "TEACHING MODE (Gohan): Explain concepts."
    }
    return f"{MASTER_PROMPT}\n\n{modes.get(mode, modes['coder'])}"
```

Then update warrior query to use it (around line 380):

```python
payload = {
    "model": model_name,
    "messages": [
        {
            "role": "system",
            "content": get_system_message("coder")
        },
        {
            "role": "user",
            "content": query
        }
    ],
    # ... rest of payload
}
```

### **2. Create State Machines**

Run the script or manually create `src/services/warrior_states.py` (see script for full content).

### **3. Update Ports Registry**

Edit `docs/infrastructure/PORTS_REGISTRY.md` and add VM120 and VM150 sections (see script for format).

---

## 🐛 Troubleshooting

**"Master Prompt not found"**
- Check path: `ls -la ~/GitHub/MASTER_PROMPT_PRODUCTION.md`
- May need to adjust path in script

**"Permission denied"**
- Make scripts executable: `chmod +x scripts/*.sh`

**"Python module not found"**
- Activate venv: `source venv/bin/activate`

**"Syntax error in API"**
- Check backup: `ls -la src/api/*.backup`
- Restore if needed: `mv src/api/shenron_api_v5_mcp.py.backup src/api/shenron_api_v5_mcp.py`

---

**Ready to run!** Copy the one-command integration above and paste into your SSH session.

