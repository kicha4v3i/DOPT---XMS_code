from hydraulics.settings import *
DEBUG = True

ALLOWED_HOSTS = ['*']
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'hydradev',  
        'USER':'hydradev',  
        'PASSWORD':'chennai01',  
        'HOST':'127.0.0.1',  
        'PORT':'3306'  
    }  
} 

STATIC_ROOT = '/var/www/dopthydra/static'
