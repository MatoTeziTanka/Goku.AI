<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
#!/bin/bash
# Setup code-server on port 9001 (safe port, not used by reverse proxy)
# This script configures code-server as a systemd service

set -e

PORT=9001

echo "🔌 Setting up code-server on port ${PORT}..."
echo ""

# Check if port is in use
if sudo ss -tlnp | grep -q ":${PORT} "; then
    echo "❌ Port ${PORT} is already in use!"
    echo "   Current usage:"
    sudo ss -tlnp | grep ":${PORT} "
    echo ""
    echo "   Try a different port:"
    echo "   PORT=10000 ./VM101-CODE-SERVER-SETUP-9001.sh"
    exit 1
fi

echo "✅ Port ${PORT} is available"
echo ""

# Create config directory
mkdir -p ~/.config/code-server

# Generate random password
PASSWORD=$(openssl rand -base64 12)

echo "📝 Creating code-server configuration..."
cat > ~/.config/code-server/config.yaml << EOF
bind-addr: 0.0.0.0:${PORT}
auth: password
password: ${PASSWORD}
cert: false
EOF

echo "✅ Configuration created: ~/.config/code-server/config.yaml"
echo ""

# Update firewall
echo "🔥 Updating firewall..."
if sudo ufw status | grep -q "${PORT}/tcp"; then
    echo "   Port ${PORT} already allowed in firewall"
else
    sudo ufw allow ${PORT}/tcp comment "code-server"
    echo "✅ Port ${PORT} added to firewall"
fi
echo ""

# Create systemd service
echo "⚙️  Creating systemd service..."
sudo tee /etc/systemd/system/code-server.service > /dev/null << EOF
[Unit]
Description=Code Server (VS Code in Browser)
After=network.target

[Service]
Type=simple
User=mgmt1
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/code-server --bind-addr 0.0.0.0:${PORT} --auth password
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Systemd service created: /etc/systemd/system/code-server.service"
echo ""

# Enable and start
echo "🚀 Starting code-server service..."
sudo systemctl daemon-reload
sudo systemctl enable code-server
sudo systemctl start code-server

# Wait a moment for service to start
sleep 2

# Check status
echo ""
echo "📊 Service status:"
sudo systemctl status code-server --no-pager -l | head -15

echo ""
echo "=========================================="
echo "✅ Code-server setup complete!"
echo ""
echo "📋 Configuration:"
echo "   Port: ${PORT}"
echo "   Password: ${PASSWORD}"
echo "   Access: http://<VM101_IP>:${PORT}"
echo ""
echo "📝 Next steps:"
echo "   1. Test: curl http://localhost:${PORT}"
echo "   2. Check logs: sudo journalctl -u code-server -f"
echo "   3. Stop service: sudo systemctl stop code-server"
echo "   4. Restart service: sudo systemctl restart code-server"
echo ""
echo "🔐 Security:"
echo "   - Password authentication enabled"
echo "   - Firewall rule added for port ${PORT}"
echo "   - Service auto-starts on boot"
echo ""




