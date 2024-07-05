from django.shortcuts import render
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from wellphases.models import WellPhases,CasingTypes,Casing,Casingrange,Casinggrade
from wells.models import Wells,WellUsers,CoordinateSystems,Projections
from welltrajectory.models import WellTrajectory
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from wellphases.forms import CasingForm
from django.http import JsonResponse,HttpResponse
from tablib import Dataset
from django.db.models import Count
import pandas as pd
from django.db.models import Q
from custom_auth.getunit import getprojectunit,convertcasingvalue,convertpipe_weight
from math import tan, pi, acos,sin,cos,sqrt
from decimal import Decimal
import decimal
from io import BytesIO as IO
from custom_auth.getunit import adduserlog,getcountries
from django.db.models import F
from muddata.models import MudData
from helpers import *
import json
from muddata.models import HydraulicData
from django.contrib import messages
from custom_auth.models import User
from custom_auth.getunit import getprojidbywellid

# Create your views here.
def details(request,well_id):
    request.session['submenu']='wellphases'
    # request.session['wellmenu']='hydraulics'
    wellphases=WellPhases.objects.filter(company=request.company,well=well_id,status=1)
    well=Wells.objects.get(id=well_id)
    if(len(wellphases) == 0):
        checkpermission=user_rights_permission_projects('Create Data',request,'well',well_id)
        if(checkpermission != True):
            messages.error(request,'No Access to create!')
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('wellphases:create',well_id=well_id)
    countries=getcountries(request.company)
    checkpermission=user_rights_permission_projects('View Data',request,'well',well_id)

    if(checkpermission != True):
        messages.error(request,'No Access to view!')
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request,'wellphases/view.html',{'wellphases': wellphases,'well_id':well_id,'countries':countries,'company':request.company,'well':well,'project_id':well.project_id,'module_id':5,"user_id":request.user,'request':request})



