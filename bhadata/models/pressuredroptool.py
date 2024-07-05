from django.db import models


class Pressuredroptool(models.Model):
    id = models.AutoField(primary_key=True)
    bhadata= models.ForeignKey("bhadata.BHAdata", on_delete=models.CASCADE,blank=True, null=True)
    bhadata_element= models.ForeignKey("bhadata.BhaElement", on_delete=models.CASCADE,blank=True, null=True)
    flowrate = models.FloatField(blank=True, null=True)
    pressure_drop = models.FloatField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)


    class Mata:
        db_table = "bhadata_pressuredrop"