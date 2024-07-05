from django.db import models

class SurfacePipeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def getsurfacepipe(self,well_id):
        return self.filter(well_id=well_id).first()
    
  
 

class SurfacePipe(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    objects=SurfacePipeManager()


    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
