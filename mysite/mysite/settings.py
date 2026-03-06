from pathlib import Path
from .my_settings import SECRET_KEY, DEBUG, ALLOWED_HOSTS
import os
from django.core.exceptions import ImproperlyConfigured

try:
    import dj_database_url
except ImportError:  # pragma: no cover - optional in local dev
    dj_database_url = None

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency during transition
    load_dotenv = None

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

if load_dotenv is not None:
    # Load both repo-level and project-level .env files if present.
    load_dotenv(BASE_DIR.parent / ".env")
    load_dotenv(BASE_DIR / ".env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.getenv("DJANGO_DEBUG", DEBUG)).lower() in ("1", "true", "yes", "on")

allowed_hosts_env = os.getenv("DJANGO_ALLOWED_HOSTS", "").strip()
if allowed_hosts_env:
    ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_env.split(",") if h.strip()]
else:
    ALLOWED_HOSTS = ALLOWED_HOSTS

csrf_trusted_origins_env = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").strip()
CSRF_TRUSTED_ORIGINS = (
    [o.strip() for o in csrf_trusted_origins_env.split(",") if o.strip()]
    if csrf_trusted_origins_env else []
)


# Application definition

INSTALLED_APPS = [
    'mini_notion.apps.MiniNotionConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mini_notion.context_processors.hero_phrase',
                'mini_notion.context_processors.reminders_for_user',
            ],
        },
    },
]


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

database_url = os.getenv("DATABASE_URL", "").strip()
if database_url:
    if dj_database_url is None:
        raise ImproperlyConfigured(
            "DATABASE_URL is set but dj-database-url is not installed. "
            "Install dependencies from requirements.txt."
        )
    DATABASES["default"] = dj_database_url.parse(
        database_url,
        conn_max_age=int(os.getenv("DJANGO_DB_CONN_MAX_AGE", "600")),
        ssl_require=str(os.getenv("DJANGO_DB_SSL_REQUIRE", "1")).lower() in ("1", "true", "yes", "on"),
    )


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Vilnius'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/


STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

LOGIN_REDIRECT_URL = 'dashboard'  # redirect after login
LOGOUT_REDIRECT_URL = 'dashboard'    # redirect after logout
LOGIN_URL = '/login/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

FORCE_SSL = str(os.getenv("DJANGO_FORCE_SSL", "0")).lower() in ("1", "true", "yes", "on")

# External API integration settings
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
NASA_API_TIMEOUT = int(os.getenv("NASA_API_TIMEOUT", "10"))
NASA_API_CACHE_TIMEOUT = int(os.getenv("NASA_API_CACHE_TIMEOUT", "3600"))

if FORCE_SSL:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
    SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"

# Logging configuration
# In production (DEBUG=0): shows WARNING and ERROR level logs
# In development (DEBUG=1): shows all levels including DEBUG/INFO
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR.parent, 'logs', 'django.log'),
            'formatter': 'verbose',
            'level': 'WARNING',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'] if DEBUG else ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO' if DEBUG else 'WARNING',
            'propagate': False,
        },
        'mini_notion': {
            'handlers': ['console'] if DEBUG else ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your_email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your_email_app_password'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
