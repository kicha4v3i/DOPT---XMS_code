from django.urls import path
from . import views

app_name = 'rig'

urlpatterns = [
   
    path('<int:well_id>/', views.details, name='detail'),
    # path('edit/<int:pk>/', views.edit, name='edit'),
    path('create/<int:well_id>/', views.create, name='create'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('alldetails/<int:well_id>/', views.alldetails, name='alldetails'),
    path('all_edit/<int:pk>/', views.all_edit, name='all_edit'),

]
