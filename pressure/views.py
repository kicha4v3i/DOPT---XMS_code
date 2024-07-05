from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pressure.models import Pressure
from django.shortcuts import render, redirect, get_object_or_404
from muddata.models import MudData,Rheogram,RheogramNameModels,RheogramDate,MudType,Sections,RheogramSections
from django.views.generic import ListView, DetailView
from wells.models import Wells
from .forms import PressureForm
from django.http import HttpResponse
from tablib import Dataset
from django.contrib import messages
import openpyxl
import csv
from django.utils.encoding import smart_str
import pandas as pd
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse,HttpResponse
import numpy as np
from custom_auth.getunit import getmd
from welltrajectory.models import WellTrajectory
from math import tan, pi, acos,sin,cos,sqrt
from custom_auth.getunit import adduserlog,getcountries
from helpers import *
from custom_auth.getunit import getprojidbywellid
from helpers.commonimport import xlsxwriter,io

def details(request,well_id):
    pressure=Pressure.objects.filter(company=request.company,well=well_id,status=1)
    request.session['submenu']='pressure'
    well=Wells.objects.get(id=well_id) 
    if(len(pressure) == 0):
        checkpermission=user_rights_permission('Create Data',request)
        if(checkpermission != True):
            messages.error(request,'No Access to create!')
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('pressure:create',well_id=well_id)

# Chart
    labels = []
    data = []
    data1=[]
    newdata =[]
    newdata1=[]
    ig_unit=None
    # queryset = Pressure.objects.order_by('true_vertical_depth')
    pore_pressure=[]
    true_vertical_depth=[]
    fracture_pressure=[]
    # print(pressure)
    for val in pressure:
        ig_unit=val.pressure_unit
        s1 = pd.Series(val.pore_pressure)
        s = pd.Series([0, 1, np.nan, 3])
        pore_pressure.append(val.pore_pressure)
        true_vertical_depth.append(val.true_vertical_depth)
        fracture_pressure.append(val.fracture_pressure)
        # if(val.pore_pressure and val.fracture_pressure):
           
        #     data = {'x':val.pore_pressure ,'y':val.true_vertical_depth}
        #     data1 = {'x':val.fracture_pressure ,'y':val.true_vertical_depth}
        #     labels.append(val.true_vertical_depth)
           
        #     newdata.append(data)
        #     newdata1.append(data1)
    # print(pore_pressure)
    pore_series = pd.Series(pore_pressure)
    pore_interploate=pore_series.interpolate()
    
    tvd_series = pd.Series(true_vertical_depth)
    tvd_interploate=tvd_series.interpolate()

    fracture_series = pd.Series(fracture_pressure)
    fracture_interploate=fracture_series.interpolate()

    for i in range(len(fracture_interploate)):
        data = {'x': tvd_interploate[i],'y':pore_interploate[i]}
        data1 = {'x':tvd_interploate[i] ,'y':fracture_interploate[i]}
        labels.append(tvd_interploate[i])
        newdata.append(data)
        newdata1.append(data1)

    og_unit=request.GET.get('unit', ig_unit)   
    checkpermission=user_rights_permission_projects('View Data',request,'well',well_id)

    if(checkpermission != True):
        messages.error(request,'No Access to view!')
        return redirect(request.META.get('HTTP_REFERER'))     
    return render(request,'pressure/view.html',{'pressure': pressure,'well_id':well_id,'labels': labels,'newdata':newdata,'newdata1':newdata1,'og_unit':og_unit,'countries':getcountries(request.company),'company':request.company,'well':well,'user_id':request.user,'project_id':well.project_id,'module_id':5})


