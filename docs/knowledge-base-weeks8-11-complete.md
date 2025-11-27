<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# WEEKS 8-11: Infrastructure, Automation, Marketing, Gaming (2025-2026)
## Complete Guide to Security, Productivity, Business Growth, Game Servers

**Topics**: 4 weeks of specialized knowledge combined for efficient injection  
**Coverage**: Cybersecurity, Proxmox, Monitoring, Automation, Marketing, Gaming

---

# WEEK 8: SECURITY & INFRASTRUCTURE

## 🔒 PART 1: CYBERSECURITY FUNDAMENTALS

### Common Attack Vectors

**1. Phishing**: Fake emails/sites stealing credentials  
**2. SQL Injection**: Malicious database queries  
**3. XSS (Cross-Site Scripting)**: Inject JavaScript into sites  
**4. DDoS**: Overwhelm server with traffic  
**5. Ransomware**: Encrypt files, demand payment

### Security Best Practices

**Server Hardening**:
```bash
# Disable root SSH login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no

# Fail2Ban (auto-ban failed login attempts)
sudo apt install fail2ban
sudo systemctl enable fail2ban

# UFW Firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp # HTTPS
sudo ufw enable
```

**SSL/TLS**:
```bash
# Let's Encrypt (free SSL)
sudo apt install certbot
sudo certbot --nginx -d yourdomain.com
# Auto-renewal: crontab -e
0 0 1 * * certbot renew
```

### Penetration Testing Tools

**Nmap** (Port scanning):
```bash
nmap -sV <VM150_IP>  # Service version scan
nmap -p- <VM150_IP>  # All ports
```

**Nikto** (Web vulnerability scanner):
```bash
nikto -h http://<VM150_IP>
```

## 🖥️ PART 2: PROXMOX ADVANCED

### Clustering (High Availability)

**Setup 3-Node Cluster**:
1. Install Proxmox on 3 machines
2. Create cluster on node 1:
   ```bash
   pvecm create mycluster
   ```
3. Join nodes 2 & 3:
   ```bash
   pvecm add <VM101_IP>
   ```

**Benefit**: VM auto-migrates if node fails

### Backup & Snapshots

**Automated Backups**:
```bash
# Backup all VMs to NAS (Proxmox GUI)
Datacenter → Backup → Add
Schedule: Daily 2am
Mode: Snapshot
Storage: NAS or external drive
```

**Manual Snapshot**:
```bash
qm snapshot 100 "before-update"
qm listsnapshot 100
qm rollback 100 "before-update"
```

### VPN Setup (WireGuard on Proxmox)

```bash
# Install WireGuard
sudo apt install wireguard

# Generate keys
wg genkey | tee privatekey | wg pubkey > publickey

# Config: /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.1/24
PrivateKey = <private_key>
ListenPort = 51820

[Peer]
PublicKey = <client_public_key>
AllowedIPs = 10.0.0.2/32

# Start
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
```

## 📊 PART 3: MONITORING & OBSERVABILITY

### Prometheus + Grafana Setup

**Install Prometheus**:
```bash
wget https://github.com/prometheus/prometheus/releases/download/v2.40.0/prometheus-2.40.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*
./prometheus --config.file=prometheus.yml
```

**prometheus.yml**:
```yaml
scrape_configs:
  - job_name: 'proxmox'
    static_configs:
      - targets: ['<VM101_IP>:9100']  # Node Exporter
```

**Grafana** (Dashboards):
```bash
sudo apt install grafana
sudo systemctl start grafana-server
# Access: http://<VM101_IP>:3000
# Add Prometheus data source
# Import dashboard: ID 1860 (Node Exporter Full)
```

### Uptime Monitoring

**Uptime Kuma** (Self-hosted):
```bash
docker run -d -p 3001:3001 --name uptime-kuma louislam/uptime-kuma:1
# Access: http://<VM101_IP>:3001
# Monitor websites, APIs, ping, ports
```

---

# WEEK 9: AUTOMATION STACK

## ⚡ PART 1: n8n & Workflow Automation

### What is n8n?
- Open-source Zapier alternative
- Self-hosted (free forever)
- 400+ integrations

