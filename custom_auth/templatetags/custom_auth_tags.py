from django import template
register = template.Library()
from helpers.allmodels import User,Countries,Rights,Modules

# get user role id
@register.simple_tag
def getusergroup(userid):
    user = User.objects.get(id=userid)
    groups = user.groups.all()
    group_id=''
    for group in groups:
        group_id=group.id
    return group_id

@register.simple_tag
def getcountry_byid(country_id):
    return Countries.objects.getcountry_byid(country_id)






@register.simple_tag
def getuserrights(module_id,role_id,company_id):
    rights = Rights.objects.check_userrights(role_id,module_id,company_id)
    if(rights.count()>0):
        if(rights[0].status==1):
            return True
        else:
            return False
   
@register.simple_tag
def getsubmenu(mainmenu_id):
    return Modules.objects.getsubmodules(mainmenu_id)
