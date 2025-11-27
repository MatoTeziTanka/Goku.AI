#!/bin/bash
################################################################################
# WORDPRESS MULTI-TENANT HOSTING AUTOMATION
# For LightSpeedUp Hosting - VM150 (Ubuntu 22.04)
# Automated WordPress site creation, management, and billing
################################################################################

set -euo pipefail

# Configuration
ADMIN_EMAIL="seth.schultz@lightspeedup.com"
MYSQL_ROOT_PASSWORD=$(cat /root/.mysql_root_password 2>/dev/null || openssl rand -base64 32)
WEB_ROOT="/var/www"
BACKUP_ROOT="/mnt/backups/wordpress"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

################################################################################
# FUNCTION: Create new WordPress site (called by Shenron on payment)
################################################################################

create_wordpress_site() {
    local DOMAIN=$1
    local PLAN=$2  # basic, managed, business, enterprise
    local CLIENT_NAME=$3
    local CLIENT_EMAIL=$4
    
    log_info "Creating WordPress site: ${DOMAIN} (Plan: ${PLAN})"
    
    # Generate secure passwords
    local DB_PASS=$(openssl rand -base64 32)
    local WP_ADMIN_PASS=$(openssl rand -base64 16)
    local DB_NAME="wp_$(echo ${DOMAIN} | tr '.' '_' | tr '-' '_')"
    local DB_USER="${DB_NAME}_user"
    
    # Create database
    log_info "Creating database: ${DB_NAME}"
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE DATABASE ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';"
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';"
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "FLUSH PRIVILEGES;"
    
    # Create directory
    mkdir -p ${WEB_ROOT}/${DOMAIN}
    cd ${WEB_ROOT}/${DOMAIN}
    
    # Download WordPress
    log_info "Downloading WordPress..."
    wp core download --allow-root
    
    # Create wp-config.php
    wp config create \
        --dbname="${DB_NAME}" \
        --dbuser="${DB_USER}" \
        --dbpass="${DB_PASS}" \
        --dbhost="localhost" \
        --allow-root
    
    # Install WordPress
    log_info "Installing WordPress..."
    wp core install \
        --url="https://${DOMAIN}" \
        --title="${CLIENT_NAME} Website" \
        --admin_user="admin" \
        --admin_password="${WP_ADMIN_PASS}" \
        --admin_email="${CLIENT_EMAIL}" \
        --allow-root
    
    # Install essential plugins based on plan
    log_info "Installing plugins for ${PLAN} plan..."
    
    # Basic plugins (all plans)
    wp plugin install wordfence --activate --allow-root  # Security
    wp plugin install updraftplus --allow-root  # Backups
    wp plugin install wp-super-cache --activate --allow-root  # Caching
    wp plugin install contact-form-7 --activate --allow-root  # Contact forms
    
    # Managed plan and above
    if [[ "${PLAN}" != "basic" ]]; then
        wp plugin install google-analytics-for-wordpress --activate --allow-root
        wp plugin install yoast-seo --allow-root  # SEO (basic setup)
    fi
    
    # Business plan and above
    if [[ "${PLAN}" == "business" || "${PLAN}" == "enterprise" ]]; then
        wp plugin install woocommerce --allow-root  # E-commerce ready
        wp plugin install mailchimp-for-wp --allow-root  # Email marketing
    fi
    
    # Configure UpdraftPlus backup
    wp option update updraft_interval 1 --allow-root  # Daily backups
    wp option update updraft_retain 30 --allow-root  # Keep 30 days
    
    # Configure Wordfence
    wp option update wordfence_serverIP "auto" --allow-root
    
    # Set permissions
    chown -R www-data:www-data ${WEB_ROOT}/${DOMAIN}
    find ${WEB_ROOT}/${DOMAIN} -type d -exec chmod 755 {} \;
    find ${WEB_ROOT}/${DOMAIN} -type f -exec chmod 644 {} \;
    
    # Create Nginx config
    log_info "Creating Nginx configuration..."
    cat > /etc/nginx/sites-available/${DOMAIN}.conf << EOF
server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ${DOMAIN} www.${DOMAIN};
    
    root ${WEB_ROOT}/${DOMAIN};
    index index.php index.html index.htm;
    
    access_log /var/log/nginx/${DOMAIN}-access.log;
    error_log /var/log/nginx/${DOMAIN}-error.log;
    
    # SSL Configuration (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;
    ssl_session_cache shared:SSL:10m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # WordPress permalinks
    location / {
        try_files \$uri \$uri/ /index.php?\$args;
    }
    
    # PHP processing
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name;
        include fastcgi_params;
    }
    
    # Deny access to sensitive files
    location ~ /\.ht {
        deny all;
    }
    
    location = /xmlrpc.php {
        deny all;
    }
    
    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

    ln -sf /etc/nginx/sites-available/${DOMAIN}.conf /etc/nginx/sites-enabled/${DOMAIN}.conf
    
    # Obtain SSL certificate
    log_info "Obtaining SSL certificate..."
    certbot certonly --webroot -w ${WEB_ROOT}/${DOMAIN} -d ${DOMAIN} -d www.${DOMAIN} \
        --email ${ADMIN_EMAIL} --agree-tos --non-interactive || log_warn "SSL cert failed (may need DNS)"
    
    # Test Nginx config and reload
    nginx -t && systemctl reload nginx
    
    # Save credentials to file
    local CRED_FILE="/root/wordpress-credentials/${DOMAIN}.txt"
    mkdir -p /root/wordpress-credentials
    cat > ${CRED_FILE} << CREDS
