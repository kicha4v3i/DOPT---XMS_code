from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from bhadata.forms import BhaDataForm,BhaElementForm,DrillcollersForm,DrillpipeForm,DrillpipeHWDPForm,SpecificationsForm
from helpers.allmodels import Wells, WellUsers, CoordinateSystems, Projections, MudData, Rheogram, RheogramNameModels, RheogramDate, DrillBit, DrillBitNozzle, BitTypesNames, BhaData, BhaElement, Drillcollers, Drillpipe, DrillpipeHWDP, Specifications, Pressuredroptool, Empirical, Differential_pressure
import openpyxl
import csv
import pandas as pd
from io import BytesIO as IO
from django.http import JsonResponse,HttpResponse
from tablib import Dataset
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from wellphases.models import WellPhases
from django.db.models import Count
from bhadata.mixed_fractions import Mixed
from django.forms.models import model_to_dict
from django.db.models import Q
from custom_auth.getunit import getprojectunit,convertcollarvalue,convertpipevalue,convertpipe_weight,converttosi,converthwdpvalue
from django.db.models import F
from custom_auth.getunit import adduserlog,getcountries
from helpers import * 
from django.contrib import messages
from custom_auth.models import User

def create(request,wellphase_id):
    well_id=request.session['well_id']
    request.session['mainmenu']='hydraulics'
    collar=Drillcollers.objects.values('normal_od','unit').annotate(Count('normal_od')).order_by().filter(normal_od__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company))
    pipe=Drillpipe.objects.values('normal_od','unit').annotate(Count('normal_od')).order_by().filter(normal_od__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company))
    hwdp=DrillpipeHWDP.objects.values('nominal_od','unit').annotate(Count('nominal_od')).order_by().filter(nominal_od__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company))
    unit=getprojectunit(well_id)
    drillunit=collar[0]['unit']
    if(pipe.count()>0):
        pipeunit=pipe[0]['unit']
    else:
       pipeunit='API' 
    if(hwdp.count()>0):
        hwdpunit=hwdp[0]['unit']
    else:
        hwdpunit='API' 
    collardata=convertcollarvalue(drillunit,unit,collar)
    pipedata=convertpipevalue(pipeunit,unit,pipe)
    hwdpdata=converthwdpvalue(hwdpunit,unit,hwdp)
    well = Wells.objects.get(id=well_id)
    welltype = well.well_type
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    loop_times = range(1, 5)

    currentwellphase=WellPhases.objects.filter(id=wellphase_id).values('measured_depth','id','well_id').first()
    previouswellphase=WellPhases.objects.filter(id__lt=currentwellphase['id']).filter(well_id=currentwellphase['well_id']).order_by("-id").values('measured_depth','id')[:1]
    fromdepth=0 if previouswellphase.count()==0 else previouswellphase[0]['measured_depth']
    todepth= currentwellphase['measured_depth']

    well_details=Wells.objects.filter(id=well_id).values()
    if(well_details[0]['well_type']=='ACTUAL'):
        planwell=well_details[0]['plan_well_list_id']
        bha_data = BhaData.objects.filter(well_id=planwell).values()
        if(bha_data.count() > 0):
            bhaelement_data = BhaElement.objects.filter(bhadata=bha_data[0]['id']).filter(status=1).values()
        else:
            bhaelement_data = ''
    else:
        bha_data = ''
        bhaelement_data = ''

    welltype=well_details[0]['well_type']
    
    if request.method == 'POST':
        
        if(request.session['welltype']=='ACTUAL'):
            # date=request.POST.getlist('date')
            # time=request.POST.getlist('time')
            depth=request.POST.getlist('depth')
            bhaname=request.POST.getlist('bhaname')
            print(request.POST)
            i = 0 
            
            while i < len(bhaname):
                if(bhaname[i]):
                    # timestamp=dateconversion(date[i],time[i])
                    BhaData.objects.create(company=request.company,well_id=well_id,well_phases_id=wellphase_id,bhaname=bhaname[i],depth=depth[i])
                    
                    type_name=request.POST.getlist('type_name'+str(i))
                    element=request.POST.getlist('element'+str(i))
                    od=request.POST.getlist('od'+str(i))
                    weight=request.POST.getlist('weight'+str(i))
                    pipe_type=request.POST.getlist('pipe_type'+str(i))
                    connection_type=request.POST.getlist('connection_type'+str(i))
                    tool_od=request.POST.getlist('tool_od'+str(i))
                    tool_id=request.POST.getlist('tool_id'+str(i))
                    class_type=request.POST.getlist('classtype'+str(i))
                    grade=request.POST.getlist('grade'+str(i))
                    onejoint_length=request.POST.getlist('onejoint_length'+str(i))
                    box_tj_length=request.POST.getlist('box_tj_length'+str(i))
                    pin_tj_length=request.POST.getlist('pin_tj_length'+str(i))
                    identity=request.POST.getlist('identity'+str(i))
                    length=request.POST.getlist('length'+str(i))
                    length_onejoint=request.POST.getlist('length_onejoint'+str(i)) 
                    j=0 ; bhadata_id = []
                    while j < len(type_name):
                        if(type_name[j]):
                            weight_data=weight[j] if(weight[j]!='') else None 
                            pipe_type_data=pipe_type[j] if(pipe_type[j]!='') else None 
                            connection_type_data=connection_type[j] if(connection_type[j]!='') else None 
                            tool_od_data=tool_od[j] if(tool_od[j]!='') else None 
                            tool_id_data=tool_id[j] if(tool_id[j]!='') else None 
                            classtype_data=class_type[j] if(class_type[j]!='') else None
                            grade_data=grade[j] if(grade[j]!='') else None
                            onejoint_length_data=onejoint_length[j] if(onejoint_length[j]!='') else None
                            box_tj_length_data=box_tj_length[j] if(box_tj_length[j]!='') else None
                            pin_tj_length_data=pin_tj_length[j] if(pin_tj_length[j]!='') else None
                            bhaelement=BhaElement.objects.create(element=element[j],od=od[j],weight=weight_data,pipe_type=pipe_type_data,connection_type=connection_type_data,tool_od=tool_od_data,tool_id=tool_id_data,identity=identity[j],length=length[j],type_name=type_name[j],length_onejoint=length_onejoint[j],bhadata=bhadata,
                            class_element=classtype_data,grade=grade_data,onejoint_length=onejoint_length_data,pin_tj_length=pin_tj_length_data,box_tj_length=box_tj_length_data)
                            bhadata_id.append(bhaelement.id)
                            if((type_name[j]=='RSS') or (type_name[j]=='Mud Motor') or (type_name[j]=='MWD') or (type_name[j]=='LWD') or (type_name[j]=='Others')):
                                name=request.POST.get('name'+str(i)+'_'+str(j))
                                specification_od=request.POST.get('specification_od'+str(i)+'_'+str(j))
                                specification_id=request.POST.get('specification_id'+str(i)+'_'+str(j))

                                specification_length=request.POST.get('specification_length'+str(i)+'_'+str(j))
                                minimum_flowrate=request.POST.get('minimum_flowrate'+str(i)+'_'+str(j))
                                maximum_flowrate=request.POST.get('maximum_flowrate'+str(i)+'_'+str(j))
                                flowrate=request.POST.getlist('flowrate'+str(i)+'_'+str(j))
                                formulatext=request.POST.get('formulatext'+str(i)+'_'+str(j))
                                formulatext_python=request.POST.get('formula_python_text'+str(i)+'_'+str(j))
                                pressure_drop=request.POST.getlist('pressure_drop'+str(i)+'_'+str(j))
                                minimum_rpm = request.POST.get('minimum_rpm'+str(i)+'_'+str(j))
                                maximum_rpm = request.POST.get('maximum_rpm'+str(i)+'_'+str(j))
                                no_load_diff_pressure = request.POST.get('no_load_diff_pressure'+str(i)+'_'+str(j))
                                max_dp = request.POST.get('max_dp'+str(i)+'_'+str(j))
                                recom_dp = request.POST.get('recom_dp'+str(i)+'_'+str(j))
                                max_wob = request.POST.get('max_wob'+str(i)+'_'+str(j))
                                torque = request.POST.getlist('torque'+str(i)+'_'+str(j))
                                diff_pressure = request.POST.getlist('diff_pressure'+str(i)+'_'+str(j))
                                print('specifications',name,specification_od,specification_id,specification_length,minimum_flowrate,maximum_flowrate,minimum_rpm,maximum_rpm,no_load_diff_pressure,max_dp,recom_dp,max_wob,bhadata,bhaelement)
                                Specifications.objects.create(name=name,specification_od=specification_od,specification_id=specification_id,specification_length=specification_length,minimum_flowrate=minimum_flowrate,maximum_flowrate=maximum_flowrate,minimum_rpm=minimum_rpm,maximum_rpm=maximum_rpm,no_load_diff_pressure=no_load_diff_pressure,max_dp=max_dp,recom_dp=recom_dp,max_wob=max_wob,bhadata=bhadata,bhadata_element=bhaelement)
                                calculationtype=0
                                if((type_name[j]=='RSS') or (type_name[j]=='MWD') or (type_name[j]=='LWD') or (type_name[j]=='Others')):
                                    k=0
                                    while k<len(flowrate):
                                        if(flowrate[k]):
                                            calculationtype=1
                                            Pressuredroptool.objects.create(flowrate=flowrate[k],pressure_drop=pressure_drop[k],bhadata=bhadata,bhadata_element=bhaelement)
                                        k +=1
                                    if(formulatext!='' and formulatext_python!=''):
                                        Empirical.objects.create(bhadata=bhadata,bhadata_element=bhaelement,formula=formulatext,formula_python_text=formulatext_python)
                                        calculationtype=2 
                            
                                    BhaElement.objects.filter(id=bhaelement.pk).update(calculation_type=calculationtype)
                                else:
                                    k=0
                                    while k<len(torque):
                                        if(torque[k]):
                                            Differential_pressure.objects.create(torque=torque[k],diff_pressure=diff_pressure[k],bhadata=bhadata,bhadata_element=bhaelement)
                                        k +=1    
                                
                        j +=1
                i += 1
            print('bhaelement_currentid')
            source_id=bhadata_id
            adduserlog('BHA data Created',request,source_id,'BHA data',request.user.licence_type,well.project_id,well_id,wellphase_id,'create')
            return redirect('bhadata:bhadatalist', wellphase_id=wellphase_id)

        else:
            print(f"request.POST {request.POST}")
            form = BhaDataForm(request.POST)

            if form.is_valid():
                bhadata=form.save()
                bhadata.company=request.company
                bhadata.well_phases_id=wellphase_id
                bhadata.save()
                element=request.POST.getlist('element')
                od=request.POST.getlist('od')
                weight=request.POST.getlist('weight')
                pipe_type=request.POST.getlist('pipe_type')
                connection_type=request.POST.getlist('connection_type')
                tool_od=request.POST.getlist('tool_od')
                tool_id=request.POST.getlist('tool_id')
                identity=request.POST.getlist('identity')
                length=request.POST.getlist('length')
                length_onejoint=request.POST.getlist('length_onejoint')
                type_name=request.POST.getlist('type_name')
                class_type=request.POST.getlist('classtype')
                grade=request.POST.getlist('grade')
                onejoint_length=request.POST.getlist('onejoint_length')
                box_tj_length=request.POST.getlist('box_tj_length')
                pin_tj_length=request.POST.getlist('pin_tj_length')
                
                i = 0
                bhadata_id = []
                
                while i < len(element):
                    if(element[i]):
                        weight_data=weight[i] if(weight[i]!='') else None 
                        pipe_type_data=pipe_type[i] if(pipe_type[i]!='') else None 
                        connection_type_data=connection_type[i] if(connection_type[i]!='') else None 
                        tool_od_data=tool_od[i] if(tool_od[i]!='') else None 
                        tool_id_data=tool_id[i] if(tool_id[i]!='') else None 
                        classtype_data=class_type[i] if(class_type[i]!='') else None
                        grade_data=grade[i] if(grade[i]!='') else None
                        onejoint_length_data=onejoint_length[i] if(onejoint_length[i]!='') else None
                        box_tj_length_data=box_tj_length[i] if(box_tj_length[i]!='') else None
                        pin_tj_length_data=pin_tj_length[i] if(pin_tj_length[i]!='') else None
                        bhaelement=BhaElement.objects.create(element=element[i],od=od[i],weight=weight_data,pipe_type=pipe_type_data,connection_type=connection_type_data,tool_od=tool_od_data,tool_id=tool_id_data,identity=identity[i],length=length[i],type_name=type_name[i],length_onejoint=length_onejoint[i],bhadata=bhadata,
                        class_element=classtype_data,grade=grade_data,onejoint_length=onejoint_length_data,pin_tj_length=pin_tj_length_data,box_tj_length=box_tj_length_data)
                        bhadata_id.append(bhaelement.id)

                        if((type_name[i]=='RSS') or (type_name[i]=='Mud Motor') or (type_name[i]=='MWD') or (type_name[i]=='LWD') or (type_name[i]=='Others')):
                            name=request.POST.get('name'+str(i))
                            specification_od=request.POST.get('specification_od'+str(i))
                            specification_id=request.POST.get('specification_id'+str(i))

                            specification_length=request.POST.get('specification_length'+str(i))
                            minimum_flowrate=request.POST.get('minimum_flowrate'+str(i))
                            maximum_flowrate=request.POST.get('maximum_flowrate'+str(i))
                            flowrate=request.POST.getlist('flowrate'+str(i))
                            formulatext=request.POST.get('formulatext'+str(i))
                            formulatext_python=request.POST.get('formula_python_text'+str(i))
                            # print(f"formulatext {formulatext}")
                            # print(f"formulatext_python {formulatext_python}")
                            # print(f"flowrate {flowrate}")

                            pressure_drop=request.POST.getlist('pressure_drop'+str(i))
                            minimum_rpm = request.POST.get('minimum_rpm'+str(i))
                            maximum_rpm = request.POST.get('maximum_rpm'+str(i))
                            no_load_diff_pressure = request.POST.get('no_load_diff_pressure'+str(i))
                            max_dp = request.POST.get('max_dp'+str(i))
                            recom_dp = request.POST.get('recom_dp'+str(i))
                            max_wob = request.POST.get('max_wob'+str(i))
                            torque = request.POST.getlist('torque'+str(i))
                            diff_pressure = request.POST.getlist('diff_pressure'+str(i))
                            Specifications.objects.create(name=name,specification_od=specification_od,specification_id=specification_id,specification_length=specification_length,minimum_flowrate=minimum_flowrate,maximum_flowrate=maximum_flowrate,minimum_rpm=minimum_rpm,maximum_rpm=maximum_rpm,no_load_diff_pressure=no_load_diff_pressure,max_dp=max_dp,recom_dp=recom_dp,max_wob=max_wob,bhadata=bhadata,bhadata_element=bhaelement)
                            calculationtype=0
                            j=0
                            while j<len(flowrate):
                                if(flowrate[j]):
                                    calculationtype=1
                                    Pressuredroptool.objects.create(flowrate=flowrate[j],pressure_drop=pressure_drop[j],bhadata=bhadata,bhadata_element=bhaelement)
                                j +=1
                            k=0
                            while k<len(torque):
                                if(torque[k]):
                                    Differential_pressure.objects.create(torque=torque[k],diff_pressure=diff_pressure[k],bhadata=bhadata,bhadata_element=bhaelement)
                                k +=1
                            
                            if(formulatext and formulatext_python):
                                Empirical.objects.create(bhadata=bhadata,bhadata_element=bhaelement,formula=formulatext,formula_python_text=formulatext_python)
                                calculationtype=2 
                        
                            BhaElement.objects.filter(id=bhaelement.pk).update(calculation_type=calculationtype)

                            
                    i += 1
                print('bhaelement_currentid')
                source_id=bhadata_id
                adduserlog('BHA data Created',request,source_id,'BHA data',request.user.licence_type,well.project_id,well_id,wellphase_id,'create')
                
                return redirect('bhadata:bhadatalist', wellphase_id=wellphase_id)
            else: 
                print(form.errors)
        

    
    form = BhaDataForm()
    bhaelement=BhaElement.objects.all()
    drillcollars=Drillcollers.objects.values('normal_od').annotate(Count('id')).order_by().filter(id__count__gt=0).filter(is_superadmin=1)
    collar_weight=Drillcollers.objects.values('weight').annotate(Count('id')).order_by().filter(id__count__gt=0).filter(is_superadmin=1)
    pipe_type=Drillcollers.objects.values('pipe_type').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1)
    connection_type=Drillcollers.objects.values('connection_type').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1)
    tool_od=Drillcollers.objects.values('tool_od').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1)
    # drillpipes=Drillpipe.objects.filter(is_superadmin=1).
    drillpipes=Drillpipe.objects.values('normal_od').annotate(Count('id')).order_by().filter(id__count__gt=0).filter(is_superadmin=1)
    drillpipeshwdp=DrillpipeHWDP.objects.values('nominal_od').annotate(Count('id')).order_by().filter(id__count__gt=0).filter(is_superadmin=1)
    drillhwdptool=DrillpipeHWDP.objects.values('tool_od').annotate(Count('id')).order_by().filter(id__count__gt=0).filter(is_superadmin=1)
    row=[]
    for i in range(4):
        row.append(i)
    
    if(request.session['welltype']=='PLAN'):
        return render(request,'bhadata/create.html',{'form': form,'bhaelement':bhaelement,'well_id':well_id,'welltype':welltype,'row':row,
        'drillcollars':collardata,'collar_weight':collar_weight,'pipe_type':pipe_type,'connection_type':connection_type,'tool_od':tool_od,'well':well,
        'drillpipes':pipedata,'drillpipeshwdp':hwdpdata,'drillhwdptool':drillhwdptool,'wellphases':wellphase,'welltype':welltype,'bha_data':bha_data,'bhaelement_data':bhaelement_data,'wellphase_id':int(wellphase_id),'loop_times':loop_times,'fromdepth':fromdepth,'countries':getcountries(request.company),'company':request.company,'todepth':todepth})
    else:
        return render(request,'bhadata/create_actual.html',{'form': form,'bhaelement':bhaelement,'well_id':well_id,'welltype':welltype,'row':row,
        'drillcollars':collardata,'collar_weight':collar_weight,'pipe_type':pipe_type,'connection_type':connection_type,'tool_od':tool_od,'well':well,
        'drillpipes':pipedata,'drillpipeshwdp':hwdpdata,'drillhwdptool':drillhwdptool,'wellphases':wellphase,'welltype':welltype,'bha_data':bha_data,'bhaelement_data':bhaelement_data,'wellphase_id':int(wellphase_id),'loop_times':loop_times,'fromdepth':fromdepth,'countries':getcountries(request.company),'company':request.company,'todepth':todepth})



