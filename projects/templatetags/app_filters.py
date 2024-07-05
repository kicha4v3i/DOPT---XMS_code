from django import template
from muddata.models import MudData,Rheogram,RheogramNameModels,RheogramDate,MudType,Sections,RheogramSections,HydraulicData,Pressureloss_data
from bhadata.models import BhaData,BhaElement,Drillcollers,Drillpipe,DrillpipeHWDP,Specifications,Pressuredroptool,Empirical,Differential_pressure
from projects.models import Projects,ProjectBlock,ProjectField
from projects.views import permission
from ticket.models import Tickets
from custom_auth.models import Userlog
import json
from wells.models import Wells
from custom_auth.getunit import getprojectunit
from django.db.models import F,Count, Min, Sum, Avg , Max
from math import sqrt,pow,log10
import numpy as np
from scipy.optimize import curve_fit,fsolve
from sklearn.linear_model import LinearRegression
from scipy.optimize import newton,root_scalar
from scipy import interpolate
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import time
from drillbitdata.models import DrillBit,DrillBitNozzle,BitTypesNames
from django.contrib.auth.models import Group
from notifications.models import *
from helpers import *
from helpers.allmodels import ProjectUsers,User,Rights,Companies,Modules,Enquiry,WellUsers,Wells 
from rig.models import Rig
register = template.Library()
from django.contrib import messages
from custom_auth.getunit import getprojidbywellid
from datetime import datetime




@register.filter(name='depthunit')
def depthunit(data, unit):
    if unit =="SI":
        return str(data)+" m"
    else:
        return str(data)+" ft"

@register.simple_tag
def display_depthunit(unit):
    if unit =="SI":
        return "m"
    else:
        return "ft"


@register.filter(name='lengthunit')
def lengthunit(data, unit):
    if unit =="SI":
        return str(data)+" m"
    else:
        return str(data)+" ft"

@register.simple_tag
def display_lengthunit(unit):
    if unit =="SI":
        return "m"
    else:
        return "ft"

@register.filter(name='diameterunit')
def diameterunit(data, unit):
    if unit =="SI":
        return str(data)+" mm"
    else:
        return str(data)+" in"

@register.simple_tag
def display_diameterunit(unit):
    if unit =="SI":
        return "(mm)"
    else:
        return "(in)"

@register.simple_tag
def display_diameter(unit):
    if unit =="SI":
        return " mm"
    else:
        return " in"
        
@register.filter(name='pressureunit')
def pressureunit(data, unit):
    if unit =="SI":
        return str(data)+" kPa"
    else:
        return str(data)+" psi"

@register.simple_tag
def display_pressureunit(unit):
    if unit =="SI":
        return "kPa"
    else:
        return "psi"

@register.filter(name='flowrateunit')
def flowrateunit(data, unit):
    if unit =="SI":
        return str(data)+" LPM"
    else:
        return str(data)+" GPM"

@register.simple_tag
def display_flowrateunit(unit):
    if unit =="SI":
        return "LPM"
    else:
        return "GPM"

@register.filter(name='severityunit')
def severityunit(data, unit):
    if unit =="SI":
        return str(data)+" °/30 m"
    else:
        return str(data)+" °/100 ft"

@register.simple_tag
def display_severityunit(unit):
    if unit =="SI":
        return "(°/30 m)"
    else:
        return "(°/100 ft)"

@register.filter(name='densityunit')
def densityunit(data, unit):
    if unit =="SI":
        return str(data)+" g/cc"
    else:
        return str(data)+" ppg"

@register.simple_tag
def display_densityunit(unit):
    if unit =="SI":
        return " (g/cc)"
    else:
        return " (ppg)"


@register.filter(name='gelstrengthunit')
def gelstrengthunit(data, unit):
    if unit =="SI":
        return str(data)+" Pa"
    else:
        return str(data)+" lbf/100ft2"

@register.simple_tag
def display_gelstrengthunit(unit):
    if unit =="SI":
        return " (Pa)"
    else:
        return " (lbf/100ft2)" 
     
@register.simple_tag
def display_dlsunit(unit):
    if unit =="SI":
        return "(°/30 m)"
    else:
        return "(°/100 ft)"

@register.filter(name='dlsunit')
def dlsunit(data, unit):
    if unit =="SI":
        return str(data)+" °/30 m"
    else:
        return str(data)+" °/100 ft"

@register.filter(name='plastic_viscosity')
def plastic_viscosity(unit,unitdata):
    if unit =="SI":
        return " Pa.sec"
    else:
        return " cP"

@register.filter(name='yield_point')
def yield_point(unit,unitdata):
    if unit =="SI":
        return " Pa"
    else:
        return " lbf/100ft2"

@register.filter(name='low_shear_rate')
def low_shear_rate(unit,unitdata):
    if unit =="SI":
        return " Pa"
    else:
        return " lbf/100ft2"

@register.simple_tag
def display_plastic_viscosity(unit):
    if unit =="SI":
        return " (Pa.sec)"
    else:
        return " (cP)"
@register.simple_tag
def display_yield_point(unit):
    if unit =="SI":
        return " Pa"
    else:
        return " lbf/100ft2"
@register.simple_tag
def display_low_shear_rate(unit):
    if unit =="SI":
        return " Pa"
    else:
        return " lbf/100ft2"
@register.simple_tag
def display_rop(unit):
    if unit =="SI":
        return " m/hr"
    else:
        return " ft/hr"

@register.filter(name='nozzle_size_unit')
def nozzle_size_unit(data, unit):
    if unit =="SI":
        return str(data)+" mm"
    else:
        return str(data)+" 1/32 in"

@register.simple_tag
def display_nozzle_size_unit(unit):
    if unit =="SI":
        return " (mm)"
    else:
        return " (1/32 in)"

