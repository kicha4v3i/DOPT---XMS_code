from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'ticket'

urlpatterns = [

    path('queries',views.queries,name="queries"),
    path('query_form',views.query_form,name="query_form"),
    path('query_chat',views.query_chat,name="query_chat"),
    path('query_chat_message',views.query_chat_message,name="query_chat_message"),
    path('getalltickets',views.getalltickets,name="getalltickets"),
    path('startticket/<int:id>/', views.startticket, name='startticket'),
    path('poaqueries',views.poaqueries,name="poaqueries"),
    path('getallpoatickets',views.getallpoatickets,name="getallpoatickets"),
    path('email_query',views.Emailquery.as_view(),name="email_query"),
    path('viewticket/<int:id>/', views.Viewticket.as_view(), name='viewticket'),
    path('download_attachment/<int:attachment_id>/', views.download_attachment, name='download_attachment'),
    path('file_upload', views.file_upload, name='file_upload'),
    path('sendmessage', views.Sendmessage.as_view(), name='sendmessage'),




  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
