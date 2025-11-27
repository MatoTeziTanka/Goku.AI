<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Cleanup After Uninstalling Multi-Agent Extension

The `multiagent.multiagent-ai-system` extension might have left behind settings that are causing issues.

## Step 1: Check for Leftover Settings

### Check User Settings
1. Press `Ctrl+Shift+P`
2. Type: `Preferences: Open User Settings (JSON)`
3. Look for any settings starting with:
   - `multiagent.`
   - `bitphoenix.`

### Check Workspace Settings
Your `.vscode/settings.json` should be clean (I don't see any multiagent settings in it).

## Step 2: Remove Leftover Settings

If you find any `multiagent.*` or `bitphoenix.*` settings in your user settings.json, remove them:

**Before:**
```json
{
  "multiagent.backendUrl": "http://localhost:8000",
  "multiagent.autoStart": true,
  "bitphoenix.backendUrl": "http://<VM101_IP>:8000"
}
```

**After:** (remove those lines)

## Step 3: Clear Extension Cache

The extension might have left cache files:

1. Close Cursor completely
2. Check these locations:
   - `%APPDATA%\Cursor\User\workspaceStorage\`
   - `%LOCALAPPDATA%\Cursor\CachedExtensions\`
   - `%APPDATA%\Cursor\logs\`

3. Look for folders/files related to:
   - `multiagent`
   - `multi-agent`
   - `bitphoenix`

## Step 4: Reset Terminal Settings

Since the extension is gone, let's make sure terminal settings are clean:

Your current `.vscode/settings.json` looks good - it doesn't have any multiagent settings.

## Step 5: Reload Cursor

1. Press `Ctrl+Shift+P`
2. Type: `Developer: Reload Window`
3. Or: `Developer: Restart Extension Host`

## Step 6: Test Terminal

1. Press `` Ctrl+` `` to open terminal
2. Should open without errors
3. If it still crashes, see next steps

## If Terminal Still Broken

The extension uninstall might have corrupted something. Try:

### Option A: Reset User Settings
1. `Ctrl+Shift+P` → `Preferences: Open User Settings (JSON)`
2. Remove any `multiagent.*` or `bitphoenix.*` settings
3. Save and reload

### Option B: Clear Workspace Storage
1. Close Cursor
2. Delete: `%APPDATA%\Cursor\User\workspaceStorage\*`
3. Restart Cursor

### Option C: Reinstall Extension (if you want it back)
If you want the extension back:
1. The extension code is in: `unknown/multi-agent-system/cursor-extension/`
2. You can rebuild and reinstall it
3. Or find it in the extension marketplace

## Quick Check Script

Run this to find leftover settings:

```powershell
# Check user settings
$userSettings = "$env:APPDATA\Cursor\User\settings.json"
if (Test-Path $userSettings) {
    $content = Get-Content $userSettings -Raw
    if ($content -match "multiagent|bitphoenix") {
        Write-Host "Found leftover settings!" -ForegroundColor Red
        Write-Host "Remove these from your settings.json"
    } else {
        Write-Host "No leftover settings found" -ForegroundColor Green
    }
}
```


