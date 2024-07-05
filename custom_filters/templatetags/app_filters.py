from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='unit')
def unit(data, args):
    return data+" MM"



    



