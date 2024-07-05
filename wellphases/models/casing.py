from django.db import models

class CasingTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=250,blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class Casinggrade(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    is_superadmin = models.IntegerField(blank=True,default=0)
    grade_name = models.CharField(max_length=250,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    class Mata:
        db_table = "wellphases_casinggrade"
    
class Casingrange(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    is_superadmin = models.IntegerField(blank=True,default=0)
    range_name = models.CharField(max_length=250,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    class Mata:
        db_table = "wellphases_casingrange"

class Casing(models.Model):
    id = models.AutoField(primary_key=True)
    nominal_od=models.FloatField(blank=True, null=True)
    weight=models.FloatField(blank=True, null=True)
    inside_diameter=models.FloatField(blank=True, null=True)
    grade=models.CharField(max_length=30,blank=True, null=True)
    casing_range = models.CharField(max_length=30,blank=True, null=True)
    connection_type = models.CharField(max_length=30,blank=True, null=True)
    connection_od = models.FloatField(blank=True, null=True)
    is_superadmin = models.IntegerField(blank=True,default=0)
    unit = models.CharField(max_length=30,blank=True, null=True)
    drift_id=models.FloatField(blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    class Mata:
        db_table = "casing_master"