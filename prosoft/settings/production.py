#from prosoft.settings.base import *
from .base import *
# Override base.py settings here
#print "in production.py"

DEBUG = True
ALLOWED_HOSTS = ['prosoft-tms.herokuapp.com']
INSTALLED_APPS += (
	'django.contrib.admin',
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(SECRET_KEY,'afl549q&v2eppw3reii)7wozdiol47n)hr7^fis*g#5a!-e04=')

MIDDLEWARE_CLASSES = (
	'whitenoise.middleware.WhiteNoiseMiddleware',
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


