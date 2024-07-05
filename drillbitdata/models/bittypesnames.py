from django.db import models

class BitTypesNamesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def getbittypesname(self,bit_type_id):
        return self.get(id=bit_type_id)

class BitTypesNames(models.Model):
    id = models.AutoField(primary_key=True)
    bittype_names = models.CharField(max_length=100,null=True)  
    bit_values = models.FloatField(blank=True, null=True)
    objects=BitTypesNamesManager()
    class Meta:
        db_table = "bittype_names"
    def __str__(self):
        return str(self.bittype_names)