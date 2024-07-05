from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import WellTrajectory
from wells.models import Wells,WellUsers,CoordinateSystems,Projections
from django.views.generic import ListView, DetailView
from .forms import WellTrajectoryForm
from django.http import JsonResponse,HttpResponse
import json 
from .resources import WellTrajectoryResource
from tablib import Dataset
from django.contrib import messages
from wells.models import Wells
import openpyxl
import csv
from django.utils.encoding import smart_str
import pandas as pd
from io import BytesIO as IO
import xlsxwriter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from math import tan, pi, acos,sin,cos,sqrt,asin,atan
import math
from custom_auth.getunit import adduserlog,getcountries,getprojectunit
import numpy as np
import matplotlib.pyplot as plt
from helpers import *
from custom_auth.getunit import getprojidbywellid

# Create your views here.
def details(request,well_id):
    welltrajectory=WellTrajectory.objects.filter(company=request.company,well=well_id,status=1)
    paginator = Paginator(welltrajectory, 20)
    request.session['submenu']='welltrajectory'
    page = request.GET.get('page', 1)
    try:
        welltrajectory = paginator.page(page)
    except PageNotAnInteger:
        welltrajectory = paginator.page(1)
    except EmptyPage:
        welltrajectory = paginator.page(paginator.num_pages)

    welltrajectory_details=WellTrajectory.objects.filter(company=request.company,well=well_id,status=1)
    if(welltrajectory_details.count()>0):
        md=[float(welltrajectory.measured_depth) for welltrajectory in welltrajectory_details]
        inclination=[float(welltrajectory.inclination) for welltrajectory in welltrajectory_details]
        azimuth=[float(welltrajectory.azimuth) for welltrajectory in welltrajectory_details]
        chart=calculatewelltrajectory(md,inclination,azimuth)
    else:
        chart={}
        chart['chartdata']=[]
        chart['chartdata_tvd_vs']=[]
    well=Wells.objects.get(id=well_id)
    if(len(welltrajectory) == 0):
        checkpermission=user_rights_permission_projects('Create Data',request,'well',well_id)
        if(checkpermission != True):
            messages.error(request,'No Access to create!')
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('welltrajectory:create',well_id=well_id)
    countries=getcountries(request.company)
    checkpermission=user_rights_permission_projects('View Data',request,'well',well_id)
    if(checkpermission != True):
        messages.error(request,'No Access to view!')
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request,'welltrajectory/view.html',{'welltrajectory_details': welltrajectory_details,'well_id':well_id,'chartdata':chart['chartdata'],'chartdata_tvd_vs':chart['chartdata_tvd_vs'],'countries':countries,'company':request.company,'well':well,'project_id':well.project_id,'module_id':5,'user_id':request.user})


def create(request,well_id):
    well_details=Wells.objects.filter(id=well_id).values()
    easting_data=well_details[0]['easting'].replace(',',"") if well_details[0]['easting'] else ''
    northing_data=well_details[0]['northing'].replace(',',"") if well_details[0]['northing'] else ''
    request.session['submenu']='welltrajectory'
    welltype=request.session['welltype']

    if request.method == 'POST':
        trajectory_date=request.POST.getlist('trajectory_date')
        # trajectory_time=request.POST.getlist('trajectory_time')
        measured_depth=request.POST.getlist('measured_depth')
        inclination=request.POST.getlist('inclination')
        azimuth=request.POST.getlist('azimuth')
        true_vertical_depth=request.POST.getlist('true_vertical_depth')
        delta_e=request.POST.getlist('delta_e')
        delta_n=request.POST.getlist('delta_n')
        east=request.POST.getlist('east')
        north=request.POST.getlist('north')
        easting=request.POST.getlist('easting')
        northing=request.POST.getlist('northing')
        vertical_section=request.POST.getlist('vertical_section')
        dls=request.POST.getlist('dls')
        i = 0 
        trajectory_ids = []
        while i < len(measured_depth):   
            if(measured_depth[i]):   
                delta_e_data=delta_e[i] if(delta_e[i]!='') else None  
                delta_n_data=delta_n[i] if(delta_n[i]!='') else None  
                easting_data=easting[i] if(easting[i]!='') else None  
                northing_data=northing[i] if(northing[i]!='') else None  
                if(welltype=='PLAN'):
                    welltrajectory = WellTrajectory.objects.create(measured_depth=measured_depth[i],inclination=inclination[i],azimuth=azimuth[i],true_vertical_depth=true_vertical_depth[i],dls=dls[i],well_id=well_id,company=request.company,delta_e=delta_e_data,delta_n=delta_n_data,east=east[i],north=north[i],easting=easting_data,northing=northing_data,vertical_section=vertical_section[i])
                    trajectory_ids.append(welltrajectory.id)
                else:
                    timestamp=dateconversion(trajectory_date[i])
                    welltrajectory = WellTrajectory.objects.create(measured_depth=measured_depth[i],inclination=inclination[i],azimuth=azimuth[i],true_vertical_depth=true_vertical_depth[i],dls=dls[i],well_id=well_id,company=request.company,delta_e=delta_e_data,delta_n=delta_n_data,east=east[i],north=north[i],easting=easting_data,northing=northing_data,vertical_section=vertical_section[i],date=convertdateformat(trajectory_date[i]),timestamp=timestamp)
                    trajectory_ids.append(welltrajectory.id)
            i += 1
        source_id=trajectory_ids 
        userlog=adduserlog('Welltrajectory Created',request,source_id,'Welltrajectory',request.user.licence_type,well_details[0]['project_id'],well_id,None,'create')
        return redirect('welltrajectory:detail', well_id=well_id)
    max=[]
    for i in range(4):
        max.append(i)
    # messages.add_message(request, messages.INFO, 'Minimum Radius Curvature.')
    countries=getcountries(request.company)
    well=Wells.objects.get(id=well_id)
    return render(request,'welltrajectory/create.html',{'well_id':well_id,'max':max,'well_details':well_details,'easting_data':easting_data,'northing_data':northing_data,'countries':countries,'company':request.company,'well':well})


