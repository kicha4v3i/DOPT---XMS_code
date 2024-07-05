from django.db import models

class CountriesManager(models.Manager):
    def getcountry_byid(self,id):
        return self.get(id=id)

class Countries(models.Model):  
    id = models.AutoField(primary_key=True)
    iso= models.CharField(max_length=255)
    name= models.CharField(max_length=255)
    nicename= models.CharField(max_length=255)
    iso3= models.CharField(max_length=255)
    numcode= models.CharField(max_length=255)
    phonecode= models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True,default=1)
    objects=CountriesManager()

    def __str__(self):
        """stirng representation"""
        return self.nicename

class Basecountries(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    iso3=models.CharField(max_length=255)
    numeric_code=models.CharField(max_length=255)
    iso2=models.CharField(max_length=255)
    phonecode=models.CharField(max_length=255)
    capital=models.CharField(max_length=255)
    currency=models.CharField(max_length=255)
    currency_name=models.CharField(max_length=255)
    currency_symbol=models.CharField(max_length=255)
    tld=models.CharField(max_length=255)
    native=models.CharField(max_length=255)
    region=models.CharField(max_length=255)
    subregion=models.CharField(max_length=255)
    timezones=models.TextField()
    translations=models.TextField()
    flag=models.IntegerField(blank=True, null=True,default=1)
    latitude=models.DecimalField(max_digits=10, decimal_places=8)
    longitude=models.DecimalField(max_digits=11, decimal_places=8)
    emoji=models.CharField(max_length=255)
    emojiU=models.CharField(max_length=255,blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    updated_at=models.DateTimeField(auto_now_add=True, editable=False)
    wikiDataId=models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        """stirng representation"""
        return self.name

class ModulesManager(models.Manager):
    def getmodules(self,module_type):
        return self.filter(status=1,module_type=module_type) 
    def getsubmodules(self,mainmodule_id):
        return self.filter(status=1,main_module=mainmodule_id) 
   
class Modules(models.Model):  
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=255)
    module_type=models.IntegerField(blank=True,default=0)
    status = models.IntegerField(blank=True,default=0)
    main_module=models.IntegerField(blank=True,null=True)

    objects=ModulesManager()
    class Meta:
        db_table = "modules"