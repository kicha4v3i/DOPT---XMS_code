from django.db import models

class ProjectfieldManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def createprojectfield(self,field,projectid,blockid):
        return self.create(field_name=field,project_id=projectid,status=1,block_id=blockid)

    def getfield_byid(self,id):
        return self.get(id=id)
    
    def getfield_byblockid(self,block_id,projectid):
        return self.filter(project_id=projectid,status=1,block_id=block_id)

class ProjectField(models.Model): 
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey("Projects",on_delete=models.CASCADE,blank=True, null=True)
    block = models.ForeignKey("ProjectBlock",on_delete=models.CASCADE,blank=True, null=True)
    field_name= models.CharField(max_length=255)
    status = models.IntegerField(blank=True,default=1)
    objects=ProjectfieldManager()
