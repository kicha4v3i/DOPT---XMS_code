from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.http import HttpResponse,BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from helpers.commonimport import force_bytes,force_text,urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from custom_auth.helpers import getcurrenturl
from custom_auth.models import Companies
from helpers import getlogo




def send_confirmation_mail(company):
    subject = 'Email From hydraulics'
    html_message = render_to_string('mail/confirm.html', {'name': company.first_name+" "+company.last_name,'cin': company.cin})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER

    to = company.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def send_approvel_mail(company,request,payment):
    subject = 'Email From hydraulics'
    html_message = render_to_string('mail/approve.html', {'name': company.first_name+" "+company.last_name,'cin': company.cin,'request':request,'licensekey':payment.licensekey})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER

    to = company.email
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def send_proposal_conform(email,request):
    subject = 'Email From hydraulics'
    html_message = render_to_string('mail/proposal_sended.html')
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER

    to = email
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def send_reject_mail(company):
    subject = 'Email From hydraulics'
    html_message = render_to_string('mail/reject.html', {'name': company.first_name+" "+company.last_name,'cin': company.cin})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER

    to = company.email
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def send_passwordchange_mail(user,request):
    subject = "DOPT - Forgot Password"
    email_template_name = "password/password_reset_email.txt"
    from_email = settings.EMAIL_HOST_USER

    current_url=f'{request.scheme}://{request.get_host()}'


    maildetails = {
    "email":user.email,
    "name":user.name,
    "title":user.title,
    "last_name":user.lastname,
    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
    "user": user.name,
    'token': default_token_generator.make_token(user),
    'request':request,
    'protocol': 'https',
    'domain':'hydraulics.mo.vc',
    'current_url':current_url,
    'logo':getlogo()
    }

    html_message = render_to_string('mail/reset.html',  maildetails)
    plain_message = strip_tags(html_message)
    try:
        mail.send_mail(subject, plain_message, from_email, [user.email], html_message=html_message)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

def send_userconfirmation_mail(user,request,current_user,group,groupname,email,password):
    subject = 'DOPT Login Credentials'
    role=user.designation if user.is_superuser == 1 else group
    url=f'{request.scheme}://{request.get_host()}'

    html_message = render_to_string('mail/userconfirm.html', {'password': request.POST.get('password'),'email': user.email,'name': user.name,'lastname':user.lastname,'company':request.company.company_name,'title':user.title,'current_user':current_user,'groupname':groupname,'email':email,'password':password,'role':role,'url':url})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER

    to = user.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def send_adminuserconfirmation_mail(user,request,current_user,password):
    subject = 'DOPT Login Credentials'
    url=f'{request.scheme}://{request.get_host()}'
    html_message = render_to_string('mail/adminuserconfirm.html', {'email': user.email,'name': user.name,'lastname':user.lastname,'title':user.title,'current_user':current_user,'role':user.designation,'password':password,'url':url})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def send_reset_password(request,user,password):
    print('request',request,password)
    subject = 'DOPT - Request for Password Reset'
    html_message = render_to_string('mail/reset_password.html', {'user':user,'password':password,'logo':getlogo()})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER

    to = user.email 
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    
def send_proposal_mail(enquiry,request):
    
    subject = 'DOPT Login Credentials'
    url='https://hydraulics.mo.vc/create_password/'
    print('enquiry_details',enquiry.name)
    html_message = render_to_string('mail/proposal.html',{'enquiry': enquiry,'url':url,'request':request})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    
    to = enquiry.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def confirmation_of_enquiry(email,name,last_name,gender,request):
    subject = 'DOPT Enquiry Acknowledgement'
    html_message = render_to_string('mail/enquiry.html',{'email':email,'name':name,'last_name':last_name,'gender':gender,'request':request})
    print('name_enquiry',gender,name,last_name)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    
    to = email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def confirmation_of_payment(user,request):
    subject = 'DOPT Payment Confirmation'

    email = user.email 
    name = user.name
    gender = user.title
    license_type = user.licence_type 
    company_name = None

    if(license_type == "CompanyPlan"):
        company = Companies.objects.get(userid_id=user.id)
        company_name = company.company_name
        end_date=company.end_date
    else:
        end_date=user.end_date
    url=f'{request.scheme}://{request.get_host()}'

    html_message = render_to_string('mail/payment.html',{'gender':gender,'license_type':license_type,'company_name':company_name,'request':request,'end_date':end_date,'user':user,'url':url})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    
    to = email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def confirmation_of_companyregister(email,firstname,lastname,title,designation,companyname,password,request):
    subject = 'DOPT Company Registration Acknowledgement'
    html_message = render_to_string('mail/company_register.html',{'email':email,'firstname':firstname,'lastname':lastname,'title':title,'designation':designation,'companyname':companyname,'password':password,'request':request})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER 
    to = email 
    return mail.send_mail(subject,plain_message,from_email,[to],html_message=html_message)