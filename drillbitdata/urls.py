from django.urls import path
from . import views

app_name = 'drillbitdata'

urlpatterns = [
    path('<int:pk>/', views.details, name='detail'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('create/<int:wellphase_id>/', views.create, name='create'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('drillbitlist/<int:wellphase_id>/', views.drillbitlist, name='drillbitlist'),
    path('edit_actual/<int:wellphase_id>/', views.edit_actual, name='edit_actual'),
    path('delete_actual/<int:wellphase_id>/', views.delete_actual, name='delete_actual')
]