#!/usr/bin/env bash
# ==============================================================================
# Auralytix EC2 Deployment Script (Ubuntu 22.04 LTS Free Tier)
# Automates Nginx, HTTPS SSL Certificate, Python Virtualenv, and Systemd Daemon
# ==============================================================================
set -e

DOMAIN_OR_IP="${1:-}"

echo "============================================================"
echo "    Deploying Auralytix Production Backend on Amazon EC2    "
echo "============================================================"

# 1. Update OS and install prerequisites
echo "[1/6] Updating system packages & installing Nginx + Certbot..."
sudo apt-get update -y
sudo apt-get install -y python3-pip python3-venv nginx certbot python3-certbot-nginx git curl

# 2. Setup project folder and virtual environment
APP_DIR="/home/ubuntu/auralytix"
echo "[2/6] Setting up project in $APP_DIR..."
sudo mkdir -p "$APP_DIR"
sudo chown -R ubuntu:ubuntu "$APP_DIR"

cd "$APP_DIR"
if [ ! -d "venv" ]; then
    echo "Creating Python virtualenv..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
fi

# 3. Setup Systemd Service
echo "[3/6] Configuring systemd background service..."
sudo cp deploy/auralytix.service /etc/systemd/system/auralytix.service
sudo systemctl daemon-reload
sudo systemctl enable auralytix
sudo systemctl restart auralytix

# 4. Configure HTTPS SSL & Nginx
echo "[4/6] Setting up HTTPS & Nginx..."
sudo mkdir -p /etc/letsencrypt/live/auralytix

if [ -n "$DOMAIN_OR_IP" ] && [[ "$DOMAIN_OR_IP" == *"."* ]] && [[ "$DOMAIN_OR_IP" != *"localhost"* ]]; then
    echo "Acquiring trusted SSL Certificate via Let's Encrypt for $DOMAIN_OR_IP..."
    sudo certbot --nginx -d "$DOMAIN_OR_IP" --non-interactive --agree-tos --register-unsafely-without-email || true
else
    echo "Generating high-security self-signed TLS SSL certificate for EC2 HTTPS..."
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/letsencrypt/live/auralytix/privkey.pem \
        -out /etc/letsencrypt/live/auralytix/fullchain.pem \
        -subj "/CN=auralytix.local/O=Auralytix/C=US"
fi

sudo cp deploy/nginx.conf /etc/nginx/sites-available/auralytix
sudo ln -sf /etc/nginx/sites-available/auralytix /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# 5. Verify local health
echo "[5/6] Verifying service health..."
sleep 3
curl -k -s https://127.0.0.1/cloud/status | grep -q "Amazon Web Services" && echo "✅ HTTPS API is online & healthy!" || echo "⚠️ Service starting, check journalctl -u auralytix -f"

echo "============================================================"
echo "    Auralytix EC2 Deployment Complete!                      "
echo "    Access via HTTPS: https://<your-ec2-public-ip-or-domain> "
echo "============================================================"