def details(request,pk):
    bhadata=BhaData.objects.get(pk=pk)
    wellphase_id=request.GET['wellphase']
    request.session['submenu']='bhadata'
    request.session['wellphasetab']=int(wellphase_id)
    bhaelement=BhaElement.objects.filter(bhadata=bhadata,status=1).order_by('length_onejoint')
    well_id=bhadata.well_id
    well = Wells.objects.get(id=well_id)
    welltype = well.well_type
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    return render(request,'bhadata/view.html',{'bhadata': bhadata,'bhaelement':bhaelement,'welltype':welltype,'wellphases':wellphase,'wellphase_id':int(wellphase_id),'well_id':well_id,'countries':getcountries(request.company),'company':request.company,'well':well,'project_id':well.project_id,'user_id':request.user,'module_id':4})


def bhadatalist(request,wellphase_id):
    well_id=request.session['well_id']
    well_type=request.session['welltype']

    data = BhaData.objects.filter(company=request.company,well_id=well_id,well_phases_id=wellphase_id,status=1)

    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    request.session['submenu']='bhadata'
    request.session['wellphasetab']=wellphase_id
    well = Wells.objects.get(id=well_id)
    welltype = well.well_type
    if(len(data) == 0):
        checkpermission=user_rights_permission('Create Data',request)
        if(checkpermission == True):
            return redirect('bhadata:create',wellphase_id=wellphase_id)
        else:
            messages.error(request,'No Access to create!')
            return redirect(request.META.get('HTTP_REFERER'))
    
    checkpermission=user_rights_permission('View Data',request)
    if(checkpermission != True):
        messages.error(request,'No Access to view!')
        return redirect(request.META.get('HTTP_REFERER'))
       
    if(well_type=='PLAN'):
        return render(request,'bhadata/list.html',{'data': data,'well_id':well_id,'welltype':welltype,'wellphases':wellphase,'wellphase_id':wellphase_id,'countries':getcountries(request.company),'company':request.company,'well':well,'project_id':well.project_id,'user_id':request.user,'module_id':5})
    else:
        return render(request,'bhadata/actuallist.html',{'data': data,'well_id':well_id,'welltype':welltype,'wellphases':wellphase,'wellphase_id':wellphase_id,'countries':getcountries(request.company),'company':request.company,'well':well}) 
    
