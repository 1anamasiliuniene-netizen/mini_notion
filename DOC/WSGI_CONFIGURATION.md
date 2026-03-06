# PythonAnywhere WSGI Configuration Guide

This guide explains how to properly configure your WSGI file for PythonAnywhere deployment.

## Steps to Configure WSGI

### 1. In PythonAnywhere Web App Settings

1. Go to **Web** in PythonAnywhere dashboard
2. Click on your web app
3. Scroll to **Code** section
4. Find **WSGI configuration file** 
5. Click the path (usually `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
6. Replace the entire content with the code below

### 2. WSGI Configuration File Content

```python
import os
import sys
from pathlib import Path

# Add your project directory to Python path
project_home = '/home/yourusername/PythonProject38'
if project_home not in sys.path:
    sys.path.append(project_home)

# Add mysite subdirectory to path
mysite_home = os.path.join(project_home, '../mysite')
if mysite_home not in sys.path:
    sys.path.append(mysite_home)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

# Get WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
```

**IMPORTANT:** Replace `yourusername` with your actual PythonAnywhere username!

### 3. Virtual Environment Configuration

1. In **Web** settings, scroll to **Virtualenv** section
2. Set virtualenv path to: `/home/yourusername/.virtualenvs/venv`
   (or whatever you named your virtual environment)

### 4. Environment Variables

**CRITICAL:** Set these in PythonAnywhere Web app settings (not in .env file):

```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
DJANGO_FORCE_SSL=1
NASA_API_KEY=DEMO_KEY
```

To add environment variables in PythonAnywhere:
1. Go to **Web** settings
2. Scroll to **Environment variables**
3. Click **Add a new variable**
4. Enter key and value for each variable above

### 5. Static Files Configuration

In **Web** settings, scroll to **Static files** section and add:

| URL | Directory |
|-----|-----------|
| /static/ | /home/yourusername/PythonProject38/mysite/staticfiles |
| /media/ | /home/yourusername/PythonProject38/mysite/media |

### 6. Reload Web App

After making all changes:
1. Click the green **Reload** button at the top of the Web settings page
2. Wait for it to show "Reloading..." then "Reloaded"

### 7. Test Your Application

Visit: `https://yourusername.pythonanywhere.com/health/`

Expected response:
```json
{"status": "ok"}
```

---

## Troubleshooting

### "500 Internal Server Error"

1. Check **Error log** in Web settings
2. Common issues:
   - Missing `DJANGO_SECRET_KEY` environment variable
   - `DJANGO_DEBUG=True` (set to 0)
   - Wrong `DJANGO_ALLOWED_HOSTS`
   - Database migrations not run

### "Forbidden CSRF token missing"

1. Ensure `DJANGO_CSRF_TRUSTED_ORIGINS` is set
2. Include `{% csrf_token %}` in all POST forms
3. Set `DJANGO_FORCE_SSL=1` for HTTPS

### "TemplateDoesNotExist"

1. Ensure all template files are uploaded
2. Check file path: `/home/yourusername/PythonProject38/mysite/mini_notion/templates/`
3. Run: `python manage.py check`

### "No such table"

1. SSH into PythonAnywhere
2. Run: `cd /home/yourusername/PythonProject38/mysite && python manage.py migrate`

### "Static files not loading"

1. SSH into PythonAnywhere
2. Run: `cd /home/yourusername/PythonProject38/mysite && python manage.py collectstatic --noinput`
3. Check **Static files** section in Web settings
4. Click **Reload**

---

## Detailed Setup Instructions

### From Command Line (PythonAnywhere SSH)

```bash
# 1. Navigate to home directory
cd ~

# 2. Clone or upload your code
git clone https://github.com/yourusername/PythonProject38.git

# 3. Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 venv

# 4. Install dependencies
cd PythonProject38
pip install -r requirements.txt

# 5. Run migrations
cd mysite
python manage.py migrate

# 6. Create superuser (optional)
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Test setup
python manage.py check
```

### In PythonAnywhere Web Settings

1. **Source code:** `/home/yourusername/PythonProject38`
2. **Working directory:** `/home/yourusername/PythonProject38`
3. **WSGI configuration file:** (use the code from section 2 above)
4. **Virtualenv:** `/home/yourusername/.virtualenvs/venv`
5. **Python version:** 3.10
6. **Environment variables:** (see section 4 above)
7. **Static files:**
   - URL: `/static/` → Directory: `/home/yourusername/PythonProject38/mysite/staticfiles`
   - URL: `/media/` → Directory: `/home/yourusername/PythonProject38/mysite/media`

---

## Security Checklist

- ✅ `DJANGO_DEBUG=0`
- ✅ `DJANGO_SECRET_KEY` is unique and strong
- ✅ `DJANGO_FORCE_SSL=1` (for HTTPS)
- ✅ `DJANGO_ALLOWED_HOSTS` configured
- ✅ `DJANGO_CSRF_TRUSTED_ORIGINS` configured
- ✅ Database backups enabled
- ✅ Error logs monitored

---

## Getting Help

- [PythonAnywhere FAQ](https://www.pythonanywhere.com/forums/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- Check your **Error log** in Web settings for detailed error messages

