from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from wells.models import Wells,WellUsers,CoordinateSystems,Projections
from custom_auth.models import Countries,User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import WellsForm,WellUsersForm
from django.views.generic import ListView, DetailView
from projects.models import Projects,ProjectUsers,ProjectBlock,ProjectField
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from custom_auth.getunit import adduserlog,getcountries
from django.db.models import Count
from helpers.commonimport import notify,Notification,json
from custom_auth.models import Userlog
# Create your views here.
class IndexView(ListView):
    template_name = 'well/list.html'
    context_object_name = 'wells'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mainmenu'] = self.request.session['mainmenu']
        countrylist=[]
        if self.request.company:
            projects=Projects.objects.filter(company=self.request.company).values('country').annotate(Count('country'))
        else:
            projects=Projects.objects.filter(created_by_id=self.request.user.id).values('country').annotate(Count('country'))
        print('proj-list',projects)
        for project in projects:
            country=Countries.objects.filter(id=project['country']).first()
            countrylist.append({'name':country.name,'id':country.id})
        print('countrylist',countrylist)
        context['countries'] = countrylist
        context['company'] = self.request.company
        user_rights_privilege_project = "Create Project"
        user_rights_companyid = self.request.user.company_id
        user = User.objects.getuserid(self.request.user.id)
        user_rights_groups = user.groups.all().first()
        context['user_rights_privilege_project']=user_rights_privilege_project 
        context['user_rights_companyid']=user_rights_companyid
        context['user_rights_groups']=user_rights_groups
        


        print("dsg")
        if 'country' in self.request.session:
            del self.request.session['country']
        if 'project' in self.request.session:
            del self.request.session['project']
        if 'block' in self.request.session:
            del self.request.session['block']
        if 'field' in self.request.session:
            del self.request.session['field']
        if 'well' in self.request.session:
            del self.request.session['well']

        return context
    
    def get(self, request, *args, **kwargs):
        mainmenu = request.session.get('mainmenu')
        request.session['mainmenu'] = 'projects'
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return Wells.objects.filter(company=self.request.company).prefetch_related('wellusers_set')


class WellDetailView(DetailView):
    model = Wells
    template_name = 'well/view.html'
    context_object_name = 'well'
    def get_context_data(self, **kwargs):
        context = super(WellDetailView, self).get_context_data(**kwargs)
        self.request.session['well_id'] = self.get_object().id
        self.request.session['unit'] = self.get_object().project.unit
        self.request.session['welltype'] = self.get_object().well_type


        context['wellusers'] = WellUsers.objects.filter(well=self.get_object(),role=4)
        context['mainmenu'] = self.request.session['mainmenu']
        context['wellengineers'] = WellUsers.objects.filter(well=self.get_object(),role=3)
        countrylist=[]
        projects=Projects.objects.filter(company=self.request.company).values('country').annotate(Count('country'))
        for project in projects:
            country=Countries.objects.filter(id=project['country']).first()
            countrylist.append({'name':country.name,'id':country.id})
        context['project_id']=self.get_object().project.id
        context['user_id']=self.request.user.id
        context['module_id']="4"
        context['countries'] = countrylist
        context['company'] = self.request.company
        return context
    
    def get(self, request, *args, **kwargs):
        mainmenu = request.session.get('mainmenu')
        request.session['mainmenu']='projects'
        request.session['wellmenu']='well_details'
        request.session['submenu']=''



        

        return super().get(request, *args, **kwargs)
    
def getprojectblock(request):
    project_id=request.GET['project_id']
    blocks=ProjectBlock.objects.filter(project_id=project_id,status=1).values()
    return JsonResponse({"blocks": list(blocks)})

def getblockfield(request):
    project_id=request.GET['project_id']
    block_id=request.GET['block_id']

    fields=ProjectField.objects.filter(project_id=project_id,block_id=block_id,status=1).values()
    return JsonResponse({"fields": list(fields)})


