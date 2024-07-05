from django.db import models

class HydraulicData(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    well_phase = models.ForeignKey("wellphases.WellPhases", on_delete=models.CASCADE,blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    timestamp=models.IntegerField(blank=True,null=True)
    time=models.TimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    measured_depth = models.FloatField(blank=True, null=True)
    flowrate = models.FloatField(blank=True, null=True)
    rop = models.FloatField(blank=True, null=True)
    rpm = models.IntegerField(blank=True, null=True)
    pump_pressure = models.FloatField(blank=True, null=True)
    annular_pressure = models.IntegerField(blank=True, null=True)
    ecd = models.FloatField(blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class Planwell_data(models.Model):
    id = models.AutoField(primary_key=True)
    flowrate = models.IntegerField(blank=True, null=True)
    rop = models.FloatField(blank=True, null=True)
    rpm = models.IntegerField(blank=True, null=True)
    bitdepth = models.FloatField(blank=True, null=True)
    surface_pressure = models.FloatField(blank=True, null=True)
    ecd = models.FloatField(blank=True, null=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    well_phase = models.ForeignKey("wellphases.WellPhases", on_delete=models.CASCADE,blank=True, null=True)
    section_name = models.CharField(max_length=100,null=True) 
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        db_table = "muddata_plandate"