def editbha_actual(request):
    well_id=request.session['well_id']
    wellphase_id=request.GET['wellphase']

    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    well = Wells.objects.get(id=well_id)
    collar=Drillcollers.objects.values('normal_od','unit').annotate(Count('normal_od')).order_by().filter(normal_od__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company))
    unit=getprojectunit(well_id)
    drillunit=collar[0]['unit']
    collardata=convertcollarvalue(drillunit,unit,collar)

    pipe=Drillpipe.objects.values('normal_od','unit').annotate(Count('normal_od')).order_by().filter(normal_od__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company))
    pipeunit='API' if(pipe.count()==0) else pipe[0]['unit']
    pipedata=convertpipevalue(pipeunit,unit,pipe)

    hwdp=DrillpipeHWDP.objects.values('nominal_od','unit').annotate(Count('nominal_od')).order_by().filter(nominal_od__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company))
    hwdpunit='API' if(hwdp.count()==0) else hwdp[0]['unit']
    hwdpdata=converthwdpvalue(hwdpunit,unit,hwdp)


    if request.method == 'POST':
        depth=request.POST.getlist('depth')
        bhaname=request.POST.getlist('bhaname')
        bha_id=request.POST.getlist('bha_id')
        current_bha_id=[]
        i = 0
        while i < len(depth):
            if(depth[i]):
                if(bha_id[i]):
                    bhadata=BhaData.objects.filter(id=bha_id[i]).update(depth=depth[i],bhaname=bhaname[i])
                    bhaid=bha_id[i]
                    current_bha_id.append(bha_id[i])
                else:
                    bhadata=BhaData.objects.create(depth=depth[i],company=request.company,well_id=well_id,well_phases_id=wellphase_id,bhaname=bhaname[i])
                    bhaid=BhaData.objects.values('id').last()
                    current_bha_id.append(bhaid['id'])
                    bhaid=bhaid['id']
                type_name=request.POST.getlist('type_name'+str(i))
                element=request.POST.getlist('element'+str(i))
                od=request.POST.getlist('od'+str(i))
                weight=request.POST.getlist('weight'+str(i))
                pipe_type=request.POST.getlist('pipe_type'+str(i))
                connection_type=request.POST.getlist('connection_type'+str(i))
                tool_od=request.POST.getlist('tool_od'+str(i))
                tool_id=request.POST.getlist('tool_id'+str(i))
                class_type=request.POST.getlist('classtype'+str(i))
                grade=request.POST.getlist('grade'+str(i))
                onejoint_length=request.POST.getlist('onejoint_length'+str(i))
                box_tj_length=request.POST.getlist('box_tj_length'+str(i))
                pin_tj_length=request.POST.getlist('pin_tj_length'+str(i))
                identity=request.POST.getlist('identity'+str(i))
                length=request.POST.getlist('length'+str(i))
                length_onejoint=request.POST.getlist('length_onejoint'+str(i))
                bhaelement_id=request.POST.getlist('bhaelement_id'+str(i))
                j=0
                current_bhaelement_id=[]
                while j < len(type_name):
                    if(type_name[j]):
                        weight_data=weight[j] if(weight[j]!='') else None 
                        pipe_type_data=pipe_type[j] if(pipe_type[j]!='') else None 
                        connection_type_data=connection_type[j] if(connection_type[j]!='') else None 
                        tool_od_data=tool_od[j] if(tool_od[j]!='') else None 
                        tool_id_data=tool_id[j] if(tool_id[j]!='') else None 
                        classtype_data=class_type[j] if(class_type[j]!='') else None
                        grade_data=grade[j] if(grade[j]!='') else None
                        onejoint_length_data=onejoint_length[j] if(onejoint_length[j]!='') else None
                        box_tj_length_data=box_tj_length[j] if(box_tj_length[j]!='') else None
                        pin_tj_length_data=pin_tj_length[j] if(pin_tj_length[j]!='') else None
                        
                        if(bhaelement_id[j]):
                            bhaelement=BhaElement.objects.filter(id=bhaelement_id[j]).update(element=element[j],od=od[j],weight=weight_data,pipe_type=pipe_type_data,connection_type=connection_type_data,tool_od=tool_od_data,tool_id=tool_id_data,identity=identity[j],length=length[j],type_name=type_name[j],length_onejoint=length_onejoint[j],bhadata_id=bhaid,
                            class_element=classtype_data,grade=grade_data,onejoint_length=onejoint_length_data,pin_tj_length=pin_tj_length_data,box_tj_length=box_tj_length_data)
                            bhaelementid=bhaelement_id[j]
                            current_bhaelement_id.append(bhaelement_id[j])
                        else:
                            bhaelement=BhaElement.objects.create(element=element[j],od=od[j],weight=weight_data,pipe_type=pipe_type_data,connection_type=connection_type_data,tool_od=tool_od_data,tool_id=tool_id_data,identity=identity[j],length=length[j],type_name=type_name[j],length_onejoint=length_onejoint[j],bhadata_id=bhaid,
                            class_element=classtype_data,grade=grade_data,onejoint_length=onejoint_length_data,pin_tj_length=pin_tj_length_data,box_tj_length=box_tj_length_data)
                            bhaelementid=BhaElement.objects.values('id').last()
                            current_bhaelement_id.append(bhaelementid['id'])
                            bhaelementid=bhaelementid['id']
                        
                        if((type_name[j]=='RSS') or (type_name[j]=='MWD') or (type_name[j]=='LWD') or (type_name[j]=='Others')):
                            name=request.POST.get('name'+str(i)+'_'+str(j))
                            specification_od=request.POST.get('specification_od'+str(i)+'_'+str(j))
                            specification_id=request.POST.get('specification_id'+str(i)+'_'+str(j))
                            specification_length=request.POST.get('specification_length'+str(i)+'_'+str(j))
                            minimum_flowrate=request.POST.get('minimum_flowrate'+str(i)+'_'+str(j))
                            maximum_flowrate=request.POST.get('maximum_flowrate'+str(i)+'_'+str(j))
                            flowrate=request.POST.getlist('flowrate'+str(i)+'_'+str(j))
                            formulatext=request.POST.get('formulatext'+str(i)+'_'+str(j))
                            formulatext_python=request.POST.get('formula_python_text'+str(i)+'_'+str(j))
                            pressure_drop=request.POST.getlist('pressure_drop'+str(i)+'_'+str(j))
                            pressure_drop_id=request.POST.getlist('pressuredrop_tool'+str(i)+'_'+str(j))
                            minimum_rpm = request.POST.get('minimum_rpm'+str(i)+'_'+str(j))
                            maximum_rpm = request.POST.get('maximum_rpm'+str(i)+'_'+str(j))
                            no_load_diff_pressure = request.POST.get('no_load_diff_pressure'+str(i)+'_'+str(j))
                            max_dp = request.POST.get('max_dp'+str(i)+'_'+str(j))
                            recom_dp = request.POST.get('recom_dp'+str(i)+'_'+str(j))
                            max_wob = request.POST.get('max_wob'+str(i)+'_'+str(j))
                            torque = request.POST.getlist('torque'+str(i)+'_'+str(j))
                            diff_pressure = request.POST.getlist('diff_pressure'+str(i)+'_'+str(j))

                            if(bhaelement_id[j]):
                                Specifications.objects.filter(bhadata_element_id=bhaelementid).update(name=name,specification_od=specification_od,specification_id=specification_id,specification_length=specification_length,minimum_flowrate=minimum_flowrate,maximum_flowrate=maximum_flowrate,minimum_rpm=minimum_rpm,maximum_rpm=maximum_rpm,no_load_diff_pressure=no_load_diff_pressure,max_dp=max_dp,recom_dp=recom_dp,max_wob=max_wob)
                            else:
                                Specifications.objects.create(name=name,specification_od=specification_od,specification_id=specification_id,specification_length=specification_length,minimum_flowrate=minimum_flowrate,maximum_flowrate=maximum_flowrate,minimum_rpm=minimum_rpm,maximum_rpm=maximum_rpm,no_load_diff_pressure=no_load_diff_pressure,max_dp=max_dp,recom_dp=recom_dp,max_wob=max_wob,bhadata=bhadata,bhadata_element=bhaelement)
                            
                            
                            if(bhaelement_id[j]):
                                checkempirical=Empirical.objects.filter(bhadata_element_id=bhaelement_id[j]).first()
                                if(checkempirical != None):
                                    Empirical.objects.filter(bhadata_element_id=bhaelement_id[j]).update(formula=formulatext,formula_python_text=formulatext_python)
                                else:
                                    Empirical.objects.create(bhadata=bhadata,bhadata_element_id=bhaelement_id[j],formula=formulatext,formula_python_text=formulatext_python) 

                                l=0
                                while l<len(flowrate):
                                    if(flowrate[l]):
                                        if(pressure_drop_id[l]):
                                            Pressuredroptool.objects.filter(id=pressure_drop_id[l]).update(flowrate=flowrate[l],pressure_drop=pressure_drop[l])
                                        else:
                                            Pressuredroptool.objects.create(flowrate=flowrate[l],pressure_drop=pressure_drop[l],bhadata_id=bhaid,bhadata_element_id=bhaelementid)
                                    l += 1

                            else:
                                if(formulatext!='' and formulatext_python!=''):
                                    Empirical.objects.create(bhadata=bhadata,bhadata_element_id=bhaelementid,formula=formulatext,formula_python_text=formulatext_python) 
                                    calculation_type=2
                                
                                if(len(flowrate)>0 and len(pressure_drop)>0):
                                    k=0
                                    while k<len(flowrate):
                                        if(flowrate[k]):
                                            pressuredrop=Pressuredroptool.objects.create(flowrate=flowrate[k],pressure_drop=pressure_drop[k],bhadata=bhadata,bhadata_element_id=bhaelementid)
                                        k +=1
                                    calculation_type=1
                                BhaElement.objects.filter(id=bhaelementid).update(calculation_type=calculation_type)
                        
                        if(type_name[j]=='Mud Motor'):
                            name=request.POST.get('name'+str(i)+'_'+str(j))
                            minimum_flowrate=request.POST.get('minimum_flowrate'+str(i)+'_'+str(j))
                            maximum_flowrate=request.POST.get('maximum_flowrate'+str(i)+'_'+str(j))
                            minimum_rpm = request.POST.get('minimum_rpm'+str(i)+'_'+str(j))
                            maximum_rpm = request.POST.get('maximum_rpm'+str(i)+'_'+str(j))
                            no_load_diff_pressure = request.POST.get('no_load_diff_pressure'+str(i)+'_'+str(j))
                            max_dp = request.POST.get('max_dp'+str(i)+'_'+str(j))
                            recom_dp = request.POST.get('recom_dp'+str(i)+'_'+str(j))
                            max_wob = request.POST.get('max_wob'+str(i)+'_'+str(j))
                            torque = request.POST.getlist('torque'+str(i)+'_'+str(j))
                            diff_pressure = request.POST.getlist('diff_pressure'+str(i)+'_'+str(j))
                            diff_pressure_id = request.POST.getlist('differntial_pressure'+str(i)+'_'+str(j))
                            pressure_diff=list(filter(None, diff_pressure_id))
                            if(bhaelement_id[j]):
                                Specifications.objects.filter(bhadata_element_id=bhaelement_id[j]).update(name=name,minimum_flowrate=minimum_flowrate,maximum_flowrate=maximum_flowrate,
                                minimum_rpm=minimum_rpm,maximum_rpm=maximum_rpm,max_dp=max_dp,recom_dp=recom_dp,max_wob=max_wob,no_load_diff_pressure=no_load_diff_pressure,bhadata=bhadata)
                            else:
                                Specifications.objects.create(name=name,minimum_flowrate=minimum_flowrate,maximum_flowrate=maximum_flowrate,
                                minimum_rpm=minimum_rpm,maximum_rpm=maximum_rpm,max_dp=max_dp,recom_dp=recom_dp,max_wob=max_wob,no_load_diff_pressure=no_load_diff_pressure,bhadata=bhadata,bhadata_element_id=bhaelementid)

                            m=0
                            while m<len(torque):
                                if(torque[m]):
                                    if(diff_pressure_id[m]):
                                        Differential_pressure.objects.filter(id=diff_pressure_id[m]).update(torque=torque[m],diff_pressure=diff_pressure[m])
                                    else:
                                        Differential_pressure.objects.create(torque=torque[m],diff_pressure=diff_pressure[m],bhadata_id=bhaid,bhadata_element_id=bhaelementid)
                                m += 1
                    j += 1
                BhaElement.objects.filter(bhadata_id=bhaid).exclude(id__in=current_bhaelement_id).update(status=0)
            i += 1
        BhaData.objects.filter(well_phases_id=wellphase_id).exclude(id__in=current_bha_id).update(status=0)
        return redirect('bhadata:bhadatalist', wellphase_id=wellphase_id)

    data = BhaData.objects.filter(company=request.company,well_id=well_id,well_phases_id=wellphase_id,status=1)
    return render(request,'bhadata/edit_actual_bha.html',{'data': data,'well_id':well_id,'wellphases':wellphase,'wellphase_id':wellphase_id,'countries':getcountries(request.company),'company':request.company,'well':well,'drillcollars':collardata,'drillpipes':pipedata,'drillpipeshwdp':hwdpdata}) 


