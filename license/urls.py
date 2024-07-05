from django.urls import path
from . import views

app_name = 'license'

urlpatterns = [
    path('listlicense', views.listlicense, name='listlicense'),
    path('createlicense/', views.CreateLicense.as_view(), name='createlicense'),
    path('upgradelicense', views.UpgradeLicense.as_view(), name='upgradelicense'),
    path('success',views.success,name="success"),
    path('changepassword', views.Changepassword.as_view(), name='changepassword'),
    path('checkoldpassword/',views.checkoldpassword,name="checkoldpassword"),
    path('editprofile/<int:id>/',views.Editprofile.as_view(),name="editprofile"),
    path('editcompanyprofile/',views.Editcompanyprofile.as_view(),name="editcompanyprofile"),



    
    


]
