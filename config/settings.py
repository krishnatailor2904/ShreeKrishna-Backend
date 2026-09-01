"""
Django settings for Shree Krishnaa e-commerce project.
"""

import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv
import dj_database_url
import cloudinary
import cloudinary_storage


# =========================================================
# BASE CONFIG
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=True)


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-change-this-in-production-shreekrishnaa"
)

DEBUG = os.getenv("DEBUG", "False") == "True"


ALLOWED_HOSTS = [
    ".vercel.app",
    "shreekrishnaa.com",
    "www.shreekrishnaa.com",
    "localhost",
    "127.0.0.1",
]


# =========================================================
# INSTALLED APPS
# =========================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",

    # Cloudinary
    "cloudinary",
    "cloudinary_storage",

    # Project apps
    "accounts",
    "products",
    "orders",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URL CONFIG
# =========================================================

ROOT_URLCONF = "config.urls"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates"
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================================================
# WSGI / ASGI
# =========================================================

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"


# =========================================================
# DATABASE
# =========================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        f"DATABASE_URL not found. Checked: {ENV_FILE}"
    )


DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=True,
    )
}


# =========================================================
# CUSTOM USER MODEL
# =========================================================

AUTH_USER_MODEL = "accounts.User"


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6
        },
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator"
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# =========================================================
# MEDIA FILES
# =========================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# CLOUDINARY
# =========================================================

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv(
        "CLOUDINARY_CLOUD_NAME"
    ),

    "API_KEY": os.getenv(
        "CLOUDINARY_API_KEY"
    ),

    "API_SECRET": os.getenv(
        "CLOUDINARY_API_SECRET"
    ),
}


# =========================================================
# DJANGO STORAGE
# =========================================================

STORAGES = {
    "default": {
        "BACKEND":
        "cloudinary_storage.storage.MediaCloudinaryStorage",
    },

    "staticfiles": {
        "BACKEND":
        "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# DJANGO REST FRAMEWORK
# =========================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}


# =========================================================
# JWT
# =========================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),

    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),

    "AUTH_HEADER_TYPES": (
        "Bearer",
    ),
}


# =========================================================
# CORS
# =========================================================

CORS_ALLOWED_ORIGINS = [
    "https://shreekrishnaa.com",
    "https://www.shreekrishnaa.com",

    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


CORS_ALLOW_CREDENTIALS = True


# =========================================================
# CSRF TRUSTED ORIGINS
# =========================================================

CSRF_TRUSTED_ORIGINS = [
    "https://shreekrishnaa.com",
    "https://www.shreekrishnaa.com",
]


# =========================================================
# EMAIL
# =========================================================

EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = os.getenv(
    "EMAIL_HOST",
    "smtp.gmail.com"
)

EMAIL_PORT = int(
    os.getenv(
        "EMAIL_PORT",
        587
    )
)

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv(
    "EMAIL_HOST_USER",
    ""
)

EMAIL_HOST_PASSWORD = os.getenv(
    "EMAIL_HOST_PASSWORD",
    ""
)

DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    EMAIL_HOST_USER
)


# =========================================================
# ADMIN NOTIFICATIONS
# =========================================================

ADMIN_NOTIFY_EMAIL = os.getenv(
    "ADMIN_NOTIFY_EMAIL",
    ""
)

ADMIN_NOTIFY_PHONE = os.getenv(
    "ADMIN_NOTIFY_PHONE",
    ""
)


# =========================================================
# SMS - FAST2SMS
# =========================================================

FAST2SMS_API_KEY = os.getenv(
    "FAST2SMS_API_KEY",
    ""
)


# =========================================================
# UPI
# =========================================================

UPI_ID = os.getenv(
    "UPI_ID",
    "9408222280@ybl"
)

UPI_PAYEE_NAME = os.getenv(
    "UPI_PAYEE_NAME",
    "Shree Krishnaa"
)


# =========================================================
# DEBUG EMAIL FALLBACK
# =========================================================

if DEBUG and not EMAIL_HOST_USER:
    EMAIL_BACKEND = (
        "django.core.mail.backends.console.EmailBackend"
    )