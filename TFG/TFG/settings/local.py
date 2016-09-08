from .base import *

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TFG',
        'USER': 'alvaro',
        'PASSWORD': get_secret("DATABASE_PASSWD"),
        'HOST': 'localhost', 
        'PORT': '',
    }

}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'