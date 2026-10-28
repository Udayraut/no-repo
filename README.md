# Skyniya Growth OS 🚀
> **Production-Ready, Premium Social Media Management & Growth Tracking SaaS**
> Built with Django 4.2+, Python 3.10+, PostgreSQL, Bootstrap 5, Chart.js, HTML5, CSS3, and Google OAuth 2.0.

---

## 🌟 Executive Overview
**Skyniya Growth OS** is a minimal, Apple-inspired growth operating system tailored for creators, growth marketers, and SaaS founders. It streamlines social post scheduling, daily content logging, multi-platform view/engagement analytics, Google Play Store conversion tracking, and deadline-driven goal milestones.

### ✨ Key Capabilities
* **Minimalist Apple-Inspired Design System**: Clean typography (Inter font), whitespace, rounded cards, refined badge indicators, and restrained color accents.
* **Social Media Content Tracker (CRUD)**: Draft, schedule, and log published posts across Instagram, YouTube, Twitter / X, TikTok, LinkedIn, and Facebook.
* **Views & Engagement Metrics**: Record multi-date engagement snapshots (views, likes, comments, shares, saves, clicks, reach, impressions, calculated engagement rates).
* **Clear Metric Source Separation**: Strictly distinguishes **Manual Entry** (`MANUAL`) from **API Synchronized** (`API_SYNC`) metrics across all dashboards and reports.
* **Google Play Store Funnel**: Track store listing visitors, acquisitions (installs), uninstalls, active devices, store ratings, and automated conversion rate calculations.
* **Configurable Growth Goals**: Track numerical targets, automated percentage completion calculations, deadline countdowns, and overdue alerts.
* **Interactive Calendar**: Visual monthly view of scheduled content, published posts, and daily production logs.
* **Daily Content Logger**: Productivity scoring (1-5 stars), hours spent, outputs produced, and qualitative reflection logs.
* **Enterprise Reports & Export**: One-click download of all posts, Play Store metrics, and daily logs to **CSV** and native Microsoft **Excel (.xlsx)**.
* **Google OAuth 2.0 & Email Auth**: Seamless sign-in powered by maintained `django-allauth`.
* **In-App Notification Center**: Milestone alerts, deadline reminders, and global unread counter in navbar and sidebar.

---

## 🏛 Architecture & Project Structure

```text
skyniya/
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
├── skyniya/                   # Project Core & Configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py            # Shared settings, apps, middleware, allauth
│       ├── development.py     # Local dev SQLite settings
│       └── production.py      # Production PostgreSQL, SSL, Whitenoise, HSTS
├── accounts/                  # User profile, preferences, Google SSO
│   ├── models.py              # UserProfile & preferences
│   ├── views.py               # Profile & settings
│   ├── forms.py
│   ├── signals.py
│   ├── urls.py
│   └── tests.py
├── tracker/                   # Social posts, metrics, daily logs & calendar
│   ├── models.py              # SocialPost, PostMetric, DailyLog
│   ├── views.py               # Post CRUD, metric snapshots, daily tracker, calendar
│   ├── forms.py
│   ├── urls.py
│   └── tests.py
├── analytics/                 # Play Store metrics & growth goals
│   ├── models.py              # PlayStoreMetric, GrowthGoal
│   ├── views.py               # Overview, PlayStore tracking, Goal milestones
│   ├── forms.py
│   ├── urls.py
│   └── tests.py
├── dashboard/                 # SaaS central command center & KPIs
│   ├── views.py               # Executive KPIs & custom 404/500 handlers
│   ├── urls.py
│   └── tests.py
├── reports/                   # CSV and Excel (.xlsx) export engine
│   ├── views.py               # Export handlers (openpyxl & csv)
│   ├── urls.py
│   └── tests.py
├── notifications/             # Milestone alerts & notification badges
│   ├── models.py              # Notification
│   ├── context_processors.py  # Global unread count
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── templates/                 # Bootstrap 5 minimalist templates
│   ├── base.html              # Apple-inspired master layout
│   ├── 404.html & 500.html    # Custom branded error pages
│   ├── includes/              # Sidebar, navbar, messages, pagination
│   ├── accounts/
│   ├── tracker/
│   ├── analytics/
│   ├── dashboard/
│   ├── reports/
│   └── notifications/
└── static/
    ├── css/style.css          # Custom minimalist Apple CSS system
    └── js/app.js              # Chart.js integration & interaction scripts
```

---

## 🛠 Local Setup Instructions (Step-by-Step)

