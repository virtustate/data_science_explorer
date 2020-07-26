from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': 'startup',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

SYSTEM_NAME = 'localhost'