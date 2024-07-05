from django.db import models

class MudDataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def getmuddata_bywellphase(self,well_phase_id,section):
        return self.filter(well_phase_id=well_phase_id,section=section,status=1).first()
    
    def getallmuddata_bywellphase(self,well_phase_id):
        return self.filter(well_phase_id=well_phase_id,status=1)

    
    

class MudData(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    well_phase = models.ForeignKey("wellphases.WellPhases", on_delete=models.CASCADE,blank=True, null=True)
    gel_strength_0sec = models.FloatField(blank=True,null=True)
    gel_strength_10min = models.FloatField(blank=True,null=True)
    gel_strength_30min = models.FloatField(blank=True,null=True)
    mud_weight = models.FloatField(blank=True,null=True)
    plastic_viscosity=  models.FloatField(blank=True,null=True)
    yield_point=  models.FloatField(blank=True,null=True)
    low_shear_rate=  models.FloatField(blank=True,null=True)
    date = models.DateField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    section=models.CharField(max_length=255, blank=True, null=True)
    from_depth=models.FloatField(blank=True,null=True)
    todepth=models.FloatField(blank=True,null=True)
    mudtype=models.ForeignKey("muddata.MudType", on_delete=models.CASCADE,blank=True, null=True)
    objects=MudDataManager()
    timestamp=models.IntegerField(blank=True,null=True)
    time=models.TimeField(auto_now=False, auto_now_add=False,blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class MudTypeManager(models.Manager):
    def getmudtype_byid(self,mudtype_id):
        return self.get(id=mudtype_id)
    

class MudType(models.Model):
    id = models.AutoField(primary_key=True)
    mud_name = models.CharField(max_length=100,null=True) 
    status= models.IntegerField(blank=True,default=1)
    objects=MudTypeManager()
    
    class Meta:
        db_table = "mudtype"


class SectionsManager(models.Manager):
    def getsection_bywellphase_id(self,well_phase_id):
        return self.get(well_phase_id=well_phase_id,status=1)
    

class Sections(models.Model):
    id = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=100,null=True) 
    from_depth=models.FloatField(blank=True,null=True)
    todepth=models.FloatField(blank=True,null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    well_phase = models.ForeignKey("wellphases.WellPhases", on_delete=models.CASCADE,blank=True, null=True)
    selected_model=models.CharField(max_length=255, blank=True, null=True)
    status= models.IntegerField(blank=True,default=1)
    date = models.DateField(blank=True, null=True)
    timestamp=models.IntegerField(blank=True,null=True)
    time=models.TimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    objects=SectionsManager()

    
    class Meta:
        db_table = "Sections"


class Pressureloss_data(models.Model):
    id = models.AutoField(primary_key=True)
    all_data=models.JSONField(blank=True, null=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    well_phase = models.ForeignKey("wellphases.WellPhases", on_delete=models.CASCADE,blank=True, null=True)
    section_name = models.CharField(max_length=100,null=True) 
    status = models.IntegerField(blank=True,default=0)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)

    class Mete:
        db_table="pressureloss_data"