def edit(request, pk, template_name='welltrajectory/edit.html',queryset=None):
    welltrajectory= WellTrajectory.objects.filter(well_id=pk,status=1)
    well_details=Wells.objects.filter(id=pk).values()
    easting_data=well_details[0]['easting'].replace(',',"") 
    northing_data=well_details[0]['northing'].replace(',',"") 
    request.session['submenu']='welltrajectory'
    welltype=request.session['welltype']

    if request.method == 'POST':
        # WellTrajectory.objects.filter(well_id=pk).delete()
        trajectory_date=request.POST.getlist('trajectory_date')
        measured_depth=request.POST.getlist('measured_depth')
        inclination=request.POST.getlist('inclination')
        azimuth=request.POST.getlist('azimuth')
        true_vertical_depth=request.POST.getlist('true_vertical_depth')
        delta_e=request.POST.getlist('delta_e')
        delta_n=request.POST.getlist('delta_n')
        east=request.POST.getlist('east')
        north=request.POST.getlist('north')
        easting=request.POST.getlist('easting')
        northing=request.POST.getlist('northing')
        vertical_section=request.POST.getlist('vertical_section')
        dls=request.POST.getlist('dls')
        welltrajectory_id=request.POST.getlist('welltrajectory_id')
        trajectory=list(filter(None, welltrajectory_id))
        i = 0
        currentid=[] 
        trajectory_ids = []
        while i < len(measured_depth):   
            if(measured_depth[i]):
                if(welltrajectory_id[i]):
                    print('edit_trajectory')
                    currentid.append(int(welltrajectory_id[i]))
                    if(welltype=='PLAN'):
                        welltrajectory = WellTrajectory.objects.filter(id=welltrajectory_id[i]).update(measured_depth=measured_depth[i],inclination=inclination[i],azimuth=azimuth[i],true_vertical_depth=true_vertical_depth[i],dls=dls[i],delta_e=0,delta_n=0,east=east[i],north=north[i],easting=0,northing=0,vertical_section=vertical_section[i]) 
                        
                    else:
                        timestamp=dateconversion(trajectory_date[i])
                        welltrajectory = WellTrajectory.objects.filter(id=welltrajectory_id[i]).update(measured_depth=measured_depth[i],inclination=inclination[i],azimuth=azimuth[i],true_vertical_depth=true_vertical_depth[i],dls=dls[i],delta_e=0,delta_n=0,east=east[i],north=north[i],easting=0,northing=0,vertical_section=vertical_section[i],date=convertdateformat(trajectory_date[i]),timestamp=timestamp)     
                        
                else: 
                    print('create_trajectory')
                    if(welltype=='PLAN'):
                        welltrajectory = WellTrajectory.objects.create(measured_depth=measured_depth[i],inclination=inclination[i],azimuth=azimuth[i],true_vertical_depth=true_vertical_depth[i],dls=dls[i],well_id=pk,company=request.company,delta_e=0,delta_n=0,east=east[i],north=north[i],easting=0,northing=0,vertical_section=vertical_section[i])
                        
                    else:
                        timestamp=dateconversion(trajectory_date[i])
                        welltrajectory = WellTrajectory.objects.create(measured_depth=measured_depth[i],inclination=inclination[i],azimuth=azimuth[i],true_vertical_depth=true_vertical_depth[i],dls=dls[i],well_id=pk,company=request.company,delta_e=0,delta_n=0,east=east[i],north=north[i],easting=0,northing=0,vertical_section=vertical_section[i],date=convertdateformat(trajectory_date[i]),timestamp=timestamp)
                        
                    welltrajectory_id=WellTrajectory.objects.values('id').last()
                    currentid.append(int(welltrajectory_id['id']))
            i += 1 
      
        trajectory_id_del = WellTrajectory.objects.filter(well_id=pk,status=1).exclude(id__in=currentid)
        trajectory_id_list = [trajectory.id for trajectory in trajectory_id_del]
        WellTrajectory.objects.filter(well_id=pk,status=1).exclude(id__in=currentid).update(status=0)
        source_id=currentid 
        if (trajectory_id_del):
            adduserlog('Welltrajectory Deleted',request,trajectory_id_list,'Welltrajectory',request.user.licence_type,well_details[0]['project_id'],pk,None,'delete')
        userlog=adduserlog('Welltrajectory Edited',request,source_id,'Welltrajectory',request.user.licence_type,well_details[0]['project_id'],pk,None,'edit')
        return redirect('welltrajectory:detail', well_id=pk)
    well=Wells.objects.get(id=pk)
    countries=getcountries(request.company)
    return render(request, template_name, {'welltrajectory':welltrajectory,'well_id':pk,'easting_data':easting_data,'northing_data':northing_data,'countries':countries,'company':request.company,'well':well})