def edit(request, pk, template_name='bhadata/edit.html'):
    bhadata = get_object_or_404(BhaData, pk=pk)
    wellphase_id=request.GET['wellphase']
    form = BhaDataForm(request.POST or None, instance=bhadata)
    bhaelement = BhaElement.objects.filter(bhadata=pk).filter(status=1).order_by('length_onejoint')
    well_id=bhadata.well_id
    request.session['mainmenu']='hydraulics'
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    drillcollars=Drillcollers.objects.values('normal_od','unit').annotate(Count('normal_od')).order_by().filter(normal_od__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company))
    drillpipes=Drillpipe.objects.values('normal_od','unit').annotate(Count('normal_od')).filter(normal_od__count__gt=0).order_by().filter(Q(is_superadmin=1) | Q(company=request.company))
    drillpipeshwdp=DrillpipeHWDP.objects.values('nominal_od','unit').annotate(Count('nominal_od')).order_by().filter(nominal_od__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company))
    well = Wells.objects.get(id=well_id)
    currentwellphase=WellPhases.objects.filter(id=wellphase_id).values('measured_depth','id','well_id').first()
    previouswellphase=WellPhases.objects.filter(id__lt=currentwellphase['id']).filter(well_id=currentwellphase['well_id']).order_by("-id").values('measured_depth','id')[:1]
    fromdepth=0 if previouswellphase.count()==0 else previouswellphase[0]['measured_depth']
    todepth= currentwellphase['measured_depth']
    welltype = well.well_type
    if request.method == 'POST':
        print(f"post request {request.POST}")
        if form.is_valid():
            bhadata=form.save()
            bhadata.company=request.company
            bhadata.well_phases_id=wellphase_id
            bhadata.save()
            # BhaElement.objects.filter(bhadata=pk).delete()
            element=request.POST.getlist('element')
            od=request.POST.getlist('od_edit')
            weight=request.POST.getlist('weight')
            pipe_type=request.POST.getlist('pipe_type')
            connection_type=request.POST.getlist('connection_type')
            tool_od=request.POST.getlist('tool_od')
            tool_id=request.POST.getlist('tool_id')
            identity=request.POST.getlist('identity_edit')
            length=request.POST.getlist('length')
            length_onejoint=request.POST.getlist('length_onejoint')
            type_name=request.POST.getlist('type_name_edit')
            class_type=request.POST.getlist('classtype')
            grade=request.POST.getlist('grade')
            bhaelement_id=request.POST.getlist('bhaelement_id')
            onejoint_length=request.POST.getlist('onejoint_length')
            calculation_type=request.POST.getlist('calculation_type')
            box_tj_length=request.POST.getlist('box_tj_length')
            pin_tj_length=request.POST.getlist('pin_tj_length')

            i = 0
            currentid=[]
            allpressuredropid=[]
            alldiff_pressure_id=[]
            
            while i < len(element):
                if(element[i]):
                    weight_data=weight[i] if(weight[i]!='') else None 
                    pipe_type_data=pipe_type[i] if(pipe_type[i]!='') else None 
                    connection_type_data=connection_type[i] if(connection_type[i]!='') else None 
                    tool_od_data=tool_od[i] if(tool_od[i]!='') else None 
                    tool_id_data=tool_id[i] if(tool_id[i]!='') else None 
                    classtype_data=class_type[i] if(class_type[i]!='') else None
                    grade_data=grade[i] if(grade[i]!='') else None
                    onejoint_length_data=onejoint_length[i] if(onejoint_length[i]!='') else None
                    box_tj_length_data=box_tj_length[i] if(box_tj_length[i]!='') else None
                    pin_tj_length_data=pin_tj_length[i] if(pin_tj_length[i]!='') else None

                    if(bhaelement_id[i]):
                        currentid.append(bhaelement_id[i])
                        bhaelementid=bhaelement_id[i]
                        bhaelement=BhaElement.objects.filter(id=bhaelement_id[i]).update(element=element[i],od=od[i],weight=weight_data,pipe_type=pipe_type_data,connection_type=connection_type_data,tool_od=tool_od_data,tool_id=tool_id_data,identity=identity[i],length=length[i],length_onejoint=length_onejoint[i],type_name=type_name[i],class_element=classtype_data,grade=grade_data,onejoint_length=onejoint_length_data,box_tj_length=box_tj_length_data,pin_tj_length=pin_tj_length_data)
                      
                    else:
                        bhaelement=BhaElement.objects.create(element=element[i],od=od[i],weight=weight_data,pipe_type=pipe_type_data,connection_type=connection_type_data,tool_od=tool_od_data,tool_id=tool_id_data,identity=identity[i],length=length[i],length_onejoint=length_onejoint[i],type_name=type_name[i],bhadata=bhadata,class_element=classtype_data,grade=grade_data,onejoint_length=onejoint_length_data,box_tj_length=box_tj_length_data,pin_tj_length=pin_tj_length_data)
                        currentid.append(bhaelement.id)
                        bhaelementid=bhaelement.id
                    print(f"calculation_type {calculation_type[i]}")
                    if((type_name[i]=='RSS') or (type_name[i]=='MWD') or (type_name[i]=='LWD') or (type_name[i]=='Others')):
                        name=request.POST.get('name'+str(i))
                        specification_od=request.POST.get('specification_od'+str(i))
                        specification_id=request.POST.get('specification_id'+str(i))
                        specification_length=request.POST.get('specification_length'+str(i))
                        minimum_flowrate=request.POST.get('minimum_flowrate'+str(i))
                        maximum_flowrate=request.POST.get('maximum_flowrate'+str(i))
                        flowrate=request.POST.getlist('flowrate'+str(i))
                        formulatext=request.POST.get('formulatext'+str(i))
                        formulatext_python=request.POST.get('formula_python_text'+str(i))
                        pressure_drop=request.POST.getlist('pressure_drop'+str(i))
                        pressuredrop_id=request.POST.getlist('pressuredrop_tool'+str(i))
                        drop=list(filter(None, pressuredrop_id))

                        if(bhaelement_id[i]):
                            if(specification_od != None):
                                Specifications.objects.filter(bhadata_element_id=bhaelement_id[i]).update(name=name,specification_od=specification_od,specification_id=specification_id,specification_length=specification_length,minimum_flowrate=minimum_flowrate,maximum_flowrate=maximum_flowrate,bhadata=bhadata)
                        else:
                            Specifications.objects.create(name=name,specification_od=specification_od,specification_id=specification_id,specification_length=specification_length,minimum_flowrate=minimum_flowrate,maximum_flowrate=maximum_flowrate,bhadata=bhadata,bhadata_element_id=bhaelementid['id'])
                    
                        if(calculation_type[i]=='2' and formulatext):
                            if(Empirical.objects.filter(bhadata_element_id=bhaelementid)):
                                Empirical.objects.filter(bhadata_element_id=bhaelementid).update(bhadata=bhadata,formula=formulatext,formula_python_text=formulatext_python)
                            else:
                                empirical=Empirical.objects.create(bhadata=bhadata,bhadata_element_id=bhaelementid,formula=formulatext,formula_python_text=formulatext_python)    
                            BhaElement.objects.filter(id=bhaelementid).update(calculation_type=calculation_type[i])

                        if(calculation_type[i]=='1'):
                            j=0
                            while j<len(flowrate):
                                if(flowrate[j] and pressure_drop[j]):
                                    if(pressuredrop_id[j]):
                                        allpressuredropid.append(pressuredrop_id[j])
                                        Pressuredroptool.objects.filter(id=pressuredrop_id[j]).update(flowrate=flowrate[j],pressure_drop=pressure_drop[j])
                                    else:
                                        pressuredrop=Pressuredroptool.objects.create(flowrate=flowrate[j],pressure_drop=pressure_drop[j],bhadata=bhadata,bhadata_element_id=bhaelementid)
                                        allpressuredropid.append(pressuredrop.pk)
                                j +=1
                            BhaElement.objects.filter(id=bhaelementid).update(calculation_type=calculation_type[i])
                            Pressuredroptool.objects.filter(bhadata_element_id=bhaelementid).exclude(id__in=allpressuredropid).update(status=0)

                          
                    if(type_name[i]=='Mud Motor'):
                        name=request.POST.get('name'+str(i))
                        minimum_flowrate=request.POST.get('minimum_flowrate'+str(i))
                        maximum_flowrate=request.POST.get('maximum_flowrate'+str(i))
                        minimum_rpm = request.POST.get('minimum_rpm'+str(i))
                        maximum_rpm = request.POST.get('maximum_rpm'+str(i))
                        no_load_diff_pressure = request.POST.get('no_load_diff_pressure'+str(i))
                        max_dp = request.POST.get('max_dp'+str(i))
                        recom_dp = request.POST.get('recom_dp'+str(i))
                        max_wob = request.POST.get('max_wob'+str(i))
                        torque = request.POST.getlist('torque'+str(i))
                        diff_pressure = request.POST.getlist('diff_pressure'+str(i))
                        diff_pressure_id = request.POST.getlist('differntial_pressure'+str(i))
                        pressure_diff=list(filter(None, diff_pressure_id))
                        if(bhaelement_id[i]):
                            if(minimum_flowrate != None):
                                Specifications.objects.filter(bhadata_element_id=bhaelement_id[i]).update(name=name,minimum_flowrate=minimum_flowrate,maximum_flowrate=maximum_flowrate,
                                minimum_rpm=minimum_rpm,maximum_rpm=maximum_rpm,max_dp=max_dp,recom_dp=recom_dp,max_wob=max_wob,no_load_diff_pressure=no_load_diff_pressure,bhadata=bhadata)
                        else:
                            Specifications.objects.create(name=name,minimum_flowrate=minimum_flowrate,maximum_flowrate=maximum_flowrate,
                                minimum_rpm=minimum_rpm,maximum_rpm=maximum_rpm,max_dp=max_dp,recom_dp=recom_dp,max_wob=max_wob,no_load_diff_pressure=no_load_diff_pressure,bhadata=bhadata,bhadata_element_id=bhaelementid['id'])
                        k=0
                        while k < len(torque):
                            if(torque[k] and diff_pressure[k]):
                                if(diff_pressure_id[k]):
                                    Differential_pressure.objects.filter(id=diff_pressure_id[k]).update(torque=torque[k],diff_pressure=diff_pressure[k])
                                    alldiff_pressure_id.append(diff_pressure_id[k])
                                else:
                                    diff_pressure=Differential_pressure.objects.create(torque=torque[k],diff_pressure=diff_pressure[k],bhadata=bhadata,bhadata_element_id=bhaelementid)
                                    alldiff_pressure_id.append(diff_pressure.id)
                            k +=1

                        if alldiff_pressure_id != []:
                            Differential_pressure.objects.filter(bhadata_element_id=bhaelementid).exclude(id__in=alldiff_pressure_id).update(status=0)
                i += 1
            
            source_id=currentid
            userlog=adduserlog('BHA data Edited',request,source_id,'BHA data',request.user.licence_type,well.project_id,well_id,wellphase_id,'edit')
            BhaElement.objects.filter(bhadata_id=bhadata.id).exclude(id__in=currentid).update(status=0)
            return redirect('bhadata:bhadatalist', wellphase_id=wellphase_id)
    collar=Drillcollers.objects.values('normal_od','unit').annotate(Count('normal_od')).order_by().filter(normal_od__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company))
    pipe=Drillpipe.objects.values('normal_od','unit').annotate(Count('normal_od')).order_by().filter(normal_od__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company))
    hwdp=DrillpipeHWDP.objects.values('nominal_od','unit').annotate(Count('nominal_od')).order_by().filter(nominal_od__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company))
    unit=getprojectunit(well_id)
    drillunit='API' if(collar.count()==0) else collar[0]['unit']
    pipeunit='API' if(pipe.count()==0) else pipe[0]['unit']
    hwdpunit='API' if(hwdp.count()==0) else hwdp[0]['unit']
    collardata=convertcollarvalue(drillunit,unit,collar)
    pipedata=convertpipevalue(pipeunit,unit,pipe)
    hwdpdata=converthwdpvalue(hwdpunit,unit,hwdp)
    
    
    return render(request, template_name, {'form':form,'bhaelement':bhaelement,'well_id':well_id,'welltype':welltype,'wellphases':wellphase,'drillcollars':collardata,'drillpipes':pipedata,'drillpipeshwdp':hwdpdata,'wellphase_id':int(wellphase_id),'fromdepth':fromdepth,'todepth':todepth,'countries':getcountries(request.company),'company':request.company,'well':well})


def delete(request, id, template_name='crudapp/confirm_delete.html'):
    bhadata = get_object_or_404(BhaData, id=id)
    print('bhadata',bhadata)
    well_id=bhadata.well_id
    well = Wells.objects.get(id=well_id)
    well_phases_id=bhadata.well_phases_id
    source_id=bhadata.id
    bhaelement_ids = list(BhaElement.objects.filter(bhadata_id=bhadata.id).values_list('id', flat=True))
    userlog=adduserlog('BHA data Deleted',request,bhaelement_ids,'BHA data',request.user.licence_type,well.project_id,well_id,well_phases_id,'delete')
  
    bhadata.delete()
    
    
    return redirect('bhadata:bhadatalist',wellphase_id=well_phases_id)

def deletebha_actual(request, wellphase_id, template_name='crudapp/confirm_delete.html'):
    well_id=request.session['well_id']
    bhadata=BhaData.objects.filter(company=request.company,well_id=well_id,well_phases_id=wellphase_id,status=1)
    bhadata.update(status=0)
    return redirect('bhadata:bhadatalist',wellphase_id=wellphase_id)

def importbha_actual(request,wellphase_id):
    well_id=request.session['well_id']
    if request.method == 'POST' and 'myfile' in request.FILES:    
        dataset = Dataset()
        new_datas = request.FILES['myfile']
        if not new_datas.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'bhadata/importbha_actual.html', {'well_id':well_id})
        obj={}
        element=[]
        od=[]
        id=[]
        length=[]
        imported_bha = dataset.load(new_datas.read(),format='xlsx')
        for data in imported_bha:
            element.append(data[0])
            od.append(data[1])
            id.append(data[2])
            length.append(data[3])
        
        obj['element']=element
        obj['od']=od
        obj['id']=id
        obj['length']=length
        request.session['element'] = element
        request.session['od'] = od
        request.session['id'] = id
        request.session['length'] = length
        request.session['imported_bha'] = obj
        print(imported_bha)
        loop_times = range(1, 5)
        well = Wells.objects.get(id=well_id)
        welltype = well.well_type
        data = BhaData.objects.filter(company=request.company,well_id=well_id,well_phases_id=wellphase_id,status=1)
        wellphase=WellPhases.objects.filter(id=wellphase_id)
        # return render(request,'bhadata/create.html',{'data': data,'well_id':well_id,'welltype':welltype,'wellphases':wellphase,'wellphase_id':wellphase_id,'countries':getcountries(request.company),'company':request.company,'well':well}) 
        return redirect('bhadata:bhadatalist',wellphase_id=wellphase_id)
        
    return render(request, 'bhadata/importbha_actual.html', {'well_id':well_id})

def download_xls_data(self,well_id):
    df_output = pd.DataFrame({'BHA Element': [],'OD': [],'ID': [],'Length': [] })
    excel_file = IO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter' )
    df_output.to_excel(xlwriter, 'sheetname',index=False)

    xlwriter.save()
    xlwriter.close()

    excel_file.seek(0)
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Hydraulics.xlsx'
    return response