WordPress Site Created: ${DOMAIN}
==================================
Client: ${CLIENT_NAME}
Email: ${CLIENT_EMAIL}
Plan: ${PLAN}
Created: $(date)

LOGIN CREDENTIALS:
==================
URL: https://${DOMAIN}/wp-admin
Username: admin
Password: ${WP_ADMIN_PASS}

DATABASE CREDENTIALS:
=====================
Database: ${DB_NAME}
User: ${DB_USER}
Password: ${DB_PASS}
Host: localhost

CREDS

    chmod 600 ${CRED_FILE}
    
    log_info "Site created successfully: https://${DOMAIN}"
    log_info "Credentials saved to: ${CRED_FILE}"
    
    # Return credentials (Shenron will email customer)
    echo "URL=https://${DOMAIN}/wp-admin|USERNAME=admin|PASSWORD=${WP_ADMIN_PASS}"
}

################################################################################
# FUNCTION: Update WordPress sites (weekly maintenance)
################################################################################

update_wordpress_sites() {
    log_info "Running WordPress updates for all sites..."
    
    for SITE_DIR in ${WEB_ROOT}/*/; do
        if [[ -f "${SITE_DIR}/wp-config.php" ]]; then
            local DOMAIN=$(basename ${SITE_DIR})
            log_info "Updating: ${DOMAIN}"
            
            cd ${SITE_DIR}
            
            # Backup before updating
            wp db export /tmp/${DOMAIN}_pre_update_$(date +%Y%m%d).sql --allow-root
            
            # Update WordPress core
            wp core update --allow-root || log_warn "${DOMAIN}: Core update failed"
            wp core update-db --allow-root || log_warn "${DOMAIN}: DB update failed"
            
            # Update plugins
            wp plugin update --all --allow-root || log_warn "${DOMAIN}: Plugin update failed"
            
            # Update themes
            wp theme update --all --allow-root || log_warn "${DOMAIN}: Theme update failed"
            
            # Clear cache
            wp cache flush --allow-root 2>/dev/null || true
            
            log_info "${DOMAIN}: Update complete!"
        fi
    done
    
    log_info "All sites updated!"
}

################################################################################
# FUNCTION: Backup all WordPress sites
################################################################################

backup_wordpress_sites() {
    log_info "Backing up all WordPress sites..."
    
    mkdir -p ${BACKUP_ROOT}
    local BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
    
    for SITE_DIR in ${WEB_ROOT}/*/; do
        if [[ -f "${SITE_DIR}/wp-config.php" ]]; then
            local DOMAIN=$(basename ${SITE_DIR})
            local BACKUP_DIR="${BACKUP_ROOT}/${DOMAIN}/${BACKUP_DATE}"
            mkdir -p ${BACKUP_DIR}
            
            log_info "Backing up: ${DOMAIN}"
            
            # Backup database
            cd ${SITE_DIR}
            wp db export ${BACKUP_DIR}/${DOMAIN}.sql --allow-root
            
            # Backup files (exclude cache and temp files)
            tar czf ${BACKUP_DIR}/${DOMAIN}_files.tar.gz \
                --exclude='wp-content/cache' \
                --exclude='wp-content/uploads/cache' \
                --exclude='*.log' \
                -C ${WEB_ROOT} ${DOMAIN}
            
            log_info "${DOMAIN}: Backup complete (${BACKUP_DIR})"
        fi
    done
    
    # Delete backups older than 30 days
    find ${BACKUP_ROOT} -type d -mtime +30 -exec rm -rf {} + 2>/dev/null || true
    
    log_info "All backups complete!"
}

################################################################################
# FUNCTION: Delete WordPress site (on cancellation)
################################################################################

delete_wordpress_site() {
    local DOMAIN=$1
    
    log_warn "Deleting WordPress site: ${DOMAIN}"
    
    # Final backup before deletion
    backup_wordpress_sites
    
    # Remove database
    local DB_NAME="wp_$(echo ${DOMAIN} | tr '.' '_' | tr '-' '_')"
    local DB_USER="${DB_NAME}_user"
    
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "DROP DATABASE IF EXISTS ${DB_NAME};" || true
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "DROP USER IF EXISTS '${DB_USER}'@'localhost';" || true
    
    # Remove files
    rm -rf ${WEB_ROOT}/${DOMAIN}
    
    # Remove Nginx config
    rm -f /etc/nginx/sites-enabled/${DOMAIN}.conf
    rm -f /etc/nginx/sites-available/${DOMAIN}.conf
    nginx -t && systemctl reload nginx
    
    # Remove SSL certificate
    certbot delete --cert-name ${DOMAIN} --non-interactive || true
    
    log_info "${DOMAIN} deleted successfully"
}

