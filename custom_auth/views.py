import json
from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.views.generic.edit import FormView
from matplotlib.font_manager import json_dump, json_load
from requests import request
from django.http import HttpResponseServerError
import requests
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from custom_auth.models import Companies,User,Countries,Packages,PackageConcurrentUsers,PackageUsers,CompanyPackages,Basecountries,Payments,Modules,Userlog,CountryUsers
# from projects.models import Userrights,Projectuserrights
from django.contrib.auth.hashers import check_password
from custom_auth.mailer import send_confirmation_mail,confirmation_of_enquiry,send_approvel_mail,send_reject_mail,send_passwordchange_mail,send_userconfirmation_mail,send_proposal_mail,send_proposal_conform,confirmation_of_companyregister,confirmation_of_payment,send_reset_password,send_adminuserconfirmation_mail
from django.views.generic import ListView, DetailView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from notifications.signals import notify
from custom_auth.helpers import generatecin
from django.core import serializers
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from custom_auth.getunit import adduserlog,getprojectunit,getcountries
import uuid
from helpers import *
from projects.models import Projects,ProjectField
from notifications.models import Notification
from wells.models import Wells
from django.db.models import Count,Prefetch
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
stripe.api_key = settings.STRIPE_SECRET_KEY
from urllib.parse import urlencode
from custom_auth.helpers import generate_random_password
from django.utils.http import urlsafe_base64_encode
import base64
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from helpers.allmodels import Rights,Enquiry,Poamainmodules,ProjectBlock
from license.models import Licensepackage
from django.views.decorators.cache import never_cache
from helpers.commonimport import JsonResponse,date, timedelta,datetime,urlsafe_base64_decode,force_text
from itertools import chain
from helpers.allmodels import ProjectBlock
import xlsxwriter 
import io
from django.core.serializers import serialize
from django.core.paginator import Paginator
from surfacepipe.models import SurfacePipe,SurfacePipeData




class SignupView(FormView):
    """sign up user view"""
    form_class = forms.SignupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('custom_auth:dashboard')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Countries.objects.all()
        context['packages'] = Packages.objects.all()
        return context

    def form_valid(self, form):
        """ process user signup"""
        postvalues=self.request.POST
        scheme=request.scheme
        gethost=request.get_host()
        company=Companies.objects.create(
            company_name=postvalues.get('company_name'),
            cin= generatecin(postvalues.get('company_name')),
            first_name=postvalues.get('name'),
            last_name=postvalues.get('last_name'),
            country_id=postvalues.get('country_id'),
            email=postvalues.get('email'),
            hydraulics=postvalues.get('hydraulics'),
            irocks=postvalues.get('irocks'),
            contact_no=postvalues.get('contact_no'),
            status=0,
        )
        CompanyPackages.objects.create(
            company=company,
            package_id=postvalues.get('package'),
            concurrent_users=postvalues.get('concurrent_users'),
            admins=postvalues.get('admins'),
            well_managers=postvalues.get('well_managers'),
            well_engineers=postvalues.get('well_engineers'),
            other_users=postvalues.get('other_users'),
            )

        send_confirmation_mail(company)
        user = form.save(commit=False)
        user.company_id=company.id
        user.set_password(form.cleaned_data['password'])
        user.save()
        sender = User.objects.get(is_superuser=1)
        recipient = User.objects.filter(is_superadmin=1)
        url=json.dumps({"url":scheme+'://'+gethost+'/company/view/'+str(company.id)})
        notify.send(sender, recipient=recipient,data=url, verb='Company got registered newly', description='New Company registered Company Name '+company.company_name,action_object=company)

        # login(self.request, user)
        messages.success(self.request, "Company Registered Successfully")
        if user is not None:
            #return HttpResponseRedirect(self.success_url)
            return redirect('/login/')

        return super().form_valid(form)

 
def license_check(request):
    if request.method == 'POST':
        licensekey=request.POST.get('licensekey')
        company=request.session['company']
        try:
            payment_key=Payments.objects.filter(company_id=company,status=1).first()
        except Payments.DoesNotExist:
            payment_key=None
        if payment_key is not None:
            if payment_key.licensekey == licensekey:
                payment_key.payment_status=2
                payment_key.save()
                return redirect('custom_auth:dashboard')
            else:
                messages.add_message(request, messages.SUCCESS, 'License key incorrect')
        else:
            messages.add_message(request, messages.SUCCESS, 'License key incorrect')
            return redirect('custom_auth:license_check')
        
    return render(request,'license_key.html') 

def getconcurrentusers(request):
    package_id = request.GET['package']
    concurrentusers=PackageConcurrentUsers.objects.filter(package=package_id)
    data = serializers.serialize('json', concurrentusers)
    return JsonResponse(data, safe=False)
    

def getuserscount(request):
    package_concurrent_id = request.GET['packageconcurrent']
    users=PackageUsers.objects.filter(package_concurrent_users=package_concurrent_id)
    data = serializers.serialize('json', users)
    return JsonResponse(data, safe=False)

@login_required(login_url='/login/')
def Dashboard(request):
    request.session['mainmenu'] = 'dashboard'
    if( not request.user.is_superuser):
        last_userlog = Userlog.objects.filter(user_id=request.user.id,status=1).last()  
       
        last_userlog_url = '/'
        last_userlog_name = ''
        
        if last_userlog:
            well_id = last_userlog.well_id
            wellphase_id = last_userlog.wellphase_id
            source_type = last_userlog.source_Type
            if source_type == 'Project' and ('Deleted' not in last_userlog.message):
                last_userlog_name = Projects.objects.get(id=last_userlog.source_id).project_name 
                last_userlog_url = '/projects/'+last_userlog.source_id+'/'
            if source_type == 'ProjectUsers' :
                last_userlog_name = Projects.objects.get(id=last_userlog.source_id).project_name 
                last_userlog_url = '/projects/createprojectusers/'+last_userlog.source_id+'/'
            if source_type == 'Well' :
                last_userlog_name = Wells.objects.get(id=last_userlog.source_id).name 
                if 'Deleted' not in last_userlog.message:
                    last_userlog_url = '/wells/'+last_userlog.source_id+'/' 
            if source_type == 'WellUsers' :
                last_userlog_name = Wells.objects.get(id=last_userlog.source_id).name 
                last_userlog_url = '/wells/createwellusers/'+last_userlog.source_id+'/'
            if source_type == 'Rig' or source_type == 'SurfacePipe' or source_type == 'Mud Pump' :
                if 'Deleted' in last_userlog.message:
                    last_userlog_url = '/'
                else:
                    last_userlog_url = '/wells/rig/alldetails/'+str(well_id)+'/'
            if source_type == 'Welltrajectory' :
                last_userlog_url = '/wells/welltrajectory/'+str(well_id)+'/'
            if source_type == 'Wellphases' :
                last_userlog_url = '/wells/wellphases/'+str(well_id)+'/'
            if source_type == 'Pore and Fracture pressure' :
                last_userlog_url = '/wells/pressure/'+str(well_id)+'/'
            if source_type == 'Mud Data' :
                last_userlog_url = '/wells/muddata/muddatarheogramlist/'+str(wellphase_id)+'/'
            if source_type == 'Drillbit' :
                last_userlog_url = '/wells/drillbitdata/drillbitlist/'+str(wellphase_id)+'/'
            if source_type == 'BHA data' :
                last_userlog_url = '/wells/bhadata/bhadatalist/'+str(wellphase_id)+'/'
            
    if (request.method == "POST") and (not request.user.is_superuser):
        country_ids = request.POST.getlist('selectedValues') 
        country_ids_list = [int(cid) for cid in country_ids]
        # if(request.user.licence_type != 'Individual'):
        #     projects_filter = Projects.objects.getproject_bygroupcountry_filtercountries(request.company.id, country_ids_list)
        # else:
        #     projects_filter = Projects.objects.getproject_bygroupcountry_indfiltercountries(request.user.id, country_ids_list)
        # projects_list = [project for project in projects_filter.values()]
        country_list = []
        for country_id in country_ids_list:
            country_name = Countries.objects.get(id=country_id).name 
            if request.company:
                project_count = Projects.objects.filter(country_id=country_id,company_id=request.company.id).count() 
                projects_ids = list(Projects.objects.filter(country_id=country_id,company_id=request.company.id).values_list('id',flat=True))
                block_count = ProjectBlock.objects.filter(project_id__in=projects_ids).count()
                wells_count = Wells.objects.filter(project_id__in=projects_ids,company_id=request.company.id).count()
            else:
                project_count = Projects.objects.filter(country_id=country_id,created_by_id=request.user.id).count() 
                projects_ids = list(Projects.objects.filter(country_id=country_id,created_by_id=request.user.id).values_list('id',flat=True))
                block_count = ProjectBlock.objects.filter(project_id__in=projects_ids).count()
                wells_count = Wells.objects.filter(project_id__in=projects_ids,created_by_id=request.user.id).count()
                
                
            country_list.append(
                {
                    'country_id':country_id,
                    'country_name':country_name,
                    'project_count':project_count,
                    'block_count':block_count,
                    'wells_count':wells_count
                        
                }
            ) 
        return JsonResponse({'status': True, 'country_list': country_list})
    if(request.user.is_superuser):
        totalindividuals=User.objects.getindividuals_count()
        totalcompanies=Companies.objects.getcompaniescount('CompanyPlan')
        totalenterprise=Companies.objects.getcompaniescount('Enterprise')
        totalEnquiries = Enquiry.objects.getenquirycount()
        totaluserenquiry=0
        for enquiry in totalEnquiries:
            if enquiry['form_type'] == 'enterprise':
                totalenquiryenterprise = enquiry['count'] 
            elif enquiry['form_type'] == 'enquiry':
                totaluserenquiry = enquiry['count'] 
        totalpoausers = User.objects.getpoausercount()
        data={
            'totalindividuals':totalindividuals,
            'totalcompanies':totalcompanies,
            'totalenterprise':totalenterprise,
            'totalenquiryenterprise':totalenquiryenterprise,
            'totaluserenquiry':totaluserenquiry,
            'totalpoausers':totalpoausers
        }
        return render(request, 'dashboardsuperuser.html',{'data':data})
    else:
        if(request.user.licence_type != 'Individual'):
            projects=Projects.objects.getproject_bygroupcountry(request)
        else:
            projects=Projects.objects.getproject_bygroupcountry_individual(request.user.id)
        return render(request, 'dashboard.html',{'projects':projects,'request':request,'last_userlog_name':last_userlog_name,'last_userlog_url':last_userlog_url,'last_userlog':last_userlog,'last_userlog':last_userlog})
        # return render(request, 'dashboard.html',{'projects':projects,'request':request,})
    
