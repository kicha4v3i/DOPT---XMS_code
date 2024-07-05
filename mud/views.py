from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mud.models import MudPump,MudPumpData,PumpManufacturer,Pumps,MudPumpMasterData,MudPumpMasterSpeed,MudPumpMasterFlowRate,MudPumpFlowRate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MudPumpForm,MudPumpFlowRateForm,MudPumpDataForm,MudPumpSpeed,PumpManufacturerForm,PumpsForm
from django.views.generic import ListView, DetailView
from django.forms import formset_factory
from django.core import serializers
from django.http import JsonResponse,HttpResponse
import json 
from wells.models import Wells
from .serializers import PumpsSerializer
from custom_auth.models import User
from math import pi
from custom_auth.getunit import adduserlog

# Create your views here.
def details(request,well_id):
    try:
        mud=MudPump.objects.get(company=request.company,well=well_id)
    except MudPump.DoesNotExist:
        mud = None
    if(mud is None):
        return redirect('mud:create',well_id=well_id)

    return render(request,'mud/view.html',{'mud': mud,'well_id':well_id})


def create(request,well_id):
    if request.method == 'POST':
        form = MudPumpForm(request.POST)
        if form.is_valid():
            mud_pump=form.save()
            mud_pump.company=request.company
            mud_pump.save()
            linear_size=request.POST.getlist('linear_size')
            max_discharge_pressure=request.POST.getlist('max_discharge_pressure')
            i = 0
            while i < len(linear_size):
                if(linear_size[i]):     
                    MudPumpData.objects.create(linear_size=linear_size[i],well=mud_pump.well,max_discharge_pressure=max_discharge_pressure[i],company=request.company,mud_pump=mud_pump)
                i += 1
            i = 0
            pump_speed=request.POST.getlist('pump_speed')
            flowrate=request.POST.getlist('flowrate')
            print(type(flowrate))
            print(pump_speed)
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
            source_id=mud_pump.id
            userlog=adduserlog('Mud Pump Created',request,source_id,'Mud Pump',request.user.licence_type,request)
            return redirect('mud:detail', well_id=well_id)
        else:
            print(form.errors)
    form = MudPumpForm()
    manufactureres=PumpManufacturer.objects.all()
    well=Wells.objects.get(id=well_id)
    row=[]
    colum=[]
    for i in range(5):
        row.append(i)
    for i in range(4):
        colum.append(i)
    return render(request,'mud/create.html',{'form': form,'well_id':well_id,'well':well,'manufactureres':manufactureres,'row':row,"colum":colum})


def edit(request, pk):
    mud = get_object_or_404(MudPump, pk=pk)
    form = MudPumpForm(request.POST or None, instance=mud)
    wellid=MudPump.objects.filter(id=pk).values('well_id')
    well_id=wellid[0]['well_id']
    well=Wells.objects.get(id=well_id)
    unit=well.project.unit
   
    if form.is_valid():
        mud_pump=form.save()
        mud_pump.company=request.company
        mud_pump.save()
        MudPumpData.objects.filter(mud_pump=mud_pump).delete()
        MudPumpSpeed.objects.filter(mud_pump=mud_pump).delete()
        linear_size=request.POST.getlist('linear_size')
        max_discharge_pressure=request.POST.getlist('max_discharge_pressure')
        i = 0
        while i < len(linear_size):
            if(linear_size[i]):     
                MudPumpData.objects.create(linear_size=linear_size[i],well=mud_pump.well,max_discharge_pressure=max_discharge_pressure[i],company=request.company,mud_pump=mud_pump)
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
                        MudPumpFlowRate.objects.create(flowrate=flowraterow[j],company=request.company,well=mud_pump.well,mud_pump_speed=mud_pump_speed)
                        j += 1
            i += 1
        source_id=mud_pump.id
        userlog=adduserlog('Mud Pump Edited',request,source_id,'Mud Pump',request.user.licence_type,request)
        return redirect('mud:detail', well_id=mud.well_id)
    else:
        print(form)

    return render(request, 'mud/edit.html', {'form':form,'mud':mud,'unit':unit,'well_id':well_id})


