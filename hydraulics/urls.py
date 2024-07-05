"""hydraulics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import notifications.urls
from django.contrib.auth import views as auth_views #import this
from custom_auth import views
from helpers.commonimport import settings,static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('custom_auth.urls')),
    path('projects/', include('projects.urls')),
    path('wells/', include('wells.urls')),
    path('wells/rig/', include('rig.urls')),
    path('wells/mud/', include('mud.urls')),
    path('wells/surfacepipe/', include('surfacepipe.urls')),
    path('wells/pressure/', include('pressure.urls')),
    path('wells/wellphases/', include('wellphases.urls')),
    path('wells/welltrajectory/', include('welltrajectory.urls')),
    path('wells/muddata/', include('muddata.urls')),
    path('wells/drillbitdata/', include('drillbitdata.urls')),
    path('wells/bhadata/', include('bhadata.urls')),
    path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('reset/done/',views.resetdone, name='password_reset_complete'),   
    path('pressureloss/', include('pressureloss.urls')),
    path('ticket/', include('ticket.urls')),
    path('license/', include('license.urls')),
    path('userlog/',include('userlog.urls')),


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)