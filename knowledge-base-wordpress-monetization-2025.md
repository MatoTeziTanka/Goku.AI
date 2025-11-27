<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# WordPress Development & Monetization Guide (2025-2026)
## Complete LightSpeedUp.com Setup & Profit Maximization

**Goal**: Turn WordPress into a revenue-generating machine  
**Stack**: WordPress 6.4+, PHP 8.2+, MySQL 8.0+, Apache/Nginx  
**Current Setup**: VM150 (Ubuntu 24.04), lightspeedup.com

## LIGHTSPEEDUP.COM CURRENT INFRASTRUCTURE

### Server Details
- **VM**: VM150 (<VM150_IP>)
- **OS**: Ubuntu 24.04 LTS
- **Web Server**: Apache 2.4
- **Domain**: lightspeedup.com, www.lightspeedup.com, wp.lightspeedup.com
- **Document Root**: /var/www/html
- **WordPress Path**: /var/www/html/wordpress (if installed in subdirectory)
- **Database**: MySQL/MariaDB
- **PHP**: 8.1+ (check with `php -v`)

### Apache Configuration
- **Config**: /etc/apache2/sites-available/lightspeedup.com.conf
- **VirtualHost**: Configured for lightspeedup.com
- **Logs**: /var/log/apache2/lightspeedup.com-*.log

## WORDPRESS BASICS

### Installation
```bash
# SSH to VM150
ssh wp1@<VM150_IP>

# Download WordPress
cd /tmp
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz

# Move to web root
sudo mv wordpress/* /var/www/html/
sudo chown -R www-data:www-data /var/www/html/
sudo chmod -R 755 /var/www/html/
```

### Database Setup
```bash
# Create database
sudo mysql -u root -p

CREATE DATABASE wordpress_db;
CREATE USER 'wp_user'@'localhost' IDENTIFIED BY 'Norelec7!';
GRANT ALL PRIVILEGES ON wordpress_db.* TO 'wp_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### wp-config.php
```php
define('DB_NAME', 'wordpress_db');
define('DB_USER', 'wp_user');
define('DB_PASSWORD', 'Norelec7!');
define('DB_HOST', 'localhost');
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');

// Security keys (generate at https://api.wordpress.org/secret-key/1.1/salt/)
define('AUTH_KEY',         'put your unique phrase here');
define('SECURE_AUTH_KEY',  'put your unique phrase here');
// ... etc

$table_prefix = 'wp_';
define('WP_DEBUG', false);
```

## WORDPRESS DEVELOPMENT

### Theme Development
```php
// themes/mytheme/functions.php
<?php
function mytheme_setup() {
    // Add theme support
    add_theme_support('post-thumbnails');
    add_theme_support('title-tag');
    add_theme_support('custom-logo');
    
    // Register menus
    register_nav_menus(array(
        'primary' => __('Primary Menu'),
        'footer' => __('Footer Menu')
    ));
}
add_action('after_setup_theme', 'mytheme_setup');

// Enqueue styles and scripts
function mytheme_scripts() {
    wp_enqueue_style('main-style', get_stylesheet_uri());
    wp_enqueue_script('main-js', get_template_directory_uri() . '/js/main.js', array('jquery'), '1.0', true);
}
add_action('wp_enqueue_scripts', 'mytheme_scripts');
?>
```

### Plugin Development
```php
// plugins/myplugin/myplugin.php
<?php
/*
Plugin Name: My Plugin
Description: Custom functionality
Version: 1.0
Author: Seth
*/

// Add shortcode
function my_shortcode($atts) {
    $atts = shortcode_atts(array(
        'title' => 'Default Title'
    ), $atts);
    
    return '<h2>' . esc_html($atts['title']) . '</h2>';
}
add_shortcode('mytitle', 'my_shortcode');

