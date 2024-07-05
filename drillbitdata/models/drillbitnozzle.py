from django.db import models

class DrillBitNozzleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def getdrillbitnozzle(self,drillbit,well_id):
        return self.filter(drillbit_id=drillbit,well_id=well_id,status=1)

class DrillBitNozzle(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    drillbit= models.ForeignKey("drillbitdata.DrillBit", on_delete=models.CASCADE,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    nozzle_size = models.FloatField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    objects=DrillBitNozzleManager()

    
    class Meta:
        db_table = "drillbitdata_drillbitnozzle"

    def __str__(self):
        return str(self.pk)