def delete(request, pk, template_name='crudapp/confirm_delete.html'):
    welltrajectory = WellTrajectory.objects.filter(well_id=pk,status=1)
    id_list = [trajectory.id for trajectory in welltrajectory]
    source_id=id_list
    proj_id = getprojidbywellid(pk)
    userlog=adduserlog('Welltrajectory Deleted',request,source_id,'Welltrajectory',request.user.licence_type,proj_id,pk,None,'delete')
    WellTrajectory.objects.filter(well_id=pk).update(status=0)

    return redirect('welltrajectory:detail', well_id=pk)
    

def importdata(request,well_id ):
    welltype=request.session['welltype']

    welltrajectory=WellTrajectory.objects.filter(company=request.company,well=well_id)
    well_details=Wells.objects.filter(id=well_id).values()
    # northing=well_details[0]['northing'].replace(",", "")
    # easting=well_details[0]['easting'].replace(",", "")
    request.session['submenu']='welltrajectory'
    if request.method == 'POST' and 'myfile' in request.FILES:
        welltrajectory = WellTrajectoryForm(request.POST, request.FILES)  
        dataset = Dataset()
        new_datas = request.FILES['myfile']

        if not new_datas.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'welltrajectory/importdata.html', {'well_id':well_id})
        imported_data = dataset.load(new_datas.read(),format='xlsx')
        # print(imported_data)
        md=[]
        inclination=[]
        azimuth=[]
        date=[]
        key=0
        trajectory_list=[]
        for welltrajectory in imported_data:
            md.append(float(welltrajectory[0]))
            inclination.append(float(welltrajectory[1]))
            azimuth.append(float(welltrajectory[2]))
            last_azimuth=azimuth[-1]

            MD=np.array(md)
            Inc=np.array(inclination)
            Azi=np.array(azimuth)
            Azi_ref=last_azimuth*pi/180 
            Inc_r=Inc/180*pi
            Azi_r=Azi/180*pi
            TVD=np.zeros([len(MD),1])
            TVD[0]=0
            t={}
            for i in range(len(MD)):
                t[i]=np.zeros([3,1])
            
            for i in range(len(MD)):
                t[i][0]=sin(Inc_r[i])*cos(Azi_r[i])
                t[i][1]=sin(Inc_r[i])*sin(Azi_r[i])
                t[i][2]=cos(Inc_r[i])
            
            A=np.zeros([len(MD),1])
            DLS=np.zeros([len(MD),1])
            N=np.zeros([len(MD),1])
            E=np.zeros([len(MD),1])
            VS=np.zeros([len(MD),1])
            
            #calculate tvd north east and vertical section
            for i in range(1,len(MD)):
                A[i]=2*asin(((sin((Inc_r[i]-Inc_r[i-1])/2))**2+sin(Inc_r[i-1])*sin(Inc_r[i])*(sin((Azi_r[i]-Azi_r[i-1])/2))**2)**0.5)
                DLS[i]=A[i]/(MD[i]-MD[i-1])*180/math.pi*100
                if A[i]==0 or Inc[i-1]==Inc[i]:
                    N[i]=N[i-1]+((MD[i]-MD[i-1])/2)*(t[i][0]+t[i-1][0])
                    E[i]=E[i-1]+((MD[i]-MD[i-1])/2)*(t[i][1]+t[i-1][1])
                    TVD[i]=TVD[i-1]+((MD[i]-MD[i-1])/2)*(t[i][2]+t[i-1][2])
                else:
                    N[i]=N[i-1]+(((MD[i]-MD[i-1])/A[i])*tan(A[i]/2))*(t[i][0]+t[i-1][0])
                    E[i]=E[i-1]+(((MD[i]-MD[i-1])/A[i])*tan(A[i]/2))*(t[i][1]+t[i-1][1])
                    TVD[i]=TVD[i-1]+(((MD[i]-MD[i-1])/A[i])*tan(A[i]/2))*(t[i][2]+t[i-1][2])
            
            for i in range(1,len(MD)):
                VS[i]=sqrt(N[i]**2+E[i]**2)*cos(abs(Azi_ref-Azi_r[i]))
        
            S_s=10
            MD_i=np.arange(MD[0],MD[len(MD)-1]+S_s,S_s)
            TVD_i=np.zeros([len(MD_i),1])
            Inc_i=np.zeros([len(MD_i),1])
            Azi_i=np.zeros([len(MD_i),1])
            A_i=np.zeros([len(MD_i),1])
            N_i=np.zeros([len(MD_i),1])
            E_i=np.zeros([len(MD_i),1])
            t_i={}
            for i in range(len(MD_i)):
                t_i[i]=np.zeros([3,1])
        
            for i in range(1,len(MD)):
                for j in range(1,len(MD_i)):
                    #Step 1: Calculate Subtended Angle
                    if MD[i-1]<MD_i[j] and MD_i[j]<=MD[i]:
                        A_i[j]=(MD_i[j]-MD[i-1])*A[i]/(MD[i]-MD[i-1])
                        
                        #Step 2: Calculate the Unit Vectors
                        if A_i[j]==0:
                            t_i[j][0]=(1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i-1][0]+((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i][0]
                            t_i[j][1]=(1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i-1][1]+((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i][1]
                            t_i[j][2]=(1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i-1][2]+((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i][2]
                        else:
                            t_i[j][0]=(sin((1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*A_i[j])/sin(A_i[j])*t[i-1][0])+(sin((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1])*A_i[j])/sin(A_i[j])*t[i][0])
                            t_i[j][1]=(sin((1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*A_i[j])/sin(A_i[j])*t[i-1][1])+(sin((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1])*A_i[j])/sin(A_i[j])*t[i][1])
                            t_i[j][2]=(sin((1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*A_i[j])/sin(A_i[j])*t[i-1][2])+(sin((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1])*A_i[j])/sin(A_i[j])*t[i][2])
                        
                        #Step 3: Interpolate North, East and TVD
                        if A_i[j]==0:
                            N_i[j]=N[i-1]+((MD_i[j]-MD[i-1])/2)*(t[i-1][0]+t_i[j][0])
                            E_i[j]=E[i-1]+((MD_i[j]-MD[i-1])/2)*(t[i-1][1]+t_i[j][1])
                            TVD_i[j]=TVD[i-1]+((MD_i[j]-MD[i-1])/2)*(t[i-1][2]+t_i[j][2])
                        else:
                            N_i[j]=N[i-1]+((MD_i[j]-MD[i-1])/A_i[j])*tan(A_i[j]/2)*(t[i-1][0]+t_i[j][0])
                            E_i[j]=E[i-1]+((MD_i[j]-MD[i-1])/A_i[j])*tan(A_i[j]/2)*(t[i-1][1]+t_i[j][1])
                            TVD_i[j]=TVD[i-1]+((MD_i[j]-MD[i-1])/A_i[j])*tan(A_i[j]/2)*(t[i-1][2]+t_i[j][2])
                        
                        #Step 4: Calculate Azimuth and Inclination
                        Inc_i[j]=atan(((N_i[j]-N_i[j-1])**2+(E_i[j]-E_i[j-1])**2)**0.5/(TVD_i[j]-TVD_i[j-1]))
                        if N_i[j]==0 :
                            Azi_i[j]=Azi_i[j-1]
                        else:
                            Azi_i[j]=atan((E_i[j])/(N_i[j]))

            Azi_vsd=np.zeros([len(MD_i),1])
            VS_i=np.zeros([len(MD_i),1])
            for i in range(1,len(MD_i)):
                Azi_vsd[i]=abs(Azi_ref-(Azi_i[i]))
                VS_i[i]=sqrt(N_i[i]**2+E_i[i]**2)*cos(Azi_vsd[i])
            # print(f"MD {MD[key]}")
            # print(f"inclination {inclination[key]}")
            # print(f"azimuth {azimuth[key]}")
            # print(f"TVD_i {TVD_i[key]}")
            # print(f"DLS {DLS[key]}")
            # print(f"E_i {E_i[key]}")
            # print(f"N_i {N_i[key]}")
            # print(f"VS_i {VS_i[key]}")
            

            # print(TVD[key].tolist()[0])
            # print(type(TVD[key].tolist()))
            if(welltype=='ACTUAL'):
                date.append(welltrajectory[3])
                # time.append(welltrajectory[4])
                timestamp=dateconversion_welltrajectory(date[key])
                obj = WellTrajectory.objects.create(well_id=well_id,company=request.company, measured_depth=MD[key],inclination=inclination[key],azimuth=azimuth[key],true_vertical_depth=TVD[key].tolist()[0],dls=DLS[key].tolist()[0],east=E[key].tolist()[0],north=N[key].tolist()[0],vertical_section=VS[key].tolist()[0],date=date[key],timestamp=timestamp) 
            else:
                trajectory_data=WellTrajectory(
                well_id=well_id,company=request.company, measured_depth=MD[key],inclination=inclination[key],azimuth=azimuth[key],true_vertical_depth=TVD[key].tolist()[0],dls=DLS[key].tolist()[0],east=E[key].tolist()[0],north=N[key].tolist()[0],vertical_section=VS[key].tolist()[0]
                )
            trajectory_list.append(trajectory_data)
            key += 1
        WellTrajectory.objects.bulk_create(trajectory_list)
        return redirect('welltrajectory:detail', well_id=well_id)
    return render(request, 'welltrajectory/importdata.html', {'well_id':well_id,'welltype':welltype})

def download_csv_data(self,well_id):
    welltype=self.session['welltype']
    print(f"welltype {welltype}")

    unit='ft'
    # if(welltype=='PLAN'):
    df_output = pd.DataFrame({'MD'+'(ft)':[], 'Inclination'+'(°)':[],'Azimuth'+'(°)':[],'Date':[]})
    # else:
    #     df_output = pd.DataFrame({'MD'+'(ft)':[], 'Inclination'+'(°)':[],'Azimuth'+'(°)':[],'Date':[],'Time':[]})


    # my "Excel" file, which is an in-memory output file (buffer) 
    # for the new workbook
    excel_file = IO()

    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    
    df_output.to_excel(xlwriter, 'sheetname',index=False)

    # xlwriter.save()
    xlwriter.close()

    # rewind the buffer
    excel_file.seek(0)

    # set the mime type so that the browser knows what to do with the file
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # set the file name in the Content-Disposition header
    response['Content-Disposition'] = 'attachment; filename=welltrajectory.xlsx'

    return response


def welltrajectorytvdcal(request):
    # current_azimuth = float(request.GET['current_azimuth'])
    # prev_inclination = float(request.GET['prev_inclination'])
    # prev_azimuth = float(request.GET['prev_azimuth'])
    # current_inclination = float(request.GET['current_inclination'])
    # tvd = float(request.GET['tvd'])
    # current_md=float(request.GET['current_md'])
    # prev_md=float(request.GET['prev_md'])
    # prev_north=float(request.GET['prev_north'])
    # prev_east=float(request.GET['prev_east'])
    # surface_easting=float(request.GET['surface_easting'])
    # surface_northing=float(request.GET['surface_northing'])
    # print(f'current_inclination {current_inclination}')
    # print(f'prev_inclination {prev_inclination}')
    # print(f'current_azimuth {current_azimuth}')
    # print(f'prev_azimuth {prev_azimuth}')
    # print(acos(round((sin(current_inclination*pi/180)*sin(prev_inclination*pi/180)*cos((current_azimuth-prev_azimuth)*pi/180))+(cos(prev_inclination*pi/180)*cos(current_inclination*pi/180)))))

    # dl = acos(round((sin(current_inclination*pi/180)*sin(prev_inclination*pi/180)*cos((current_azimuth-prev_azimuth)*pi/180))+(cos(prev_inclination*pi/180)*cos(current_inclination*pi/180))))*180/pi
    # print(f'dl{dl}')
    # print((sin(45.00*pi/180)*sin(0.00*pi/180)*cos((50.00-0.00)*pi/180))+(cos(0.00*pi/180)*cos(45.00*pi/180)))
    # print(acos((sin(45.00*pi/180)*sin(0.00*pi/180)*cos((50.00-0.00)*pi/180))+(cos(0.00*pi/180)*cos(45.00*pi/180)))*180/pi)
    # # dl = round(acos((sin(1.66*pi/180)*sin(0.78*pi/180)*cos((323.52-323.52)*pi/180))+(cos(0.78*pi/180)*cos(1.66*pi/180)))*180/pi,2)
    # if(current_azimuth==prev_azimuth or current_inclination==prev_inclination):
    #     rf=1.00
    # else:
    #     if(dl==0.0):
    #         rf=1.00
    #     else:
    #         rf=tan(dl/2*pi/180)*180/pi*(2/dl)
    # print(f'rf {rf}')
    # delts_e=((sin(prev_inclination*pi/180)*sin(prev_azimuth*pi/180))+(sin(current_inclination*pi/180)*sin(current_azimuth*pi/180)))*(rf*(current_md-prev_md)/2)
    # delts_n=((sin(prev_inclination*pi/180)*cos(prev_azimuth*pi/180))+(sin(current_inclination*pi/180)*cos(current_azimuth*pi/180)))*(rf*(current_md-prev_md)/2)
    # east=prev_east+delts_e
    # north=prev_north+delts_n
    # easting=delts_e+surface_easting
    # northing=delts_n+surface_northing
    # tvd=(cos(prev_inclination*pi/180)+cos(current_inclination*pi/180))*(rf*(current_md-prev_md)/2)+tvd
    # dls=dl*100/(current_md-prev_md)
    # vartical_section=sqrt((east)**2+(north)**2)
    # data={
    #     "tvd": round(tvd,2),
    #     "dls":round(dls,2),
    #     "delts_e":round(delts_e,2),
    #     "delts_n":round(delts_n,2),
    #     "east":round(east,2),
    #     "north":round(north,2),
    #     "easting":round(easting,2),
    #     "northing":round(northing,2),
    #     "vartical_section":vartical_section
    # }
    prev_mds = request.POST.getlist('prev_mds[]')
    prev_azimuths = request.POST.getlist('prev_azimuths[]')
    prev_inclinations = request.POST.getlist('prev_inclinations[]')
    well_id = request.POST.get('well_id')
    unit=getprojectunit(well_id)
    md=[float(md) for md in prev_mds]
    print(f"md {md}")
    inclination=[float(inc) for inc in prev_inclinations]
    azimuth=[float(azi) for azi in prev_azimuths]
    last_azimuth=azimuth[-1]
    # print(last_azimuth)

    MD=np.array(md)
    Inc=np.array(inclination)
    Azi=np.array(azimuth)
    Azi_ref=last_azimuth*pi/180 
    Inc_r=Inc/180*pi
    Azi_r=Azi/180*pi
    TVD=np.zeros([len(MD),1])
    TVD[0]=0
    t={}
    for i in range(len(MD)):
        t[i]=np.zeros([3,1])
    
    for i in range(len(MD)):
        t[i][0]=sin(Inc_r[i])*cos(Azi_r[i])
        t[i][1]=sin(Inc_r[i])*sin(Azi_r[i])
        t[i][2]=cos(Inc_r[i])
            
    A=np.zeros([len(MD),1])
    DLS=np.zeros([len(MD),1])
    N=np.zeros([len(MD),1])
    E=np.zeros([len(MD),1])
    VS=np.zeros([len(MD),1])
            
    #calculate tvd north east and vertical section
    for i in range(1,len(MD)):
        A[i]=2*asin(((sin((Inc_r[i]-Inc_r[i-1])/2))**2+sin(Inc_r[i-1])*sin(Inc_r[i])*(sin((Azi_r[i]-Azi_r[i-1])/2))**2)**0.5)
        DLS[i]=A[i]/(MD[i]-MD[i-1])
        if A[i]==0 or Inc[i-1]==Inc[i]:
            N[i]=N[i-1]+((MD[i]-MD[i-1])/2)*(t[i][0]+t[i-1][0])
            E[i]=E[i-1]+((MD[i]-MD[i-1])/2)*(t[i][1]+t[i-1][1])
            TVD[i]=TVD[i-1]+((MD[i]-MD[i-1])/2)*(t[i][2]+t[i-1][2])
        else:
            N[i]=N[i-1]+(((MD[i]-MD[i-1])/A[i])*tan(A[i]/2))*(t[i][0]+t[i-1][0])
            E[i]=E[i-1]+(((MD[i]-MD[i-1])/A[i])*tan(A[i]/2))*(t[i][1]+t[i-1][1])
            TVD[i]=TVD[i-1]+(((MD[i]-MD[i-1])/A[i])*tan(A[i]/2))*(t[i][2]+t[i-1][2])
    
    for i in range(1,len(MD)):
        VS[i]=sqrt(N[i]**2+E[i]**2)*cos(abs(Azi_ref-Azi_r[i]))
        
    S_s=10
    MD_i=np.arange(MD[0],MD[len(MD)-1]+S_s,S_s)


    TVD_i=np.zeros([len(MD_i),1])
    Inc_i=np.zeros([len(MD_i),1])
    Azi_i=np.zeros([len(MD_i),1])
    A_i=np.zeros([len(MD_i),1])
    N_i=np.zeros([len(MD_i),1])
    E_i=np.zeros([len(MD_i),1])
    t_i={}
    for i in range(len(MD_i)):
        t_i[i]=np.zeros([3,1])
        
    for i in range(1,len(MD)):
        for j in range(1,len(MD_i)):
            #Step 1: Calculate Subtended Angle
            if MD[i-1]<MD_i[j] and MD_i[j]<=MD[i]:
                A_i[j]=(MD_i[j]-MD[i-1])*A[i]/(MD[i]-MD[i-1])
                
                #Step 2: Calculate the Unit Vectors
                if A_i[j]==0:
                    t_i[j][0]=(1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i-1][0]+((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i][0]
                    t_i[j][1]=(1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i-1][1]+((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i][1]
                    t_i[j][2]=(1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i-1][2]+((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i][2]
                else:
                    t_i[j][0]=(sin((1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*A_i[j])/sin(A_i[j])*t[i-1][0])+(sin((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1])*A_i[j])/sin(A_i[j])*t[i][0])
                    t_i[j][1]=(sin((1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*A_i[j])/sin(A_i[j])*t[i-1][1])+(sin((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1])*A_i[j])/sin(A_i[j])*t[i][1])
                    t_i[j][2]=(sin((1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*A_i[j])/sin(A_i[j])*t[i-1][2])+(sin((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1])*A_i[j])/sin(A_i[j])*t[i][2])
                
                #Step 3: Interpolate North, East and TVD
                if A_i[j]==0:
                    N_i[j]=N[i-1]+((MD_i[j]-MD[i-1])/2)*(t[i-1][0]+t_i[j][0])
                    E_i[j]=E[i-1]+((MD_i[j]-MD[i-1])/2)*(t[i-1][1]+t_i[j][1])
                    TVD_i[j]=TVD[i-1]+((MD_i[j]-MD[i-1])/2)*(t[i-1][2]+t_i[j][2])
                else:
                    N_i[j]=N[i-1]+((MD_i[j]-MD[i-1])/A_i[j])*tan(A_i[j]/2)*(t[i-1][0]+t_i[j][0])
                    E_i[j]=E[i-1]+((MD_i[j]-MD[i-1])/A_i[j])*tan(A_i[j]/2)*(t[i-1][1]+t_i[j][1])
                    TVD_i[j]=TVD[i-1]+((MD_i[j]-MD[i-1])/A_i[j])*tan(A_i[j]/2)*(t[i-1][2]+t_i[j][2])
                
                #Step 4: Calculate Azimuth and Inclination
                Inc_i[j]=atan(((N_i[j]-N_i[j-1])**2+(E_i[j]-E_i[j-1])**2)**0.5/(TVD_i[j]-TVD_i[j-1]))
                if N_i[j]==0 or N_i[j]==N_i[j-1]:
                    Azi_i[j]=Azi_i[j-1]
                else:
                    Azi_i[j]=atan((E_i[j])/(N_i[j]))

    Azi_vsd=np.zeros([len(MD_i),1])
    VS_i=np.zeros([len(MD_i),1])
    for i in range(1,len(MD_i)):
        Azi_vsd[i]=abs(Azi_ref-(Azi_i[i]))
        VS_i[i]=sqrt(N_i[i]**2+E_i[i]**2)*cos(Azi_vsd[i])
    print(f"MD_i {MD_i}")
    print(f"TVD_i {TVD_i}")

    tvd=TVD_i[:-1]
    vs=VS_i[:-1]
    e=E_i[:-1]
    n=N_i[:-1]
    chart_tvd=[tvd[0] for tvd in tvd.tolist()]
    chart_verticalsection=[vs[0] for vs in vs.tolist()]
    chart_e=[e[0] for e in e.tolist()]
    chart_n=[n[0] for n in n.tolist()]
    
    chartdata=[]
    for i in range(len(chart_e)):
        data = [chart_e[i],chart_n[i]]
        chartdata.append(data)
    chartdata_tvd_vs=[]
    for i in range(len(chart_verticalsection)):
        detail = [chart_verticalsection[i],chart_tvd[i]]
        chartdata_tvd_vs.append(detail)
    tvd_length = len(TVD)
    last_tvd = TVD[tvd_length - 1]
    print(f"last_tvd[0] {TVD}")
    # print(f"dls {DLS*180/pi*100}")
    # print(f"TVD {TVD}")
    # print(f"MD {MD}")
    DLS_length=len(DLS)
    last_DLS = DLS[DLS_length - 1]
    # print(f"last_DLS {last_DLS}")
    # print(f"last_DLS {last_DLS[0]}")

    E_length=len(E)
    last_E = E[E_length - 1]
    N_length=len(N)
    last_N = N[N_length - 1]
    VS_length=len(VS)
    last_VS = VS[VS_length - 1]
    if unit == 'API':
        converteddls = last_DLS[0]*180/pi*100
    else:
        converteddls = last_DLS[0]*180/pi*30.478
    data={
        'chartdata':chartdata,
        'chartdata_tvd_vs':chartdata_tvd_vs,
        'tvd':last_tvd[0],
        'converteddls':converteddls,
        'dls':last_DLS[0],
        'e':last_E[0],
        'n':last_N[0],
        'vs':last_VS[0]
    }
    return JsonResponse(data, safe=False)

def download_welltrajectory(request,well_id):
    welltrajectory=WellTrajectory.objects.filter(company=request.company,well=well_id)
    md=[]
    inclination=[]
    azimuth=[]
    tvd=[]
    dls=[]
    # delta_e=[]
    # delta_n=[]
    east=[]
    north=[]
    # easting=[]
    # northing=[]
    vertical_section=[]
    for val in welltrajectory:
        md.append(val.measured_depth)
        inclination.append(val.inclination)
        azimuth.append(val.azimuth)
        tvd.append(val.true_vertical_depth)
        dls.append(val.dls)
        # delta_e.append(val.delta_e)
        # delta_n.append(val.delta_n)
        east.append(val.east)
        north.append(val.north)
        # easting.append(val.easting)
        # northing.append(val.northing)
        vertical_section.append(val.vertical_section)
    df_output = pd.DataFrame({'MD'+'(ft)': md, 'Inclination'+'(°)': inclination,'Azimuth'+'(°)': azimuth,
    'TVD'+'(ft)': tvd,
    'DLS'+('ft'): dls,
    # 'ΔE'+'(°/100 ft)' :delta_e,
    # 'ΔN' :delta_n,
    'East' :east,
    'North' :north,
    # 'Easting'+'(mE)' :easting,
    # 'Northing'+'(mN)' :northing,
    'Vertical Section'+'(ft)' :vertical_section,
    })

    # my "Excel" file, which is an in-memory output file (buffer) 
    # for the new workbook
    excel_file = IO()

    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    
    df_output.to_excel(xlwriter, 'sheetname',index=False)

    xlwriter.save()
    xlwriter.close()

    # rewind the buffer
    excel_file.seek(0)

    # set the mime type so that the browser knows what to do with the file
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # set the file name in the Content-Disposition header
    response['Content-Disposition'] = 'attachment; filename=welltrajectory.xlsx'

    return response

def calculatewelltrajectory(md,inclination,azimuth):
    MD=np.array(md)
    Inc=np.array(inclination)
    Azi=np.array(azimuth)
    Azi_ref=160*pi/180 
    Inc_r=Inc/180*pi
    Azi_r=Azi/180*pi
    TVD=np.zeros([len(MD),1])
    TVD[0]=0
    t={}
    for i in range(len(MD)):
        t[i]=np.zeros([3,1])
    
    for i in range(len(MD)):
        t[i][0]=sin(Inc_r[i])*cos(Azi_r[i])
        t[i][1]=sin(Inc_r[i])*sin(Azi_r[i])
        t[i][2]=cos(Inc_r[i])
            
    A=np.zeros([len(MD),1])
    DLS=np.zeros([len(MD),1])
    N=np.zeros([len(MD),1])
    E=np.zeros([len(MD),1])
    VS=np.zeros([len(MD),1])
            
    #calculate tvd north east and vertical section
    for i in range(1,len(MD)):
        A[i]=2*asin(((sin((Inc_r[i]-Inc_r[i-1])/2))**2+sin(Inc_r[i-1])*sin(Inc_r[i])*(sin((Azi_r[i]-Azi_r[i-1])/2))**2)**0.5)
        DLS[i]=A[i]/(MD[i]-MD[i-1])
        if A[i]==0 or Inc[i-1]==Inc[i]:
            N[i]=N[i-1]+((MD[i]-MD[i-1])/2)*(t[i][0]+t[i-1][0])
            E[i]=E[i-1]+((MD[i]-MD[i-1])/2)*(t[i][1]+t[i-1][1])
            TVD[i]=TVD[i-1]+((MD[i]-MD[i-1])/2)*(t[i][2]+t[i-1][2])
        else:
            N[i]=N[i-1]+(((MD[i]-MD[i-1])/A[i])*tan(A[i]/2))*(t[i][0]+t[i-1][0])
            E[i]=E[i-1]+(((MD[i]-MD[i-1])/A[i])*tan(A[i]/2))*(t[i][1]+t[i-1][1])
            TVD[i]=TVD[i-1]+(((MD[i]-MD[i-1])/A[i])*tan(A[i]/2))*(t[i][2]+t[i-1][2])
    
    for i in range(1,len(MD)):
        VS[i]=sqrt(N[i]**2+E[i]**2)*cos(abs(Azi_ref-Azi_r[i]))
        
    S_s=10
    MD_i=np.arange(MD[0],MD[len(MD)-1]+S_s,S_s)
    TVD_i=np.zeros([len(MD_i),1])
    Inc_i=np.zeros([len(MD_i),1])
    Azi_i=np.zeros([len(MD_i),1])
    A_i=np.zeros([len(MD_i),1])
    N_i=np.zeros([len(MD_i),1])
    E_i=np.zeros([len(MD_i),1])
    t_i={}
    for i in range(len(MD_i)):
        t_i[i]=np.zeros([3,1])
        
    for i in range(1,len(MD)):
        for j in range(1,len(MD_i)):
            #Step 1: Calculate Subtended Angle
            if MD[i-1]<MD_i[j] and MD_i[j]<=MD[i]:
                A_i[j]=(MD_i[j]-MD[i-1])*A[i]/(MD[i]-MD[i-1])
                
                #Step 2: Calculate the Unit Vectors
                if A_i[j]==0:
                    t_i[j][0]=(1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i-1][0]+((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i][0]
                    t_i[j][1]=(1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i-1][1]+((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i][1]
                    t_i[j][2]=(1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i-1][2]+((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*t[i][2]
                else:
                    t_i[j][0]=(sin((1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*A_i[j])/sin(A_i[j])*t[i-1][0])+(sin((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1])*A_i[j])/sin(A_i[j])*t[i][0])
                    t_i[j][1]=(sin((1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*A_i[j])/sin(A_i[j])*t[i-1][1])+(sin((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1])*A_i[j])/sin(A_i[j])*t[i][1])
                    t_i[j][2]=(sin((1-(MD_i[j]-MD[i-1])/(MD[i]-MD[i-1]))*A_i[j])/sin(A_i[j])*t[i-1][2])+(sin((MD_i[j]-MD[i-1])/(MD[i]-MD[i-1])*A_i[j])/sin(A_i[j])*t[i][2])
                
                #Step 3: Interpolate North, East and TVD
                if A_i[j]==0:
                    N_i[j]=N[i-1]+((MD_i[j]-MD[i-1])/2)*(t[i-1][0]+t_i[j][0])
                    E_i[j]=E[i-1]+((MD_i[j]-MD[i-1])/2)*(t[i-1][1]+t_i[j][1])
                    TVD_i[j]=TVD[i-1]+((MD_i[j]-MD[i-1])/2)*(t[i-1][2]+t_i[j][2])
                else:
                    N_i[j]=N[i-1]+((MD_i[j]-MD[i-1])/A_i[j])*tan(A_i[j]/2)*(t[i-1][0]+t_i[j][0])
                    E_i[j]=E[i-1]+((MD_i[j]-MD[i-1])/A_i[j])*tan(A_i[j]/2)*(t[i-1][1]+t_i[j][1])
                    TVD_i[j]=TVD[i-1]+((MD_i[j]-MD[i-1])/A_i[j])*tan(A_i[j]/2)*(t[i-1][2]+t_i[j][2])
                
                #Step 4: Calculate Azimuth and Inclination
                Inc_i[j]=atan(((N_i[j]-N_i[j-1])**2+(E_i[j]-E_i[j-1])**2)**0.5/(TVD_i[j]-TVD_i[j-1]))
                if N_i[j]==0 or N_i[j]==N_i[j-1]:
                    Azi_i[j]=Azi_i[j-1]
                else:
                    Azi_i[j]=atan((E_i[j])/(N_i[j]))

    Azi_vsd=np.zeros([len(MD_i),1])
    VS_i=np.zeros([len(MD_i),1])
    for i in range(1,len(MD_i)):
        Azi_vsd[i]=abs(Azi_ref-(Azi_i[i]))
        VS_i[i]=sqrt(N_i[i]**2+E_i[i]**2)*cos(Azi_vsd[i])
   
    tvd=TVD_i[:-1]
    vs=VS_i[:-1]
    e=E_i[:-1]
    n=N_i[:-1]

    # print(f"MD {MD[key]}")
    # print(f"inclination {inclination[key]}")
    # print(f"azimuth {azimuth[key]}")
    # print(f"TVD_i {TVD_i}")
    # # print(f"DLS {DLS[key]}")
    # print(f"E_i {E_i}")
    # print(f"N_i {N_i}")
    # print(f"VS_i {VS_i}")
    tvdlist=tvd.tolist()
    eastlist=e.tolist()
    northlist=n.tolist()
    vertical_section=vs.tolist()
    chartdata=[]
    for i in range(len(tvdlist)):
        data = [eastlist[i][0],northlist[i][0]]
        chartdata.append(data)

    chartdata_tvd_vs=[]
    for i in range(len(vertical_section)):
        detail = [vertical_section[i][0],tvdlist[i][0]]
        chartdata_tvd_vs.append(detail)
    data={
      'chartdata':chartdata,
      'chartdata_tvd_vs':chartdata_tvd_vs
    }
    # print(f"chartdata_tvd_vs {chartdata_tvd_vs}")
    # print(f"chartdata {chartdata}")

    # print(f"DLS {DLS[key]}")
    # print(f"E_i {E_i}")
    # print(f"N_i {N_i}")
    # print(f"VS_i {VS_i}")
    

    # print(TVD[key].tolist()[0])
    # print(type(TVD[key].tolist()))
    return data

def gettrajectory(request):
    if request.method == "GET":
        well_id = request.GET.get('well_id')
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
   
    filtered_trajectory = WellTrajectory.objects.gettrajectory(request.company,well_id,1,start,length)
    total_records = WellTrajectory.objects.getalltrajectory(request.company,well_id,1).count()


    # print(f"filtered_trajectory {filtered_trajectory}")

    data = []
    for trajectory in filtered_trajectory:
        data.append({
            'md': trajectory.measured_depth,
            'lnclination': trajectory.inclination,
            'azimuth':trajectory.azimuth,
            'tvd':round(trajectory.true_vertical_depth,2),
            'dls':round(trajectory.dls,2),
            'vertical_section':round(trajectory.vertical_section,2),
        })
    
    print(f"data {data}")

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)





         