def delete(request, pk):
    mud = get_object_or_404(MudPump, pk=pk)
    well_id=mud.well_id
    source_id=mud.id
    mud.delete()
    userlog=adduserlog('Mud Pump Deleted',request,source_id,'Mud Pump',request.user.licence_type,request)
    return redirect('mud:detail', well_id=well_id)

def manufacturerdelete(request, pk):
    manufacturer = get_object_or_404(PumpManufacturer, pk=pk)
    manufacturer.delete()
    return redirect('mud:manufacturerindex')
    
def pumpdelete(request, pk):  
    pump = get_object_or_404(Pumps, pk=pk)
    source_id=pump.id
    adduserlog('mudpump master deleted',request,source_id,'mudpumpmaster',request.user.licence_type,None,None)
    pump.delete()
    return redirect('mud:pumpindex')

def manufacturerindex(request):
    request.session['mainmenu']  = 'masters'
    manufactureres=PumpManufacturer.objects.filter(company=request.company)
    staticmanufactureres=PumpManufacturer.objects.filter(is_superadmin=1)
    return render(request, "master/manufacturerindex.html", {'manufactureres':manufactureres,'staticmanufactureres':staticmanufactureres,'request':request})

def manufacturercreate(request):
    if request.method == 'POST':
        form = PumpManufacturerForm(request.POST)
        if form.is_valid():
            pump=form.save()
            pump.company=request.company
            pump.user_id=request.user.id
            form.save()
            return redirect('mud:manufacturerindex')
    form = PumpManufacturerForm()
    if(request.user.licence_type != 'Individual'):
        form.fields['company'].initial = request.company.id
    return render(request,'master/manufacturerform.html',{'form': form})


def manufactureredit(request, pk, template_name='master/manufacturerform.html'):
    manufacturer = get_object_or_404(PumpManufacturer, pk=pk)
    form = PumpManufacturerForm(request.POST or None, instance=manufacturer)
    if form.is_valid():
        manufacture=form.save()
        manufacture.company=request.company
        manufacture.save()
        return redirect('mud:manufacturerindex')
    return render(request, template_name, {'form':form})

def pumpindex(request):
    if(request.user.licence_type != 'Individual'):
        pumps=Pumps.objects.filter(company=request.company)
    else:
        pumps=Pumps.objects.getindividuals_pump(request.user.id)

    request.session['master']='pumps'
    staticpumps=Pumps.objects.filter(is_superadmin=1)
    user_rights_companyid = request.user.company_id
    user = User.objects.getuserid(request.user.id)
    user_rights_groups = user.groups.all().first()
    return render(request, "master/pumpindex.html",
     {'pumps':pumps,
     'staticpumps':staticpumps,
     'user_rights_companyid':user_rights_companyid,
     'user_rights_groups':user_rights_groups,

     })

def pumpcreate(request):
    if(request.user.licence_type != 'Individual'):
        pumpmanufacture = PumpManufacturer.objects.getallpumpmanufacture(request.company.id)
    else:
        pumpmanufacture = PumpManufacturer.objects.get_individual_pumpmanufacture(request.user.id)

    if request.method == 'POST':
        form = PumpsForm(request.POST)
        form.fields["pump_manufacturer"].queryset =PumpManufacturer.objects.filter(company=request.company)
        if(request.user.licence_type != 'Individual'):
            form.fields['company'].initial = request.company.id

        if form.is_valid():
            mud_pump_master=form.save()
            mud_pump_master.company=request.company
            mud_pump_master.user_id=request.user.id
            mud_pump_master.save()
            linear_size=request.POST.getlist('linear_size')
            max_discharge_pressure=request.POST.getlist('max_discharge_pressure')
            i = 0
            while i < len(linear_size):
                if(linear_size[i]):     
                    MudPumpMasterData.objects.create(linear_size=linear_size[i],max_discharge_pressure=max_discharge_pressure[i],company=request.company,mud_pump_master=mud_pump_master)
                i += 1
            i = 0
            pump_speed=request.POST.getlist('pump_speed')
            flowrate=request.POST.getlist('flowrate')
            

            while i < len(pump_speed):
                if(pump_speed[i]):     
                    mud_pump_master_speed=MudPumpMasterSpeed.objects.create(pump_speed=pump_speed[i],company=request.company,mud_pump_master=mud_pump_master)
                    flowraterow = flowrate[i*len(linear_size):len(linear_size)+(i*len(linear_size))] 
                    
                    j=0
                    while j < len(flowraterow):
                        if(flowraterow[j]): 
                            MudPumpMasterFlowRate.objects.create(flowrate=flowraterow[j],company=request.company,mud_pump_master_speed=mud_pump_master_speed)
                            j += 1
                i += 1
            adduserlog('mudpump master created',request,mud_pump_master.id,'mudpumpmaster',request.user.licence_type,None,None,None)
            return redirect('mud:pumpindex')
        else:
            print('error')
    form = PumpsForm()
    form.fields["pump_manufacturer"].queryset =PumpManufacturer.objects.filter(company=request.company)
    # form.fields['company'].initial = request.company.id
    row=[]
    colum=[]
    for i in range(5):
        row.append(i)
    for i in range(4):
        colum.append(i)
    # userlog=adduserlog('pumpcreate',request,source_id,'form')    
    return render(request,'master/pumpform.html',{'form': form, 'pumpmanufacture':pumpmanufacture,'row':row,"colum":colum})


