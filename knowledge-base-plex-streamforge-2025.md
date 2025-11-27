<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Plex Media Server & StreamForge Complete Guide (2025-2026)
## Media Server Empire on Dell R730 & Proxmox

**Goal**: Build a powerful streaming media server for personal use and potential monetization  
**Hardware**: Dell R730, Proxmox VMs, NVIDIA GRID K1 GPU  
**Software**: Plex Media Server, Jellyfin, Sonarr, Radarr, Transmission  
**Reference**: StreamForge GitHub repo

## PLEX MEDIA SERVER BASICS

### What is Plex?
- Media server software (organize & stream movies, TV shows, music, photos)
- Client-server architecture (server hosts media, clients stream)
- Transcoding support (convert media on-the-fly)
- Remote access (stream from anywhere)
- Multi-platform (Windows, Linux, Docker, mobile, smart TVs)

### Plex vs Jellyfin
- **Plex**: Polished UI, better mobile apps, paid Plex Pass ($5/month or $120 lifetime)
- **Jellyfin**: 100% free, open-source, no analytics tracking
- **Choice**: Plex for ease-of-use, Jellyfin for privacy/cost

## INSTALLATION ON DELL R730 / PROXMOX

### Option 1: Docker Installation (Recommended)
```bash
# SSH to VM (Ubuntu VM101 or dedicated media VM)
ssh user@<VM101_IP>

# Create Plex directories
mkdir -p ~/plex/config
mkdir -p ~/plex/media/movies
mkdir -p ~/plex/media/tv
mkdir -p ~/plex/media/music

# Run Plex in Docker
docker run -d \
  --name=plex \
  --net=host \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=America/New_York \
  -e VERSION=docker \
  -v ~/plex/config:/config \
  -v ~/plex/media/tv:/tv \
  -v ~/plex/media/movies:/movies \
  -v ~/plex/media/music:/music \
  --restart unless-stopped \
  plexinc/pms-docker

# Access Plex: http://<VM101_IP>:32400/web
```

### Option 2: Native Installation (Ubuntu)
```bash
# Add Plex repository
echo deb https://downloads.plex.tv/repo/deb public main | sudo tee /etc/apt/sources.list.d/plexmediaserver.list
curl https://downloads.plex.tv/plex-keys/PlexSign.key | sudo apt-key add -

# Install
sudo apt update
sudo apt install plexmediaserver

# Start service
sudo systemctl start plexmediaserver
sudo systemctl enable plexmediaserver

# Access: http://<VM101_IP>:32400/web
```

## PLEX CONFIGURATION

### Initial Setup
1. Create Plex account (free)
2. Claim server (link to account)
3. Add libraries:
   - Movies: /movies
   - TV Shows: /tv
   - Music: /music
4. Configure remote access (port forward 32400 on router)

### Media Organization
```
/media/
├── movies/
│   ├── Avatar (2009)/
│   │   └── Avatar (2009).mkv
│   └── Inception (2010)/
│       └── Inception (2010).mp4
├── tv/
│   ├── Breaking Bad/
│   │   ├── Season 01/
│   │   │   ├── Breaking Bad - S01E01.mkv
│   │   │   └── Breaking Bad - S01E02.mkv
│   │   └── Season 02/
│   └── Game of Thrones/
└── music/
    ├── Artist Name/
    │   └── Album Name/
    │       ├── 01 - Track Name.mp3
    │       └── 02 - Track Name.mp3
```

### Hardware Transcoding (NVIDIA GPU)
```bash
# Requires Plex Pass

# Pass GPU to Plex VM
# In Proxmox:
qm set 101 -hostpci0 83:00.0,pcie=1

# Install NVIDIA drivers in VM
sudo apt install nvidia-driver-535

# Enable hardware transcoding in Plex:
# Settings → Transcoder → Use hardware acceleration when available
# Select NVIDIA NVENC
```

## JELLYFIN (FREE ALTERNATIVE)

### Installation
```bash
# Docker
docker run -d \
  --name=jellyfin \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=America/New_York \
  -p 8096:8096 \
  -v ~/jellyfin/config:/config \
  -v ~/jellyfin/media:/media \
  --restart unless-stopped \
  jellyfin/jellyfin

# Access: http://<VM101_IP>:8096
```

## AUTOMATION WITH *ARR STACK

### Sonarr (TV Show Automation)
```bash
# Docker
docker run -d \
  --name=sonarr \
  -e PUID=1000 \
  -e PGID=1000 \
  -p 8989:8989 \
  -v ~/sonarr/config:/config \
  -v ~/plex/media/tv:/tv \
  -v ~/downloads:/downloads \
  --restart unless-stopped \
  linuxserver/sonarr

# Access: http://<VM101_IP>:8989
```