def create(request,well_id):
    checkpermission=user_rights_permission_projects('Create Data',request,'well',well_id)
    if(checkpermission != True):
        messages.error(request,'No Access to create!')
        return redirect(request.META.get('HTTP_REFERER'))
    request.session['submenu']='wellphases'
    md_last_data = WellTrajectory.objects.get_lastmd(well_id)
  

    casing=Casing.objects.values('nominal_od','unit').annotate(Count('nominal_od')).order_by().filter(nominal_od__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company))
    unit=getprojectunit(well_id)
    casingunit='API' if casing.count()==0 else casing[0]['unit'] 
    casingdata=convertcasingvalue(casingunit,unit,casing)
    # Casing.objects.filter(Q(name__icontains=tag) | Q(tags__name__in=tags)).filter(isActive=True).order_by('-score').distinct()
    welltype=request.session['welltype']

    well_details=Wells.objects.filter(id=well_id).values()
    if(well_details[0]['well_type']=='ACTUAL'):
        planwell=well_details[0]['plan_well_list_id']
        wellphases = WellPhases.objects.filter(well_id=planwell).filter(status=1)
    else:
        wellphases = ''
    welltype=well_details[0]['well_type']
    if request.method == 'POST':
        phase_name=request.POST.getlist('phase_name')
        casing_type=request.POST.getlist('casing_type')
        hole_size=request.POST.getlist('hole_size')
        casing_size=request.POST.getlist('casing_size')
        nominal_od=request.POST.getlist('nominal_od')
        wellphase_grade=request.POST.getlist('wellphase_grade')
        wellphase_connection_type=request.POST.getlist('wellphase_connection_type')
        wellphase_range=request.POST.getlist('wellphase_range')
        weight=request.POST.getlist('weight')
        casing_size=request.POST.getlist('casing_size')
        measured_depth=request.POST.getlist('measured_depth')
        true_vertical_depth=request.POST.getlist('true_vertical_depth')
        lineartop=request.POST.getlist('lineartop')
        drift_id=request.POST.getlist('driftid')
        wellphase_startdate=request.POST.getlist('wellphase_startdate')
        # wellphase_starttime=request.POST.getlist('wellphase_starttime')

        i = 0
        wellphaseid_list = []
        while i < len(phase_name):
            if(phase_name[i]):     
                lineartop_data=lineartop[i] if(lineartop[i]!='') else None  
                nominal_od_data=nominal_od[i] if(nominal_od[i]!='') else None    
                weight_data=weight[i] if(weight[i]!='') else None 
                casing_size_data=casing_size[i] if(casing_size[i]!='') else None 
                wellphase_grade_data=wellphase_grade[i] if(wellphase_grade[i]!='') else None 
                wellphase_connection_type_data=wellphase_connection_type[i] if(wellphase_connection_type[i]!='') else None 
                wellphase_range_data=wellphase_range[i] if(wellphase_range[i]!='') else None
                drift_id_data=drift_id[i] if(drift_id[i]!='') else None
                
                if(welltype=='PLAN'):
                    Wellphase = WellPhases.objects.create(phase_name=phase_name[i],casing_type_id=casing_type[i],hole_size=hole_size[i],casing_size=casing_size_data,measured_depth=measured_depth[i],true_vertical_depth=true_vertical_depth[i],lineartop=lineartop_data,well_id=well_id,company=request.company,nominal_od=nominal_od_data,weight=weight_data,grade=wellphase_grade_data,connection_type=wellphase_connection_type_data,casing_range=wellphase_range_data,drift_id=drift_id_data)
                    wellphaseid_list.append(Wellphase.id)
                else:
                    print(f"wellphase_startdate {wellphase_startdate[i]}")
                    timestamp=dateconversion(wellphase_startdate[i])
                    Wellphase = WellPhases.objects.create(phase_name=phase_name[i],casing_type_id=casing_type[i],hole_size=hole_size[i],casing_size=casing_size_data,measured_depth=measured_depth[i],true_vertical_depth=true_vertical_depth[i],lineartop=lineartop_data,well_id=well_id,company=request.company,nominal_od=nominal_od_data,weight=weight_data,grade=wellphase_grade_data,connection_type=wellphase_connection_type_data,casing_range=wellphase_range_data,drift_id=drift_id_data,date=convertdateformat(wellphase_startdate[i]),timestamp=timestamp)
                    wellphaseid_list.append(Wellphase.id)
            i += 1  
        print('wellphase_list',wellphaseid_list) 
        source_id=wellphaseid_list
        proj_id = getprojidbywellid(well_id)
        adduserlog('Wellphases Created',request,source_id,'Wellphases',request.user.licence_type,proj_id,well_id,None,'create')
        return redirect('wellphases:detail', well_id=well_id)
    casingtypes=CasingTypes.objects.all()
    max=[]
    for i in range(4):
        max.append(i)
    well=Wells.objects.get(id=well_id)
    countries=getcountries(request.company)
    
    return render(request,'wellphases/create.html',{'well_id':well_id,'max':max,'casingtypes':casingtypes,'casing':casingdata,'welltype':welltype,'wellphases':wellphases,'countries':countries,'company':request.company,'well':well,'md_last_data':md_last_data.measured_depth if md_last_data else None})