@register.filter(name='tfa_unit')
def tfa_unit(data, unit):
    if unit =="SI":
        return str(data)+" mm\u00b2"
    else:
        return str(data)+" in\u00b2"

@register.simple_tag
def display_tfa_unit(unit):
    if unit =="SI":
        return " mm\u00b2"
    else:
        return " in\u00b2"

@register.simple_tag
def display_bhhp(unit):
    if unit == 'SI':
        return " kW"
    else:
        return " hp"

@register.simple_tag
def display_impactforce(unit):
    if unit == 'SI':
        return " N"
    else:
        return " lbf"

@register.filter(name='changeporepressureunit')
def changeporepressureunit(data, og_unit):
    ig_unit=data.pressure_unit
    pressure=data.pore_pressure
    tvd=data.true_vertical_depth

    if(ig_unit==og_unit):
        disp= pressure 
    if(ig_unit=="psi" and og_unit=="ppg"):
        disp= pressure/(0.052 * tvd) 
    if(ig_unit=="psi" and og_unit=="psi/ft"):
        disp= pressure * tvd        
    if(ig_unit=="ppg" and og_unit=="psi"):
        disp= 0.052 * pressure * tvd
    if(ig_unit=="ppg" and og_unit=="psi/ft"):
        disp= 0.052 * pressure  
    if(ig_unit=="psi/ft" and og_unit=="ppg"):
        disp= pressure/0.052
    if(ig_unit=="psi/ft" and og_unit=="psi"):
        disp= pressure * tvd        

    if(ig_unit=="g/cc" and og_unit=="kPa"):
        disp= 9.80665 * pressure * tvd
    if(ig_unit=="kPa" and og_unit=="g/cc"):
        disp= pressure/(9.80665 * tvd)       
    if(ig_unit=="g/cc" and og_unit=="kPa/m"):
        disp= 9.80665 * pressure       
    if(ig_unit=="kPa" and og_unit=="kPa/m"):
        disp= pressure/tvd       
    if(ig_unit=="kPa/m" and og_unit=="g/cc"):
        disp= pressure/9.80665    
    if(ig_unit=="kPa/m" and og_unit=="kPa"):
        disp= pressure * tvd    
     
    return ('%6.2f' % disp)

@register.filter(name='changefracpressureunit')
def changefracpressureunit(data, og_unit):
    ig_unit=data.pressure_unit
    pressure=data.fracture_pressure
    tvd=data.true_vertical_depth

    if(ig_unit==og_unit):
        disp= pressure 
    if(ig_unit=="psi" and og_unit=="ppg"):
        disp= pressure/(0.052 * tvd) 
    if(ig_unit=="psi" and og_unit=="psi/ft"):
        disp= pressure * tvd        
    if(ig_unit=="ppg" and og_unit=="psi"):
        disp= 0.052 * pressure * tvd
    if(ig_unit=="ppg" and og_unit=="psi/ft"):
        disp= 0.052 * pressure   
    if(ig_unit=="psi/ft" and og_unit=="ppg"):
        disp= pressure/0.052
    if(ig_unit=="psi/ft" and og_unit=="psi"):
        disp= pressure * tvd        

    if(ig_unit=="g/cc" and og_unit=="kPa"):
        disp= 9.80665 * pressure * tvd
    if(ig_unit=="kPa" and og_unit=="g/cc"):
        disp= pressure/(9.80665 * tvd)       
    if(ig_unit=="g/cc" and og_unit=="kPa/m"):
        disp= 9.80665 * pressure       
    if(ig_unit=="kPa" and og_unit=="kPa/m"):
        disp= pressure/tvd       
    if(ig_unit=="kPa/m" and og_unit=="g/cc"):
        disp= pressure/9.80665    
    if(ig_unit=="kPa/m" and og_unit=="kPa"):
        disp= pressure * tvd  

    return ('%6.2f' % disp)

@register.filter
def getrheogram(rheogram,section_id):
    return Rheogram.objects.filter(rheogram_sections_id =section_id)

@register.filter
def getmuddata(data,field):
    field_data=MudData.objects.filter(todepth=data.todepth,well_id=data.well_id,status=1).values(field)
    if(field_data.count()==0):
        return ''
    else:
        if(field_data[0][field]==None):
            return ''
        else:
         return field_data[0][field]

@register.filter
def getrheogramdata_actual(rheogram,section):
    muddata=MudData.objects.filter(todepth=section.todepth,well_phase_id=section.well_phase_id,status=1).first()
    rheogramdate=RheogramDate.objects.filter(muddata_id=muddata.id).first()
    rheogram=Rheogram.objects.filter(rheogram_date_id=rheogramdate.id,rpm=rheogram['rpm']).first()
    return rheogram
   

@register.filter
def getmuddatadate(data,field):
    field_data=MudData.objects.filter(section=data.section_name,well_id=data.well_id,status=1).values(field)
    if(field_data.count()==0):
        return ''
    else:
        if(field_data[0][field]==None):
            return ''
        else:
            converted_date=datetime.datetime.strftime(field_data[0][field], '%d-%m-%Y')
            return converted_date

@register.filter
def getmuddatatime(data,field):
    field_data=MudData.objects.filter(section=data.section_name,well_id=data.well_id,status=1).values(field)
    if(field_data.count()==0):
        return ''
    else:
        if(field_data[0][field]==None):
            return ''
        else:
            converted_time=datetime.time.strftime(field_data[0][field], '%H:%M')
            return converted_time

