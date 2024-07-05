from django.db import models
from helpers.commonimport import Q


class ProjectuserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def createprojectuser(self,projectid,user):
        return self.create(project_id=projectid,user_id=user,role_id=2,status=1) 
    def filterproj_getuserid(self,proj_id):
        return self.filter(project_id=proj_id).values_list('user_id', flat=True)
    def filterprojstatus_getuserid(self,proj_id,status):
        return self.filter(project_id=proj_id,status=status).values_list('user_id','user__name', 'user__lastname')
    def update_status(self,project_id,user_ids,status):
        return self.filter(project_id=project_id,user_id__in=user_ids).update(status=status)
    def getproject_userid(self,user_id):
        return self.filter(user_id=user_id,status=1)
    def getuserprojects(self,user_id):
        return self.filter(user_id=user_id).select_related('project')
    def getprojectusers(self,project_id):
        return self.filter(project_id=project_id,status=1)
    def updateprojectusers(self,project_id,olduser_id,newuser_id):
        return self.filter(project_id=project_id,user_id=olduser_id).update(user_id=newuser_id,status=1)
    def getprojectusers_byid_project(self,project_id,user_id):
        return self.get(project_id=project_id,user_id=user_id)
    def updatestatus_id(self,id):
        return self.filter(id=id).update(status=1)
    def getremovingusers(self,user_ids,project_id):
        return self.filter(Q(project_id=project_id) & ~Q(id__in=user_ids))
    def updateremovingusers(self,ids,project_id):
        return self.filter(project_id=project_id,id__in=ids).update(status=0)
    def checkuserexist(self,project_id,user_id):
        return self.filter(project_id=project_id,user_id=user_id,status=1)

class ProjectUsers(models.Model):   
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey("Projects",on_delete=models.CASCADE,blank=True, null=True)
    user = models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    role = models.ForeignKey("auth.Group",on_delete=models.CASCADE,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True,default=1)
    objects=ProjectuserManager()
