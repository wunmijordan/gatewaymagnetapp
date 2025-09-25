import os
from pathlib import Path
import environ
from decouple import config
from dotenv import load_dotenv
import cloudinary
import dj_database_url

# =========================
# BASE DIRECTORY & ENV SETUP
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
load_dotenv(dotenv_path=BASE_DIR / ".env")

# =========================
# CORE SETTINGS
# =========================
SECRET_KEY = config("SECRET_KEY", default="goodnewsonlygoodnewsalways")
DEBUG = config("DEBUG", default=True, cast=bool)
ENVIRONMENT = config("DJANGO_ENV", default="development")

allowed_hosts_env = os.getenv(
    "ALLOWED_HOSTS", "localhost,127.0.0.1,magnet.gatewaynation.org"
)
ALLOWED_HOSTS = [
    host.strip() for host in allowed_hosts_env.split(",") if host.strip()
]

# =========================
# INSTALLED APPS
# =========================
INSTALLED_APPS = [
    # Django default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # Third-party
    "cloudinary",
    "cloudinary_storage",
    "widget_tweaks",
    "channels",
    "django_htmx",

    # Your apps
    "guests.apps.GuestsConfig",
    "accounts.apps.AccountsConfig",
    "notifications.apps.NotificationsConfig",
    "messaging.apps.MessagingConfig",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "notifications.middleware.CurrentUserMiddleware",
    #"accounts.middleware.OnlineNowMiddleware",
]

if DEBUG:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

# =========================
# URLS & TEMPLATES
# =========================
ROOT_URLCONF = "gatewaymagnetapp.urls"
WSGI_APPLICATION = "gatewaymagnetapp.wsgi.application"
ASGI_APPLICATION = "gatewaymagnetapp.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "notifications.context_processors.unread_notifications",
                "notifications.context_processors.user_settings",
                "messaging.context_processors.bulk_message_form",
                "guests.context_processors.superuser_guests",
            ],
        },
    },
]

# =========================
# DATABASE
# =========================
if ENVIRONMENT == "production":
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    try:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": config("DB_NAME"),
                "USER": config("DB_USER"),
                "PASSWORD": config("DB_PASSWORD"),
                "HOST": config("DB_HOST"),
                "PORT": config("DB_PORT"),
            }
        }
    except Exception:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }

# =========================
# REDIS CHANNEL LAYER
# =========================
import os

# Prefer a single REDIS_URL for simplicity (works in dev and prod)
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
            # Optional: tweak capacity/expiry to reduce disconnects
            "capacity": 1000,
            "expiry": 60,
        },
    }
}


# =========================
# STATIC & MEDIA
# =========================
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =========================
# CLOUDINARY
# =========================
cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET"),
)

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
}

# =========================
# PWA CONFIGURATION
# =========================
PWA_APP_NAME = "Gateway Nation Magnet App"
PWA_APP_SHORT_NAME = "Magnet"
PWA_APP_DESCRIPTION = "Guest Management System for Gateway Nation"
PWA_APP_THEME_COLOR = "#2e303e"
PWA_APP_BACKGROUND_COLOR = "#2e303e"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_START_URL = "/"
PWA_APP_ORIENTATION = "portrait"
PWA_APP_STATUS_BAR_COLOR = "default"
PWA_APP_ICONS = [
    {"src": "/static/images/icons/icon-192x192.png", "sizes": "192x192"},
    {"src": "/static/images/icons/icon-512x512.png", "sizes": "512x512"},
]
PWA_APP_ICONS_APPLE = PWA_APP_ICONS
PWA_APP_SPLASH_SCREEN = [
    {
        "src": "/static/images/splash-512x1024.png",
        "media": "(device-width: 360px) and (device-height: 740px)",
    }
]
PWA_APP_DIR = "ltr"
PWA_APP_LANG = "en-US"

# =========================
# AUTHENTICATION & SESSIONS
# =========================
AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "/post-login/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = False

# =========================
# PASSWORD VALIDATORS
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================
# LOCALIZATION
# =========================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True

# =========================
# DEFAULT AUTO FIELD
# =========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================
# WEBSOCKET SCHEME
# =========================
WS_SCHEME = "wss://" if ENVIRONMENT == "production" else "ws://"

# =========================
# CSRF & SECURITY
# =========================
csrf_origins_env = os.getenv(
    "CSRF_TRUSTED_ORIGINS", "https://magnet.gatewaynation.org"
)
CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in csrf_origins_env.split(",") if origin.strip()
]

CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

if DEBUG:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    CSRF_TRUSTED_ORIGINS.append("http://127.0.0.1:8000")

