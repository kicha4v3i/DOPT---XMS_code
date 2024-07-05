from django.urls import path
from . import views

app_name = 'pressure'

urlpatterns = [
    path('<int:well_id>/', views.details, name='detail'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('create/<int:well_id>/', views.create, name='create'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('importpressure/<int:well_id>/', views.importpressure, name='importpressure' ),
    path('download_xls_data/<int:well_id>/', views.download_xls_data, name='download_xls_data' ),
    path('getinterpolatedata', views.getinterpolatedata, name='getinterpolatedata' ),

    

]