def create(request,project_id=None):
    planwells = Wells.objects.filter(well_type='PLAN',company=request.company)
   
    if request.method == 'POST':
        form = WellsForm(request.POST)
        if form.is_valid():
            longtitude=(str(request.POST.get('longtitude_coords_degrees'))+u'\N{DEGREE SIGN}')+' '+(str(request.POST.get('longtitude_coords_minutes'))+"'")+' '+(str(request.POST.get('longtitude_coords_seconds'))+'"')+' '+request.POST.get('longtitude_compass')
            latitude=(str(request.POST.get('latitude_coords_degrees'))+u'\N{DEGREE SIGN}')+' '+(str(request.POST.get('latitude_coords_minutes'))+"'")+' '+(str(request.POST.get('latitude_coords_seconds'))+'"')+' '+request.POST.get('latitude_compass')
            well=form.save()
            if(request.POST.get('slot_longtitude_coords_degrees') !=''):
                slot_longtitude=(str(request.POST.get('slot_longtitude_coords_degrees'))+u'\N{DEGREE SIGN}')+' '+(str(request.POST.get('slot_longtitude_coords_minutes'))+"'")+' '+(str(request.POST.get('slot_longtitude_coords_seconds'))+'"')+' '+request.POST.get('slot_longtitude_compass')
                slot_latitude=(str(request.POST.get('slot_latitude_coords_degrees'))+u'\N{DEGREE SIGN}')+' '+(str(request.POST.get('slot_latitude_coords_minutes'))+"'")+' '+(str(request.POST.get('slot_latitude_coords_seconds'))+'"')+' '+request.POST.get('slot_latitude_compass')
                well.slot_longtitude=slot_longtitude
                well.slot_latitude=slot_latitude
            well.company=request.company
            well.longtitude=longtitude
            well.latitude=latitude
            well.block_id=request.POST.get('block')
            well.field_id=request.POST.get('field')
            well.created_by_id=request.user.id
            well.save()
            source_id=well.id
            adduserlog('Well Created',request,source_id,'Well',request.user.licence_type,well.project_id,well.id,None,'create')

            return redirect('wells:detail',pk=well.id)
        else:
            print(f"error {form.errors}")
    form = WellsForm()
    if(request.user.licence_type != 'Individual'):
        projects = Projects.objects.filter(company=request.company)
    else:
        projects = Projects.objects.getindividual_projects(request.user.id)

    coordinate_systems = CoordinateSystems.objects.all()
    projections = Projections.objects.all()
    wellengineer_group = Group.objects.get(id=3)
    view_group = Group.objects.get(id=4)
    blocks=ProjectBlock.objects.filter(project_id=project_id,status=1)
    return render(request,'well/create.html',{'form': form,'projects':projects,'coordinate_systems':coordinate_systems,'projections':projections,'project_id':project_id,'planwells':planwells,'blocks':blocks})


def getplanwells(request):
    plan_well_list_id = request.GET['plan_well_list_id']
    planwell=Wells.objects.filter(project_id=plan_well_list_id,well_type='PLAN')
    data = serializers.serialize('json', planwell)
    return JsonResponse(data, safe=False)


def edit(request, pk, template_name='well/edit.html'):
    planwells = Wells.objects.filter(well_type='PLAN',company=request.company)
    well = get_object_or_404(Wells, pk=pk)
    well_details=Wells.objects.get(id=pk)
    form = WellsForm(request.POST or None, instance = well)
    if form.is_valid():
        print("valid")
        longtitude=(str(request.POST.get('longtitude_coords_degrees'))+u'\N{DEGREE SIGN}')+' '+(str(request.POST.get('longtitude_coords_minutes'))+"'")+' '+(str(request.POST.get('longtitude_coords_seconds'))+'"')+' '+request.POST.get('longtitude_compass')
        latitude=(str(request.POST.get('latitude_coords_degrees'))+u'\N{DEGREE SIGN}')+' '+(str(request.POST.get('latitude_coords_minutes'))+"'")+' '+(str(request.POST.get('latitude_coords_seconds'))+'"')+' '+request.POST.get('latitude_compass')
        well=form.save()
        if(request.POST.get('slot_longtitude_coords_degrees') !=''):
            slot_longtitude=(str(request.POST.get('slot_longtitude_coords_degrees'))+u'\N{DEGREE SIGN}')+' '+(str(request.POST.get('slot_longtitude_coords_minutes'))+"'")+' '+(str(request.POST.get('slot_longtitude_coords_seconds'))+'"')+' '+request.POST.get('slot_longtitude_compass')
            slot_latitude=(str(request.POST.get('slot_latitude_coords_degrees'))+u'\N{DEGREE SIGN}')+' '+(str(request.POST.get('slot_latitude_coords_minutes'))+"'")+' '+(str(request.POST.get('slot_latitude_coords_seconds'))+'"')+' '+request.POST.get('slot_latitude_compass')
            well.slot_longtitude=slot_longtitude
            well.slot_latitude=slot_latitude
        well.company=request.company
        well.longtitude=longtitude
        well.latitude=latitude
        well.save()
        WellUsers.objects.filter(well=well,role_id=3).delete()
        WellUsers.objects.create(user_id=request.POST.get('well_engineer'),well=well,role_id=3)
        source_id=well.id 
       
        userlog=adduserlog('Well Edited',request,source_id,'Well',request.user.licence_type,well_details.project_id,pk,None,'edit')


        return redirect('wells:detail',pk=well.id)
    else:
        print(f" error_form_welledit  {form.errors}")
        print("check")

    projects = Projects.objects.filter(company=request.company)
    wellengineers =User.objects.filter(company=request.company)
    coordinate_systems = CoordinateSystems.objects.all()
    projections = Projections.objects.all()
    group = Group.objects.get(id=3)
    view_group = Group.objects.get(id=4)
    wellengineers = group.user_set.filter(company=request.company)
    viewers = view_group.user_set.filter(company=request.company).count()
    wellengineer= WellUsers.objects.filter(well=well,role=3)
    # wellengineer_id=wellengineer[0].user_id if wellengineer[0].user_id else None
    countries=getcountries(request.company)
    blocks=ProjectBlock.objects.filter(project_id=well_details.project_id,status=1)
    fields=ProjectField.objects.getfield_byblockid(well_details.block_id,well_details.project_id)

    return render(request, template_name, {'form':form,'projects':projects,'wellengineers':wellengineers,'coordinate_systems':coordinate_systems,'projections':projections,'planwells':planwells,'wellengineers_count':wellengineers.count,'viewers':viewers,'countries':countries,'company':request.company,'well':well_details,'blocks':blocks,'fields':fields})


