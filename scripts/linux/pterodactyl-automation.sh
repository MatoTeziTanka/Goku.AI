#!/bin/bash
################################################################################
# PTERODACTYL GAME SERVER AUTOMATION SYSTEM
# For LightSpeedUp Hosting - Dell R730 Game Server Business
# VM: 203 (Ubuntu 22.04)
################################################################################

set -euo pipefail

# Configuration
PTERODACTYL_DOMAIN="gameservers.lightspeedup.com"
ADMIN_EMAIL="seth.schultz@lightspeedup.com"
MYSQL_ROOT_PASSWORD=$(openssl rand -base64 32)
PANEL_PASSWORD=$(openssl rand -base64 24)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

################################################################################
# STEP 1: SYSTEM PREPARATION
################################################################################

install_dependencies() {
    log_info "Installing system dependencies..."
    
    # Update system
    apt update && apt upgrade -y
    
    # Install required packages
    apt install -y \
        software-properties-common \
        curl \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release \
        tar \
        unzip \
        git \
        redis-server \
        mariadb-server \
        nginx \
        certbot \
        python3-certbot-nginx \
        php8.1 \
        php8.1-{cli,gd,mysql,pdo,mbstring,tokenizer,bcmath,xml,fpm,curl,zip} \
        composer
    
    log_info "Dependencies installed successfully!"
}

################################################################################
# STEP 2: DOCKER INSTALLATION (for game servers)
################################################################################

install_docker() {
    log_info "Installing Docker..."
    
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Set up Docker repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker Engine
    apt update
    apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Enable Docker service
    systemctl enable docker
    systemctl start docker
    
    log_info "Docker installed successfully!"
}

################################################################################
# STEP 3: DATABASE SETUP
################################################################################

configure_database() {
    log_info "Configuring MariaDB database..."
    
    # Secure MySQL installation
    mysql -e "UPDATE mysql.user SET Password = PASSWORD('${MYSQL_ROOT_PASSWORD}') WHERE User = 'root'"
    mysql -e "DELETE FROM mysql.user WHERE User=''"
    mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1')"
    mysql -e "DROP DATABASE IF EXISTS test"
    mysql -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%'"
    mysql -e "FLUSH PRIVILEGES"
    
    # Create Pterodactyl database
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE DATABASE panel;"
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE USER 'pterodactyl'@'127.0.0.1' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';"
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "GRANT ALL PRIVILEGES ON panel.* TO 'pterodactyl'@'127.0.0.1' WITH GRANT OPTION;"
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "FLUSH PRIVILEGES;"
    
    log_info "Database configured successfully!"
    log_warn "MySQL root password: ${MYSQL_ROOT_PASSWORD}"
    echo "${MYSQL_ROOT_PASSWORD}" > /root/.mysql_root_password
    chmod 600 /root/.mysql_root_password
}

################################################################################
# STEP 4: PTERODACTYL PANEL INSTALLATION
################################################################################