// Add custom post type
function create_custom_post_type() {
    register_post_type('portfolio',
        array(
            'labels' => array(
                'name' => __('Portfolio'),
                'singular_name' => __('Portfolio Item')
            ),
            'public' => true,
            'has_archive' => true,
            'supports' => array('title', 'editor', 'thumbnail')
        )
    );
}
add_action('init', 'create_custom_post_type');
?>
```

### Custom Fields (ACF Alternative)
```php
// Add meta box
function add_custom_meta_box() {
    add_meta_box(
        'custom_meta_box',
        'Custom Fields',
        'custom_meta_box_callback',
        'post'
    );
}
add_action('add_meta_boxes', 'add_custom_meta_box');

function custom_meta_box_callback($post) {
    $value = get_post_meta($post->ID, '_custom_field', true);
    echo '<input type="text" name="custom_field" value="' . esc_attr($value) . '" />';
}

// Save meta box
function save_custom_meta_box($post_id) {
    if (array_key_exists('custom_field', $_POST)) {
        update_post_meta($post_id, '_custom_field', sanitize_text_field($_POST['custom_field']));
    }
}
add_action('save_post', 'save_custom_meta_box');
```

## WORDPRESS REST API

### Custom Endpoints
```php
// Add custom REST API endpoint
add_action('rest_api_init', function () {
    register_rest_route('myplugin/v1', '/data', array(
        'methods' => 'GET',
        'callback' => 'get_custom_data',
        'permission_callback' => '__return_true'
    ));
});

function get_custom_data($request) {
    $data = array(
        'message' => 'Hello from WordPress API',
        'timestamp' => time()
    );
    return new WP_REST_Response($data, 200);
}

// Access: https://lightspeedup.com/wp-json/myplugin/v1/data
```

### Authentication
```php
// JWT authentication for headless WordPress
// Install plugin: JWT Authentication for WP REST API

// Use Bearer token in headers
// Authorization: Bearer YOUR_JWT_TOKEN
```

## MONETIZATION STRATEGIES

### 1. Affiliate Marketing
```php
// Add affiliate links to content
function add_affiliate_link($content) {
    $affiliate_link = '<a href="https://affiliate.com/product?ref=lightspeedup">Buy Now</a>';
    return $content . $affiliate_link;
}
add_filter('the_content', 'add_affiliate_link');
```

### 2. Ad Networks
- **Google AdSense**: Display ads, auto-optimize
- **Media.net**: Yahoo/Bing ads
- **Ezoic**: AI-driven ad optimization
- **AdThrive**: Premium network (requires 100k+ pageviews/month)

### 3. Membership Sites
```php
// Use plugins:
// - MemberPress
// - Restrict Content Pro
// - Paid Memberships Pro

// Custom membership check
function is_premium_member() {
    if (is_user_logged_in()) {
        $user = wp_get_current_user();
        return in_array('premium_member', $user->roles);
    }
    return false;
}

// Restrict content
if (is_premium_member()) {
    // Show premium content
} else {
    // Show upgrade message
}
```

### 4. WooCommerce (E-commerce)
```bash
# Install WooCommerce
wp plugin install woocommerce --activate

# Add product programmatically
$product = new WC_Product_Simple();
$product->set_name('My Product');
$product->set_price('29.99');
$product->save();
```

### 5. Online Courses (LMS)
- **LearnDash**: Premium LMS
- **LifterLMS**: Free + paid addons
- **Tutor LMS**: Modern, feature-rich

## PERFORMANCE OPTIMIZATION

### Caching
```php
// Install W3 Total Cache or WP Rocket

// Object caching (Redis)
sudo apt install redis-server
wp plugin install redis-cache --activate
wp redis enable
```

### CDN Integration
```php
// Cloudflare (free CDN)
// 1. Add site to Cloudflare
// 2. Update nameservers at domain registrar
// 3. Enable caching, minification, Brotli compression
```

### Database Optimization
```bash
# WP-CLI database optimize
wp db optimize

# Clean up
wp post delete $(wp post list --post_status=trash --format=ids) --force
wp transient delete --all
```

### Image Optimization
```bash
# Install Imagify or ShortPixel
wp plugin install imagify --activate

