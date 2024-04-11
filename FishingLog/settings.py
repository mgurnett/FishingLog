from pathlib import Path
import os
import json

with open ('/etc/config.json') as config_file:
    config = json.load (config_file)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config ['SECRET_KEY']
SESSION_COOKIE_SECURE = True

GOOGLE_MAPS_API_KEY = config ['GOOGLE_MAPS_API_KEY']

OW_API_KEY = config ['OW_api_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config ['DEBUG']
SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = list(config ['ALLOWED_HOSTS'])
CSRF_TRUSTED_ORIGINS = ['https://*.stillwaterflyfishing.com']
CSRF_COOKIE_SECURE = True


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'catches.apps.CatchesConfig',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_extensions',
    "taggit",
    'ckeditor',    
    'easyaudit',
    'blacklist',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'blacklist.middleware.BlacklistMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FishingLog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': ["templates/"], 
        'DIRS': [''],
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

WSGI_APPLICATION = 'FishingLog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_REDIRECT_URL = 'catch_home'
LOGIN_URL = 'login'

FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o644

# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'emails'
EMAIL_BACKEND = config ['EMAIL_BACKEND']
EMAIL_HOST = config ['EMAIL_HOST']
EMAIL_HOST_USER = config ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = config ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = config ['DEFAULT_FROM_EMAIL']

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TAGGIT_CASE_INSENSITIVE = True

TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING  = False

GRAPH_MODELS = {
  'app_labels': ["catches", "blog"],
  'group_models': True,
  'color_code_deletions': True,
#   'arrow_shape': True,
#   'hide_edge_labels': True,
}   
#may need: sudo apt install graphviz
#to run: python3 manage.py graph_models -o fish_log_models.png

# CRISPY_FAIL_SILENTLY = not DEBUG

# https://dreampuf.github.io/GraphvizOnline/ - you can copy the dot file into this to see it.
# python3 manage.py graph_models catches blog > models.dot