def pumpedit(request, pk, template_name='master/pumpedit.html'):
    pump = get_object_or_404(Pumps, pk=pk)
    form = PumpsForm(request.POST or None, instance=pump)
    if form.is_valid():
        mud_pump_master=form.save()
        mud_pump_master.company=request.company
        mud_pump_master.save()
        MudPumpMasterData.objects.filter(mud_pump_master=mud_pump_master).delete()
        MudPumpMasterSpeed.objects.filter(mud_pump_master=mud_pump_master).delete()
        linear_size=request.POST.getlist('linear_size')
        max_discharge_pressure=request.POST.getlist('max_discharge_pressure')
        i = 0
        while i < len(linear_size):
            if(linear_size[i]):     
                MudPumpMasterData.objects.create(linear_size=linear_size[i],max_discharge_pressure=max_discharge_pressure[i],company=request.company,mud_pump_master=mud_pump_master)
            i += 1
        i = 0
        pump_speed=request.POST.getlist('pump_speed')
        flowrate=request.POST.getlist('flowrate')

        while i < len(pump_speed):
            if(pump_speed[i]):     
                mud_pump_master_speed=MudPumpMasterSpeed.objects.create(pump_speed=pump_speed[i],company=request.company,mud_pump_master=mud_pump_master)
                flowraterow = flowrate[i*len(linear_size):len(linear_size)+(i*len(linear_size))]
                j=0
                while j < len(flowraterow):
                    if(flowraterow[j]): 
                        MudPumpMasterFlowRate.objects.create(flowrate=flowraterow[j],company=request.company,mud_pump_master_speed=mud_pump_master_speed)
                        j += 1
            i += 1
        Pumpedit=mud_pump_master.id 
        adduserlog('mudpump master edited',request,Pumpedit,'mudpumpmaster',request.user.licence_type,None,None)
        return redirect('mud:pumpindex')
    pumpmanufacture = PumpManufacturer.objects.filter(company=request.company)   
    return render(request, template_name, {'form':form,'pump':pump,'pumpmanufacture':pumpmanufacture})

def pumpview(request, pk):
    pump=Pumps.objects.get(pk=pk)
    return render(request, 'master/pumpview.html', {'pump':pump})

def getpumps(request):
    pump_manufacturer_id = request.GET['pump_manufacturer_id']
    pumps=Pumps.objects.filter(pump_manufacturer_id=pump_manufacturer_id)
    data = serializers.serialize('json', pumps)
    return JsonResponse(data, safe=False)

def getpump(request):
    id = request.GET['id']
    pump=Pumps.objects.filter(id=id)
    unit=Pumps.objects.filter(id=id).values('unit')
    current_unit=unit[0]['unit']
    datas = PumpsSerializer(pump, many=True).data
    data={
        'datas':datas,
        'current_unit':current_unit
    }
    return JsonResponse(data, safe=False)

    # data = serializers.serialize('json', pump)
    # return JsonResponse(data, safe=False) 