################################################################################
# FUNCTION: Generate income report
################################################################################

generate_income_report() {
    log_info "Generating WordPress hosting income report..."
    
    local TOTAL_SITES=0
    local BASIC=0
    local MANAGED=0
    local BUSINESS=0
    local ENTERPRISE=0
    
    # Count sites by plan (stored in custom field)
    for SITE_DIR in ${WEB_ROOT}/*/; do
        if [[ -f "${SITE_DIR}/wp-config.php" ]]; then
            TOTAL_SITES=$((TOTAL_SITES + 1))
            
            # Read plan from metadata file
            local DOMAIN=$(basename ${SITE_DIR})
            if [[ -f "/root/wordpress-credentials/${DOMAIN}.txt" ]]; then
                local PLAN=$(grep "^Plan:" /root/wordpress-credentials/${DOMAIN}.txt | cut -d' ' -f2)
                case $PLAN in
                    basic) BASIC=$((BASIC + 1)) ;;
                    managed) MANAGED=$((MANAGED + 1)) ;;
                    business) BUSINESS=$((BUSINESS + 1)) ;;
                    enterprise) ENTERPRISE=$((ENTERPRISE + 1)) ;;
                esac
            fi
        fi
    done
    
    # Calculate revenue
    local BASIC_REV=$((BASIC * 25))
    local MANAGED_REV=$((MANAGED * 50))
    local BUSINESS_REV=$((BUSINESS * 100))
    local ENTERPRISE_REV=$((ENTERPRISE * 200))
    local TOTAL_REV=$((BASIC_REV + MANAGED_REV + BUSINESS_REV + ENTERPRISE_REV))
    
    # Generate report
    cat > /tmp/wordpress_income_report_$(date +%Y%m%d).txt << REPORT
WORDPRESS HOSTING INCOME REPORT
================================
Generated: $(date)

ACTIVE SITES: ${TOTAL_SITES}
=========================
Basic ($25/mo):      ${BASIC} sites = \$${BASIC_REV}
Managed ($50/mo):    ${MANAGED} sites = \$${MANAGED_REV}
Business ($100/mo):  ${BUSINESS} sites = \$${BUSINESS_REV}
Enterprise ($200/mo): ${ENTERPRISE} sites = \$${ENTERPRISE_REV}

TOTAL MONTHLY REVENUE: \$${TOTAL_REV}
====================================

REPORT

    cat /tmp/wordpress_income_report_$(date +%Y%m%d).txt
    log_info "Report saved to: /tmp/wordpress_income_report_$(date +%Y%m%d).txt"
}

################################################################################
# FUNCTION: Health check all sites
################################################################################

health_check_sites() {
    log_info "Running health checks on all WordPress sites..."
    
    for SITE_DIR in ${WEB_ROOT}/*/; do
        if [[ -f "${SITE_DIR}/wp-config.php" ]]; then
            local DOMAIN=$(basename ${SITE_DIR})
            
            # Check if site is accessible
            local HTTP_CODE=$(curl -sL -w "%{http_code}" "https://${DOMAIN}" -o /dev/null || echo "000")
            
            if [[ "${HTTP_CODE}" == "200" ]]; then
                echo -e "${GREEN}✓${NC} ${DOMAIN}: Online (HTTP ${HTTP_CODE})"
            else
                echo -e "${RED}✗${NC} ${DOMAIN}: OFFLINE (HTTP ${HTTP_CODE})"
                # Alert Shenron
                echo "ALERT: ${DOMAIN} is offline (HTTP ${HTTP_CODE})" >> /tmp/shenron_alerts.log
            fi
            
            # Check database connection
            cd ${SITE_DIR}
            if wp db check --allow-root >/dev/null 2>&1; then
                echo -e "${GREEN}  ✓${NC} Database: OK"
            else
                echo -e "${RED}  ✗${NC} Database: ERROR"
                echo "ALERT: ${DOMAIN} database connection failed" >> /tmp/shenron_alerts.log
            fi
            
            # Check disk space
            local DISK_USAGE=$(du -sm ${SITE_DIR} | cut -f1)
            echo "  📊 Disk usage: ${DISK_USAGE} MB"
        fi
    done
    
    log_info "Health check complete!"
}

################################################################################
# MAIN CLI
################################################################################

case "${1:-help}" in
    create)
        create_wordpress_site "$2" "$3" "$4" "$5"
        ;;
    update)
        update_wordpress_sites
        ;;
    backup)
        backup_wordpress_sites
        ;;
    delete)
        delete_wordpress_site "$2"
        ;;
    report)
        generate_income_report
        ;;
    health)
        health_check_sites
        ;;
    *)
        echo "WordPress Multi-Tenant Automation"
        echo "Usage: $0 {create|update|backup|delete|report|health}"
        echo ""
        echo "Commands:"
        echo "  create <domain> <plan> <client_name> <client_email>  - Create new site"
        echo "  update                                                 - Update all sites"
        echo "  backup                                                 - Backup all sites"
        echo "  delete <domain>                                        - Delete a site"
        echo "  report                                                 - Generate income report"
        echo "  health                                                 - Health check all sites"
        ;;
esac

