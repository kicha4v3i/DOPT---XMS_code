from django.db import models
from helpers.commonimport import Q

class MudPumpManager(models.Manager):
    def createmudpump(self,stroke_length,pump_name,pump_manufacturer,pump_type,company_id,well_id,number_of_pumps):
        return self.create(stroke_length=stroke_length,pump_name=pump_name,pump_manufacturer=pump_manufacturer,pump_type=pump_type,company_id=company_id,well_id=well_id,number_of_pumps=number_of_pumps) 
    
  
# Create your models here.
class MudPump(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    stroke_length = models.FloatField(blank=True, null=True)
    pump_name = models.IntegerField(blank=True, null=True)
    pump_manufacturer = models.IntegerField(blank=True, null=True)
    pump_type = models.CharField(max_length=30,blank=True, null=True)
    number_of_pumps = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    objects=MudPumpManager()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)


class MudPumpSpeed(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    pump_speed =models.IntegerField(blank=True, null=True)
    mud_pump = models.ForeignKey("mud.MudPump", on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)

class MudPumpFlowRate(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    mud_pump_speed = models.ForeignKey("mud.MudPumpSpeed", on_delete=models.CASCADE,blank=True, null=True)
    flowrate = models.FloatField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    order = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False) 
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)


class MudPumpData(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    mud_pump = models.ForeignKey("mud.MudPump", on_delete=models.CASCADE,blank=True, null=True)
    linear_size = models.FloatField(blank=True, null=True)
    max_discharge_pressure = models.FloatField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
type_choice=(
    ('Triplex','Triplex'),
    ('Duplex', 'Duplex'),
)

API = 0
SI = 1
MIXED = 2

UNITS = (
    (API, 'API'),
    (SI, 'SI'),
    (MIXED, 'MIXED'),
)

class PumpManufacturerManager(models.Manager):
    def getpumpmanufacture(self,manufacture_id):
        return self.get(id=manufacture_id) 
    def getallpumpmanufacture(self,company_id):
        return self.filter(Q(company_id=company_id) | Q(is_superadmin=1)) 
    def get_individual_pumpmanufacture(self,user_id):
        return self.filter(Q(user_id=user_id) | Q(is_superadmin=1))
    


class PumpManufacturer(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    is_superadmin = models.IntegerField(blank=True,default=0)
    name = models.CharField(max_length=250,blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    user_id = models.IntegerField(blank=True,null=True)
    objects=PumpManufacturerManager()
    def __str__(self):
        return str(self.name)

class PumpsManager(models.Manager):
    def getpumpdetails(self,pump_id):
        return self.get(id=pump_id) 
    def getallpump_bymanufacture(self,manufacture_id):
        return self.filter(pump_manufacturer_id=manufacture_id)
    def getindividuals_pump(self,user_id):
        return self.filter(Q(user_id=user_id) | Q(is_superadmin=1))


class Pumps(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    pump_manufacturer = models.ForeignKey("mud.PumpManufacturer", on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=250,blank=True, null=True)
    type = models.CharField(max_length=250, choices=type_choice,blank=True, null=True)
    unit= models.CharField(max_length=255, blank=True, null=True)
    # roddiameter = models.FloatField(blank=True, null=True)
    stroke_length = models.FloatField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    is_superadmin = models.IntegerField(blank=True,default=0)
    user_id = models.IntegerField(blank=True,null=True)
    objects=PumpsManager()
    def __str__(self):
        return str(self.name)


class MudPumpMasterSpeed(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    pump_speed =models.IntegerField(blank=True, null=True)
    mud_pump_master = models.ForeignKey("mud.Pumps", on_delete=models.CASCADE,blank=True, null=True)
    is_superadmin = models.IntegerField(blank=True,default=0)


class MudPumpMasterFlowRate(models.Model):
    id = models.AutoField(primary_key=True)
    mud_pump_master_speed = models.ForeignKey("mud.MudPumpMasterSpeed", on_delete=models.CASCADE,blank=True, null=True)
    flowrate = models.FloatField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    order = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False) 
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    is_superadmin = models.IntegerField(blank=True,default=0)
    
    class Meta:
        pass

    def __str__(self):
        return str(self.pk)


class MudPumpMasterData(models.Model):
    id = models.AutoField(primary_key=True)
    mud_pump_master = models.ForeignKey("mud.Pumps", on_delete=models.CASCADE,blank=True, null=True)
    linear_size = models.FloatField(blank=True, null=True)
    max_discharge_pressure = models.FloatField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    is_superadmin = models.IntegerField(blank=True,default=0)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
