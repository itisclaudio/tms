#from prosoft.settings.base import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print "in base.py, BASE_DIR:"
print BASE_DIR

DEBUG = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'afl549q&v2eppw3reii)7wozdiol47n)hr7^fis*g#5a!-e04='

#TEMPLATE_DEBUG = DEBUG #For error handling
ALLOWED_HOSTS = ['*']

#9-For middleware LoginRequiredMiddleware:
LOGIN_URL = '/login/'
LOGIN_EXEMPT_URLS = (
 r'^about\.html$',
 r'^admin/', # allow any URL under /legal/*
 r'^user/',
 r'^reset/',
 r'^media/',
)
#End 9

# Application definition

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'prosoft.files',
	'whitenoise.runserver_nostatic',
)

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

ROOT_URLCONF = 'prosoft.urls'

INTERNAL_IPS = ('127.0.0.1',)#For debug_toolbar
WSGI_APPLICATION = 'prosoft.wsgi.application'

#TEMPLATE_DIRS = (
#	os.path.join(os.path.dirname(__file__),'templates'),
#)

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'prosoft',
		'USER': 'prosoft',
		'PASSWORD': 'admin',
	}
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(os.path.dirname(__file__)),'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
			'debug':DEBUG,
        },
    },
]

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'prosoft/static'),
)

UPLOAD_DOCS = 'prosoft/media/docs'

#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

MEDIA_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(__file__)),'media/'))
MEDIA_URL = '/media/'

#To send emails
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'worldfoodguideapp@gmail.com'
EMAIL_HOST_PASSWORD = 'wfgpass1'
ADMINS = (('Claudio', 'itisclaudio@gmail.com'),) # A tuple that lists people who get code error notifications. When DEBUG=False