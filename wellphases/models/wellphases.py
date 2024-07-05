from django.db import models
from django.db.models import Q


class WellPhasesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def getwellphase_byid(self,id):
        return self.filter(id=id).first()
    
    def getprevious_wellphase(self,previousid,well_id):
        return self.filter(id__lt=previousid,well_id=well_id).order_by('-id').first()
    
    def checkliner(self,well_id,sectiontodepth):
        return self.filter(Q(casing_type_id=7) | Q(casing_type_id=8) | Q(casing_type_id=11) | Q(casing_type_id=12)).filter(well_id=well_id,status=1,measured_depth__lt=sectiontodepth)
    
    def getallwellphases_bywellid(self,well_id):
        return self.filter(well_id=well_id,status=1)

    
 

class WellPhases(models.Model): 
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    phase_name = models.CharField(max_length=250,blank=True, null=True)
    casing_type = models.ForeignKey("CasingTypes", on_delete=models.CASCADE,blank=True, null=True)
    hole_size = models.FloatField(blank=True, null=True)
    casing_size = models.FloatField(blank=True, null=True)
    measured_depth = models.FloatField(blank=True, null=True)
    true_vertical_depth = models.FloatField(blank=True, null=True)
    lineartop = models.FloatField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1) # 0-deleted 1-not deleted
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    nominal_od=models.FloatField(blank=True, null=True)
    weight=models.FloatField(blank=True, null=True)
    grade=models.CharField(max_length=250,blank=True, null=True)
    connection_type=models.CharField(max_length=250,blank=True, null=True)
    casing_range = models.IntegerField(blank=True,null=True)
    drift_id=models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    timestamp=models.IntegerField(blank=True,null=True)
    time=models.TimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    objects=WellPhasesManager()


    class Meta:
        pass

    def __str__(self):
        return str(self.pk)