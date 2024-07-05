from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from drillbitdata.models import DrillBit,DrillBitNozzle,BitTypesNames
from drillbitdata.forms import DrillBitForm,DrillBitNozzleForm,DrillBitNozzleFormset
from wells.models import Wells,WellUsers,CoordinateSystems,Projections
from django.views.generic import ListView, DetailView
from wellphases.models import WellPhases
from math import pi,sqrt
from custom_auth.getunit import adduserlog,getprojectunit,getcountries
from bhadata.models import BhaData,BhaElement,Drillcollers,Drillpipe,DrillpipeHWDP,Specifications,Pressuredroptool,Empirical,Differential_pressure
from helpers import *
from django.contrib import messages

def create(request,wellphase_id):
    well_id=request.session['well_id']
    request.session['submenu']='drillbit'
    request.session['wellphasetab']=wellphase_id
    drillbitnozzleformset=DrillBitNozzleFormset(prefix="nozzles")
    well = Wells.objects.get(id=well_id)
    unit=getprojectunit(well_id)
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    welltype = well.well_type
    if request.method == 'POST':
        drillbit_id = []
        if(request.session['welltype']=='PLAN'):
            form = DrillBitForm(request.POST)
            if form.is_valid():
                drillbit=form.save()
                drillbit.company=request.company
                drillbit.well_phases_id=wellphase_id
                external_nozzle=request.POST.get('external_nozzle')
                drillbit.external_nozzle=external_nozzle
                drillbit.save()
                no_of_nozzle = drillbit.no_of_nozzle
                i=0 
                while(i < no_of_nozzle):
                    nozzle_size=request.POST.get('nozzles-'+str(i)+'-nozzle_size')
                    DrillBitNozzle.objects.create(company_id=drillbit.company_id,drillbit_id=drillbit.id,well_id=drillbit.well_id,status=1,nozzle_size=nozzle_size)
                    i+=1
      
        else:
            # date=request.POST.getlist('date')
            # time=request.POST.getlist('time')
            serial_no=request.POST.getlist('serial_no')
            bit_type=request.POST.getlist('bit_type')
            bhaname=request.POST.getlist('bhaname')
            no_of_nozzle=request.POST.getlist('no_of_nozzle')
            tfa=request.POST.getlist('tfa')
            manufacture=request.POST.getlist('manufacture')
            bit_type=request.POST.getlist('bit_type')
            idac_code=request.POST.getlist('idac_code')

            i=0
            while i < len(serial_no):   
                if(serial_no[i]):
                    # timestamp=dateconversion(date[i],time[i])
                    drillbit=DrillBit.objects.create(no_of_nozzle=no_of_nozzle[i],tfa=tfa[i],manufacture=manufacture[i],bit_type_id=bit_type[i],company=request.company,well_id=well_id,well_phases_id=wellphase_id,bha_id=bhaname[i],serial_no=serial_no[i],idac_code=idac_code[i])
                    
                    nozzle_size=request.POST.getlist('nozzle_size'+str(i))
                    j=0
                    while j < len(nozzle_size): 
                        drillbitnozzle = DrillBitNozzle.objects.create(nozzle_size=nozzle_size[j],company=request.company,drillbit=drillbit,well_id=well_id)
                        drillbit_id.append(drillbitnozzle.id)
                        j +=1
                i += 1
        source_id=drillbit_id
        userlog=adduserlog('Drillbit Created',request,source_id,'Drillbit',request.user.licence_type,well.project_id,well_id,wellphase_id,'create')  
        return redirect('drillbitdata:drillbitlist', wellphase_id=wellphase_id)
    form = DrillBitForm()
    bit_types=BitTypesNames.objects.all()
    # drillbitnozzle = DrillBitNozzle.objects.all()
    bhadata=BhaData.objects.filter(well_phases_id=wellphase_id,status=1)
    if(request.session['welltype']=='PLAN'):
        return render(request,'drillbitdata/create.html',{'form': form,'well_id':well_id,'unit':unit,'bit_types':bit_types,'welltype':welltype,'wellphases':wellphase,'drillbitnozzleformset':drillbitnozzleformset,'countries':getcountries(request.company),'company':request.company,'wellphase_id':wellphase_id,'well':well})
    else:
        print("vdgg")
        return render(request,'drillbitdata/create_actual.html',{'form': form,'well_id':well_id,'unit':unit,'bit_types':bit_types,'welltype':welltype,'wellphases':wellphase,'drillbitnozzleformset':drillbitnozzleformset,'countries':getcountries(request.company),'company':request.company,'wellphase_id':wellphase_id,'well':well,'bhadata':bhadata})


