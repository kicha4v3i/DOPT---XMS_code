from django.db import models

class Drillcollers(models.Model):
    id = models.AutoField(primary_key=True)
    normal_od=models.FloatField(blank=True, null=True)
    normal_id=models.FloatField(blank=True, null=True)
    weight=models.FloatField(blank=True, null=True)
    pipe_type=models.CharField(max_length=30,blank=True, null=True)
    connection_type=models.CharField(max_length=30,blank=True, null=True)
    tool_od=models.FloatField(blank=True, null=True)
    tool_id=models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=30,blank=True, null=True)
    # length_onejoint=models.FloatField(blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    is_superadmin = models.IntegerField(blank=True,default=0)

    class Mata:
        db_table = "bhadata_drillcollars"