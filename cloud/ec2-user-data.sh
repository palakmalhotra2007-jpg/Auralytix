#!/bin/bash
# ==============================================================================
# Auralytix AWS EC2 Automated Provisioning and Deployment Script
# Compatible with Amazon Linux 2023, Amazon Linux 2, Ubuntu 22.04 / 24.04 LTS
# Free Tier Architecture: EC2 (t2.micro / t3.micro), S3 (boto3), RDS PostgreSQL
# ==============================================================================

set -euo pipefail

echo "=================================================="
echo " Starting Auralytix Cloud Deployment on AWS EC2"
echo " Date: $(date)"
echo "=================================================="

# 1. Detect OS and install Docker + Git
if command -v dnf &> /dev/null; then
    echo "[1/5] Detected Amazon Linux / RHEL / Fedora (dnf)"
    dnf update -y
    dnf install -y docker git curl
elif command -v apt-get &> /dev/null; then
    echo "[1/5] Detected Ubuntu / Debian (apt)"
    apt-get update -y
    apt-get install -y docker.io docker-compose-v2 git curl
fi

# 2. Enable and Start Docker Daemon
echo "[2/5] Starting and enabling Docker daemon..."
systemctl enable --now docker
if id "ec2-user" &>/dev/null; then
    usermod -aG docker ec2-user
elif id "ubuntu" &>/dev/null; then
    usermod -aG docker ubuntu
fi

# 3. Ensure Docker Compose is installed
if ! docker compose version &>/dev/null; then
    echo "[3/5] Installing Docker Compose CLI plugin..."
    DOCKER_CONFIG=${DOCKER_CONFIG:-/usr/local/lib/docker}
    mkdir -p $DOCKER_CONFIG/cli-plugins
    curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
    chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
fi

# 4. Clone or pull repository
APP_DIR="/opt/auralytix"
echo "[4/5] Setting up deployment directory at ${APP_DIR}..."
if [ -d "${APP_DIR}/.git" ]; then
    echo "Updating existing repository..."
    cd "${APP_DIR}"
    git pull origin main || true
else
    echo "Cloning Auralytix repository from GitHub..."
    git clone https://github.com/palakmalhotra2007-jpg/Auralytix.git "${APP_DIR}"
    cd "${APP_DIR}"
fi

# Ensure default environment variables exist if not present
if [ ! -f ".env" ]; then
    cat << 'EOF' > .env
DATABASE_URL=postgresql://auralytix_user:auralytix_secure_password@postgres:5432/auralytix_db
AWS_S3_BUCKET=auralytix-cloud-artifacts
AWS_REGION=us-east-1
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=auralytix_knowledge
EOF
fi

# 5. Launch containers via Docker Compose
echo "[5/5] Launching Auralytix Full-Stack Containers (Nginx, React SPA, FastAPI, Qdrant)..."
docker compose up -d --build

PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 || echo 'localhost')

echo "=================================================="
echo " Auralytix Cloud Deployment Complete!"
echo " Frontend URL: http://${PUBLIC_IP}"
echo " Backend API:  http://${PUBLIC_IP}:8000/docs"
echo "=================================================="