### Radarr (Movie Automation)
```bash
# Docker
docker run -d \
  --name=radarr \
  -e PUID=1000 \
  -e PGID=1000 \
  -p 7878:7878 \
  -v ~/radarr/config:/config \
  -v ~/plex/media/movies:/movies \
  -v ~/downloads:/downloads \
  --restart unless-stopped \
  linuxserver/radarr

# Access: http://<VM101_IP>:7878
```

### Lidarr (Music Automation)
```bash
# Docker
docker run -d \
  --name=lidarr \
  -e PUID=1000 \
  -e PGID=1000 \
  -p 8686:8686 \
  -v ~/lidarr/config:/config \
  -v ~/plex/media/music:/music \
  -v ~/downloads:/downloads \
  --restart unless-stopped \
  linuxserver/lidarr

# Access: http://<VM101_IP>:8686
```

### Prowlarr (Indexer Manager)
```bash
# Docker
docker run -d \
  --name=prowlarr \
  -e PUID=1000 \
  -e PGID=1000 \
  -p 9696:9696 \
  -v ~/prowlarr/config:/config \
  --restart unless-stopped \
  linuxserver/prowlarr

# Access: http://<VM101_IP>:9696
```

## DOWNLOAD CLIENTS

### Transmission (BitTorrent)
```bash
# Docker
docker run -d \
  --name=transmission \
  -e PUID=1000 \
  -e PGID=1000 \
  -p 9091:9091 \
  -p 51413:51413 \
  -p 51413:51413/udp \
  -v ~/transmission/config:/config \
  -v ~/downloads:/downloads \
  --restart unless-stopped \
  linuxserver/transmission

# Access: http://<VM101_IP>:9091
```

### qBittorrent (Alternative)
```bash
docker run -d \
  --name=qbittorrent \
  -e PUID=1000 \
  -e PGID=1000 \
  -p 8080:8080 \
  -p 6881:6881 \
  -p 6881:6881/udp \
  -v ~/qbittorrent/config:/config \
  -v ~/downloads:/downloads \
  --restart unless-stopped \
  linuxserver/qbittorrent

# Access: http://<VM101_IP>:8080
```

## COMPLETE DOCKER COMPOSE STACK

### docker-compose.yml
```yaml
version: '3.8'

services:
  plex:
    image: plexinc/pms-docker
    container_name: plex
    network_mode: host
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
      - VERSION=docker
    volumes:
      - ./plex/config:/config
      - ./media/tv:/tv
      - ./media/movies:/movies
      - ./media/music:/music
    restart: unless-stopped

  sonarr:
    image: linuxserver/sonarr
    container_name: sonarr
    environment:
      - PUID=1000
      - PGID=1000
    ports:
      - 8989:8989
    volumes:
      - ./sonarr/config:/config
      - ./media/tv:/tv
      - ./downloads:/downloads
    restart: unless-stopped

  radarr:
    image: linuxserver/radarr
    container_name: radarr
    environment:
      - PUID=1000
      - PGID=1000
    ports:
      - 7878:7878
    volumes:
      - ./radarr/config:/config
      - ./media/movies:/movies
      - ./downloads:/downloads
    restart: unless-stopped

  prowlarr:
    image: linuxserver/prowlarr
    container_name: prowlarr
    environment:
      - PUID=1000
      - PGID=1000
    ports:
      - 9696:9696
    volumes:
      - ./prowlarr/config:/config
    restart: unless-stopped

  transmission:
    image: linuxserver/transmission
    container_name: transmission
    environment:
      - PUID=1000
      - PGID=1000
    ports:
      - 9091:9091
      - 51413:51413
      - 51413:51413/udp
    volumes:
      - ./transmission/config:/config
      - ./downloads:/downloads
    restart: unless-stopped

  overseerr:
    image: linuxserver/overseerr
    container_name: overseerr
    environment:
      - PUID=1000
      - PGID=1000
    ports:
      - 5055:5055
    volumes:
      - ./overseerr/config:/config
    restart: unless-stopped
```

### Launch Stack
```bash
docker-compose up -d
```

## OVERSEERR (REQUEST MANAGEMENT)

### What is Overseerr?
- User-friendly interface for requesting movies/TV shows
- Integrates with Plex, Sonarr, Radarr
- Approval workflows for family/friends

### Setup
1. Access: http://<VM101_IP>:5055
2. Connect to Plex server
3. Add Sonarr and Radarr instances
4. Configure user permissions
5. Share with family/friends

## STREAMFORGE PROJECT

