from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # path('', views.Projectslist, name='projects'),
    # path('create', views.Projectscreate, name='projectscreate'),

    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('createprojectusers/<int:project_id>/', views.createprojectusers, name='createprojectusers'),
    path('create/', views.create, name='create'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('permission/<int:project_id>/', views.permission, name='permission'),
    path('notifications/', views.Notifications, name='notifications'),
    path('markallread/', views.markallread,name="markallread"),
    path('notifications_datatable',views.notifications_datatable,name="notifications_datatable"),
    path('check_user_hasproject',views.check_user_hasproject,name="check_user_hasproject"),
    path('migrateuser/<int:user_id>/', views.Migrateuser.as_view(), name='migrateuser'),



]
