from django.db import models

class ProjectblockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def createprojectblock(self,block,projectid):
        return self.create(block_name=block,project_id=projectid,status=1)
    
    def getblock_byid(self,id):
        return self.get(id=id)

class ProjectBlock(models.Model): 
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey("Projects",on_delete=models.CASCADE,blank=True, null=True)
    block_name= models.CharField(max_length=255)
    status = models.IntegerField(blank=True,default=1)
    objects=ProjectblockManager()
