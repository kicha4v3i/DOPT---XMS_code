from django.db import models

# Create your models here.
class Rig(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    rig_name = models.CharField(max_length=60,blank=True, null=True)
    rig_contractor = models.CharField(max_length=60,blank=True, null=True)
    rig_type = models.CharField(max_length=60,blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        db_table = "rig_information"