def adminmanufacturerindex(request):
    manufactureres=PumpManufacturer.objects.filter(is_superadmin=1)
    return render(request, "adminmaster/manufacturerindex.html", {'manufactureres':manufactureres})

def adminmanufacturercreate(request):
    if request.method == 'POST':
        form = PumpManufacturerForm(request.POST)
        if form.is_valid():
            adminmanufacturer=form.save()
            adminmanufacturer.is_superadmin=1
            adminmanufacturer.save()
            userlog=adduserlog('Manufacture Created',request,adminmanufacturer.id,'adminmanufacturer',None,None,None,None)
            return redirect('mud:adminmanufacturerindex')
    form = PumpManufacturerForm()
    return render(request,'adminmaster/manufacturerform.html',{'form': form})


def adminmanufactureredit(request, pk, template_name='adminmaster/manufacturedit.html'):
    manufacturer = get_object_or_404(PumpManufacturer, pk=pk)
    form = PumpManufacturerForm(request.POST or None, instance=manufacturer)
    if form.is_valid():
        adminmanufacturer = form.save()
        userlog=adduserlog('Manufacture Edited',request,adminmanufacturer.id,'adminmanufacturer',None,None,None)
        return redirect('mud:adminmanufacturerindex')
    return render(request, template_name, {'form':form})


def adminmanufacturerdelete(request, pk):
    manufacturer = get_object_or_404(PumpManufacturer, pk=pk)
    userlog=adduserlog('Manufacture Deleted',request,manufacturer.id,'adminmanufacturer',None,None,None)
    manufacturer.delete()
    return redirect('mud:adminmanufacturerindex')


def adminpumpindex(request):
    pumps=Pumps.objects.filter(is_superadmin=1)
    request.session['master']='pumps'
    return render(request, "adminmaster/pumpindex.html", {'pumps':pumps})


def adminpumpcreate(request):
    pumpmanufacture = PumpManufacturer.objects.filter(is_superadmin=1)
    if request.method == 'POST':
        form = PumpsForm(request.POST)
        form.fields["pump_manufacturer"].queryset =PumpManufacturer.objects.filter(is_superadmin=1)

        if form.is_valid():
            print('vvvvvvvv')
            mud_pump_master=form.save()
            print(request.POST)
            linear_size=request.POST.getlist('linear_size')
            max_discharge_pressure=request.POST.getlist('max_discharge_pressure')
            i = 0 ; 
            # pumpmasterdata_ids = []
            while i < len(linear_size):
                if(linear_size[i]):     
                    pumpmasterdata = MudPumpMasterData.objects.create(linear_size=linear_size[i],max_discharge_pressure=max_discharge_pressure[i],is_superadmin=1,mud_pump_master=mud_pump_master)
                    # pumpmasterdata_ids.append(pumpmasterdata.id)
                i += 1 
            # userlog=adduserlog('Mudpump created',request,pumpmasterdata_ids,'adminmudpump',None,None,None)
            i = 0
            pump_speed=request.POST.getlist('pump_speed')
            flowrate=request.POST.getlist('flowrate')
            pump_speed_ids = []
            while i < len(pump_speed):
                if(pump_speed[i]):     
                    mud_pump_master_speed=MudPumpMasterSpeed.objects.create(pump_speed=pump_speed[i],is_superadmin=1,mud_pump_master=mud_pump_master)
                    flowraterow = flowrate[i*len(linear_size):len(linear_size)+(i*len(linear_size))]
                    pump_speed_ids.append(mud_pump_master_speed.id)
                    j=0
                    while j < len(flowraterow):
                        if(flowraterow[j]): 
                            MudPumpMasterFlowRate.objects.create(flowrate=flowraterow[j],is_superadmin=1,mud_pump_master_speed=mud_pump_master_speed)
                            j += 1
                i += 1
            userlog=adduserlog('Pumps created',request,pump_speed_ids,'adminpumpspeed',None,None,None,None)
            superadmin=form.save()
            superadmin.is_superadmin=1
            superadmin.save()
            return redirect('mud:adminpumpindex')
    form = PumpsForm()
    form.fields["pump_manufacturer"].queryset =PumpManufacturer.objects.filter(is_superadmin=1)
    # form.fields['company'].initial = request.company.id
    row=[]
    colum=[]
    for i in range(5):
        row.append(i)
    for i in range(4):
        colum.append(i)
    return render(request,'adminmaster/pumpform.html',{'form': form,'pumpmanufacture':pumpmanufacture,'row':row,'colum':colum})