def bhacaluculation(request):
    nominal_od = float(request.GET['drillcoll'])
    well_id = request.GET['well_id']
    drillcollars=Drillcollers.objects.values('normal_od').annotate(Count('id')).order_by().filter(id__count__gt=0).filter(is_superadmin=1)
    collar_weight=Drillcollers.objects.values('weight','unit').annotate(Count('weight')).order_by().filter(weight__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company)).filter(normal_od=nominal_od)
    pipe_type=Drillcollers.objects.values('pipe_type').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1).filter(normal_od=nominal_od)
    unit=getprojectunit(well_id)
    if(collar_weight.count()>0):
        pipeunit=collar_weight[0]['unit']
    else:
        pipeunit='API'
    pipeweight_data=convertpipe_weight(pipeunit,unit,collar_weight)
    data={
        "collar_weight":collar_weight,
        "pipe_type":pipe_type
    }   
    return JsonResponse({"data": list(pipeweight_data)})

def getweight_drillpipe(request):
    # normal_od = float(request.GET['normal_od'])
    # drillpipe_weight=Drillpipe.objects.values('weight').annotate(Count('id')).order_by().filter(id__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company)).filter(normal_od=normal_od)
    # return JsonResponse({"data": list(drillpipe_weight)})
    normal_od = float(request.GET['normal_od'])
    well_id = request.GET['well_id']
    drillpipe_weight=Drillpipe.objects.values('weight','unit').annotate(Count('id')).order_by().filter(id__count__gt=0).filter(Q(is_superadmin=1) | Q(company=request.company)).filter(normal_od=normal_od)
    unit=getprojectunit(well_id)
    if(drillpipe_weight.count()>0):
        pipeunit=drillpipe_weight[0]['unit']
    else:
        pipeunit='API'
    pipeweight_data=convertpipe_weight(pipeunit,unit,drillpipe_weight)
    return JsonResponse({"data": list(pipeweight_data)})

def getweight_hwdpnod(request):
    normal_od = float(request.GET['normal_od'])
    well_id = request.GET['well_id']
    # hwdp_weight=DrillpipeHWDP.objects.values('weight').annotate(Count('id')).order_by().filter(id__count__gt=0).filter(is_superadmin=1).filter(nominal_od=normal_od)
    hwdp_weight=DrillpipeHWDP.objects.values('weight','unit').annotate(Count('id')).order_by().filter(id__count__gt=0,nominal_od=normal_od).filter(Q(is_superadmin=1) | Q(company=request.company))
    unit=getprojectunit(well_id)
    if(hwdp_weight.count()>0):
        hwdpunit=hwdp_weight[0]['unit']
    else:
        hwdpunit='API'
    collerweight_data=convertpipe_weight(hwdpunit,unit,hwdp_weight)
    return JsonResponse({"data": list(collerweight_data)})

def bha_pipe_calc(request):
    pipe_type = float(request.GET['collar_weight'])
    pipe_type=Drillcollers.objects.values('pipe_type').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1).filter(weight=pipe_type)
    data={
        "pipe_type":pipe_type
    }   
    return JsonResponse({"data": list(pipe_type)})

def getgrade_drillpipe(request):
    drillpipe_weight = float(request.GET['drillpipe_weight'])
    normal_od=float(request.GET['normal_od']) 
    grade=Drillpipe.objects.values('steel_grade').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1).filter(weight=drillpipe_weight).filter(normal_od=normal_od)
    return JsonResponse({"data": list(grade)})

def getjointtype_drillpipe(request):
    drillpipe_weight = float(request.GET['drillpipe_weight'])
    normal_od=float(request.GET['normal_od']) 
    drillpipe_grade=request.GET['drillpipe_grade']
    joint_type=Drillpipe.objects.values('connection_type').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1).filter(weight=drillpipe_weight).filter(normal_od=normal_od).filter(steel_grade=drillpipe_grade)
    return JsonResponse({"data": list(joint_type)})

def getjointtype_hwdp(request):
    hwdp_weight = float(request.GET['hwdp_weight'])
    normal_od=float(request.GET['normal_od']) 
    joint_type=DrillpipeHWDP.objects.values('connection_type').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1).filter(weight=hwdp_weight).filter(nominal_od=normal_od)
    return JsonResponse({"data": list(joint_type)})

def getjointod_drillpipe(request):
    drillpipe_weight = float(request.GET['drillpipe_weight'])
    normal_od=float(request.GET['normal_od'])
    drillpipe_grade=request.GET['drillpipe_grade']
    drillpipe_jointtype=request.GET['drillpipe_jointtype']
    well_id=request.GET['well_id']
    nod=request.GET['nod']
    joint_od=Drillpipe.objects.values('tool_od','unit','tool_id').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1).filter(weight=drillpipe_weight).filter(normal_od=normal_od).filter(steel_grade=drillpipe_grade).filter(connection_type=drillpipe_jointtype).annotate(data=F('tool_od'))
    tool_id=Drillpipe.objects.values('unit','tool_id').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1).filter(weight=drillpipe_weight).filter(normal_od=normal_od).filter(steel_grade=drillpipe_grade).filter(connection_type=drillpipe_jointtype).annotate(data=F('tool_id'))
    joint_id=Drillpipe.objects.values('pipebody_id').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1,weight=drillpipe_weight,normal_od=normal_od,steel_grade=drillpipe_grade,connection_type=drillpipe_jointtype).annotate(data=F('pipebody_id'))
    unit=getprojectunit(well_id)
    drillunit=joint_od[0]['unit']
    tool_od_data=converttosi(drillunit,unit,joint_od)    
    tool_id_data=converttosi(drillunit,unit,joint_id)  
    tool_ids_data=converttosi(drillunit,unit,tool_id)  
    tool_id=joint_od[0]['tool_id']
    return JsonResponse({"data": list(zip(tool_id_data,tool_od_data)),'nod':nod,'tool_id':tool_ids_data[0]})

def getjointod_hwdp(request):
    hwdp_weight = float(request.GET['hwdp_weight'])
    normal_od=float(request.GET['normal_od']) 
    hwdp_jointtype=request.GET['hwdp_jointtype']
    well_id=request.GET['well_id']
    nod=request.GET['nod']
    joint_od=DrillpipeHWDP.objects.values('tool_od','unit').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1).filter(weight=hwdp_weight).filter(nominal_od=normal_od).filter(connection_type=hwdp_jointtype).annotate(data=F('tool_od'))
    joint_id=DrillpipeHWDP.objects.values('tool_id','unit').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1,weight=hwdp_weight,nominal_od=normal_od,connection_type=hwdp_jointtype).annotate(data=F('tool_id'))
    unit=getprojectunit(well_id)
    hwdpunit=joint_od[0]['unit']
    tool_od_data=converttosi(hwdpunit,unit,joint_od)
    tool_ids_data=converttosi(hwdpunit,unit,joint_id)
    return JsonResponse({"data": list(zip(tool_od_data,joint_id)),'nod':nod,'tool_id':tool_ids_data[0]})

def getclass_drillpipe(request):
    drillpipe_weight = float(request.GET['drillpipe_weight'])
    normal_od=float(request.GET['normal_od']) 
    drillpipe_grade=request.GET['drillpipe_grade']
    drillpipe_jointtype=request.GET['drillpipe_jointtype']
    drillpipe_jointod=float(request.GET['drillpipe_jointod'])
    classtype=Drillpipe.objects.values('class_type').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1).filter(weight=drillpipe_weight).filter(normal_od=normal_od).filter(steel_grade=drillpipe_grade).filter(connection_type=drillpipe_jointtype)
    return JsonResponse({"data": list(classtype)})

def getclass_hwdp(request):
    hwdp_weight = float(request.GET['hwdp_weight'])
    normal_od=float(request.GET['normal_od'])
    hwdp_jointtype=request.GET['hwdp_jointtype']
    hwdp_jointod=request.GET['hwdp_jointod']
    classtype=DrillpipeHWDP.objects.values('class_type').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1).filter(weight=hwdp_weight).filter(nominal_od=normal_od).filter(connection_type=hwdp_jointtype)
    return JsonResponse({"data": list(classtype)})

def bha_Connectpipe_calc(request):
    pipe_type = request.GET['pipe_type']
    w_pipe = request.GET['w_pipe']
    connect_pipe_type=Drillcollers.objects.values('connection_type').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1).filter(pipe_type=pipe_type).filter(weight=w_pipe)
    data={
        "connect_pipe_type":connect_pipe_type
    }   
    return JsonResponse({"data": list(connect_pipe_type)})

def bha_tooljoint_calc(request):
    well_id = request.GET['well_id']
    conn_type = request.GET['conn_type']
    pipe_type = request.GET['pipe_type']
    w_pipe = request.GET['w_pipe']
    tool_od=Drillcollers.objects.values('tool_od','unit').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1).filter(pipe_type=pipe_type).filter(weight=w_pipe).filter(connection_type=conn_type).annotate(data=F('tool_od'))
    unit=getprojectunit(well_id)
    drillunit=tool_od[0]['unit']
    tool_od_data=converttosi(drillunit,unit,tool_od)
    data={
        "tool_od":tool_od
    }   
    return JsonResponse({"data": list(tool_od_data)})

def getdrillcollordetails(request):
    bhaelement_id = request.GET['bhaelement_id']
    drillcollars=Drillcollers.objects.annotate(Count('id')).order_by().filter(id__count__gt=0).filter(is_superadmin=1).only('normal_od')
    bhaelement = BhaElement.objects.filter(id=bhaelement_id).only('od')
    drillcollarsdata = serializers.serialize('json', drillcollars)
    bhaelementdata = serializers.serialize('json', bhaelement)
    return JsonResponse({"data": drillcollarsdata,"bhaelement":bhaelementdata})

def bha_tooljoint_id_calc(request):
    pipe_type = request.GET['pipe_type']
    w_pipe = request.GET['w_pipe']
    c_type = request.GET['c_type']
    well_id = request.GET['well_id']
    nod = request.GET['nod']
    tool_od=Drillcollers.objects.values('tool_od','unit').annotate(Count('id')).filter(id__count__gt=0).filter(is_superadmin=1,pipe_type=pipe_type,weight=w_pipe,connection_type=c_type).annotate(data=F('tool_od'))
    tool_id=Drillcollers.objects.values('tool_id','unit').annotate(Count('id')).filter(id__count__gt=0,is_superadmin=1,pipe_type=pipe_type,weight=w_pipe,connection_type=c_type).annotate(data=F('tool_id'))
    unit=getprojectunit(well_id)
    drillunit=tool_od[0]['unit']
    # tool_id=tool_od[0]['tool_id']
    tool_od_data=converttosi(drillunit,unit,tool_od)
    tool_id_data=converttosi(drillunit,unit,tool_id)
    print(f'tool_id_data{tool_id_data}')
    return JsonResponse({"data": list(tool_od_data),'tool_id':tool_id_data,'nod':nod})



#Admin Dril Collars
def admindrillcollersdetails(request):
    
    drillcollers=Drillcollers.objects.filter(is_superadmin=1)
    request.session['master']='drill_collars'
    if(len(drillcollers) == 0):
        return redirect('bhadata:admindrillcollerscreate')
    return render(request,'adminmaster/drillcollersview.html',{'drillcollers': drillcollers})

def admindrillcollerscreate(request):
    if request.method == 'POST':
        normal_od=request.POST.getlist('normal_od')
        normal_id=request.POST.getlist('normal_id')
        weight=request.POST.getlist('weight')
        pipe_type=request.POST.getlist('pipe_type')
        connection_type=request.POST.getlist('connection_type')
        tool_od=request.POST.getlist('tool_od')
        tool_id=request.POST.getlist('tool_id')
        i = 0 ; drillcollers_id = []
        while i < len(normal_od):
            if(normal_od[i]):     
                drillcollers = Drillcollers.objects.create(normal_od=normal_od[i],normal_id=normal_id[i],weight=weight[i],pipe_type=pipe_type[i],
                connection_type=connection_type[i],tool_od=tool_od[i],tool_id=tool_id[i],
                company=request.company,is_superadmin=1)
                drillcollers_id.append(drillcollers.id)
            i += 1 
        userlog=adduserlog('DrillCollers created',request,drillcollers_id,'admindrillcoller',None,None,None)
        return redirect('bhadata:admindrillcollersdetails')
    
    return render(request,'adminmaster/drillcollerscreate.html')


