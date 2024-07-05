from custom_auth.models import Companies,User
from notifications.models import Notification
import django.utils.timezone



# def tenant_middleware(get_response):
#     def middleware(request):
#         if request.user.is_authenticated:
#             try:
#                 company = Companies.objects.get(pk=request.user.company_id)
#             except Companies.DoesNotExist:
#                 company = None
#             # and it to the request
#             request.company = company
            
#             # all done, the view will receive a request with a tenant attribute
#         return get_response(request)

#     return middleware

def tenant_middleware(get_response):
    def middleware(request):
        zone=request.COOKIES.get('timezone')
        if zone:
            django.utils.timezone.activate(zone)
            
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            group = user.groups.first()
            if(group):
                request.role=group.name
            try:
                company = Companies.objects.get(pk=request.user.company_id)
            except Companies.DoesNotExist:
                company = None
            request.company = company
            id = request.GET.get('msgid', '')
            if id:
                Notification.objects.get(pk=id).mark_as_read()

        return get_response(request)

    return middleware