def edit(request, pk, template_name='wellphases/edit.html',queryset=None):
    wellphases = WellPhases.objects.filter(well_id=pk).filter(status=1)
    casing=Casing.objects.values('nominal_od','unit').annotate(Count('nominal_od')).order_by().filter(nominal_od__count__gt=0)
    casinggrade=Casinggrade.objects.filter(company=request.company)
    request.session['submenu']='wellphases'
    casingrange=Casingrange.objects.filter(company=request.company)
    unit=getprojectunit(pk)
    casingunit=casing[0]['unit']
    casingdata=convertcasingvalue(casingunit,unit,casing)
    if request.method == 'POST':
        # WellPhases.objects.filter(well_id=pk).delete()
        phase_name=request.POST.getlist('phase_name')
        casing_type=request.POST.getlist('casing_type')
        hole_size=request.POST.getlist('hole_size')
        casing_size=request.POST.getlist('casing_size')
        measured_depth=request.POST.getlist('measured_depth')
        true_vertical_depth=request.POST.getlist('true_vertical_depth')
        lineartop=request.POST.getlist('lineartop')
        nominal_od=request.POST.getlist('nominal_od')
        wellphase_grade=request.POST.getlist('wellphase_grade')
        wellphase_connection_type=request.POST.getlist('wellphase_connection_type')
        wellphase_range=request.POST.getlist('wellphase_range')
        weight=request.POST.getlist('weight')
        wellphase_id=request.POST.getlist('wellphase_id')
        driftid=request.POST.getlist('driftid')

        i = 0
        currentid=[]
        while i < len(phase_name): 
            if(phase_name[i]):
                print('phase',phase_name[i])
                lineartop_data=lineartop[i] if(lineartop[i]!='') else None  
                nominal_od_data=nominal_od[i] if(nominal_od[i]!='') else None    
                weight_data=weight[i] if(weight[i]!='') else None 
                casing_size_data=casing_size[i] if(casing_size[i]!='') else None 
                wellphase_grade_data=wellphase_grade[i] if(wellphase_grade[i]!='') else None 
                wellphase_connection_type_data=wellphase_connection_type[i] if(wellphase_connection_type[i]!='') else None 
                wellphase_range_data=wellphase_range[i] if(wellphase_range[i]!='') else None
                drift_id_data=driftid[i] if(driftid[i]!='') else None


                if(wellphase_id[i]):
                    print('update')
                    currentid.append(int(wellphase_id[i]))
                    WellPhases.objects.filter(id=wellphase_id[i]).update(phase_name=phase_name[i],casing_type_id=casing_type[i],hole_size=hole_size[i],casing_size=casing_size_data,measured_depth=measured_depth[i],true_vertical_depth=true_vertical_depth[i],lineartop=lineartop_data,nominal_od=nominal_od_data,weight=weight_data,grade=wellphase_grade_data,connection_type=wellphase_connection_type_data,casing_range=wellphase_range_data,drift_id=drift_id_data)
                else:
                    print('create')
                    WellPhases.objects.create(phase_name=phase_name[i],casing_type_id=casing_type[i],hole_size=hole_size[i],casing_size=casing_size_data,measured_depth=measured_depth[i],true_vertical_depth=true_vertical_depth[i],lineartop=lineartop_data,well_id=pk,company=request.company,nominal_od=nominal_od_data,weight=weight_data,grade=wellphase_grade_data,connection_type=wellphase_connection_type_data,casing_range=wellphase_range_data,drift_id=drift_id_data)
                    wellphaseid=WellPhases.objects.values('id').last()
                    currentid.append(int(wellphaseid['id']))
            i += 1
         
        phaseid_del = WellPhases.objects.filter(company=request.company,well_id=pk,status=1).exclude(id__in=currentid)
        phase_id_list = [phase.id for phase in phaseid_del]
        WellPhases.objects.filter(company=request.company,well_id=pk,status=1).exclude(id__in=currentid).update(status=0)
        source_id=currentid
        proj_id = getprojidbywellid(pk)
        if (phaseid_del):
            adduserlog('Wellphases Deleted',request,phase_id_list,'Wellphases',request.user.licence_type,proj_id,pk,None,'delete')
        userlog=adduserlog('Wellphases Edited',request,source_id,'Wellphases',request.user.licence_type,proj_id,pk,None,'edit')
        return redirect('wellphases:detail', well_id=pk)
    casingtypes=CasingTypes.objects.all()
    well=Wells.objects.get(id=pk)
    countries=getcountries(request.company)
    return render(request, template_name, {'wellphases':wellphases,'well_id':pk,'casingtypes':casingtypes,'casing':casingdata,'casinggrade':casinggrade,'casingrange':casingrange,'countries':countries,'company':request.company,'well':well})


def delete(request, pk, template_name='crudapp/confirm_delete.html'):
    wellphases = WellPhases.objects.filter(well_id=pk,status=1)
    id_list = [phase.id for phase in wellphases]
    for wellphase_id in wellphases:
        muddata=MudData.objects.filter(well_id=pk,well_phase_id=wellphase_id).update(status=0)
    source_id=id_list
    proj_id = getprojidbywellid(pk)
    WellPhases.objects.filter(well_id=pk,status=1).update(status=0)
    userlog=adduserlog('Wellphases Deleted',request,source_id,'Wellphases',request.user.licence_type,proj_id,pk,None,'delete')
    
    
    return redirect('wellphases:detail', well_id=pk)

# Client Casing Master Create
def clientmastercasingindex(request):
    clientcasingvalue=Casing.objects.filter(company=request.company).filter(status=1)
    superadmincasingvalue=Casing.objects.filter(is_superadmin=1).filter(status=1)
    request.session['master']='casing'
    # if(len(clientcasingvalue) == 0):
    #     return redirect('wellphases:clientmastercasingcreate')

    
    user_rights_privilege_create = "Create Master"
    user_rights_privilege_edit = "Edit Master"
    user_rights_companyid = request.user.company_id
    user = User.objects.getuserid(request.user.id)
    user_rights_groups = user.groups.all().first()
     
    return render(request, 'master/clientcasingindex.html',
    {'clientcasingvalue':clientcasingvalue,
    'superadmincasingvalue':superadmincasingvalue,
    'user_rights_privilege_create':user_rights_privilege_create,
    'user_rights_privilege_edit':user_rights_privilege_edit,
    'user_rights_companyid':user_rights_companyid,
    'user_rights_groups':user_rights_groups
    })

