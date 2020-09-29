"""
Django settings for foris_dev project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import yaml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


is_deployed = os.path.exists("./deployment_settings.yaml")

if is_deployed:
    with open("./deployment_settings.yaml", "r") as settings_file:
        settings = yaml.safe_load(settings_file)
    SECRET_KEY = settings["DJANGO_SECRET_KEY"]
    ALLOWED_HOSTS = [settings["SITE_NAME"]]
    DEBUG = False
else:
    DEBUG = True
    SECRET_KEY = "insecure-key-for-dev"
    ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_page',
    'accounts',
    'lists',
    'functional_tests',
    'rest_framework',
    'the_elder_commands',
]

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    "accounts.authentication.PasswordlessAuthenticationBackend",
]

# Make that all error messages are displayed in terminal
# noinspection PyUnresolvedReferences
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        'main_page_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'main_page.log'),
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        },
        'main_page': {
            'handlers': ['main_page_logfile'],
            'level': 'DEBUG',
        },
    },
    "root": {"level": "INFO"},
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foris_dev.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "the_elder_commands.inventory.template_variables",
            ],
        },
    },
]

WSGI_APPLICATION = 'foris_dev.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
with open("../.secret") as secret_file:
    secret = yaml.safe_load(secret_file)

if is_deployed:
    database_name = settings["DATABASE_NAME"]
else:
    database_name = "test_database"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': database_name,
        'USER': secret["user_name"],
        'PASSWORD': secret["postgresql"],
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# ReCaptcha
if is_deployed:
    RECAPTCHA_SITE_KEY = secret[f"recaptcha_{database_name}_site_key"]
    RECAPTCHA_SECRET_KEY = secret[f"recaptcha_{database_name}_secret_key"]
else:
    RECAPTCHA_SITE_KEY = secret["recaptcha_site_key"]
    RECAPTCHA_SECRET_KEY = secret["recaptcha_secret_key"]


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# E-mail settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

if is_deployed:
    EMAIL_HOST_USER = "foris.dev@gmail.com"
    EMAIL_HOST_PASSWORD = secret["email_host_pass"]
else:
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""


# Security setting

if is_deployed:
    # security tweaks from:
    # https://github.com/benyaminsalimi/Secure-Headers/blob/master/example/Django_Settings.py

    # X-XSS-Protection
    SECURE_BROWSER_XSS_FILTER = True
    # X-Frame-Options
    X_FRAME_OPTIONS = 'DENY'
    # X-Content-Type-Options
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # These are redundant thanks to .dev domain.
    # Strict-Transport-Security
    # SECURE_HSTS_SECONDS = 15768000
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True

    # that requests over HTTP are redirected to HTTPS. also can config in webserver
    # SECURE_SSL_REDIRECT = True

    # for more security
    CSRF_COOKIE_SECURE = True
    CSRF_USE_SESSIONS = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Strict'
