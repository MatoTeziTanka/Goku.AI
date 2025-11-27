<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# VM 101 Final Setup Steps

This guide covers the remaining steps to complete VM 101 setup so you can move Cursor AI from your personal PC.

## Current Status

✅ VM 101 created and configured
✅ SSH keys set up (VM 180 skipped - will rebuild later)
✅ code-server running
✅ Python environment set up
✅ Docker installed
✅ Management scripts created

## Remaining Tasks

### 1. Sync GitHub Repositories

**Option A: Run the sync script on VM 101**

1. Copy the sync script to VM 101:
   ```bash
   # From your local PC, copy the script
   scp Dell-Server-Roadmap/scripts/sync-all-repos-to-vm101.sh mgmt1@<VM101_IP>:~/sync-all-repos-to-vm101.sh
   ```

2. On VM 101, make it executable and run:
   ```bash
   chmod +x ~/sync-all-repos-to-vm101.sh
   ~/sync-all-repos-to-vm101.sh
   ```

**Option B: Manual clone (if SSH keys to GitHub aren't set up yet)**

On VM 101:
```bash
cd ~
mkdir -p GitHub
cd GitHub

# Clone repositories (you'll need to authenticate)
git clone https://github.com/sethpizzaboy/ScalpStorm.git
git clone https://github.com/sethpizzaboy/FamilyFork.git
git clone https://github.com/sethpizzaboy/Games-with-Logan.git
git clone https://github.com/sethpizzaboy/CursorAI.git
git clone https://github.com/MatoTeziTanka/Dell-Server-Roadmap.git
# ... add other repos as needed
```

### 2. Transfer Chat History

The chat history from Cursor is stored in:
- **Windows**: `%APPDATA%\Cursor\User\workspaceStorage\` and `%APPDATA%\Cursor\retrieval\`
- Or in the `CursorAI/transfer_data/Cursor_Chat/` folder if you've already exported it

**To transfer:**

1. If you have chat history in `CursorAI/transfer_data/Cursor_Chat/`:
   ```bash
   # From your PC, copy the chat history
   scp -r CursorAI/transfer_data/Cursor_Chat mgmt1@<VM101_IP>:~/CursorAI/transfer_data/
   ```

2. Or manually copy the files from your Windows PC to VM 101 using your preferred method.

### 3. Install Cursor on VM 101

**Note**: Cursor is primarily a desktop application. For VM 101 (Linux server), you have a few options:

**Option A: Use code-server (Already Set Up!)**
- ✅ Already installed and running on port 8080
- Access via SSH tunnel or Cloudflare Tunnel with Access policy
- This is actually better for server environments

**Option B: Install Cursor Desktop (if you need GUI)**
- Cursor doesn't have a native Linux server version
- You'd need X11 forwarding or a desktop environment
- Not recommended for headless server

**Recommended**: Use code-server! It's already set up and works great for remote development.

### 4. Configure code-server Access

You have two options:

**Option A: SSH Tunnel (Recommended)**
```bash
# From your local PC or laptop
ssh -L 8080:localhost:8080 mgmt1@<VM101_IP>

# Then access: http://localhost:8080
```

**Option B: Cloudflare Tunnel (For remote access)**
1. Add VM 101 to Cloudflare Tunnel configuration
2. Set up Access policy for security
3. Access via domain name

### 5. Final Testing

Test all functionality:

```bash
# On VM 101, test everything:
vm-check          # Check VM 101 status
vm-status         # Check all VMs
vm-ssh 120        # SSH to reverse proxy
vm-ssh 150        # SSH to WordPress

# Test git operations
cd ~/GitHub/Dell-Server-Roadmap
git status
git pull

# Test Python environment
ai-env            # Activate environment
python --version

# Test Docker
docker ps

# Test code-server access
curl http://localhost:8080  # Should return HTML
```

### 6. Update VM 101 Script

After testing, update the setup script if needed:
```bash
cd ~/GitHub/Dell-Server-Roadmap
git status
git add scripts/sync-all-repos-to-vm101.sh
git commit -m "Add repo sync script for VM 101"
git push
```

## Quick Reference

**VM 101 Access:**
- **SSH**: `ssh mgmt1@<VM101_IP>`
- **code-server**: `http://<VM101_IP>:8080` (via SSH tunnel or Cloudflare)
- **Home directory**: `~/`
- **GitHub repos**: `~/GitHub/`

**Useful Aliases (already set up):**
- `ai-env` - Activate Python environment
- `vm-status` - Check all VMs
- `vm-ssh <number>` - SSH to specific VM
- `vm-check` - Check VM 101 status

## Next Steps After VM 101 is Complete

1. ✅ Move Cursor AI instance to VM 101
2. ✅ Access everything remotely via code-server
3. ✅ Continue WordPress business setup
4. 🔄 Rebuild VM 180 when ready

## Troubleshooting

**If repos fail to clone:**
- Check GitHub SSH key is added: `cat ~/.ssh/id_ed25519.pub`
- Or use HTTPS and authenticate manually
- Check network connectivity: `ping github.com`

**If code-server doesn't work:**
- Check it's running: `ps aux | grep code-server`
- Check port: `netstat -tlnp | grep 8080`
- Restart: `systemctl --user restart code-server` (if using systemd)
- Or restart manually: `killall code-server && code-server &`

**If SSH to other VMs fails:**
- Check key is in target VM's `authorized_keys`
- Test from VM 101: `ssh -v user@192.168.12.XXX`

