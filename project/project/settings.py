from datetime import timedelta
from pathlib import Path

from decouple import config

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = config('SECRET_KEY')
DEBUG = True

ALLOWED_HOSTS = ['*']  



INSTALLED_APPS = [
    'rest_framework_simplejwt.token_blacklist',
    'ninja_jwt',
    'ninja_extra',

    'accounts',
    'books', 

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'project.urls'

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
            ],
        },
    },
]

NINJA_SIMPLE_JWT = {
    "USE_STATELESS_AUTH": True,
}


WSGI_APPLICATION = 'project.wsgi.application'

"""PROD DB"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

"""LOCAL DB"""
""" DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
} """

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

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





LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True      
USE_L10N = True      
USE_TZ = True




STATIC_URL = 'static/'
AUTH_USER_MODEL = 'accounts.User'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
PASSWORD_RESET_TIMEOUT = 60 * 60 * 24  # 24 часа

EMAIL_HOST="smtp.gmail.com"       
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')




SPECTACULAR_SETTINGS = {
    "TITLE": "Books API",
    "DESCRIPTION": "Документация API проекта Books",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,

    # JWT
    "SECURITY": [
        {"bearerAuth": []}
    ],
    "COMPONENT_SPLIT_REQUEST": True,
}