def admindrillcollersedit(request,template_name='adminmaster/drillcollersedit.html'):
    drillcollers=Drillcollers.objects.filter(is_superadmin=1)
    if request.method == 'POST':
        Drillcollers.objects.filter(is_superadmin=1).delete()
        normal_od=request.POST.getlist('normal_od')
        normal_id=request.POST.getlist('normal_id')
        weight=request.POST.getlist('weight')
        pipe_type=request.POST.getlist('pipe_type')
        connection_type=request.POST.getlist('connection_type')
        tool_od=request.POST.getlist('tool_od')
        tool_id=request.POST.getlist('tool_id')
        i = 0
        while i < len(normal_od):
            if(normal_od[i]):     
                Drillcollers.objects.create(normal_od=normal_od[i],normal_id=normal_id[i],weight=weight[i],pipe_type=pipe_type[i],
                connection_type=connection_type[i],tool_od=tool_od[i],tool_id=tool_id[i],
                is_superadmin=1)
            i += 1
        userlog=adduserlog('DrillCollers edited',request,[],'admindrillcoller',None,None,None)
        return redirect('bhadata:admindrillcollersdetails')
    return render(request, template_name, {'drillcollers':drillcollers})


def admindrillcollersdelete(request,template_name='crudapp/confirm_delete.html'):
    drillcollers = Drillcollers.objects.filter(is_superadmin=1)
    drillcollers.delete()
    return redirect('bhadata:admindrillcollersdetails')

def adminimportdata(request):
    drillcollers=Drillcollers.objects.filter(is_superadmin=1)
    if request.method == 'POST' and 'myfile' in request.FILES:
        drillcollers = DrillcollersForm(request.POST, request.FILES) 
        dataset = Dataset()
        new_datas = request.FILES['myfile']
        unit=request.POST['unit']
        if not new_datas.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'adminmaster/adminimportdata.html')
        imported_data = dataset.load(new_datas.read(),format='xlsx')
        for data in imported_data:
            obj = Drillcollers.objects.create(normal_od=data[0],normal_id=data[1],
            weight=data[2],pipe_type=data[3],
            connection_type=data[4],tool_od=data[5],
            tool_id=data[6],unit=unit,is_superadmin=1)
            obj.save()       
        return redirect('bhadata:admindrillcollersdetails')
    return render(request, 'adminmaster/adminimportdata.html')


def download_csv_data(self):
    df_output = pd.DataFrame({'Nominal OD': [], 'Normal ID': [],'Weight': [],
    'Type': [],'Connection Type':[],'Tool OD':[],'Tool ID': []})
    excel_file = IO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter' )   
    df_output.to_excel(xlwriter, 'sheetname',index=False)
    xlwriter.save()
    xlwriter.close()
    excel_file.seek(0)
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Hydraulics.xlsx'
    return response

# Master Dril Collers
def drillcollersdetails(request):
    collers=Drillcollers.objects.filter(company=request.company)
    admincollers=Drillcollers.objects.filter(is_superadmin=1)
    request.session['master']='drill_collars'   
    paginator = Paginator(collers, 20)
    page = request.GET.get('page', 1)
    try:
        collers = paginator.page(page)
    except PageNotAnInteger:
        collers = paginator.page(1)
    except EmptyPage:
        collers = paginator.page(paginator.num_pages)
    # if(len(collers) == 0):
    #     return redirect('bhadata:drillcollerscreate')
    user_rights_privilege_create = "Create Master"
    user_rights_privilege_edit = "Edit Master"
    user_rights_companyid = request.user.company_id
    user = User.objects.getuserid(request.user.id)
    user_rights_groups = user.groups.all().first()
    
    return render(request,'master/drillcollerview.html',
    {'collers': collers,
    'admincollers':admincollers,
    'user_rights_companyid':user_rights_companyid,
    'user_rights_groups':user_rights_groups,
    'request':request


    
    })

def drillcollerscreate(request):
    if request.method == 'POST':
        normal_od=request.POST.getlist('normal_od')
        normal_id=request.POST.getlist('normal_id')
        weight=request.POST.getlist('weight')
        pipe_type=request.POST.getlist('pipe_type')
        connection_type=request.POST.getlist('connection_type')
        tool_od=request.POST.getlist('tool_od')
        tool_id=request.POST.getlist('tool_id')
        unit=request.POST.get('unit')
        i = 0
        drillcollerscereate=[]
        while i < len(normal_od):
            if(normal_od[i]):     
                dril=Drillcollers.objects.create(normal_od=normal_od[i],normal_id=normal_id[i],weight=weight[i],pipe_type=pipe_type[i],
                connection_type=connection_type[i],tool_od=tool_od[i],tool_id=tool_id[i],unit=unit,
                company=request.company)
                drillcollerscereate.append(dril.id)
            i += 1


        drillcollerscereate = ', '.join(map(str, drillcollerscereate))
        adduserlog('drill collers create',request,drillcollerscereate,'drillcollers',request.user.licence_type,None,None)
        return redirect('bhadata:drillcollersview')

    return render(request,'master/drillcollercreate.html')

def drillcollersedit(request,template_name='master/drillcollersedit.html'):
    drillcollers = Drillcollers.objects.filter(company=request.company)
    unit=drillcollers[0].unit
    if request.method == 'POST':    
        Drillcollers.objects.filter(company=request.company).delete()
        normal_od=request.POST.getlist('normal_od')
        normal_id=request.POST.getlist('normal_id')
        weight=request.POST.getlist('weight')
        pipe_type=request.POST.getlist('pipe_type')
        connection_type=request.POST.getlist('connection_type')
        tool_od=request.POST.getlist('tool_od')
        tool_id=request.POST.getlist('tool_id')
        unit=request.POST.getlist('unit')
        
        i = 0
        while i < len(normal_od)-1:
            if(normal_od[i]):     
                Drillcollers.objects.create(normal_od=normal_od[i],normal_id=normal_id[i],weight=weight[i],pipe_type=pipe_type[i],
                connection_type=connection_type[i],tool_od=tool_od[i],tool_id=tool_id[i],unit=unit[i],
                company=request.company)
            i += 1
            
        adduserlog('drill collers edit',request,[],'drillcollers',request.user.licence_type,None,None)
        return redirect('bhadata:drillcollersview')
    return render(request, template_name, {'drillcollers':drillcollers,'unit':unit})


def drillcollersdelete(request, template_name='crudapp/confirm_delete.html'):
    drillcollers = Drillcollers.objects.filter(company=request.company)
    drillcollers.delete()
    adduserlog('drill collers delete',request,None,'drillcollers',request.user.licence_type,None,None)
    return redirect('bhadata:drillcollersview')

def masterimportdata(request):
    drillcollers=Drillcollers.objects.filter(company=request.company)
    if request.method == 'POST' and 'myfile' in request.FILES:
        drillcollers = DrillcollersForm(request.POST, request.FILES) 
        dataset = Dataset()
        new_datas = request.FILES['myfile']
        unit=request.POST.get('unit')
        if not new_datas.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'adminmaster/adminimportdata.html')
        imported_data = dataset.load(new_datas.read(),format='xlsx')
        for data in imported_data:
            obj = Drillcollers.objects.create(normal_od=data[0],normal_id=data[1],
            weight=data[2],pipe_type=data[3],
            connection_type=data[4],tool_od=data[5],
            tool_id=data[6],
            company=request.company,unit=unit)
            obj.save()       
        return redirect('bhadata:drillcollersview')
    return render(request, 'master/masterimportdata.html')

# Admin Dril Pipe
def admindrillpipedetails(request):
    drillpipe=Drillpipe.objects.filter(is_superadmin=1)
    request.session['master']='drill_pipe'
    # paginator = Paginator(drillpipe, 20)
    # page = request.GET.get('page', 1)
    # try:
    #     drillpipe = paginator.page(page)
    # except PageNotAnInteger:
    #     drillpipe = paginator.page(1)
    # except EmptyPage:
    #     drillpipe = paginator.page(paginator.num_pages)
    if(len(drillpipe) == 0):
        return redirect('bhadata:admindrillpipecreate')
    return render(request,'adminmaster/drillpipeview.html',{'drillpipe': drillpipe})


def admindrillpipecreate(request):
    if request.method == 'POST':
        normal_od=request.POST.getlist('normal_od')
        class_type=request.POST.getlist('class_type')
        pipebody_od=request.POST.getlist('pipebody_od')
        weight=request.POST.getlist('weight')
        pipebody_id=request.POST.getlist('pipebody_id')
        connection_type=request.POST.getlist('connection_type')
        upset=request.POST.getlist('upset')
        tool_od=request.POST.getlist('tool_od')
        tool_id=request.POST.getlist('tool_id')
        box_length=request.POST.getlist('box_length')
        pin_length=request.POST.getlist('pin_length')
        steel_grade=request.POST.getlist('steel_grade')
        i = 0 ; drillpipe_ids = []
        while i < len(normal_od):
            if(normal_od[i]):     
                drillpipe = Drillpipe.objects.create(normal_od=normal_od[i],class_type=class_type[i],pipebody_od=pipebody_od[i],weight=weight[i],pipebody_id=pipebody_id[i],
                connection_type=connection_type[i],upset=upset[i],tool_od=tool_od[i],tool_id=tool_id[i],box_length=box_length[i],pin_length=pin_length[i],
                is_superadmin=1,steel_grade=steel_grade[i])
                drillpipe_ids.append(drillpipe.id)
            i += 1 
        userlog=adduserlog('Drillpipe created',request,drillpipe_ids,'admindrillpipe',None,None,None)
        return redirect('bhadata:admindrillpipeview')
    return render(request,'adminmaster/drillpipecreate.html')

def admindrillpipeedit(request, template_name='adminmaster/drillpipeedit.html'):
    drillpipe = Drillpipe.objects.filter(is_superadmin=1)
    if request.method == 'POST':
        Drillpipe.objects.filter(is_superadmin=1).delete()
        normal_od=request.POST.getlist('normal_od')
        class_type=request.POST.getlist('class_type')
        pipebody_od=request.POST.getlist('pipebody_od')
        weight=request.POST.getlist('weight')
        pipebody_id=request.POST.getlist('pipebody_id')
        connection_type=request.POST.getlist('connection_type')
        upset=request.POST.getlist('upset')
        tool_od=request.POST.getlist('tool_od')
        tool_id=request.POST.getlist('tool_id')
        box_length=request.POST.getlist('box_length')
        pin_length=request.POST.getlist('pin_length')
        steel_grade=request.POST.getlist('steel_grade')
        i = 0
        while i < len(normal_od):
            if(normal_od[i]):     
                Drillpipe.objects.create(normal_od=normal_od[i],class_type=class_type[i],pipebody_od=pipebody_od[i],weight=weight[i],pipebody_id=pipebody_id[i],
                connection_type=connection_type[i],upset=upset[i],tool_od=tool_od[i],tool_id=tool_id[i],box_length=box_length[i],pin_length=pin_length[i],
                is_superadmin=1,steel_grade=steel_grade[i])
            i += 1 
        userlog=adduserlog('Drillpipe edited',request,[],'admindrillpipe',None,None,None)
        return redirect('bhadata:admindrillpipeview')
    return render(request, template_name, {'drillpipe':drillpipe})

def admindrillpipedelete(request):
    drillpipe = Drillpipe.objects.filter(is_superadmin=1)
    drillpipe.delete()
    return redirect('bhadata:admindrillpipeview')

def adminpipeimportdata(request):
    drillpipe=Drillpipe.objects.filter(is_superadmin=1)
    if request.method == 'POST' and 'myfile' in request.FILES:
        drillpipe = DrillpipeForm(request.POST, request.FILES) 
        dataset = Dataset()
        new_datas = request.FILES['myfile']
        unit=request.POST['unit']
        if not new_datas.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'adminmaster/adminpipeimportdata.html')
        imported_data = dataset.load(new_datas.read(),format='xlsx')
        for data in imported_data:
            if(type(data[0]) == str):
                nominal_od=float(Mixed(data[0]))
            else:
                nominal_od=data[0]
            obj = Drillpipe.objects.create(normal_od=nominal_od,class_type=data[1],pipebody_od=data[2],
            weight=data[3],pipebody_id=data[4],
            connection_type=data[5],upset=data[6],tool_od=data[7],
            tool_id=data[8],box_length=data[9],pin_length=data[10],steel_grade=data[11],
            is_superadmin=1,unit=unit)
            obj.save()       
        return redirect('bhadata:admindrillpipeview')
    return render(request, 'adminmaster/adminpipeimportdata.html')

def pipe_download_csv_data(self):
    df_output = pd.DataFrame({'Nominal OD': [],'Class':[], 'Pipe OD': [],'Weight': [],'Pipe ID': [],
    'Connection Type':[],'Upset': [],'Tool OD':[],'Tool ID': [],'Box Length': [],'Pin Length': [],'Steel Grade': [],})
    excel_file = IO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter' )   
    df_output.to_excel(xlwriter, 'sheetname',index=False)
    xlwriter.save()
    xlwriter.close()
    excel_file.seek(0)
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Hydraulics.xlsx'
    return response

