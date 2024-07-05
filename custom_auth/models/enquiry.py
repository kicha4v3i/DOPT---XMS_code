from django.db import models
from helpers.commonimport import Q
from django.db.models import Count
class EnquiryManager(models.Manager):
    def create_enquiry(self,first_name,last_name,email,company_name,designation,user_id,user_type,form_type,no_of_users):
        return self.create(name=first_name,last_name=last_name,email=email,company_name=company_name,designation=designation,user_type_id=user_id,user_type=user_type,form_type=form_type,no_of_users=no_of_users)
    def get_enquirybyid(self,id):
        return self.get(id=id) 
    def update_status_enquiry(self,id,status):
        return self.filter(id=id).update(status=1)
    def get_enquirybyuser_type(self,user_type_id,user_type):
        return self.filter(user_type_id=user_type_id,user_type=user_type) 
    
    
    def getenquiries_all(self,offset,limit,search_value):
        enquiry=self.filter(~Q(form_type='license') & (Q(email__icontains=search_value)| Q(name__icontains=search_value)|Q(last_name__icontains=search_value)))
        enquiry_set=enquiry.order_by('-id')
        result= enquiry_set[offset:offset+limit]
        return result
    
    def gettotalenquiries_all(self,search_value):
        return self.filter(~Q(form_type='license') & (Q(email__icontains=search_value)| Q(name__icontains=search_value)|Q(last_name__icontains=search_value)))
    
    def getenquiries(self,superuser_country_ids,offset,limit,search_value):
        enquiry=self.filter(~Q(form_type='license') & (Q(email__icontains=search_value)| Q(name__icontains=search_value)|Q(last_name__icontains=search_value)) & Q(country__in=superuser_country_ids))
        enquiry_set=enquiry.order_by('-id')
        result= enquiry_set[offset:offset+limit]
        return result
    
    def gettotalenquiries(self,superuser_country_ids,search_value):
        return self.filter(~Q(form_type='license') & (Q(email__icontains=search_value)| Q(name__icontains=search_value)|Q(last_name__icontains=search_value))& Q(country__in=superuser_country_ids))

    def getenquirycount(self):
        return self.values('form_type').annotate(count=Count('form_type'))


class Enquiry(models.Model):  
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=50,blank=True,default='')
    company_name = models.CharField(max_length=100,blank=True,default='')
    designation = models.CharField(max_length=100,blank=True,default='')
    gender = models.CharField(max_length=255,default="", editable=False)
    email = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    notification_status = models.IntegerField(blank=True,default=0)
    status = models.IntegerField(blank=True,default=0)
    form_type = models.CharField(max_length=50,null=True)
    user_type = models.CharField(max_length=50,null=True)
    user_type_id = models.IntegerField(blank=True,default=0)
    no_of_users = models.IntegerField(blank=True,default=0)
    country=models.IntegerField(blank=True,null=True)
    objects=EnquiryManager()
    
    class Meta:
        db_table = "enquiries"
    