from django.urls import path
from . import views

app_name = 'wellphases'

urlpatterns = [
    # path('', views.Projectslist, name='projects'),
    # path('create', views.Projectscreate, name='projectscreate'),

    path('<int:well_id>/', views.details, name='detail'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('create/<int:well_id>/', views.create, name='create'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    
    # Admin Master
    # path('admincasinggrade', views.admincasinggradeindex, name='admincasinggradeindex'),
    # path('admincasinggrade/create/', views.admincasinggradecreate, name='admincasinggradecreate'),
    # path('admincasinggrade/edit/<int:pk>/', views.admincasinggradeedit, name='admincasinggradeedit'),
    # path('admincasinggrade/delete/<int:pk>/', views.admincasinggradedelete, name='admincasinggradedelete'),
    path('admincasing', views.adminmastercasingindex, name='adminmastercasingindex'),
    path('admincasing/create/', views.adminmastercasingcreate, name='adminmastercasingcreate'),
    path('admincasing/edit/', views.adminmastercasingedit, name='adminmastercasingedit'),
    # path('admincasing/delete/<int:pk>/', views.adminmastercasingdelete, name='adminmastercasingdelete'),
    # path('admincasingrange', views.admincasingrangeindex, name='admincasingrangeindex'),
    # path('admincasingrange/create/', views.admincasingrangecreate, name='admincasingrangecreate'),
    # path('admincasingrange/edit/<int:pk>/', views.admincasingrangeedit, name='admincasingrangeedit'),
    # path('admincasingrange/delete/<int:pk>/', views.admincasingrangedelete, name='admincasingrangedelete'),

    #client Master
    path('clientcasing', views.clientmastercasingindex, name='clientmastercasingindex'),
    path('clientcasing/create/', views.clientmastercasingcreate, name='clientmastercasingcreate'),
    path('clientcasing/edit/', views.clientmastercasingedit, name='clientmastercasingedit'),

    # path('clientcasing/edit/<int:pk>/', views.clientmastercasingedit, name='clientmastercasingedit'),
    # path('clientcasing/delete/<int:pk>/', views.clientmastercasingdelete, name='clientmastercasingdelete'),
    # path('clientcasinggrade', views.clientcasinggradeindex, name='clientcasinggradeindex'),
    # path('clientcasinggrade/create/', views.clientcasinggradecreate, name='clientcasinggradecreate'),
    

    # path('casingrange',views.casingrangeindex, name='casingrangeindex'),
    # path('casingrange/create/', views.casingrangecreate, name='casingrangecreate'),
    # path('casingrange/edit/<int:pk>/', views.casingrangeedit, name='casingrangeedit'),
    # path('casingrange/delete/<int:pk>/', views.casingrangedelete, name='casingrangedelete'),

    # path('admincasingrange', views.admincasingrangeindex, name='admincasingrangeindex'),
    # path('admincasingrange/create/', views.admincasingrangecreate, name='admincasingrangecreate'),
    # path('admincasingrange/edit/<int:pk>/',views.admincasingrangeedit,name='admincasingrangeedit'),
    # path('admincasingrange/delete/<int:pk>/', views.admincasingrangedelete, name='admincasingrangedelete'),

    path('getmdtvd', views.getmdtvd, name='getmdtvd'),
    path('importdata', views.importdata, name='importdata'),
    path('getcasingweight', views.getcasingweight, name='getcasingweight'),
    path('insertrange', views.insertrange, name='insertrange'),
    path('insertgrade', views.insertgrade, name='insertgrade'),
    path('getcasing_connection_type', views.getcasing_connection_type, name='getcasing_connection_type'),
    path('getplanwellpage_byactualwell', views.getplanwellpage_byactualwell, name='getplanwellpage_byactualwell'),
    path('wellphase_casing', views.wellphase_casing, name='wellphase_casing'),
    path('getcasing_driftID', views.getcasing_driftID, name='getcasing_driftID'),
    path('casing_download_csv_data', views.casing_download_csv_data, name='casing_download_csv_data'),
    path('checkwellphase', views.checkwellphase, name='checkwellphase'),
    path('getmdtvd_actualwell', views.getmdtvd_actualwell, name='getmdtvd_actualwell'),
    path('wellphasesummary/<int:well_id>/',views.wellphasesummary,name='wellphasesummary'),


]
