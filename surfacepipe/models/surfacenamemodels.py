from django.db import models

class SurfaceNameModels(models.Model):
    id = models.AutoField(primary_key=True)
    surfacepiping_name = models.CharField(max_length=100,null=True)  
    
    class Meta:
        db_table = "surfacepiping_names"