### 1. Prerequisites
* Python 3.10+ installed
* Git

### 2. Clone and Create Virtual Environment
```bash
# Clone the repository
git clone <your-repo-url> skyniya
cd skyniya

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
For local development, the default values in `skyniya.settings.development` use a local SQLite database automatically.

### 5. Run Database Migrations
```bash
python manage.py makemigrations accounts tracker analytics notifications
python manage.py migrate
```

### 6. Create Superuser (Admin Access)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser. You will be prompted to log in or create an account. Admin panel is available at `http://127.0.0.1:8000/admin/`.

---

## 🌐 Google OAuth 2.0 Configuration

Skyniya Growth OS uses standard, robust `django-allauth` for Google Authentication.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project: `Skyniya Growth OS`.
3. Under **APIs & Services** > **OAuth Consent Screen**:
   * User Type: **External**
   * App name: `Skyniya Growth OS`
   * Scopes: `.../auth/userinfo.email`, `.../auth/userinfo.profile`
4. Under **APIs & Services** > **Credentials**:
   * Click **Create Credentials** > **OAuth Client ID**.
   * Application type: **Web application**.
   * Authorized redirect URIs:
     * Development: `http://localhost:8000/accounts/google/login/callback/` and `http://127.0.0.1:8000/accounts/google/login/callback/`
     * Production: `https://yourdomain.com/accounts/google/login/callback/`
5. Copy your **Client ID** and **Client Secret** into `.env`:
   ```env
   GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   ```

---

## 🚀 Production Deployment & PostgreSQL Configuration

### 1. PostgreSQL Database Setup
```sql
CREATE DATABASE skyniya_db;
CREATE USER skyniya_user WITH ENCRYPTED PASSWORD 'StrongProductionPassword';
GRANT ALL PRIVILEGES ON DATABASE skyniya_db TO skyniya_user;
ALTER DATABASE skyniya_db OWNER TO skyniya_user;
```

### 2. Production `.env` Settings
Set the following environment variables:
```env
DJANGO_SETTINGS_MODULE=skyniya.settings.production
SECRET_KEY=generate-a-strong-random-50-character-string
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

DB_NAME=skyniya_db
DB_USER=skyniya_user
DB_PASSWORD=StrongProductionPassword
DB_HOST=localhost
DB_PORT=5432

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 3. Static Files & Production Migrations
```bash
python manage.py collectstatic --noinput
python manage.py migrate
```

### 4. Running with Gunicorn & Systemd
Sample Gunicorn systemd unit file (`/etc/systemd/system/skyniya.service`):
```ini
[Unit]
Description=Skyniya Growth OS Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/skyniya
ExecStart=/var/www/skyniya/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/skyniya.sock skyniya.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 5. Nginx Reverse Proxy Configuration
```nginx
server {
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/skyniya;
    }
    location /media/ {
        root /var/www/skyniya;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/skyniya.sock;
    }

    listen 443 ssl http2;
    # SSL certificates handled via Certbot / Let's Encrypt
}
```

---

## 💾 Automated Database Backups Guidance

To safeguard user content and metrics, configure an automated daily PostgreSQL dump with retention pruning:

```bash
#!/bin/bash
# Backup script: /usr/local/bin/backup_skyniya.sh
BACKUP_DIR="/var/backups/skyniya"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
mkdir -p "$BACKUP_DIR"

# Dump database
pg_dump -U skyniya_user -h localhost skyniya_db | gzip > "$BACKUP_DIR/skyniya_db_$TIMESTAMP.sql.gz"

# Retain last 30 days of backups
find "$BACKUP_DIR" -type f -name "*.sql.gz" -mtime +30 -exec rm {} \;
```
Add to crontab (`crontab -e`):
```cron
0 2 * * * /usr/local/bin/backup_skyniya.sh
```

---

## 🧪 Automated Tests

Run the full automated test suite covering all modules:
```bash
python manage.py test accounts tracker analytics dashboard reports notifications
```

---

## 🔒 Security Best Practices Implemented
* Strict CSRF validation on all POST requests.
* User isolation: All models querysets are scoped to `request.user`.
* No secrets hardcoded in source code; managed via `.env`.
* Password hashing with Django PBKDF2 with SHA256.
* Full HTTPS, HSTS, Secure Cookies, and Clickjacking protection in production.
* Manual metrics and API-synced metrics clearly isolated and tagged.
#   n o - r e p o  
 #   n o - r e p o  
 