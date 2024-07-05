from django import template
from helpers.allmodels import User,Companies,Ticketattachments
register = template.Library()

# get user role id
@register.simple_tag
def getcompanydetails_byticket(ticket):
    print(f"ticket {ticket}")
    if(ticket.licence_type != 'Individual'):
        company_details=Companies.objects.getcompanyname_byid(ticket.company_id)
        name=company_details.company_name
        mainuser=User.objects.getadminuser(company_details.id)
        designation=mainuser.designation
    else:
        user_details=User.objects.getuserid(ticket.user_id)
        name=user_details.name+' '+user_details.lastname
        designation=user_details.designation
    data={
        'name':name,
        'designation':designation
    }
    return data

@register.simple_tag
def getticketattachments_byticket(ticket):
    attachments=Ticketattachments.objects.getattachments_byticketid(ticket.id)
    return attachments






