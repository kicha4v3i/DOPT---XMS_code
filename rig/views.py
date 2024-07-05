from django.shortcuts import render,redirect

# Create your views here.
from rig.models import Rig
from surfacepipe.models import SurfaceNameModels,SurfacePipeData,SurfacePipe
from .forms import RigForm
from surfacepipe.forms import SurfacePipeForm
from django.shortcuts import render, redirect, get_object_or_404
from mud.models import MudPump,MudPumpData,PumpManufacturer,Pumps,MudPumpMasterData,MudPumpMasterSpeed,MudPumpMasterFlowRate,MudPumpFlowRate
from mud.forms import MudPumpForm,MudPumpFlowRateForm,MudPumpDataForm,MudPumpSpeed,PumpManufacturerForm,PumpsForm
from wells.models import Wells 
from custom_auth.getunit import getprojectunit,getcountries,adduserlog,getprojidbywellid
from helpers import user_rights_permission,user_rights_permission_projects
from django.contrib import messages
from helpers.allmodels import MudPump


def details(request,well_id):
    rig_data=Rig.objects.filter(company=request.company,well=well_id,status=1)
    request.session['submenu']='rig_details'
    if(len(rig_data) == 0):
        return redirect('rig:alldetails',well_id=well_id)
    return render(request,'rig/view.html',{'rig_data': rig_data,'well_id':well_id})

def create(request,well_id):
    # request.session['submenu'] = 'rig_details'
    # if 'surface_form' in request.POST:
    #     form = SurfacePipeForm(request.POST)
    #     if form.is_valid():
    #         surfacepipe=form.save()
    #         surfacepipe.company=request.company
    #         surfacepipe.save()
    #         names=request.POST.getlist('name')
    #         length=request.POST.getlist('length')
    #         identity=request.POST.getlist('identity')
    #         i = 0
    #         while i < len(names):
    #             if(names[i]):     
    #                 SurfacePipeData.objects.create(name=names[i],length=length[i],identity=identity[i],surfacepipe=surfacepipe,well_id=well_id,company=request.company)
    #             i += 1
    # if request.method == 'POST':
    #     rig_name=request.POST.getlist('rig_name')
    #     rig_contractor=request.POST.getlist('rig_contractor')
    #     rig_type=request.POST.getlist('rig_type')
    #     i = 0
    #     while i < len(rig_name):
    #         if(rig_name[i]):     
    #             Rig.objects.create(rig_name=rig_name[i],rig_contractor=rig_contractor[i],rig_type=rig_type[i],well_id=well_id,company=request.company)
    #         i += 1
    #     return redirect('rig:detail', well_id=well_id)
    # surface_names= SurfaceNameModels.objects.all()
    # surface=SurfacePipe.objects.filter(company=request.company,well_id=well_id,status=1).last()
    # if surface != None:
    #     surfacepipedata=SurfacePipeData.objects.filter(surfacepipe=surface.id,well_id=well_id,status=1)
    # else:
    #     surfacepipedata=SurfacePipeData.objects.filter(surfacepipe=surface,well_id=well_id,status=1)
    # surface_count=SurfacePipe.objects.filter(company=request.company,well_id=well_id,status=1).count()
    # data={
    #     'surface_names':surface_names,
    #     'well_id':well_id,
    #     'surface_count':surface_count,
    #     'surface':surface,
    #     'surfacepipedata':surfacepipedata
    # }
    return render(request,'rig/create.html')

def edit(request, pk, template_name='rig/edit.html'):
    rig_data = Rig.objects.filter(well_id=pk)
    request.session['submenu'] = 'rig_details'
    if request.method == 'POST':
        Rig.objects.filter(well_id=pk).delete()
        rig_name=request.POST.getlist('rig_name')
        rig_contractor=request.POST.getlist('rig_contractor')
        rig_type=request.POST.getlist('rig_type')
        print('rig_info',rig_name,rig_contractor,rig_type)
        i = 0
        while i < len(rig_name):
            if(rig_name[i]):     
                Rig.objects.create(rig_name=rig_name[i],rig_contractor=rig_contractor[i],rig_type=rig_type[i],well_id=pk,company=request.company)
            i += 1  
        # source_id=1
        # userlog=adduserlog('Rig Informations Created',request,source_id,'Rig')
        print()
        return redirect('rig:detail', well_id=pk)
    return render(request, template_name, {'rig_data':rig_data,'well_id':pk})

