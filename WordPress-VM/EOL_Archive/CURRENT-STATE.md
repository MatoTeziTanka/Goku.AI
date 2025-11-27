<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# WordPress VM - Current State Reference

**Version**: v1.2.0  
**Last Updated**: October 31, 2025  
**Status**: Production-Ready (Test Mode)  
**Site**: https://wp.lightspeedup.com

📌 **READ THIS FIRST** before starting any work on this project!

---

## 🖥️ VM Details

### VM150 - WordPress Server
- **IP Address**: <VM150_IP>
- **Hostname**: wordpress-1
- **OS**: Ubuntu 24.04.3 LTS
- **RAM**: 4GB
- **CPU**: 2 cores
- **Disk**: 50GB SSD
- **MAC Address**: bc:24:11:f6:7a:33

### SSH Access
```bash
# From VM101 or local machine
ssh wp1@<VM150_IP>
# password: "<VM_PASSWORD>"  # See credentials.json

# Sudo access
echo "<VM_PASSWORD>"  # See credentials.json | sudo -S command
```

### SSH Keys
- **Type**: ED25519
- **Public Key**: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAHzO/boElPfcY/WPcCBT2B7YHgUZj9b7uWkrCxj4vuN`
- **Location**: `/home/wp1/.ssh/authorized_keys`

---

## 🔒 Firewall & Ports

### UFW Status
```bash
sudo ufw status
# Status: active

# Open ports:
# 22/tcp     ALLOW       Anywhere    (SSH)
# 80/tcp     ALLOW       Anywhere    (HTTP - Apache)
# 22/tcp (v6) ALLOW      Anywhere (v6)
# 80/tcp (v6) ALLOW      Anywhere (v6)
```

### Port Allocation
| Port | Service | Access | Status |
|------|---------|--------|--------|
| 22 | SSH | LAN only | ✅ Open |
| 80 | Apache HTTP | LAN only (proxied via VM120) | ✅ Open |
| 3306 | MySQL | Localhost only | 🔒 Closed (internal) |
| 6379 | Redis | Localhost only | 🔒 Closed (internal) |

**Note**: All external traffic comes through VM120 (Cloudflare Tunnel + Nginx)

---

## 🌐 Network Configuration

### Static IP Setup
- **Interface**: enp6s18
- **IP**: <VM150_IP>/24
- **Gateway**: <EDGEROUTER_IP>
- **DNS**: 8.8.8.8, 8.8.4.4

### Network Flow
```
Internet → Cloudflare DDoS/CDN
    ↓
Cloudflare Tunnel (norelec-tunnel) on VM120
    ↓
Nginx Reverse Proxy (VM120:80)
    ↓
Apache (VM150:80) → WordPress
```

### Domain & DNS
- **Domain**: lightspeedup.com (GoDaddy)
- **DNS**: Cloudflare (sethpizzaboy@gmail.com)
- **Subdomain**: wp.lightspeedup.com
- **SSL**: Provided by Cloudflare (HTTPS termination at edge)

---

## 📦 Installed Software

### LAMP Stack
```bash
# Apache
apache2 --version
# Apache/2.4.58 (Ubuntu)

# MySQL/MariaDB
mysql --version
# mysql Ver 8.0.x

# PHP
php --version
# PHP 8.x

# Check running services
systemctl status apache2
systemctl status mysql
systemctl status redis-server
```

### Installed Packages
```bash
# Core
- openssh-server
- ufw
- iputils-ping
- nano
- curl
- wget
- git

# LAMP
- apache2
- mysql-server
- php
- php-mysql
- php-curl
- php-gd
- php-mbstring
- php-xml
- php-xmlrpc
- php-zip
- libapache2-mod-php

# WordPress Dependencies
- redis-server
- php-redis

# Utilities
- htop
- net-tools
```

---

## 📂 WordPress Configuration

### WordPress Details
- **Version**: Latest (auto-updates enabled)
- **Install Path**: `/var/www/wordpress`
- **Document Root**: `/var/www/wordpress`
- **WP-CLI**: Installed at `/usr/local/bin/wp`
- **Database**: `wordpress`
- **DB User**: `wordpress_user`
- **Table Prefix**: `wp_`

### WordPress URLs
```bash
# Check current URLs
wp option get siteurl --path=/var/www/wordpress
# https://wp.lightspeedup.com