def createold(request,well_id):
    well = Wells.objects.get(id=well_id)
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company)
    welltype = well.well_type
    if request.method == 'POST':
        form = DrillBitForm(request.POST)
        if form.is_valid():
            drillbit=form.save()
            drillbit.company=request.company
            drillbit.save()
            nozzle_size=request.POST.getlist('nozzle_size')
            # drillbit=request.POST.getlist('bit_type')
            i = 0
            while i < len(nozzle_size):
                if(nozzle_size[i]):
                    DrillBitNozzle.objects.create(nozzle_size=nozzle_size[i],drillbit=drillbit,well_id=well_id,company=request.company)
                i += 1
                
            return redirect('drillbitdata:drillbitlist', well_id=well_id)
    form = DrillBitForm()
    bit_types=BitTypesNames.objects.all()
    # drillbitnozzle = DrillBitNozzle.objects.all()
    return render(request,'drillbitdata/create.html',{'form': form,'well_id':well_id,'bit_types':bit_types,'welltype':welltype,'wellphase':wellphase})

def details(request,pk):
    drillbits=DrillBit.objects.get(pk=pk)
    wellphase_id=request.GET['wellphase']
    request.session['wellphasetab']=int(wellphase_id)
    request.session['submenu']='drillbit'
    drillbitnozzle=DrillBitNozzle.objects.filter(drillbit=drillbits)
    well_id=drillbits.well_id
    well = Wells.objects.get(id=well_id)
    welltype = well.well_type
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    return render(request,'drillbitdata/view.html',{'drillbits': drillbits,'drillbitnozzle':drillbitnozzle,'welltype':welltype,'wellphase_id':int(wellphase_id),'wellphases':wellphase,'well_id':well_id,'countries':getcountries(request.company),'company':request.company,'well':well,'project_id':well.project_id,'user_id':request.user,'module_id':4})

def drillbitlist(request,wellphase_id):
    well_id=request.session['well_id']
    welltype=request.session['welltype']
    request.session['wellphasetab']=wellphase_id
    drillbits=DrillBit.objects.filter(company=request.company,well_id=well_id,well_phases_id=wellphase_id,status=1)
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    request.session['submenu']='drillbit'
    well = Wells.objects.get(id=well_id)
    welltype = well.well_type
    if(len(drillbits) == 0):
        checkpermission=user_rights_permission('Create Data',request)
        if(checkpermission != True):
            messages.error(request,'No Access to create!')
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('drillbitdata:create',wellphase_id=wellphase_id)
    
    checkpermission=user_rights_permission('View Data',request)
    if(checkpermission != True):
        messages.error(request,'No Access to view!')
        return redirect(request.META.get('HTTP_REFERER'))
    
    if(welltype=='PLAN'):
        return render(request,'drillbitdata/list.html',{'drillbits': drillbits,'well_id':well_id,'welltype':welltype,'wellphases':wellphase,'wellphase_id':wellphase_id,'countries':getcountries(request.company),'company':request.company,'well':well,'project_id':well.project_id,'user_id':request.user,'module_id':5})
    else:
        return render(request,'drillbitdata/list_actual.html',{'drillbits': drillbits,'well_id':well_id,'welltype':welltype,'wellphases':wellphase,'wellphase_id':wellphase_id,'countries':getcountries(request.company),'company':request.company,'well':well,'project_id':well.project_id,'user_id':request.user.id,'module_id':4})
    # bhadata=DrillBit.objects.get(well_id=well_id)
    # ids=bhadata.id
    # return redirect('drillbitdata:detail',pk=ids)

    
    
def edit(request, pk, template_name='drillbitdata/edit.html'):
    wellphase_id=request.GET['wellphase']
    request.session['wellphasetab']=int(wellphase_id)
    request.session['submenu']='drillbit'
    drillbit = get_object_or_404(DrillBit, pk=pk)
    form = DrillBitForm(request.POST or None, instance=drillbit)
    drillbitnozzle = DrillBitNozzle.objects.filter(drillbit=pk)
    well_id=drillbit.well_id
    unit=getprojectunit(well_id)
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    well = Wells.objects.get(id=well_id)
    welltype = well.well_type
    if form.is_valid():
        drillbit=form.save()
        drillbit.company=request.company
        drillbit.well_phases_id=wellphase_id
        external_nozzle=request.POST.get('external_nozzle')
        drillbit.external_nozzle=external_nozzle
        drillbit.save()
        DrillBitNozzle.objects.filter(drillbit=pk).delete()
        nozzle_size=request.POST.getlist('nozzle_size')
        i = 0
        drillbit_id = []
        while i < len(nozzle_size):
            if(nozzle_size[i]):
                drillbitnozzle = DrillBitNozzle.objects.create(nozzle_size=nozzle_size[i],drillbit=drillbit,well_id=well_id,company=request.company)
                drillbit_id.append(drillbitnozzle.id)
            i += 1 
        source_id=drillbit_id
        userlog=adduserlog('Drillbit Edited',request,source_id,'Drillbit',request.user.licence_type,well.project_id,well_id,wellphase_id,'edit')  
        return redirect('drillbitdata:drillbitlist', wellphase_id=wellphase_id)
    bit_types=BitTypesNames.objects.all()
    return render(request, template_name, {'form':form,'bit_types':bit_types,'drillbitnozzle':drillbitnozzle,'welltype':welltype,'wellphases':wellphase,'wellphase_id':int(wellphase_id),'well_id':well_id,'unit':unit,'countries':getcountries(request.company),'company':request.company,'well':well})

