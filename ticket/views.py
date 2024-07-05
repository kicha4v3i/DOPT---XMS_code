from django.shortcuts import render,redirect
from custom_auth.models import User
from notifications.signals import notify
from django.core import serializers
from helpers.commonimport import base64,Image,io,FileSystemStorage,View,os,mimetypes,settings,unquote,JsonResponse,HttpResponse,Http404,json
from helpers.allmodels import CountryUsers,Tickets,Ticketattachments,Ticketrecipient,Companies
from helpers.unit_calculation import getassigneusers_tickets,getassigneusers_tickets_excludepoa
from django.views.decorators.clickjacking import xframe_options_exempt




def queries(request):
    request.session['mainmenu'] = "queries"
    return render(request,'queries.html')

def poaqueries(request):
    request.session['mainmenu'] = "queries"
    return render(request,'poaqueries.html')

    

def query_form(request):
    scheme=request.scheme
    gethost=request.get_host()
    url=json.dumps({"url":scheme+'://'+gethost+'/ticket/queries'})

    if request.method =='POST':  
        title = request.POST.get('title')
        message = request.POST.get('ticket_message')
        if(request.user.licence_type != 'Individual'):
            country_id=request.company.country_id
        else:
            country_id=request.user.country_user
        country_allcountry_user=getassigneusers_tickets(country_id)
       
        if(request.user.licence_type != 'Individual'):
            queries = Tickets.objects.createticket(title,message,request.user.id,request.user.licence_type,request.company.id,None,'software',None,'pending',0)
        else:
            queries = Tickets.objects.createticket(title,message,request.user.id,request.user.licence_type,None,request.user.id,'software',None,'pending',0)
        for user in country_allcountry_user:
            Ticketrecipient.objects.createticketrecipient(queries.id,user['id'])
            recipient_user = User.objects.get(id=user['id'])
            notify.send(request.user, recipient=recipient_user,extra_data=url, verb='New Ticket', description='New Ticket Received From '+request.user.name,action_object=queries)


        if 'attachment' in request.FILES:
            ticket_attachments=request.FILES.getlist('attachment')
            for ticket_attachment in ticket_attachments:
                # fs = FileSystemStorage()
                # filename = "ticket" + ticket_attachment.name
                # ticket_attachmentfile = fs.save(filename, ticket_attachment)
                Ticketattachments.objects.createticketattachments(queries.id,ticket_attachment,ticket_attachment.name)
        return redirect('ticket:queries')
    
    return render(request,'query_form.html')


def query_chat(request):
    
    query_id = request.GET.get('query_id')
    ticket = Tickets.objects.filter(id=query_id, message_id__isnull=True).first()

    if request.user.is_superuser:
        sender = ticket.recipient 
        recipient = ticket.sender
    else:
        sender = ticket.sender 
        recipient = ticket.recipient
    print('tickets_first',ticket)

    if request.method == 'POST' : 
       
        # file_input = request.FILES.get('file_input')
        query_input = request.POST.get('query_input')
        # print('file_inputss',file_input)
        Tickets.objects.create(title=ticket.title,message=query_input,sender=sender,recipient=recipient,message_id=query_id)

    tickets_chat = Tickets.objects.filter(message_id=query_id)
    context = {
        'query_id':query_id,
        'user_id':request.user.id,
        'first_message':ticket.message,
        'tickets_chat':tickets_chat
    }
    return render(request,'query_chat.html',context)

def query_chat_message(request):
    value = request.GET.get('query_chat_id')
    tickets_chat = Tickets.objects.filter(message_id=value)
    data = serializers.serialize('json', tickets_chat)
    json_data = json.loads(data)
    return JsonResponse(json_data,safe=False)

@xframe_options_exempt
def startticket(request, id):  
    ticket_details=Tickets.objects.getticket_byid(id)
    allmessages=Tickets.objects.getallmessages_byticketid(id)
    print(f"allmessages {allmessages}")

    return render(request,'query_chat.html',{'ticket_id':id,'request':request,'ticket_details':ticket_details,'allmessages':allmessages})
   