def countrysearch(request):
    country_search_value = request.POST.get('country_search_value')
    country_ids = Projects.objects.filter(company_id=request.company.id).values_list('country_id')
    countries = Countries.objects.filter(id__in=country_ids)
    country_results = []
    for country in countries:
        if country_search_value.lower() in country.name.lower():
            country_results.append({
                'country_id': country.id,
                'country_name': country.name
            })

    
    return JsonResponse(country_results,safe=False)

@login_required(login_url='/login/')
def Companieslist(request):
    if 'active_subscriber_menu' in request.session:
        active_subscriber_menu = request.session['active_subscriber_menu']
    else:
        active_subscriber_menu='CompanyPlan'
    return render(request, 'subscriberlist.html',{'subscriber_menu':active_subscriber_menu})

def Companymailexists(request):
    """ make company view """
    email = request.GET.get('email', '')
    if email is not None:
        obj = Companies.objects.filter(email=email).exists()
        data = {
            'email': obj,
        }
        return JsonResponse(data)

def Usermailexists(request):
    email = request.GET.get('email', '')
    idvalue = request.GET.get('id', '')
    if email is not None:
        if(idvalue):
            obj = User.objects.filter(email=email,is_active=1).exclude(id=idvalue).exists()
        else:
            obj = User.objects.filter(email=email,is_active=1).exists()
        data = {
            'email': obj,
        }
        print(f"dataobjmailexists {obj}")
        return JsonResponse(data)

def Countryphonecode(request):
    """ make company view """
    country_id = request.GET.get('country_id', '')
    if country_id is not None:
        obj = Countries.objects.get(id=country_id)
        data = {
            'phonecode': obj.phonecode,
        }
        return JsonResponse(data)

@login_required(login_url='/login/')
def Companiesapprove(request, id):  
    scheme=request.scheme
    gethost=request.get_host()
    date=datetime.datetime.now().strftime ("%d-%m-%Y")
    timestamp=dateconversion(date)
    companyupdate =  Companies.objects.filter(pk=id).update(status= 1)
    company =  Companies.objects.get(id=id)
    license_key=Payments.objects.filter(company_id=id,status=1).first()
    license_key.payment_status=1
    license_key.approved_timestamp=timestamp
    license_key.approved_date=convertdateformat(date)
    license_key.save()
    payment_details=Payments.objects.filter(company_id=id)
    if payment_details.count()>1:
        payment_detail=Payments.objects.filter(company_id=id).first()
        sender = User.objects.get(is_superuser=1)
        recipient = User.objects.filter(company=id).first()
        url=json.dumps({"url":scheme+'://'+gethost+'/license_details'})
        notify.send(sender, recipient=recipient, verb='License was approved',data=url, description='License was approved successfully',action_object=payment_detail)          
            
    send_approvel_mail(company,request,license_key)
    messages.success(request, "Company Approved Successfully")
    return redirect("/company/list")

@login_required(login_url='/login/')
def Companiesreject(request, id):  
    company =  Companies.objects.filter(pk=id).update(status= 2)
    company =  Companies.objects.get(id=id)
    send_reject_mail(company)
    messages.error(request, "Company Rejected Successfully")
    return redirect("/company/list")
    
@login_required(login_url='/login/')
def Companiesview(request, id,license_type): 
    request.session['active_subscriber_menu']=license_type
    if request.method == "POST":
        result = request.POST.get('enquiry_result')
        enquiry_data = Enquiry.objects.get_enquirybyid(result)
        status = request.POST.get('status')
        if status == "accept":
            if license_type == "Individual":
                no_of_users = 1 
                recipient = User.objects.getuserid(id)
            else:
                company_details = Companies.objects.getcompanyname_byid(id)
                no_of_users = company_details.no_of_users
                recipient = User.objects.getadminuser(company_details.id)

                
                
            no_of_users_new = enquiry_data.no_of_users 
            enquiry = Enquiry.objects.get_enquirybyid(result)
            
            Enquiry.objects.update_status_enquiry(result,1)
            
            if enquiry_data.user_type != "Individual":
                User.objects.update_userlicense_company(enquiry_data.user_type_id,"Enterprise")
                Companies.objects.updatecompany_noofusers(enquiry_data.user_type_id,enquiry_data.no_of_users,'Enterprise')
                company = Companies.objects.filter(company_name=enquiry.company_name).first()
            else:
                user = User.objects.getuserid(enquiry_data.user_type_id)
                company = Companies.objects.createcompany(enquiry_data.company_name,None,enquiry_data.name,enquiry_data.last_name,enquiry_data.email,1,enquiry_data.user_type_id,user.subscription_type,user.start_date,user.end_date,enquiry_data.no_of_users,'Enterprise')
                User.objects.update_userlicense_individual(enquiry_data.user_type_id,enquiry.designation,"Enterprise",company.id)
            CompanyPackages.objects.createcompany_package(company.id,enquiry_data.no_of_users,'Enterprise') 
            sender = User.objects.getuserid(request.user.id)
            scheme=request.scheme
            gethost=request.build_absolute_uri()
            url=json.dumps({"url":scheme+'://'+gethost})
            notify.send(sender=sender, recipient=recipient,extra_data=url, verb='License Upgraded', description='Your License has been Upgraded from '+ str(no_of_users) +' Users to '+ str(no_of_users_new))
        else:
            Enquiry.objects.get_enquirybyid(result).delete()

    scheme=request.scheme
    gethost=request.build_absolute_uri()
    if(license_type=='Individual'):
        data = User.objects.getuserid(id)
        subscription_type=data.subscription_type
        getmainuser_details={}
    else:
        data = Companies.objects.getcompanyname_byid(id)
        subscription_type=data.subscription_type
        getmainuser_details=User.objects.getadminuser(id)

    licences = CompanyPackages.objects.getcompany_current_package(id,license_type)
    payment_details=Payments.objects.getpayments(id,license_type)
    # all_payment=Payments.objects.filter(company_id=id)
    # company_payment=Payments.objects.filter(company_id=id,status=1).last()
    # checkenquiry=Enquiry.objects.get_enquirybyuser_type(request.user.company_id,)

    currencies=Basecountries.objects.all()
    return render(request,'company/view.html', {'data':data,'licences':licences,'payment_details':payment_details,'currencies':currencies,'license_type':license_type,'subscription_type':subscription_type,'getmainuser_details':getmainuser_details})
 
 
@login_required(login_url='/login/')   
def CreateUser(request):
    type_of_service = request.GET.get('type', '')
    countries = Countries.objects.all()
    groups = Group.objects.filter(name__in=["Admin", "Creator","Editor","Viewer"])
    user_modules = Modules.objects.getmodules(1)
    print('user_modules_create_user',user_modules)
    return render(request,'users/create_user.html',
    {
    'groups':groups,
    'countries':countries,
    'request':request,
    'type_of_service':type_of_service,
    'user_modules':user_modules
    })
    
@login_required(login_url='/login/')
def EditUser(request,id):

    user = User.objects.getuserid(id) 
    groups = Group.objects.filter(name__in=["Admin", "Creator","Editor","Viewer"])
    user_group = user.groups.all().first()
    group_id = Group.objects.filter(name=user_group).first()
    rights_ids = list(Rights.objects.filter(role_id=group_id,status=1).values_list('module_id',flat=True))
    
    scheme=request.scheme
    gethost=request.get_host()
    user_modules = Modules.objects.getmodules(1)
    if request.method == "POST":
        if(request.POST.get('group')=='new'):
            request.session['userdata']=request.POST
            return redirect('custom_auth:editcustomuserrights',id)
        else:
            sender = User.objects.get(id=id)
            url=json.dumps({"url":scheme+'://'+gethost+'/users'})
            user =User.objects.get(id=id)
            existing_user = user.groups.first()
            existing_user_name=existing_user.name
            user.name=request.POST.get('name')
            user.email=request.POST.get('email')
            user.designation=request.POST.get('designation')
            default_groups=[1,2,3,4]
            if(request.POST.get('group')=='new'):
                if existing_user.id in default_groups:
                    group, created = Group.objects.get_or_create(name=request.POST.get('custom_role'))
                else:
                    group = Group.objects.get(id=existing_user.id)
                    group.name = request.POST.get('custom_role')
                    group.save()
            else:
                if not existing_user.id in default_groups:
                    existing_group = Group.objects.get(id=existing_user.id)
                    existing_group.delete()
                group = Group.objects.get(id=request.POST.get('group'))

            user.groups.clear()
            user.groups.add(group)


            user.lastname=request.POST.get('lastname')
            user.title=request.POST.get('title')
            user.groups.clear()
            user.groups.add(group)
            user.save()
            user_role_new = user.groups.first() 
            
            # user_modules = Modules.objects.getmodules(1)
            # current_ids=[]
            # for modules in user_modules:
            #     value = request.POST.get("rights"+str(modules.id))
            #     if value != None:
            #         checkcustomuserrights=Rights.objects.checkcustom_rights_exist(request.company.id,modules.id,group.id)           
            #         if(checkcustomuserrights):
            #             Rights.objects.updatepoauserrights(checkcustomuserrights[0].id)
            #         else:
            #             rights=Rights.objects.create(company_id=request.company.id,module_id=modules.id,role_id=group.id,status=1)
            #     else:
            #         checkcustomuserrights=Rights.objects.checkcustom_rights_exist(request.company.id,modules.id,group.id)
                
            #         if (checkcustomuserrights):
            #             Rights.objects.filter(company_id=request.company.id,module_id=modules.id,role_id=group.id).update(status=0)
        
            # # Rights.objects.update_userrights_excludedid(current_ids)
            if(user_role_new.name != existing_user_name):
                notify.send(sender, recipient=user,extra_data=url,verb='New User', description='Your role has been Modified from '+ existing_user_name + ' to '+user_role_new.name,action_object=user)
            return redirect("/users")
                
    return render(request,'users/edit_user.html',
    {
        'title':user.title,
        'first_name':user.name,
        'last_name':user.lastname,
        'email':user.email,
        'designation':user.designation,
        'groups':groups,
        'request':request,
        'group_id':group_id,
        'user_modules':user_modules,
        'rights_ids':rights_ids,
        'user_id':id,
     
    })

@login_required(login_url='/login/')
def Userlist(request):
    if request.method == 'POST':
        id = request.POST.get('user_id')
        return redirect('custom_auth:edit_user',id)
       
    request.session['mainmenu']  = 'users'
    user = User.objects.getuserid(request.user.id)
    groups = user.groups.all().first()
    groups_name = Group.objects.filter(name=groups).first().name
    if(request.user.licence_type!='Individual'):
        users = User.objects.getuser_bycompany(request.company,request.user.id)
    else:
        users = User.objects.getindividuals(request.user.id)
   
    user_rights_privilege = "Create User"
    user_rights_companyid = request.user.company_id
    user = User.objects.getuserid(request.user.id)
    user_rights_groups = user.groups.all().first()
    groups = Group.objects.all()
    return render(request,'users/list.html',
    {
    'data': users,
    'groups':groups,
    'countries':getcountries(request.company),
    'company':request.company,
    'user_rights_privilege':user_rights_privilege,
    'user_rights_companyid':user_rights_companyid,
    'user_rights_groups':user_rights_groups,
    'request':request
    })


@login_required(login_url='/login/')
def UserRights(request):
    request.session['mainmenu']  = 'users_rights'
    company = request.company
    user_rights = Group.objects.filter(name__in=["Admin", "Creator","Editor","Viewer"])
    user_modules = Modules.objects.getmodules(1)
    if request.method == "POST":
        value = request.POST.get('type')
        if value == "create":
            for modules in user_modules:
                for rights in user_rights:
                    value = request.POST.get(rights.name+'_'+str(modules.id))
                    if value != None:
                        Rights.objects.create(company_id=company.id,module_id=modules.id,role_id=value,status=1) 
        elif value == "edit":
            for modules in user_modules:
                for rights in user_rights:
                    value = request.POST.get(rights.name+'_'+str(modules.id))
                    boolean_rights = Rights.objects.filter(company_id=company.id,module_id=modules.id,role_id=rights.id).exists()
                    if value != None:
                        if boolean_rights == False:
                            Rights.objects.create(company_id=company.id,module_id=modules.id,role_id=value,status=1)
                        else:
                           Rights.objects.filter(company_id=company.id,module_id=modules.id,role_id=value).update(status=1) 
                    elif value == None:
                        
                        if boolean_rights == True:
                            Rights.objects.filter(company_id=company.id,module_id=modules.id,role_id=rights.id).update(status=0)

    return render(request,'users/user_rights.html',{'user_rights':user_rights,'user_modules':user_modules,'company':company})

@login_required(login_url='/login/')
def Userview(request,id):
    user = User.objects.getuserid(id)
    return render(request,'users/view.html',{'user': user})

@login_required(login_url='/login/')
def Usercreate(request):
    scheme=request.scheme
    gethost=request.get_host()
    if request.method == 'POST':
        if(request.POST.get('group')=='new'):
            request.session['userdata']=request.POST
            return redirect('custom_auth:customuserrights')
                  
        else:
            sender = User.objects.get(id=request.user.id)
            url=json.dumps({"url":scheme+'://'+gethost+'/users'})
            form = forms.SignupForm(request.POST)
            current_user = User.objects.getuserid(request.user.id)
            group_names = current_user.groups.values_list('name', flat=True)
            type_of_service=request.POST.get('type_of_service')
            if form.is_valid():
                password=generate_random_password()
                current_user = User.objects.getuserid(request.user.id)
                groupdata = current_user.groups.first()
                user=form.save()
                user.set_password(password)
                user.company=request.company
                user.is_active=1
                user.licence_type = current_user.licence_type 
                user.start_date = current_user.start_date
                user.end_date = current_user.end_date
                user.subscription_type = current_user.subscription_type
                user.save()
                messages.success(request, "User is created successfully")
                if(request.user.licence_type !='Individual'):
                    if(request.POST.get('group')=='new'):
                        group, created = Group.objects.get_or_create(name=request.POST.get('custom_role'))
                    else:
                        group = Group.objects.get(id=request.POST.get('group'))
                    user.groups.add(group)
                    user_modules = Modules.objects.getmodules(1)
                    for modules in user_modules:
                        value = request.POST.get("rights"+str(modules.id))
                        if value != None:
                            Rights.objects.create(company_id=request.company.id,module_id=value,status=1,role_id=group.id)   

                    send_userconfirmation_mail(user,request,current_user,group,groupdata.name,request.POST.get('email'),password)
                    
                    notify.send(sender, recipient=user,extra_data=url,verb='Role assigned', description='You have been assigned as '+group.name,action_object=user)
                    userlog=adduserlog('User Created',request,user.id,'User',current_user.licence_type,None,None,None)
                return redirect("/users")
            else:
                return redirect("/users")
    form = forms.SignupForm()

    return render(request,'users/list.html',{'form': form})


def Userdelete(request, pk):
    user = get_object_or_404(User, pk=pk)
    User.objects.updateuser(pk)
    data = {
        'status': "success",
    }
    return JsonResponse(data)
   

@login_required(login_url='/adminlogin/')
@never_cache
def AdminUserlist(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        print('user_id_admin',user_id)
        return redirect('custom_auth:admin_user_edit',user_id)
    data = User.objects.getpoausers(request.user.id)
    return render(request,'admin/users/list.html',{'data': data})

@login_required(login_url='/adminlogin/')
def AdminUserview(request,id):
    data = User.objects.get(pk=id)
    return render(request,'admin/users/view.html',{'data': data})


@login_required(login_url='/adminlogin/')
def AdminUser_create(request):
    countries = Countries.objects.all()
    return render(request,'admin/users/create.html',{'countries':countries})


@login_required(login_url='/adminlogin/')
def AdminUser_edit(request,id):
    user = User.objects.getuserid(id=id) 
    countries = Countries.objects.all()
    selected_countries = list(CountryUsers.objects.filter(userid_id=id,status=1).values_list('country_name',flat=True))
    selected_country_ids = [int(id) for id in selected_countries]
    print('selected_countriesss',selected_country_ids)
    if request.method == "POST":
        user =User.objects.getuserid(id)
        user.name=request.POST.get('name')
        user.lastname=request.POST.get('last_name')
        user.email=request.POST.get('email')
        user.designation=request.POST.get('designation')
        country_ids = request.POST.getlist('country')
        current_selected_country_ids = [int(id) for id in country_ids]
        print('current_selected_country_ids',current_selected_country_ids)
        old_ids = [] 
        for id in selected_country_ids:
            if id not in current_selected_country_ids:
                old_ids.append(id)
        for id in current_selected_country_ids:
            if id not in selected_country_ids:
                CountryUsers.objects.create_countryuser(user.id,1,id) 
        CountryUsers.objects.update_countryuser(user.id,old_ids,0)
        user.is_superuser=1
        user.save() 
        messages.add_message(request, messages.SUCCESS, 'User Updated Successfully')
        return redirect("/adminusers") 
        
    return render(request,'admin/users/edit.html',{
        'title':user.title,
        'first_name':user.name,
        'last_name':user.lastname,
        'email':user.email,
        'designation':user.designation,
        'countries':countries,
        'selected_countries':selected_country_ids
        
    })
    
    
    
    
    
@login_required(login_url='/adminlogin/')
def AdminUsercreate(request):
    if request.method == 'POST':
        current_user = User.objects.getuserid(request.user.id)
        
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            password=generate_random_password()
            print(f"password {password}")
            user=form.save()
            user.set_password(password)
            user.lastname=request.POST.get('last_name')
            country = request.POST.getlist('country') 
            if not request.POST.get('is_allcountry'):
                for i in country:
                    CountryUsers.objects.create_countryuser(user.id,1,i)
            else:
                user.is_allcountry=1
            user.is_superuser=1
            user.is_active=1
            user.save() 
            send_adminuserconfirmation_mail(user,request,current_user,password)
            messages.add_message(request, messages.SUCCESS, 'User Created Successfully')
            return redirect("custom_auth:poauserrights",user.id)
    form = forms.SignupForm()
    return render(request,'admin/users/list.html',{'form': form})


def AdminUserdelete(request, pk, template_name='crudapp/confirm_delete.html'):
    user = get_object_or_404(User, pk=pk)
    if request.method=='POST':
        user.delete()
        return redirect('index')
    return render(request, template_name, {'object':user})

def Logout(request):
    """logout logged in user"""
    if(request.user.is_superadmin==1):
        logouturl="custom_auth:adminlogin"
    else:
        logouturl="custom_auth:login"
    current_user = request.user

    current_user.is_loggedin = 0
    current_user.save()

    logout(request)
    return HttpResponseRedirect(reverse_lazy(logouturl))

def updateuser(request):
    current_user = request.user
    current_user.is_loggedin = 0
    current_user.save()
    return HttpResponse(status=204)


def UnderConstruction(request):
    """login view"""
    return render(request, 'underconstruction.html')

# class LoginView(FormView):
#     """login view"""

#     form_class = forms.LoginForm
#     template_name = 'login.html'
    
#     def form_valid_old(self, form):
#         """ process user login"""
#         credentials = form.cleaned_data
#         try:
#             company =  Companies.objects.get(cin=credentials['cin'],status=1)
#         except Companies.DoesNotExist:
#             company = None
#         if company is not None:
#             key=Payments.objects.filter(company_id=company,status=1).first()
#         else:
#             key=None
#         if key is not None:
#             if key.payment_status == 1:
#                 success_url = reverse_lazy('custom_auth:license_check')
#             elif key.payment_status == 2:
#                 success_url = reverse_lazy('custom_auth:dashboard')
#             else:
#                 messages.add_message(self.request, messages.SUCCESS, 'Payment Pending')
#                 success_url = reverse_lazy('custom_auth:login')
#         else:
#             success_url = reverse_lazy('custom_auth:dashboard')
#         if company is None:
#             messages.add_message(self.request, messages.SUCCESS, 'CIN NO does not exists')
#             return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
#         company_id=company.id
#         user = authenticate_user(email=credentials['email'],
#         password=credentials['password'],cin=credentials['cin'],company_id=company_id)

#         if user is not None:
#             if user == 'password':
#                 messages.add_message(self.request, messages.SUCCESS, 'Incorrect Password')
#                 return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
#             else:
#                 login(self.request, user)
#                 self.request.session['company']=company.id
#                 dates=Payments.objects.filter(company_id=company.id).last()
#                 if dates.approved_date is not None:
#                     expire_date = dates.approved_date + timedelta(days=365)
#                     today_date = date.today()
#                     if today_date > expire_date: 
#                         messages.add_message(self.request, messages.SUCCESS,'Your License is expired, Please contact Admin')
#                         return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
#                     else:
#                         return HttpResponseRedirect(success_url)
#                 else:
#                     return HttpResponseRedirect(success_url)

#         else:
#             messages.add_message(self.request, messages.SUCCESS, 'Wrong credentials\
#                                 please try again')
#             return HttpResponseRedirect(reverse_lazy('custom_auth:login'))


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = 'login.html'
    
    
    
    def form_valid(self, form):
        credentials = form.cleaned_data
        user = authenticate_user(email=credentials['email'],
        password=credentials['password'])

        if user is not None:
            if user == 'password':
                messages.add_message(self.request, messages.SUCCESS, 'Incorrect Password')
                return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
            else:
                loginstatus=login(self.request, user)
                user.is_loggedin=1
                user.save()
                return HttpResponseRedirect(reverse_lazy('custom_auth:dashboard'))

        else:
            messages.add_message(self.request, messages.SUCCESS, 'Wrong credentials\
                                please try again')
            return HttpResponseRedirect(reverse_lazy('custom_auth:login'))


class AdminLoginView(FormView):

    form_class = forms.AdminLoginForm
    success_url = reverse_lazy('custom_auth:dashboard')
    template_name = 'adminlogin.html'

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data
        # user = authenticate_admin(email=credentials['email'],
        #                     password=credentials['password'], is_superuser=1)
        user = User.objects.authenticate_poauser(credentials['email'], credentials['password'])

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.SUCCESS, 'Wrong credentials\
                                please try again')
            return HttpResponseRedirect(reverse_lazy('custom_auth:adminlogin'))

def authenticate_admin(email, password,is_superadmin):
    try:
        user = User.objects.get(email=email,is_superadmin=1)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user

    return None

def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user
        else:
            return 'password'
    return None

def resetdone(request):
    messages.add_message(request, messages.SUCCESS, 'Password Changed Successfully you can login now')
    if(request.session['type']):
        usertype = request.session['type']
        if(usertype=='superadmin'):
            return HttpResponseRedirect(reverse_lazy('custom_auth:adminlogin'))
        else:
            return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
    else:
        return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
def enquiry(request,licence_name):
    scheme=request.scheme
    gethost=request.get_host()
    countries=Countries.objects.all()
    if request.method == 'POST':
        name=request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        company_name = request.POST.get('companyname')
        email=request.POST.get('email')
        message=request.POST.get('message')
        gender=request.POST.get('gender')
        country=request.POST.get('country')
        enquiry=Enquiry.objects.create(name=name,last_name=last_name,company_name=company_name,email=email,message=message,gender=gender,form_type=licence_name,country=country)
        confirmation_of_enquiry(email,name,last_name,gender,request)
        super_admin = User.objects.filter(is_superadmin=1,is_active=1) 
        user_ids = list(CountryUsers.objects.filter(country_name=country,status=1).values_list('userid_id',flat=True)) 
        superusers = User.objects.filter(id__in=user_ids) 
        recipients = superusers | super_admin
        url=json.dumps({"url":scheme+'://'+gethost+'/enquiries'})
        for recipient in recipients:
            notify.send(sender=recipient, recipient=recipient,extra_data=url,verb='New enquiry have been received', description='New Enquiry received Name '+name,action_object=enquiry)
        messages.add_message(request, messages.SUCCESS, 'Enquiry Submitted Successfully,Please wait for admin Approval')        
        return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
    return render(request,'users/enquiry.html',{'countries':countries,'licence_name':licence_name})

def addinvoice(request):
    invoice_no=request.POST.get('invoice_no')
    amount=request.POST.get('amount')
    company_id=request.POST.get('company_id')
    Payments.objects.create(invoice_no=invoice_no,amount=amount,company_id =company_id)

    data = {
        'status': 'success',
    }
    return JsonResponse(data)


def enquiries(request):

    return render(request,'users/enquiries.html',{'enquiries':enquiries})

# def approveenquiry(request,id):
#     enquiryupdate =  Enquiry.objects.filter(pk=id).update(status= 1)
#     enquiry =  Enquiry.objects.filter(pk=id).first()
#     enquiries=Enquiry.objects.all().order_by('-id')
#     send_proposal_mail(enquiry,request)
#     return HttpResponseRedirect(reverse_lazy('custom_auth:enquiries'))

def company_signup(request):
    checkpermission=poauser_rights_permission('Add Enterprise',request)
    if(checkpermission != True):
        messages.error(request,'No Access to create!')
        return redirect(request.META.get('HTTP_REFERER'))
    if request.method == 'POST':
        
        title=request.POST.get('gender')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        password=request.POST.get('new_password1')
        designation=request.POST.get('designation')
        companyname=request.POST.get('companyname')
        noofusers=request.POST.get('no_of_users')
        concurrent_users = request.POST.get('concurrent_users')
        subscription_type = request.POST.get('subscription_type') 
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        userid = User.objects.create(title=title,name=firstname,lastname=lastname,email=email,licence_type="Enterprise",designation=designation,subscription_type=subscription_type,start_date=start_date,end_date=end_date,is_active=1,is_admin=1)
        userid.set_password(password)
        userid.save()
        companies = Companies.objects.create(company_name=companyname,first_name=firstname,last_name=lastname,email=email,no_of_users=noofusers,subscription_type=subscription_type,start_date=start_date,end_date=end_date,status=1,userid_id=userid.id,licence_type="Enterprise")  
        CompanyPackages.objects.createcompany_package(companies.id,noofusers,'Enterprise')
        userid.company_id=companies.id
        userid.save()
        group = Group.objects.get(name='Admin')
        userid.groups.add(group)
        confirmation_of_companyregister(email,firstname,lastname,title,designation,companyname,password,request)
        return HttpResponseRedirect(reverse_lazy('custom_auth:companies'))
        
    return render(request,'users/company_sign.html')


def create_password(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        users = Enquiry.objects.filter(email=email).last()
        user = User.objects.create(title=users.gender,name=users.name,lastname=users.last_name,email=users.email,licence_type='Enterprise',companyname=users.company_name,password=password)
        user.set_password(password)
        user.save()
        Companies.objects.create(title=users.gender,company_name=users.company_name,first_name=users.name,last_name=users.last_name,email=users.email,status=0,userid_id=user.id)  
        return redirect('custom_auth:login')

    return render(request,'createpassword.html')


def license_upgrade(request):
    enquiries=Enquiry.objects.all().order_by('-id')
    return render(request,'licenseupgrade.html',{'enquiries':enquiries})

# old license upgrade
# def proposal(request,id):
#     scheme=request.scheme
#     gethost=request.get_host()
#     countries= Countries.objects.all()
#     packages= Packages.objects.all()
#     try:
#         company=Companies.objects.get(id=id)
#     except Companies.DoesNotExist:
#         company=None
#     if request.method=='POST':
#         company_id=request.POST.get('company_id')
#         if company_id is not None:
#             Payments.objects.filter(company_id=company_id).update(status=0)
#             CompanyPackages.objects.filter(company_id=company_id).update(status=0)
#             company=Companies.objects.filter(id=company_id).update(
#             company_name=request.POST.get('company_name'),
#             type_of_license=request.POST.get('license_type'),
#             no_of_users=request.POST.get('no_of_users'),
#             concurrentusers=request.POST.get('concurrent_users'),
#             server=request.POST.get('cloudserver'))
#             company_packages=CompanyPackages.objects.create(company_id=company_id,
#             concurrent_users=request.POST.get('concurrent_users'),
#             other_users=request.POST.get('no_of_users'),
#             package_id=request.POST.get('license_type'),server=request.POST.get('cloudserver'),status=1)
#             company_details=Companies.objects.filter(id=company_id).first()
#             sender = User.objects.get(is_superuser=1)
#             recipient = User.objects.filter(is_superadmin=1)
#             print("sender",company_id)
#             url=json.dumps({"url":scheme+'://'+gethost+'/company/view/'+str(company_id)})
#             notify.send(sender, recipient=recipient,data=url, verb='License update request has been received', description='License Update Request From '+request.POST.get('company_name'),action_object=company_details)          
#             messages.add_message(request, messages.SUCCESS, 'License Updated Successfully, please wait for Admin Approval.')
#         else:
#             company=Companies.objects.create(
#                 company_name=request.POST.get('company_name'),
#                 cin= generatecin(request.POST.get('company_name')),
#                 first_name=request.POST.get('name'),
#                 last_name=request.POST.get('last_name'),
#                 country_id=request.POST.get('country_id'),
#                 email=request.POST.get('email'),
#                 contact_no=request.POST.get('contact_no'),
#                 type_of_license=request.POST.get('license_type'),
#                 no_of_users=request.POST.get('no_of_users'),
#                 concurrentusers=request.POST.get('concurrent_users'),
#                 server=request.POST.get('cloudserver'),
#                 status=0,
#             )
#             CompanyPackages.objects.create(company_id=company.id,
#             concurrent_users=request.POST.get('concurrent_users'),
#             other_users=request.POST.get('no_of_users'),
#             package_id=request.POST.get('license_type'),server=request.POST.get('cloudserver'),status=1)
#             form = forms.SignupForm(request.POST)

#             if form.is_valid():
#                 user = form.save(commit=False)
#                 user.company_id=company.id
#                 user.set_password(form.cleaned_data['password'])
#                 user.save()
#                 sender = User.objects.get(is_superuser=1)
#                 recipient = User.objects.filter(is_superadmin=1)
#                 print("companyid",company.id)
#                 url=json.dumps({"url":scheme+'://'+gethost+'/company/view/'+str(company.id)})
#                 notify.send(sender, recipient=recipient,data=url, verb='Company got registered newly', description='New company registered Company Name '+company.company_name,action_object=company)
#                 send_proposal_conform(request.POST.get('email'),request)
#                 messages.add_message(request, messages.SUCCESS, 'License Submitted Successfully, please wait for Admin Approval.')
#         return redirect('custom_auth:login')
#     return render(request,"proposalform.html",{'packages':packages,'countries':countries,'company':company})

def addinvoice(request):
    invoice_no=request.POST.get('invoice_no')
    amount=request.POST.get('amount')
    company_id=request.POST.get('company_id')
    currency=request.POST.get('currency')
    date=request.POST.get('date')
    timestamp=dateconversion(date)
    genlicensekey= uuid.uuid4()
    Payments.objects.create(invoice_no=invoice_no,amount=amount,company_id =company_id,currency=currency,licensekey=genlicensekey,date=convertdateformat(date),timestamp=timestamp)
    data = {
        'status': 'success',
    }
    return JsonResponse(data)   

def password_reset_request(request):
    if request.method == "POST":

        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            user = User.objects.filter(email=data).first() 
            if(user is None):
                messages.error(request,'Email does not exist')
                return redirect ('custom_auth:password_reset')


            if not user.is_superuser:
                groups = user.groups.all().first()
                group_name = Group.objects.filter(name=groups).first().name
            else:
                group_name = ''
                
            if (user.is_superadmin == 1) or (group_name == "Admin") or (user.licence_type == "Individual"):
                send_passwordchange_mail(user,request)
                messages.add_message(request, messages.SUCCESS, 'Password reset Instructions are sent to your Email id')
                if(user.is_superadmin==True):
                    request.session['type']='superadmin'
                    return HttpResponseRedirect(reverse_lazy('custom_auth:adminlogin'))
                else:
                    request.session['type']='admin'
                    return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
            else:
                messages.error(request,'You didn’t have access to Reset Password. Please Contact Client Admin')
                return redirect ('custom_auth:login')
                
                    
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

def get_levels_for_project(project):
    project_name = project.project_name
    default_units = project.unit
    country = getcountryname(project.country_id)
    total_actual_wells = getnumberofwells(project.id, 'actual')
    total_plan_wells = getnumberofwells(project.id, 'plan')
    total_offset_wells = getnumberofwells(project.id, 'offset')
   
    return [project_name, default_units, country, total_actual_wells, total_plan_wells, total_offset_wells]

def get_levels_for_wells(well):
    well_name = well.name
    well_type = well.well_type
    project_name = getprojectname(well.project_id)
    block_name = getblockname(well.block_id)
    field_name = getfieldname(well.field_id)
    environment = well.environment 
    return [well_name,well_type,project_name,block_name,field_name,environment]

def download_template(request):
    
    selected_values = request.GET.get('selected_values', '').split(',')
    filter_type = request.GET.get('filter', '')
    search_value = request.GET.get('search','')
    print('--------------------',selected_values,filter_type,search_value)
    print('download_template_____',selected_values,filter_type,search_value)
    print('length_selected_ss',selected_values)
    if (selected_values == ['']):
        if request.company:
            selected_values = Projects.objects.filter(company_id=request.company.id).values_list('country_id')
        else:
            selected_values = Projects.objects.filter(created_by_id=request.user.id).values_list('country_id')
              
    if not filter_type:
        filter_type = "projects"
    print('kkk',len(selected_values),filter_type)
    # if not filter_type:
    #     filter_type = "projects"
    # if not selected_values:
    #     selected_values = [99,100]
    #     print('selected_values_projects',selected_values)
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    locked_format = workbook.add_format({'locked': True})
    unlocked_format = workbook.add_format({'locked': False})
    worksheet.protect()
    if filter_type == "wells":
        if request.company:
            total_projects = Projects.objects.filter(country_id__in=selected_values,company_id=request.company.id)  
        else:
            total_projects = Projects.objects.filter(country_id__in=selected_values,created_by_id=request.user.id)
            
        total_projects_id = [project.id for project in total_projects]
        total_wells = Wells.objects.filter(project_id__in=total_projects_id)
        total_wells = [well for well in total_wells if search_value.lower() in well.name.lower()]
        print('total_wells_download',total_wells)
        row = 0
        col = 0
        headers = ['Well Name','Well Type','Project Name','Block Name','Field Name','Environment'] 
        for header in headers:
            worksheet.write(row, col, header, locked_format)
            col += 1
        row += 1
        col = 0
        for well in total_wells:
            levels = get_levels_for_wells(well)
            print('wellLevels',levels)
            for level_data in levels:
                print('level_datas',level_data)
                worksheet.write(row, col, level_data, unlocked_format)
                col += 1
            row += 1
            col = 0
    if filter_type == "projects":
        if request.company:
            totalprojects = Projects.objects.filter(country_id__in=selected_values,company_id=request.company.id)
        else:
            totalprojects = Projects.objects.filter(country_id__in=selected_values,created_by_id=request.user.id)
        totalprojects = [project for project in totalprojects if search_value.lower() in project.project_name.lower()]  
        print('totalprojects',totalprojects)
        row = 0
        col = 0
        headers = ['Project Name','Default Units','Country','Total Actual Wells','Total Plan Wells','Total Offset Wells'] 
        for header in headers:
            worksheet.write(row, col, header, locked_format)
            col += 1
        row += 1
        col = 0
        for project in totalprojects:
            levels = get_levels_for_project(project)
            print('levels',levels)
            for level_data in levels:
                print('level_data',level_data)
                worksheet.write(row, col, level_data, unlocked_format)
                col += 1
            row += 1
            col = 0
   

    workbook.close()
    output.seek(0)
    filename = 'Table.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

def license_details(request):
    user_id = request.user.id
    user_details = User.objects.get(id=user_id)
    user_license = user_details.licence_type
    licence_type = request.GET.get('type', None)
    request.session['mainmenu']='license'
    if(user_license == "CompanyPlan" or user_license == "Enterprise"):
        user_ids=[]
        users=User.objects.getcompanyusers(request.user.company_id)
        for user in users:
            user_ids.append(user.id) 
        packages=CompanyPackages.objects.getindividual_package(user_ids,'Individual')
        company=Companies.objects.get(id=request.company.id)
        license_detail=CompanyPackages.objects.getcompany_current_package(request.company.id,user_license)
        for i in license_detail:
            print('licccc',i.created)
        return render(request,"license_details.html",{'company':company,'license_detail':license_detail,'user':user_details,'user_license':user_license,'packages':packages,'request':request,'licence_type':licence_type,'subscription_type':company.subscription_type})
    else:
        license_detail=CompanyPackages.objects.getcompany_current_package(user_id,user_license)
        
        
        return render(request,"license_details.html",{'user':user_details,'license_detail':license_detail,'packages':[],'request':request,'licence_type':licence_type,'subscription_type':request.user.subscription_type})
    
def userlog(request, activity, well_id, user_id):
    print('userlog_SSS',activity,well_id,user_id)
    return render(request, 'userlog.html',{'activity':activity,'well_id':well_id,'user_id':user_id})


def getprojectname(project_id):
    getprojectname = Projects.objects.get(id=project_id).project_name
    return getprojectname
def getblockname(block_id):
    getblockname = ProjectBlock.objects.get(id=block_id).block_name
    return getblockname
def getfieldname(field_id):
    getfieldname  = ProjectField.objects.get(id=field_id).field_name
    return getfieldname
def getcountryname(country_id):
    getcountryname = Countries.objects.get(id=country_id).name
    return getcountryname
def getnumberofwells(project_id,well_type):
    well_type_counts = Wells.objects.filter(project_id=project_id).values('well_type').annotate(count=Count('well_type'))
    if well_type == 'actual':
        for welltype in well_type_counts:
            if welltype['well_type'] == 'ACTUAL':
                return welltype['count']
    elif well_type == 'plan':
        for welltype in well_type_counts:
            if welltype['well_type'] == 'PLAN':
                return welltype['count']
    elif well_type == 'offset':
        for welltype in well_type_counts:
            if welltype['well_type'] == 'OFFSET':
                return welltype['count']
    return 0

def getprojectstatus(proj_id):
    status = Projects.objects.get(id=proj_id).status   
    if status == 1:
        return "Active"    
    else:
        return "Inactive"

def getwelldatas(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 5))
    page = int(request.GET.get('page', 1))  
    selected_values_str = request.GET.get('selected_values', '')
    filter_type = request.GET.get('filter_type','')
    search_value = request.GET.get('search_value','')

   
    if selected_values_str:
        selected_values = [int(value) for value in selected_values_str.split(',')]
    else:
        if request.company:
            selected_values = Projects.objects.filter(company_id=request.company.id,status=1).values_list('country_id')
        else:
            selected_values = Projects.objects.filter(created_by_id=request.user.id,status=1).values_list('country_id')
            
  
    if filter_type == "wells":
        data = []
        if request.company:
            total_projects = Projects.objects.getallfiltered_projects_company(selected_values,request.company.id,request)
        else:
            total_projects = Projects.objects.filter(country_id__in=selected_values,created_by_id=request.user.id)
        
        total_projects_id = [project.id for project in total_projects]
        total_blocks = ProjectBlock.objects.filter(project_id__in=total_projects_id)
        total_wells = Wells.objects.filter(project_id__in=total_projects_id)
        filtered_totalwells =  Wells.objects.getfiltered_wells(total_projects_id,start,length)
        totalwells = Wells.objects.getallfiltered_wells(total_projects_id).count()
        

        if search_value:
            filtered_totalwells = [well for well in total_wells if search_value.lower() in well.name.lower()]
            totalwells = len(filtered_totalwells)
            
        paginator = Paginator(filtered_totalwells,length)  
        paginated_data = paginator.get_page(page)
        for well in filtered_totalwells:
            data.append({
                "well_id":well.id,
                "well_name": well.name,
                "well_type": well.well_type,
                "project_name": getprojectname(well.project_id),
                "block_name": getblockname(well.block_id),
                "field_name": getfieldname(well.field_id),
                "environment": well.environment,
                "actions": "actions",
            })
                

        response = {
            'data':data,
            'draw': draw,
            'recordsTotal': totalwells,
            'recordsFiltered': totalwells,
        }
        return JsonResponse(response, safe=False)
    
    if filter_type=="projects":
        data = []
        if request.company:
            filtered_totalprojects = Projects.objects.getfiltered_projects_company(selected_values,request.company.id,start,length,request)
            totalprojects = Projects.objects.getallfiltered_projects_company(selected_values,request.company.id,request).count()
            total_projects = Projects.objects.getallfiltered_projects_company(selected_values,request.company.id,request)
        else:
           filtered_totalprojects = Projects.objects.getfiltered_projects_individual(selected_values,request.user.id,start,length)
           totalprojects = Projects.objects.getallfiltered_projects_individual(selected_values,request.user.id).count()
           total_projects = Projects.objects.filter(country_id__in = selected_values, created_by_id = request.user.id)
        
        
        if search_value:
            filtered_totalprojects = [project for project in total_projects if search_value.lower() in project.project_name.lower()]
            totalprojects = len(filtered_totalprojects)

        paginator = Paginator(filtered_totalprojects,length)  
        paginated_data = paginator.get_page(page)
        
        for project in filtered_totalprojects:
            data.append({
                "project_id": project.id,
                "project_name": project.project_name,
                "default_units": project.unit,
                "country": getcountryname(project.country_id),
                "total_actual_wells": getnumberofwells(project.id,'actual'),
                "total_plan_wells": getnumberofwells(project.id,'plan'),
                "total_offset_wells": getnumberofwells(project.id,'offset'),
                "status": getprojectstatus(project.id),
                "actions":"actions"
            })
                
            
        response = {
            'data':data,
            'draw': draw,
            'recordsTotal': totalprojects,
            'recordsFiltered': totalprojects,
        }
        return JsonResponse(response, safe=False)
          
    
    

def create_common_permissions(request, id):
    modules=Modules.objects.filter(module_type=1) 
    if request.method == "POST":
        for module in modules:
            permission=Userrights.objects.filter(user_id=id,module_id=module.id,status=0).first()
            create=request.POST.get(str(module.name)+'_create')
            view=request.POST.get(str(module.name)+'_view')
            delete=request.POST.get(str(module.name)+'_delete')
            edit=request.POST.get(str(module.name)+'_edit')
            if(permission==None):
                Userrights.objects.create(create=create,edit=edit,view=view,delete=delete,module_id=module.id,user_id=id,permission_type=1)
            else:
                Userrights.objects.filter(id=permission.id).update(create=create,edit=edit,view=view,delete=delete)
        return redirect('custom_auth:create_common_permissions', id=id)
    return render(request,"commonpermission.html",{'modules':modules,'userid':id})

# def create_projects_permissions(request,id):
#     scheme=request.scheme
#     gethost=request.get_host()
#     project_details=Projects.objects.get(id=id)
#     users = User.objects.filter(company=request.company)
#     rights=Userrights.objects.filter(project_id=id)
#     wells=Wells.objects.filter(project_id=id)
#     if(wells.count()==0):
#         modules=Modules.objects.filter(name='Wells') 
#     else:
#         modules=Modules.objects.filter(module_type=2).exclude(name='Wells') 
#     well_rights_user=[]
#     for right in rights:
#         well_rights_user.append(right.user_id)
#     if request.method == "POST":
#         users=request.POST.get('user_id')
#         well=request.POST.get('well_id')
#         for module in modules:
#             create=request.POST.get(str(module.name)+'_create')
#             view=request.POST.get(str(module.name)+'_view')
#             delete=request.POST.get(str(module.name)+'_delete')
#             edit=request.POST.get(str(module.name)+'_edit')
#             rights=Userrights.objects.filter(well_id=well,user_id=users,module_id=module.id)
#             if(rights.count()==0):
#                 rights=Userrights.objects.create(create=create,edit=edit,view=view,delete=delete,module_id=module.id,user_id=users,permission_type=2,project_id=project_details.id,well_id=well)
#             else:
#                 rights=Userrights.objects.filter(user_id=users,module_id=module.id,project_id=id).update(create=create,edit=edit,view=view,delete=delete)
#         well_detail=Wells.objects.filter(id=well).first()
#         sender = Companies.objects.filter(id=request.company.id).first()
#         recipient = User.objects.filter(id=users).first()
#         url=json.dumps({"url":scheme+'://'+gethost+'/wells/'+well})
#         notify.send(sender, recipient=recipient,data=url,verb='Well got assigned', description='Your assigned on well '+well_detail.name,action_object=well_detail)
#         return redirect('custom_auth:create_projects_permissions', id=project_details.id)
#     return render(request,"projectpermission.html",{'modules':modules,'users':users,'project_id':project_details.id,'well_rights_user':well_rights_user,'wells':wells,'wellcount':wells.count()})

def reset_password(request,user_id):
    user = User.objects.getuserid(user_id)
    password=generate_random_password()
    print(f"password {password}")
    user.set_password(password)
    user.save()
    send_reset_password(request,user,password)
    messages.success(request, f"Reset Password sent Successfully to {user.name} {user.lastname}")
    return redirect('/users')

def getuserrights(request):
    user_id=request.GET['user_id']
    project_id=request.GET['project_id']
    if 'well_id' in request.GET:
        well_id=request.GET['well_id']
        rights=Userrights.objects.filter(well_id=well_id,user_id=user_id)
    else:
        rights=Userrights.objects.filter(project_id=project_id,user_id=user_id)
    data = serializers.serialize('json', rights)
    return JsonResponse(data,safe=False)

def getcountrycode(request):
    country_id=request.POST.get('country_id')
    try:
        country=Countries.objects.get(id=country_id)
    except Countries.DoesNotExist:
        country=None
    data={
        'conuntrycode':country.phonecode
    }
    return JsonResponse(data)

def Notifications(request):
    print('gggg')
    user = User.objects.get(pk=request.user.id)
    notifications=user.notifications.all()
    print(f"notifications {notifications}")


    # limit = request.GET.get('limit', 10)  
    # offset = request.GET.get('offset', 0)  
    # data = user.notifications.all()[offset:offset+limit]
    # serialized_data = user(data, many=True).data
    # return JsonResponse(serialized_data, safe=False)
    
    return render(request, 'notifications.html',{'notifications':notifications})

def notify_endpoint(request):
    limit = request.GET.get('limit', 10)  
    offset = request.GET.get('offset', 0)  
    data = YourModel.objects.all()[offset:offset+limit]
    serialized_data = YourModelSerializer(data, many=True).data
    return JsonResponse(serialized_data, safe=False)

def markallread(request):
    notifications=Notification.objects.filter(recipient=request.user)
    for notification in notifications:
        Notification.objects.get(pk=notification.id).mark_as_read()
    return redirect ("/notifications/")

def licensesignup(request,licence_name):
    countries = Countries.objects.all()
    if request.method == 'POST':
        title=request.POST.get('gender')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        designation=request.POST.get('designation')
        companyname=request.POST.get('companyname')
        noofusers=request.POST.get('noofusers')
        subscription_type=request.POST.get('subscription_type')
        is_autoremainder=request.POST.get('is_autoremainder',False)
       

        country_id=request.POST.get('country')
        transaction_id=None
        getlicensepackage=Licensepackage.objects.getlicense_users_type(noofusers,licence_name,subscription_type)
        price = getlicensepackage.amount*100
        product_name = 'License'

        customer = stripe.Customer.create(
            email=email,
        )

        try:
            query_params = {'title':title,'firstname':firstname,'lastname': lastname, 'email': email,'password':password,'designation':designation,'companyname':companyname,'noofusers':noofusers,'subscription_type':subscription_type,'licence_name':licence_name,'country_id':country_id,'is_autoremainder':is_autoremainder }  
            query_string = urlencode(query_params) 
            checkout_session = stripe.checkout.Session.create(
                customer=customer.id,
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': product_name,
                            },
                            'unit_amount': price,
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url = request.build_absolute_uri(reverse('custom_auth:success')) + '?' + query_string + '&' + urlencode({'session_id':transaction_id}),
                cancel_url=request.build_absolute_uri(reverse('custom_auth:users')),
            )      
            request.session['transaction_id']=checkout_session['id']   

            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(f"e {e}")
            return HttpResponseServerError()
    else:
        print('Not Post Method--')
    return render(request, 'licensesignup.html',{'licence_name':licence_name,'countries':countries})


def renewlicense(request):
    email = User.objects.getuserid(request.user.id).email
    if request.company:
        no_of_users = Companies.objects.get(id=request.company.id).no_of_users
        print('no_of_users_license',no_of_users)
        license_details = Licensepackage.objects.filter(no_of_users = no_of_users)
        print('license_details',license_details)
    else:
        license_details = Licensepackage.objects.filter(type_of_license = 'Individual')
        
    if request.method == 'POST':
        subscription_type = request.POST.get('choose_package')
        transaction_id=None 
        if request.company:
            getlicensepackage=Licensepackage.objects.getlicense_users_type(no_of_users,'CompanyPlan',subscription_type)
            price = getlicensepackage.amount*100
        else:
            getlicensepackage=Licensepackage.objects.getlicense_users_type(1,'Individual',subscription_type)
            price = getlicensepackage.amount*100
            
            
        product_name = 'Renewal'

        customer = stripe.Customer.create(
            email=email,
        )

        try:
            query_params = {'user_id':request.user.id,'email': email,'subscription_type':subscription_type,'price':price}  
            query_string = urlencode(query_params) 
            checkout_session = stripe.checkout.Session.create(
                customer=customer.id,
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': product_name,
                            },
                            'unit_amount': price,
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url = request.build_absolute_uri(reverse('custom_auth:success_renewal')) + '?' + query_string + '&' + urlencode({'session_id':transaction_id}),
                cancel_url=request.build_absolute_uri(reverse('custom_auth:users')),
            )      
            request.session['transaction_id']=checkout_session['id']   

            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(f"e {e}")
            return HttpResponseServerError()
 


    return render(request, 'renewlicense.html',{'license_details':license_details})


def success_renewal(request):
    user_id = request.GET.get('user_id')
    subscription_type = request.GET.get('subscription_type')
    transaction_id=request.session.get('transaction_id')
    price = request.GET.get('price')
    start_date = datetime.now().date()
    if(subscription_type=='monthly'):
        end_date=start_date + timedelta(days=30)
    else:
        end_date=start_date + timedelta(days=365)
    User.objects.filter(id=user_id).update(subscription_type=subscription_type,start_date=start_date,end_date=end_date)
    if request.company:
        Companies.objects.filter(id=request.company.id).update(subscription_type=subscription_type,start_date=start_date,end_date=end_date)
        Payments.objects.createpayment(price,request.company.id,'CompanyPlan',transaction_id)
    else:
        Payments.objects.createpayment(price,request.user.id,'Individual',transaction_id)
    
    
    return HttpResponseRedirect(reverse_lazy('custom_auth:dashboard')) 
    
  
def success(request):
    title=request.GET['title']
    firstname=request.GET['firstname']
    lastname=request.GET['lastname']
    email=request.GET['email']
    password=request.GET['password']
    print(f"password {password}")
    designation=request.GET['designation']
    companyname=request.GET['companyname']
    noofusers=request.GET['noofusers']
    is_autoremainder=request.GET['is_autoremainder']
    subscription_type=request.GET['subscription_type']
    transaction_id=request.session.get('transaction_id')
    licence_name=request.GET['licence_name']
    country_id=int(request.GET['country_id'])
    start_date = datetime.now().date()
    
    if(subscription_type=='monthly'):
        end_date=start_date + timedelta(days=30)
    else:
        end_date=start_date + timedelta(days=365)
    
    user=User.objects.createuser_data(title,firstname,lastname,email,licence_name,designation,subscription_type,start_date,end_date,1,country_id,is_autoremainder)
    user.set_password(password)
    if(licence_name=='Individual'):
        user.individual_id=user.id
    
    user.save()
        
    if(licence_name == 'CompanyPlan'):
        cin= generatecin(companyname)
        companydetails=Companies.objects.createcompany(companyname,cin,firstname,lastname,email,1,user.id,subscription_type,start_date,end_date,noofusers,'CompanyPlan',is_autoremainder) 
        user.company_id=companydetails.id
        user.save()
        amount=int(noofusers)*50
        Payments.objects.createpayment(amount,companydetails.id,'CompanyPlan',transaction_id)
        CompanyPackages.objects.createcompany_package(companydetails.id,noofusers,'CompanyPlan')
    else:
        Payments.objects.createpayment(50,user.id,'Individual',transaction_id)
        CompanyPackages.objects.createcompany_package(user.id,1,'Individual')
    group = Group.objects.get(name='Admin')
    user.groups.add(group)

    login(request,user)
    confirmation_of_payment(user,request)
    return HttpResponseRedirect(reverse_lazy('custom_auth:dashboard')) 

def getindividuals(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    filtered_individuals=User.objects.getindividualusers('Individual',start,length,search_value)
    total_records = User.objects.getallindividualusers('Individual',search_value).count()

    data = []
    for individual in filtered_individuals:
        data.append({
            'first_name': individual.name,
            'last_name': individual.lastname,
            'email':individual.email,
            'id':individual.id,
        })
    print(data)
    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)

def getcompanies(request,license_type):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    filtered_companies=Companies.objects.getcompanies(license_type,start,length,search_value)
    total_records = Companies.objects.getallcompanies(license_type,search_value).count()
    data = []
    for company in filtered_companies:
        item={
            'company_name': company.company_name,
            'email': company.email,
            'no_of_users':company.no_of_users,
            'subscription_type':company.subscription_type,
            'id':company.id,
            

        }
     
        
        data.append(item)
    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)

class Forgotpassword(View):
    def get(self,request,uidb64,token):
        return render(request,'password/password_reset_confirm.html')
    def post(self,request,uidb64,token):
        password=request.POST.get('password')
        user_id=urlsafe_base64_decode(uidb64)
        user_id = force_text(user_id)
        user = User.objects.get(id=user_id)
        user.set_password(password)
        user.save()
        messages.success(request, "Password Changed Successfully")
        return HttpResponseRedirect(reverse_lazy('custom_auth:login'))



class Editcustomuserrights(View):
    def get(self,request,id):
        user_modules = Modules.objects.getmodules(1)
        return render(request,'users/custom_user_rights.html',{'user_modules':user_modules,'company_id':request.company.id,'groupid':0})
    def post(self,request,id):
        scheme=request.scheme
        # gethost=request.get_host()
        # userdetails=request.session['userdata']
        # sender = User.objects.get(id=request.user.id)
        # url=json.dumps({"url":scheme+'://'+gethost+'/users'})
        # form = forms.SignupForm(userdetails)
        # current_user = User.objects.getuserid(request.user.id)
        # if form.is_valid():
        #     password=generate_random_password()
        #     current_user = User.objects.getuserid(request.user.id)
        #     groupdata = current_user.groups.first()
        #     user=form.save()
        #     user.set_password(password)
        #     user.company=request.company
        #     user.is_active=1
        #     user.licence_type = current_user.licence_type 
        #     user.start_date = current_user.start_date
        #     user.end_date = current_user.end_date
        #     user.subscription_type = current_user.subscription_type
        #     user.save()
        #     messages.success(request, "User is created successfully")
        #     if(request.user.licence_type !='Individual'):
        #         if(userdetails['group']=='new'):
        #             group, created = Group.objects.get_or_create(name=userdetails['custom_role'])
        #         else:
        #             group = Group.objects.get(id=userdetails['group'])
        #         user.groups.add(group)
        #         user_modules = Modules.objects.getmodules(1)
        #         for modules in user_modules:
        #             value = request.POST.get("rights"+str(modules.id))
        #             if value != None:
        #                 Rights.objects.create(company_id=request.company.id,module_id=value,status=1,role_id=group.id)   

        #         send_userconfirmation_mail(user,request,current_user,group,groupdata.name,request.POST.get('email'),password)
        #         notify.send(sender, recipient=user,extra_data=url,verb='Role assigned', description='You have been assigned as '+group.name,action_object=user)
        #         userlog=adduserlog('User Created',request,user.id,'User',current_user.licence_type,None,None,None)
        return redirect("/users")

class Customuserrights(View):
    def get(self,request):
        user_modules = Modules.objects.getmodules(1)
        return render(request,'users/custom_user_rights.html',{'user_modules':user_modules,'company_id':request.company.id,'groupid':0})
    def post(self,request):
        scheme=request.scheme
        gethost=request.get_host()
        userdetails=request.session['userdata']
        sender = User.objects.get(id=request.user.id)
        url=json.dumps({"url":scheme+'://'+gethost+'/users'})
        form = forms.SignupForm(userdetails)
        current_user = User.objects.getuserid(request.user.id)
        if form.is_valid():
            password=generate_random_password()
            current_user = User.objects.getuserid(request.user.id)
            groupdata = current_user.groups.first()
            user=form.save()
            user.set_password(password)
            user.company=request.company
            user.is_active=1
            user.licence_type = current_user.licence_type 
            user.start_date = current_user.start_date
            user.end_date = current_user.end_date
            user.subscription_type = current_user.subscription_type
            user.save()
            messages.success(request, "User is created successfully")
            if(request.user.licence_type !='Individual'):
                if(userdetails['group']=='new'):
                    group, created = Group.objects.get_or_create(name=userdetails['custom_role'])
                else:
                    group = Group.objects.get(id=userdetails['group'])
                user.groups.add(group)
                user_modules = Modules.objects.getmodules(1)
                for modules in user_modules:
                    value = request.POST.get("rights"+str(modules.id))
                    if value != None:
                        Rights.objects.create(company_id=request.company.id,module_id=value,status=1,role_id=group.id)   

                send_userconfirmation_mail(user,request,current_user,group,groupdata.name,request.POST.get('email'),password)
                notify.send(sender, recipient=user,extra_data=url,verb='Role assigned', description='You have been assigned as '+group.name,action_object=user)
                userlog=adduserlog('User Created',request,user.id,'User',current_user.licence_type,None,None,None)
            return redirect("/users")

class Poauserrights(View):  
    def get(self,request,userid):
        main_modules=Poamainmodules.objects.getmain_modules()
        return render(request,'users/poauser_rights.html',{'userid':userid,'main_modules':main_modules})

    def post(self,request,userid):
        user_modules = Modules.objects.getmodules(2)
        current_id=[]
        for module in user_modules:
            checkuserrights=Rights.objects.checkpoauserrights(userid,module.id)
            rights=request.POST.get('rights'+str(module.id))
            if(rights):
                if(checkuserrights.count() > 0):
                    Rights.objects.updatepoauserrights(checkuserrights[0].id)
                    current_id.append(checkuserrights[0].id)
                else:
                    rights_details=Rights.objects.createpoarights(userid,module.id)
                    current_id.append(rights_details.id)
        Rights.objects.update_posuserrights_excludedid(userid,current_id)
        return redirect("/adminusers")

def getenquiries(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '') 
    superuser_id=request.user.id 
    is_superadmin_user = User.objects.filter(id=superuser_id,is_superadmin=1,is_active=1).exists() 

    if is_superadmin_user:
        filtered_enquiries = Enquiry.objects.getenquiries_all(start,length,search_value)
        total_records = Enquiry.objects.gettotalenquiries_all(search_value).count() 
    else:
        superuser_country = list(CountryUsers.objects.filter(userid_id=superuser_id,status=1).values_list('country_name',flat=True))
        superuser_country_ids = [int(country_id) for country_id in superuser_country]
        filtered_enquiries = Enquiry.objects.getenquiries(superuser_country_ids,start,length,search_value)
        total_records = Enquiry.objects.gettotalenquiries(superuser_country_ids,search_value).count()
    data = []
    for enquiry in filtered_enquiries:
        data.append({
            'title': enquiry.gender,
            'first_name': enquiry.name,
            'last_name':enquiry.last_name,
            'email':enquiry.email,
            'message':enquiry.message,
            'id':enquiry.id,
            'form_type':enquiry.form_type
        })
    

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)

def view_enquiries(request,id):
    enquiry=Enquiry.objects.get_enquirybyid(id)
    return render(request, 'viewenquiries.html',{'enquiry':enquiry})


    