def adminmastercasingindex(request):
    clientcasingvalue=Casing.objects.filter(is_superadmin=1).filter(status=1)
    request.session['master']='casing'
    if(len(clientcasingvalue) == 0):
        return redirect('wellphases:adminmastercasingcreate')
    return render(request, 'adminmaster/admincasingindex.html',{'clientcasingvalue':clientcasingvalue})

def adminmastercasingcreate(request):
    if request.method == 'POST':
        nominal_od=request.POST.getlist('nominal_od')
        weight=request.POST.getlist('weight')
        inside_diameter=request.POST.getlist('inside_diameter')
        # grade=request.POST.getlist('grade')
        connection_type=request.POST.getlist('connection_type')
        connection_od=request.POST.getlist('connection_od')
        # casing_range=request.POST.getlist('casing_range')
        drift_id=request.POST.getlist('drift_id')
        unit=request.POST.get('unit')
        i = 0 ; casing_id = []
        while i < len(nominal_od):
            if(nominal_od[i]):     
                casing = Casing.objects.create(nominal_od=nominal_od[i],weight=weight[i],inside_diameter=inside_diameter[i],connection_type=connection_type[i],connection_od=connection_od[i],drift_id=drift_id[i],unit=unit,is_superadmin=1)
                casing_id.append(casing.id)
            i += 1 
        userlog=adduserlog('Casing Created',request,casing_id,'admincasing',None,None,None)
        return redirect('wellphases:adminmastercasingindex')
    form = CasingForm()
    return render(request,'adminmaster/admincasingcreate.html',{'form': form})

def clientmastercasingcreate(request):
    if request.method == 'POST':
        nominal_od=request.POST.getlist('nominal_od')
        weight=request.POST.getlist('weight')
        inside_diameter=request.POST.getlist('inside_diameter')
        # grade=request.POST.getlist('grade')
        connection_type=request.POST.getlist('connection_type')
        connection_od=request.POST.getlist('connection_od')
        # casing_range=request.POST.getlist('casing_range')
        drift_id=request.POST.getlist('drift_id')
        unit=request.POST.get('unit')
        i = 0
        createcase = []
        while i < len(nominal_od):
            if(nominal_od[i]):     
                cast = Casing.objects.create(nominal_od=nominal_od[i],weight=weight[i],inside_diameter=inside_diameter[i],connection_type=connection_type[i],connection_od=connection_od[i],drift_id=drift_id[i],unit=unit,company=request.company)
                createcase.append(cast.id)

            i += 1
        createcase = ','.join(map(str, createcase))    
        adduserlog('createcasing created',request,createcase,'create casting master',request.user.licence_type,None,None)
        return redirect('wellphases:clientmastercasingindex')
    form = CasingForm()
    
    return render(request,'master/clientcasingcreate.html',{'form': form})