class Viewticket(View):
    def get(self,request,id):
        ticket_details=Tickets.objects.getticket_byid(id)
        if(ticket_details.licence_type != 'Individual'):
            company_details=Companies.objects.getcompanyname_byid(ticket_details.company_id)
            country_id=company_details.country_id
        else:
            user_details=User.objects.getuserid(ticket_details.user_id)
            country_id=user_details.country_user
        country_allcountry_user=getassigneusers_tickets_excludepoa(country_id)
        return render(request,'viewticket.html',{'ticket_details':ticket_details,'country_allcountry_users':country_allcountry_user})
    def post(self,request,id):
        ticket_details=Tickets.objects.getticket_byid(id)
        if(ticket_details.licence_type != 'Individual'):
            company_details=Companies.objects.getcompanyname_byid(ticket_details.company_id)
            country_id=company_details.country_id
        else:
            user_details=User.objects.getuserid(ticket_details.user_id)
            country_id=user_details.country_user
        country_allcountry_user=getassigneusers_tickets_excludepoa(country_id)
        user=request.POST.get('user')
        Tickets.objects.updateassigne(id,user)
        return render(request,'viewticket.html',{'ticket_details':ticket_details,'country_allcountry_users':country_allcountry_user})


def file_upload(request):
    if request.method == 'POST':
        attachments=request.FILES.getlist('query_attachment_file')
        print(f"attachments {attachments}")
        attachments_data=[]
        for file in attachments:
            attachment_details=Ticketattachments.objects.uploadattachments(file,file.name)
            attachments_data.append({'id':attachment_details.id,'name':file.name})

        return JsonResponse({'data':attachments_data})


class Emailquery(View):
    def get(self,request):
        return render(request,'emailquery.html')


class Sendmessage(View):
    def post(self,request):
        ticket_data = json.loads(request.POST.get('ticket_data'))
        message=Tickets.objects.createticketmessage(ticket_data['message'],ticket_data['sender'],ticket_data['message_id'],ticket_data['uid'])
        if(ticket_data['attachments']):
            atachments_list=json.loads(ticket_data['attachments'])
            for atachment in atachments_list:
                Ticketattachments.objects.updateticket_id(atachment['id'],message.id)
        return JsonResponse(ticket_data)

def getalltickets(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
   
    filtered_tickets = Tickets.objects.getticket(length,start,request)
    total_records = Tickets.objects.getallticket(request).count()

    data = []
    i=1
    for ticket in filtered_tickets:
        data.append({
            'sno':i,
            'title': ticket.title,
            'message': ticket.message,
            'status':ticket.status,
            'id':ticket.id,
        })
        i +=1
    
    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)


def getallpoatickets(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    print(f"search_value {search_value}")
    data = []
    if(request.user.is_superadmin == 1):
        filtered_tickets = Tickets.objects.getpoaticket(length,start,search_value)
        total_records = Tickets.objects.getallpoaticket(search_value).count()
    elif(request.user.is_superuser == 1):
        filtered_tickets = Ticketrecipient.objects.getsuperuseticket(request.user.id,length,start,search_value)
        total_records = Ticketrecipient.objects.getallsuperuseticket(request.user.id,search_value).count()
    
    i=1
    for ticket in filtered_tickets:
        license_type=ticket.licence_type if(request.user.is_superadmin == 1) else ticket.ticket.licence_type
        ticket_details=ticket if(request.user.is_superadmin == 1) else ticket.ticket
        assigne=ticket.assigne if(request.user.is_superadmin == 1) else ticket.ticket.assigne

        if(license_type != 'Individual'):
            company_details=Companies.objects.getcompanyname_byid(ticket_details.company_id)
            name=company_details.company_name
            mainuser=User.objects.getadminuser(company_details.id)
            designation=mainuser.designation
        else:
            user_details=User.objects.getuserid(ticket_details.user_id)
            name=user_details.name+' '+user_details.lastname
            designation=user_details.designation
        data.append({
            'sno':i,
            'title': ticket.title if(request.user.is_superadmin == 1) else ticket.ticket.title,
            'message': ticket.message if(request.user.is_superadmin == 1) else ticket.ticket.message,
            'status':ticket.status if(request.user.is_superadmin == 1) else ticket.ticket.status,
            'id':ticket.id if(request.user.is_superadmin == 1) else ticket.ticket.id,
            'designation':designation,
            'name':name,
            'assigne':ticket.assigne if(request.user.is_superadmin == 1) else ticket.ticket.assigne,
            'is_assigne':True if(assigne==request.user.id) else False
            
        })
        i +=1
    
    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)

def download_attachment(request, attachment_id):
    attachment = Ticketattachments.objects.getattachments_byid(attachment_id)
    file_path = os.path.join(settings.MEDIA_ROOT,'ticket_attachments', unquote(attachment.name))
    file_name = os.path.basename(file_path)
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
   
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=content_type)

    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    return response





   