@register.filter(name='getrheogram')
def getrheogramsections(section,well_phase_id):
    rheogram_section=RheogramSections.objects.filter(section_name=section.section_name,well_phase_id=well_phase_id,status=1).values('id')
    if(rheogram_section.count()==0):
        return RheogramNameModels.objects.values('rheogram_rpm').annotate(rpm = F('rheogram_rpm'))
    else:
        return Rheogram.objects.filter(rheogram_sections_id=rheogram_section[0]['id'],status=1).values('rpm','dial','id')

@register.filter(name='getrheogramsectionid')
def getrheogramsectionid(section,section_name):
    rheogram_section=RheogramSections.objects.filter(section_name=section.section_name,status=1).values('id')
    if(rheogram_section.count()==0):
        return ""
    else:
        return rheogram_section[0]['id']

@register.filter(name='getviscocity')
def getviscocity(section,section_name):
    muddata=MudData.objects.filter(section=section.section_name,well_phase_id=section.well_phase_id).values('plastic_viscosity')
    if(muddata.count()==0):
        return ""
    else:
        return muddata[0]['plastic_viscosity']

@register.filter(name='checkmuddata')
def checkmuddata(section,section_name):
    muddata=MudData.objects.filter(section=section.section_name,well_phase_id=section.well_phase_id,status=1).first()
    if(muddata.plastic_viscosity == None and muddata.yield_point == None and muddata.low_shear_rate == None):
        return ""
    else:
        return muddata.plastic_viscosity

@register.simple_tag
def getsectionbywellphase_id(wellphase_id):
    sections=Sections.objects.filter(well_phase_id=wellphase_id,status=1)
    return sections

# @register.filter(name='getprojectby_countryid')
# def getprojectby_countryid(country_id,company):
 

#     projectlist=Projects.objects.filter(country_id=country_id,company=company).prefetch_related('projectusers_set')
#     return projectlist

@register.simple_tag
def getprojectby_countryid(country_id,request):
    if(request.user.licence_type != 'Individual'):
        if(request.user.is_admin==1):
            filter_condition = {'country_id': country_id, 'company_id': request.company.id,'status':1}
        else:
            filter_condition = {'country_id': country_id, 'company_id': request.company.id, 'status':1,'projectusers__user_id': request.user.id,'projectusers__status':1}
        projectlist=Projects.objects.filter(**filter_condition).prefetch_related('projectusers_set')
    else:
        projectlist=Projects.objects.filter(country_id=country_id,created_by_id=request.user.id,status=1).prefetch_related('projectusers_set')

    return projectlist


@register.filter(name='getprojectfield')
def getprojectfield(block_id,project_id):
    fieldlist=ProjectField.objects.filter(project_id=project_id,block_id=block_id,status=1)
    return fieldlist

@register.filter(name='changeint')
def changeint(data):
    return int(data)

@register.filter(name='getblockby_projectid')
def getblockby_projectid(project_id,project):
    blocklist=ProjectBlock.objects.filter(project_id=project_id,status=1)
    return blocklist

@register.filter(name='getfieldby_blockid')
def getfieldby_blockid(block_id,block):
    fieldlist=ProjectField.objects.filter(block_id=block_id,status=1)
    return fieldlist

@register.simple_tag
def getwellby_fieldid(field_id,request,project_id):
    if(request.user.licence_type != 'Individual'):
        checkuserexist_inproject=ProjectUsers.objects.checkuserexist(project_id,request.user.id)
        if(request.user.is_admin==1 or checkuserexist_inproject.count() > 0):
            filter_condition = {'field_id': field_id, 'status': 1}
        else:
            filter_condition = {'field_id': field_id, 'status': 1,'wellusers__user_id': request.user.id,'wellusers__status': 1}
        welllist=Wells.objects.filter(**filter_condition).prefetch_related('wellusers_set')
    else:
        welllist=Wells.objects.filter(field_id=field_id,status=1)
    return welllist

@register.simple_tag
def getcalculateddial(rpm,section,modal,well_id):
    section_name=section.section_name
    wellphase_id=section.well_phase_id
    dial=0
    unit = getprojectunit(well_id)
    if(modal=='newtonian'):
        muddata=MudData.objects.filter(section=section_name,well_phase_id=wellphase_id,well_id=well_id,status=1).first()
        if(muddata.plastic_viscosity != None):
            if unit == 'API':
                dial=round((muddata.plastic_viscosity/1000*0.02088*100*int(rpm)*1.703)/1.066) 
            else:
                plastic_viscosity=muddata.plastic_viscosity*1000
                dial=round((plastic_viscosity/1000*0.02088*100*int(rpm)*1.703)/1.066)
    elif(modal=='bingham'):
        muddata=MudData.objects.filter(section=section_name,well_phase_id=wellphase_id,status=1).first()
        if(muddata.plastic_viscosity != None and muddata.yield_point != None):
            if unit == 'API':
                dial=round(muddata.plastic_viscosity/1000*0.02088*100*int(rpm)*1.703/1.066+muddata.yield_point)
            else:
                plastic_viscosity=muddata.plastic_viscosity*1000
                yield_point = muddata.yield_point/0.4788
                dial=round(plastic_viscosity/1000*0.02088*100*int(rpm)*1.703/1.066+yield_point)
    elif(modal=='powerlaw'):
        muddata=MudData.objects.filter(section=section_name,well_phase_id=wellphase_id,status=1).first()
        if(muddata.plastic_viscosity != None and muddata.yield_point != None):
            if unit == 'API':
                t300=muddata.plastic_viscosity+muddata.yield_point
                t600=t300+muddata.plastic_viscosity
            else:
                plastic_viscosity=muddata.plastic_viscosity*1000
                yield_point = muddata.yield_point/0.4788
                t300=plastic_viscosity+yield_point
                t600=t300+plastic_viscosity
            n=3.32*log10(t600/t300)
            k_pl=t300/pow(511,n)
            dial=round(k_pl*pow((int(rpm)*1.703),n))
    elif(modal=='hershel'):
        muddata=MudData.objects.filter(section=section_name,well_phase_id=wellphase_id,status=1).first()
        if(muddata.plastic_viscosity != None and muddata.yield_point != None and muddata.low_shear_rate != None):
            if unit == 'API':
                plastic_viscosity = muddata.plastic_viscosity
                yield_point = muddata.yield_point
                low_shear_rate = muddata.low_shear_rate
            else:
                plastic_viscosity = muddata.plastic_viscosity*1000
                yield_point = muddata.yield_point/0.4788
                low_shear_rate = muddata.low_shear_rate/0.4788
            t300=plastic_viscosity + yield_point
            t600=t300+plastic_viscosity
            m=3.32*log10((t600-low_shear_rate)/(t300-low_shear_rate))
            k_hb=(t300-low_shear_rate)/pow(511,m)
            dial=round(low_shear_rate+k_hb*pow((int(rpm)*1.703),m))
    return dial

