from django.urls import path
from . import views
from django.contrib.auth import views as auth_views #import this

app_name = 'custom_auth'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('', views.Dashboard, name='dashboard'),
    path('countrysearch/',views.countrysearch,name='countrysearch'),
    path('logout/', views.Logout, name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('adminlogin/', views.AdminLoginView.as_view(), name='adminlogin'),
    path('underconstruction/', views.UnderConstruction, name='underconstruction'),
    path('company/list/', views.Companieslist, name='companies'),
    path('company/views/<int:id>/<str:license_type>', views.Companiesview, name='companyview'),
    path('company/approve/<int:id>/', views.Companiesapprove, name='companyapprove'),
    path('company/reject/<int:id>/', views.Companiesreject, name='companyreject'),
    path('adminusers/', views.AdminUserlist, name='adminusers'),
    path('adminusers/<int:pk>/', views.AdminUserview, name='adminuserdetail'),
    path('adminusers/create/', views.AdminUsercreate, name='adminusercreate'),
    path('adminusers_create',views.AdminUser_create,name='admin_user_create'),
    path('adminusers_edit/<int:id>/',views.AdminUser_edit,name='admin_user_edit'),
    path('adminusers/delete/<int:pk>/', views.AdminUserdelete, name='adminuserdelete'),
    path('users/', views.Userlist, name='users'),
    
    path('user_create/',views.CreateUser, name='user_create'),
    path('edit_user/<int:id>/',views.EditUser,name='edit_user'),
    path('users_rights/', views.UserRights, name='users_rights'),
    path('users/<int:id>/', views.Userview, name='userdetail'),
    path('users/create/', views.Usercreate, name='usercreate'),
    path('users/delete/<int:pk>/', views.Userdelete, name='userdelete'),
    path('companymailexists/', views.Companymailexists, name='companymailexists'),
    path('usermailexists/', views.Usermailexists, name='usermailexists'),
    path('countryphonecode/', views.Countryphonecode, name='countryphonecode'),
    path('getconcurrentusers',views.getconcurrentusers,name="getconcurrentusers"),
    path('getuserscount',views.getuserscount,name="getuserscount"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('forgetpassword/<uidb64>/<token>/',   views.Forgotpassword.as_view(), name='forgetpassword'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('enquiry/<str:licence_name>/', views.enquiry, name='enquiry'),
    path('enquiries', views.enquiries, name='enquiries'),
    # path('approveenquiry/<int:id>/', views.approveenquiry, name='approveenquiry'),
    path('company_signup',views.company_signup,name='company_signup'),
    path('create_password',views.create_password,name='create_password'),
    path('addinvoice', views.addinvoice, name='addinvoice'),
    path('license_check', views.license_check, name='license_check'),
    path('license_details', views.license_details, name='license_details'),
    path('create_common_permissions/<int:id>/', views.create_common_permissions, name='create_common_permissions'),
    # path('create_projects_permissions/<int:id>/', views.create_projects_permissions, name='create_projects_permissions'),
    path('getuserrights', views.getuserrights, name='getuserrights'),
    path('getcountrycode', views.getcountrycode, name='getcountrycode'),
    path('notifications/', views.Notifications, name='notifications'),
    path('markallread/', views.markallread,name="markallread"),
    path('licensesignup/<str:licence_name>/',views.licensesignup,name="licensesignup"),
    path('success/',views.success,name="success"),
    path('success_renewal/',views.success_renewal,name="success_renewal"),
    
    path('license_upgrade',views.license_upgrade,name="license_upgrade"),
    # path('notify-table-view',views.notify-table-view,name='notify-table-view')
    # path('notify_endpoint',views.notify_endpoint,name="notify_endpoint")
    path('getindividuals/', views.getindividuals, name="getindividuals"),
    path('getcompanies/<str:license_type>/', views.getcompanies, name="getcompanies"),
    path('reset_password/<int:user_id>/',views.reset_password,name='reset_password'),
    path('userlog/<str:activity>/<int:well_id>/<int:user_id>/', views.userlog, name='userlog'),
    path('poauserrights/<userid>/',views.Poauserrights.as_view(), name='poauserrights'),
    path('getenquiries/', views.getenquiries, name='getenquiries'),
    path('getwelldatas', views.getwelldatas, name="getwelldatas"),
    path('download_template/',views.download_template,name='download_template'),
    path('customuserrights',views.Customuserrights.as_view(), name='customuserrights'),
    path('editcustomuserrights/<int:id>/',views.Editcustomuserrights.as_view(), name='editcustomuserrights'),

    path('view_enquiries/<int:id>/',views.view_enquiries,name='view_enquiries'),
    path('renewlicense',views.renewlicense,name='renewlicense')




]
