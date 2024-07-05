from hydraulics.settings import *
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'hydraulics_dev', 
        # 'USER':'root',  
        # 'PASSWORD':'', 
        'NAME': 'hydradev',  
        'USER':'hydradev',  
        'PASSWORD':'chennai01', 
        'HOST':'',  
        'PORT':'3306'  
    }  
} 

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
