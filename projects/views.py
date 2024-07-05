import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from matplotlib.font_manager import json_dump
from requests import request
from projects.models import Projects,ProjectUsers,ProjectBlock,ProjectField
from custom_auth.models import Companies, Countries,User
from notifications.signals import notify
from django.shortcuts import render, redirect, get_object_or_404
from .models import Projects
from .forms import ProjectsForm,ProjectUsersForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import Group
from notifications.models import Notification
from django.contrib import messages
from custom_auth.getunit import adduserlog
from django.forms import formset_factory
from django import forms
from django.core import serializers
from helpers import dateformat
from django.views import View
from helpers.allmodels import ProjectUsers,WellUsers
from helpers.commonimport import JsonResponse
from custom_auth.models import Userlog

# list project
class IndexView(ListView):
    template_name = 'project/list.html'
    context_object_name = 'projects'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mainmenu'] = self.request.session['mainmenu']
        return context
    
    def get(self, request, *args, **kwargs):
        mainmenu = request.session.get('mainmenu')
        request.session['mainmenu'] = 'projects'
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self,**kwargs):
        return Projects.objects.filter(company=self.request.company).prefetch_related('projectusers_set')

# view project byid
class ProjectDetailView(DetailView):
    model = Projects
    template_name = 'project/view.html'
    context_object_name = 'project'
    def get_context_data(self, **kwargs):
       

        user_rights_privilege = "Create Well"
        user_rights_companyid = self.request.user.company_id
        user = User.objects.getuserid(self.request.user.id)
        user_rights_groups = user.groups.all().first()
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['createwell']=self.request.session.pop('trigger_popup',None)
        context['usercount']=User.objects.getcompanyusers(self.request.user.company_id).count()
        context['projectusers'] = ProjectUsers.objects.filterprojstatus_getuserid(self.get_object().id,1)
        print(f"context['projectusers'] {context['projectusers']}")

        context['projectblock'] = ProjectBlock.objects.filter(project=self.get_object(),status=1)
        context['project_details']=self.get_object()
        context['user_email']=str(self.request.user)
        context['user_rights_privilege']=user_rights_privilege
        context['user_rights_companyid']=user_rights_companyid
        context['user_rights_groups']=user_rights_groups
        context['request']=self.request
        return context

# create project
def create(request):
    
    if request.method == 'POST':
        print('inside_create_post')
        project=Projects.objects.createproject(request.POST.get('project_name'),request.POST.get('unit'),request.POST.get('country'),request.company,request.user.id)
        # projectusers=ProjectUsers.objects.createprojectuser(project.id,request.POST.get('user'))
        blocks=request.POST.getlist('block')
        i=0
        for block in blocks:
            createblock=ProjectBlock.objects.createprojectblock(block,project.id)
            fields=request.POST.getlist("field"+str(i))
            for field in fields:
                ProjectField.objects.createprojectfield(field,project.id,createblock.id)
            i +=1
        source_id=project.id
        adduserlog('Project Created',request,source_id,'Project',request.user.licence_type,project.id,None,None)
        return redirect('projects:detail',pk=project.id)
    
    countries = Countries.objects.all()
    user_count=User.objects.filter(company=request.company).count()
    group = Group.objects.get(id=2)
    wellmanagers = group.user_set.filter(company=request.company)

    view_group = Group.objects.get(id=4)
    viewers = view_group.user_set.filter(company=request.company).count()

    wellengineer_group = Group.objects.get(id=3)
    wellengineers = wellengineer_group.user_set.filter(company=request.company).count()
    wellmanagers_count=wellmanagers.count()

    # print(wellmanagers.count())
    # if(wellmanagers.count()==0):
    #     messages.error(request, "Please create a well manager before create a project")
    #     return redirect('custom_auth:users')
                
    return render(request,'project/create.html',{'countries':countries,'wellmanagers':wellmanagers,'user_count':user_count,'viewers':viewers,'wellengineers':wellengineers,'wellmanagers_count':wellmanagers_count})