def getinterpolatedata(request):
    pressure=Pressure.objects.filter(company=request.company,well=request.POST['well_id'],status=1)
    labels = []
    data = []
    data1=[]
    newdata =[]
    newdata1=[]
    pore_pressure=[]
    true_vertical_depth=[]
    muddatamd=[]
    mudweight=[]
    mudtvd=[]

    ig_unit=None
    muddata=MudData.objects.filter(well_id=request.POST['well_id'],status=1).order_by('todepth')
    i=0
    while(i<len(muddata)):
        if(i==0):
            muddatamd.append(muddata[i].from_depth)
            muddatamd.append(muddata[i].todepth)
            md=getmd(request,muddata[i].from_depth)
            mudtvd.append(md)
            if(request.POST['pressureunit']=="psi"):
                weight=0.052 * muddata[i].mud_weight * md 
                mudweight.append(weight)
            else:
                mudweight.append(muddata[i].mud_weight)
            md=getmd(request,muddata[i].todepth)
            mudtvd.append(md)
            if(request.POST['pressureunit']=="psi"):
                weight=0.052 * muddata[i].mud_weight * md
                mudweight.append(weight)
            else:
                mudweight.append(muddata[i].mud_weight)
        else:
            muddatamd.append(muddata[i].todepth)
            md=getmd(request,muddata[i].todepth)
            if(request.POST['pressureunit']=="psi"):
                weight=0.052 * muddata[i].mud_weight * md
                mudweight.append(weight)
            else:
                mudweight.append(muddata[i].mud_weight)
            mudtvd.append(md)
        i +=1
    fracture_pressure=[]
    for val in pressure:
        ig_unit=val.pressure_unit
        true_vertical_depth.append(val.true_vertical_depth)
        if(request.POST['pressureunit']==ig_unit):
            pore_pressure.append(val.pore_pressure)
            fracture_pressure.append(val.fracture_pressure)
        if(ig_unit=="psi" and request.POST['pressureunit']=="ppg"):

            if(val.pore_pressure!=None):
                porepressure= val.pore_pressure/(0.052 * val.true_vertical_depth) 
            else:
                porepressure= None
            if(val.fracture_pressure):
                fractionpressure=val.fracture_pressure/(0.052 * val.true_vertical_depth)
            else:
                fractionpressure=None
            pore_pressure.append(porepressure)
            fracture_pressure.append(fractionpressure)
        if(ig_unit=="psi" and request.POST['pressureunit']=="psi/ft"):
            if(val.pore_pressure!=None):
                porepressure= val.pore_pressure * val.true_vertical_depth 
            else:
                porepressure= None
            if(val.fracture_pressure):
                fractionpressure= val.fracture_pressure* val.true_vertical_depth
            else:
                fractionpressure=None
            pore_pressure.append(porepressure)
            fracture_pressure.append(fractionpressure)
        if(ig_unit=="ppg" and request.POST['pressureunit']=="psi"):
            if(val.pore_pressure!=None):
                porepressure= 0.052 * val.pore_pressure * val.true_vertical_depth 
            else:
                porepressure= None
            if(val.fracture_pressure):
                fractionpressure=0.052 * val.fracture_pressure* val.true_vertical_depth
            else:
                fractionpressure=None
            pore_pressure.append(porepressure)
            fracture_pressure.append(fractionpressure)
        if(ig_unit=="ppg" and request.POST['pressureunit']=="psi/ft"):
            if(val.pore_pressure!=None):
                porepressure= val.pore_pressure * val.true_vertical_depth
            else:
                porepressure= None
            if(val.fracture_pressure):
                fractionpressure=val.fracture_pressure* val.true_vertical_depth
            else:
                fractionpressure=None
            pore_pressure.append(porepressure)
            fracture_pressure.append(fractionpressure)
        if(ig_unit=="psi/ft" and request.POST['pressureunit']=="ppg"):
            if(val.pore_pressure!=None):
                porepressure= val.pore_pressure/0.052 
            else:
                porepressure= None
            if(val.fracture_pressure):
                fractionpressure=val.fracture_pressure/0.052
            else:
                fractionpressure=None
            pore_pressure.append(porepressure)
            fracture_pressure.append(fractionpressure)
        if(ig_unit=="psi/ft" and request.POST['pressureunit']=="psi"):
            if(val.pore_pressure!=None):
                porepressure= val.pore_pressure * val.true_vertical_depth 
            else:
                porepressure= None
            if(val.fracture_pressure):
                fractionpressure=val.fracture_pressure* val.true_vertical_depth
            else:
                fractionpressure=None
            pore_pressure.append(porepressure)
            fracture_pressure.append(fractionpressure)
        if(ig_unit=="g/cc" and request.POST['pressureunit']=="kPa"):
            if(val.pore_pressure!=None):
                porepressure= 9.80665 * val.pore_pressure * val.true_vertical_depth 
            else:
                porepressure= None
            if(val.fracture_pressure):
                fractionpressure=9.80665 * val.fracture_pressure* val.true_vertical_depth
            else:
                fractionpressure=None
            pore_pressure.append(porepressure)
            fracture_pressure.append(fractionpressure)
        if(ig_unit=="g/cc" and request.POST['pressureunit']=="kPa/m"):
            if(val.pore_pressure!=None):
                porepressure= 9.80665 * val.pore_pressure
            else:
                porepressure= None
            if(val.fracture_pressure):
                fractionpressure=9.80665 * val.fracture_pressure
            else:
                fractionpressure=None
            pore_pressure.append(porepressure)
            fracture_pressure.append(fractionpressure)
        if(ig_unit=="kPa" and request.POST['pressureunit']=="kPa/m"):
            if(val.pore_pressure!=None):
                porepressure= val.pore_pressure/val.true_vertical_depth
            else:
                porepressure= None
            if(val.fracture_pressure):
                fractionpressure=val.fracture_pressure/val.true_vertical_depth
            else:
                fractionpressure=None
            pore_pressure.append(porepressure)
            fracture_pressure.append(fractionpressure)
        if(ig_unit=="kPa/m" and request.POST['pressureunit']=="g/cc"):
            if(val.pore_pressure!=None):
                porepressure= val.pore_pressure/9.80665
            else:
                porepressure= None
            if(val.fracture_pressure):
                fractionpressure=val.fracture_pressure/9.80665
            else:
                fractionpressure=None
            pore_pressure.append(porepressure)
            fracture_pressure.append(fractionpressure)
        if(ig_unit=="kPa/m" and request.POST['pressureunit']=="kPa"):
            if(val.pore_pressure!=None):
                porepressure= val.pore_pressure*val.true_vertical_depth
            else:
                porepressure= None
            if(val.fracture_pressure):
                fractionpressure=val.fracture_pressure*val.true_vertical_depth
            else:
                fractionpressure=None
            pore_pressure.append(porepressure)
            fracture_pressure.append(fractionpressure)
    pore_series = pd.Series(pore_pressure)
    pore_interploate=pore_series.interpolate()
    # print(pore_interploate)

    tvd_series = pd.Series(true_vertical_depth)
    tvd_interploate=tvd_series.interpolate()

    fracture_series = pd.Series(fracture_pressure)
    fracture_interploate=fracture_series.interpolate()

    for i in range(len(fracture_interploate)):
        labels.append(float('% 6.2f' %tvd_interploate[i]))
        newdata.append(float('% 6.2f' %pore_interploate[i]))
        newdata1.append(float('% 6.2f' %fracture_interploate[i]))
    # return JsonResponse({"tvd": list(zip(labels,newdata,newdata1,muddatamd,mudweight,mudtvd))})
    return JsonResponse({"tvd": list(labels),'pore_pressure':list(newdata),'fraction_pressure':list(newdata1),'muddatamd':list(muddatamd),'mudweight':list(mudweight),'mudtvd':list(mudtvd)})