@register.simple_tag
def getrheogrambymodels(rpm,section,modal,well_id,wellphase_id):
    rheogram_section=RheogramSections.objects.filter(section_name=section.section_name,well_phase_id=wellphase_id,status=1).values('id')
    rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogram_section[0]['id'],well_id=well_id,status=1,rpm=rpm).values('rpm','dial','id')
    if(rheogram.count()==0):
        if(modal!='None'):
            return getcalculateddial(rpm,section,modal,well_id)
        else:
            return ""
    else:
        return rheogram[0]['dial']

@register.filter('timestamp_to_time')
def convert_timestamp_to_time(timestamp,date):
    converted_date=datetime.datetime.fromtimestamp(int(timestamp))
    converted_date=datetime.datetime.strftime(converted_date, '%d-%m-%Y %H:%M')
    return converted_date

@register.filter('getmuddataid')
def getmuddataid(section,wellphase_id):
    muddata=MudData.objects.filter(todepth=section.todepth,well_phase_id=wellphase_id).first()
    return muddata.id


@register.filter('getbhaelement')
def getbhaelement(bha,bhadata):
    bhaelement=BhaElement.objects.filter(bhadata_id=bha.id)
    return bhaelement  

@register.simple_tag
def getuserrights(value1,value2,company_id):
    rights = Rights.objects.getuserrights_company(value1.id,value2,1,company_id)
    return rights

@register.simple_tag
def getpoauserrights(module_id,user_id):
    rights = Rights.objects.checkpoauserrights(user_id,module_id)
    if(rights.count()>0):
        if(rights[0].status==1):
            return True
        else:
            return False
    

@register.simple_tag
def getcreateedit(company):
    print('cccc',company.id)
    rights = Rights.objects.filter(company_id=company.id).exists()
    if rights == True:
        return "edit"
    else:
        return "create"


@register.filter('get_hydraulic_data_by_month')
def get_hydraulic_data_by_month(hydraulic_data,wellphase_id):
    getdata=HydraulicData.objects.filter(date__month=hydraulic_data['month'],well_phase_id=wellphase_id).values('date').annotate(total=Count('*'))
    # print(f"data {hydraulic_data['month']}") 
    # print(f"getdata {getdata}")
    return getdata

@register.filter('getmd')
def getmd(bha_id,bha):
    bhaelement=BhaElement.objects.filter(bhadata_id=bha_id).order_by('-id').first()
    return bhaelement.length_onejoint

@register.filter('getmonth_string')
def getmonth_string(month_data,month):
    month=['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return month[month_data]


@register.filter('getmonthdata')
def getmonthdata(hydraulic_data,wellphase_id):
    getdata=HydraulicData.objects.filter(date=hydraulic_data['date'],well_phase_id=wellphase_id)
    return getdata

@register.filter('getbittype')
def getbittype(bitdata,drllbit):
    bittype=BitTypesNames.objects.filter(id=bitdata).first()
    return bittype.bittype_names

@register.filter('getnozzle')
def getnozzle(drillbitid,drllbit):
    nozzle=DrillBitNozzle.objects.filter(drillbit_id=drillbitid)
    return nozzle

@register.filter('getbha')
def getbha(bha,drllbit):
    print(f"bha {bha}")
    if bha == None:
        return None
    else:
        bha=BhaData.objects.filter(id=bha).first()
        return bha.bhaname

@register.filter('getrheogram_actual')
def getrheogram_actual(rheogramdate,data):
    rheogramdate=RheogramDate.objects.filter(muddata_id=rheogramdate['id']).first()
    rheogram=Rheogram.objects.filter(rheogram_date_id=rheogramdate.id,status=1)
    return rheogram

    

@register.simple_tag
def getpvyp(section,wellphase_id,typename):
    muddata=MudData.objects.filter(section=section.section_name,well_phase_id=wellphase_id,status=1).first()
    unit=getprojectunit(muddata.well_id)
    rheogramsections=RheogramSections.objects.filter(well_phase_id=wellphase_id,section_name=section.section_name,status=1).first()
    if(rheogramsections !=None):
        rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id)
        dial_600=0
        dial_300=0
        userenterdial=[]
        rpm=[]
        for rheo in rheogram:
            if(rheo.rpm==300):
                dial_300=float(rheo.dial)
            elif(rheo.rpm==600):
                dial_600=float(rheo.dial)
            if(rheo.dial):
                rpm.append(rheo.rpm)
                userenterdial.append(float(rheo.dial))
        section_name = Sections.objects.filter(well_phase_id=wellphase_id,status=1).first()
        if typename=='plastic_viscocity':
            if(muddata.plastic_viscosity==None):
                plastic_viscosity=(dial_600-dial_300)
                val=round(viscosity_conversion(plastic_viscosity,unit),2)
            else:
                val=muddata.plastic_viscosity
        elif typename=='yield_point':
            if(muddata.yield_point==None):
                if section_name.selected_model != '1':
                    plastic_viscosity=dial_600-dial_300
                    yield_point=(dial_300-plastic_viscosity)
                    val=round(yieldpoint_conversion(yield_point,unit),2)
                else: val=''
            else:
                val=muddata.yield_point
        else:
            if(muddata.low_shear_rate==None):
                if section_name.selected_model == '4':
                    userrpm=[int(i) for i in rpm]
                    userdial=[float(j) for j in userenterdial]
                    hershelmodal=gethershel_modal(unit,userrpm,userdial,muddata.plastic_viscosity,muddata.yield_point,muddata.low_shear_rate,dial_300,dial_600)
                    val=round(hershelmodal['Ty'],2)
                else: val=''
            else:
                val=muddata.low_shear_rate
        return val
    else:
        if typename=='plastic_viscocity':
            val=muddata.plastic_viscosity
        elif typename=='yield_point':
            val=muddata.yield_point
        else:
            val=muddata.low_shear_rate
        return val


