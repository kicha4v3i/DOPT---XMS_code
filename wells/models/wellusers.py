from django.db import models
from helpers.commonimport import Q,ObjectDoesNotExist

class WellUsersManager(models.Manager):
    def getuserwells(self,user_id):
        return self.filter(user_id=user_id).select_related('well')
    def getwellusers(self,well_id):
        return self.filter(well_id=well_id,status=1)
    def updatewellusers(self,well_id,olduser_id,newuser_id):
        return self.filter(well_id=well_id,user_id=olduser_id).update(user_id=newuser_id,status=1)
    def getwellusers_byid_well(self,well_id,user_id):
        try:
            return self.get(well_id=well_id,user_id=user_id)
        except ObjectDoesNotExist:
            return None

    def updatestatus_id(self,id):
        return self.filter(id=id).update(status=1)
    def createwelluser(self,wellid,user):
        return self.create(well_id=wellid,user_id=user,role_id=2,status=1) 
    def getremovingusers(self,user_ids,well_id):
        return self.filter(Q(well_id=well_id) & ~Q(id__in=user_ids))
    def updateremovingusers(self,ids,well_id):
        return self.filter(well_id=well_id,id__in=ids).update(status=0)
    def getwell_userid(self,user_id):
        return self.filter(user_id=user_id,status=1)

class WellUsers(models.Model):  
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey("Wells",on_delete=models.CASCADE,blank=True, null=True)
    user = models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    role = models.ForeignKey("auth.Group",on_delete=models.CASCADE,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True,default=1)
    objects=WellUsersManager()
