from django.db import models
from django.contrib.auth.models import Group

class LicensepackageManager(models.Manager):
    def createlicensepackage(self,type_of_license,no_of_users,amount,subscription_type):
        return self.create(type_of_license=type_of_license,no_of_users=no_of_users,amount=amount,subscription_type=subscription_type)
    def getalllicense(self):
        return self.filter(status=1)
    def getlicense_users_type(self,no_of_users,license_type,subscription_type):
        if(license_type=='Individual'):
            return self.filter(type_of_license=license_type,subscription_type=subscription_type).first()
        else:
            return self.filter(type_of_license=license_type,no_of_users=no_of_users,subscription_type=subscription_type).first()
    def updatelicensepackage(self,no_of_users,amount,id):
        return self.filter(id=id).update(no_of_users=no_of_users,amount=amount,status=1)
    def getcompanylicense(self):
        return self.filter(status=1,type_of_license='CompanyPlan')
   
    def getlicensebyid(self,id):
        return self.get(id=id)


class Licensepackage(models.Model):
    id = models.AutoField(primary_key=True)
    type_of_license= models.CharField(choices=(('Individual', 'Individual'), ('Company Plan', 'Company Plan'), ('Enterprise','Enterprise')), max_length=25, blank=True, null=True)
    no_of_users = models.IntegerField(blank=True, null=True)
    subscription_type=models.CharField(max_length=100,blank=True,null=True)
    country_id=models.IntegerField(blank=True,null=True)
    amount=models.IntegerField(blank=True,null=True)
    status = models.IntegerField(blank=True,default=1)
    objects=LicensepackageManager()


