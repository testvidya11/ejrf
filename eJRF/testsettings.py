from settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ejrf_test",
        "USER": "andrew",
        "PASSWORD": "",
        "HOST": "localhost",
    }
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_nose',
    'south',
    'lettuce.django',
    'django_extensions',
    'bootstrap_pagination',
    'questionnaire'
)

SOUTH_TESTS_MIGRATE = False

import logging

south_logger = logging.getLogger('south')
south_logger.setLevel(logging.INFO)