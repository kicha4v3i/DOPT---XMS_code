
from django.db import models

class CoordinateSystems(models.Model):  
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    status = models.IntegerField(blank=True,default=1)

class Projections(models.Model):  
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    status = models.IntegerField(blank=True,default=1)

class WellsManager(models.Manager):
    def getwell_byid(self,id):
        return self.get(id=id)

    def getwell_and_project_byid(self,id):
        return self.select_related('project').get(id=id)
    def getindividual_wells(self,proj_id,user_id):
        return self.filter(created_by_id=user_id,project_id=proj_id)
    
    
    def getfiltered_wells(self,total_projects_id,offset,limit):
        return self.filter(project_id__in=total_projects_id)[offset:offset+limit]
    
    def getallfiltered_wells(self,total_projects_id):
        return self.filter(project_id__in=total_projects_id)

# Create your models here.
class Wells(models.Model):

    # Relationships
    #project_id = models.ForeignKey("project.projects",on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey("projects.Projects",on_delete=models.CASCADE,blank=True, null=True)
    block = models.ForeignKey("projects.ProjectBlock",on_delete=models.CASCADE,blank=True, null=True)
    field = models.ForeignKey("projects.ProjectField",on_delete=models.CASCADE,blank=True, null=True)

    # Fields
    number_of_well_pads = models.FloatField(blank=True, null=True)
    ground_elevation = models.FloatField(blank=True, null=True)
    air_gap = models.FloatField(blank=True, null=True)
    slot_longtitude = models.CharField(max_length=60,blank=True, null=True)
    name = models.CharField(max_length=60)
    environment = models.CharField(max_length=30,blank=True, null=True)
    longtitude = models.CharField(max_length=60,blank=True, null=True)
    #project_id = models.IntegerField(blank=True, null=True)
    zone = models.CharField(max_length=30,blank=True, null=True)
    rkb_wellhead = models.FloatField(blank=True, null=True)
    well_type = models.CharField(max_length=30,blank=True, null=True)
    plan_well_list = models.ForeignKey("wells.Wells",on_delete=models.CASCADE,blank=True, null=True)
    number_of_well_slots_in_pad = models.FloatField(blank=True, null=True)
    projection = models.ForeignKey("Projections",on_delete=models.CASCADE,blank=True, null=True)
    latitude = models.CharField(max_length=60,blank=True, null=True)
    slot_easting = models.FloatField(blank=True, null=True)
    water_depth = models.FloatField(blank=True, null=True)
    number_of_slots_in_platform = models.FloatField(blank=True, null=True)
    wellhead_to_datum = models.FloatField(blank=True, null=True)
    platform_name = models.CharField(max_length=30,blank=True, null=True)
    slot_no = models.FloatField(blank=True, null=True)
    slot_latitude = models.CharField(max_length=60,blank=True, null=True)
    datum = models.CharField(max_length=60,blank=True, null=True)
    pad_name = models.CharField(max_length=30,blank=True, null=True)
    northing = models.CharField(max_length=10,blank=True, null=True)
    rkb_datum = models.FloatField(blank=True, null=True)
    cluster_name = models.CharField(max_length=60,blank=True, null=True)
    well_slot_no_or_name = models.CharField(max_length=60,blank=True, null=True)
    environment_sub_type = models.CharField(max_length=60,blank=True, null=True)
    easting = models.CharField(max_length=10,blank=True, null=True)
    coordinate_system = models.ForeignKey("CoordinateSystems",on_delete=models.CASCADE,blank=True, null=True)
    slot_northing = models.FloatField(blank=True, null=True)
    created_by = models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True,default=1)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    objects=WellsManager()

    class Meta:
        pass

    def __str__(self):
        return str(self.name)