@register.simple_tag
def get_low_shear_rate(section,wellphase_id):
    muddata=MudData.objects.filter(section=section.section_name,well_phase_id=wellphase_id).first()
    rheogramsections=RheogramSections.objects.filter(well_phase_id=wellphase_id,section_name=section.section_name,status=1).first()
    if(rheogramsections !=None):
        if(muddata.low_shear_rate!=None):
            val=muddata.low_shear_rate
        else:
            if(section.selected_model=='4'):
                rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=None)
                rpm=[]
                dial=[]
                for rheogramdata in rheogram:
                    if rheogramdata.dial!='':
                        rpm.append(rheogramdata.rpm)
                        dial.append(float(rheogramdata.dial))
                X=np.array(rpm).reshape(-1,1)
                Y=np.array(dial).reshape(-1,1)
                popt,pcov=curve_fit(f,np.squeeze(X.T).tolist(),np.squeeze(Y.T).tolist(),maxfev=10000)
                m,Ty,K_HB=popt[0],popt[1],popt[2]
                val=round(Ty,1)
            else:
                val=""
        return val
    
def f(x,n,Ty,K):
    return Ty+K*x**n

@register.simple_tag
def getrheogramid(rpm,section,modal):
    rheogram_section=RheogramSections.objects.filter(section_name=section.section_name,status=1).values('id')
    rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogram_section[0]['id'],status=1,rpm=rpm).values('rpm','dial','id')
    if(rheogram.count()==0):
        return ""
    else:
        return rheogram[0]['id']

# @register.simple_tag
# def getrheogram_section(section):
#     rheogram_section=RheogramSections.objects.filter(section_name=section.section_name).values('id')
#     return rheogram_section[0]['id']



@register.simple_tag
def getflowtestspecifications(bhaelementid,bhaid):
    specification=Specifications.objects.filter(bhadata_id=bhaid,bhadata_element_id=bhaelementid).first()
    return specification 

@register.simple_tag
def getflowtestpressuredrop(bhaelementid,bhaid):
    pressuredrop=Pressuredroptool.objects.filter(bhadata_id=bhaid,bhadata_element_id=bhaelementid,status=1)
    return pressuredrop 

@register.simple_tag
def getempirical(bhaelementid,bhaid):
    empirical=Empirical.objects.filter(bhadata_id=bhaid,bhadata_element_id=bhaelementid).first()
    return empirical

@register.simple_tag
def getdiff_pressure(bhaelementid,bhaid):
    differential_pressure=Differential_pressure.objects.filter(bhadata_id=bhaid,bhadata_element_id=bhaelementid,status=1)
    return differential_pressure 

@register.simple_tag
def display_weightunit(unit):
    if unit =="SI":
        return "N/m"
    else:
        return "ppf"

# @register.filter(name='getcalculateddial')
# def getcalculateddial(section,args):
#     print(section.section_name)
#     print(args)

    # print(args)

    # section_name=section.section_name
    # wellphase_id=section.well_phase_id
    # rheogram_rpm= RheogramNameModels.objects.all()
    # rpm=[int(rpm.rheogram_rpm) for rpm in rheogram_rpm]
    # # print(rpm)
    # newtoniandial=[]
    # binghamdial=[]
    # powerlawdial=[]
    # hersheldial=[]
    # muddata=MudData.objects.filter(section=section_name,well_phase_id=wellphase_id).first()
    # if(muddata.plastic_viscosity != None):
    #     for rheorpm in rpm:
    #         dial=(muddata.plastic_viscosity/1000*0.02088*100*rheorpm*1.703)/1.066 
    #         newtoniandial.append(round(dial))
    
    # muddata=MudData.objects.filter(section=section_name,well_phase_id=wellphase_id).first()
    # if(muddata.plastic_viscosity != None and muddata.yield_point != None):
    #     for rheorpm in rpm:
    #         dial=(muddata.plastic_viscosity/1000*0.02088*100*rheorpm*1.703/1.066+muddata.yield_point)
    #         binghamdial.append(round(dial))
    
    # muddata=MudData.objects.filter(section=section_name,well_phase_id=wellphase_id).first()
    # if(muddata.plastic_viscosity != None and muddata.yield_point != None):
    #     t300=muddata.plastic_viscosity+muddata.yield_point
    #     t600=t300+muddata.plastic_viscosity
    #     n=3.32*log10(t600/t300)
    #     k_pl=t300/pow(511,n)
    #     for rheorpm in rpm:
    #         dial=k_pl*pow((rheorpm*1.703),n)
    #         powerlawdial.append(round(dial))
    
    # muddata=MudData.objects.filter(section=section_name,well_phase_id=wellphase_id).first()
    # if(muddata.plastic_viscosity != None and muddata.yield_point != None and muddata.low_shear_rate != None):
    #     t300=muddata.plastic_viscosity+muddata.yield_point
    #     t600=t300+muddata.plastic_viscosity
    #     m=3.32*log10((t600-muddata.low_shear_rate)/(t300-muddata.low_shear_rate))
    #     k_hb=(t300-muddata.low_shear_rate)/pow(511,m)
    #     for rheorpm in rpm:
    #         dial=muddata.low_shear_rate+k_hb*pow((rheorpm*1.703),m)
    #         hersheldial.append(round(dial))
    # data={
    #     'newtoniandial':newtoniandial,
    #     'binghamdial':binghamdial,
    #     'powerlawdial':powerlawdial,
    #     'hersheldial':hersheldial
    # }
    # print("fbgfbgf")
    # print(data)
    # return data