def delete(request, pk, template_name='crudapp/confirm_delete.html'):
    proj_id = getprojidbywellid(pk)

    if request.GET['name'] == 'rig':
        rig=Rig.objects.filter(well_id=pk).first()
        source_id=rig.id
        adduserlog('Rig Informations Deleted',request,source_id,'Rig',request.user.licence_type,proj_id,pk,None)
 
        rig = Rig.objects.filter(well_id=pk).update(status=0)
    elif request.GET['name'] == 'surface':
        surfacepipe = get_object_or_404(SurfacePipe, well_id=pk,status=1)
        print('surface_delete',surfacepipe)
        surfacepipes = SurfacePipe.objects.filter(id=surfacepipe.id,well_id=pk).update(status=0)
        source_id=surfacepipe.id
        adduserlog('Surface Form Deleted',request,source_id,'SurfacePipe',request.user.licence_type,proj_id,pk,None)
      
        surfacepipedata = SurfacePipeData.objects.filter(surfacepipe_id=surfacepipe,well_id=pk,status=1).update(status=0)
    elif request.GET['name'] == 'mudpump':
        mud = get_object_or_404(MudPump, well_id=pk,status=1)
        print('mud_delete',mud)
        mud_id=mud.id
        mudpumpspeed=MudPumpSpeed.objects.filter(mud_pump_id=mud_id, well_id=pk,status=1)
        for mud in mudpumpspeed:
            MudPumpFlowRate.objects.filter(mud_pump_speed_id=mud.id, well_id=pk,status=1).update(status=0)
        MudPumpData.objects.filter(mud_pump_id=mud_id, well_id=pk,status=1).update(status=0)
        MudPumpSpeed.objects.filter(mud_pump_id=mud_id, well_id=pk,status=1).update(status=0)
        MudPump.objects.filter(id=mud_id,well_id=pk).update(status=0)
        source_id=mud_id
        adduserlog('Mud Pump Deleted',request,source_id,'Mud Pump',request.user.licence_type,proj_id,pk,None)

    return redirect('rig:alldetails', well_id=pk)