def create(request,well_id):
    checkpermission=user_rights_permission_projects('Create Data',request,'well',well_id)
    if(checkpermission != True):
        messages.error(request,'No Access to create!')
        return redirect(request.META.get('HTTP_REFERER'))     
    request.session['submenu']='pressure'
    if request.method == 'POST':
        measured_depth=request.POST.getlist('measured_depth')
        true_vertical_depth=request.POST.getlist('true_vertical_depth')
        pore_pressure=request.POST.getlist('pore_pressure')
        fracture_pressure=request.POST.getlist('fracture_pressure')
        pressure_unit=request.POST.get('pressure_unit')

        comments=request.POST.getlist('comments')
        i = 0 
        pressure_ids = []
        while i < len(measured_depth):  
            if(measured_depth[i]):
                pore_pressure_disp=pore_pressure[i] if pore_pressure[i] else None;  
                fracture_pressure_disp=fracture_pressure[i] if fracture_pressure[i] else None;    
                pressure = Pressure.objects.create(measured_depth=measured_depth[i],comments=comments[i],true_vertical_depth=true_vertical_depth[i],pore_pressure=pore_pressure_disp,fracture_pressure=fracture_pressure_disp,pressure_unit=pressure_unit,well_id=well_id,company=request.company)
                pressure_ids.append(pressure.id)
            i += 1
        source_id=pressure_ids
        proj_id = getprojidbywellid(well_id)
        userlog=adduserlog('Pore and Fracture pressure Created',request,source_id,'Pore and Fracture pressure',request.user.licence_type,proj_id,well_id,None,'create')
        return redirect('pressure:detail', well_id=well_id)
    max=[]
    for i in range(5):
        max.append(i)
    well=Wells.objects.get(id=well_id) 
    return render(request,'pressure/create.html',{'well_id':well_id,'max':max,'countries':getcountries(request.company),'company':request.company,'well':well})

