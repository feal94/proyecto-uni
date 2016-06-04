from .base import *

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TFG',
        'USER': 'dev',
        'PASSWORD': 'Proyecto_Uni001',
        'HOST': 'localhost', 
        'PORT': '',
    }

}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False 

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'