def alldetails(request,well_id):
    checkpermission=user_rights_permission_projects('Create Data',request,'well',well_id)
    if(checkpermission != True):
        messages.error(request,'No Access to create!')
        return redirect(request.META.get('HTTP_REFERER'))
    
    well=Wells.objects.get(id=well_id)
    request.session['submenu'] = 'rig_details'
    if 'surface_form' in request.POST:
        form = SurfacePipeForm(request.POST)
        if form.is_valid():
            surfacepipe=form.save()
            surfacepipe.company=request.company
            surfacepipe.save()
            names=request.POST.getlist('name')
            length=request.POST.getlist('length')
            identity=request.POST.getlist('identity')
            i = 0 
            surface_pipe_ids = []
            while i < len(names):
                if(names[i]):     
                    surface_pipe_data = SurfacePipeData.objects.create(name=names[i],length=length[i],identity=identity[i],surfacepipe=surfacepipe,well_id=well_id,company=request.company)
                    surface_pipe_ids.append(surface_pipe_data.id)
                i += 1 
            proj_id = getprojidbywellid(well_id)
            adduserlog('Surface pipe Created',request,surface_pipe_ids,'SurfacePipe',request.user.licence_type,proj_id,well_id,None,'create')
            # userlog=adduserlog('Surface pipe Created',request,source_id,'Rig')
            # print('userlog',userlog)
    if 'rig_form' in request.POST:
        print('rig_form_crated')
        form = RigForm(request.POST)
        if form.is_valid():
            rig=form.save()
            rig.company=request.company
            rig.save()
            source_id=rig.id 
            adduserlog('Rig Informations Created',request,source_id,'Rig',request.user.licence_type,well.project_id,well_id,None,'create')
            
    if 'mud_pump' in request.POST:
        form = MudPumpForm(request.POST)
        if form.is_valid():
            mud_pump=MudPump.objects.createmudpump(request.POST.get('stroke_length'),request.POST.get('pump_name_select'),request.POST.get('master'),request.POST.get('pump_type'),request.company.id,well_id,request.POST.get('number_of_pumps'))

            linear_size=request.POST.getlist('linear_size')
            max_discharge_pressure=request.POST.getlist('max_discharge_pressure')
            i = 0 
            mudpump_ids = []
            while i < len(linear_size):
                if(linear_size[i]):     
                    mudpump = MudPumpData.objects.create(linear_size=linear_size[i],well=mud_pump.well,max_discharge_pressure=max_discharge_pressure[i],company=request.company,mud_pump=mud_pump)
                    mudpump_ids.append(mudpump.id)
                i += 1
            i = 0
            pump_speed=request.POST.getlist('pump_speed')
            flowrate=request.POST.getlist('flowrate')
            while i < len(pump_speed):
                if(pump_speed[i]):     
                    mud_pump_speed=MudPumpSpeed.objects.create(pump_speed=pump_speed[i],well=mud_pump.well,company=request.company,mud_pump=mud_pump)
                    flowraterow = flowrate[i*len(linear_size):len(linear_size)+(i*len(linear_size))]
                    j=0
                    while j < len(flowraterow):
                        if(flowraterow[j]): 
                            MudPumpFlowRate.objects.create(flowrate=flowraterow[j],well=mud_pump.well,company=request.company,mud_pump_speed=mud_pump_speed)
                            j += 1
                i += 1
            source_id=mudpump_ids
            adduserlog('Mud Pump Created',request,source_id,'Mud Pump',request.user.licence_type,well.project_id,well_id,None,'create')

    rig_data = Rig.objects.filter(company=request.company,well=well_id,status=1)
    rig_count = rig_data.count()
    surface_names= SurfaceNameModels.objects.all()
    surface=SurfacePipe.objects.filter(company=request.company,well_id=well_id,status=1).last()
    if surface != None:
        surfacepipedata=SurfacePipeData.objects.filter(surfacepipe=surface.id,well_id=well_id,status=1)
    else:
        surfacepipedata=SurfacePipeData.objects.filter(surfacepipe=surface,well_id=well_id,status=1)
    surface_count=SurfacePipe.objects.filter(company=request.company,well_id=well_id,status=1).count()
    mudpump_count = MudPump.objects.filter(company=request.company,well_id=well_id,status=1).count()
    print(f"mudpump_count {mudpump_count}")
    # mud=MudPump.objects.get(company=request.company,well=well_id,status=1)
    try:
        mud=MudPump.objects.get(company=request.company,well=well_id,status=1)
    except MudPump.DoesNotExist:
        mud = None
    if(request.user.licence_type != 'Individual'):
        manufactureres = PumpManufacturer.objects.getallpumpmanufacture(request.company.id)
    else:
        manufactureres = PumpManufacturer.objects.get_individual_pumpmanufacture(request.user.id)
    print(f"manufactureres {manufactureres}")

    form = PumpsForm()
    row=[]
    colum=[]
    for i in range(5):
        row.append(i)
    for i in range(4):
        colum.append(i)
    
    countries=getcountries(request.company)
    data={
        'surface_names':surface_names,
        'well_id':well_id,
        'surface_count':surface_count,
        'surface':surface,
        'surfacepipedata':surfacepipedata,
        'rig_data':rig_data,
        'rig_count':rig_count,
        'form': form,
        'manufactureres':manufactureres,
        'well':well,
        'row':row,
        "colum":colum,
        'mudpump_count':mudpump_count,
        'mud':mud,
        'countries':countries,
        'company':request.company,
        'user_id':request.user,
        'module_id':'5',
        'project_id':well.project_id 
    }

    return render(request,'rig/create.html',data)

