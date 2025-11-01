# 🚀 Deployment Guide

## Quick Deploy to Render.com (Recommended)

### Step 1: Prepare Repository
```bash
cd "c:\Users\asus\Desktop\internship project\our_voice_app"
git init
git add .
git commit -m "Initial commit - MGNREGA MVP"
```

### Step 2: Push to GitHub
```bash
# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/mgnrega-app.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `mgnrega-tracker`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free tier is fine for MVP

5. Add Environment Variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-random-string>
   DATA_GOV_API_KEY=<your-api-key>
   ```

6. Click "Create Web Service"
7. Wait 2-3 minutes for deployment
8. Your app will be live at: `https://mgnrega-tracker.onrender.com`

## Alternative: Railway.app

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway init
railway up
```

## Alternative: Heroku

```bash
# Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create mgnrega-tracker

# Push code
git push heroku main

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATA_GOV_API_KEY=your-api-key

# Open app
heroku open
```

## Manual VPS Deployment (Ubuntu 22.04)

### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Install PostgreSQL (optional)
sudo apt install postgresql postgresql-contrib -y
```

### Step 2: Application Setup
```bash
# Create app directory
sudo mkdir -p /var/www/mgnrega
cd /var/www/mgnrega

# Clone repository
sudo git clone https://github.com/YOUR_USERNAME/mgnrega-app.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
sudo nano .env
# Add your environment variables
```

### Step 3: Gunicorn Setup
```bash
# Test Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Create systemd service
sudo nano /etc/systemd/system/mgnrega.service
```

Add this content:
```ini
[Unit]
Description=MGNREGA Flask Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/mgnrega
Environment="PATH=/var/www/mgnrega/venv/bin"
ExecStart=/var/www/mgnrega/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable mgnrega
sudo systemctl start mgnrega
sudo systemctl status mgnrega
```

### Step 4: Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/mgnrega
```

Add this content:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/mgnrega/static;
        expires 30d;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/mgnrega /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## Post-Deployment Checklist

- [ ] Test the live URL
- [ ] Check all 75 districts load
- [ ] Test on mobile device
- [ ] Verify geolocation works
- [ ] Check error handling (disconnect internet)
- [ ] Monitor logs for errors
- [ ] Set up uptime monitoring
- [ ] Add to your resume/portfolio!

## Monitoring Setup

### Uptime Robot (Free)
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Add monitor for your URL
3. Set check interval: 5 minutes
4. Add email alerts

### Sentry (Error Tracking)
```bash
pip install sentry-sdk[flask]
```

Add to `app.py`:
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
)
```

## Troubleshooting

### App won't start
```bash
# Check logs
sudo journalctl -u mgnrega -f

# Test manually
cd /var/www/mgnrega
source venv/bin/activate
python app.py
```

### Database errors
```bash
# Reset database
rm mgnrega_cache.db
python app.py  # Will recreate with fresh schema
```

### Nginx errors
```bash
# Check configuration
sudo nginx -t

# View error logs
sudo tail -f /var/log/nginx/error.log
```

### Port already in use
```bash
# Find process using port 5000
sudo lsof -i :5000
# Kill it
sudo kill -9 <PID>
```

## Performance Tips

1. **Enable caching**: Add Redis for API responses
2. **CDN**: Use Cloudflare for static assets
3. **Compression**: Enable gzip in Nginx
4. **Database**: Upgrade to PostgreSQL for production
5. **Workers**: Scale Gunicorn workers based on CPU cores

## Success Metrics to Track

- Daily active users
- Most viewed districts
- API success rate
- Average load time
- Mobile vs desktop usage
- Error rates

---

**🎉 You're ready to deploy! Choose your platform and go live!**
