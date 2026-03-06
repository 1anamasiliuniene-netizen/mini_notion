# ⚙️ Deployment Settings Configuration

**Date:** March 6, 2026  
**Status:** PRODUCTION-READY

---

## Settings.py Updates for Deployment

Your `settings.py` has been configured for both development and production environments.

### Key Features

#### 1. **Environment-Based Configuration**
All critical settings are controlled via environment variables:
- `DJANGO_SECRET_KEY` - Must be set in production
- `DJANGO_DEBUG` - Set to 0 for production
- `DJANGO_ALLOWED_HOSTS` - Your domain(s)
- `DJANGO_CSRF_TRUSTED_ORIGINS` - HTTPS origins
- `DJANGO_FORCE_SSL` - Enable HTTPS redirect

#### 2. **Smart Logging**
- **Development (DEBUG=1):** 
  - Verbose logging to console
  - Shows DEBUG and INFO messages
  - All logs visible in terminal

- **Production (DEBUG=0):**
  - Logs saved to file: `logs/django.log`
  - Only WARNING and ERROR logged
  - Less console spam
  - Better error tracking

#### 3. **Security Headers**
Automatically enabled when `DJANGO_FORCE_SSL=1`:
- HTTPS redirect (`SECURE_SSL_REDIRECT`)
- Secure cookies (`SESSION_COOKIE_SECURE`)
- CSRF secure cookies (`CSRF_COOKIE_SECURE`)
- HSTS headers
- Content type protection
- Referrer policy
- X-Frame options

#### 4. **Static Files**
- WhiteNoise middleware for serving static files
- CompressedManifestStaticFilesStorage for optimization
- Automatic gzip compression
- Browser caching support

#### 5. **Database Flexibility**
- Default: SQLite3 (local development)
- Set `DATABASE_URL` env var for PostgreSQL (production)
- Auto-connection pooling with `DJANGO_DB_CONN_MAX_AGE`
- SSL requirement configurable

---

## Production Environment Variables (Required)

Set these on PythonAnywhere or your production server:

```bash
# CRITICAL - MUST SET
DJANGO_SECRET_KEY=generate-a-new-strong-secret-key-here
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=yourdomain.pythonanywhere.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.pythonanywhere.com
DJANGO_FORCE_SSL=1

# RECOMMENDED - SHOULD SET
DATABASE_URL=postgresql://user:password@host:port/dbname
DJANGO_DB_SSL_REQUIRE=1
DJANGO_SECURE_HSTS_SECONDS=31536000

# OPTIONAL
NASA_API_KEY=your-api-key-or-DEMO_KEY
NASA_API_TIMEOUT=10
NASA_API_CACHE_TIMEOUT=3600
```

---

## Development Environment Variables (Optional)

Your local `.env` file can override defaults:

```bash
# Local development overrides
DJANGO_DEBUG=1
DJANGO_SECRET_KEY=your-dev-secret-key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_FORCE_SSL=0
NASA_API_KEY=DEMO_KEY
```

---

## Logging Directory

A new `logs/` directory has been created:

```
/Users/anamasiliuniene/PycharmProjects/PythonProject38/logs/
└── .gitkeep (placeholder to track directory in git)
```

On production, Django will automatically create:
```
logs/
└── django.log (production error logs)
```

---

## Configuration Checklist

### Before Deployment
- [ ] Generate new `DJANGO_SECRET_KEY` (use Django command)
- [ ] Set all CRITICAL environment variables
- [ ] Set database URL if using PostgreSQL
- [ ] Enable FORCE_SSL for HTTPS
- [ ] Configure ALLOWED_HOSTS for your domain

### During Deployment
- [ ] Verify environment variables are set
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Create logs directory if not exists
- [ ] Test health endpoint

### After Deployment
- [ ] Monitor `logs/django.log` for errors
- [ ] Test HTTPS redirect working
- [ ] Verify security headers present
- [ ] Check static files loading
- [ ] Test login/logout flow

---

## Generating a New Secret Key

Run this command locally:

```bash
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38/mysite
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Use the generated key as your `DJANGO_SECRET_KEY` environment variable.

---

## Settings.py Structure

### Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Default
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# If DATABASE_URL is set, uses PostgreSQL instead
if database_url:
    DATABASES["default"] = dj_database_url.parse(...)
```

### Logging Configuration
```python
LOGGING = {
    # Development: console only, all levels
    # Production: console + file, WARNING+ only
}
```

### Security Configuration
```python
if FORCE_SSL:
    # Enable HTTPS redirect
    # Enable secure cookies
    # Enable HSTS headers
    # Enable content protection headers
```

---

## Common Issues & Solutions

### Issue: DEBUG=True in production
**Solution:** Set `DJANGO_DEBUG=0` in environment variables

### Issue: Static files not loading
**Solution:** Run `python manage.py collectstatic --noinput`

### Issue: HTTPS redirect loop
**Solution:** Ensure `DJANGO_FORCE_SSL=1` and HTTPS is properly configured

### Issue: Secret key errors
**Solution:** Generate new key and set `DJANGO_SECRET_KEY` env var

### Issue: ALLOWED_HOSTS errors
**Solution:** Set `DJANGO_ALLOWED_HOSTS=yourdomain.com`

### Issue: No logs appear
**Solution:** Check `logs/` directory exists, Django will create `django.log`

---

## Next Steps

1. **Deploy to PythonAnywhere** (follow deployment guides)
2. **Set environment variables** (use provided list)
3. **Run migrations and collectstatic** (see deployment guide)
4. **Verify HTTPS working** (test with your domain)
5. **Monitor logs** (check `django.log` for errors)

---

## Security Notes

✅ **Enabled by Default:**
- CSRF protection
- XSS protection
- Clickjacking protection
- SQL injection prevention

✅ **Enabled with FORCE_SSL=1:**
- HTTPS redirect
- HSTS preload
- Secure cookies
- Referrer policy
- Content-Security-Policy support

⚠️ **Important:**
- Generate new SECRET_KEY for production (don't use default)
- Never commit `.env` file to git
- Use strong database passwords
- Enable database SSL for production PostgreSQL
- Monitor logs regularly

---

## References

- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [Django Settings Reference](https://docs.djangoproject.com/en/6.0/ref/settings/)
- [Django Logging Configuration](https://docs.djangoproject.com/en/6.0/topics/logging/)
- [dj-database-url](https://github.com/jacobian/dj-database-url)

---

**Your application is now configured and ready for production deployment!** 🚀

*Settings configuration completed March 6, 2026*