def edit(request, pk, template_name='project/edit.html'):
    project = get_object_or_404(Projects, pk=pk)
    form = ProjectsForm(request.POST or None, instance=project)
    block_ids = ProjectBlock.objects.filter(project_id=project.id).values_list('id', flat=True)
    if form.is_valid():
        project=form.save()
        if request.company:
            project.company=request.company 
        else:
            project.created_by_id = request.user.id
        project.save()
        blocks=request.POST.getlist('block')
        block_id=request.POST.getlist('block_id')
        print(f"post {request.POST}")
        current_blockid=[]
        current_fieldid=[]
        i=0
        for block in blocks:
            if (block_id[i] !=''):
                ProjectBlock.objects.filter(id=block_id[i]).update(block_name=block)
                createblock=block_id[i]
                current_blockid.append(block_id[i])
                field_id=request.POST.getlist('field_id'+block_id[i])
                fields=request.POST.getlist("field"+block_id[i])
                j=0
                for field in fields:
                    if (field_id[j] !=''):
                        current_fieldid.append(field_id[j])
                        ProjectField.objects.filter(id=field_id[j]).update(field_name=field)
                    else:
                        ProjectField.objects.create(field_name=field,project_id=project.id,status=1,block_id=block_id[i])
                        field_ids=ProjectField.objects.values('id').last()
                        current_fieldid.append(field_ids['id'])
                    j+=1
            else:
                createblock=ProjectBlock.objects.create(block_name=block,project_id=project.id,status=1)
                currentblock=ProjectBlock.objects.values('id').last()
                current_blockid.append(currentblock['id'])
                fields=request.POST.getlist("field"+str(i))
                for field in fields:
                    ProjectField.objects.create(field_name=field,project_id=project.id,status=1,block_id=createblock.id)
                    field_ids=ProjectField.objects.values('id').last()
                    current_fieldid.append(field_ids['id'])
            i +=1
        ProjectField.objects.filter(project_id=project.id).exclude(id__in=current_fieldid).update(status=0)
        ProjectBlock.objects.filter(project_id=project.id).exclude(id__in=current_blockid).update(status=0)
        source_id=project.id
        adduserlog('Project Edited',request,source_id,'Project',request.user.licence_type,project.id,None,None,'edit')
        return redirect('projects:detail',pk=project.id)
    countries = Countries.objects.all()
    projectblock = ProjectBlock.objects.filter(project=project,status=1)
    return render(request, template_name, {'form':form,'project':project,'countries':countries,'projectblock':projectblock})

def delete(request, pk):
    project = get_object_or_404(Projects, pk=pk)
    source_id=project.id 
    proj_name = Projects.objects.get(id=source_id).project_name
    Projects.objects.update_project_status(project.id)
    adduserlog(proj_name+' Project Deleted',request,pk,'Project',request.user.licence_type,pk,None,None,'delete')

    return redirect('projects:create')


def createprojectusers(request,project_id):
    scheme=request.scheme
    gethost=request.get_host()
    arr1=[]
    arr2=[]
    project=Projects.objects.getproject_byid(project_id)
    url=json.dumps({"url":scheme+'://'+gethost+'/projects/'+str(project_id)})
    sender = User.objects.getuserid(request.user.id)

    if request.method == 'POST':
        users=request.POST.getlist('user')
        current_ids=[]
        for user in users:
            try:
                ckeck_user_exist_inproject=ProjectUsers.objects.getprojectusers_byid_project(project_id,user)
            except:
                ckeck_user_exist_inproject = None
            if(ckeck_user_exist_inproject):
                ProjectUsers.objects.updatestatus_id(ckeck_user_exist_inproject.id)
                current_ids.append(ckeck_user_exist_inproject.id)
            else:
                project_user=ProjectUsers.objects.createprojectuser(project_id,user)
                current_ids.append(project_user.id)
            
            recipient = User.objects.getuserid(user)
            notify.send(sender, recipient=recipient,extra_data=url,verb='Project Assigned', description='You have been assigned to '+project.project_name,action_object=project)
        print(f"current_ids {current_ids}")
        removing_users=ProjectUsers.objects.getremovingusers(current_ids,project_id)
        print(f"removing_users {removing_users}")

        removing_users_list=[]
        for removing_user in removing_users:
            removing_users_list.append(removing_user.id)

        ProjectUsers.objects.updateremovingusers(removing_users_list,project_id)
        adduserlog('ProjectUsers Created',request,project_id,'ProjectUsers',request.user.licence_type,project_id,None,None,'create')
        for removing_user in removing_users:
            recipient = User.objects.getuserid(removing_user.user_id)
            notify.send(sender, recipient=recipient,extra_data=url,verb='Project Assigned', description='You have been removed from '+project.project_name,action_object=project)
        
    form = ProjectUsersForm()
    if request.company:
        users = User.objects.getallcompanyusers_exclude_currentuser(request.company.id,request.user.id)
    else:
        users = User.objects.filter(individual_id = request.user.individual_id,is_active=1)
    current_selected_user = ProjectUsers.objects.filterprojstatus_getuserid(project_id,1)
    current_selected_users=[]
    for user_id,name,lastname in current_selected_user:
        current_selected_users.append(user_id)
    print(f"current_selected_user {current_selected_user}")
    return render(request,'project/createprojectuser.html',{'form': form,'users':users,'project_id':project_id,'current_selected_user':current_selected_users})

