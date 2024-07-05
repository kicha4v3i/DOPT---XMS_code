from django.db import models

class RheogramManager(models.Manager):
    def getmuddata_bywellphase(self,well_phase_id):
        return self.select_related('rheogram_date').filter(rheogram_date__well_phase_id=well_phase_id,status=1)
    def getrheogram_byselectedmodel(self,rheogram_date_id,model_name,rheogramsection_id):
        return self.filter(rheogram_date_id=rheogram_date_id,status=1,modelname=model_name,)
    def getrheogram(self,rheogram_date_id):
        return self.filter(rheogram_date_id=rheogram_date_id,status=1)
    
    

class Rheogram(models.Model):
    id = models.AutoField(primary_key=True)
    rheogram_date= models.ForeignKey("muddata.RheogramDate", on_delete=models.CASCADE,blank=True, null=True)
    rheogram_sections= models.ForeignKey("muddata.RheogramSections", on_delete=models.CASCADE,blank=True, null=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    rpm =  models.IntegerField(blank=True,null=True)
    dial =  models.CharField(max_length=255, blank=True, null=True)
    modelname =  models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    calculateddial =  models.CharField(max_length=255, blank=True, null=True)
    objects=RheogramManager()
    
    class Meta:
        pass

    def __str__(self):
        return str(self.pk)


class RheogramNameModels(models.Model):
    id = models.AutoField(primary_key=True)
    rheogram_rpm = models.CharField(max_length=100,null=True)  
    
    class Meta:
        db_table = "rheogram_rpm"

class RheogramDateManager(models.Manager):
    def getrheogramdate_bywellphase(self,well_phase_id,muddata_id):
        return self.get(well_phase_id=well_phase_id,status=1,muddata_id=muddata_id)
    def getrheogramdate_byid(self,id):
        return self.get(id=id)
    
    

class RheogramDate(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    well_phase = models.ForeignKey("wellphases.WellPhases", on_delete=models.CASCADE,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    selected_model=models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    timestamp=models.IntegerField(blank=True,null=True)
    time=models.TimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    muddata = models.ForeignKey("muddata.MudData", on_delete=models.CASCADE,blank=True, null=True)
    objects=RheogramDateManager()


    class Meta:
        db_table = "rheogram_date"

class RheogramSectionsManager(models.Manager):
    def getrheogramsections(self,section_name,wellphase_id):
        return self.get(section_name=section_name,status=1,well_phase_id=wellphase_id)
   

class RheogramSections(models.Model):
    id = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=100,null=True) 
    rheogram_date= models.ForeignKey("muddata.RheogramDate", on_delete=models.CASCADE,blank=True, null=True)
    from_depth=models.FloatField(blank=True,null=True)
    todepth=models.FloatField(blank=True,null=True)
    status= models.IntegerField(blank=True,default=1)
    well_phase = models.ForeignKey("wellphases.WellPhases", on_delete=models.CASCADE,blank=True, null=True)
    objects=RheogramSectionsManager()

    
    class Meta:
        db_table = "rheogram_sections"



