from django.db import models
from helpers.commonimport import Q


class TicketsManager(models.Manager):
    def createticket(self,title,message,sender,license_type,company_id,user_id,ticket_type,message_id,status,is_superadmin):
        print(f"message1 {message}")

        if(license_type != 'Individual'):
            return self.create(title=title,message=message,sender=sender,company_id=company_id,ticket_type=ticket_type,status=status,licence_type=license_type)
        else:
            return self.create(title=title,message=message,sender=sender,user_id=user_id,ticket_type=ticket_type,status=status,licence_type=license_type)

    def getticket_byid(self,id):
        return self.get(id=id)
    def getticket(self,limit,offset,request):
        if(request.user.licence_type != 'Individual'):
            return self.filter(company_id=request.company.id).order_by('-id')[offset:offset+limit]
        else:
            return self.filter(user_id=request.user.id).order_by('-id')[offset:offset+limit]
    
    def getallticket(self,request):
        if(request.user.licence_type != 'Individual'):
            return self.filter(company_id=request.company.id).order_by('-id')
        else:
            return self.filter(user_id=request.user.id).order_by('-id')
    
    def getpoaticket(self,limit,offset,search_value):
        return self.filter(Q(title__icontains=search_value)| Q(message__icontains=search_value)).order_by('-id')[offset:offset+limit]
    
    def getallpoaticket(self,search_value):
        return self.filter(Q(title__icontains=search_value)| Q(message__icontains=search_value)).order_by('-id')
    
    def updateassigne(self,ticket_id,user_id):
        return self.filter(id=ticket_id).update(assigne=user_id,status='ongoing')

    def createticketmessage(self,message,sender,message_id,uid):
        return self.create(message=message,sender=sender,message_id=message_id,uid=uid)
    
    def check_message_exist(self,uid,sender):
        try:
            return self.get(uid=uid,sender=sender)
        except Tickets.DoesNotExist:
            return None
    def getallmessages_byticketid(self,message_id):
        return self.filter(message_id=message_id)





class Tickets(models.Model):
    TYPE_CHOICES = (
        ('email', 'Email'),
        ('software', 'Software'),
    )
    id = models.AutoField(primary_key=True) 
    title = models.CharField(max_length=50,blank=True,null=True)
    message = models.TextField(blank=True,null=True)
    sender = models.IntegerField(blank=True,null=True) 
    message_id = models.IntegerField(blank=True,null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    is_superadmin = models.BooleanField(('is_superadmin'), default=False)
    ticket_type= models.CharField(max_length=10,choices=TYPE_CHOICES,blank=True,null=True)
    assigne= models.IntegerField(blank=True,null=True)
    status = models.CharField(blank=True,null=True,max_length=20)
    licence_type = models.CharField(choices=(('Individual', 'Individual'), ('CompanyPlan', 'CompanyPlan'), ('Enterprise','Enterprise')), max_length=50, blank=True, null=True)
    uid=models.CharField(max_length=455,blank=True, null=True)
    timestamp=models.DateTimeField(auto_now_add=True,blank=True, null=True)

    objects=TicketsManager()

    class Meta:
        db_table = "tickets"

class TicketattachmentsManager(models.Manager):
    def createticketattachments(self,ticket_id,attachment,filename):
        return self.create(ticket_id=ticket_id,attachment=attachment,name=filename)
    def getattachments_byticketid(self,ticket_id):
        return self.filter(ticket_id=ticket_id,status=1)
    def getattachments_byid(self,ticket_id):
        return self.get(id=ticket_id)
    def uploadattachments(self,attachment,name):
        return self.create(attachment=attachment,name=name)
    def updateticket_id(self,id,ticket_id):
        return self.filter(id=id).update(ticket_id=ticket_id)


class Ticketattachments(models.Model):
    id = models.AutoField(primary_key=True) 
    ticket= models.ForeignKey("Tickets",on_delete=models.CASCADE,blank=True, null=True)
    attachment = models.FileField(upload_to='ticket_attachments/',null=True,blank=True)
    name = models.CharField(blank=True,null=True,max_length=255)
    status = models.IntegerField(blank=True,default=1)
    objects=TicketattachmentsManager()

    class Meta:
        db_table = "ticket_attachments"

class TicketrecipientManager(models.Manager):
    def createticketrecipient(self,ticket_id,user_id):
        return self.create(ticket_id=ticket_id,user_id=user_id)
    
    def getsuperuseticket(self,user_id,limit,offset,search_value):
        return self.select_related('ticket').filter(Q(user_id=user_id) & (Q(ticket__title__icontains=search_value)| Q(ticket__message__icontains=search_value))).order_by('-id')[offset:offset + limit]
    
    def getallsuperuseticket(self,user_id,search_value):
        return self.select_related('ticket').filter(Q(user_id=user_id) & (Q(ticket__title__icontains=search_value)| Q(ticket__message__icontains=search_value))).order_by('-id')
       

    
class Ticketrecipient(models.Model):
    id = models.AutoField(primary_key=True) 
    ticket= models.ForeignKey("Tickets",on_delete=models.CASCADE,blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True,default=1)
    objects=TicketrecipientManager()
    class Meta:
        db_table = "ticket_recipients"





    