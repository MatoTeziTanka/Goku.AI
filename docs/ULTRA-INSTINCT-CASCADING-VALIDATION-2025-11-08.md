<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# ULTRA INSTINCT CASCADING VALIDATION – 2025-11-08

## Summary
- Quantized all six LM Studio fighters to `Q8_0` and imported them via `lms import --yes --copy`, ensuring both the new and legacy Q4 builds remain available.
- Reloaded LM Studio with `--identifier` aliases so Shenron can address each warrior explicitly.
- Enforced a 72 GB balloon limit for VM100 (`qm set 100 --balloon 73728`) to hold steady-state RAM around 74 GB while keeping 192 GB maximum available for spikes.
- Implemented staged cascading validation in `shenron_v4_orchestrator.py`: GOKU handles fast-path queries, risk keywords trigger full council escalation and TRUE synthesis.
- Hardened Windows Firewall to expose port 5000 internally (`New-NetFirewallRule -DisplayName "SHENRON Port 5000" ...`).
- Patched the Windows startup script to avoid overwriting read-only `$PID` and confirm the API is listening before returning success.

## Commands Executed
```powershell
# Quantized model downloads (one example – repeat per warrior)
set PYTHONIOENCODING=utf-8
huggingface-cli download bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF --include "*Q8_0.gguf" --local-dir C:\AI-Models-Quantized\GOKU

# Import into LM Studio catalog
y| lms import --copy --user-repo bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF C:\AI-Models-Quantized\GOKU\DeepSeek-Coder-V2-Lite-Instruct-Q8_0.gguf

# Load final warrior set
lms load bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF/DeepSeek-Coder-V2-Lite-Instruct-Q8_0.gguf --identifier Goku-deepseek-coder-v2-lite-instruct --context-length 16384 --yes
lms load bartowski/Llama-3.2-3B-Instruct-GGUF/Llama-3.2-3B-Instruct-Q8_0.gguf --identifier Vegeta-llama-3.2-3b-instruct --context-length 8192 --yes --quiet
lms load bartowski/Qwen2.5-Coder-7B-Instruct-GGUF/Qwen2.5-Coder-7B-Instruct-Q8_0.gguf --identifier Piccolo-qwen2.5-coder-7b-instruct --context-length 16384 --yes --quiet
lms load bartowski/Mistral-7B-Instruct-v0.3-GGUF/Mistral-7B-Instruct-Q8_0.gguf --identifier Gohan-mistral-7b-instruct-v0.3 --context-length 8192 --yes --quiet
lms load QuantFactory/Phi-3-mini-128k-instruct-GGUF/Phi-3-mini-128k-instruct.Q8_0.gguf --identifier Krillin-phi-3-mini-128k-instruct --context-length 32768 --yes --quiet
lms load QuantFactory/Phi-3-mini-128k-instruct-GGUF/Phi-3-mini-128k-instruct.Q8_0.gguf --identifier Frieza-phi-3-mini-128k-instruct --context-length 32768 --yes --quiet

# Proxmox memory guardrails (run on host <PROXMOX_IP>)
qm set 100 --balloon 73728

# Windows firewall opening (run on VM100)
New-NetFirewallRule -DisplayName "SHENRON Port 5000" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5000

# Deploy orchestrator + startup script
scp /home/mgmt1/GitHub/Dell-Server-Roadmap/backend/shenron/shenron_v4_orchestrator.py Administrator@<VM100_IP>:C:/GOKU-AI/shenron/shenron_v4_orchestrator.py
scp /home/mgmt1/GitHub/Dell-Server-Roadmap/backend/shenron/start-shenron-api.ps1 Administrator@<VM100_IP>:C:/GOKU-AI/shenron/start-shenron.ps1
```

## Verification
```shell
# Firewall-open health
curl -s http://<VM100_IP>:5000/health

# Cascading fast-path
action='{"query":"Provide a 2 sentence summary of Proxmox."}'
curl -s -X POST -H "Content-Type: application/json" -d "$action" http://<VM100_IP>:5000/api/shenron/grant-wish | jq '.validation'

# Cascading risk escalation
action='{"query":"Should we delete the production database or reboot the live server?"}'
curl -s -X POST -H "Content-Type: application/json" -d "$action" http://<VM100_IP>:5000/api/shenron/grant-wish | jq '.validation'

# LM Studio residency
lms ps
```
Expected outputs:
- Health endpoint returns `{"status":"operational"...}` from mgmt1.
- First wish shows `"required": false` with only `GOKU` consulted.
- Risk wish lists all six fighters with `"required": true` and recorded trigger reasons.
- `lms ps` reports six Q8 models loaded with contexts (16 GB + 7.7 GB + …) and idle status.

## Known Follow-Ups
- Update the Task Scheduler job on VM100 to call the new `start-shenron.ps1` directly (optional once validated manually).
- Optional: expose `/health` via HTTPS through nginx on VM150 so Cloudflare tunnels no longer proxy the backend port directly.
- Monitor RAM usage (`Get-Process | Measure-Object WorkingSet64 -Sum`) after 24h to confirm ballooning maintains ~74 GB steady-state.
```
