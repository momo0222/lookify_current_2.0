"""
Django settings for user_management project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import dj_database_url
from pathlib import Path

# To keep secret keys in environment variables
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# settings.py

ALLOWED_HOSTS = [
    'lookify123.pythonanywhere.com', 
    'www.lookify.org', 
    '127.0.0.1', 
    'localhost'
]



# Application definition

INSTALLED_APPS = [
    'widget_tweaks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_select2',
    'users',
    'taggit',
    'opportunity',
    'easyaudit',
    'dashboard',
    'orgs',
    'notifications'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware",

]

ROOT_URLCONF = 'lookify.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'lookify', 'templates'),  # This line includes the lookify/templates directory
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processor.notification_context_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'lookify.wsgi.application'
ASGI_APPLICATION = 'lookify.asgi.application'


# settings.py
# DATABASE_URL = os.getenv('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.parse("postgresql://lookify_mc05_user:obyTQTt4vwYklq4FCox9delSaQLcWygj@dpg-cq295clds78s73eagb7g-a.oregon-postgres.render.com/lookify_mc05")
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'users.backends.UsernameOrEmailBackend',
    'django.contrib.auth.backends.ModelBackend',


)


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'users.CustomUser'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Define the directory where uploaded media files will be stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Define the URL prefix for media files
MEDIA_URL = '/media/'


LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'

LOGOUT_REDIRECT_URL = '/'
# # social auth configs for github
# SOCIAL_AUTH_GITHUB_KEY = str(os.getenv('GITHUB_KEY'))
# SOCIAL_AUTH_GITHUB_SECRET = str(os.getenv('GITHUB_SECRET'))

# # social auth configs for google
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = str(os.getenv('GOOGLE_KEY'))
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = str(os.getenv('GOOGLE_SECRET'))

# email configs
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
# EMAIL_HOST_USER = str(os.getenv('EMAIL_USER'))
EMAIL_HOST_USER = "lookify123@gmail.com"
EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_PASSWORD'))



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = False
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = False

#channles
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}