def gethershel_modal(unit,rpm,userenterdial,plastic_viscosity,yieldpoint,low_shear_rate,dial_300,dial_600,rheogramsectionsid=''):
    newdial=[]
    if(plastic_viscosity==None):
        X=np.array(rpm).reshape(-1,1)
        Y=np.array(userenterdial).reshape(-1,1)
        popt,pcov=curve_fit(f,np.squeeze(X.T).tolist(),np.squeeze(Y.T).tolist(),maxfev=10000)
        m,Ty,K_HB=popt[0],popt[1],popt[2]
        K=K_HB
        n=m  
        last_rpm=rpm[-1:]
        dial_300 = 0
        dial_600 = 0
        for i in range(last_rpm[0]+1):
            y=round(Ty+K_HB*i**m,2)
            newdial.append([i, y])
            if(i==300):
                dial_300=y
            elif(i==600):
                dial_600=y
        plastic_viscosity=dial_600-dial_300
        yieldpoint=dial_300-round(plastic_viscosity,2)
        rms=0
        j=0
        while j < len(rpm):
            new_dial=Ty+K_HB*pow(rpm[j],m)
            difference=(userenterdial[j]-new_dial)**2
            rms +=difference
            j += 1
        rmsvalue=round((sqrt(rms/len(rpm))),2)
    else:
        rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsectionsid,modelname='hershel')
        last_rpm=rpm[-1]
        if unit == 'API':
            plastic_viscosity = plastic_viscosity
            yieldpoint = yieldpoint
            low_shear_rate = low_shear_rate
        else:
            plastic_viscosity = plastic_viscosity*1000
            yieldpoint = yieldpoint/0.4788
            low_shear_rate = low_shear_rate/0.4788
        t300=plastic_viscosity+yieldpoint
        t600=t300+plastic_viscosity
        m=3.32*log10((t600-low_shear_rate)/(t300-low_shear_rate))
        k_hb=(t300-low_shear_rate)/pow(511,m)
        K=k_hb
        n=m
        for i in range(0,last_rpm+1):
            y=round(low_shear_rate+k_hb*i**m,2)
            newdial.append([i, y])
        rmsvalue=''
        Ty=0
    data={
        'modal':newdial,
        'rmsvalue':rmsvalue,
        'plastic_viscosity':plastic_viscosity,
        'yieldpoint':yieldpoint,
        'K':K,
        'n':n,
        'Ty':Ty
    }
    return data

@register.filter
def getdrilldate(data,field):
    field_data=DrillBit.objects.filter(id=data.id,well_id=data.well_id,well_phases_id=data.well_phases).values(field)
    if(field_data.count()==0):
        return ''
    else:
        if(field_data[0][field]==None):
            return ''
        else:
            converted_date=datetime.datetime.strftime(field_data[0][field], '%d-%m-%Y')
            return converted_date

@register.filter
def getdrilltime(data,field):
    field_data=DrillBit.objects.filter(id=data.id,well_id=data.well_id,well_phases_id=data.well_phases).values(field)
    if(field_data.count()==0):
        return ''
    else:
        if(field_data[0][field]==None):
            return ''
        else:
            converted_time=datetime.time.strftime(field_data[0][field], '%H:%M')
            return converted_time

@register.filter
def getdatas(wellphase_id,well_id):
    print(f'wellphase_id{wellphase_id}')
    print(f'well_id{well_id}')
    section=Sections.objects.filter(well=well_id,well_phase_id=wellphase_id,status=1).first()
    print(section)
    if(section):
        muddata=MudData.objects.filter(section=section.section_name,well_phase=wellphase_id,well=well_id,status=1)
    else:
        muddata=0
    print(muddata)
    # data['muddata']=muddata
    # data['drillbit']=drillbit
    return muddata


@register.simple_tag
def getcummulative(wellphase_id,section_name,well_id,index):
    pressure=Pressureloss_data.objects.filter(well_id=well_id,section_name=section_name,well_phase_id=wellphase_id).first()
    cummulative_data=[]
    cummulatives=1
    for data in reversed(pressure.all_data['data']['annularpressureloss']):
        cummulatives=cummulatives+data['length_against']
        cummulative_data.append(round(cummulatives))
    return cummulative_data[index-1]

