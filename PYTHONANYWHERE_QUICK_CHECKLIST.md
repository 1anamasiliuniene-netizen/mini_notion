# ⚡ PythonAnywhere Quick Reference Checklist

**Use this checklist during deployment to avoid errors**

---

## 🔴 CRITICAL - MUST DO

- [ ] Set `DJANGO_SECRET_KEY` to a new strong random value
- [ ] Set `DJANGO_DEBUG=0` (absolutely critical!)
- [ ] Set `DJANGO_ALLOWED_HOSTS` to your domain
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py collectstatic --noinput`

---

## 🟡 IMPORTANT - MUST DO

- [ ] Set `DJANGO_CSRF_TRUSTED_ORIGINS` to `https://yourdomain`
- [ ] Set `DJANGO_FORCE_SSL=1`
- [ ] Configure WSGI file (use provided template)
- [ ] Configure static files in Web settings
- [ ] Verify virtualenv path is correct

---

## 🟢 RECOMMENDED - SHOULD DO

- [ ] Set `NASA_API_KEY` to your own key (or leave as DEMO_KEY)
- [ ] Create superuser for admin panel
- [ ] Test health endpoint: `/health/`
- [ ] Test login page: `/login/`
- [ ] Monitor error logs for 24 hours

---

## 📋 Environment Variables (Copy-Paste)

```bash
DJANGO_SECRET_KEY=generate-new-value-here
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
DJANGO_FORCE_SSL=1
NASA_API_KEY=DEMO_KEY
```

---

## 📁 File Locations

After cloning to PythonAnywhere:

```
/home/yourusername/PythonProject38/
├── mysite/
│   ├── db.sqlite3 (will be created)
│   ├── staticfiles/ (created by collectstatic)
│   ├── media/
│   ├── mini_notion/
│   │   ├── templates/
│   │   ├── static/
│   │   └── models.py
│   ├── mysite/
│   │   ├── wsgi.py (use this)
│   │   └── settings.py
│   └── manage.py
├── requirements.txt
└── .env (create this from .env.example)
```

---

## 🔧 Essential Commands

### SSH Access
```bash
# These commands run in PythonAnywhere terminal/SSH

# Activate virtualenv
workon venv

# Run migrations
cd ~/PythonProject38/mysite
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser (optional)
python manage.py createsuperuser

# Test setup
python manage.py check
```

---

## 🎯 WSGI Configuration

Replace `/var/www/yourusername_pythonanywhere_com_wsgi.py` content with:

```python
import os
import sys

project_home = '/home/yourusername/PythonProject38'
if project_home not in sys.path:
    sys.path.append(project_home)

mysite_home = os.path.join(project_home, 'mysite')
if mysite_home not in sys.path:
    sys.path.append(mysite_home)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Don't forget to replace `yourusername`!**

---

## 🌐 Static Files in Web Settings

Add these in **Static files** section:

| URL | Directory |
|-----|-----------|
| /static/ | /home/yourusername/PythonProject38/mysite/staticfiles |
| /media/ | /home/yourusername/PythonProject38/mysite/media |

---

## ✅ Post-Deployment Tests

Run these in order:

1. **Health Check**
   ```
   GET https://yourusername.pythonanywhere.com/health/
   Expected: {"status": "ok"}
   ```

2. **Login Page**
   ```
   GET https://yourusername.pythonanywhere.com/login/
   Expected: Login form with CSRF token
   ```

3. **Dashboard** (after logging in)
   ```
   GET https://yourusername.pythonanywhere.com/dashboard/
   Expected: Dashboard with analytics
   ```

4. **NASA APOD**
   ```
   GET https://yourusername.pythonanywhere.com/integrations/nasa-apod/
   Expected: Form to select date and view APOD
   ```

---

## 🚨 If You Get 500 Error

1. **Check error log** in PythonAnywhere Web settings
2. **Look for:**
   - "no such table" → Run migrations
   - "TemplateDoesNotExist" → Verify files uploaded
   - "DisallowedHost" → Set ALLOWED_HOSTS
   - "DEBUG in production" → Set DEBUG=0
   - "SECRET_KEY" → Set DJANGO_SECRET_KEY
   - "static files" → Run collectstatic

3. **Click Reload** after each fix

---

## 💾 Backup Before Deployment

```bash
# Backup database
cp ~/PythonProject38/mysite/db.sqlite3 ~/db.sqlite3.backup

# Backup settings
cp ~/PythonProject38/mysite/mysite/settings.py ~/settings.py.backup
```

---

## 📞 Helpful Links

- [PythonAnywhere FAQ](https://help.pythonanywhere.com/)
- [Django Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [Your Error Logs](https://www.pythonanywhere.com/web_app_setup/)

---

## 🎯 Expected Outcome

After completing all steps:
- ✅ Domain accessible via HTTPS
- ✅ Login/signup working
- ✅ Dashboard loading with analytics
- ✅ NASA APOD integration working
- ✅ Static files (CSS/JS) loading
- ✅ No 500 errors in logs

---

**Remember: 80% of deployment issues are configuration-related, not code-related. You've got this!** 🚀

