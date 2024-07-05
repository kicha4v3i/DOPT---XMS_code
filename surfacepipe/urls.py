from django.urls import path
from . import views

app_name = 'surfacepipe'

urlpatterns = [
    # path('', views.Projectslist, name='projects'),
    # path('create', views.Projectscreate, name='projectscreate'),

    path('<int:well_id>/', views.details, name='detail'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('create/<int:well_id>/', views.create, name='create'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    # path('surface_name', views.surface_name)

]