def edit(request, pk, template_name='pressure/edit.html',format=None):
    pressure= Pressure.objects.filter(well_id=pk,status=1)
    request.session['submenu']='pressure'
    if request.method =='POST':
        # Pressure.objects.filter(well_id=pk).delete()
        measured_depth=request.POST.getlist('measured_depth')
        true_vertical_depth=request.POST.getlist('true_vertical_depth')
        pore_pressure=request.POST.getlist('pore_pressure')
        fracture_pressure=request.POST.getlist('fracture_pressure')
        comments=request.POST.getlist('comments')
        pressure_unit=request.POST.get('pressure_unit')
        pressure_id=request.POST.getlist('pressure_id')
        pressure_id_value=list(filter(None, pressure_id))
        print('pressure_id_value',pressure_id_value)
        currentid=[]
        i = 0
        while i < len(measured_depth):
            
            if(measured_depth[i]):   
                print('edit_len',i)
                pore_pressure_disp=pore_pressure[i] if pore_pressure[i] else None;  
                fracture_pressure_disp=fracture_pressure[i] if fracture_pressure[i] else None; 
                # if(pressure_id[i]):
                if(pressure_id[i]):
                    print('update')
                    currentid.append(pressure_id[i])
                    Pressure.objects.filter(id=pressure_id[i]).update(measured_depth=measured_depth[i],comments=comments[i],true_vertical_depth=true_vertical_depth[i],pore_pressure=pore_pressure_disp,fracture_pressure=fracture_pressure_disp,pressure_unit=pressure_unit)
                else:
                    print('create')
                    Pressure.objects.create(measured_depth=measured_depth[i],comments=comments[i],true_vertical_depth=true_vertical_depth[i],pore_pressure=pore_pressure_disp,fracture_pressure=fracture_pressure_disp,pressure_unit=pressure_unit,well_id=pk,company=request.company)
                    pressure_id=Pressure.objects.values('id').last()
                    currentid.append(pressure_id['id'])
            i += 1
        # source_id=pk 
        print('current',currentid)
        pressureid_del = Pressure.objects.filter(well_id=pk,status=1).exclude(id__in=currentid)
        pressure_id_list = [pressure.id for pressure in pressureid_del]
        Pressure.objects.filter(well_id=pk,status=1).exclude(id__in=currentid).update(status=0)
        source_id=currentid
        proj_id = getprojidbywellid(pk) 
        if (pressureid_del):
            adduserlog('Pore and Fracture pressure Deleted',request,pressure_id_list,'Pore and Fracture Pressure',request.user.licence_type,proj_id,pk,None,'delete')
        userlog=adduserlog('Pore and Fracture pressure Edited',request,source_id,'Pore and Fracture pressure',request.user.licence_type,proj_id,pk,None,'edit')
        return redirect('pressure:detail', well_id=pk)
    well=Wells.objects.get(id=pk) 
    return render(request, 'pressure/edit.html', {'pressure':pressure,'well_id':pk,'countries':getcountries(request.company),'company':request.company,'well':well})

def delete(request, pk, template_name='crudapp/confirm_delete.html'):
    pressure= Pressure.objects.filter(well_id=pk,status=1)
    id_list = [pressure.id for pressure in pressure]
    source_id=id_list
    proj_id = getprojidbywellid(pk)
    Pressure.objects.filter(well_id=pk,status=1).update(status=0)
    userlog=adduserlog('Pore and Fracture pressure Deleted',request,source_id,'Pore and Fracture pressure',request.user.licence_type,proj_id,pk,None,'delete')

    return redirect('pressure:detail', well_id=pk)
  