def delete(request, pk, template_name='crudapp/confirm_delete.html'):
    drillbit = get_object_or_404(DrillBit, pk=pk)
    nozzle_ids = list(DrillBitNozzle.objects.filter(drillbit_id=pk).values_list('id', flat=True))
    well_id=drillbit.well_id
    wellphase_id=drillbit.well_phases_id
    source_id=nozzle_ids 
    well = Wells.objects.get(id=well_id)
    userlog=adduserlog('Drillbit Deleted',request,source_id,'Drillbit',request.user.licence_type,well.project_id,well_id,wellphase_id,'delete')
 
    drillbit.delete()
    return redirect('drillbitdata:drillbitlist', wellphase_id=wellphase_id)

def edit_actual(request,wellphase_id,template_name='drillbitdata/edit_actual.html'):
    well_id=request.session['well_id']
    drillbits=DrillBit.objects.filter(company=request.company,well_id=well_id,well_phases_id=wellphase_id,status=1)
    well = Wells.objects.get(id=well_id)
    welltype = well.well_type
    bit_types=BitTypesNames.objects.all()
    bhadata=BhaData.objects.filter(well_phases_id=wellphase_id)
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    unit=getprojectunit(well_id)
    if request.method == 'POST':
        # date=request.POST.getlist('date')
        # time=request.POST.getlist('time')
        serial_no=request.POST.getlist('serial_no')
        bit_type=request.POST.getlist('bit_type')
        bhaname=request.POST.getlist('bhaname')
        manufacture=request.POST.getlist('manufacture')
        idac_code=request.POST.getlist('idac_code')
        tfa=request.POST.getlist('tfa')
        no_of_nozzle=request.POST.getlist('no_of_nozzle')
        drill_id=request.POST.getlist('drill_id')
        current_drill_id=[]
        i=0
        while i < len(serial_no): 
            if(serial_no[i]):
                # timestamp=dateconversion(date[i],time[i])
                if(drill_id[i]):
                    drillbit=DrillBit.objects.filter(id=drill_id[i]).update(no_of_nozzle=no_of_nozzle[i],tfa=tfa[i],manufacture=manufacture[i],bit_type_id=bit_type[i],company=request.company,well_id=well_id,well_phases_id=wellphase_id,bha_id=bhaname[i],serial_no=serial_no[i],idac_code=idac_code[i])
                    current_drill_id.append(drill_id[i])
                    DrillBitNozzle.objects.filter(drillbit=drill_id[i]).delete()
                    nozzle_size=request.POST.getlist('nozzle_size'+str(i))
                    j = 0
                    while j < len(nozzle_size):
                        DrillBitNozzle.objects.create(nozzle_size=nozzle_size[j],drillbit_id=drill_id[i],well_id=well_id,company=request.company)
                        j += 1
                else:
                    drillbit=DrillBit.objects.create(no_of_nozzle=no_of_nozzle[i],tfa=tfa[i],manufacture=manufacture[i],bit_type_id=bit_type[i],company=request.company,well_id=well_id,well_phases_id=wellphase_id,bha_id=bhaname[i],serial_no=serial_no[i],idac_code=idac_code[i])
                    drillid=DrillBit.objects.values('id').last()
                    current_drill_id.append(drillid['id'])                  
                    j = 0
                    while j < len(nozzle_size):
                        DrillBitNozzle.objects.create(nozzle_size=nozzle_size[j],drillbit=drillbit,well_id=well_id,company=request.company)
                        j += 1
                    
            i += 1
        DrillBit.objects.filter(well_id=well_id).exclude(id__in=current_drill_id).update(status=0)
        return redirect('drillbitdata:drillbitlist', wellphase_id=wellphase_id)
   

    return render(request, template_name,{'unit':unit,'drillbits':drillbits,'wellphase_id':wellphase_id,'well_id':well_id,'bit_types':bit_types,'bhadata':bhadata,'wellphases':wellphase})

def delete_actual(request, wellphase_id, template_name='crudapp/confirm_delete.html'):
    well_id=request.session['well_id']
    drillbit=DrillBit.objects.filter(company=request.company,well_id=well_id,well_phases_id=wellphase_id,status=1)
    drillbit.update(status=0)
    return redirect('drillbitdata:drillbitlist', wellphase_id=wellphase_id)