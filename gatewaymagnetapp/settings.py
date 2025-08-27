import os
import socket
from pathlib import Path
import environ
from decouple import config
import cloudinary
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment setup
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
load_dotenv(dotenv_path=BASE_DIR / '.env')

# Core settings
SECRET_KEY = config('SECRET_KEY', default='goodnewsonlygoodnewsalways')
DEBUG = config('DEBUG', default=True, cast=bool)
ENVIRONMENT = config('DJANGO_ENV', default='development')

# Allowed hosts
allowed_hosts_env = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]

# Installed apps
INSTALLED_APPS = [
  # Third-party apps
  'cloudinary',
  'cloudinary_storage',
  'widget_tweaks',
  'channels',

  # Django default apps
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django_htmx',
  'django.contrib.humanize',

  # Your apps
  'guests.apps.GuestsConfig',
  'accounts.apps.AccountsConfig',
  'notifications.apps.NotificationsConfig',
  'messaging.apps.MessagingConfig',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
    'notifications.middleware.CurrentUserMiddleware',
]

if DEBUG:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'gatewaymagnetapp.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processors.unread_notifications',
                'notifications.context_processors.user_settings',
                'messaging.context_processors.bulk_message_form',
            ],
        },
    },
]

WSGI_APPLICATION = 'gatewaymagnetapp.wsgi.application'

ASGI_APPLICATION = "gatewaymagnetapp.asgi.application"

# Use Redis for channel layer (requires Redis running)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [{
                "host": os.getenv("REDIS_HOST"),
                "port": int(os.getenv("REDIS_PORT", 6379)),
                "password": os.getenv("REDIS_PASSWORD") or None,
            }],
        },
    },
}

# Database
if ENVIRONMENT == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
            'OPTIONS': {'sslmode': 'require'},
        }
    }
else:
    try:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': config('DB_NAME'),
                'USER': config('DB_USER'),
                'PASSWORD': config('DB_PASSWORD'),
                'HOST': config('DB_HOST'),
                'PORT': config('DB_PORT'),
            }
        }
    except Exception:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

# Debug toolbar internal IPs
if DEBUG:
    INTERNAL_IPS = ['127.0.0.1']
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Cloudinary configuration
cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET')
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

# Static and media files
if DEBUG:
    STATIC_URL = '/static/'
else:
    STATIC_URL = 'https://gatewaymagnetapp-static.onrender.com/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # fallback for local uploads

AUTH_USER_MODEL = "accounts.CustomUser"

# Authentication redirects
LOGIN_REDIRECT_URL = '/post-login/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = False

# Default primary key field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# PWA Configuration (minimal, no caching)
PWA_APP_NAME = 'Gateway Nation Magnet App'
PWA_APP_SHORT_NAME = 'Magnet'
PWA_APP_DESCRIPTION = "Guest Management System for Gateway Nation"
PWA_APP_THEME_COLOR = '#2e303e'
PWA_APP_BACKGROUND_COLOR = '#2e303e'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {'src': '/static/images/icons/icon-192x192.png', 'sizes': '192x192'},
    {'src': '/static/images/icons/icon-512x512.png', 'sizes': '512x512'},
]
PWA_APP_ICONS_APPLE = PWA_APP_ICONS
PWA_APP_SPLASH_SCREEN = [
    {'src': '/static/images/splash-512x1024.png', 'media': '(device-width: 360px) and (device-height: 740px)'}
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
