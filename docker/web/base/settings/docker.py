from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': 'startup',
        'HOST': 'postgres',
        'PORT': 5432,
    }
}

SYSTEM_NAME = 'docker'

REDIS_SERVER = 'redis'
REDIS_PORT = '6379'