def adminpumpview(request, pk):
    pump=Pumps.objects.get(pk=pk)
    return render(request, 'adminmaster/pumpview.html', {'pump':pump})


def adminpumpedit(request, pk, template_name='adminmaster/pumpedit.html'):
    pump = get_object_or_404(Pumps, pk=pk)
    form = PumpsForm(request.POST or None, instance=pump)
    pumpmanufacture = PumpManufacturer.objects.filter(is_superadmin=1)
    if form.is_valid():
        mud_pump_master=form.save()
        MudPumpMasterData.objects.filter(mud_pump_master=mud_pump_master).delete()
        MudPumpMasterSpeed.objects.filter(mud_pump_master=mud_pump_master).delete()
        linear_size=request.POST.getlist('linear_size')
        max_discharge_pressure=request.POST.getlist('max_discharge_pressure')
        i = 0
        while i < len(linear_size):
            if(linear_size[i]):     
                MudPumpMasterData.objects.create(linear_size=linear_size[i],max_discharge_pressure=max_discharge_pressure[i],is_superadmin=1,mud_pump_master=mud_pump_master)
            i += 1
        i = 0
        pump_speed=request.POST.getlist('pump_speed')
        flowrate=request.POST.getlist('flowrate')
        pump_speed_ids = []
        while i < len(pump_speed):
            if(pump_speed[i]):     
                mud_pump_master_speed=MudPumpMasterSpeed.objects.create(pump_speed=pump_speed[i],is_superadmin=1,mud_pump_master=mud_pump_master)
                flowraterow = flowrate[i*len(linear_size):len(linear_size)+(i*len(linear_size))] 
                pump_speed_ids.append(mud_pump_master_speed.id)
                j=0
                while j < len(flowraterow):
                    if(flowraterow[j]): 
                        MudPumpMasterFlowRate.objects.create(flowrate=flowraterow[j],is_superadmin=1,mud_pump_master_speed=mud_pump_master_speed)
                        j += 1
            i += 1 
        userlog=adduserlog('Pumps Edited',request,pump_speed_ids,'adminpumpspeed',None,None,None)
        return redirect('mud:adminpumpindex')
    return render(request, template_name, {'form':form,'pump':pump,'pumpmanufacture':pumpmanufacture})


def adminpumpdelete(request, pk):
    print('pumpdel')
    pump = get_object_or_404(Pumps, pk=pk)
    userlog=adduserlog('Pumps Delete',request,pump.id,'adminpump',None,None,None)
    pump.delete()
    return redirect('mud:adminpumpindex')


def flowratecalculation(request):
    length = request.GET['length']
    linear_size = request.GET['linear_size']
    pump_speed = request.GET['pump_speed']
    pump_type = request.GET['type']
    pump_unit = request.GET['unit']
    
    if(pump_type == 'Triplex' and pump_unit == 'API'):
        flowrate_values = round((pi/4 * float(linear_size) ** 2 * float(length) * float(pump_speed) / 12 ** 3*7.48*3))
    elif(pump_type == 'Triplex' and pump_unit == 'SI'):
        flowrate_values = round((pi/4 * float(linear_size) ** 2 * float(length) * float(pump_speed) * 3/1000000))
    elif(pump_type == 'Duplex' and pump_unit == 'API'):
        flowrate_values = round((pi/4 * (2 * float(linear_size) ** 2 - float(length) ** 2) * float(pump_speed) / 12 ** 3*7.48*2))
    elif(pump_type == 'Duplex' and pump_unit == 'SI'):
        flowrate_values = round((pi/4 * (2 * float(linear_size) ** 2 - float(length) ** 2) * float(pump_speed) * 2/1000000))
 #   data = serializers.serialize('json', flowrate)
    return JsonResponse(flowrate_values, safe=False)

