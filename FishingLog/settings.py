# from pathlib import Path # this is the new and better version see: https://youtu.be/yxa-DJuuTBI?si=NBw3V8_2o8Db0y4s
import os
import environ
 
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, 'FishingLog/.env'))

# False if not in os.environ because of casting above
DEBUG = env('DEBUG')

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

# APIs
GOOGLE_MAPS_API_KEY = env('GOOGLE_MAPS_API_KEY')
OW_API_KEY = env('OW_api_key')
CSRF_TRUSTED_ORIGINS = ['https://*.stillwaterflyfishing.com']

if not DEBUG:
    # PRODUCTION
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    SECURE_HSTS_SECONDS = 86400 
    SECURE_HSTS_PRELOAD = True 
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    ALLOWED_HOSTS = ['www.stillwaterflyfishing.com']
else:
    ALLOWED_HOSTS = ['*']
    print (f"Operating in: DEBUG mode - using: {env('DB_NAME')} / MariaDB at {env('DB_HOST')}:{env('DB_PORT')} located at {BASE_DIR}")

# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
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
    # 'ckeditor',    
    'easyaudit',
    'blacklist',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
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
                'catches.context_processors.week_context',                
            ],
        },
    },
]

WSGI_APPLICATION = 'FishingLog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "NAME": env('DB_NAME'),
        "ENGINE": "django.db.backends.mysql",
        "USER": env('DB_USER'),
        "PASSWORD": env('DB_PASSWORD'),
        "HOST": env('DB_HOST'),
        "PORT": env('DB_PORT'),
    },
    # "sqlite": {
    #     # "NAME": BASE_DIR / 'db.sqlite3',
    #     "NAME": "/home/michael/Desktop/FishingLog/db.sqlite3",
    #     "ENGINE": "django.db.backends.sqlite3",
    # },
}
# DATABASES = {
#     "default": {
#         "NAME": "/home/michael/Desktop/FishingLog/db.sqlite3",
#         "ENGINE": "django.db.backends.sqlite3",
#     },
# }


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

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_REDIRECT_URL = 'catch_home'
LOGIN_URL = 'login'

FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o644

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_THOUSAND_SEPARATOR = True

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
 
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# DEVELOPMENT
STATIC_URL = '/public/assets/'
MEDIA_URL  = '/public/uploads/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'public/assets')]
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder'
# )

# PRODUCTION
STATIC_ROOT = os.path.join(BASE_DIR, 'public/assets')
MEDIA_ROOT = os.path.join(BASE_DIR, 'public/uploads')


# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR,  'emails')
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')