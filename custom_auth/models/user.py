
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.db.models import Q

class CustomUserManager(BaseUserManager):
    use_in_migration = True
    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
  
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
    def authenticate_poauser(self, email, password):
        try:
            user = self.get(email=email)
            if user.check_password(password) and (user.is_superuser or user.is_superadmin):
                return user
        except self.model.DoesNotExist:
            return None
    
    def createuser_data(self,title,firstname,lastname,email,licence_name,designation,subscription_type,start_date,end_date,is_admin,country_id,is_autoremainder):
        return self.create(title=title,name=firstname,lastname=lastname,email=email,licence_type=licence_name,designation=designation,subscription_type=subscription_type,start_date=start_date,end_date=end_date,is_active=1,is_admin=is_admin,country_user=country_id,is_autoremainder=is_autoremainder)
    
    def getuser_bycompany(self,company,current_user):
        return self.filter(company=company,is_active=1).exclude(Q(id=current_user) | Q(is_admin=1)).order_by('-id')
    
    def getuserid(self,id):
        return self.get(id=id)

    def update_userlicense_individual(self,user_id,designation,license_type,companyid):
        return self.filter(id=user_id).update(designation=designation,licence_type=license_type,company_id=companyid)
    
    
    def update_userlicense_company(self,user_id,license_type):
        return self.filter(company_id=user_id).update(licence_type=license_type)
    
    def getcompanyusers(self,company_id):
        return self.filter(company_id=company_id,is_active=1)
    
    def getindividualusers(self,licence_type,offset,limit,search_value):
        individuals=self.filter(Q(licence_type=licence_type) & (Q(email__icontains=search_value)| Q(name__icontains=search_value)|Q(lastname__icontains=search_value)))
        individuals_set=individuals.order_by('-id')
        result= individuals_set[offset:offset+limit]  
        return result

    def getallindividualusers(self,licence_type,search_value):
        return self.filter(licence_type=licence_type, email__icontains=search_value,name__icontains=search_value,lastname__icontains=search_value).order_by('-id')
    
    def getindividuals(self,id):
        return self.filter(individual_id=id,is_active=1).exclude(id=id).order_by('-id')
    
    def getadminuser(self,company_id):
        return self.get(company_id=company_id,is_admin=1)
    
    def exclude_projectusers(self,company_id,user_ids):
        return self.filter(company_id=company_id,is_active=1).exclude(id__in=user_ids)
    
    def updateuser(self,user_id):
        self.filter(id=user_id).update(is_active=0)
       
    def getpoausers(self,user_id):
        return self.filter(is_superuser=1,is_active=1).exclude(id=user_id)
    
    def getpoausercount(self):
        return self.filter(is_superuser=1,is_active=1).count()
        
    def getuser_byemail(self,email):
        return self.get(email=email,is_active=1)
    
    # def getsuperadmin_user(self):
    #     return list(self.filter(is_superadmin=1,is_active=1).values_list('id',flat=True))
    def update_isadmin(self,user_id):
        self.filter(id=user_id).update(is_admin=0)
    
    def getindividuals_count(self):
        return self.filter(licence_type='Individual',is_active=1).count()
    
    def getmainpoa(self):
        return self.get(is_superadmin=1,is_active=1)
    
    def getallcountryusers(self):
        return self.filter(is_allcountry=1,is_active=1,is_superuser=1)
    def getallcompanyusers_exclude_currentuser(self,company_id,id):
        return self.filter(company_id=company_id,is_active=1).exclude(id=id)

    



   

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    title = models.CharField(('title'),blank=True,null=True,max_length=15)
    email = models.EmailField(('email'), unique=True, default='')
    name = models.CharField(('name'), max_length=50, blank=False)
    lastname = models.CharField(('lastname'), max_length=50, blank=True,null=True)
    designation=models.CharField(max_length=50, blank=True,null=True)
    is_superadmin = models.BooleanField(('is_superadmin'), default=False)
    is_active = models.BooleanField(('is_active'), default=False)
    is_staff = models.BooleanField(default=True)
    company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
    licence_type = models.CharField(choices=(('Individual', 'Individual'), ('Company Plan', 'Company Plan'), ('Enterprise','Enterprise')), max_length=50, blank=True, null=True)
    subscription_type=models.CharField(_('subscription_type'),max_length=100,blank=True,null=True)
    start_date=models.CharField(_('start_date'),max_length=100,blank=True,null=True)
    end_date=models.CharField(_('end_date'),max_length=100,blank=True,null=True)
    is_loggedin = models.BooleanField(('is_loggedin'), default=False)
    individual_id = models.IntegerField(blank=True,null=True)
    is_admin = models.BooleanField(('is_admin'), default=False)
    country_user=models.IntegerField(blank=True,null=True)
    is_allcountry = models.BooleanField(('is_allcountry'), default=False)
    is_autoremainder = models.BooleanField(('is_autoremainder'), default=False)
    profile_image = models.FileField(upload_to='profile_images/',null=True,blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()
    

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """stirng representation"""
        return self.email 
    
    
class CountryUserManager(models.Manager):
    def create_countryuser(self,user_id,status,country_name):
        return self.create(userid_id=user_id,status=status,country_name=country_name) 
    def update_countryuser(self,user_id,country_name,status):
        return self.filter(userid_id=user_id,country_name__in=country_name).update(status=status)
    def getcountry_allcountry_user(self,country_id):
        return self.select_related('userid').filter(country_name=country_id,userid__is_active=1)
    
class CountryUsers(models.Model):
    id = models.AutoField(primary_key=True)
    userid= models.ForeignKey("User",on_delete=models.CASCADE,blank=True, null=True)
    country_name = models.CharField(max_length=100, blank=False)
    status = models.IntegerField(blank=True,default=1)
    objects = CountryUserManager()
    class Meta:
        db_table = "country_user"
    
    
class RightsManager(models.Manager):
    def getuserrights_company(self,module_id,role_id,status,company):
        return self.filter(module_id=module_id,role_id=role_id,status=status,company_id=company).first()
    def createpoarights(self,userid,module_id):
        return self.create(module_id=module_id,user_id=userid,is_superadmin=1)
    def checkpoauserrights(self,userid,module_id):
        return self.filter(module_id=module_id,user_id=userid,is_superadmin=1)
    def updatepoauserrights(self,rights_id):
        self.filter(id=rights_id).update(status=1)
    def update_posuserrights_excludedid(self,user_id,current_rights_id):
        self.filter(user_id=user_id).exclude(id__in=current_rights_id).update(status=0)
    def checkpoa_userrights(self,user_id,module_id):
        return self.filter(user_id=user_id,is_superadmin=1,module_id=module_id,status=1)
    def checkcustom_rights_exist(self,company_id,module_id,role_id):
        return self.filter(company_id=company_id,module_id=module_id,role_id=role_id)
    def update_userrights_excludedid(self,current_rights_id):
        self.filter(id__in=current_rights_id).update(status=0)
    def check_userrights(self,role_id,module_id,company_id):
        return self.filter(role_id=role_id,module_id=module_id,status=1,company_id=company_id)
  
class Rights(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
    role=models.ForeignKey(Group, on_delete=models.CASCADE,blank=True, null=True)
    module=models.ForeignKey("Modules", on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    is_superadmin = models.BooleanField(('is_superadmin'), default=False)
    user_id=models.IntegerField(blank=True,null=True)

    objects=RightsManager()

    class Meta:
        db_table = "rights"

class PoamainmodulesManager(models.Manager):
    def getmain_modules(self):
        return self.filter(status=1)
   
class Poamainmodules(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(('name'), max_length=25, blank=False)
    status = models.IntegerField(blank=True,default=1)
    has_submenu = models.BooleanField(('has_submenu'), default=True)
    objects=PoamainmodulesManager()

    class Meta:
        db_table = "poamainmodules"