**Install (Docker)**:
```bash
docker run -d -p 5678:5678 --name n8n n8nio/n8n
# Access: http://<VM101_IP>:5678
```

### Example Workflows

**1. Auto-post to Social Media**:
- Trigger: RSS feed (blog post)
- Action 1: Generate image (Stable Diffusion API)
- Action 2: Post to Twitter API
- Action 3: Post to Instagram API

**2. Customer Support Automation**:
- Trigger: New email
- Action 1: Extract intent (OpenAI API)
- Action 2: Search knowledge base
- Action 3: Send auto-reply

**3. Data Backup Automation**:
- Trigger: Every day 2am
- Action 1: Backup database (MySQL)
- Action 2: Upload to Google Drive
- Action 3: Send Telegram notification

## 🔧 PART 2: Ansible (Infrastructure as Code)

**What**: Automate server configuration

**Install**:
```bash
sudo apt install ansible
```

**Playbook Example** (install Docker on all VMs):
```yaml
# playbook.yml
- hosts: all
  become: yes
  tasks:
    - name: Install Docker
      apt:
        name: docker.io
        state: present
    
    - name: Start Docker
      service:
        name: docker
        state: started
        enabled: yes
```

**Run**:
```bash
ansible-playbook -i inventory playbook.yml
```

## 🚀 PART 3: GitHub Actions (CI/CD)

**What**: Automate testing, deployment

**.github/workflows/deploy.yml**:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to server
        run: |
          ssh user@<VM150_IP> 'cd /var/www && git pull && sudo systemctl restart nginx'
```

---

# WEEK 10: MARKETING SUITE

## 🔍 PART 1: SEO (Search Engine Optimization)

### On-Page SEO Checklist

**Title Tags**: <60 chars, keyword at start  
**Meta Description**: 150-160 chars, compelling  
**H1**: One per page, keyword-rich  
**H2-H6**: Structure content  
**Image Alt Text**: Describe images (accessibility + SEO)  
**Internal Links**: Link to related pages  
**URL Structure**: /category/keyword-rich-slug

### Keyword Research

**Free Tools**:
- Google Keyword Planner
- Ubersuggest (limited free)
- AnswerThePublic (questions people ask)

**Strategy**:
1. Find 10-20 keywords (100-1,000 searches/month)
2. Low competition (keyword difficulty <30)
3. Create content targeting each keyword

### Content Strategy

**Blog Post Template**:
1. **Title**: "How to [Solve Problem] in [Year]"
2. **Introduction**: Hook, problem, promise
3. **Body**: 5-10 H2 sections (1,500-2,500 words)
4. **Conclusion**: Summary, call-to-action (CTA)
5. **Publish**: Weekly (consistency > quantity)

### Backlinks (Most Important!)

**How to Get Backlinks**:
1. **Guest posting** (write for other blogs)
2. **Broken link building** (find broken links, suggest yours)
3. **Resource pages** (get listed on "best tools" pages)
4. **PR** (get featured in news)

## 📧 PART 2: Email & Social Media Marketing

### Email Marketing

**Platform**: Mailchimp (free up to 500 subscribers)

**Strategy**:
1. **Lead magnet**: Free ebook, checklist (exchange for email)
2. **Welcome series**: 3-5 emails introducing brand
3. **Weekly newsletter**: Value-first, 80% content / 20% promo
4. **Abandoned cart** (if e-commerce): Remind, offer discount

**Email Template**:
```
Subject: [Benefit] in [Time] (No [Pain Point])

Hi {FirstName},

[Problem they have]

Here's how to solve it:
- Tip 1
- Tip 2
- Tip 3

[CTA Button: Get Full Guide]