def permission(request,project_id):
    users =User.objects.filter(company=request.company)
    if request.method == 'POST':
        print("ggg")
    return render(request,'project/createpermission.html',{'users':users,'project_id':project_id})

def Notifications(request):
    return render(request, 'notifications.html')

def notifications_datatable(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    user = User.objects.get(pk=request.user.id)
    filtered_notifications = user.notifications.all()[start:start+length] 
    total_notifications = user.notifications.all().count()
    data = []
    for notify in filtered_notifications:
        data_dict = json.loads(notify.data['extra_data'])
        data.append({
            'data1': notify.verb +'<br>' +notify.description,
            'data2': dateformat(notify.timestamp),
            'url':data_dict['url'],
            'id':notify.id
            
        })
    response = {
        'draw': draw,
        'recordsTotal': total_notifications,
        'recordsFiltered': total_notifications,
        'data': data,

    }

    return JsonResponse(response)


def gettrajectory(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    filtered_trajectory = WellTrajectory.objects.gettrajectory(request.company,start,length)
    total_records = WellTrajectory.objects.getalltrajectory(request.company).count()


    print(f"filtered_trajectory {filtered_trajectory}")

    data = []
    for trajectory in filtered_trajectory:
        data.append({
            'md': trajectory.measured_depth,
            'lnclination': trajectory.inclination,
            'azimuth':trajectory.azimuth,
            'tvd':trajectory.true_vertical_depth,
            'dls':trajectory.dls,
            'vertical_section':trajectory.vertical_section,
        })
    
    print(f"data {data}")

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)

def markallread(request):
    notifications=Notification.objects.filter(recipient=request.user)
    for notification in notifications:
        Notification.objects.get(pk=notification.id).mark_as_read()
    return redirect ("/notifications/")

def check_user_hasproject(request):
    print(f"post {request.POST}")
    user_id=request.POST.get('user_id')
    print(f"user_id {user_id}")
    projectusers=ProjectUsers.objects.getproject_userid(user_id)
    print(f"projectusers {projectusers}")
    print(f"projectusers.count() {projectusers.count()}")
    wellusers=WellUsers.objects.getwell_userid(user_id)

    if(projectusers.count()>0 or wellusers.count()>0):
        status=True
    else:
        status=False
    return JsonResponse({'status':status})
#migrate user
class Migrateuser(View):
    def get(self, request,user_id):
        projects=ProjectUsers.objects.getuserprojects(user_id)
        wells=WellUsers.objects.getuserwells(user_id)
        return render(request,'project/migrateuser.html',{'projects':projects,'user_id':user_id,'request':request,'wells':wells})

    def post(self, request,user_id):
        project_id=request.POST.getlist('project_id')
        project_user=request.POST.getlist('project_user')
        well_id=request.POST.getlist('well_id')
        well_user=request.POST.getlist('well_user')
        i=0
        while i<len(project_id):
            projectnewuser_id=project_user[i]
            ProjectUsers.objects.updateprojectusers(project_id[i],user_id,projectnewuser_id)
            i +=1
        j=0
        while j<len(well_id):
            wellnewuser_id=well_user[j]
            WellUsers.objects.updatewellusers(well_id[j],user_id,wellnewuser_id)
            j +=1

        user=User.objects.updateuser(user_id)
        return redirect('custom_auth:users')  