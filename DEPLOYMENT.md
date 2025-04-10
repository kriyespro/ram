# RamJaap Deployment Guide

This guide provides instructions for deploying the RamJaap application to a production environment.

## System Requirements

- Python 3.12
- PostgreSQL
- Node.js and npm (for Tailwind CSS)

## 1. Clone the Repository

```bash
git clone [your-repository-url]
cd ramjaap
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Set Up the Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Django settings
SECRET_KEY=your-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database settings
DATABASE_URL=postgres://username:password@localhost:5432/ramjaap

# Email settings (optional)
EMAIL_HOST=smtp.yourprovider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
```

## 5. Set Up PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE ramjaap;
CREATE USER ramjaap_user WITH PASSWORD 'secure-password';
GRANT ALL PRIVILEGES ON DATABASE ramjaap TO ramjaap_user;
```

## 6. Compile Tailwind CSS

```bash
python manage.py tailwind install
python manage.py tailwind build
```

## 7. Collect Static Files

```bash
python manage.py collectstatic --no-input
```

## 8. Run Migrations

```bash
python manage.py migrate
```

## 9. Create a Superuser

```bash
python manage.py createsuperuser
```

## 10. Production Server Setup

### Using Gunicorn

```bash
gunicorn ramjaap.wsgi:application --bind 0.0.0.0:8000
```

### Using Systemd Service (Linux)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/ramjaap.service
```

Add the following content:

```ini
[Unit]
Description=RamJaap Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/ramjaap
ExecStart=/path/to/ramjaap/venv/bin/gunicorn --access-logfile - --workers 3 --bind 0.0.0.0:8000 ramjaap.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Start and enable the service:

```bash
sudo systemctl start ramjaap
sudo systemctl enable ramjaap
```

## 11. Nginx Configuration (recommended)

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/ramjaap;
    }
    
    location /media/ {
        root /path/to/ramjaap;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://localhost:8000;
    }
}
```

## 12. SSL Configuration (recommended)

Use Certbot to obtain and configure SSL certificates:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## 13. Maintenance

### Database Backups

```bash
pg_dump -U ramjaap_user ramjaap > ramjaap_backup_$(date +%Y-%m-%d).sql
```

### Updating the Application

```bash
cd /path/to/ramjaap
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py tailwind build
sudo systemctl restart ramjaap
```

## Troubleshooting

1. Check the application logs:
   ```bash
   sudo journalctl -u ramjaap.service
   ```

2. Check the Nginx logs:
   ```bash
   sudo tail -f /var/log/nginx/access.log
   sudo tail -f /var/log/nginx/error.log
   ```

3. Test the Gunicorn configuration:
   ```bash
   cd /path/to/ramjaap
   source venv/bin/activate
   gunicorn --check-config ramjaap.wsgi:application
   ``` 