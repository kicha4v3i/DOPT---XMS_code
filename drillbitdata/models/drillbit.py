from django.db import models

class DrillbitManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def getdrillbit(self,well_id,wellphase_id):
        return self.filter(well_id=well_id,well_phases_id=wellphase_id,status=1).first()
    
 
 

# Create your models here.
class DrillBit(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    well_phases = models.ForeignKey("wellphases.WellPhases", on_delete=models.CASCADE,blank=True, null=True)
    bit_type = models.ForeignKey("drillbitdata.BitTypesNames", on_delete=models.CASCADE,blank=True, null=True)
    manufacture = models.CharField(max_length=50,blank=True, null=True)
    no_of_nozzle = models.IntegerField(blank=True, null=True)
    tfa=models.FloatField(blank=True, null=True)
    external_nozzle = models.BooleanField(blank=True,null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    manufacture=models.CharField(max_length=50, blank=True, null=True)
    timestamp=models.IntegerField(blank=True,null=True)
    time=models.TimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    serial_no=models.CharField(max_length=50,blank=True, null=True)
    bha=models.ForeignKey("bhadata.BHAdata", on_delete=models.CASCADE,blank=True, null=True)
    idac_code=models.CharField(max_length=50,blank=True, null=True)
    objects=DrillbitManager()


    class Meta:
        db_table = "drillbitdata_drillbit"

    def __str__(self):
        return str(self.pk)