def importpressure(request,well_id):
    pressure = Pressure.objects.filter(company=request.company,well=well_id)
    request.session['submenu']='pressure'
    if request.method == 'POST' and 'myfile' in request.FILES:
        pressure = PressureForm(request.POST, request.FILES)    
        pressure_unit=request.POST['pressure_unit']    
        dataset = Dataset()
        new_datas = request.FILES['myfile']
        if not new_datas.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'pressure/importdata.html', {'well_id':well_id})
        imported_pressure = dataset.load(new_datas.read(),format='xlsx')
        non_empty_rows = [row for row in imported_pressure if any(cell is not None for cell in row)]
        for datas in non_empty_rows: 
            print(f"datas {datas[0]}")
            welltrajectory=WellTrajectory.objects.gettrajectory_bywell_md(datas[0],well_id)
            if(welltrajectory.count()>0):
                val=welltrajectory[0].true_vertical_depth
            else:
                belowmd=WellTrajectory.objects.getbelowmd(datas[0],well_id)
                print(f"belowmd {belowmd}")
                abovemd=WellTrajectory.objects.getabovemd(datas[0],well_id)
                print(f"abovemd {abovemd}")

                previous_md=WellTrajectory.objects.filter(id=belowmd.id)
                print(f"previous_md {previous_md}")

                next_md=WellTrajectory.objects.filter(id=abovemd.id)
                print(f"next_md {next_md}")

                pre_md=previous_md[0].measured_depth
                print(f"pre_md {pre_md}")

                n_md=next_md[0].measured_depth
                print(f"n_md {n_md}")

                pre_tvd=previous_md[0].true_vertical_depth
                print(f"pre_tvd {pre_tvd}")

                n_tvd=next_md[0].true_vertical_depth
                print(f"n_tvd {n_tvd}")

                pre_inc=previous_md[0].inclination
                print(f"pre_inc {pre_inc}")

                n_inc=next_md[0].inclination
                print(f"n_inc {n_inc}")

                pre_azi=previous_md[0].azimuth
                print(f"pre_azi {pre_azi}")

                n_azi=next_md[0].azimuth
                print(f"n_azi {n_azi}")

                
                dl_inc = acos(sin(n_inc*pi/180)*sin(pre_inc*pi/180)+(cos(pre_inc*pi/180)*cos(n_inc*pi/180)))*180/pi
                print(f"dl_inc {dl_inc}")

                dls_inc=round(dl_inc,2)*100/(n_tvd-pre_tvd)
                print(f"dls_inc {dls_inc}")

                dl_azi=acos(cos((n_azi-pre_azi)*pi/180))*180/pi
                print(f"dl_azi {dl_azi}")

                dls_azi=round(dl_azi,2)*100/(n_tvd-pre_tvd)
                print(f"dls_azi {dls_azi}")

                target_inculination=round(dls_inc,2)*(float(datas[0])-pre_tvd)/100+pre_inc
                print(f"target_inculination {target_inculination}")

                target_azimuth=pre_azi-dls_azi*(float(datas[0])-pre_tvd)/100
                print(f"target_azimuth {target_azimuth}")

                if(pre_inc==n_inc):
                    target_rf=0
                else:
                    target_rf=tan(round(dl_inc,2)/2*pi/180)*180/pi*2/round(dl_inc,2)
                print(f"target_rf {target_rf}")

                val=(cos(pre_inc*pi/180)+cos(round(target_inculination,2)*pi/180))*round(target_rf)*(float(datas[0])-pre_md)/2+pre_tvd 

                print(f"val {val}")


            obj = Pressure.objects.create(well_id=well_id,company=request.company,measured_depth=datas[0],true_vertical_depth=round(val,2),pore_pressure=datas[1],fracture_pressure=datas[2],comments=datas[3],pressure_unit=pressure_unit)
            obj.save()
        source_id=well_id
        userlog=adduserlog('Pore and Fracture pressure Created',request,source_id,'Pore and Fracture pressure',request.user.licence_type,None,well_id,None,'create')
        # final_data = list()
        #print(obj)
        # print(datas)
        # if datas[4].value == None:
        #     return ''

        features_x = list(filter(None, datas))
        # if self.datas:
        #     return ''
        # else:
        #     return datas  
        
        #return HttpResponse("File uploaded successfully")
        return redirect('pressure:detail', well_id=well_id)
    return render(request, 'pressure/importdata.html', {'well_id':well_id})

def download_xls_data(self,well_id):

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    header = pd.DataFrame=['TVD','Pore Pressure','Fracture Pressure','Comments']
    header_format = workbook.add_format({'bold': True, 'align': 'center'})
    for col_num, header_text in enumerate(header):
        worksheet.write(0, col_num, header_text, header_format)
        worksheet.set_column(col_num, col_num, len(header_text) + 2)

    workbook.close()
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=porepressure_fracturepressure.xlsx'
    output.seek(0)
    response.write(output.read())
    return response

    # df_output = pd.DataFrame({'TVD': [],'Pore Pressure': [],
    # 'Fracture Pressure': [],'Comments': [],
    # })

    # # my "Excel" file, which is an in-memory output file (buffer) 
    # # for the new workbook
    # excel_file = BytesIO()

    # xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter' )
    
    # df_output.to_excel(xlwriter, 'sheetname',index=False)

    # # xlwriter.save()
    # xlwriter.close()

    # # rewind the buffer
    # excel_file.seek(0)

    # # set the mime type so that the browser knows what to do with the file
    # response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # # set the file name in the Content-Disposition header
    # response['Content-Disposition'] = 'attachment; filename=Hydraulics.xlsx'

    # return response
   
