from django.db import models
from django.contrib.auth.models import Group
from django.db.models import Q


class CompaniesManager(models.Manager):
    def createcompany(self,companyname,cin,firstname,lastname,email,status,userid,subscription_type,start_date,end_date,noofusers,licence_type,is_autoremainder):
        return self.create(company_name=companyname,cin=cin,first_name=firstname,last_name=lastname,email=email,status=status,userid_id=userid,subscription_type=subscription_type,start_date=start_date,end_date=end_date,no_of_users=noofusers,licence_type=licence_type,is_autoremainder=is_autoremainder) 
    
    def getcompanyname_byid(self,cid):
        return self.get(id=cid)
    
    def update_company(self,company_id,no_of_users,user_id,start_date,end_date,subscription_type):
        return self.filter(id=company_id).update(no_of_users=no_of_users,userid_id=user_id,start_date=start_date,end_date=end_date,subscription_type=subscription_type)
    
    def updatecompany_noofusers(self,company_id,no_of_users,license_type):
        return self.filter(id=company_id).update(no_of_users=no_of_users,licence_type=license_type)

    def getcompanies(self,licence_type,offset,limit,search_value):
        companies=self.filter(Q(licence_type=licence_type) & (Q(email__icontains=search_value)| Q(first_name__icontains=search_value)|Q(last_name__icontains=search_value)))
        companies_set=companies.order_by('-id')
        result= companies_set[offset:offset+limit]  
        return result

    def getallcompanies(self,licence_type,search_value):
        return self.filter(Q(licence_type=licence_type) & (Q(email__icontains=search_value)| Q(first_name__icontains=search_value)|Q(last_name__icontains=search_value))).order_by('-id')
    
    def getcompaniescount(self,licence_type):
        return self.filter(licence_type=licence_type,status=1).count()

  
class Companies(models.Model):
    id = models.AutoField(primary_key=True)
    company_name= models.CharField(max_length=255)
    cin= models.CharField(max_length=255, blank=True, null=True)
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    country = models.ForeignKey("Countries",on_delete=models.CASCADE,blank=True, null=True)
    email= models.CharField(max_length=255)
    hydraulics = models.IntegerField(default=0, blank=True, null=True)
    irocks = models.IntegerField(default=0, blank=True, null=True)
    contact_no= models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    type_of_license = models.CharField(max_length=50, blank=True,null=True)
    no_of_users = models.IntegerField(blank=True,default=0)
    concurrentusers=models.IntegerField(blank=True,default=0)
    subscription_type=models.CharField(max_length=100,blank=True,null=True)
    start_date=models.CharField(max_length=100,blank=True,null=True)
    end_date=models.CharField(max_length=100,blank=True,null=True)
    server=models.CharField(blank=True,max_length=200,default="")
    status = models.IntegerField(blank=True,default=0)
    userid= models.ForeignKey("User",on_delete=models.CASCADE,blank=True, null=True)
    licence_type = models.CharField(choices=(('Company Plan', 'Company Plan'), ('Enterprise','Enterprise')), max_length=50, blank=True, null=True)
    is_autoremainder = models.BooleanField(('is_autoremainder'), default=False)
    company_image = models.FileField(upload_to='profile_images/',null=True,blank=True)



    objects=CompaniesManager()

    #licenses = models.ManyToManyField(Licenses)

class CompanyPackagesManager(models.Manager):
    def createcompany_package(self,company_id,noof_users,user_type):
        return self.create(user_id=company_id,concurrent_users=noof_users,user_type=user_type)
    def getcompany_current_package(self,company_id,user_type):
        print('user_id,user_type',company_id,user_type)
        return self.filter(user_id=company_id,user_type=user_type).order_by('-id')
    def getindividual_package(self,user_ids,user_type):
        return self.filter(user_id__in=user_ids,user_type=user_type)


class CompanyPackages(models.Model):  
    id = models.AutoField(primary_key=True)
    user_type = models.CharField(max_length=50,blank=True,null=True)
    user_id =  models.IntegerField(blank=True,null=True)
    concurrent_users=models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True,default=1)
    objects=CompanyPackagesManager()

class PaymentsManager(models.Manager):
    def createpayment(self,amount,user_id,user_type,checkoutid=None):
        return self.create(amount=amount,user_id=user_id,user_type=user_type,transaction_id=checkoutid)
    def getpayments(self,user_id,user_type):
        return self.filter(user_id=user_id,user_type=user_type)

class Payments(models.Model):  
    id = models.AutoField(primary_key=True)
    user_type = models.CharField(max_length=50,blank=True,null=True)
    user_id =  models.IntegerField(blank=True,null=True)
    amount= models.IntegerField(blank=True,default=0)
    currency=models.CharField(max_length=255,default='')
    licensekey=models.CharField(max_length=255,blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    transaction_id=models.CharField(max_length=100,blank=True,null=True)
    payment_status=models.IntegerField(blank=True,default=0)
    objects=PaymentsManager()


