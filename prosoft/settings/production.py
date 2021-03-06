#from prosoft.settings.base import *
from .base import *
# Override base.py settings here
#print "in production.py"

DEBUG = True
ALLOWED_HOSTS = ['tms-s.herokuapp.com','tms-s-production.herokuapp.com/','prosoft-tms-stage.s3.amazonaws.com']
INSTALLED_APPS += (
	'storages',#App needed for Amazon AWS S3
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY','afl549q&v2eppw3reii)7wozdiol47n)hr7^fis*g#5a!-e04=')

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'prosoft.libs.middleware.LoginRequiredMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
)

import dj_database_url
#db_from_env = dj_database_url.config()
DATABASES = {
	'default': dj_database_url.config()
}
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'prosoft/static'),
	#os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#So whitenoise can handle storage in heroku
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# To load different files when run localy, like in url for debug_toolbar
LOCAL_DEV = False

#Heroku variable for https:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#For Amazon S3
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False#Doesn't add signature after media files
MEDIAFILES_LOCATION = 'media'
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'custom_storages.StaticRootS3BotoStorage'
S3DIRECT_REGION = 'us-west-2'
S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

MEDIA_ROOT = os.path.join(S3_URL, "media")
STATIC_URL = S3_URL + 'static/'
MEDIA_URL = S3_URL + 'media/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

#To send emails
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'worldfoodguideapp@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
ADMINS = (('Claudio', 'itisclaudio@gmail.com'),) # A tuple that lists people who get code error notifications. When DEBUG=False