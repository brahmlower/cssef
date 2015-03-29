"""
Django settings for cssefwebfront project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import djcelery
djcelery.setup_loader()



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '80%qqhb_g2n8hdeh2)s#uu^vw*s_mz4!p751+5!@5!1396e#(m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (BASE_DIR + "/cssefwebfront/templates",)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'rest_framework',
    'djcelery',
    'cssefwebfront',
    'ScoringEngine',
    'WebApi',
    'WebInterface',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = {
    'cssefwebfront.authbackends.TeamAuth',
    'cssefwebfront.authbackends.AdminAuth'
}

ROOT_URLCONF = 'cssefwebfront.urls'

WSGI_APPLICATION = 'cssefwebfront.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Anchorage'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = ''

STATICFILES_DIRS = (BASE_DIR + '/static/',)

STATIC_URL = '/static/'

# Celery Settings
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
BROKER_POOL_LIMIT = 1

# CSSEF Specific
CONTENT_PLUGGINS_PATH =         "/cssefwebfront/resources/plugins/"
CONTENT_INJECT_PATH =           "/cssefwebfront/resources/content/injects/"
CONTENT_INJECT_REPONSE_PATH =   "/cssefwebfront/resources/content/injectresponses/"
CONTENT_INCIDENT_REPONSE_PATH = "/cssefwebfront/resources/content/incidentresponses/"


# Logging configurations
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'django_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django_debug.log',
            'formatter': 'verbose'
        },
        'cssefwebfront_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'cssefwebfront_debug.log',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers':['django_debug'],
            'propagate': True,
            'level':'DEBUG',
        },
        'cssefwebfront': {
            'handlers': ['cssefwebfront_debug'],
            'level': 'DEBUG',
        },
    }
}

import logging
logger = logging.getLogger(__name__)


