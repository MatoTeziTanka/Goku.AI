# Azure Review and Reorganization Process

## Overview

This script uses Azure GPT-4.1 API to:
1. Review and improve uninstall scripts
2. Move files from "Doesnt Belong" to correct repositories
3. Clean up BitPhoenix files (move irrelevant to EOL)
4. Review and delete EOL files

## Current Status

**Script is running:** `azure_review_and_reorganize.py`

This process may take **30-60 minutes** due to:
- Multiple Azure API calls for file analysis
- Rate limiting between API calls
- File movement operations

## What's Happening

### Phase 1: Review Uninstall Scripts ✅
- Reviewing `scripts/windows/uninstall-bitphoenix.ps1`
- Reviewing `scripts/linux/uninstall.sh`
- Reviewing `scripts/windows/uninstall-wsl.sh`
- Reviewing `UNINSTALL.md`
- Azure will check for improvements and update files if needed

### Phase 2: Move Files from "Doesnt Belong" 🔄
Files detected in "Doesnt Belong":
- `shenron-ultra-instinct/` → **Goku.AI** (Shenron/DragonBall Z related)
- `shenron-env/` → **Goku.AI** (Shenron virtual environment)
- `Marketing-Automation/` → To be determined by Azure
- `documentation/dinocloud/` → **DinoCloud** repo
- `venv/` → May be deleted (virtual environment)

Azure will analyze each file and determine the correct destination.

### Phase 3: Clean BitPhoenix Files 🔄
- Scanning all files in BitPhoenix
- Identifying files irrelevant to v1.0.0
- Moving old/legacy files to EOL folder

### Phase 4: Review and Delete EOL Files 🔄
- Reviewing all files in EOL folder
- Confirming they are truly End of Life
- Deleting all EOL files (keeping the folder)

## Expected Results

After completion:
- ✅ Uninstall scripts reviewed and improved
- ✅ "Doesnt Belong" folder deleted (after files moved)
- ✅ BitPhoenix cleaned (irrelevant files in EOL)
- ✅ EOL folder empty (but folder kept)

## Monitoring Progress

Check the console output for:
- `📝 Reviewing:` - File being reviewed
- `✅ Moved to:` - File successfully moved
- `📦 Moved to EOL:` - File moved to EOL
- `🗑️ Deleting:` - EOL files being deleted

## Files Being Processed

### "Doesnt Belong" Folder Contents:
- `shenron-ultra-instinct/phase1/` (2 Python files)
- `shenron-env/` (Python virtual environment)
- `Marketing-Automation/` (Many marketing files)
- `documentation/dinocloud/` (DinoCloud docs)
- `venv/` (Python virtual environment)

### Expected Destinations:
- **Goku.AI**: `shenron-ultra-instinct/`, `shenron-env/`
- **DinoCloud**: `documentation/dinocloud/`
- **Marketing Repo** (if exists): `Marketing-Automation/`
- **Delete**: `venv/` (virtual environments typically not committed)

## Troubleshooting

If the script stops or errors:
1. Check Azure API rate limits
2. Verify file permissions
3. Check disk space
4. Review error messages in console

## Next Steps After Completion

1. Review moved files in their new locations
2. Verify "Doesnt Belong" folder is deleted
3. Check EOL folder is empty
4. Review improved uninstall scripts
5. Test uninstall scripts if needed

---

**Started:** Running in background  
**Estimated Time:** 30-60 minutes  
**Status:** In Progress





