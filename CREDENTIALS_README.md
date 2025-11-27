# Credentials Management

## 🔒 Secure Credentials File

**File:** `credentials.json`  
**Status:** ⚠️ **GITIGNORED** - Never commit this file!

This file contains all sensitive infrastructure information:
- VM IP addresses
- Usernames and passwords
- API endpoints
- SSH key paths
- Database credentials
- API keys (truncated)

## 📋 Usage

### For Local Development:
```python
import json
from pathlib import Path

credentials_path = Path("credentials.json")
if credentials_path.exists():
    with open(credentials_path) as f:
        creds = json.load(f)
    
    vm100_ip = creds["vm_ips"]["vm100"]["ip"]
    vm100_user = creds["vm_credentials"]["vm100"]["username"]
    vm100_pass = creds["vm_credentials"]["vm100"]["password"]
```

### For Production:
- Use environment variables
- Use secure vault (e.g., HashiCorp Vault, AWS Secrets Manager)
- Never hardcode credentials in code

## 🔄 Template File

**File:** `credentials.template.json`  
**Status:** ✅ Safe to commit

This template file shows the structure without real values. Use it as a reference.

## ⚠️ Security Notes

1. **Never commit `credentials.json`** - It's in `.gitignore`
2. **Rotate passwords** if they're ever exposed
3. **Use SSH keys** instead of passwords when possible
4. **Store backups** in password manager (LastPass, 1Password, etc.)
5. **Restrict file permissions**: `chmod 600 credentials.json`

## 📝 File Structure

```json
{
  "vm_ips": { ... },
  "vm_credentials": { ... },
  "api_endpoints": { ... },
  "database": { ... },
  "api_keys": { ... }
}
```

## 🔐 Access Control

- **Local only**: File exists only on your machine
- **Git ignored**: Never pushed to GitHub
- **Secure storage**: Keep backups in password manager
- **Permissions**: Restrict file access (chmod 600)

---

**Last Updated:** 2025-11-27
