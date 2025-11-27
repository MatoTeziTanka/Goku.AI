<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🚀 BitPhoenix Clean Deployment Instructions

## Prerequisites
- Ubuntu/Debian Linux (or WSL on Windows)
- 4GB RAM minimum, 8GB recommended
- Internet connection for initial setup

## Step 1: Transfer Files
```bash
# On your machine, download the deployment package:
# Visit: http://<VM101_IP>:8080/bitphoenix-deploy.tar.gz
# Save to your home directory

# Verify integrity:
echo "900f9138f8475fb8691bed4dac23e8dd2ec1d1359af15cf3c2273a2c98f65dfb  bitphoenix-deploy.tar.gz" | sha256sum -c
```

## Step 2: Clean Installation
```bash
# Remove any old files (clean slate)
rm -rf ~/bitphoenix* 2>/dev/null || true

# Extract and enter directory
tar -xzf bitphoenix-deploy.tar.gz
cd bitphoenix-deploy

# Run auto-setup (installs all dependencies)
./scripts/auto_setup.sh
```

## Step 3: Start BitPhoenix
```bash
# Start backend (terminal 1)
cd backend && source ../venv/bin/activate
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 &

# Start frontend (terminal 2)
cd frontend && npm start &
```

## Step 4: Verify Running
```bash
# Check processes
ps aux | grep -E "(uvicorn|npm)"

# Test API
curl http://localhost:8000/docs

# Access web interface
# Open browser: http://localhost:3000
```

## Troubleshooting

### If auto-setup fails:
```bash
# Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
cd frontend && npm install
```

### If ports are in use:
```bash
# Kill existing processes
pkill -f uvicorn
pkill -f "npm start"

# Or use different ports
python -m uvicorn src.main:app --host 0.0.0.0 --port 8080 &
cd frontend && PORT=3001 npm start &
```

### If permission errors:
```bash
# Fix permissions
chmod +x scripts/auto_setup.sh
chmod +x scripts/linux/install.sh
```

## Expected Output

After successful startup, you should see:
- Backend: "INFO: Started server process [PID] ..."
- Frontend: "Compiled successfully" and "Local: http://localhost:3000"

## Ready for Testing

Once both services are running:
- **API Documentation:** http://localhost:8000/docs
- **Web Interface:** http://localhost:3000
- **Health Check:** http://localhost:8000/health

BitPhoenix is now ready for manual testing! 🎉</contents>
</xai:function_call">Create comprehensive deployment instructions for clean BitPhoenix installation.