def clientmastercasingedit(request, template_name='master/clientcasingedits.html'):
    form = Casing.objects.filter(company=request.company).filter(status=1)
    grade_array=['K 55','L 80','N 80','C 90','T 95','P 110','Q 125','others']
    range_array=['25','34','45','others']
    casing_grade=Casing.objects.exclude(grade__in=grade_array).annotate(gradecount=Count('grade'))
    casing_range=Casing.objects.exclude(casing_range__in=range_array).annotate(rangecount=Count('casing_range'))
    for i in casing_grade:
        grade_array.append(i.grade)
    for j in casing_range:
        range_array.append(j.casing_range)
    unit=form[0].unit
    if request.method == 'POST': 
        nominal_od=request.POST.getlist('nominal_od')
        weight=request.POST.getlist('weight')
        inside_diameter=request.POST.getlist('inside_diameter')
        # grade=request.POST.getlist('grade')
        # casing_range=request.POST.getlist('casing_range')
        connection_type=request.POST.getlist('connection_type')
        connection_od=request.POST.getlist('connection_od')
        drift_id=request.POST.getlist('drift_id')
        unit=request.POST.get('unit')
        casing_id=request.POST.getlist('casing_id')

        i = 0
        currentid=[]
        while i < len(nominal_od):
            if(nominal_od[i]):
                if(casing_id[i]):
                    currentid.append(casing_id[i])
                    Casing.objects.filter(id=casing_id[i]).update(nominal_od=nominal_od[i],inside_diameter=inside_diameter[i],weight=weight[i],connection_type=connection_type[i],connection_od=connection_od[i],drift_id=drift_id[i],unit=unit)

                else:
                    Casing.objects.create(nominal_od=nominal_od[i],inside_diameter=inside_diameter[i],weight=weight[i],connection_type=connection_type[i],connection_od=connection_od[i],drift_id=drift_id[i],unit=unit,company=request.company)
                    casingid=Casing.objects.values('id').last()
                    currentid.append(casingid['id'])
            i += 1
        Casing.objects.exclude(id__in=currentid).filter(company=request.company).update(status=0)
        # i = 0
        # createcase = []
        # while i < len(nominal_od):
        #     if(nominal_od[i]):     
        #         cast = Casing.objects.create(nominal_od=nominal_od[i],weight=weight[i],inside_diameter=inside_diameter[i],connection_type=connection_type[i],connection_od=connection_od[i],drift_id=drift_id[i],unit=unit,company=request.company)
        #         createcase.append(cast.id)

        #     i += 1
        # createcase = ','.join(map(str, createcase)) 
        # print('editcase',createcase)   

        adduserlog('createcasing edited',request,currentid,'Edit casting master',request.user.licence_type,None,None)
        return redirect('wellphases:clientmastercasingindex')
    return render(request, template_name, {'form':form,'unit':unit,'grade_array':grade_array,'range_array':range_array})

def adminmastercasingedit(request, template_name='adminmaster/admincasingedit.html'):
    form = Casing.objects.filter(is_superadmin=1).filter(status=1)
    grade_array=['K 55','L 80','N 80','C 90','T 95','P 110','Q 125','others']
    range_array=['25','34','45','others']
    casing_grade=Casing.objects.exclude(grade__in=grade_array).annotate(gradecount=Count('grade'))
    casing_range=Casing.objects.exclude(casing_range__in=range_array).annotate(rangecount=Count('casing_range'))
    for i in casing_grade:
        grade_array.append(i.grade)
    for j in casing_range:
        range_array.append(j.casing_range)
    unit=form[0].unit
    if request.method == 'POST': 
        nominal_od=request.POST.getlist('nominal_od')
        weight=request.POST.getlist('weight')
        inside_diameter=request.POST.getlist('inside_diameter')
        # grade=request.POST.getlist('grade')
        # casing_range=request.POST.getlist('casing_range')
        connection_type=request.POST.getlist('connection_type')
        connection_od=request.POST.getlist('connection_od')
        drift_id=request.POST.getlist('drift_id')
        unit=request.POST.get('unit')
        casing_id=request.POST.getlist('casing_id')

        i = 0
        currentid=[]
        while i < len(nominal_od):
            if(nominal_od[i]):
                if(casing_id[i]):
                    currentid.append(casing_id[i])
                    Casing.objects.filter(id=casing_id[i]).update(nominal_od=nominal_od[i],inside_diameter=inside_diameter[i],weight=weight[i],connection_type=connection_type[i],drift_id=drift_id[i],connection_od=connection_od[i],unit=unit)

                else:
                    Casing.objects.create(nominal_od=nominal_od[i],inside_diameter=inside_diameter[i],weight=weight[i],connection_type=connection_type[i],connection_od=connection_od[i],drift_id=drift_id[i],unit=unit,company=request.company,is_superadmin=1)
                    casingid=Casing.objects.values('id').last()
                    currentid.append(casingid['id'])
            i += 1 
        userlog=adduserlog('Casing Edited',request,[],'admincasing',None,None,None)
        Casing.objects.exclude(id__in=currentid).filter(is_superadmin=1).update(status=0)
        return redirect('wellphases:adminmastercasingindex')
    return render(request, template_name, {'form':form,'unit':unit,'grade_array':grade_array,'range_array':range_array})

def clientmastercasingdelete(request, pk):
    casingvalue = get_object_or_404(Casing, pk=pk)
    casingvalue.delete()
    return redirect('wellphases:adminmastercasingindex')


