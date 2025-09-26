# Deployment Runbook

## Prereqs
- Ubuntu 22.04+ VPS (Hetzner)
- Domain pointing to VPS IP
- Docker optional (backend can run via systemd or container)

## Environment
- Copy `.env` to server and set required keys
- Expose API on 127.0.0.1:8000 (gunicorn/uvicorn)

## Reverse Proxy (Nginx + HTTPS)
On the server (Ubuntu):
```bash
apt-get update -y && apt-get install -y nginx certbot python3-certbot-nginx
# Render nginx config similar to deploy/nginx/nginx.conf
# Obtain cert
certbot --nginx -d your.domain.com --non-interactive --agree-tos -m admin@your.domain.com --redirect
systemctl enable certbot.timer && systemctl start certbot.timer
```
Ensure:
- `https://your.domain.com/health` returns 200
- Logs are rotating in `/var/log/nginx`

## Backend as a service
Example systemd unit (uvicorn):
```ini
[Unit]
Description=Polymarket Edge API
After=network.target

[Service]
WorkingDirectory=/opt/polymarket/backend
EnvironmentFile=/opt/polymarket/.env
ExecStart=/opt/polymarket/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
User=www-data
Group=www-data

[Install]
WantedBy=multi-user.target
```