# Client drill pipe

def drillpipedetails(request):
    drillpipe=Drillpipe.objects.filter(company=request.company)
    admindrillpipe=Drillpipe.objects.filter(is_superadmin=1)
    request.session['master']='drill_pipe'
    # paginator = Paginator(drillpipe, 20)
    # page = request.GET.get('page', 1)
    # try:
    #     drillpipe = paginator.page(page)
    # except PageNotAnInteger:
    #     drillpipe = paginator.page(1)
    # except EmptyPage:
    #     drillpipe = paginator.page(paginator.num_pages)
    # if(len(drillpipe) == 0):
    #     return redirect('bhadata:drillpipecreate')
    user_rights_companyid = request.user.company_id
    user = User.objects.getuserid(request.user.id)
    user_rights_groups = user.groups.all().first()
    return render(request,'master/drillpipeview.html',
    {'drillpipe': drillpipe,
    'admindrillpipe':admindrillpipe,
    'user_rights_companyid':user_rights_companyid,
    'user_rights_groups':user_rights_groups,
    'request':request

    })


def drillpipecreate(request):
    if request.method == 'POST':
        normal_od=request.POST.getlist('normal_od')
        class_type=request.POST.getlist('class_type')
        pipebody_od=request.POST.getlist('pipebody_od')
        weight=request.POST.getlist('weight')
        pipebody_id=request.POST.getlist('pipebody_id')
        connection_type=request.POST.getlist('connection_type')
        upset=request.POST.getlist('upset')
        tool_od=request.POST.getlist('tool_od')
        tool_id=request.POST.getlist('tool_id')
        box_length=request.POST.getlist('box_length')
        pin_length=request.POST.getlist('pin_length')
        steel_grade=request.POST.getlist('steel_grade')
        unit=request.POST.get('unit')
        print(f"units {unit}")
        print(len(normal_od))
        drillpipecreate=[]
        print('1',normal_od)
        print('2',class_type)
        print('3',pipebody_od)
        print('4',weight)
        print('5',pipebody_id)
        print('6',connection_type)
        print('7',upset)
        print('8',tool_od)
        print('9',tool_id)
        print('10',box_length)
        print('11',pin_length)
        print('12',steel_grade)
        
        i=0
        while i < len(normal_od)-1:
            print(i)
            if(normal_od[i]):  
                drillpipe=Drillpipe.objects.create(normal_od=normal_od[i],class_type=class_type[i],pipebody_od=pipebody_od[i],weight=weight[i],pipebody_id=pipebody_id[i],
                connection_type=connection_type[i],upset=upset[i],tool_od=tool_od[i],tool_id=tool_id[i],box_length=box_length[i],pin_length=pin_length[i],
                company=request.company,steel_grade=steel_grade[i])
                drillpipecreate.append(drillpipe.id)
            i += 1

        drillpipecreate = ', '.join(map(str, drillpipecreate))
        adduserlog("Drillpipecreate",request,drillpipecreate,"Drillpipe",request.user.licence_type,None,None)    
        return redirect('bhadata:drillpipeview')
    return render(request,'master/drillpipecreate.html')

def drillpipeedit(request, template_name='master/drillpipeedit.html'):
    drillpipe = Drillpipe.objects.filter(company=request.company)
    unit=drillpipe[0].unit
    if request.method == 'POST':
        Drillpipe.objects.filter(company=request.company).delete()
        normal_od=request.POST.getlist('normal_od')
        class_type=request.POST.getlist('class_type')
        pipebody_od=request.POST.getlist('pipebody_od')
        weight=request.POST.getlist('weight')
        pipebody_id=request.POST.getlist('pipebody_id')
        connection_type=request.POST.getlist('connection_type')
        upset=request.POST.getlist('upset')
        tool_od=request.POST.getlist('tool_od')
        tool_id=request.POST.getlist('tool_id')
        box_length=request.POST.getlist('box_length')
        pin_length=request.POST.getlist('pin_length')
        steel_grade=request.POST.getlist('steel_grade')
        unit=request.POST.getlist('unit')
        i = 0
        while i < len(normal_od):
            if(normal_od[i]):     
                Drillpipe.objects.create(normal_od=normal_od[i],class_type=class_type[i],pipebody_od=pipebody_od[i],weight=weight[i],pipebody_id=pipebody_id[i],
                connection_type=connection_type[i],upset=upset[i],tool_od=tool_od[i],tool_id=tool_id[i],box_length=box_length[i],pin_length=pin_length[i],
                unit=unit[i],company=request.company,steel_grade=steel_grade[i])
            i += 1
        adduserlog("Drillpipeedit",request,[],"Drillpipe",request.user.licence_type,None,None) 
        return redirect('bhadata:drillpipeview')
    return render(request, template_name, {'drillpipe':drillpipe,'unit':unit})


def drillpipedelete(request):
    drillpipe = Drillpipe.objects.filter(company=request.company)
    drillpipe.delete()
    return redirect('bhadata:drillpipeview')


def masterpipeimportdata(request):
    drillpipe=Drillpipe.objects.filter(company=request.company)
    if request.method == 'POST' and 'myfile' in request.FILES:
        drillpipe = DrillpipeForm(request.POST, request.FILES) 
        dataset = Dataset()
        new_datas = request.FILES['myfile']
        unit=request.POST['unit']
        if not new_datas.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'master/masterpipeimportdata.html')
        imported_data = dataset.load(new_datas.read(),format='xlsx')
        for data in imported_data:
            if(type(data[0]) == str):
                nominal_od=float(Mixed(data[0]))
            else:
                nominal_od=data[0]
            obj = Drillpipe.objects.create(normal_od=nominal_od,class_type=data[1],pipebody_od=data[2],
            weight=data[3],pipebody_id=data[4],
            connection_type=data[5],upset=data[6],tool_od=data[7],
            tool_id=data[8],box_length=data[9],pin_length=data[10],steel_grade=data[11],
            company=request.company,unit=unit)
            obj.save()       
        return redirect('bhadata:drillpipeview')
    return render(request, 'master/masterpipeimportdata.html')

# Admin Dril Pipe HWDP
def admindrillHWDPdetails(request):
    drillhwdp=DrillpipeHWDP.objects.filter(is_superadmin=1)
    request.session['master']='hwdp'
    # paginator = Paginator(drillhwdp, 20)
    # page = request.GET.get('page', 1)
    # try:
    #     drillhwdp = paginator.page(page)
    # except PageNotAnInteger:
    #     drillhwdp = paginator.page(1)
    # except EmptyPage:
    #     drillhwdp = paginator.page(paginator.num_pages)
    if(len(drillhwdp) == 0):
        return redirect('bhadata:admindrillHWDPcreate')
    return render(request,'adminmaster/drillhwdpview.html',{'drillhwdp': drillhwdp})

def admindrillHWDPcreate(request):
    if request.method == 'POST':
        nominal_od=request.POST.getlist('nominal_od')
        class_type=request.POST.getlist('class_type')
        pipebody_od=request.POST.getlist('pipebody_od')
        weight=request.POST.getlist('weight')
        pipebody_id=request.POST.getlist('pipebody_id')
        connection_type=request.POST.getlist('connection_type')
        tool_od=request.POST.getlist('tool_od')
        tool_id=request.POST.getlist('tool_id')
        box_length=request.POST.getlist('box_length')
        pin_length=request.POST.getlist('pin_length')
        unit=request.POST.getlist('unit')
        i = 0 ; hwdp_ids = []
        while i < len(nominal_od):
            if(nominal_od[i]):     
                hwdp = DrillpipeHWDP.objects.create(nominal_od=nominal_od[i],class_type=class_type[i],pipebody_od=pipebody_od[i],weight=weight[i],pipebody_id=pipebody_id[i],
                connection_type=connection_type[i],tool_od=tool_od[i],tool_id=tool_id[i],box_length=box_length[i],pin_length=pin_length[i],unit=unit,
                is_superadmin=1) 
                hwdp_ids.append(hwdp.id)
            i += 1 
        userlog=adduserlog('drillhwdp created',request,hwdp_ids,'admindrillhwdp',None,None,None)
        return redirect('bhadata:admindrillHWDPview')
    return render(request,'adminmaster/drillhwdpcreate.html')

def admindrillHWDPedit(request, template_name='adminmaster/drillhwdpedit.html'):
    drillhwdp = DrillpipeHWDP.objects.filter(is_superadmin=1)
    if request.method == 'POST':
        DrillpipeHWDP.objects.filter(is_superadmin=1).delete()
        nominal_od=request.POST.getlist('nominal_od')
        class_type=request.POST.getlist('class_type')
        pipebody_od=request.POST.getlist('pipebody_od')
        weight=request.POST.getlist('weight')
        pipebody_id=request.POST.getlist('pipebody_id')
        connection_type=request.POST.getlist('connection_type')
        tool_od=request.POST.getlist('tool_od')
        tool_id=request.POST.getlist('tool_id')
        box_length=request.POST.getlist('box_length')
        pin_length=request.POST.getlist('pin_length')
        unit=request.POST.getlist('unit')
        i = 0 ; 
        while i < len(nominal_od):
            if(nominal_od[i]):     
                DrillpipeHWDP.objects.create(nominal_od=nominal_od[i],class_type=class_type[i],pipebody_od=pipebody_od[i],weight=weight[i],pipebody_id=pipebody_id[i],
                connection_type=connection_type[i],tool_od=tool_od[i],tool_id=tool_id[i],box_length=box_length[i],pin_length=pin_length[i],unit=unit,
                is_superadmin=1)
            i += 1 
        userlog=adduserlog('drillhwdp edited',request,[],'admindrillhwdp',None,None,None)
        return redirect('bhadata:admindrillHWDPview')
    return render(request, template_name, {'drillhwdp':drillhwdp})

def admindrillHWDPdelete(request):
    drillhwdp = DrillpipeHWDP.objects.filter(is_superadmin=1)
    drillhwdp.delete()
    return redirect('bhadata:admindrillHWDPview')

def adminHWDPimportdata(request):
    drillhwdp=DrillpipeHWDP.objects.filter(is_superadmin=1)
    if request.method == 'POST' and 'myfile' in request.FILES:
        drillhwdp = DrillpipeHWDPForm(request.POST, request.FILES) 
        dataset = Dataset()
        new_datas = request.FILES['myfile']
        unit=request.POST.get('unit')
        if not new_datas.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'adminmaster/adminhwdpimportdata.html')
        imported_data = dataset.load(new_datas.read(),format='xlsx')
        for data in imported_data:
            obj = DrillpipeHWDP.objects.create(nominal_od=data[0],class_type=data[1],pipebody_od=data[2],
            weight=data[3],pipebody_id=data[4],
            connection_type=data[5],tool_od=data[6],
            tool_id=data[7],box_length=data[8],pin_length=data[9],unit=unit,
            is_superadmin=1)
            obj.save()       
        return redirect('bhadata:admindrillHWDPview')
    return render(request, 'adminmaster/drillhwdpimport.html')

def HWDP_download_csv_data(self):
    df_output = pd.DataFrame({'Nominal OD': [],'Class':[], 'Pipe OD': [],'Weight': [],'Pipe ID': [],
    'Connection Type':[],'Tool OD':[],'Tool ID': [],'Box Length': [],'Pin Length': []})
    excel_file = IO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter' )   
    df_output.to_excel(xlwriter, 'sheetname',index=False)
    xlwriter.save()
    xlwriter.close()
    excel_file.seek(0)
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Hydraulics.xlsx'
    return response



# Client drill pipe HWDP
def drillHWDPdetails(request):
    drillhwdp=DrillpipeHWDP.objects.filter(company=request.company)
    admindrillhwdp=DrillpipeHWDP.objects.filter(is_superadmin=1)
    request.session['master']='hwdp'
    paginator = Paginator(drillhwdp, 20)
    page = request.GET.get('page', 1)
    try:
        drillhwdp = paginator.page(page)
    except PageNotAnInteger:
        drillhwdp = paginator.page(1)
    except EmptyPage:
        drillhwdp = paginator.page(paginator.num_pages)

    user_rights_companyid = request.user.company_id
    user = User.objects.getuserid(request.user.id)
    user_rights_groups = user.groups.all().first()
    # if(len(drillhwdp) == 0):
    #     return redirect('bhadata:drillHWDPcreate')
    return render(request,'master/drillhwdpview.html',
    {'drillhwdp': drillhwdp,
    'admindrillhwdp':admindrillhwdp,
    'user_rights_companyid':user_rights_companyid,
    'user_rights_groups':user_rights_groups,
    'request':request
    })