def all_edit(request, pk, template_name='rig/edit.html'):

    rig_id = Rig.objects.filter(well_id=pk,status=1).last()
    surf_id=SurfacePipe.objects.filter(well_id=pk,status=1).last()  
    mudpump_id=MudPump.objects.filter(well_id=pk,status=1).last()  
    well=Wells.objects.get(id=pk)

    request.session['submenu'] = 'rig_details'
    print('rig_informationss',request.method)
    
    if 'rig_form' in request.POST: 
        print('rig_form_edited_ss')
        rig = get_object_or_404(Rig, pk=rig_id.id)
        form = RigForm(request.POST or None, instance=rig)
        if form.is_valid():
            rig=form.save()
            rig.company=request.company
            rig.save()
            source_id=rig_id.id 
            adduserlog('Rig Informations Edited',request,source_id,'Rig',request.user.licence_type,well.project_id,pk,None)
            print('created')
        return redirect('rig:alldetails', well_id=pk)
    if 'surface_form' in request.POST: 
        print('surface_form_eDited')
        if surf_id !=None:
            surfacepipe = get_object_or_404(SurfacePipe, pk=surf_id.id)
            form = SurfacePipeForm(request.POST or None, instance=surfacepipe)
            SurfacePipeData.objects.filter(surfacepipe=surf_id.id).delete()
        else:
            form = SurfacePipeForm(request.POST)
        
        if form.is_valid():
            surfacepipe=form.save()
            surfacepipe.company=request.company
            surfacepipe.save()
            names=request.POST.getlist('name')
            length=request.POST.getlist('length')
            identity=request.POST.getlist('identity')
            surfacepipe_id=request.POST.getlist('surfacepipe_id')
            i = 0
            currentid=[]
            
            while i < len(names):
                if(names[i]):
                    surfacepipedata = SurfacePipeData.objects.create(name=names[i],length=length[i],identity=identity[i],surfacepipe=surfacepipe,well_id=pk,company=request.company)
                    currentid.append(surfacepipedata.id)
                i += 1
            source_id=currentid 
            proj_id = getprojidbywellid(pk)
            adduserlog('Surface pipe Edited',request,source_id,'SurfacePipe',request.user.licence_type,proj_id,pk,None)
        return redirect('rig:alldetails', well_id=pk)
    if 'mud_pump' in request.POST:
        mud = get_object_or_404(MudPump, pk=mudpump_id.id)
        form = MudPumpForm(request.POST or None, instance=mud)
        well=Wells.objects.get(id=pk)  
    
        if form.is_valid():
            mud_pump=form.save()
            mud_pump.company=request.company
            mud_pump.pump_manufacturer=request.POST.get('master')
            mud_pump.pump_name=request.POST.get('pump_name_select')
            mud_pump.save()
            MudPumpData.objects.filter(mud_pump=mud_pump).delete()
            MudPumpSpeed.objects.filter(mud_pump=mud_pump).delete()
            linear_size=request.POST.getlist('linear_size')
            max_discharge_pressure=request.POST.getlist('max_discharge_pressure')
            i = 0 
            current_id = []
            while i < len(linear_size):
                if(linear_size[i]):     
                    mudpump = MudPumpData.objects.create(linear_size=linear_size[i],well_id=pk,max_discharge_pressure=max_discharge_pressure[i],company=request.company,mud_pump=mud_pump)
                    current_id.append(mudpump.id)
                i += 1
            i = 0
            pump_speed=request.POST.getlist('pump_speed')
            flowrate=request.POST.getlist('flowrate')
            while i < len(pump_speed):
                if(pump_speed[i]):     
                    mud_pump_speed=MudPumpSpeed.objects.create(pump_speed=pump_speed[i],well_id=pk,company=request.company,mud_pump=mud_pump)
                    flowraterow = flowrate[i*len(linear_size):len(linear_size)+(i*len(linear_size))]
                    j=0
                    while j < len(flowraterow):
                        if(flowraterow[j]): 
                            MudPumpFlowRate.objects.create(flowrate=flowraterow[j],company=request.company,well_id=pk,mud_pump_speed=mud_pump_speed)
                            j += 1
                i += 1
            source_id=current_id
            userlog=adduserlog('Mud Pump Edited',request,source_id,'Mud Pump',request.user.licence_type,well.project_id,pk,None)
        return redirect('rig:alldetails', well_id=pk)
    rig_data = Rig.objects.filter(well_id=pk,status=1)
    if surf_id !=None:
        surfacepipedata = SurfacePipeData.objects.filter(surfacepipe=surf_id.id,status=1)
        surfacepipe = get_object_or_404(SurfacePipe, pk=surf_id.id)
        form = SurfacePipeForm(request.POST or None, instance=surfacepipe)
    else:
        surfacepipedata = 0
        surfacepipe = 0
        form = 0
    if mudpump_id != None:
        mud = get_object_or_404(MudPump, pk=mudpump_id.id)
        mud_form = MudPumpForm(request.POST or None, instance=mud)
    else:
        mud = 0
        mud_form = 0
    unit=getprojectunit(pk)
    row=[]
    colum=[]
    for i in range(5):
        row.append(i)
    for i in range(4):
        colum.append(i)
    if request.company:
        manufactureres=PumpManufacturer.objects.getallpumpmanufacture(request.company.id)
    else:
        manufactureres=PumpManufacturer.objects.filter(user_id=request.user.id)
        
    surface_names= SurfaceNameModels.objects.all()
    surface_count = SurfacePipe.objects.filter(well_id=pk,status=1).count()
    mudpump_count = MudPump.objects.filter(well_id=pk,status=1).count()
    rig_count = Rig.objects.filter(well_id=pk,status=1).count()
    countries=getcountries(request.company)
    data={
        'rig_count':rig_count,
        'rig_data':rig_data,
        'surface_names':surface_names,
        'surface_count':surface_count,
        'mudpump_count':mudpump_count,
        'well_id':pk,
        'surfacepipedata':surfacepipedata,
        'form':form,
        'mud':mud,
        'unit':unit,
        'row':row,
        "colum":colum,
        'manufactureres':manufactureres,
        'mud_form':mud_form,
        'well':well,
        'countries':countries,
        'company':request.company
    }
    return render(request, template_name, data)