@register.simple_tag
def getsummary(section,wellphase_id,well_id,type):
    pressure=Pressureloss_data.objects.filter(well_id=well_id,section_name=section.section_name,well_phase_id=wellphase_id).first()
    total_surface=0
    total_annular=0
    total_drillstring=0
    total_bit=0
    totalpressure_loss=[]
    data=0
    if(pressure is not None):
        if(type=='surface'):
            for surface in pressure.all_data['data']['surfacelosses']:
                data+=round(surface['pressureloss'])
        elif(type=='drillstring'):
            for annular in pressure.all_data['data']['annularpressureloss']:
                data+=round(annular['drillstringloss'])
        elif(type=='annular'):
            for annular in pressure.all_data['data']['annularpressureloss']:
                data+=round(annular['pressureloss'])
        elif(type=='bit_pressure'):
            for bit in pressure.all_data['data']['bitpressurelosses']:
                data+=round(bit['bit_pressure_loss'])
        else:
            for surface in pressure.all_data['data']['surfacelosses']:
                total_surface+=round(surface['pressureloss'])
            for annular in pressure.all_data['data']['annularpressureloss']:
                total_annular+=round(annular['pressureloss'])
                total_drillstring+=round(annular['drillstringloss'])
            for bit in pressure.all_data['data']['bitpressurelosses']:
                total_bit+=round(bit['bit_pressure_loss'])
            data=total_surface+total_annular+total_drillstring+total_bit
    return data

@register.simple_tag
def checkproject_permission(projectrights_users_list,projectrights_wells_list,module_id,permission_type):
    print(f"projectrights_users_list {projectrights_users_list}")

# @register.simple_tag    
# def users_rights(userid,projectid,module,type):
#     permission=Userrights.objects.filter(user_id=userid,project_id=projectid,module_id=module,status=0).values(type).first()
#     if permission:
#         return permission[type]
#     else:
#         return ''

# @register.simple_tag    
# def input_rights(userid,projectid,module,wellid,type):
#     permission=Userrights.objects.filter(user_id=userid,project_id=projectid,module_id=module,well_id=wellid,status=0).values(type).first()
#     if permission:
#         return permission[type]
#     else:
#         return ''

import ast


@register.simple_tag 
def getsendername(sender_id):
    print('sender_id',sender_id)
    users = User.objects.getuserid(sender_id)
    users_type = users.licence_type
    if(users_type == "Individual"):
        print('lllss',users.name)
        return users.name
    else:
        users_cid = users.company_id
        company = Companies.objects.getcompanyname_byid(users_cid)
        print('llltt',company)
        return company.company_name

@register.simple_tag 
def getEnquiries(user,license_type):
    enquiries = Enquiry.objects.filter(user_type_id=user.id,status=0)
    return enquiries

    


@register.simple_tag 
def geturlname(value):
    

    if (value != None):
        parsed_data = json.loads(value)
        url = parsed_data['url']
        return url
    #     data=value.get('url')
  
        # geturl=ast.literal_eval(data)
        # print(f'geturl {geturl.get("url")}')
        # return geturl.get('url')
    return ""
# register.filter('geturlname',geturlname)

@register.simple_tag 
def getuservalues(type_val,type_id):
    print(type_val)
    if(type_val == "CompanyPlan" or type_val == "Enterprise"):
        company = Companies.objects.get(id=type_id)
        context={
            'firstname':company.first_name,
            'lastname':company.last_name,
            'email':company.email,
            'company_name':company.company_name 
            
        }
    else:
        user = User.objects.get(id=type_id) 
        context={
            'firstname':user.name,
            'lastname':user.lastname,
            'email':user.email,
            'company_name':""

        }

    return context
  
@register.simple_tag 
def geturlid(value):

    if (value != None):
        data=value.get('data')
        getid=ast.literal_eval(data)
        print(f'getuid {getid.get("id")}')
        return getid.get('url')
    return ""

@register.filter
def get_user_roles(user_id):
    user = User.objects.get(id=user_id)
    groups = user.groups.all()
    for group in groups:
        return group.name
    

@register.simple_tag
def user_rights_permission(privilege,request):
    if request.user.individual_id:
        return True
    user = User.objects.get(pk=request.user.id)
    group = user.groups.first()
    module = Modules.objects.filter(name=privilege).first()

    if group:
        module_id = module.id
        check = Rights.objects.filter(company_id=request.user.company_id,module_id=module_id,role_id=group.id,status=1).exists()
        if group.name == "Admin":
            check = True
        return check 
    
    return False
@register.simple_tag 
def user_rights_permission_changeusertype(privilege,request,user_id):
    if request.user.individual_id:
        return True
    user = User.objects.get(pk=user_id)
    group = user.groups.first()
    module = Modules.objects.filter(name=privilege).first()
    print('module_id',module.id,user_id)
    if group:
        module_id = module.id
        check = Rights.objects.filter(module_id=module_id,role_id=group.id,status=1).exists()
        print(privilege,check,group.id)
        if group.name == "Admin":
            check = True
        return check 
    
    return False




@register.simple_tag
def poauser_rights_permission(privilege,request):
    user = User.objects.get(pk=request.user.id)
    module = Modules.objects.filter(name=privilege).first()
    check = Rights.objects.checkpoa_userrights(user.id,module.id).exists()
    if user.is_superadmin == 1:
        check = True 
    return check
 
@register.simple_tag 
def check_useraccess(activity,activity_id,request):
    if request.role == "Admin":
        check = True
    if request.user.individual_id:
        return True
    if activity == 'project':
        user_ids = ProjectUsers.objects.filter(project_id=activity_id,status=1).values_list('user_id', flat=True)
        if request.user.id in user_ids:
            return True
        else:
            return False
    elif activity == 'well':
        user_ids_well = list(WellUsers.objects.filter(well_id=activity_id,status=1).values_list('user_id', flat=True)) 
        proj_id = Wells.objects.get(id=activity_id).project_id
        user_ids_proj = list(ProjectUsers.objects.filter(project_id=proj_id,status=1).values_list('user_id', flat=True))
        if (request.user.id in user_ids_well) or (request.user.id in user_ids_proj):
            return True 
        else:
            return False
    