def getmdtvd(request): 
    data_type=request.GET['type']
    data=request.GET['data']
    well_id=request.GET['well_id']
    if data_type=='md':
        welltrajectory=WellTrajectory.objects.filter(measured_depth=data,company=request.company,well_id=well_id)
        
        if(welltrajectory.count()>0):
            val=welltrajectory[0].true_vertical_depth
        else:
            belowmd=WellTrajectory.objects.filter(measured_depth__lte=data,company=request.company,well_id=well_id).order_by('-measured_depth')[:1].first()
            abovemd=WellTrajectory.objects.filter(measured_depth__gte=data,company=request.company,well_id=well_id).order_by('measured_depth')[:1].first()
            print(f"belowmd {belowmd.measured_depth}")
            print(f"abovemd {abovemd.measured_depth}")

            previous_md=WellTrajectory.objects.filter(id=belowmd.id)
            next_md=WellTrajectory.objects.filter(id=abovemd.id)
            pre_md=previous_md[0].measured_depth
            print(f'pre_md {pre_md}')
            n_md=next_md[0].measured_depth
            print(f'n_md {n_md}')
            pre_inc=previous_md[0].inclination
            n_inc=next_md[0].inclination
            pre_azi=previous_md[0].azimuth
            print(f'pre_azi {pre_azi}')
            n_azi=next_md[0].azimuth
            print(f'n_azi {n_azi}')
            pre_tvd=previous_md[0].true_vertical_depth

            dl_inc = acos(sin(n_inc*pi/180)*sin(pre_inc*pi/180)+(cos(pre_inc*pi/180)*cos(n_inc*pi/180)))*180/pi
            print(f"dl_inc {dl_inc}")

            dls_inc=round(dl_inc,2)*100/(n_md-pre_md) if dl_inc != 0 else 0
            print(f"dls_inc {dls_inc}")

            dl_azi=acos(cos((n_azi-pre_azi)*pi/180))*180/pi
            print(f"dl_azi {dl_azi}")


           
            dls_azi=round(dl_azi,2)*100/(n_md-pre_md) if dl_azi != 0 else 0
            print(f"dls_azi {dls_azi}")

            # target_rf=tan(dl_inc/2*pi/180)*180/pi*2/dl_inc
            target_inculination=dls_inc*(float(data)-pre_md)/100+pre_inc
            print(f"target_inculination {target_inculination}")


            target_azimuth=pre_azi-dls_azi*(float(data)-pre_md)/100
            print(f"target_azimuth {target_azimuth}")


            target_rf=tan(dl_inc/2*pi/180)*180/pi*2/dl_inc if dl_inc != 0 else 0
            print(f"target_rf {target_rf}")


            val=(cos(pre_inc*pi/180)+cos(round(target_inculination,2)*pi/180))*round(target_rf)*(float(data)-pre_md)/2+pre_tvd
            print(f"val {val}")

    else:
        welltrajectory=WellTrajectory.objects.filter(true_vertical_depth=data,company=request.company,well_id=well_id)
        if(welltrajectory.count()>0):
            val=welltrajectory[0].measured_depth
        else:
            belowmd=WellTrajectory.objects.filter(true_vertical_depth__lte=data,company=request.company).order_by('-true_vertical_depth')[:1].first()
            abovemd=WellTrajectory.objects.filter(true_vertical_depth__gte=data,company=request.company).order_by('true_vertical_depth')[:1].first()
            previous_md=WellTrajectory.objects.filter(id=belowmd.id)
            next_md=WellTrajectory.objects.filter(id=abovemd.id)
            pre_md=previous_md[0].measured_depth
            n_md=next_md[0].measured_depth
            pre_tvd=previous_md[0].true_vertical_depth
            n_tvd=next_md[0].true_vertical_depth
            pre_inc=previous_md[0].inclination
            n_inc=next_md[0].inclination
            pre_azi=previous_md[0].azimuth
            n_azi=next_md[0].azimuth
            
            dl_inc = acos(sin(n_inc*pi/180)*sin(pre_inc*pi/180)+(cos(pre_inc*pi/180)*cos(n_inc*pi/180)))*180/pi
            dls_inc=round(dl_inc,2)*100/(n_tvd-pre_tvd)
            dl_azi=acos(cos((n_azi-pre_azi)*pi/180))*180/pi
            dls_azi=round(dl_azi,2)*100/(n_tvd-pre_tvd)
            target_inculination=round(dls_inc,2)*(float(data)-pre_tvd)/100+pre_inc
            target_azimuth=pre_azi-dls_azi*(float(data)-pre_tvd)/100
            if(pre_inc==n_inc):
                target_rf=1
            else:
                target_rf=tan(round(dl_inc,2)/2*pi/180)*180/pi*2/round(dl_inc,2)
            val=(cos(pre_inc*pi/180)+cos(round(target_inculination,2)*pi/180))*round(target_rf)*(float(data)-pre_tvd)/2+pre_md
            # val=12.34
            # allmd=[]
            # allmd.append(belowmd.measured_depth)
            # allmd.append(None)
            # allmd.append(abovemd.measured_depth)
            # allmd_series = pd.Series(allmd)
            # md_interploate=allmd_series.interpolate(method='index')
            # val=md_interploate[1]  
    return JsonResponse(round(val,2), safe=False)

