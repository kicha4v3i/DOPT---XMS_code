from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.http import HttpResponse,BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings
from custom_auth.helpers import getcurrenturl
from custom_auth.models import Companies




def confirmation_of_licenseupdate(user,request):
    subject = 'DOPT License Upgrade Confirmation'

    email = user.email 
    name = user.name
    gender = user.title
    license_type = user.licence_type 
    company_name = None

    if(license_type == "CompanyPlan"):
        company = Companies.objects.get(userid_id=user.id)
        company_name = company.company_name
 

    html_message = render_to_string('mail/update_license_conformation.html',{'gender':gender,'license_type':license_type,'company_name':company_name,'request':request,'user':user})
    print('user_id_pay',user)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