# Bulk optimize
wp imagify optimize --all
```

## SECURITY BEST PRACTICES

### Hardening
```php
// wp-config.php security
define('DISALLOW_FILE_EDIT', true);  // Disable theme/plugin editor
define('WP_AUTO_UPDATE_CORE', true); // Auto updates

// .htaccess protection
<Files wp-config.php>
    order allow,deny
    deny from all
</Files>
```

### Security Plugins
- **Wordfence**: Firewall, malware scanner
- **Sucuri Security**: Hardening, monitoring
- **iThemes Security**: 30+ security measures

### SSL/HTTPS
```bash
# Install Let's Encrypt SSL
sudo apt install certbot python3-certbot-apache
sudo certbot --apache -d lightspeedup.com -d www.lightspeedup.com

# Force HTTPS in WordPress
define('FORCE_SSL_ADMIN', true);
```

## WP-CLI (COMMAND LINE)

### Installation
```bash
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar
sudo mv wp-cli.phar /usr/local/bin/wp
```

### Common Commands
```bash
# Core
wp core update
wp core version

# Plugins
wp plugin list
wp plugin install contact-form-7 --activate
wp plugin update --all

# Themes
wp theme list
wp theme install twentytwentyfour --activate

# Database
wp db export backup.sql
wp db import backup.sql

# Users
wp user create seth seth@lightspeedup.com --role=administrator
wp user list

# Posts
wp post create --post_title="My Post" --post_content="Content" --post_status=publish

# Search/Replace
wp search-replace 'http://oldsite.com' 'https://lightspeedup.com'
```

## BACKUP & RECOVERY

### Automated Backups
```bash
# UpdraftPlus plugin
wp plugin install updraftplus --activate

# Manual backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
wp db export /backup/db_$DATE.sql
tar -czf /backup/files_$DATE.tar.gz /var/www/html/
```

### Restore
```bash
wp db import backup.sql
tar -xzf backup.tar.gz -C /var/www/html/
```

## MULTISITE NETWORK

### Enable Multisite
```php
// wp-config.php
define('WP_ALLOW_MULTISITE', true);

// After network setup
define('MULTISITE', true);
define('SUBDOMAIN_INSTALL', false); // Subdirectory install
define('DOMAIN_CURRENT_SITE', 'lightspeedup.com');
define('PATH_CURRENT_SITE', '/');
define('SITE_ID_CURRENT_SITE', 1);
define('BLOG_ID_CURRENT_SITE', 1);
```

## HEADLESS WORDPRESS (JAMSTACK)

### Next.js + WordPress
```javascript
// pages/index.js
export async function getStaticProps() {
    const res = await fetch('https://lightspeedup.com/wp-json/wp/v2/posts');
    const posts = await res.json();
    return { props: { posts } };
}

export default function Home({ posts }) {
    return (
        <div>
            {posts.map(post => (
                <article key={post.id}>
                    <h2>{post.title.rendered}</h2>
                    <div dangerouslySetInnerHTML={{ __html: post.content.rendered }} />
                </article>
            ))}
        </div>
    );
}
```

## REVENUE TRACKING

### Google Analytics 4
```php
// Add to header.php
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### MonsterInsights Plugin
```bash
wp plugin install google-analytics-for-wordpress --activate
```

## LEARNING RESOURCES

- WordPress Codex: codex.wordpress.org
- WordPress Developer Docs: developer.wordpress.org
- WP-CLI Handbook: wp-cli.org
- WooCommerce Docs: woocommerce.com/documentation

## PROFIT MAXIMIZATION CHECKLIST

✅ Install caching plugin (WP Rocket)  
✅ Setup CDN (Cloudflare)  
✅ Enable ads (AdSense, Ezoic)  
✅ Add affiliate links to high-traffic posts  
✅ Create membership tier (premium content)  
✅ Launch online course (LearnDash)  
✅ Setup WooCommerce store (digital products)  
✅ Email marketing (Mailchimp, ConvertKit)  
✅ SEO optimization (Yoast SEO, Rank Math)  
✅ A/B testing (Google Optimize)  

**Complete WordPress monetization guide for SHENRON - LightSpeedUp focused**

