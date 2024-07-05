from django.db import models
from django.db.models import signals
from django.contrib.auth.models import Group
from helpers.commonimport import Count,Q

def create_project(sender, instance, **kwargs):
    print("Project Created")

class ProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def createproject(self,project_name,unit,country,company,user):
        return self.create(project_name=project_name,unit=unit,country_id=country,company=company,created_by_id=user)
    
    def getproject_byid(self,id):
        return self.get(id=id)
    
    def getindividual_projects(self,user_id):
        return self.filter(created_by_id=user_id,status=1)
    
    def getcompanies_projects(self,company_id):
        return self.filter(company_id=company_id,status=1)
    
    def getfiltered_projects_company(self,selected_values,company_id,offset,limit,request):
        if(request.role=='Admin'):
            filter_condition = {'country_id__in': selected_values, 'company_id': company_id,'status':1}
        else:
            filter_condition = {'country_id__in': selected_values, 'company_id': company_id,'status':1,'projectusers__user_id':request.user.id}
        return self.filter(**filter_condition).prefetch_related('projectusers_set')[offset:offset+limit]
    
    def getallfiltered_projects_company(self,selected_values,company_id,request):
        if(request.role=='Admin'):
            filter_condition = {'country_id__in': selected_values, 'company_id': company_id,'status':1}
        else:
            filter_condition = {'country_id__in': selected_values, 'company_id': company_id,'status':1,'projectusers__user_id':request.user.id}
        return self.filter(**filter_condition).prefetch_related('projectusers_set')
    
    def getfiltered_projects_individual(self,selected_values,user_id,offset,limit):
        return self.filter(country_id__in=selected_values,created_by_id=user_id)[offset:offset+limit]
    def getallfiltered_projects_individual(self,selected_values,user_id):
        return self.filter(country_id__in=selected_values,created_by_id=user_id)
    
    def getproject_bygroupcountry(self,request):
        if(request.role=='Admin'):
            filter_condition = {'company_id': request.company.id,'status':1}
        else:
            filter_condition = {'projectusers__user_id': request.user.id, 'company_id': request.company.id,'status':1}
        return self.filter(**filter_condition).values('country').annotate(country_count=Count('country')).prefetch_related('projectusers_set')
    
    def getproject_bygroupcountry_filtercountries(self,company_id,country_ids):
        return self.filter(company_id=company_id,country_id__in=country_ids).values('country').annotate(country_count=Count('country'))
        
    def getproject_bygroupcountry_indfiltercountries(self,user_id,country_ids):
        return self.filter(created_by_id=user_id,country_id__in=country_ids).values('country').annotate(country_count=Count('country'))
        
    def getproject_bygroupcountry_individual(self,user_id):
        return self.filter(created_by_id=user_id,status=1).values('country').annotate(country_count=Count('country'))
    
    def update_project_status(self,project_id):
        return self.filter(id=project_id).update(status=0)
    
   
    
class Projects(models.Model):  
    API = 0
    SI = 1
    MIXED = 2

    UNITS = (
        (API, 'API'),
        (SI, 'SI'),
        (MIXED, 'MIXED'),
    )

    id = models.AutoField(primary_key=True)
    project_name= models.CharField(max_length=255)
    country = models.ForeignKey("custom_auth.Countries",on_delete=models.CASCADE,blank=True, null=True)
    block= models.CharField(max_length=255, blank=True, null=True)
    field= models.CharField(max_length=255, blank=True, null=True)
    unit= models.CharField(max_length=255, blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    created_by = models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True,default=1)
    objects=ProjectManager()


# class Userrights(models.Model):  
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
#     module = models.ForeignKey("custom_auth.Modules",on_delete=models.CASCADE,blank=True, null=True)
#     create=models.IntegerField(blank=True,default=0, null=True)
#     edit=models.IntegerField(blank=True,default=0, null=True)
#     view=models.IntegerField(blank=True,default=0, null=True)
#     delete=models.IntegerField(blank=True,default=0, null=True)
#     permission_type=models.IntegerField(blank=True,default=0, null=True)
#     project=models.ForeignKey("projects.Projects",on_delete=models.CASCADE,blank=True, null=True)
#     well=models.ForeignKey("wells.Wells",on_delete=models.CASCADE,blank=True, null=True)
#     status = models.IntegerField(blank=True,default=0, null=True)
#     class Meta:
#         db_table = "userrights"

# class Projectuserrights(models.Model):  
#     id = models.AutoField(primary_key=True)
#     rights = models.ForeignKey("Userrights",on_delete=models.CASCADE,blank=True, null=True)
#     project=models.ForeignKey("projects.Projects",on_delete=models.CASCADE,blank=True, null=True)
#     well=models.ForeignKey("wells.Wells",on_delete=models.CASCADE,blank=True, null=True)
#     status = models.IntegerField(blank=True,default=0, null=True)
#     class Meta:
#         db_table = "project_userrights"

signals.post_save.connect(receiver=create_project, sender=Projects)