def importdata(request):
    if request.method == 'POST' and 'myfile' in request.FILES:
        dataset = Dataset()
        new_datas = request.FILES['myfile']
        unit=request.POST['unit']
        if not new_datas.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'master/importcasing.html')
        imported_data = dataset.load(new_datas.read(),format='xlsx')
        print(f"imported_data {imported_data}")
        for data in imported_data:
            if(request.company==None):
                obj = Casing.objects.create(nominal_od=data[0],weight=data[1],inside_diameter=data[2],
                connection_type=data[3],
                connection_od=data[4],drift_id=data[5],unit=unit,
                is_superadmin=1)
                obj.save()   
            else:
                obj = Casing.objects.create(nominal_od=data[0],weight=data[1],inside_diameter=data[2],
                connection_type=data[3],
                connection_od=data[4],drift_id=data[5],
                company=request.company,unit=unit)
                obj.save()  
        if(request.company==None):
            return redirect('wellphases:adminmastercasingindex')
        else:
            return redirect('wellphases:clientmastercasingindex')
    return render(request, 'master/importcasing.html')

def casing_download_csv_data(self):
    df_output = pd.DataFrame({
        'Nominal OD': [],
        'Weight': [],
        'Inside Diameter': [],
        'Connection Type': [],
        'Connection OD': [],
        'Drift ID': []
    })

    excel_file = IO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter' )   
    df_output.to_excel(xlwriter, 'sheetname',index=False)
    # xlwriter.save()
    xlwriter.close()
    excel_file.seek(0)

    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Hydraulics.xlsx'
    return response

def getcasingweight(request):
    nominal_od=request.GET['nominal_od']
    well_id=request.GET['well_id']
    # casing_weight=Casing.objects.values('weight').annotate(Count('weight')).filter(weight__count__gt=0).filter(nominal_od=nominal_od)
    casing_weight=Casing.objects.values('weight','unit').annotate(Count('weight')).filter(weight__count__gt=0).filter(nominal_od=nominal_od).filter(Q(is_superadmin=1) | Q(company=request.company))
    unit=getprojectunit(well_id)
    if(casing_weight.count()>0):
        casing_unit=casing_weight[0]['unit']
    else:
        casing_unit='API'
    pipeweight_data=convertpipe_weight(casing_unit,unit,casing_weight)
    return JsonResponse({"data": list(pipeweight_data)})

def insertrange(request):
    other_range=request.GET['range']
    Casingrangedata=Casingrange.objects.filter(range_name=other_range,company=request.company)
    if(len(Casingrangedata)==0):
        Casingrange.objects.create(range_name=other_range,company=request.company)
        casingrange=Casingrange.objects.values('id').last()
        status="true"
    else:
        status="false"
    return JsonResponse({"status": status})

def insertgrade(request):
    other_grade=request.POST['grade']
    Casinggradedata=Casinggrade.objects.filter(grade_name=other_grade,company=request.company)
    if(len(Casinggradedata)==0):
        Casinggrade.objects.create(grade_name=other_grade,company=request.company)
        casinggrade=Casinggrade.objects.values('id').last()
        status="true"
    else:
       status="false" 
    return JsonResponse({"status": status})

def getcasing_connection_type(request):
    casing_weight=request.GET['casing_weight']
    nominal_od=request.GET['nominal_od']
    # connection_type=Casing.objects.values('connection_type').annotate(Count('connection_type')).filter(connection_type__count__gt=0).filter(nominal_od=nominal_od).filter(weight=casing_weight)
    connection_type=Casing.objects.values('connection_type').annotate(Count('connection_type')).filter(connection_type__count__gt=0,nominal_od=nominal_od,weight=casing_weight).filter(Q(is_superadmin=1) | Q(company=request.company))
    return JsonResponse({"data": list(connection_type)})

