# makes selected variables in settings available to templates
# https://chriskief.com/2013/09/19/access-django-constants-from-settings-py-in-a-template/
from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'SYSTEM_NAME': settings.SYSTEM_NAME,
    }
