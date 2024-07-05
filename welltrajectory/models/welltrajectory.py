from django.db import models


class WellTrajectoryManager(models.Manager):
    def get_lastmd(self,well_id):
        return self.filter(well_id=well_id).order_by('-id').first()
    
    def gettrajectory(self,company,well_id,status,offset,limit):
        return self.filter(company=company,well=well_id,status=status)[offset:offset+limit]
    
    def getalltrajectory(self,company,well_id,status):
        return self.filter(company=company,well=well_id,status=status)
    
    def gettrajectory_bywell_md(self,measured_depth,well_id):
        return self.filter(measured_depth=measured_depth,well=well_id)
    
    def getbelowmd(self,measured_depth,well_id):
        return self.filter(measured_depth__lte=measured_depth,well=well_id).order_by('-measured_depth')[:1].first()
    
    def getabovemd(self,measured_depth,well_id):
        return self.filter(measured_depth__gte=measured_depth,well=well_id).order_by('measured_depth')[:1].first()
   
    
  
    
    
# Create your models here.
class WellTrajectory(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    measured_depth = models.FloatField(blank=True, null=True)
    inclination = models.FloatField(blank=True, null=True)
    azimuth = models.FloatField(blank=True, null=True)
    true_vertical_depth = models.FloatField(blank=True, null=True)
    dls = models.FloatField(blank=True, null=True)
    delta_e = models.FloatField(blank=True, null=True)
    delta_n = models.FloatField(blank=True, null=True)
    east = models.FloatField(blank=True, null=True)
    north = models.FloatField(blank=True, null=True)
    easting = models.FloatField(blank=True, null=True)
    northing = models.FloatField(blank=True, null=True)
    vertical_section = models.FloatField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    timestamp=models.IntegerField(blank=True,null=True)
    time=models.TimeField(auto_now=False, auto_now_add=False,blank=True, null=True)

    objects=WellTrajectoryManager()



    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
 