def delete(request, pk, template_name='crudapp/confirm_delete.html'):
    well = get_object_or_404(Wells, pk=pk)
    source_id=well.id
    well_details=Wells.objects.get(id=pk)
    userlog=adduserlog('Well Deleted',request,source_id,'Well',request.user.licence_type,well_details.project_id,source_id,None,'delete')
 
    well.status = 0
    well.save()
    return redirect('wells:index')


def createwellusers(request,well_id):
    scheme=request.scheme
    gethost=request.get_host()
    well_details=Wells.objects.getwell_byid(well_id)
    sender = User.objects.getuserid(request.user.id)
    url=json.dumps({"url":scheme+'://'+gethost+'/wells/'+str(well_id)})
    if request.method == 'POST':
        users=request.POST.getlist('well_user')
        current_ids=[]
        for user in users:
            ckeck_user_exist_inwell=WellUsers.objects.getwellusers_byid_well(well_id,user)
            if(ckeck_user_exist_inwell):
                WellUsers.objects.updatestatus_id(ckeck_user_exist_inwell.id)
                current_ids.append(ckeck_user_exist_inwell.id)
            else:
                well_user=WellUsers.objects.createwelluser(well_id,user)
                current_ids.append(well_user.id)
            
            recipient = User.objects.getuserid(user)
            notify.send(sender, recipient=recipient,extra_data=url,verb='Well Assigned', description='You have been assigned to '+well_details.name,action_object=well_details)
        removing_users=WellUsers.objects.getremovingusers(current_ids,well_id)

        WellUsers.objects.updateremovingusers(removing_users,well_id)
        for removing_user in removing_users:
            recipient = User.objects.getuserid(removing_user.user_id)
            notify.send(sender, recipient=recipient,extra_data=url,verb='Well Assigned', description='You have been removed from '+well_details.name,action_object=well_details)
        adduserlog('WellUsers Created',request,well_id,'WellUsers',request.user.licence_type,well_details.project_id,well_id,None,'create')
        return redirect('wells:detail',pk=well_id)
    proj_id = Wells.objects.get(id=well_id).project_id
    project_users_queryset = ProjectUsers.objects.filter(project_id=proj_id,status=1)
    user_ids_list = [entry.user_id for entry in project_users_queryset]
    user_ids_list.append(request.user.id)
    if request.company:
        users = User.objects.filter(company_id = request.company.id,is_active=1).exclude(id__in = user_ids_list)
    else:
        users = User.objects.filter(individual_id = request.user.individual_id)
    
    current_selected_user = WellUsers.objects.filter(well_id=well_id,status=1).values_list('user_id', flat=True)
    return render(request,'well/createwelluser.html',{'users':users,'well_id':well_id,'current_selected_user':current_selected_user})

def getwelldetailsbyid(request):
    well_id=request.GET['well_id']
    well_details = Wells.objects.filter(id=well_id).values()
    well_users=WellUsers.objects.filter(well_id=well_id).values()
    return JsonResponse(list(zip(well_details,well_users)),safe=False)

def selectedunit(request):
    project_id=request.GET['project_id']
    selected_unit=Projects.objects.filter(id=project_id).values('unit')
    unit=selected_unit[0]['unit']
    return JsonResponse({"data":unit})