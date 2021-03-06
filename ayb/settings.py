"""
Django settings for ayb project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
import moneyed
from django.db import models

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cva(q33ri%ok*0w$zr25fb_t$4%ra8*ols=m7=v76h=3pl-umu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'costos',
    'gettext',
    'crispy_forms',
    'formtools',
    'account',
    'django_registration',
    'django_quill',
    'django_countries',
    'djmoney',

]
ACCOUNT_ACTIVATION_DAYS = 7

AUTH_USER_MODEL = 'costos.User'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',
    'account.middleware.ExpiredPasswordMiddleware',
]

ROOT_URLCONF = 'ayb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = [
      "account.context_processors.account",
      "django.core.context_processors.request",
    ]

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]


WSGI_APPLICATION = 'ayb.wsgi.application'

INTERNAL_IPS = [
    '127.0.0.1',
]
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nscgdb',
        'USER': 'nscguser',
        'PASSWORD': 'nscgpass',
        'HOST': 'localhost',
        'PORT': '5432',

    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en'
CURRENCIES = ('COP', 'USD')
DEFAULT_CURRENCY = 'COP'
CURRENCIES_PLACE = {'COP': 2, 'USD': 2}
#CURRENCIES_PLACE = {'COP': 2, 'USD': 2, 'BTC': 8}
CURRENCY_CHOICES = [('COP', 'COP $'), ('USD', 'USD $')]
#CURRENCY_CHOICES = [('COP', 'COP $'), ('USD', 'USD $'), ('BTC', 'BTC B')]
TIME_ZONE = 'UTC'
#BASE_CURRENCY = 'COP'
USE_I18N = True
USE_TZ = True
USE_L10N = True

COUNTRIES_FIRST = ['COL', 'US']

COP = moneyed.add_currency(
    code='COP',
    numeric='170',
    name='Colombian Peso',
    countries=('COLOMBIA', )
)

USD = moneyed.add_currency(
    code='USD',
    numeric='840',
    name='US Dollar',
    countries=('US', )
)
#
# BTC = moneyed.add_currency(
#     code='BTC',
#     numeric='1000',
#     name='Bitcoin',
#     countries=('Bitcoin',),
# )



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
VENV_PATH = os.path.dirname(BASE_DIR)
STATIC_ROOT = os.path.join(VENV_PATH, 'static_root')
str = 'costos/fig'

if not os.path.exists(str):
    if not os.path.exists(str):
        os.mkdir(str)


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'home'
SITE_ID=1

QUILL_CONFIGS = {
    'default':{
        'theme': 'snow',
        'modules': {
            'syntax': True,
            'toolbar': [
                [
                    {'font': []},
                    {'header': []},
                    {'align': []},
                    'bold', 'italic', 'underline', 'strike', 'blockquote',
                    {'color': []},
                    {'background': []},
                ],
                ['code-block', 'link'],
                ['clean'],
            ]
        }
    }
}

