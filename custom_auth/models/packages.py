from django.db import models

class Packages(models.Model):  
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    types = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True,default=1)
    def __str__(self):
        return self.name


class PackageConcurrentUsers(models.Model):  
    id = models.AutoField(primary_key=True)
    package = models.ForeignKey("Packages",on_delete=models.CASCADE)
    name= models.CharField(max_length=50)
    concurrent_users=models.IntegerField(blank=True,default=0)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True,default=1)

class PackageUsers(models.Model):  
    id = models.AutoField(primary_key=True)
    package_concurrent_users = models.ForeignKey("PackageConcurrentUsers",on_delete=models.CASCADE)
    name= models.CharField(max_length=50)
    concurrent_users=models.IntegerField(blank=True,default=0)
    admins=models.IntegerField(blank=True,default=1)
    well_managers=models.IntegerField(blank=True,default=0)
    well_engineers=models.IntegerField(blank=True,default=0)
    other_users=models.IntegerField(blank=True,default=0)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True,default=1)