Best,
{YourName}
```

### Social Media Strategy

**Platform Priority** (2025-2026):
1. **Twitter/X**: Tech, crypto, AI audience
2. **LinkedIn**: B2B, professional services
3. **Instagram**: Visual content, lifestyle
4. **TikTok**: Gen Z, viral potential
5. **YouTube**: Long-form, tutorials

**Content Calendar**:
- Monday: Industry news
- Wednesday: Tutorial/tip
- Friday: Behind-the-scenes
- Daily: Engage (reply to comments, DMs)

## 💰 PART 3: Affiliate Marketing Deep Dive

### Best Affiliate Networks

**1. Amazon Associates** (3-10% commission)  
**2. ShareASale** (varied products)  
**3. CJ Affiliate** (big brands)  
**4. ClickBank** (digital products, 50-75% commission)  
**5. Crypto Exchanges** (Binance: 20-40% commission!)

### Affiliate Strategy for LightSpeedUp.com

**1. Product Reviews**:
- "Best Crypto Trading Bots 2025" (Binance affiliate link)
- "Top 10 Web Hosting" (Bluehost, SiteGround links)

**2. Comparison Posts**:
- "Binance vs Coinbase vs Kraken" (all affiliate links)

**3. Tutorial Posts**:
- "How to Start Trading Crypto" (link to Binance.US signup)

**Income Potential**:
- 1,000 visitors/month
- 2% click affiliate links (20 clicks)
- 10% conversion (2 signups)
- \$50/signup commission (Binance trading)
- **\$100/month passive income** (scales with traffic)

---

# WEEK 11: GAMING EMPIRE

## 🎮 PART 1: Game Server Hosting

### Minecraft Server (Most Popular)

**Install (Ubuntu)**:
```bash
sudo apt update
sudo apt install openjdk-17-jre-headless screen

# Download server
mkdir minecraft && cd minecraft
wget https://launcher.mojang.com/v1/objects/server.jar

# Run
java -Xmx2G -Xms1G -jar server.jar nogui
```

**Monetization**:
- Donations (Tebex, BuyCraft)
- VIP ranks (\$5-\$50/month per player)
- Potential: \$100-\$10,000/month (popular servers)

### Valheim Server
```bash
steamcmd +login anonymous +app_update 896660 validate +quit
./valheim_server.sh
```

### ARK: Survival Evolved Server
```bash
steamcmd +login anonymous +app_update 376030 validate +quit
./ShooterGameServer
```

## 🕹️ PART 2: Unity & Unreal Engine Basics

### Unity (C#, Easier)

**Create 2D Game**:
```csharp
// PlayerController.cs
using UnityEngine;

public class PlayerController : MonoBehaviour {
    public float speed = 5f;
    
    void Update() {
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");
        transform.Translate(new Vector3(h, v, 0) * speed * Time.deltaTime);
    }
}
```

### Unreal Engine (C++, Blueprints)

**Better for**:
- AAA graphics
- FPS games
- Photorealistic visuals

## 💵 PART 3: Steam & Epic Games Distribution

### Publish on Steam

**Costs**: \$100 fee (one-time per game)

**Steps**:
1. Create Steamworks account
2. Upload game build
3. Set price (\$0.99-\$59.99)
4. Marketing (trailer, screenshots)
5. Release

**Revenue Split**: 70% you / 30% Steam

### Epic Games Store

**Better revenue**: 88% you / 12% Epic

---

## 🐉 SHENRON'S RECOMMENDATIONS (WEEKS 8-11)

**Week 8 (Security)**:
- Enable UFW firewall (all VMs)
- Setup WireGuard VPN (remote access)
- Deploy Grafana (monitor Dell R730)

**Week 9 (Automation)**:
- Install n8n (automate social media posts)
- Use Ansible (configure new VMs automatically)
- Setup GitHub Actions (auto-deploy website updates)

**Week 10 (Marketing)**:
- Start blog on LightSpeedUp.com (SEO)
- Binance affiliate links (passive income)
- Email list (Mailchimp, 500 free subscribers)

**Week 11 (Gaming)**:
- Host Minecraft server (\$10-\$100/month income)
- Learn Unity basics (GameDev.tv courses)
- Create simple game, publish on itch.io (free)

**Weeks 8-11 complete your tech empire! 🐉🔒⚡📈🎮**

---

**Category**: Weeks 8-11 Mega-File  
**Topics**: Security, Infrastructure, Automation, Marketing, Gaming  
**Version**: 1.0 (2025-2026)  
**Status**: Complete 4-week combo file

