from wells.models import Wells
from welltrajectory.models import WellTrajectory
import pandas as pd
from scipy.interpolate import interp1d
import numpy
from custom_auth.models import Userlog,Countries
from projects.models import Projects
from django.db.models import Count, Min, Sum, Avg , Max
# from datetime import datetime


def getprojectunit(well_id):
    well=Wells.objects.get(id=well_id)
    unit=well.project.unit
    return unit

def convertcasingvalue(fromunit,tounit,data):
    converteddata=[]
    j=0
    for i in data:
        if(fromunit=='API' and tounit=='SI'):
            converteddata.append({'nominal_od':round(i['nominal_od']/12/3.281*1000,3),'databasevalue':i['nominal_od']})
        else:
            converteddata.append({'nominal_od':i['nominal_od'],'databasevalue':i['nominal_od']})
        j +=1
    return converteddata

def convertcollarvalue(fromunit,tounit,data):
    convertcollardata=[]
    j=0
    for i in data:
        if(fromunit=='API' and tounit=='SI'):
            convertcollardata.append({'normal_od':round(i['normal_od']/12/3.281*1000,3),'databasevalue':i['normal_od']})
        else:
            convertcollardata.append({'normal_od':i['normal_od'],'databasevalue':i['normal_od']})
        j +=1
    return convertcollardata

def convertpipevalue(fromunit,tounit,data):
    convertpipedata=[]
    j=0
    for i in data:
        if(fromunit=='API' and tounit=='SI'):
            convertpipedata.append({'normal_od':round(i['normal_od']/12/3.281*1000,3),'databasevalue':i['normal_od']})
        else:
            convertpipedata.append({'normal_od':i['normal_od'],'databasevalue':i['normal_od']})
        j +=1
    return convertpipedata

def converthwdpvalue(fromunit,tounit,data):
    converthwdpdata=[]
    j=0
    for i in data:
        if(fromunit=='API' and tounit=='SI'):
            converthwdpdata.append({'nominal_od':round(i['nominal_od']/12/3.281*1000,3),'databasevalue':i['nominal_od']})
        else:
            converthwdpdata.append({'nominal_od':i['nominal_od'],'databasevalue':i['nominal_od']})
        j +=1
    return converthwdpdata

def convertpipe_weight(fromunit,tounit,data):
    convertpipedata=[]
    j=0
    for i in data:
        if(fromunit=='API' and tounit=='SI'):
            convertpipedata.append({'weight':round(i['weight']*4.448*3.281,2),'databasevalue':i['weight']})
        else:
            convertpipedata.append({'weight':i['weight'],'databasevalue':i['weight']})
        j +=1
    return convertpipedata
        
def converttosi(fromunit,tounit,data):
    convertpipedata=[]
    j=0
    for i in data:
        if(fromunit=='API' and tounit=='SI'):
            convertpipedata.append({'data':round(i['data']/12/3.281*1000,3),'databasevalue':i['data']})          
        else:
            convertpipedata.append({'data':i['data'],'databasevalue':i['data']})
        j +=1
    return convertpipedata
def getmd(request,measured_depth): 
    data=measured_depth
    welltrajectory=WellTrajectory.objects.filter(measured_depth=data,company=request.company)
    if(welltrajectory.count()>0):
        val=round(welltrajectory[0].true_vertical_depth,2)
    else:
        belowmd=WellTrajectory.objects.filter(measured_depth__lte=data,company=request.company).order_by('-measured_depth')[:1].first()
        # print("few")
        # print(belowmd)
        abovemd=WellTrajectory.objects.filter(measured_depth__gte=data,company=request.company).order_by('measured_depth')[:1].first()
        alltvd=[]
        allmd=[]
        alltvd.append(belowmd.true_vertical_depth)
        alltvd.append(abovemd.true_vertical_depth)
        allmd.append(belowmd.measured_depth)
        allmd.append(abovemd.measured_depth)
        # print(alltvd)
        # print(allmd)
        interpolate_value = data
        y_interp = interp1d(allmd, alltvd)
        interpolate_value=y_interp(interpolate_value)
        rounded = format(interpolate_value,".2f")
        # print(interpolate_value)
        # print(rounded)
        # alltvd_series = pd.Series(alltvd)
        # tvd_interploate=alltvd_series.interpolate(method='index')
        val=rounded
    return val

# userlog = Userlog.objects.get(pk=id)
# new_datetime = datetime(2023, 6, 13, 2, 33)

def adduserlog(message,request,source_id,source_Type,licence_type,project_id,well_id,well_phase_id,userlog_type=None):
    if(request.user.is_superadmin):
        Userlog.objects.create(message=message,user_id=request.user.id,source_id=source_id,source_Type=source_Type,is_superadmin=1,status=1,userlog_type=userlog_type)
    else:
        from_id=request.user.company_id if request.user.licence_type != 'Individual' else request.user.individual_id 
        Userlog.objects.create(message=message,user_id=request.user.id,source_id=source_id,source_Type=source_Type,from_id=from_id,licence_type=licence_type,project_id=project_id,well_id=well_id,wellphase_id=well_phase_id,status=1,userlog_type=userlog_type)


        
def getprojidbywellid(well_id):
    proj_id = Wells.objects.get(id=well_id).project_id
    return proj_id

def converttofloat(value):
    return float(value)

def getmodaltext(selectedmodal):
    if(selectedmodal=="1"):
        modal="Newtonian"
    elif(selectedmodal=="2"):
        modal="Bingham"
    elif(selectedmodal=="3"):
        modal="Power Law"
    else:
        modal="Hershel bulkley"
    return modal

def  getcountries(company):
    projects=Projects.objects.filter(company=company).values('country').annotate(Count('country'))
    countrylist=[]
    for project in projects:
        country=Countries.objects.filter(id=project['country']).first()
        countrylist.append({'name':country.name,'id':country.id})
    return countrylist


        
    

