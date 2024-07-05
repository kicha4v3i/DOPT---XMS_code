from django.urls import path
from . import views

app_name = 'welltrajectory'

urlpatterns = [
    # path('', views.Projectslist, name='projects'),
    # path('create', views.Projectscreate, name='projectscreate'),
    path('<int:well_id>/', views.details, name='detail'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('create/<int:well_id>/', views.create, name='create'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('importdata/<int:well_id>/', views.importdata, name='importdata'),
    path('download_csv_data/<int:well_id>/', views.download_csv_data, name='download_csv_data'),
    path('welltrajectorytvdcal',views.welltrajectorytvdcal,name="welltrajectorytvdcal"), 
    path('download_welltrajectory/<int:well_id>/',views.download_welltrajectory,name="download_welltrajectory"),  
    path('gettrajectory/',views.gettrajectory,name="gettrajectory"),  

]
