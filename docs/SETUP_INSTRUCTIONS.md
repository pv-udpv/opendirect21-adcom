# Production Deployment Guide

## Prerequisites

- Ubuntu/Debian Linux or macOS
- Python 3.12+
- PostgreSQL 14+ (optional, for production DB)
- Docker (optional)
- Nginx or Apache (optional, for reverse proxy)

## Method 1: Systemd Service (Recommended for Linux)

### 1. Install dependencies

```bash
sudo apt-get update
sudo apt-get install python3.12 python3.12-venv python3-pip git -y
```

### 2. Create application user

```bash
sudo useradd -m -s /bin/bash opendirect
sudo su - opendirect
```

### 3. Clone and setup

```bash
git clone https://github.com/pv-udpv/opendirect21-adcom.git
cd opendirect21-adcom
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Create systemd service file

```bash
sudo tee /etc/systemd/system/opendirect21.service > /dev/null <<EOF
[Unit]
Description=OpenDirect 2.1 + Adcom v1.0 API Server
After=network.target

[Service]
Type=notify
User=opendirect
WorkingDirectory=/home/opendirect/opendirect21-adcom
Environment="PATH=/home/opendirect/opendirect21-adcom/venv/bin"
Environment="PYTHONPATH=/home/opendirect/opendirect21-adcom"
ExecStart=/home/opendirect/opendirect21-adcom/venv/bin/uvicorn opendirect21.main:app --host 0.0.0.0 --port 8000 --workers 4
ExecReload=/bin/kill -HUP \$MAINPID
KillMode=mixed
KillSignal=SIGTERM
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF
```

### 5. Enable and start service

```bash
sudo systemctl daemon-reload
sudo systemctl enable opendirect21
sudo systemctl start opendirect21
sudo systemctl status opendirect21
```

### 6. View logs

```bash
sudo journalctl -u opendirect21 -f
```

## Method 2: Docker (Recommended for any OS)

### 1. Build image

```bash
docker build -t opendirect21-adcom:latest .
```

### 2. Run container

```bash
docker run -d \
  --name opendirect21 \
  -p 8000:8000 \
  -e LOG_LEVEL=INFO \
  opendirect21-adcom:latest
```

### 3. With docker-compose

```bash
docker-compose up -d
```

### 4. View logs

```bash
docker logs -f opendirect21
```

## Method 3: Nginx Reverse Proxy

### 1. Install Nginx

```bash
sudo apt-get install nginx -y
```

### 2. Create Nginx config

```bash
sudo tee /etc/nginx/sites-available/opendirect21 > /dev/null <<EOF
upstream opendirect21_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.example.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://opendirect21_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }

    # Cache static OpenAPI docs
    location ~ ^/(docs|redoc|openapi.json)$ {
        proxy_pass http://opendirect21_app;
        proxy_cache_valid 200 1h;
        proxy_cache_key "\$scheme\$host\$request_uri";
    }
}
EOF
```

### 3. Enable site

```bash
sudo ln -s /etc/nginx/sites-available/opendirect21 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## PostgreSQL Setup (Optional)

### 1. Install PostgreSQL

```bash
sudo apt-get install postgresql postgresql-contrib -y
```

### 2. Create database

```bash
sudo -u postgres psql <<EOF
CREATE DATABASE opendirect21;
CREATE USER opendirect WITH PASSWORD 'secure_password';
ALTER ROLE opendirect SET client_encoding TO 'utf8';
ALTER ROLE opendirect SET default_transaction_isolation TO 'read committed';
ALTER ROLE opendirect SET default_transaction_deferrable TO on;
ALTER ROLE opendirect SET default_transaction_level TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE opendirect21 TO opendirect;
EOF
```

### 3. Update .env

```bash
DATABASE_URL=postgresql+asyncpg://opendirect:secure_password@localhost/opendirect21
```

## SSL/TLS with Let's Encrypt

### 1. Install Certbot

```bash
sudo apt-get install certbot python3-certbot-nginx -y
```

### 2. Get certificate

```bash
sudo certbot --nginx -d api.example.com
```

### 3. Auto-renewal

```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## Monitoring & Alerts

### Health Check

```bash
# Manual check
curl http://localhost:8000/health

# Automated monitoring
*/5 * * * * curl -f http://localhost:8000/health || alert
```

### View Metrics

```bash
# CPU/Memory usage
top -p $(pgrep -f "uvicorn")

# Open connections
lsof -i :8000

# Disk usage
df -h /home/opendirect
```

## Backup & Recovery

### Backup data

```bash
# Manual backup
cd /home/opendirect/opendirect21-adcom
tar -czf backup-$(date +%Y%m%d).tar.gz data/ logs/

# Automated backup (cron)
0 2 * * * cd /home/opendirect/opendirect21-adcom && tar -czf backup-$(date +\%Y\%m\%d).tar.gz data/
```

### Database backup

```bash
pg_dump opendirect21 | gzip > backup.sql.gz
```

## Security Checklist

- [ ] Use strong database passwords
- [ ] Enable HTTPS with SSL/TLS
- [ ] Configure firewall (ufw, iptables)
- [ ] Disable unnecessary services
- [ ] Regular security updates: `sudo apt-get update && sudo apt-get upgrade`
- [ ] Monitor logs for suspicious activity
- [ ] Implement rate limiting
- [ ] Set strong SECRET_KEY in production
- [ ] Restrict CORS origins
- [ ] Use environment variables for secrets
- [ ] Enable audit logging

## Troubleshooting

### Service won't start

```bash
sudo systemctl start opendirect21
sudo journalctl -u opendirect21 -n 50  # Last 50 lines
```

### Connection refused

```bash
# Check if service is running
sudo systemctl status opendirect21

# Check ports
sudo netstat -tlnp | grep 8000

# Check firewall
sudo ufw status
sudo ufw allow 8000  # If needed
```

### High memory usage

```bash
# Restart service
sudo systemctl restart opendirect21

# Check for memory leaks
free -h
pgrep -f uvicorn
```

## Performance Tuning

### Increase workers

Edit `/etc/systemd/system/opendirect21.service`:

```bash
ExecStart=... --workers 8  # CPU cores * 2 + 1
```

### Database connection pool

Set in `.env`:

```bash
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
```

## Version Updates

```bash
cd /home/opendirect/opendirect21-adcom
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl restart opendirect21
```

## Support

For issues or questions:

1. Check logs: `sudo journalctl -u opendirect21 -f`
2. Check GitHub Issues: https://github.com/pv-udpv/opendirect21-adcom/issues
3. Review documentation: https://github.com/pv-udpv/opendirect21-adcom/tree/main/docs
