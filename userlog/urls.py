from django.urls import path
from . import views
from django.conf import settings

app_name = 'userlog'

urlpatterns = [
    path('list',views.user_list,name="list"),
    path('proj_list',views.proj_list,name="proj_list"),
    path('well_list/<int:proj_id>/',views.well_list,name="well_list"),
    path('well_list_users/<int:well_id>/',views.well_list_users,name="well_list_users"),
    path('proj_list_users/<int:proj_id>/',views.proj_list_users,name="proj_list_users"),
    path('getuserlog/', views.getuserlog, name='getuserlog'),
    path('search/', views.search_view, name='search'),

    
  
]