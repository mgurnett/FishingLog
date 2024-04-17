import os
import json
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

with open ('/etc/stillwaterflyfishing.com/config.json') as config_file:
    config = json.load (config_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config ['SECRET_KEY']
 
GOOGLE_MAPS_API_KEY = config ['GOOGLE_MAPS_API_KEY']

OW_API_KEY = config ['OW_api_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://*.stillwaterflyfishing.com']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# DEVELOPMENT
STATIC_URL = '/public/assets/'
MEDIA_URL  = '/public/uploads/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'public/assets')]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

# PRODUCTION
STATIC_ROOT = os.path.join(BASE_DIR, 'public/assets')
MEDIA_ROOT = os.path.join(BASE_DIR, 'public/uploads')


# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'emails'
EMAIL_BACKEND = config ['EMAIL_BACKEND']
EMAIL_HOST = config ['EMAIL_HOST']
EMAIL_HOST_USER = config ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = config ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = config ['DEFAULT_FROM_EMAIL']