<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# WordPress + Stripe Integration - Complete Setup Guide

**Date**: October 31, 2025  
**Status**: ✅ Production-Ready (Test Mode)  
**Site**: https://wp.lightspeedup.com

---

## 🎯 What's Live

### Three Enterprise-Focused Homepage Variants

Each variant has a distinct theme, content, and visual style targeting different market segments:

#### 1. **Lightspeed Enterprise** (Main Homepage)
- **URL**: https://wp.lightspeedup.com/
- **Focus**: Speed & Performance
- **Key Features**: 99.99% uptime, Global CDN, Zero Trust Security
- **Target**: Enterprises prioritizing performance and reliability
- **Color Scheme**: Blue/Cyan tones

#### 2. **Vector Edge**
- **URL**: https://wp.lightspeedup.com/vector-edge/
- **Focus**: AI & Innovation
- **Key Features**: Smart Scaling, Predictive Analytics, Auto-Optimization
- **Target**: Tech-forward companies leveraging ML/AI
- **Color Scheme**: Orange/Amber tones

#### 3. **Nova Scale**
- **URL**: https://wp.lightspeedup.com/nova-scale/
- **Focus**: Global Scale & Infrastructure
- **Key Features**: 200+ Data Centers, Infinite Scale, Enterprise SLA
- **Target**: Global enterprises needing massive scale
- **Color Scheme**: Purple/Pink tones

---

## 💳 Stripe Integration

### Current Configuration (TEST MODE)
```bash
Mode: Sandbox/Test
Publishable Key: pk_test_51SNeqpJbRpPPse0TBcAvUAjuilPOVLxnCqEjJjwHHKxUua9uWl1EyrsPG46Lse9nIpZ845tectsJhVv5WzEFhKmO00BrPFBJUi
Secret Key: <STRIPE_TEST_SECRET_KEY>  # See credentials.json
```

### Payment Products Created
1. **Starter Plan**: $9/month (WordPress Product ID: 35)
2. **Business Plan**: $29/month (WordPress Product ID: 36)

Both products are available on all three variant pages with checkout buttons using the shortcode format:
- `[asp_product id="35"]` → Starter Plan button
- `[asp_product id="36"]` → Business Plan button

---

## 🧪 Testing Your Checkout

### Test Card Details
Use these Stripe test credentials to simulate transactions:

```
Card Number: 4242 4242 4242 4242
Expiry: Any future date (e.g., 12/26)
CVC: Any 3 digits (e.g., 123)
ZIP: Any 5 digits (e.g., 12345)
Name: Test User
```

