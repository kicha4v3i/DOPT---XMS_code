from django import template
from helpers.allmodels import PumpManufacturer,Pumps


register = template.Library()

@register.simple_tag 
def getpumpmanufacture(manufacture_id):
    pumps=PumpManufacturer.objects.getpumpmanufacture(manufacture_id)
    return pumps

@register.simple_tag 
def getpumpdetails(pump_id):
    pump=Pumps.objects.getpumpdetails(pump_id)
    return pump

@register.simple_tag 
def getpumps_bymanufacture(manufacture_id,company):
    pumps=Pumps.objects.getallpump_bymanufacture(manufacture_id)
    return pumps