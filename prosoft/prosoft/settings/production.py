#from prosoft.settings.base import *
from .base import *
# Override base.py settings here
#print "in production.py"

DEBUG = False

INSTALLED_APPS += (
	'django.contrib.admin',
)

import dj_database_url
DATABASES = {
	'default': dj_database_url.config()
}
db_from_env = dj_database_url.config(conn_max_age==500)
DATABASES['default'].update(db_from_env)

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#So whitenoise can handle storage in heroku
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

#Heroku variable for https:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