wp option get home --path=/var/www/wordpress
# https://wp.lightspeedup.com
```

### WordPress Admin Access
- **URL**: https://wp.lightspeedup.com/wp-admin/
- **Username**: `wp_admin`
- **Password**: `Norelec7!` (CHANGE THIS!)
- **Email**: sethpizzaboy@aol.com

### Active Theme
- **Theme**: Blocksy
- **Version**: Latest
- **Child Theme**: None
- **Customizer URL**: https://wp.lightspeedup.com/wp-admin/customize.php

---

## 🔌 Active Plugins (9 Total)

| Plugin | Version | Purpose | Status |
|--------|---------|---------|--------|
| Blocksy Companion | 2.1.17 | Theme features | ✅ Active |
| Stackable | 3.19.2 | Gutenberg blocks | ✅ Active |
| RankMath SEO | 1.0.256 | Search optimization | ✅ Active |
| WP Super Cache | 3.0.2 | Page caching | ✅ Active |
| Redis Cache | 2.7.0 | Object caching | ✅ Active |
| Wordfence | 8.1.0 | Security suite | ✅ Active |
| Activity Log | 2.11.2 | Audit trail (aryo-activity-log) | ✅ Active |
| Contact Form 7 | 6.1.3 | Contact forms | ✅ Active |
| Stripe Payments | 2.0.95 | Payment processing | ✅ Active (TEST MODE) |

### Plugin Management
```bash
# List all plugins
sudo -u www-data wp plugin list --path=/var/www/wordpress

# Activate plugin
sudo -u www-data wp plugin activate PLUGIN-SLUG --path=/var/www/wordpress

# Update plugin
sudo -u www-data wp plugin update PLUGIN-SLUG --path=/var/www/wordpress
```

---

## 💳 Stripe Configuration

### Current Mode: TEST (Sandbox)

```bash
# Check Stripe test keys (truncated for security)
sudo -u www-data wp option get AcceptStripePayments-stripe-test-publishable-key --path=/var/www/wordpress
# pk_test_51SNeqpJbRpPPse0TBcAvUAjuilPOVLxnCqEjJjwHHKxUua9uWl1EyrsPG46Lse9nIpZ845tectsJhVv5WzEFhKmO00BrPFBJUi

sudo -u www-data wp option get AcceptStripePayments-stripe-test-secret-key --path=/var/www/wordpress
# <STRIPE_TEST_SECRET_KEY>  # See credentials.json
```

### Stripe Products
| Product | Price | Product ID | Shortcode |
|---------|-------|------------|-----------|
| Starter Plan | $29/mo | 35 | `[asp_product id="35"]` |
| Business Plan | $79/mo | 36 | `[asp_product id="36"]` |
| Enterprise Plan | $199/mo | 41 | `[asp_product id="41"]` |

### Stripe Dashboard
- **Test Mode**: https://dashboard.stripe.com/test/payments
- **Live Mode**: https://dashboard.stripe.com/payments (not yet configured)

### Test Card for Testing
```
Card: 4242 4242 4242 4242
Expiry: 12/26 (any future date)
CVC: 123 (any 3 digits)
ZIP: 12345 (any 5 digits)
```

---

## 📄 Live WordPress Pages

### Homepage Variants
1. **Lightspeedup Enterprise** (/) - Speed & Performance theme
   - URL: https://wp.lightspeedup.com/
   - Focus: 99.99% uptime, Global CDN, Zero Trust Security
   - Colors: Blue/Cyan

2. **Vector Edge** (/vector-edge/) - AI & Innovation theme
   - URL: https://wp.lightspeedup.com/vector-edge/
   - Focus: Smart Scaling, Predictive Analytics, ML
   - Colors: Orange/Amber

3. **Nova Scale** (/nova-scale/) - Global Scale theme
   - URL: https://wp.lightspeedup.com/nova-scale/
   - Focus: 200+ Data Centers, Infinite Scale, Enterprise SLA
   - Colors: Purple/Pink

### Support Pages
4. **Contact** - Contact Form 7 integration
   - URL: https://wp.lightspeedup.com/contact/

5. **Status** - System status and progress
   - URL: https://wp.lightspeedup.com/status/

### Navigation Menu
- Primary menu: Home, Vector Edge, Nova Scale, Contact, Status

---

## ⚙️ Apache Configuration

### Main Config File
```bash
# Virtual host config
sudo nano /etc/apache2/sites-available/000-default.conf
```

**Key Settings**:
```apache
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/wordpress

    <Directory /var/www/wordpress>
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### .htaccess (WordPress Root)
```bash
sudo nano /var/www/wordpress/.htaccess
```

