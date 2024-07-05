from django.db import models


class Specifications(models.Model):
    id = models.AutoField(primary_key=True)
    bhadata= models.ForeignKey("bhadata.BHAdata", on_delete=models.CASCADE,blank=True, null=True)
    bhadata_element= models.ForeignKey("bhadata.BhaElement", on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=30,blank=True, null=True)
    specification_od = models.FloatField(blank=True, null=True)
    specification_id = models.FloatField(blank=True, null=True)
    specification_length = models.FloatField(blank=True, null=True)
    minimum_flowrate = models.FloatField(blank=True, null=True)
    maximum_flowrate = models.FloatField(blank=True, null=True)
    maximum_rpm = models.FloatField(blank=True, null=True)
    minimum_rpm = models.FloatField(blank=True, null=True)
    max_dp = models.FloatField(blank=True, null=True)
    recom_dp = models.FloatField(blank=True, null=True)
    max_wob = models.FloatField(blank=True, null=True)
    maximum_hydrostatic_pressure = models.FloatField(blank=True, null=True)
    maximum_mud_weight = models.FloatField(blank=True, null=True)
    minimum_mud_weight = models.FloatField(blank=True, null=True)
    no_load_diff_pressure = models.FloatField(blank=True, null=True)
    
    class Mata:
        db_table = "bhadata_specifications"