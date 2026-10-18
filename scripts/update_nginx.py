import subprocess
import base64

conf = """# HTTP Server (Port 80)
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    root /var/www/auralytix;
    index index.html;

    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 256;
    gzip_types text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;

    location /assets/ {
        gzip_static on;
        expires 1y;
        add_header Cache-Control "public, no-transform, immutable";
        try_files $uri =404;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~ ^/(health|cloud|api|shap|policy|rag|rl) {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto http;
        proxy_read_timeout 120s;
        proxy_connect_timeout 60s;
    }
}

# HTTPS Server (Port 443)
server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
    server_name _;

    ssl_certificate /etc/letsencrypt/live/13.239.41.80.sslip.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/13.239.41.80.sslip.io/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    root /var/www/auralytix;
    index index.html;

    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 256;
    gzip_types text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;

    location /assets/ {
        gzip_static on;
        expires 1y;
        add_header Cache-Control "public, no-transform, immutable";
        try_files $uri =404;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~ ^/(health|cloud|api|shap|policy|rag|rl) {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_read_timeout 120s;
        proxy_connect_timeout 60s;
    }
}
"""

b64 = base64.b64encode(conf.encode('utf-8')).decode('utf-8')
cmd = f"echo '{b64}' | base64 -d | sudo tee /etc/nginx/sites-available/auralytix > /dev/null && sudo nginx -t && sudo systemctl reload nginx"
res = subprocess.run(['ssh.exe', '-i', r'F:\Downloads\auralytix-key.pem', '-o', 'StrictHostKeyChecking=no', 'ubuntu@13.239.41.80', cmd], capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
print("CODE:", res.returncode)
