import os
import json
from pathlib import Path# settings.py
import cloudinary
import cloudinary.uploader
import cloudinary.api	

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

with open ('/etc/stillwaterflyfishing.com/config.json') as config_file:
    config = json.load (config_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config ['SECRET_KEY']
 
GOOGLE_MAPS_API_KEY = config ['GOOGLE_MAPS_API_KEY']

OW_API_KEY = config ['OW_api_key']

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config ['CLOUD_NAME'],
    'API_KEY': config ['API_KEY'],
    'API_SECRET': config ['API_SECRET'],
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_HSTS_SECONDS = 86400 
SECURE_HSTS_PRELOAD = True 
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

#ALLOWED_HOSTS = ['https://*.stillwaterflyfishing.com']
ALLOWED_HOSTS = ['www.stillwaterflyfishing.com']
CSRF_TRUSTED_ORIGINS = ['https://*.stillwaterflyfishing.com']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# DEVELOPMENT
# STATIC_URL = '/public/assets/'
# MEDIA_URL  = '/public/uploads/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'public/assets')]
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder'
# )

# PRODUCTION
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'
STATIC_URL = '/public/assets/'
MEDIA_URL  = '/stillwaterflyfishing.com/public/uploads/'
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

# Static file serving.
# https://whitenoise.readthedocs.io/en/stable/django.html#add-compression-and-caching-support
# STORAGES = {
#     # ...
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

#  https://djangodeployment.readthedocs.io/en/latest/05-static-files.html  Deploying Django on a single Debian or Ubuntu server
# https://arnopretorius-cwd.medium.com/django-web-application-security-checklist-64bfe2438a29  Django web application security checklist