def drillHWDPcreate(request):
    if request.method == 'POST':
        nominal_od=request.POST.getlist('nominal_od')
        class_type=request.POST.getlist('class_type')
        pipebody_od=request.POST.getlist('pipebody_od')
        weight=request.POST.getlist('weight')
        pipebody_id=request.POST.getlist('pipebody_id')
        connection_type=request.POST.getlist('connection_type')
        tool_od=request.POST.getlist('tool_od')
        tool_id=request.POST.getlist('tool_id')
        box_length=request.POST.getlist('box_length')
        pin_length=request.POST.getlist('pin_length')
        unit=request.POST.getlist('unit')
        i = 0 
        drillhwdp_ids = []
        while i < len(nominal_od)-1:
            if(nominal_od[i]):     
                drillhwdp = DrillpipeHWDP.objects.create(nominal_od=nominal_od[i],class_type=class_type[i],pipebody_od=pipebody_od[i],weight=weight[i],pipebody_id=pipebody_id[i],
                connection_type=connection_type[i],tool_od=tool_od[i],tool_id=tool_id[i],box_length=box_length[i],pin_length=pin_length[i],
                unit=unit[i],company=request.company) 
                drillhwdp_ids.append(drillhwdp.id)
            i += 1 
        adduserlog('drill hwdp create',request,drillhwdp_ids,'drillhwdp',request.user.licence_type,None,None)
        return redirect('bhadata:drillHWDPview')
    return render(request,'master/drillhwdpcreate.html')

def drillHWDPedit(request):
    drillhwdp = DrillpipeHWDP.objects.filter(company=request.company)
    unit=drillhwdp[0].unit
    if request.method == 'POST':
        DrillpipeHWDP.objects.filter(company=request.company).delete()
        nominal_od=request.POST.getlist('nominal_od')
        class_type=request.POST.getlist('class_type')
        pipebody_od=request.POST.getlist('pipebody_od')
        weight=request.POST.getlist('weight')
        pipebody_id=request.POST.getlist('pipebody_id')
        connection_type=request.POST.getlist('connection_type')
        tool_od=request.POST.getlist('tool_od')
        tool_id=request.POST.getlist('tool_id')
        box_length=request.POST.getlist('box_length')
        pin_length=request.POST.getlist('pin_length')
        unit=request.POST.getlist('unit')
        i = 0 
        drillhwdp_ids = []
        while i < len(nominal_od)-1:
            if(nominal_od[i]):     
                drillhwdp = DrillpipeHWDP.objects.create(nominal_od=nominal_od[i],class_type=class_type[i],pipebody_od=pipebody_od[i],weight=weight[i],pipebody_id=pipebody_id[i],
                connection_type=connection_type[i],tool_od=tool_od[i],tool_id=tool_id[i],box_length=box_length[i],pin_length=pin_length[i],
                unit=unit[i],company=request.company)
                drillhwdp_ids.append(drillhwdp.id)
            i += 1 
        adduserlog('drill hwdp edit',request,drillhwdp_ids,'drillhwdp',request.user.licence_type,None,None)
        return redirect('bhadata:drillHWDPview')
    return render(request,'master/drillhwdpedit.html',{'drillhwdp':drillhwdp,'unit':unit})

def drillHWDPdelete(request):
    drillhwdp = DrillpipeHWDP.objects.filter(company=request.company)
    drillhwdp_ids = drillhwdp.values_list('id', flat=True)
    adduserlog('drill hwdp delete',request,drillhwdp_ids,'drillhwdp',request.user.licence_type,None,None)
    drillhwdp.delete()
    return redirect('bhadata:drillHWDPview')

def HWDPimportdata(request):
    drillhwdp=DrillpipeHWDP.objects.filter(company=request.company)
    if request.method == 'POST' and 'myfile' in request.FILES:
        drillhwdp = DrillpipeHWDPForm(request.POST, request.FILES) 
        dataset = Dataset()
        new_datas = request.FILES['myfile']
        unit=request.POST['unit']
        if not new_datas.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'adminmaster/adminhwdpimportdata.html')
        imported_data = dataset.load(new_datas.read(),format='xlsx')
        for data in imported_data:
            obj = DrillpipeHWDP.objects.create(nominal_od=data[0],class_type=data[1],pipebody_od=data[2],
            weight=data[3],pipebody_id=data[4],
            connection_type=data[5],tool_od=data[6],
            tool_id=data[7],box_length=data[8],pin_length=data[9],unit=unit[i],
            company=request.company)
            obj.save()       
        return redirect('bhadata:drillHWDPview')
    return render(request, 'master/drillhwdpimport.html')

def getmud(request):
    wellphase = request.GET['wellphase']
    wellphase_date = request.GET['date']
    mud_data=MudData.objects.filter(well_phase_id=wellphase,date=wellphase_date).values()
    return JsonResponse({"data": list(mud_data)})

def getbhadata(request):
    wellphase = request.GET['wellphase']
    wellphase_date = request.GET['date']
    bha_data=BhaData.objects.filter(well_phases_id=wellphase,date=wellphase_date)
    bhaelement_data=BhaElement.objects.filter(bhadata_id=bha_data[0].id).values()
    return JsonResponse({"data": list(bhaelement_data)})

def getrheogram(request):
    wellphase = request.GET['wellphase']
    rheogram_date = request.GET['date']
    rheogram=RheogramDate.objects.filter(well_phase_id=wellphase,date=rheogram_date)
    rheogram_data_data=Rheogram.objects.filter(rheogram_date_id=rheogram[0].id).values()
    return JsonResponse({"data": list(rheogram_data_data)})

def getdrillbitdata(request):
    wellphase = request.GET['wellphase']
    drillbit_date = request.GET['date']
    drillbit=DrillBit.objects.filter(well_phases_id=wellphase,date=drillbit_date)
    drillbits=DrillBit.objects.filter(well_phases_id=wellphase,date=drillbit_date).values()
    drillbit_data_data=DrillBitNozzle.objects.filter(drillbit_id=drillbit[0].id).values()
    return JsonResponse({"data": list(zip(drillbit_data_data,drillbits))})

def getwellphase(request):
    well_phase=request.GET['well_phase']
    wellphase = WellPhases.objects.filter(id=well_phase).values()
    holesize=wellphase[0]['hole_size']
    element=DrillBit.objects.filter(well_phases_id=well_phase).values('bit_type')
    bit_type=BitTypesNames.objects.filter(id=element[0]['bit_type']).values()
    # return JsonResponse({"data": list(zip(wellphase,element))})
    return JsonResponse({"data":list(bit_type),'holesize':holesize})


def testphase(request,well_id):
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company)
    pagetype=None
    page_type=request.GET.get('type', pagetype)  
    if(page_type != None):
        if(page_type == 'mud'):
            return redirect('muddata:create', well_id=well_id)
        elif(page_type == 'rheogram'):
            return redirect('muddata:rheogramcreate', well_id=well_id)
        elif(page_type == 'bha'):
            return redirect('bhadata:bhadatalist', well_id=well_id)
        else:
            return redirect('drillbitdata:create', well_id=well_id)
    return render(request,'bhadata/phasewise.html',{'wellphase': wellphase})


def getpremium_val(request):
    normal_od = request.GET['normal_od']
    classtype = request.GET['classtype']
    drillpipe_jointod = request.GET['drillpipe_jointod']
    drillpipe_grade = request.GET['drillpipe_grade']
    drillpipe_weight = request.GET['drillpipe_weight']
    drillpipe_jointtype = request.GET['drillpipe_jointtype']
    drillpipe=Drillpipe.objects.filter(normal_od=normal_od,tool_od=drillpipe_jointod,steel_grade=drillpipe_grade,weight=drillpipe_weight,connection_type=drillpipe_jointtype).values()
    pipe_id=drillpipe[0]['pipebody_id']
    tool_od=drillpipe[0]['tool_od']
    if(classtype=='Premium'):
        RF=0.8
        well_thickness=(float(normal_od)-pipe_id)/2
        R_wt=round(well_thickness,2)*RF
        identity=round(R_wt,2)*2+pipe_id
    else:
        RF=0.7
        well_thickness=(float(normal_od)-pipe_id)/2
        R_wt=round(well_thickness,2)*RF
        identity=round(R_wt,2)*2+pipe_id
    data={
        'identity':identity,
        'tool_od':tool_od
    }
    return JsonResponse(data)
    
def box_pin_tooljoint(request):
    type_name = request.GET['type_name']
    well_id = request.GET['well_id']
    normal_od = request.GET['od']
    classtype = request.GET['classtype']
    grade = request.GET['grade']
    weight = request.GET['weight']
    connection_type = request.GET['connection_type']
    onejoint_length = request.GET['onejoint_length']
    total_measured_depth = request.GET['total_measured_depth']
    if(type_name=='Drill Pipe'):
        drillpipe_box=Drillpipe.objects.filter(normal_od=normal_od,steel_grade=grade,weight=weight,connection_type=connection_type).values('box_length','unit').annotate(data=F('box_length'))
        drillpipe_pin=Drillpipe.objects.filter(normal_od=normal_od,steel_grade=grade,weight=weight,connection_type=connection_type).values('pin_length','unit').annotate(data=F('pin_length'))
        # pin_length=drillpipe[0]['pin_length']
        # box_length=drillpipe[0]['box_length']
        unit=getprojectunit(well_id)
        if(drillpipe_box.count()>0):
            hwdpunit=drillpipe_box[0]['unit']
        else:
            hwdpunit='API'
        box_convert_data=converttosi(hwdpunit,unit,drillpipe_box)

        if(drillpipe_pin.count()>0):
            hwdpunit=drillpipe_pin[0]['unit']
        else:
            hwdpunit='API'
        pin_convert_data=converttosi(hwdpunit,unit,drillpipe_pin)

        box_tj_length=box_convert_data[0]
        pin_tj_length=pin_convert_data[0]
    else:
        unit=getprojectunit(well_id)
        drill_hwdp_box=DrillpipeHWDP.objects.filter(nominal_od=normal_od,weight=weight,connection_type=connection_type).values('box_length','unit').annotate(data=F('box_length'))
        drill_hwdp_pin=DrillpipeHWDP.objects.filter(nominal_od=normal_od,weight=weight,connection_type=connection_type).values('pin_length','unit').annotate(data=F('pin_length'))
        # pin_length=drill_hwdp[0]['pin_length']
        # box_length=drill_hwdp[0]['box_length']
      
        if(drill_hwdp_box.count()>0):
            hwdpunit=drill_hwdp_box[0]['unit']
        else:
            hwdpunit='API'
        box_convert_data=converttosi(hwdpunit,unit,drill_hwdp_box)
        
        if(drill_hwdp_pin.count()>0):
            hwdpunit=drill_hwdp_pin[0]['unit']
        else:
            hwdpunit='API'
        pin_convert_data=converttosi(hwdpunit,unit,drill_hwdp_pin)
        box_tj_length=box_convert_data[0]
        pin_tj_length=pin_convert_data[0]
    data={
        'box_tj_length':box_tj_length,
        'pin_tj_length':pin_tj_length
    }
    return JsonResponse(data)

def getempiricaldata(request):
    bhaelememt_id = request.GET['bhaelememt_id']
    specifications=Specifications.objects.filter(bhadata_element_id=bhaelememt_id).values()
    pressdroptool=Pressuredroptool.objects.filter(bhadata_element_id=bhaelememt_id,status=1).values()
    empirical=Empirical.objects.filter(bhadata_element_id=bhaelememt_id).values()
    alldata=[]
    alldata.append({
      'specifications':list(specifications),
      'pressdroptool':list(pressdroptool),
      'empirical':list(empirical)
    })
    return JsonResponse(alldata,safe=False)

def getdifferential_Pressure(request):
    bhaelememt_id = request.GET['bhaelememt_id']
    specifications=Specifications.objects.filter(bhadata_element_id=bhaelememt_id).values()
    differntial_pressure=Differential_pressure.objects.filter(bhadata_element_id=bhaelememt_id,status=1).values()
    alldata=[]
    alldata.append({
        'specifications':list(specifications),
        'differntial_pressure':list(differntial_pressure)
    })
    return JsonResponse(alldata,safe=False)

def getmdtvd_for_selecteddate(request):
    selected_date = request.GET['selected_date']
    selected_time = request.GET['selected_time']
    timestamp=dateconversion(selected_date,selected_time)
    print(f"timestamp {timestamp}")






    