def getplanwellpage_byactualwell(request):
    well_id=request.GET['well_id']
    well_details=Wells.objects.filter(id=well_id).values()
    planwell=well_details[0]['plan_well_list_id']
    wellphases = WellPhases.objects.filter(well_id=planwell).filter(status=1).values()
    return JsonResponse({"data": list(wellphases)})

def wellphase_casing(request):
    unit=request.POST.get('unit', False)
    nominal_od=request.POST.get('nominal_od', False)
    weight=request.POST.get('weight', False)
    inside_diameter=request.POST.get('inside_diameter', False)
    connection_type=request.POST.get('connection_type', False)
    connection_od=request.POST.get('connection_od', False)
    drift_id=request.POST.get('drift_id', False)
    Casing.objects.create(nominal_od=nominal_od,inside_diameter=inside_diameter,unit=unit,weight=weight,connection_type=connection_type,connection_od=connection_od,drift_id=drift_id,company=request.company,is_superadmin=0)
    nominal=Casing.objects.values('nominal_od').annotate(Count('nominal_od')).order_by().filter(nominal_od__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company))
    return JsonResponse({"data": list(nominal)})

def getcasing_driftID(request):
    od=request.GET['od']
    weight=request.GET['weight']
    well_id=request.GET['well_id']
    connection_type=request.GET['connection_type']
    drift_id=Casing.objects.values('inside_diameter','unit').annotate(Count('inside_diameter')).filter(inside_diameter__count__gt=0,nominal_od=od,weight=weight,connection_type=connection_type).filter(Q(is_superadmin=1) | Q(company=request.company)).annotate(nominal_od=F('inside_diameter'))
    unit=getprojectunit(well_id)
    casingunit='API' if drift_id.count()==0 else drift_id[0]['unit'] 
    drift_id_data=convertcasingvalue(casingunit,unit,drift_id)
    return JsonResponse({"data": list(drift_id_data)})

def checkwellphase(request):
    well_id=request.GET['well_id']
    request.session['submenu']='wellphases'
    wellphase=WellPhases.objects.filter(well_id=well_id).count()
    return JsonResponse({"count": wellphase})

def getmdtvd_actualwell(request):
    well_id=request.GET['well_id']
    selected_date=request.GET['selected_date']
    selected_time=request.GET['selected_time']
    previous_date=request.GET['previous_date']
    previous_time=request.GET['previous_time']
    timestamp=dateconversion(selected_date,selected_time)

    if(previous_date!=''):
        previous_timestamp=dateconversion(previous_date,previous_time)
        mdtvd=WellTrajectory.objects.filter(timestamp__gte=previous_timestamp,timestamp__lte=timestamp,well_id=well_id).order_by('-id')[:1].first()
    else:
        mdtvd=WellTrajectory.objects.filter(timestamp__lte=timestamp,well_id=well_id).order_by('-id')[:1].first()
    return JsonResponse({"md": mdtvd.measured_depth,'tvd':mdtvd.true_vertical_depth,'id':mdtvd.id})

def wellphasesummary(request,well_id):
    hydralics_data=HydraulicData.objects.filter(well_id=well_id,status=1)
    countries=getcountries(request.company)
    well=Wells.objects.get(id=well_id)
    summarypage=[]
    for data in hydralics_data:
        welltrajectory=WellTrajectory.objects.filter(measured_depth=data.measured_depth,well_id=well_id).first()
        if(welltrajectory==None):
            welltrajectory=WellTrajectory.objects.filter(measured_depth__gte=data.measured_depth,well_id=well_id).first()
        checktrajectory=[i for i,d in enumerate(summarypage) if welltrajectory.date in d]
        if(len(checktrajectory)==0):
            summarypage.append({
                welltrajectory.date:{
                    'flowrate':data.flowrate,
                    'pump_pressure':data.pump_pressure,
                    'ecd':data.ecd,
                    'bitdepth':data.measured_depth
                }
            })
    return render(request,'wellphases/wellphasesummary.html',{'summarypage': summarypage,'well_id':well_id,'countries':countries,'company':request.company,'well':well})
         