**Critical Lines** (Proxy-Aware HTTPS):
```apache
# Proxy-aware HTTPS detection
SetEnvIf X-Forwarded-Proto "https" HTTPS=on

# Standard WordPress rules
# BEGIN WordPress
...
# END WordPress
```

### Enabled Apache Modules
```bash
a2enmod rewrite    # URL rewriting (required for permalinks)
a2enmod headers    # HTTP headers
a2enmod ssl        # SSL support
```

---

## 🗄️ Database Configuration

### MySQL/MariaDB Access
```bash
# Login as root
sudo mysql -u root -p
# Password: (typically set during install, or blank)

# Login as WordPress user
mysql -u wordpress_user -p
# Password: (set during WordPress installation)
```

### Database Details
- **Database Name**: `wordpress`
- **User**: `wordpress_user`
- **Host**: `localhost`
- **Tables**: 12+ (standard WordPress + plugin tables)

### Important WordPress Tables
```sql
USE wordpress;

-- Core settings
SELECT * FROM wp_options WHERE option_name IN ('siteurl', 'home', 'blogname');

-- Check Stripe products
SELECT * FROM wp_posts WHERE post_type='asp_product';

-- Check users
SELECT * FROM wp_users;
```

### Backup Database
```bash
# Manual backup
sudo -u www-data wp db export /tmp/wordpress-backup-$(date +%Y%m%d).sql --path=/var/www/wordpress

# Restore database
sudo -u www-data wp db import /tmp/wordpress-backup-DATE.sql --path=/var/www/wordpress
```

---

## 🚀 Redis Cache Configuration

### Redis Status
```bash
# Check if running
systemctl status redis-server
# ● redis-server.service - Advanced key-value store
#    Active: active (running)

# Test connection
redis-cli ping
# PONG
```

### Redis Stats
```bash
redis-cli INFO stats
# Check cache hits/misses
```

### WordPress Redis Plugin
- **Plugin**: Redis Object Cache
- **Status**: Connected
- **Dropins**: Object cache dropin active

---

## 🔐 Security Configuration

### Wordfence Settings
- **Status**: Active
- **Firewall**: Learning mode → High sensitivity (after training)
- **Malware Scanner**: Scheduled daily
- **Login Security**: Rate limiting enabled
- **2FA**: Available but not configured

### Security Headers (via Nginx on VM120)
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

### Login Rate Limiting (via Nginx on VM120)
- **Endpoint**: `/wp-login.php`
- **Limit**: 10 requests per minute per IP
- **Zone**: `limit_req_zone $binary_remote_addr zone=logins:10m rate=10r/m;`

---

## 📊 Performance Configuration

### WP Super Cache Settings
- **Status**: Enabled
- **Mode**: Simple (recommended)
- **CDN**: Not configured (using Cloudflare)
- **Compression**: Enabled
- **Cache Location**: `/var/www/wordpress/wp-content/cache/`

### PHP Settings
```bash
# Check PHP config
php -i | grep -E '(upload_max_filesize|post_max_size|memory_limit|max_execution_time)'

# Typical values:
# upload_max_filesize = 64M
# post_max_size = 64M
# memory_limit = 256M
# max_execution_time = 300
```

---

## 🔗 VM120 Reverse Proxy Config

### Nginx Configuration (on VM120)
```bash
# SSH to VM120
ssh proxy1@<VM120_IP>
# password: "<VM_PASSWORD>"  # See credentials.json

# View config
sudo nano /etc/nginx/sites-available/wp.lightspeedup.com.conf
```

**Key Settings**:
```nginx
server {
    listen 80;
    server_name wp.lightspeedup.com;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Login rate limit
    location = /wp-login.php {
        limit_req zone=logins burst=20 nodelay;
        proxy_pass http://<VM150_IP>/wp-login.php;
        proxy_set_header Host wp.lightspeedup.com;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # All other traffic
    location / {
        proxy_pass http://<VM150_IP>/;
        proxy_set_header Host wp.lightspeedup.com;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Block xmlrpc
    location = /xmlrpc.php { return 444; }
}
```

