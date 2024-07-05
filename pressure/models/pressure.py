from django.db import models

# Create your models here.
class Pressure(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    measured_depth = models.FloatField(blank=True, null=True)
    true_vertical_depth = models.FloatField(blank=True, null=True)
    pore_pressure = models.FloatField(blank=True, null=True)
    fracture_pressure = models.FloatField(blank=True, null=True)
    comments = models.CharField(max_length=250,blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    pressure_unit = models.CharField(max_length=250,blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

