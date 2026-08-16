from pathlib import Path
import os
import dj_database_url


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-change-this-later"
)

DEBUG = os.environ.get(
    "DEBUG",
    "False"
).lower() == "true"


ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "rock-fee-portal.onrender.com",
]


# ============================================================
# CSRF / SECURITY
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    "https://rock-fee-portal.onrender.com",
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [

    # --------------------------------------------------------
    # Django
    # --------------------------------------------------------

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # --------------------------------------------------------
    # Third-party
    # --------------------------------------------------------

    "storages",

    # --------------------------------------------------------
    # Rock Fee Portal
    # --------------------------------------------------------

    "dashboard",
    "students",
    "parents",
    "fees",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "rock_fee_portal.urls"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [

    {
        "BACKEND":
            "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",

            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = "rock_fee_portal.wsgi.application"


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.environ.get("DATABASE_URL")


if DATABASE_URL:

    DATABASES = {

        "default": dj_database_url.parse(

            DATABASE_URL,

            conn_max_age=600,

            ssl_require=True,
        )
    }

else:

    DATABASES = {

        "default": {

            "ENGINE":
                "django.db.backends.sqlite3",

            "NAME":
                BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator",
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# ============================================================
# SUPABASE STORAGE
# ============================================================

AWS_ACCESS_KEY_ID = os.environ.get(
    "SUPABASE_ACCESS_KEY_ID"
)

AWS_SECRET_ACCESS_KEY = os.environ.get(
    "SUPABASE_SECRET_ACCESS_KEY"
)

AWS_STORAGE_BUCKET_NAME = os.environ.get(
    "SUPABASE_BUCKET_NAME"
)

AWS_S3_ENDPOINT_URL = os.environ.get(
    "SUPABASE_S3_ENDPOINT"
)

AWS_S3_REGION_NAME = os.environ.get(
    "AWS_S3_REGION_NAME",
    "eu-central-1"
)

AWS_S3_SIGNATURE_VERSION = os.environ.get(
    "AWS_S3_SIGNATURE_VERSION",
    "s3v4"
)

AWS_S3_FILE_OVERWRITE = False

AWS_DEFAULT_ACL = None

AWS_QUERYSTRING_AUTH = False

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

AWS_LOCATION = ""


# ============================================================
# MEDIA FILES
# ============================================================

DEFAULT_FILE_STORAGE = (
    "storages.backends.s3.S3Storage"
)

MEDIA_URL = (
    f"{AWS_S3_ENDPOINT_URL}/"
    f"{AWS_STORAGE_BUCKET_NAME}/"
)


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)