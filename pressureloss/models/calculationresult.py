from django.db import models


class CalculationchartdataManager(models.Manager):
    def create_calculation_result(self,well_id,wellphase_id,section_name,result_type,result,input_data,project_id=None):
        getresult=self.filter(well_id=well_id,wellphase_id=wellphase_id,result_type=result_type)
        if(getresult.count() > 0):
            return self.filter(well_id=well_id,wellphase_id=wellphase_id,result_type=result_type).update(result=result,input_data=input_data)
        else:
            return self.create(well_id=well_id,project_id=project_id,wellphase_id=wellphase_id,section_name=section_name,result_type=result_type,result=result,input_data=input_data)
    
    def get_calculation_result(self,well_id,wellphase_id,result_type,section_name):
        return self.get(well_id=well_id,wellphase_id=wellphase_id,result_type=result_type,section_name=section_name)
    
    def get_calculation_inputdata(self,well_id,wellphase_id,section_name):
        return self.filter(well_id=well_id,wellphase_id=wellphase_id,result_type='alongwellecd_data',section_name=section_name).first()
   
    def get_allcalculationdata(self,wellphase_id,section_name):
        return self.filter(wellphase_id=wellphase_id,section_name=section_name)
   

    
class Calculationchartdata(models.Model):
    id = models.AutoField(primary_key=True)
    well_id = models.IntegerField(blank=True,null=True)
    project_id = models.IntegerField(blank=True,null=True)
    wellphase_id = models.IntegerField(blank=True,null=True)
    section_name = models.CharField(max_length=50,null=True) 
    result_type = models.CharField(max_length=50,null=True) 
    result = models.TextField(blank=True,null=True)
    input_data = models.TextField(blank=True,null=True)
    objects=CalculationchartdataManager()

    class Meta:
        db_table = 'calculation_chartdata'

    def __str__(self):
        return str(self.pk)