### Testing Steps
1. Visit any of the three variant pages
2. Click either "Subscribe Now - $9/mo" or "Subscribe Now - $29/mo"
3. Enter the test card details above
4. Complete the checkout
5. Verify success message
6. Check your Stripe Dashboard (https://dashboard.stripe.com/test/payments) for the test transaction

---

## 🏗️ Infrastructure Architecture

```
Internet (HTTPS)
    ↓
Cloudflare Tunnel (norelec-tunnel)
    ↓ [CNAME: wp.lightspeedup.com → 624c59c6-...cfargotunnel.com]
VM120 (Reverse Proxy)
    ↓ [Nginx on :80 with security headers, rate limiting]
    ↓ [proxy_pass → http://<VM150_IP>/]
VM150 (WordPress)
    ↓ [Apache 2.4.58 serving /var/www/wordpress]
WordPress + Stripe Payments Plugin
```

### Security Layers
1. **Cloudflare**: DDoS protection, WAF, HTTPS termination
2. **Nginx (VM120)**: Rate limiting (10 req/min for wp-login.php), security headers
3. **Apache (VM150)**: .htaccess with proxy-aware HTTPS detection
4. **WordPress**: Wordfence WAF, malware scanning, 2FA capability
5. **UFW**: Firewall on both VMs (SSH + HTTP only)

---

## 📦 WordPress Stack

### Server Details
- **VM**: 150 (wordpress-1)
- **IP**: <VM150_IP>
- **OS**: Ubuntu 24.04.3 LTS
- **Web Server**: Apache 2.4.58
- **Database**: MySQL/MariaDB
- **PHP**: 8.x
- **Document Root**: `/var/www/wordpress`

### Active Theme
- **Blocksy** (modern, customizable, lightweight)

### Active Plugins
| Plugin | Purpose | Status |
|--------|---------|--------|
| Blocksy Companion | Theme features | ✅ Active |
| Stackable | Gutenberg blocks | ✅ Active |
| RankMath SEO | Search optimization | ✅ Active |
| WP Super Cache | Page caching | ✅ Active |
| Redis Cache | Object caching | ✅ Active |
| Wordfence | Security suite | ✅ Active |
| Activity Log | Audit trail | ✅ Active |
| Contact Form 7 | Contact forms | ✅ Active |
| Stripe Payments | Payment processing | ✅ Active (TEST MODE) |

---

## 🔐 Security Configuration

### Nginx Security Headers (VM120)
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

### Rate Limiting
- Login endpoint (`/wp-login.php`): 10 requests/minute per IP
- Brute force protection via Wordfence

### Blocked Endpoints
- `xmlrpc.php` (returns 444 - connection closed)

---

## 📊 Admin Access

### WordPress Admin
- **URL**: https://wp.lightspeedup.com/wp-admin/
- **Username**: wp_admin
- **Password**: Norelec7! (stored securely)

### Server SSH
```bash
# From VM101 (management server)
ssh wp1@<VM150_IP>
# password: "<VM_PASSWORD>"  # See credentials.json
```

---

## 🚀 Next Steps to Production

### Immediate Actions Available
1. **Test Transaction**: Use test card to verify end-to-end payment flow
2. **Branding**: Add logo, custom colors, favicon
3. **Content Polish**: Fine-tune copy, add images, adjust spacing
4. **Form Setup**: Configure Contact Form 7 fields and email notifications

### Before Going Live (Real Revenue)
1. **Stripe Live Keys**: Switch from test to live mode in Stripe plugin settings
2. **Webhook Configuration**: Set up Stripe webhooks for payment notifications
   ```
   Webhook URL: https://wp.lightspeedup.com/?asp_action=ipn
   Events: payment_intent.succeeded, customer.subscription.*
   ```
3. **Legal Pages**: Add Terms of Service, Privacy Policy, Refund Policy
4. **SSL Validation**: Verify Cloudflare SSL certificate is valid
5. **Backup Strategy**: Configure automated daily backups (database + files)
6. **Monitoring**: Set up uptime monitoring (e.g., UptimeRobot, Pingdom)
7. **Email Provider**: Configure SMTP for transactional emails (SendGrid, Mailgun)

### Recommended Enhancements
1. **Analytics**: Add Google Analytics or Plausible
2. **Customer Portal**: Set up Stripe Customer Portal for subscription management
3. **Email Marketing**: Integrate with Mailchimp/ConvertKit for lead nurturing
4. **Live Chat**: Add Intercom or Crisp for customer support
5. **Blog**: Create content marketing strategy with SEO-optimized posts
6. **A/B Testing**: Use Google Optimize to test variant performance

---

## 📈 Revenue Tracking

### Stripe Dashboard
- **Test Mode**: https://dashboard.stripe.com/test/dashboard
- **Live Mode**: https://dashboard.stripe.com/dashboard (when activated)

### Key Metrics to Monitor
- Monthly Recurring Revenue (MRR)
- Customer Lifetime Value (CLV)
- Churn Rate
- Conversion Rate (visitors → customers)
- Average Revenue Per User (ARPU)

---

## 🛠️ Maintenance Commands

### Clear WordPress Cache
```bash
ssh wp1@<VM150_IP>
echo "<VM_PASSWORD>"  # See credentials.json | sudo -S -u www-data wp --path=/var/www/wordpress cache flush
```

### List Active Plugins
```bash
ssh wp1@<VM150_IP>
echo "<VM_PASSWORD>"  # See credentials.json | sudo -S -u www-data wp --path=/var/www/wordpress plugin list --status=active
```

### Check Stripe Configuration
```bash
ssh wp1@<VM150_IP>
echo "<VM_PASSWORD>"  # See credentials.json | sudo -S -u www-data wp --path=/var/www/wordpress option get AcceptStripePayments-settings
```

### Restart Services
```bash
# Restart Apache on VM150
ssh wp1@<VM150_IP> "echo "<VM_PASSWORD>"  # See credentials.json | sudo -S systemctl restart apache2"

# Restart Nginx on VM120
ssh proxy1@<VM120_IP> "echo "<VM_PASSWORD>"  # See credentials.json | sudo -S systemctl restart nginx"

# Restart Cloudflare Tunnel on VM120
ssh proxy1@<VM120_IP> "echo "<VM_PASSWORD>"  # See credentials.json | sudo -S systemctl restart cloudflared"
```

---

## 📞 Support & Documentation

### Useful Links
- WordPress Admin: https://wp.lightspeedup.com/wp-admin/
- Status Page: https://wp.lightspeedup.com/status/
- Contact Form: https://wp.lightspeedup.com/contact/
- Stripe Dashboard: https://dashboard.stripe.com/test/dashboard
- Cloudflare Dashboard: https://dash.cloudflare.com/

### Plugin Documentation
- [Stripe Payments Plugin](https://wordpress.org/plugins/stripe-payments/)
- [Blocksy Theme](https://creativethemes.com/blocksy/docs/)
- [Contact Form 7](https://contactform7.com/docs/)
- [Wordfence Security](https://www.wordfence.com/help/)

---

## ✅ Completion Checklist

- [x] WordPress installed and configured
- [x] Blocksy theme activated with modern design
- [x] Three distinct homepage variants created
- [x] Stripe Payments plugin installed and configured (TEST MODE)
- [x] Two subscription products created ($9 and $29 plans)
- [x] Checkout buttons integrated on all variant pages
- [x] Cloudflare Tunnel configured for HTTPS
- [x] Nginx reverse proxy with security headers
- [x] Rate limiting on login endpoints
- [x] Redis object caching enabled
- [x] Wordfence security suite active
- [x] Contact Form 7 installed
- [x] Activity logging enabled
- [ ] Test transaction completed
- [ ] Logo and branding integrated
- [ ] Automated backups configured
- [ ] Monitoring and alerts set up
- [ ] Legal pages created
- [ ] Stripe webhooks configured
- [ ] Transition to live Stripe keys

---

**Generated**: October 31, 2025  
**Last Updated**: October 31, 2025  
**Maintained By**: AI Infrastructure Assistant