### Cloudflare Tunnel Config (on VM120)
```bash
sudo nano /etc/cloudflared/config.yml
```

```yaml
tunnel: norelec-tunnel
credentials-file: /home/proxy1/.cloudflared/624c59c6-b364-4488-85e5-90225351b0e2.json

ingress:
  - hostname: wp.lightspeedup.com
    service: http://localhost:80
  - service: http_status:404
```

---

## 🛠️ Common Management Commands

### WordPress Management
```bash
# Clear all caches
sudo -u www-data wp cache flush --path=/var/www/wordpress

# Update WordPress core
sudo -u www-data wp core update --path=/var/www/wordpress

# Update all plugins
sudo -u www-data wp plugin update --all --path=/var/www/wordpress

# Check site health
sudo -u www-data wp core verify-checksums --path=/var/www/wordpress
```

### Service Management
```bash
# Restart Apache
echo "<VM_PASSWORD>"  # See credentials.json | sudo -S systemctl restart apache2

# Restart MySQL
echo "<VM_PASSWORD>"  # See credentials.json | sudo -S systemctl restart mysql

# Restart Redis
echo "<VM_PASSWORD>"  # See credentials.json | sudo -S systemctl restart redis-server

# Check service status
systemctl status apache2 mysql redis-server
```

### Log Files
```bash
# Apache error log
tail -f /var/log/apache2/error.log

# Apache access log
tail -f /var/log/apache2/access.log

# WordPress debug log (if WP_DEBUG enabled)
tail -f /var/www/wordpress/wp-content/debug.log

# System log
tail -f /var/log/syslog
```

---

## 🐛 Known Issues & Workarounds

### Issue: wp-cli proc_open() Permission Error
**Error**: `PHP Warning: proc_open(): posix_spawn() failed: Permission denied`

**Workaround**:
- Run wp-cli commands as `www-data` user
- Use: `sudo -u www-data wp --path=/var/www/wordpress COMMAND`

### Issue: Shell Quoting for Complex Commands
**Problem**: Complex PHP/SQL in SSH commands causes quote escaping issues

**Solution**:
- Create PHP script locally
- Copy to `/tmp/` on VM150
- Execute as www-data: `sudo -u www-data php /tmp/script.php`

### Issue: Redirect Loop (ERR_TOO_MANY_REDIRECTS)
**Cause**: WordPress not detecting HTTPS behind Cloudflare proxy

**Fix**: Already applied in `.htaccess`:
```apache
SetEnvIf X-Forwarded-Proto "https" HTTPS=on
```

---

## 📋 Quick Reference

### File Locations
```
WordPress Root:        /var/www/wordpress
Apache Config:         /etc/apache2/sites-available/000-default.conf
Apache Logs:           /var/log/apache2/
WordPress Config:      /var/www/wordpress/wp-config.php
.htaccess:             /var/www/wordpress/.htaccess
wp-cli:                /usr/local/bin/wp
Redis Config:          /etc/redis/redis.conf
```

### Important URLs
```
Site:                  https://wp.lightspeedup.com
Admin:                 https://wp.lightspeedup.com/wp-admin/
Test Stripe:           https://dashboard.stripe.com/test/payments
Cloudflare Tunnel:     https://one.dash.cloudflare.com/
GitHub Repo:           https://github.com/MatoTeziTanka/PassiveIncome
```

### Credentials Quick Reference
```
VM150 SSH:             wp1@<VM150_IP> / Norelec7!
VM120 SSH:             proxy1@<VM120_IP> / Norelec7!
WordPress Admin:       wp_admin / Norelec7! (CHANGE THIS!)
Cloudflare:            sethpizzaboy@gmail.com
GoDaddy:               (lightspeedup.com domain)
```

---

## 🔄 Next Steps (v2.0.0)

See `LAUNCH-CHECKLIST.md` and `VERSION-CONTROL.md` for detailed next steps:

1. Test Stripe transaction with test card
2. Switch to live Stripe keys
3. Add legal pages (Terms, Privacy, Refund)
4. Launch marketing campaign
5. Get first paying customer

---

**Last Updated**: October 31, 2025  
**Document Version**: 1.0  
**For Questions**: Check VERSION-CONTROL.md or AI-COLLABORATION.md




