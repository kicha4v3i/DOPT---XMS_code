from django.db import models

class BhaElementManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def getbhaelement(self,bhadataid):
        return self.filter(bhadata_id=bhadataid,status=1).exclude(type_name='Bit').order_by('-id')
    
    def getpreviousbhaelement(self,bhadataid,previousbhaid):
        return self.filter(bhadata_id=bhadataid,id__lt=previousbhaid,status=1).order_by('-id').first()

class BhaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def getbha(self,wellphase_id):
        return self.filter(well_phases_id=wellphase_id,status=1).first()
      
class BhaData(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    well_phases = models.ForeignKey("wellphases.WellPhases", on_delete=models.CASCADE,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    timestamp=models.IntegerField(blank=True,null=True)
    time=models.TimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    bhaname=models.CharField(max_length=30,blank=True, null=True)
    depth=models.FloatField(blank=True, null=True)
    objects=BhaManager()


    
    class Meta:
        db_table = "bhadata_bhadata"

class BhaElement(models.Model):
    id = models.AutoField(primary_key=True)
    bhadata= models.ForeignKey("bhadata.BHAdata", on_delete=models.CASCADE,blank=True, null=True)
    element = models.CharField(max_length=30,blank=True, null=True)
    od = models.CharField(max_length=30,blank=True, null=True)
    weight=models.FloatField(blank=True, null=True)
    class_element=models.CharField(max_length=30,blank=True, null=True)
    grade=models.CharField(max_length=30,blank=True, null=True)
    pipe_type=models.CharField(max_length=30,blank=True, null=True)
    connection_type=models.CharField(max_length=30,blank=True, null=True)
    tool_od=models.FloatField(blank=True, null=True)
    identity = models.CharField(max_length=30,blank=True, null=True)
    length = models.CharField(max_length=30,blank=True, null=True)
    length_onejoint=models.FloatField(blank=True, null=True)
    onejoint_length=models.CharField(max_length=30,blank=True, null=True)
    type_name = models.CharField(max_length=30,blank=True, null=True)
    box_tj_length = models.CharField(max_length=30,blank=True, null=True)
    pin_tj_length = models.CharField(max_length=30,blank=True, null=True)
    tool_id = models.FloatField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    calculation_type = models.IntegerField(blank=True,default=0)
    objects=BhaElementManager()



    class Mata:
        db_table = "bhadata_bhaelement"

