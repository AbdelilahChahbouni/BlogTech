"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG")

ALLOWED_HOSTS = ['localhost','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'account',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'storages',
    'rest_framework',
    'api',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                 'blog.context_processors.notifications_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("DATABASE_NAME"),
        'USER': config("DATABASE_USER"),
        'PASSWORD':config("DATABASE_PASSWORD"),
        # 'HOST': 'backendblog.cjqe8s48iehr.us-east-1.rds.amazonaws.com',  # or the IP address of your database server
        'HOST':'localhost',
        'PORT': '5432',       # default PostgreSQL port
    }
}

# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 10,  # Number of items per page
# }







# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# media

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media/'



LOGIN_REDIRECT_URL = "home"

LOGIN_URL = "login"

LOGOUT_URL = "logout"

LOGOUT_REDIRECT_URL = "default"



AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
]

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKENDS = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST_USER = "dev4testemail@gmail.com"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = 'fsfe uibc kjfb uwbu '
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# AWS S3 Configuration
# AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_REGION_NAME = 'us-east-1' 
# AWS_S3_CUSTOM_DOMAIN = "https://bk-s3-st.s3.us-east-1.amazonaws.com"
# AWS_S3_FILE_OVERWRITE = False


# STORAGES = {

#     # Media file (image) management  
#     "default": {
#         "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
#     },
   
#     # CSS and JS file management
#     "staticfiles": {
#         "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
#     },
# }