install_pterodactyl_panel() {
    log_info "Installing Pterodactyl Panel..."
    
    # Create directory
    mkdir -p /var/www/pterodactyl
    cd /var/www/pterodactyl
    
    # Download latest release
    curl -Lo panel.tar.gz https://github.com/pterodactyl/panel/releases/latest/download/panel.tar.gz
    tar -xzvf panel.tar.gz
    chmod -R 755 storage/* bootstrap/cache/
    
    # Install dependencies
    composer install --no-dev --optimize-autoloader
    
    # Environment configuration
    php artisan p:environment:setup \
        --author="${ADMIN_EMAIL}" \
        --url="https://${PTERODACTYL_DOMAIN}" \
        --timezone="America/New_York" \
        --cache="redis" \
        --session="redis" \
        --queue="redis" \
        --redis-host="127.0.0.1" \
        --redis-pass="null" \
        --redis-port="6379"
    
    php artisan p:environment:database \
        --host="127.0.0.1" \
        --port="3306" \
        --database="panel" \
        --username="pterodactyl" \
        --password="${MYSQL_ROOT_PASSWORD}"
    
    # Run migrations
    php artisan migrate --seed --force
    
    # Create admin user
    php artisan p:user:make \
        --email="${ADMIN_EMAIL}" \
        --username="admin" \
        --name-first="Seth" \
        --name-last="Schultz" \
        --password="${PANEL_PASSWORD}" \
        --admin=1
    
    # Set permissions
    chown -R www-data:www-data /var/www/pterodactyl/*
    
    # Setup cron
    (crontab -l 2>/dev/null; echo "* * * * * php /var/www/pterodactyl/artisan schedule:run >> /dev/null 2>&1") | crontab -
    
    # Setup queue worker
    cat > /etc/systemd/system/pteroq.service << EOF
[Unit]
Description=Pterodactyl Queue Worker
After=redis-server.service

[Service]
User=www-data
Group=www-data
Restart=always
ExecStart=/usr/bin/php /var/www/pterodactyl/artisan queue:work --queue=high,standard,low --sleep=3 --tries=3
StartLimitInterval=180
StartLimitBurst=30
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

    systemctl enable pteroq.service
    systemctl start pteroq.service
    
    log_info "Pterodactyl Panel installed successfully!"
    log_warn "Admin password: ${PANEL_PASSWORD}"
    echo "${PANEL_PASSWORD}" > /root/.pterodactyl_admin_password
    chmod 600 /root/.pterodactyl_admin_password
}

################################################################################
# STEP 5: NGINX CONFIGURATION
################################################################################

configure_nginx() {
    log_info "Configuring Nginx..."
    
    # Remove default config
    rm -f /etc/nginx/sites-enabled/default
    
    # Create Pterodactyl config
    cat > /etc/nginx/sites-available/pterodactyl.conf << EOF
server {
    listen 80;
    server_name ${PTERODACTYL_DOMAIN};
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ${PTERODACTYL_DOMAIN};

    root /var/www/pterodactyl/public;
    index index.php;

    access_log /var/log/nginx/pterodactyl.app-access.log;
    error_log  /var/log/nginx/pterodactyl.app-error.log error;

    # allow larger file uploads and longer script runtimes
    client_max_body_size 100m;
    client_body_timeout 120s;

    sendfile off;

    # SSL Configuration - certbot will fill this in
    ssl_certificate /etc/letsencrypt/live/${PTERODACTYL_DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${PTERODACTYL_DOMAIN}/privkey.pem;
    ssl_session_cache shared:SSL:10m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384";
    ssl_prefer_server_ciphers on;

    # See https://hstspreload.org/ before uncommenting the line below.
    # add_header Strict-Transport-Security "max-age=15768000; preload;";
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Robots-Tag none;
    add_header Content-Security-Policy "frame-ancestors 'self'";
    add_header X-Frame-Options DENY;
    add_header Referrer-Policy same-origin;

    location / {
        try_files \$uri \$uri/ /index.php?\$query_string;
    }

    location ~ \.php$ {
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass unix:/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param PHP_VALUE "upload_max_filesize = 100M \n post_max_size=100M";
        fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name;
        fastcgi_param HTTP_PROXY "";
        fastcgi_intercept_errors off;
        fastcgi_buffer_size 16k;
        fastcgi_buffers 4 16k;
        fastcgi_connect_timeout 300;
        fastcgi_send_timeout 300;
        fastcgi_read_timeout 300;
        include /etc/nginx/fastcgi_params;
    }

    location ~ /\.ht {
        deny all;
    }
}
EOF

    ln -s /etc/nginx/sites-available/pterodactyl.conf /etc/nginx/sites-enabled/pterodactyl.conf
    
    # Test and reload Nginx
    nginx -t
    systemctl restart nginx
    
    log_info "Nginx configured successfully!"
}

################################################################################
# STEP 6: SSL CERTIFICATE (LET'S ENCRYPT)
################################################################################

install_ssl() {
    log_info "Installing SSL certificate..."
    
    # Stop nginx temporarily
    systemctl stop nginx
    
    # Obtain certificate
    certbot certonly --standalone --agree-tos --no-eff-email --email "${ADMIN_EMAIL}" -d "${PTERODACTYL_DOMAIN}"
    
    # Auto-renewal cron
    (crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --post-hook \"systemctl reload nginx\" >> /var/log/certbot-renew.log 2>&1") | crontab -
    
    # Start nginx
    systemctl start nginx
    
    log_info "SSL certificate installed successfully!"
}

################################################################################
# STEP 7: PTERODACTYL WINGS (Game Server Daemon)
################################################################################

install_pterodactyl_wings() {
    log_info "Installing Pterodactyl Wings..."
    
    # Create directory
    mkdir -p /etc/pterodactyl
    cd /etc/pterodactyl
    
    # Download Wings
    curl -L -o /usr/local/bin/wings "https://github.com/pterodactyl/wings/releases/latest/download/wings_linux_$([[ "$(uname -m)" == "x86_64" ]] && echo "amd64" || echo "arm64")"
    chmod u+x /usr/local/bin/wings
    
    # Systemd service
    cat > /etc/systemd/system/wings.service << EOF
[Unit]
Description=Pterodactyl Wings Daemon
After=docker.service
Requires=docker.service
PartOf=docker.service

[Service]
User=root
WorkingDirectory=/etc/pterodactyl
LimitNOFILE=4096
PIDFile=/var/run/wings/daemon.pid
ExecStart=/usr/local/bin/wings
Restart=on-failure
StartLimitInterval=180
StartLimitBurst=30
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

    systemctl enable wings
    
    log_info "Wings installed! Manual configuration needed in panel."
    log_warn "1. Log in to panel at https://${PTERODACTYL_DOMAIN}"
    log_warn "2. Go to Admin Panel → Locations → Create new location"
    log_warn "3. Go to Admin Panel → Nodes → Create new node"
    log_warn "4. Copy the configuration to /etc/pterodactyl/config.yml"
    log_warn "5. Run: systemctl start wings"
}

################################################################################
# STEP 8: GAME SERVER TEMPLATES (Pre-configured Eggs)
################################################################################

download_game_eggs() {
    log_info "Downloading game server templates (Eggs)..."
    
    mkdir -p /var/www/pterodactyl/storage/eggs
    cd /var/www/pterodactyl/storage/eggs
    
    # Minecraft (multiple versions)
    curl -sL https://raw.githubusercontent.com/parkervcp/eggs/master/game_eggs/minecraft/java/egg-vanilla-minecraft.json -o minecraft-vanilla.json
    curl -sL https://raw.githubusercontent.com/parkervcp/eggs/master/game_eggs/minecraft/java/egg-forge-minecraft.json -o minecraft-forge.json
    curl -sL https://raw.githubusercontent.com/parkervcp/eggs/master/game_eggs/minecraft/java/egg-paper.json -o minecraft-paper.json
    
    # Valheim
    curl -sL https://raw.githubusercontent.com/parkervcp/eggs/master/game_eggs/valheim/egg-valheim.json -o valheim.json
    
    # ARK: Survival Evolved
    curl -sL https://raw.githubusercontent.com/parkervcp/eggs/master/game_eggs/steamcmd_servers/ark_survival_evolved/egg-ark--survival-evolved.json -o ark.json
    
    # Rust
    curl -sL https://raw.githubusercontent.com/parkervcp/eggs/master/game_eggs/steamcmd_servers/rust/egg-rust.json -o rust.json
    
    # Terraria
    curl -sL https://raw.githubusercontent.com/parkervcp/eggs/master/game_eggs/terraria/egg-terraria-vanilla.json -o terraria.json
    
    # 7 Days to Die
    curl -sL https://raw.githubusercontent.com/parkervcp/eggs/master/game_eggs/steamcmd_servers/7_days_to_die/egg-7-days-to-die.json -o 7days.json
    
    # Project Zomboid
    curl -sL https://raw.githubusercontent.com/parkervcp/eggs/master/game_eggs/steamcmd_servers/project_zomboid/egg-project-zomboid.json -o zomboid.json
    
    log_info "Game eggs downloaded! Import them via Admin Panel → Nests → Import Egg"
}

################################################################################
# STEP 9: AUTOMATION SCRIPTS
################################################################################

create_automation_scripts() {
    log_info "Creating automation scripts..."
    
    mkdir -p /opt/pterodactyl-automation
    cd /opt/pterodactyl-automation
    
    # Script 1: Auto-deploy server on payment
    cat > deploy_server.sh << 'SCRIPT1'
#!/bin/bash
# Called by Shenron when customer payment is received
# Usage: ./deploy_server.sh <customer_email> <game_type> <plan_name>

CUSTOMER_EMAIL=$1
GAME_TYPE=$2  # minecraft, valheim, ark, rust, etc.
PLAN=$3       # starter, standard, pro, enterprise

# Pterodactyl API credentials
PANEL_URL="https://gameservers.lightspeedup.com"
API_KEY="YOUR_API_KEY_HERE"  # Generate in panel: Account → API Credentials

# Plan resources
case $PLAN in
    starter)
        RAM=2048
        CPU=200  # 2 cores (100 = 1 core)
        DISK=10240  # MB
        ;;
    standard)
        RAM=4096
        CPU=400
        DISK=25600
        ;;
    pro)
        RAM=8192
        CPU=600
        DISK=51200
        ;;
    enterprise)
        RAM=16384
        CPU=800
        DISK=102400
        ;;
esac

# Egg IDs (get from panel after importing eggs)
case $GAME_TYPE in
    minecraft) EGG_ID=1 ;;
    valheim) EGG_ID=5 ;;
    ark) EGG_ID=6 ;;
    rust) EGG_ID=7 ;;
    terraria) EGG_ID=8 ;;
    7days) EGG_ID=9 ;;
    zomboid) EGG_ID=10 ;;
esac

# Generate server name
SERVER_NAME="${CUSTOMER_EMAIL%%@*}-${GAME_TYPE}-$(date +%s)"

# API call to create server
curl -X POST "${PANEL_URL}/api/application/servers" \
    -H "Authorization: Bearer ${API_KEY}" \
    -H "Content-Type: application/json" \
    -H "Accept: Application/vnd.pterodactyl.v1+json" \
    -d '{
        "name": "'"${SERVER_NAME}"'",
        "user": 1,
        "egg": '"${EGG_ID}"',
        "docker_image": "ghcr.io/pterodactyl/yolks:java_17",
        "startup": "java -Xms128M -Xmx{{SERVER_MEMORY}}M -jar {{SERVER_JARFILE}}",
        "environment": {},
        "limits": {
            "memory": '"${RAM}"',
            "swap": 0,
            "disk": '"${DISK}"',
            "io": 500,
            "cpu": '"${CPU}"'
        },
        "feature_limits": {
            "databases": 1,
            "backups": 3
        },
        "allocation": {
            "default": 1
        }
    }'

echo "Server deployed: ${SERVER_NAME}"
SCRIPT1

    chmod +x deploy_server.sh
    
    # Script 2: Auto-backup all servers
    cat > backup_all_servers.sh << 'SCRIPT2'
#!/bin/bash
# Backup all game servers (daily cron)

BACKUP_DIR="/mnt/backups/game-servers"
mkdir -p ${BACKUP_DIR}

# Get all server UUIDs
SERVERS=$(docker ps --format "{{.ID}}" --filter "name=ptero")

for SERVER in ${SERVERS}; do
    SERVER_NAME=$(docker inspect --format='{{.Name}}' ${SERVER} | sed 's/\///')
    BACKUP_FILE="${BACKUP_DIR}/${SERVER_NAME}_$(date +%Y%m%d_%H%M%S).tar.gz"
    
    # Backup server data
    docker exec ${SERVER} tar czf /tmp/backup.tar.gz /home/container
    docker cp ${SERVER}:/tmp/backup.tar.gz ${BACKUP_FILE}
    docker exec ${SERVER} rm /tmp/backup.tar.gz
    
    echo "Backed up: ${SERVER_NAME}"
done

# Keep only last 30 days
find ${BACKUP_DIR} -name "*.tar.gz" -mtime +30 -delete

echo "Backup complete!"
SCRIPT2

    chmod +x backup_all_servers.sh
    
    # Add to cron
    (crontab -l 2>/dev/null; echo "0 2 * * * /opt/pterodactyl-automation/backup_all_servers.sh >> /var/log/pterodactyl-backups.log 2>&1") | crontab -
    
    log_info "Automation scripts created!"
}

################################################################################
# MAIN EXECUTION
################################################################################

main() {
    log_info "Starting Pterodactyl installation..."
    
    install_dependencies
    install_docker
    configure_database
    install_pterodactyl_panel
    configure_nginx
    install_ssl
    install_pterodactyl_wings
    download_game_eggs
    create_automation_scripts
    
    log_info "=================================="
    log_info "INSTALLATION COMPLETE!"
    log_info "=================================="
    log_info "Panel URL: https://${PTERODACTYL_DOMAIN}"
    log_info "Admin email: ${ADMIN_EMAIL}"
    log_info "Admin password: ${PANEL_PASSWORD}"
    log_info ""
    log_warn "NEXT STEPS:"
    log_warn "1. Log in to the panel"
    log_warn "2. Create a location (Admin → Locations)"
    log_warn "3. Create a node (Admin → Nodes)"
    log_warn "4. Copy node configuration to /etc/pterodactyl/config.yml"
    log_warn "5. Import game eggs (Admin → Nests → Import Egg)"
    log_warn "6. Start Wings: systemctl start wings"
    log_warn ""
    log_info "Credentials saved to:"
    log_info "- MySQL: /root/.mysql_root_password"
    log_info "- Panel: /root/.pterodactyl_admin_password"
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi

