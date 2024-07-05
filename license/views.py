from django.shortcuts import render,redirect
from license.models import Licensepackage
from django.views import View
from urllib.parse import urlencode
from django.urls import reverse
from custom_auth.models import CompanyPackages,Payments,Companies,User,Enquiry
import stripe
from django.conf import settings
from license.mailer import confirmation_of_licenseupdate
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
import json
from notifications.signals import notify
from notifications.models import Notification
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

stripe.api_key = settings.STRIPE_SECRET_KEY




# Create your views here.
def listlicense(request):
    license_packages=Licensepackage.objects.getalllicense()
    return render(request,'licenses.html',{'license_packages': license_packages})

class CreateLicense(View):
    def get(self, request):
        return render(request,'createlicense.html')
    def post(self, request):
        print(f"post {request.POST}")
        no_of_users = request.POST.get('no_of_users') if request.POST.get('no_of_users')!='' else None
        check_licensepackage=Licensepackage.objects.getlicense_users_type(no_of_users,request.POST.get('license_type'),request.POST.get('subscription_type'))
        
        if(check_licensepackage==None):
            license_package=Licensepackage.objects.createlicensepackage(request.POST.get('license_type'),no_of_users,request.POST.get('amount'),request.POST.get('subscription_type'))
        else:
            license_package=Licensepackage.objects.updatelicensepackage(no_of_users,request.POST.get('amount'),check_licensepackage.id) 
        return redirect('license:listlicense')

class UpgradeLicense(View):
    def get(self, request):    
        license_packages=Licensepackage.objects.getcompanylicense()
        if request.user.company_id:
            no_of_users = Companies.objects.filter(id=request.company.id).values('no_of_users').first()['no_of_users']
            license_pack = Licensepackage.objects.filter(no_of_users=no_of_users).first()
          
        else:
            no_of_users = 1
            license_pack = 1
        licence_type = request.user.licence_type
       
        return render(request,'updatelicenseform.html',{'license_packages':license_packages,'no_of_users':no_of_users,'licence_type':licence_type,'license_pack':license_pack,'request':request})
    
    def post(self,request):
        user = User.objects.getuserid(request.user.id)
        if user.licence_type == "Individual":
            user_id = user.id 
        else:
            user_id = request.company.id 
        enquiry = Enquiry.objects.filter(user_type_id=user_id,user_type=user.licence_type)
        if enquiry:
            messages.error(request,'You have already submitted enquiry. Please wait for approval')
            return redirect('license:upgradelicense')
        
        submit_type = request.POST.get('submit_type')
        choose_package=request.POST.get('choose_package')
        no_of_users=request.POST.get('no_of_users')
        if not no_of_users:
            package_details=Licensepackage.objects.getlicensebyid(choose_package)
            no_of_users = package_details.no_of_users
        if request.user.company_id:
            company = Companies.objects.filter(id=request.company.id).first()
            no_of_users_old = company.no_of_users
        
        if(submit_type == "Downgrade"):
            company = Companies.objects.getcompanyname_byid(request.user.company_id)
            CompanyPackages.objects.createcompany_package(request.user.company_id,no_of_users,company.licence_type)
            Companies.objects.updatecompany_noofusers(request.user.company_id,no_of_users,company.licence_type)
            return redirect('/')
        else:
            if (request.user.licence_type == "CompanyPlan"):
                if (choose_package != "custom"):
                    if(no_of_users_old+int(no_of_users) > 15 ):
                        print('vvv',no_of_users_old+int(no_of_users))
                        messages.error(request, "You need to Change Enterprise")
                        return redirect('license:upgradelicense') 
                      
            if not (request.user.company_id):
                company_name = request.POST.get('companyname')
                designation = request.POST.get('designation')
            
            else:
                company_name = "NULL"
                designation = "NULL"
        


                

            # if(request.user.licence_type != "Individual") and (no_of_users_old > int(no_of_users)):
            #     company = Companies.objects.getcompanyname_byid(request.user.company_id)
            #     CompanyPackages.objects.createcompany_package(request.user.company_id,no_of_users,company.licence_type)
            #     Companies.objects.updatecompany_noofusers(request.user.company_id,no_of_users,company.licence_type)
            #     return redirect('/')
            # else:
            if choose_package == 'custom':
                package_id= "NULL"
                price=int(no_of_users)*5000
                url = reverse('license:success') + f'?package_id={package_id}&no_of_users={no_of_users}&price={price}&company_name={company_name}&designation={designation}&licence_type={user.licence_type}' 
                return redirect(url)
            else:
                package_details=Licensepackage.objects.getlicensebyid(choose_package)
                price=package_details.amount*100
                package_id = package_details.id
                product_name = 'License'
                customer = stripe.Customer.create(
                email=request.user.email,
                )
                try:
                    query_params = {'company_name':company_name,'designation':designation,'package_id': package_id, 'user_id': request.user.id,'price':price,'no_of_users':no_of_users,'licence_type':user.licence_type }  
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
                        success_url = request.build_absolute_uri(reverse('license:success')) + '?' + query_string,
                        cancel_url=request.build_absolute_uri(reverse('license:listlicense')),
                    )
                    checkoutid=checkout_session['id']
                    request.session['transaction_id'] = checkoutid
                    request.session.save()
                    return redirect(checkout_session.url, code=303)
                except Exception as e:
                    print('Error',e)
                    return HttpResponseServerError()



def success(request):
    price = request.GET['price']
    no_of_users = request.GET['no_of_users']
    package_id = request.GET['package_id']
    licence_type=request.GET['licence_type']
    if (package_id != "NULL"):
        package_details = Licensepackage.objects.getlicensebyid(package_id)
        user_id=request.GET['user_id']
        package_id=request.GET['package_id']
        company_name = request.GET['company_name']
        designation = request.GET['designation'] 
        checkoutid = request.session.get('transaction_id')
    if request.user.licence_type == 'Individual':
        company_name = request.GET['company_name']
        designation = request.GET['designation'] 

 

    users = User.objects.getuserid(request.user.id)
    recipient = User.objects.filter(is_superadmin=1)
    scheme=request.scheme
    gethost=request.get_host()
    if package_id != "NULL":
        if (request.user.licence_type == 'Individual'):
            company = Companies.objects.createcompany(company_name,None,users.name,users.lastname,users.email,1,users.id,users.subscription_type,users.start_date,users.end_date,0,'CompanyPlan',request.user.is_autoremainder)
            if(package_id != "NULL"):
                Payments.objects.createpayment(package_details.amount,company.id,'CompanyPlan',checkoutid)
                CompanyPackages.objects.createcompany_package(company.id,package_details.no_of_users,'CompanyPlan')
                User.objects.update_userlicense_individual(user_id,designation,'CompanyPlan',company.id)
                Companies.objects.updatecompany_noofusers(company.id,package_details.no_of_users,'CompanyPlan')
        else:
            company=Companies.objects.getcompanyname_byid(request.user.company_id)
            if(package_id != "NULL"):
                Payments.objects.createpayment(package_details.amount,request.user.company_id,'CompanyPlan',checkoutid)
                CompanyPackages.objects.createcompany_package(request.user.company_id,package_details.no_of_users,'CompanyPlan')
                no_of_users_company = company.no_of_users + package_details.no_of_users
                Companies.objects.updatecompany_noofusers(request.user.company_id,no_of_users_company,'CompanyPlan')
                User.objects.update_userlicense_company(user_id,'CompanyPlan')

    else:
        if users.company_id:
            user_id = users.company_id 
            user_type = users.licence_type
            user_name = users.name
            company=Companies.objects.getcompanyname_byid(user_id)
            message_name=company.company_name
            Enquiry.objects.create_enquiry(company.first_name,company.last_name,company.email,company.company_name,users.designation,user_id,user_type,'license',no_of_users)
        else:
            user_id = users.id
            user_type = "Individual"
            user_name = users.name
            message_name=users.name

            Enquiry.objects.create_enquiry(users.name,users.lastname,users.email,company_name,designation,user_id,user_type,'license',no_of_users)
        
        messages.success(request, "Your enquiry submitted successfully")
        url=json.dumps({"url":scheme+'://'+gethost+'/company/views/'+str(user_id)+'/'+str(user_type)})
        notify.send(sender=users, recipient=recipient,extra_data=url, verb='Request for License Upgradation received', description='License Upgrade request from '+message_name)
        
    # notify.send(users, recipient=recipient,extra_data=url, verb='License upgraded', description='License upgraded '+company.company_name,action_object=company)
    confirmation_of_licenseupdate(request.user,request)
    if(licence_type=='Individual'):
        query_params = {
            'type': 'individual',
        }
        redirect_url = f"{reverse('custom_auth:license_details')}?{urlencode(query_params)}"
        return HttpResponseRedirect(redirect_url)


    else:
        return HttpResponseRedirect(reverse_lazy('custom_auth:license_details')) 

class Changepassword(View):
    def get(self, request):
        return render(request,'changepassword.html')
    def post(self, request):
        password=request.POST.get('password')
        user = User.objects.get(email=request.user.email)
        user.set_password(password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Password Changed Successfully")
        if(request.user.is_superadmin==1):
            logouturl="custom_auth:adminlogin"
        else:
            logouturl="custom_auth:login"
        return HttpResponseRedirect(reverse_lazy(logouturl)) 


def checkoldpassword(request):
    old_password = request.GET.get('old_password')
    user = User.objects.get(email=request.user.email)

    if user.check_password(old_password):
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})

class Editprofile(View):
    def get(self, request,id):
        return render(request,'editprofile.html')
    def post(self, request,id):
        user =User.objects.get(id=id)
        user.name=request.POST.get('name')
        user.email=request.POST.get('email')
        user.designation=request.POST.get('designation')
        user.lastname=request.POST.get('lastname')
        user.title=request.POST.get('title')
        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
            print(f"profile_image {profile_image}")
            user.profile_image=profile_image
        user.save()
        return redirect('custom_auth:license_details')

class Editcompanyprofile(View):
    def get(self, request):
        return render(request,'editcompanyprofile.html')
    def post(self, request):
        company=Companies.objects.getcompanyname_byid(request.company.id)
        if 'company_image' in request.FILES:
            company_image = request.FILES['company_image']
            company.company_image=company_image
        company.save()
        return redirect('custom_auth:license_details')





      





    






