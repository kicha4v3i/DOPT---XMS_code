from django.db import models

class SurfacePipeDataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def getsurfacepipedata(self,surfacepipe):
        return self.filter(surfacepipe_id=surfacepipe)

class SurfacePipeData(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("wells.Wells", on_delete=models.CASCADE,blank=True, null=True)
    surfacepipe= models.ForeignKey("surfacepipe.SurfacePipe", on_delete=models.CASCADE,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=30,blank=True, null=True)
    length = models.CharField(max_length=30,blank=True, null=True)
    identity = models.CharField(max_length=30,blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False,blank=True, null=True)
    objects=SurfacePipeDataManager()
    
    class Meta:
        pass

    def __str__(self):
        return str(self.pk)