@register.simple_tag
def CheckIsAdmin(request):
    user = User.objects.get(pk=request.user.id)
    group = user.groups.first()
    if group:
        return group.name
    return None


@register.simple_tag 
def getuserdetails_byid(request,id,source_id,source_type):
    user = User.objects.getuserid(id) 
    print('app_filters',id,source_id,source_type)
    context = {
        'user_name':user.name
    }
    return context

@register.simple_tag 
def getusers_project(user_id,project_id,company_id):
    users=[]
    users.append(user_id)
    projectusers=ProjectUsers.objects.getprojectusers(project_id)
    for projectuser in projectusers:
        users.append(projectuser.user_id)
    remaining_users=User.objects.exclude_projectusers(company_id,users)
    return remaining_users

@register.simple_tag 
def getusers_well(user_id,well_id,company_id):
    well_details=Wells.objects.getwell_byid(well_id)
    users=[]
    users.append(user_id)
    wellusers=WellUsers.objects.getwellusers(well_id)
    for welluser in wellusers:
        users.append(welluser.user_id)
    projectusers=ProjectUsers.objects.getprojectusers(well_details.project_id)
    for projectuser in projectusers:
        users.append(projectuser.user_id)
    remaining_users=User.objects.exclude_projectusers(company_id,users)
    return remaining_users
    
    
@register.simple_tag 
def getprojusername(user_id):
    print('user_id getprojusername',user_id)
    if(user_id):
        user = User.objects.getuserid(user_id)
        user_name = user.name 
        user_desig  = user.designation
        
        context= {
        
            'user_name':user_name,
            'user_desig':user_desig
        }
        return context
    else:
        return ""
    

@register.simple_tag 
def format_number(number):
    try:
        number = float(number)  
        formatted_number = "{:.2f}".format(number)
        return formatted_number
    except (ValueError, TypeError):
        return "" 
    
    
    
    
    
@register.simple_tag 
def getprojectusers(proj_id):
    print(f"proj_id {proj_id}")
    proj_users = ProjectUsers.objects.filter(project_id=proj_id,status=1)
    print(f"proj_users {proj_users}")
    return proj_users
    
@register.simple_tag     
def getwelllist(request, proj_id):
    if(request.user.licence_type == 'Individual'):
        wells = Wells.objects.getindividual_wells(proj_id,request.user.id)
    else:
        wells = Wells.objects.filter(company_id=request.company.id,project_id=proj_id,status=1)
    return wells

@register.simple_tag 
def getwellusers(well_id):
    well_users = WellUsers.objects.filter(well_id=well_id,status=1)
    return well_users  

@register.simple_tag 
def getuseractivity(activity,activity_id,user_id):
    print('activities',activity,activity_id,user_id)
    if activity=="project":
        userlog = Userlog.objects.filter(project_id=activity_id,user_id=user_id) 
        return userlog
    else:
        userlog = Userlog.objects.filter(well_id=activity_id,user_id=user_id) 
        print('getuseractivity',userlog)
        return userlog 

@register.simple_tag 
def getactivitydetails(activity):
    activity_type = activity.source_Type 
    act_id = activity.source_id 
    print('getactivitydetails',activity)
    if activity_type == "Rig":
        rig = Rig.objects.get(id=act_id) 
        print('rig_name',rig.rig_name)
        return activity.message +" named "+ rig.rig_name 

@register.simple_tag 
def getcountries(countries):
    return countries

@register.simple_tag 
def get_totalprojects(request,country_id):
    if request.company:
        return Projects.objects.filter(country_id=country_id,company_id=request.company.id,status=1).count()  
    else:
        return Projects.objects.filter(country_id=country_id,created_by_id=request.user.id,status=1).count()
          

@register.simple_tag 
def get_totalblocks(request,country_id):
    if request.company:
        project_ids = list(Projects.objects.filter(country_id=country_id,company_id=request.company.id,status=1).values_list('id',flat=True))
    else:
        project_ids = list(Projects.objects.filter(country_id=country_id,created_by_id=request.user.id,status=1).values_list('id',flat=True))
    return ProjectBlock.objects.filter(project_id__in=project_ids).count()


@register.simple_tag 
def get_totalwells(request,country_id):
    if request.company:
        project_ids = list(Projects.objects.filter(country_id=country_id,company_id=request.company.id,status=1).values_list('id',flat=True))
    else:
        project_ids = list(Projects.objects.filter(country_id=country_id,created_by_id=request.user.id,status=1).values_list('id',flat=True))  
    return Wells.objects.filter(project_id__in=project_ids).count()



@register.simple_tag 
def checklicense_expire(request):
    if(request.user.licence_type =='CompanyPlan' or request.user.licence_type =='Enterprise'):
        end_date=request.company.end_date
    elif(request.user.licence_type == 'Individual'):
        end_date=request.user.end_date
    else:
        return False

    current_date = str(datetime.today().date())
    currentdate_object = datetime.strptime(current_date, "%Y-%m-%d").date()
    lastdate_object = datetime.strptime(end_date, "%Y-%m-%d").date()
    date_difference = (currentdate_object - lastdate_object).days
    if(date_difference>0 and date_difference<=15):
        return True 
    return False

@register.simple_tag 
def changedateformat(dateformat):
    date = str(dateformat).split('-')
    if(date):
        monthNames = [
            "Jan", "Feb", "Mar", "Apr", "May", "June",
            "July", "Aug", "Sep", "Oct", "Nov", "Dec"
        ]
        return date[2]+'-'+monthNames[int(date[1])-1]+'-'+date[0]
    else:
        return None
      
@register.simple_tag 
def change_date_format(dateformat):
    return str(dateformat).split(' ')[0]
