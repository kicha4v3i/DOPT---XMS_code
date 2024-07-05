from django.urls import path
from . import views

app_name = 'wells'

urlpatterns = [
    # path('', views.Projectslist, name='projects'),
    # path('create', views.Projectscreate, name='projectscreate'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.WellDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('createwellusers/<int:well_id>/', views.createwellusers, name='createwellusers'),
    path('create/', views.create, name='create'),
    path('create/<int:project_id>/', views.create, name='createwithproject'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('create/getplanwells',views.getplanwells,name="getplanwells"),
    path('getwelldetailsbyid',views.getwelldetailsbyid,name="getwelldetailsbyid"),
    path('selectedunit',views.selectedunit,name="selectedunit"),
    path('getprojectblock',views.getprojectblock,name="getprojectblock"),
    path('getblockfield',views.getblockfield,name="getblockfield"),

]