### StreamForge Goals (from GitHub repo)
1. **Automated Media Management**: Sonarr, Radarr, Lidarr
2. **Quality Control**: Automatic upgrade to 1080p/4K
3. **Subtitle Management**: Bazarr for multi-language subtitles
4. **Remote Access**: Reverse proxy (Nginx/Traefik) with SSL
5. **User Management**: Overseerr for request handling
6. **Monitoring**: Tautulli for Plex analytics

### Bazarr (Subtitle Automation)
```bash
docker run -d \
  --name=bazarr \
  -e PUID=1000 \
  -e PGID=1000 \
  -p 6767:6767 \
  -v ~/bazarr/config:/config \
  -v ~/media:/media \
  --restart unless-stopped \
  linuxserver/bazarr

# Access: http://<VM101_IP>:6767
```

### Tautulli (Plex Analytics)
```bash
docker run -d \
  --name=tautulli \
  -e PUID=1000 \
  -e PGID=1000 \
  -p 8181:8181 \
  -v ~/tautulli/config:/config \
  --restart unless-stopped \
  linuxserver/tautulli

# Access: http://<VM101_IP>:8181
```

## REVERSE PROXY (NGINX + SSL)

### Nginx Configuration
```nginx
# /etc/nginx/sites-available/plex.lightspeedup.com
server {
    listen 80;
    server_name plex.lightspeedup.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name plex.lightspeedup.com;

    ssl_certificate /etc/letsencrypt/live/plex.lightspeedup.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/plex.lightspeedup.com/privkey.pem;

    location / {
        proxy_pass http://localhost:32400;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Let's Encrypt SSL
```bash
sudo certbot --nginx -d plex.lightspeedup.com
```

## REMOTE ACCESS

### Plex Remote Access
1. Plex Settings → Remote Access
2. Enable "Manually specify public port": 32400
3. Forward port 32400 on router to Plex server IP
4. Test connection

### VPN Access (Secure Alternative)
- WireGuard or OpenVPN on Proxmox
- Access Plex via VPN (no port forwarding needed)

## STORAGE OPTIMIZATION

### RAID Configuration
```bash
# Check Dell R730 RAID status
sudo megacli -LDInfo -Lall -aALL

# Expand storage with additional drives
# Use RAID 5 or RAID 10 for redundancy
```

### ZFS (Advanced)
```bash
# Install ZFS on Proxmox
apt install zfsutils-linux

# Create ZFS pool
zpool create mediapool raidz sdb sdc sdd

# Mount in VM
qm set 101 -mp0 /mediapool,mp=/mnt/media
```

## PERFORMANCE TUNING

### Transcoding Optimization
- Use hardware transcoding (NVIDIA GPU)
- Disable transcoding for direct play (Settings → Network → LAN bandwidth: Original quality)
- Pre-transcode with Tdarr

### Network Optimization
- Use wired Ethernet (not Wi-Fi) for server
- Enable jumbo frames (MTU 9000) on gigabit network
- QoS on router (prioritize Plex traffic)

## MONETIZATION (LEGAL CONSIDERATIONS)

### Personal Use Only
- Plex is for **personal media only**
- Sharing with family/friends in same household is OK
- Public streaming or charging for access is **ILLEGAL**

### Legal Alternatives
1. **Plex Channels**: Create educational/original content
2. **YouTube**: Stream gaming, tutorials
3. **Twitch**: Live streaming
4. **Patreon**: Support for content creation

## BACKUP STRATEGY

### Automated Backups
```bash
#!/bin/bash
# backup-plex.sh
DATE=$(date +%Y%m%d)
tar -czf /backup/plex-config-$DATE.tar.gz ~/plex/config
rsync -av ~/media /backup/media-mirror/
```

### Cloud Backup
- Backblaze B2 (cheap cloud storage)
- rclone for automated sync

## LEARNING RESOURCES

- Plex Support: support.plex.tv
- r/PleX: reddit.com/r/PleX
- TRaSH Guides: trash-guides.info (quality profiles, naming)
- StreamForge GitHub: github.com/YourUsername/StreamForge

## STREAMFORGE DEPLOYMENT CHECKLIST

✅ Install Plex/Jellyfin  
✅ Configure GPU transcoding  
✅ Deploy Sonarr, Radarr, Lidarr  
✅ Setup Prowlarr (indexers)  
✅ Install download client (Transmission/qBittorrent)  
✅ Deploy Overseerr (request management)  
✅ Configure Bazarr (subtitles)  
✅ Setup Tautulli (analytics)  
✅ Reverse proxy with SSL  
✅ Automated backups  

**Complete Plex & StreamForge guide for SHENRON - Dell R730 optimized**

