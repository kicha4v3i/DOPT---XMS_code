from django.urls import path
from . import views

app_name = 'mud'

urlpatterns = [
    # path('', views.Projectslist, name='projects'),
    # path('create', views.Projectscreate, name='projectscreate'),
    path('<int:well_id>/', views.details, name='detail'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('create/<int:well_id>/', views.create, name='create'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('manufacturer', views.manufacturerindex, name='manufacturerindex'),
    path('manufacturer/edit/<int:pk>/', views.manufactureredit, name='manufactureredit'),
    path('manufacturer/create/', views.manufacturercreate, name='manufacturercreate'),
    path('pump', views.pumpindex, name='pumpindex'),
    path('pump/edit/<int:pk>/', views.pumpedit, name='pumpedit'),
    path('pump/view/<int:pk>/', views.pumpview, name='pumpview'),
    path('pump/create/', views.pumpcreate, name='pumpcreate'),
    path('getpumps',views.getpumps,name="getpumps"),
    path('getpump',views.getpump,name="getpump"),
    path('manufacturer/delete/<int:pk>/', views.manufacturerdelete, name='manufacturerdelete'),
    path('pump/delete/<int:pk>/', views.pumpdelete, name='pumpdelete'),
    path('adminmanufacturer/create/', views.adminmanufacturercreate, name='adminmanufacturercreate'),
    path('adminmanufacturer', views.adminmanufacturerindex, name='adminmanufacturerindex'),
    path('adminmanufacturer/edit/<int:pk>/', views.adminmanufactureredit, name='adminmanufactureredit'),
    path('adminmanufacturer/delete/<int:pk>/', views.adminmanufacturerdelete, name='adminmanufacturerdelete'),
    path('adminpump/create/', views.adminpumpcreate, name='adminpumpcreate'),
    path('adminpump', views.adminpumpindex, name='adminpumpindex'),
    path('adminpump/delete/<int:pk>/', views.adminpumpdelete, name='adminpumpdelete'),
    path('adminpump/edit/<int:pk>/', views.adminpumpedit, name='adminpumpedit'),
    path('adminpump/view/<int:pk>/', views.adminpumpview, name='adminpumpview'),
    path('flowratecalculation',views.flowratecalculation,name="flowratecalculation"),

]
