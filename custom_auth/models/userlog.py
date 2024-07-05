from django.db import models
from django.utils import timezone
from helpers.commonimport import Q

class UserlogManager(models.Manager):
    def getwell_logs(self,well_id,user_id,offset,limit,start_date,end_date,search_value):
        filter_condition = Q(well_id=well_id,user_id=user_id)  
        if(search_value):
            filter_condition &= (Q(message__icontains=search_value) | Q(source_Type__icontains=search_value))
        if start_date and not end_date:
            filter_condition &= Q(time__gte=start_date)
        elif end_date and not start_date:
            filter_condition &= Q(time__lte=end_date)
        elif start_date and end_date:
            filter_condition &= Q(time__range=(start_date, end_date))
        
        return self.filter(filter_condition)[offset:offset+limit] 

    def getallwell_logs(self,well_id,user_id,start_date,end_date,search_value):
        filter_condition = Q(well_id=well_id,user_id=user_id)  
        if(search_value):
            filter_condition &= (Q(message__icontains=search_value) | Q(source_Type__icontains=search_value))
        if start_date and not end_date:
            filter_condition &= Q(time__gte=start_date)
        elif end_date and not start_date:
            filter_condition &= Q(time__lte=end_date)
        elif start_date and end_date:
            filter_condition &= Q(time__range=(start_date, end_date))
        return self.filter(filter_condition)
    
    def getproj_logs(self,well_id,offset,limit,start_date,end_date,search_value,user_id):
        filter_condition = Q(project_id=well_id,user_id=user_id)  
        if(search_value):
            filter_condition &= (Q(message__icontains=search_value) | Q(source_Type__icontains=search_value))
        if start_date and not end_date:
            filter_condition &= Q(time__gte=start_date)
        elif end_date and not start_date:
            filter_condition &= Q(time__lte=end_date)
        elif start_date and end_date:
            filter_condition &= Q(time__range=(start_date, end_date))
        return self.filter(filter_condition)[offset:offset+limit] 
    
    def getallproj_logs(self,well_id,start_date,end_date,search_value,user_id):
        filter_condition = Q(project_id=well_id,user_id=user_id)  
        if(search_value):
            filter_condition &= (Q(message__icontains=search_value) | Q(source_Type__icontains=search_value))
        if start_date and not end_date:
            filter_condition &= Q(time__gte=start_date)
        elif end_date and not start_date:
            filter_condition &= Q(time__lte=end_date)
        elif start_date and end_date:
            filter_condition &= Q(time__range=(start_date, end_date))
        return self.filter(filter_condition)
    
    def getuserlog(self,company_id,licence_type,offset,limit):
        return self.filter(from_id=company_id,licence_type=licence_type)[offset:offset+limit]
    def getalluserlog(self,company_id,licence_type):
        return self.filter(from_id=company_id,licence_type=licence_type)

class Userlog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User",on_delete=models.CASCADE,blank=True, null=True)
    message = models.CharField(max_length=50)
    source_id = models.CharField(max_length=50)
    source_Type = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True, editable=False)
    from_id=models.IntegerField(blank=True,null=True) 
    licence_type=models.CharField(max_length=30,blank=True,null=True) 
    project_id = models.IntegerField(blank=True,null=True)
    well_id = models.IntegerField(blank=True,null=True)
    wellphase_id = models.IntegerField(blank=True,null=True)
    status = models.IntegerField(blank=True,default=1)
    is_superadmin = models.BooleanField(('is_superadmin'), default=False)
    userlog_type=models.CharField(max_length=20,blank=True,null=True) 

    objects=UserlogManager()

    class Meta:
        db_table = "userlog"