from django.shortcuts import render
from bhadata.models import BhaData,BhaElement,Drillcollers,Drillpipe,DrillpipeHWDP,Specifications
from custom_auth.getunit import converttofloat
from muddata.models import MudData,Rheogram,RheogramNameModels,RheogramDate,MudType,Sections,RheogramSections,HydraulicData,Planwell_data,Pressureloss_data
from custom_auth.getunit import getprojectunit,adduserlog,converttofloat,getmodaltext,getcountries
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit,fsolve
import math
from helpers.mathsimport import pi,sqrt,pow,log10,log,acos,sin,cos,tan
from helpers import *
from scipy.optimize import newton,root_scalar
from helpers.unit_calculation import *
from scipy import interpolate
from surfacepipe.models import SurfacePipe,SurfacePipeData
from django.db.models import Q
from django.http import JsonResponse,HttpResponse
from drillbitdata.models import DrillBit,DrillBitNozzle,BitTypesNames
from projects.templatetags import app_filters
from welltrajectory.models import WellTrajectory
from custom_auth.getunit import getmd
from helpers.allmodels import Pressure,MudPumpFlowRate,Max,Min,Calculationchartdata,Sections,WellPhases,RheogramSections
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.views import View  
from io import BytesIO
from helpers.pdfstyle import pressurelosschart_pdfstyle,hydraulics_report_pdfstyle,totalwell_report_pdfstyle,sensitivity_report_pdfstyle
from helpers.commonimport import json,settings,get_template,Image,base64,datetime,timezone


# Create your views here.
def getallherselmodel(request):
    rpm=request.GET['rpm']
    well_id=request.session['well_id']
    flowrate=int(request.GET['flowrate'])
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    cuttings_density=converttofloat(request.GET['cuttings_density'])
    cuttings_size=converttofloat(request.GET['cuttings_size'])
    torque=request.GET['torque'] if 'torque' in request.GET else ""
    wob=request.GET['wob'] if 'wob' in request.GET else ""
    rop=request.GET['rop']
    bhadata=BhaData.objects.filter(well_phases_id=wellphase_id,status=1).first()
    muddata=MudData.objects.filter(well_phase_id=wellphase_id,section=section_name).first()
    sectionname=muddata.section
    rheogramsections=RheogramSections.objects.filter(section_name=sectionname).first()
    sectiontodepth=muddata.todepth
    wellphase = WellPhases.objects.getwellphase_byid(wellphase_id)
    previous_wellphase=WellPhases.objects.filter(id__lt=wellphase.id,well_id=well_id).order_by('-id').first()
    length_of_selected_section_from_surface=sectiontodepth
    hole_size=wellphase.hole_size
    id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
    bitdepth=sectiontodepth
    sections=Sections.objects.filter(section_name=sectionname).first()
    length_of_previous_casing_from_surface=previous_wellphase.measured_depth
    length_of_openhole_from_bitdepth=bitdepth-length_of_previous_casing_from_surface
    length_of_previous_casing_from_surface=previous_wellphase.measured_depth
    wellphasetodepth= wellphase.measured_depth
    sectionfromdepth=muddata.from_depth
    wellphasefromdepth=0 if previous_wellphase==None else previous_wellphase.measured_depth

    viscocity_hershel=calculate_viscocity_hershel(rheogramsections,sections,muddata)
    viscocity_hershel['selected_modal']="4"


    checkliner=WellPhases.objects.filter(Q(casing_type_id=7) | Q(casing_type_id=8) | Q(casing_type_id=11) | Q(casing_type_id=12)).filter(well_id=well_id,status=1,measured_depth__lt=sectiontodepth)

    if(checkliner.count()>0):
        alldata=display_bingham_liner(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,viscocity_hershel,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,checkliner)
    else:
        alldata=calculateallherselmodel(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,viscocity_hershel,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop)
    
    return JsonResponse(alldata,safe=False)

def calculateallherselmodel(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop):
    hershel_annular_pressure_loss=calculateannular_drillstring_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,selected_viscocity,'displayallmodels')
    bit_losses=getbitpressureloss(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,
    well_id)
    hershel_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,selected_viscocity,'displayallmodels')
    allhershel_pressureloss=gettotalresult(hershel_annular_pressure_loss,hershel_surface_losses)
    allherselpressureloss=round(allhershel_pressureloss['totalpressure_loss']+bit_losses[0]['bit_pressure_loss'])

    data = {
        'hershel_surface_losses':hershel_surface_losses,
        'hershel_annular_pressure_loss':hershel_annular_pressure_loss,
        'allhershel_pressureloss':allherselpressureloss,
        'allhershel':allhershel_pressureloss,
        'ty':selected_viscocity['lsryp']

    }
    
    return data

# calculate only annular and drillstring loss
def calculateannular_drillstring_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity,typename):
    allpressureloss=[]
    increased_pressureloss=[]
    alllinerdata=[]
    allslipvelocity=[]
    slipvelocitychart=[]
    allslipvelocitychartdata=[]
    allslipvelocityanuulardata=[]

    slipvelocitychart_walker=[]
    annularvelocitychartdata_walker=[]

    annularvelocitychartdata=[]
    allslipvelocity_walker=[]
    calculate_tj_pressureloss =[]
    calculate_tj_pressureloss_increased=[]
    bitelement=BhaElement.objects.filter(bhadata_id=bhadata.id,type_name='Bit',status=1).first()

    length_of_open_hole=length_of_selected_section_from_surface-length_of_previous_casing_from_surface
    previousbhaelement=BhaElement.objects.getbhaelement(bhadata.id)
    bhacount=previousbhaelement.count()
    i=bhacount
    previous_length_against_casing=[]
    cumlativelength=0
    for previousbha in previousbhaelement:
        if(previousbha.length_onejoint<sectiontodepth):
            newlength=converttofloat(previousbha.length)
        else:
            belowbha=BhaElement.objects.getpreviousbhaelement(bhadata.id,previousbha.id)
            newlength=sectiontodepth-belowbha.length_onejoint
        od_of_pipe_element=previousbha.od
        if(i==bhacount):
            length_against_casing=length_of_previous_casing_from_surface if(converttofloat(newlength)>=length_of_previous_casing_from_surface) else newlength
            previous_length_against_casing.append(length_against_casing)
        else:
            sum_of_previous_against_casing=Sum = sum(previous_length_against_casing)
            if(sum_of_previous_against_casing==length_of_previous_casing_from_surface):
                length_against_casing=0
            if((sum_of_previous_against_casing<length_of_previous_casing_from_surface) and (sum_of_previous_against_casing+newlength<length_of_previous_casing_from_surface)):
                length_against_casing=newlength
            else:
                length_against_casing=length_of_previous_casing_from_surface-sum_of_previous_against_casing
            previous_length_against_casing.append(length_against_casing)
        length_against_open_hole=converttofloat(newlength)-length_against_casing
      
        if(length_against_casing!=0):
            pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,muddata.mud_weight,previousbha.od,id_of_previous_casing,length_against_casing,'annularpressurelosscasing')
            if((previousbha.type_name=='RSS') or (previousbha.type_name=='MWD') or (previousbha.type_name=='LWD') or (previousbha.type_name=='Others') or (previousbha.type_name=='Mud Motor')):
                drillstringpressureloss=calculate_drillstringloss_downholetools(previousbha,flowrate,muddata.mud_weight,torque,wob)
            else:
                drillstringpressureloss=calculatepressloss(well_id,rpm,flowrate,muddata.mud_weight,previousbha.identity,length_against_casing,viscocity,'calculateannular_pressureloss')
            
            cumlativelength +=length_against_casing
            if((previousbha.type_name=='Drill Pipe') or (previousbha.type_name=='Heavy Weight Drill Pipe')):
                calculate_tj_pressureloss=calculatetjpressureloss(previousbha.length,length_against_casing,previousbha,rpm,flowrate,viscocity,muddata.mud_weight,id_of_previous_casing,'without')
               
   
            allpressureloss.append({
                'flowregime' : pressureloss["flowregime"],
                'od':round(converttofloat(od_of_pipe_element),2),
                'id':round(converttofloat(previousbha.identity),2),
                'type':previousbha.type_name,
                'element':previousbha.element,
                'length_against':length_against_casing,
                'pressureloss':round(pressureloss["pressureloss"]+calculate_tj_pressureloss["tjannularloss"],2),
                'element_type':'CH',
                'drillstringloss':round(drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"],2)  if 'pressureloss' in drillstringpressureloss else drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"],
                'mudweight':muddata.mud_weight,
                'cumlativelength':cumlativelength

            })


        
        if(length_against_open_hole!=0):
            # print(f"element {previousbha.type_name}")
            # print("openhole")
            pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,muddata.mud_weight,previousbha.od,hole_size,length_against_open_hole,'annularpressurelossnewtonian')
            if((previousbha.type_name=='RSS') or (previousbha.type_name=='MWD') or (previousbha.type_name=='LWD') or (previousbha.type_name=='Others') or (previousbha.type_name=='Mud Motor')):
                drillstringpressureloss=calculate_drillstringloss_downholetools(previousbha,flowrate,muddata.mud_weight,torque,wob)
            else:
                drillstringpressureloss=calculatepressloss(well_id,rpm,flowrate,muddata.mud_weight,previousbha.identity,length_against_open_hole,viscocity,'calculateannular_pressureloss')
            # print(f'drillstring hole {drillstringpressureloss}')
            cumlativelength +=length_against_open_hole
            
            if((previousbha.type_name=='Drill Pipe') or (previousbha.type_name=='Heavy Weight Drill Pipe')):
                calculate_tj_pressureloss=calculatetjpressureloss(previousbha.length,length_against_open_hole,previousbha,rpm,flowrate,viscocity,muddata.mud_weight,hole_size,'without')
           

            allpressureloss.append({
                'flowregime' : pressureloss["flowregime"],
                'od':round(converttofloat(od_of_pipe_element),2),
                'id':round(converttofloat(previousbha.identity),2),
                'type':previousbha.type_name,
                'element':previousbha.element,
                'length_against':length_against_open_hole,
                'pressureloss':round(pressureloss["pressureloss"]+calculate_tj_pressureloss['tjannularloss'],2),
                'element_type':'OH',
                'drillstringloss':round(drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"],2)  if 'pressureloss' in drillstringpressureloss else drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"],
                'mudweight':muddata.mud_weight,
                'cumlativelength':cumlativelength

            })
        previouselement_length=previousbha.length_onejoint
        i -=1
    data={
        'allpressureloss':allpressureloss, 
    }
    return data

def calculate_viscocity_hershel(rheogramsections,sections,muddata):
    well_id =muddata.well_id
    unit = getprojectunit(well_id)
    if(muddata.plastic_viscosity==None and muddata.yield_point==None and muddata.low_shear_rate==None):
        if(muddata.well.well_type == 'PLAN'):
            rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=None)
            selected_model=sections.selected_model
        else:
            rheogram=Rheogram.objects.filter(rheogram_date_id=rheogramsections[0].id,status=1,modelname=None)
            selected_model='4'
        rpm=[]
        dial=[]
        for rheogramdata in rheogram:
            if rheogramdata.dial!='':
                rpm.append(rheogramdata.rpm)
                dial.append(float(rheogramdata.dial))
                if(rheogramdata.rpm==300):
                    dial300=float(rheogramdata.dial)
                if(rheogramdata.rpm==600):
                    dial600=float(rheogramdata.dial) 
        X=np.array(rpm).reshape(-1,1)
        Y=np.array(dial).reshape(-1,1)
        popt,pcov=curve_fit(f,np.squeeze(X.T).tolist(),np.squeeze(Y.T).tolist(),maxfev=10000)
        m,Ty,K_HB=popt[0],popt[1],popt[2]
        K=K_HB
        n=m  
        last_rpm=rpm[-1:]
        dial_300 = 0
        dial_600 = 0
        for i in range(last_rpm[0]+1):
            y=round(Ty+K_HB*i**m,2)
            if(i==300):
                dial_300=y
            elif(i==600):
                dial_600=y
        plastic_viscosity=dial_600-dial_300
        yieldpoint=dial_300-round(plastic_viscosity,2)
        lsryp=Ty
        displaypv=dial600-dial300
        displayyp=dial300-displaypv
        # if unit == 'SI':
        #     displaypv = displaypv/1000
        #     displayyp = displayyp/0.4788
    else:
        if(muddata.well.well_type == 'PLAN'):
            rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname='hershel')
            selected_model=sections.selected_model
        else:
            rheogram=Rheogram.objects.filter(rheogram_date_id=rheogramsections[0].id,status=1,modelname=None)
            selected_model='4'
        # last_rpm=rpm[-1]
        if unit == 'API':
            t300=muddata.plastic_viscosity+muddata.yield_point
            t600=t300+muddata.plastic_viscosity
            
            m=3.32*log10((t600-muddata.low_shear_rate)/(t300-muddata.low_shear_rate))
            k_hb=(t300-muddata.low_shear_rate)/pow(511,m)
            K=k_hb
            n=m
            plastic_viscosity=muddata.plastic_viscosity
            yieldpoint=muddata.yield_point
            lsryp=muddata.low_shear_rate
            displaypv=plastic_viscosity
            displayyp=yieldpoint
        else:
            plastic_viscosity=muddata.plastic_viscosity*1000
            yieldpoint=muddata.yield_point/0.4788
            lsryp=muddata.low_shear_rate/0.4788
            
            t300=plastic_viscosity+yieldpoint
            t600=t300+plastic_viscosity
            m=3.32*log10((t600-lsryp)/(t300-lsryp))
            k_hb=(t300-lsryp)/pow(511,m)
            K=k_hb
            n=m
            displaypv=muddata.plastic_viscosity
            displayyp=muddata.yield_point
    data={
        'plastic_viscosity':plastic_viscosity,
        'yieldpoint':yieldpoint,
        'K':K,
        'n':n,
        'lsryp':lsryp,
        'selected_modal':selected_model,
        # 'selected_modal':sections.selected_model,
        'displaypv':displaypv,
        'displayyp':displayyp
    }
    return data

def f(x,n,Ty,K):
    return Ty+K*x**n

def calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,typename):
    unit = getprojectunit(well_id)
    if(viscocity['selected_modal']=="4"):
        pressureloss=calculate_hersel_annular(viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,typename,unit)
    elif(viscocity['selected_modal']=="3"):
        pressureloss=calculate_powerlaw_annular(viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,unit)
    elif(viscocity['selected_modal']=="2"):
        pressureloss=calculate_bingham_annular(viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,typename,unit)
    else:
        pressureloss=calculate_newtonian_annular(viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,unit)
    return pressureloss

def calculate_powerlaw_annular(viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,unit):
    k=viscocity['K']
    m=viscocity['n']
    n=m
    K=k*0.4788*1.066  
    # print(f'K {K}')
    flowrate_si = convertflowrate(flowrate,unit)
    # print(f'flowrate_si {flowrate_si}')
    casing_hole_size_si = convertcasing_hole_size(casing_hole_size,unit)
    # print(f'casing_hole_size_si {casing_hole_size_si}')
    od_of_pipe_element_si = odconversion(float(od_of_pipe_element),unit)
    # print(f'od_of_pipe_element_si {od_of_pipe_element_si}')
    rpm_si = rpm_convert(int(rpm))
    # print(f'rpm_si {rpm_si}')
    mudweight_si= mudweight_conversion(mud_weight,unit)
    # print(f'mudweight_si {mudweight_si}')
    length_si=length_conversion(length,unit)
    # print(f'length_si {length_si}')

    U=flowrate_si/(pi/4*(casing_hole_size_si**2-od_of_pipe_element_si**2))
    # print(f'U {U}')
    Y=0.37*n**-0.14
    # print(f'Y {Y}')
    Z=1-(1-(od_of_pipe_element_si/(casing_hole_size_si))**Y)**(1/Y)
    # print(f'Z {Z}')
    G=((1+Z/2)*((3-Z)*n+1))/(n*(4-Z))
    # print(f'G {G}')
    De=(casing_hole_size_si-od_of_pipe_element_si)/G
    # print(f'De {De}')
    Ss=((12*U/(casing_hole_size_si-od_of_pipe_element_si)*(2*n+1)/(3*n))**2+(rpm_si*od_of_pipe_element_si/(casing_hole_size_si-od_of_pipe_element_si))**2)**0.5
    # print(f'Ss {Ss}')

    Ts=K*Ss**n
    # print(f'Ts {Ts}')
    Re=De*mudweight_si*U/(Ts/Ss)
    # print(f'Re {Re}')

    if Re<=3470-1370*n:
        flowregime='Laminar'
        f=24/Re if Re else 0
    
    elif Re>4150-1150*n:
        flowregime='Turbulent'
        def f_x(f):
            return 1/sqrt(f)-4/n**0.75*log10(Re*f**(1-n/2))+0.4/n**1.2
        f=newton(f_x,24/Re)
    else:
        flowregime='Transitional'
        f_l=24/(3470-1370*n)
        def f_x(f):
            return 1/sqrt(f)-4/n**0.75*log10((4150-1150*n)*f**(1-n/2))+0.4/n**1.2
        f_turb=newton(f_x,f_l)
        x=(3470-1370*n,4150-1150*n)
        y=(f_l,f_turb)
        f_tran=interpolate.interp1d(x,y)
        f=f_tran(Re)

    #4.1.7 Calculate Pressure Loss, API Units
    pressureloss=2*f*mudweight_si*U**2*length_si/(casing_hole_size_si-od_of_pipe_element_si)
    pressureloss=pressureloss_conversion(pressureloss,unit)
    # print(f'pressureloss {pressureloss}')
    data={
        'pressureloss':pressureloss,
        'flowregime':flowregime
    }
    return data

def calculatepressloss(well_id,rpm,flowrate,mudweight,identity,length,viscocity,typename):
    unit = getprojectunit(well_id)
    # print(f"viscocitycalculatepressloss {viscocity}")
    pressureloss =[]
    if(viscocity['selected_modal']=="1"):
        pressureloss=calculate_newtonian_pressureloss(unit,rpm,flowrate,mudweight,identity,length,viscocity['plastic_viscosity'])
    elif(viscocity['selected_modal']=="2"):
        pressureloss=calculate_bingham_pressureloss(unit,rpm,flowrate,mudweight,identity,length,viscocity['plastic_viscosity'],viscocity['yieldpoint'])
    elif(viscocity['selected_modal']=="4"):
        pressureloss=calculate_hershel_pressureloss(unit,flowrate,mudweight,identity,length,viscocity,typename)
    elif(viscocity['selected_modal']=="3"):
        pressureloss=calculate_powerlaw_pressureloss(unit,flowrate,mudweight,identity,length,viscocity,typename)
    return pressureloss

def calculate_powerlaw_pressureloss(unit,flowrate,mudweight,identity,length,viscocity,typename):
    # print(f'identity {identity}')
    Q=convertflowrate(flowrate,unit)
    # print(f'flowrate {Q}')
    MW=mudweight_conversion(mudweight,unit)
    # print(f'MW {MW}')
    ID=odconversion(float(identity),unit)
    # print(f'ID {ID}')
    L=length_conversion(float(length),unit)
    # print(f'L {L}')
   
    n=viscocity['n']
    # print(f'n {n}')
    K=viscocity['K']*0.4788
    # print(f'K {K}')
    # 1. Calculate Average Velocity
    U=Q/(pi/4*ID**2)
    # print(f'U {U}')

    #2. Calculate Reynolds Number
    Re=(ID**n*U**(2-n)*MW)/(8**(n-1)*K)
    # print(f'Re {Re}')

    #3. Calculate Pressure Loss
    if Re<=3470-1370*n:
        t_w=K*((3*n+1)/(4*n)*(8*U)/ID)**n
        dp=4*t_w/ID*L

    elif Re>4150-1150*n:
        def f_x(x):
            return 1/(x)**0.5-4/n**0.75*log10(Re*x**(1-n/2))+0.4/n**1.2
        
        f=newton(f_x,16/Re)
        t_w=0.5*f*MW*U**2
        dp=2*f*MW*U**2/ID*L
    
    else:
        def f_x(f_turb):
            return 1/sqrt(f_turb)-4/n**0.75*log10(Re_turb*f_turb**(1-n/2))+0.4/n**1.2
        
        #End of Laminar
        Re_L=3470-1370*n
        f_l=16/Re_L
        # Start of Turbulent
        Re_turb=4150-1150*n
        f_turb=newton(f_x,f_l)
        x=[3470-1370*n,4150-1150*n]
        y=[f_l,f_turb]
        
        #Define the interpolate method
        i=interpolate.interp1d(x,y)
        f=i(Re)
        t_w=0.5*f*MW*U**2
        dp=2*f*MW*U**2/ID*L

    # print(f'dp {dp}')
    #4. Convert back to API Unit
    pressureloss=pressureloss_conversion(dp,unit)
    # print(f'pressureloss {pressureloss}')
    
    data={
        'viscocity_si':viscocity['plastic_viscosity'],
        'flowrate_si':Q,
        'mudweight_si':MW,
        'ID':ID,
        'length':L,
        'velocity':0,
        'Re': Re,
        'flowregime':"",
        'f':"",
        'pressureloss':pressureloss,
        'flowrate':flowrate,
        'mudweight':mudweight,
        'identity':identity,
        'originallength':length,
        'originalviscocity':viscocity['plastic_viscosity']
    }
    return data

def calculateslipvelocitywithoutliner(well_id,rpm,flowrate,mud_weight,cased_hole_size,od,viscocity,cuttings_density,cuttings_size,length):
    unit = getprojectunit(well_id)
    if(viscocity["selected_modal"]=="1"):
        slipvelocity=calculate_slipvelocity_newtonian(unit,rpm,flowrate,mud_weight,cased_hole_size,od,viscocity,cuttings_density,cuttings_size)
    elif(viscocity["selected_modal"]=="2"):
        slipvelocity=calculate_slipvelocity_bingham(unit,rpm,flowrate,mud_weight,cased_hole_size,od,viscocity,cuttings_density,cuttings_size)
    elif(viscocity["selected_modal"]=="3"):
        slipvelocity=calculate_slipvelocity_powerlaw(unit,rpm,flowrate,mud_weight,cased_hole_size,od,viscocity,cuttings_density,cuttings_size)
    elif(viscocity["selected_modal"]=="4"):
        slipvelocity=calculate_slipvelocity_hershel(unit,rpm,flowrate,mud_weight,cased_hole_size,od,viscocity,cuttings_density,cuttings_size)
    data={'slipvelocity':slipvelocity['slip_velocity'],'length':length,'annular_velocity':slipvelocity['annular_velocity'],'od':od}

    return data

def calculate_slipvelocity_powerlaw(unit,rpm,flowrate,mud_weight,cased_hole_size,od,viscocity,cuttings_density,cuttings_size):

    # print(f'cased_hole_size  {cased_hole_size}')
    # print(f'od  {od}')
    # print(f'mud_weight  {mud_weight}')
    # print(f'flowrate  {flowrate}')
    # print(f'cuttings_density  {cuttings_density}')
    # print(f'cuttings_size  {cuttings_size}')
    cased_hole_size = calculate_holesize(cased_hole_size,unit)
    od = calculate_od(converttofloat(od),unit)
    mud_weight = calculate_mudweight(mud_weight,unit)
    flowrate = calculate_flowrate(flowrate,unit)
    cuttings_density = calculate_cutting_density(cuttings_density,unit)
    cuttings_size = calculate_cutting_size(cuttings_size,unit)
    
    # print(f'cased_hole_size convert {cased_hole_size}')
    # print(f'od convert {od}')
    # print(f'rpm convert {rpm}')
    # print(f'mud_weight convert {mud_weight}')
    # print(f'flowrate convert {flowrate}')
    # print(f'cuttings_density convert {cuttings_density}')
    # print(f'cuttings_size convert {cuttings_size}')
    n=viscocity["n"]
    K=viscocity['K']*0.4788 
    id_si=cased_hole_size/12/3.281
    rpm_si=int(rpm)*2*pi/60
    od_si=converttofloat(od)/12/3.281
    annular_velocity=24.51*flowrate/(cased_hole_size**2-converttofloat(od)**2)
    annular_velocity_si=annular_velocity/3.281/60
    shear_rate=((12*annular_velocity_si/(id_si-od_si)*(2*n+1)/(3*n))**2+(rpm_si*od_si/(id_si-od_si))**2)**0.5
    shear_stress=K*shear_rate**n
    apparent_velocity=shear_stress/shear_rate*1000 
    turbulent_vs=9.24*sqrt(cuttings_size*(cuttings_density-mud_weight)/mud_weight)
    turbulent_nRe=15.47*mud_weight*cuttings_size*turbulent_vs/apparent_velocity
    
    stoke_vs=4972*cuttings_size**2/apparent_velocity*(cuttings_density-mud_weight)
    stoke_nRe=15.47*mud_weight*cuttings_size*stoke_vs/apparent_velocity

    transitional_vs=174*cuttings_size*(cuttings_density-mud_weight)**0.667/(mud_weight**0.333*apparent_velocity**0.333)
    transitional_nRe=15.47*mud_weight*cuttings_size*transitional_vs/apparent_velocity

    if(turbulent_nRe>2000):
        slip_velocity=turbulent_vs
    else:
        if(stoke_nRe<=1):
            slip_velocity=stoke_vs
        else:
            slip_velocity=transitional_vs

    slip_velocity = slipvelocity_conversion(slip_velocity,unit)
    data={
        'slip_velocity':slip_velocity,
        'annular_velocity':annular_velocity
    }
    return data

def calculate_hersel_annular(viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,typename,unit):
    k=viscocity['K']
    ty=viscocity['lsryp']
    m=viscocity['n']

    K=k_conversion(k,m,unit)
    LSRYP = ty_conversion(ty,unit)
    flowrate_si=convertflowrate(flowrate,unit)
    od_of_pipe_element_si = odconversion(float(od_of_pipe_element),unit)
    casing_hole_size_si =convertcasing_hole_size(float(casing_hole_size),unit)
    rpm_si = rpm_convert(int(rpm))
    mudweight_si=mudweight_conversion(mud_weight,unit)
    length_si=length_conversion(length,unit)

    U = flowrate_si/(pi/4*(casing_hole_size_si**2-od_of_pipe_element_si**2))
    
    ssz = 12*U/(casing_hole_size_si-od_of_pipe_element_si)
    sso = rpm_si*(od_of_pipe_element_si/2)**2/((casing_hole_size_si/2)**2-(od_of_pipe_element_si/2)**2)*((-2*(od_of_pipe_element_si/2)**2-((casing_hole_size_si/2)**2-(od_of_pipe_element_si/2)**2))/(od_of_pipe_element_si/2)**2)
    sst = sqrt(ssz**2+sso**2)
    def t_xc(t):
        return sst-((t-LSRYP)**((m+1)/m)/(K**(1/m)*t**2))*(3*m/(1+2*m))*(t+m/(m+1)*LSRYP)
    
    tw=newton(t_xc,LSRYP+1,maxiter=1000)

    a=(3*m/(1+2*m))*(1-(1/(1+m))*LSRYP/tw-(m/(1+m))*(LSRYP/tw)**2)
    b=1/a
    N=1/(3*(b-2/3))

    sg=(1+2*N)/(3*N)*sst
    Re = 12*mudweight_si*U**2/(LSRYP+K*sg**m)
    if Re<=3470-1370*N:
        flowregime='Laminar'
        fc=24/Re if Re else 0
    elif Re>4150-1150*N:
        flowregime='Turbulent'
        def f_x(a):
            return 1/sqrt(a)-4/N**0.75*log10(Re*a**(1-N/2))+0.4/N**1.2
        
        fc=newton(f_x,24/Re)
        
    else:
        flowregime='Transitional'
        def f_x(f_turb):
            return 1/sqrt(f_turb)-4/N**0.75*log10(Re_turb*f_turb**(1-N/2))+0.4/N**1.2
        
        #End of Laminar
        Re_L=3470-1370*N
        f_l=24/Re_L
        
        #Start of Turbulent
        Re_turb=4150-1150*N
        f_turb=newton(f_x,f_l)
        
        x=[3470-1370*N,4150-1150*N]
        y=[f_l,f_turb]
        
        #Define the interpolate method
        i=interpolate.interp1d(x,y)
        
        fc=i(Re)
    
    pressureloss = 2*fc*mudweight_si*U**2*length_si/(casing_hole_size_si-od_of_pipe_element_si)
    # if(typename=='annularpressureloss_liner'):
    #     print(f"pressurelosslinernew {pressureloss}")
    #     print(f"fclinernew {fc}")
    #     print(f"casing_hole_size_silinernew {casing_hole_size_si}")
    #     print(f"od_of_pipe_element_silinernew {od_of_pipe_element_si}")



    
    pressureloss=pressureloss_conversion(pressureloss,unit)
    data={
        'pressureloss':pressureloss,
        'flowregime':flowregime,
        'id':casing_hole_size,
        'length':length,
        'od':od_of_pipe_element
    }
    return data

def calculate_hershel_pressureloss(unit,flowrate,mudweight,identity,length,viscocity,typename):
    m=viscocity['n']
    K=k_conversion(viscocity['K'],m,unit)
    ty=ty_conversion(viscocity['lsryp'],unit)
    viscocity_si=viscocity["plastic_viscosity"]*1.066*0.4788

    flowrate_si=convertflowrate(flowrate,unit)
    mudweight_si=mudweight_conversion(mudweight,unit)
    identity_si=odconversion(float(identity),unit)
    length_si=length_conversion(float(length),unit)
    U=flowrate_si/(pi/4*identity_si**2)  
    def f_x(tw):
        # if(typename=='checkvalue'):
        #     print(f"tw {tw}")
        #     print(f"formula {8*U/identity_si-((tw-ty)**(1+1/m)/(K**(1/m)*tw**3)*(4*m/(3*m+1)))*(tw**2+(2*m/(1+2*m))*ty*tw+2*m**2/((1+m)*(1+2*m))*ty**2)}")
        return 8*U/identity_si-((tw-ty)**(1+1/m)/(K**(1/m)*tw**3)*(4*m/(3*m+1)))*(tw**2+(2*m/(1+2*m))*ty*tw+2*m**2/((1+m)*(1+2*m))*ty**2)
    t_w=newton(f_x,ty+1) # t_w=newton(f_x,ty) changed this to t_w=newton(f_x,ty+1) when Tolerance of 0.0008656012000001212 reached. Failed to converge after 1 iterations, value is 7.656877601200001,client give this correction.

    A=((1-2*m)*t_w+3*m*ty)/(m*(t_w-ty))+((2*m*(1+m))*((1+2*m)*t_w**2+m*ty*t_w))/(m*(1+m)*(1+2*m)*t_w**2+2*m**2*(1+m)*ty*t_w+2*m**3*ty**2)
    N=1/A

    K_g=t_w/(8*U/identity_si)**N

    Re=mudweight_si*U**(2-N)*identity_si**N/(K_g*8**(N-1))

    if Re<=3470-1370*N:
        f=16/Re
    elif Re>4150-1150*N:
        
        def f_x(a):
            return 1/sqrt(a)-4/N**0.75*log10(Re*a**(1-N/2))+0.4/N**1.2
        f=newton(f_x,16/Re)
    else:
        def f_x(f_turb):
            return 1/sqrt(f_turb)-4/N**0.75*log10(Re_turb*f_turb**(1-N/2))+0.4/N**1.2
        
        Re_L=3470-1370*N
        f_l=16/Re_L

        Re_turb=4150-1150*N
        f_turb=newton(f_x,f_l)
        x=[3470-1370*N,4150-1150*N]
        y=[f_l,f_turb]

        i=interpolate.interp1d(x,y)
        f=i(Re)
    
    dP=2*f*mudweight_si*U**2*length_si/identity_si
    
    dP=pressureloss_conversion(dP,unit)
    data={
        'viscocity_si':viscocity["plastic_viscosity"],
        'flowrate_si':flowrate_si,
        'mudweight_si':mudweight,
        'ID':identity,
        'length':length,
        'velocity':0,
        'Re': Re,
        'flowregime':"",
        'f':"",
        'pressureloss':dP,
        'flowrate':flowrate,
        'mudweight':mudweight,
        'identity':identity,
        'originallength':length,
        'originalviscocity':viscocity["plastic_viscosity"]
    }
    return data


def calculate_slipvelocity_hershel(unit,rpm,flowrate,mud_weight,cased_hole_size,od,viscocity,cuttings_density,cuttings_size):
    cased_hole_size = calculate_holesize(cased_hole_size,unit)
    od = calculate_od(converttofloat(od),unit)
    mud_weight = calculate_mudweight(mud_weight,unit)
    flowrate = calculate_flowrate(flowrate,unit)
    cuttings_density = calculate_cutting_density(cuttings_density,unit)
    cuttings_size = calculate_cutting_size(cuttings_size,unit)

    id_si=cased_hole_size/12/3.281
    rpm_si=int(rpm)*2*pi/60
    od_si=converttofloat(od)/12/3.281
    m=viscocity["n"]
    K=viscocity['K']*1.066*0.4788/1.703**m

    Ty=viscocity['lsryp']*1.066*0.4788

    annular_velocity=24.51*flowrate/(cased_hole_size**2-converttofloat(od)**2)
    annular_velocity_si=annular_velocity/3.281/60

    
    sao=12*annular_velocity_si/(id_si-od_si)

    sro=rpm_si*(od_si/2)**2/((id_si/2)**2-(od_si/2)**2)*((-2*(od_si/2)**2-((id_si/2)**2-(od_si/2)**2))/(od_si/2)**2)

    shear_rate=sqrt(sao**2+sro**2)

    shear_stress=Ty+K*shear_rate**m

    apparent_velocity=shear_stress/shear_rate*1000
    
    turbulent_vs=9.24*sqrt(cuttings_size*(cuttings_density-mud_weight)/mud_weight)

    turbulent_nRe=15.47*mud_weight*cuttings_size*turbulent_vs/apparent_velocity

    
    stoke_vs=4972*cuttings_size**2/apparent_velocity*(cuttings_density-mud_weight)

    stoke_nRe=15.47*mud_weight*cuttings_size*stoke_vs/apparent_velocity


    transitional_vs=174*cuttings_size*(cuttings_density-mud_weight)**0.667/(mud_weight**0.333*apparent_velocity**0.333)

    transitional_nRe=15.47*mud_weight*cuttings_size*transitional_vs/apparent_velocity


    if(turbulent_nRe>2000):
        slip_velocity=turbulent_vs
    else:
        if(stoke_nRe<=1):
            slip_velocity=stoke_vs
        else:
            slip_velocity=transitional_vs
    slip_velocity = slipvelocity_conversion(slip_velocity,unit)

    data={
        'slip_velocity':slip_velocity,
        'annular_velocity':annular_velocity
    }
    return data

def slipvelocity_walker(muddata,cased_hole_size,rpm,od,cuttings_density,cuttings_size,flowrate):
    sectionname=muddata.section
    rheogramsections=RheogramSections.objects.filter(section_name=sectionname).first()
    sections=Sections.objects.filter(section_name=sectionname).first()
    rheology_date=RheogramDate.objects.filter(well_id=muddata.well_id,muddata_id=muddata.id,status=1)
    if(muddata.well.well_type == 'PLAN'):
        viscocity=calculate_viscocity_powerlaw(rheogramsections,sections,muddata)
    else:
        viscocity=calculate_viscocity_powerlaw(rheology_date,'sections',muddata)
    unit = getprojectunit(muddata.well_id)
    # print(f'mud_weight {muddata.mud_weight}')
    # print(f'plastic_viscocity {viscocity["displaypv"]}')
    # print(f'yield_point {viscocity["displayyp"]}')
    # print(f'flowrate {flowrate}')
    # print(f'cased_hole_size {cased_hole_size}')
    # print(f'od {od}')
    # print(f'cuttings_density {cuttings_density}')
    # print(f'cuttings_size {cuttings_size}')
    # print(f"viscocitypowerlaw {viscocity}")
    mud_weight = calculate_mudweight(muddata.mud_weight,unit)
    flowrate = calculate_flowrate(flowrate,unit)
    cased_hole_size = calculate_holesize(cased_hole_size,unit)
    od = calculate_od(converttofloat(od),unit)
    cuttings_density = calculate_cutting_density(cuttings_density,unit)
    cuttings_size = calculate_cutting_size(cuttings_size,unit)
    plastic_viscocity = viscocity['displaypv']
    yield_point = viscocity['displayyp']

    # print(f'mud_weight convert {mud_weight}')
    # print(f'plastic_viscocity convert {plastic_viscocity}')
    # print(f'yield_point convert {yield_point}')
    # print(f'flowrate convert {flowrate}')
    # print(f'cased_hole_size convert {cased_hole_size}')
    # print(f'od convert {od}')
    # print(f'cuttings_density convert {cuttings_density}')
    # print(f'cuttings_size convert {cuttings_size}')


    annular_velocity=24.51*flowrate/(cased_hole_size**2-converttofloat(od)**2)
    shear_stress=7.9*sqrt(cuttings_size*(cuttings_density-mud_weight))
    # print(f"shear_stress {shear_stress}")
    n=3.222*log10((2*plastic_viscocity+yield_point)/(plastic_viscocity+yield_point))

    K=(511**(1-n)*(plastic_viscocity+yield_point))/1000/0.4788
    # print(f"n {n}")
    # print(f"K {K}")

    shear_rate=(shear_stress/K)**(1/n)
    # print(f"shear_rate {shear_rate}")
    # print(f"mud_weight {mud_weight}")
    # print(f"shear_stress {shear_stress}")

    # print(f"shear_rate {shear_rate}")


    

    app_velocity=511*shear_stress/shear_rate
    # print(f"app_velocity {app_velocity}")

    vsl=131.4*sqrt(cuttings_size*(cuttings_density-mud_weight)/mud_weight)
    # print(f"vsl {vsl}")

    nre=15.47*mud_weight*cuttings_size*vsl/app_velocity
    # print(f"nre {nre}")

    vsl1=1.218*shear_stress*sqrt(cuttings_size*shear_rate/sqrt(mud_weight))
    # print(f"vsl1 {vsl1}")

    nre1=15.47*mud_weight*cuttings_size*vsl1/app_velocity
    # print(f"nre1 {nre1}")

    if(nre>100):
        slipvelocity=vsl
    else:
       slipvelocity=vsl1 
        
    # print(f'slipvelocity {slipvelocity}')
    slipvelocity = slipvelocity_conversion(slipvelocity,unit)
    data={'slipvelocity':slipvelocity,'annular_velocity':annular_velocity}
    return data

def calculate_viscocity_powerlaw(rheogramsections,sections,muddata):
    well_id =muddata.well_id
    unit = getprojectunit(well_id)
    if(muddata.plastic_viscosity==None and muddata.yield_point==None and muddata.low_shear_rate==None):
        if(muddata.well.well_type == 'PLAN'):
            rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=None)
            selected_model=sections.selected_model
        else:
            rheogram=Rheogram.objects.filter(rheogram_date_id=rheogramsections[0].id,status=1,modelname=None)
            selected_model='3'
        rpm=[]
        dial=[]
        for rheogramdata in rheogram:
            if rheogramdata.dial!='':
                rpm.append(rheogramdata.rpm)
                dial.append(float(rheogramdata.dial))
                if(rheogramdata.rpm==300):
                    dial300=float(rheogramdata.dial)
                if(rheogramdata.rpm==600):
                    dial600=float(rheogramdata.dial) 
     
        X=np.array(rpm).reshape(-1,1)
        Y=np.array(dial).reshape(-1,1)
        X_PL=np.log10(X)
        Y_PL=np.log10(Y)
        PL=LinearRegression()
        PL.fit(X_PL,Y_PL)
        K,n=10**PL.intercept_[0],PL.coef_[0][0]
        last_rpm=rpm[-1:]
        for i in range(last_rpm[0]+1):
            calculateddial=round((K*i**n),2)
            if(i==300):
                dial_300=calculateddial
            elif(i==600):
                dial_600=calculateddial
        plastic_viscosity=dial_600-dial_300
        yield_point=dial_300-round(plastic_viscosity,2)
        displaypv=dial600-dial300
        displayyp=dial300-displaypv
        # if unit == 'SI':
        #     displaypv = displaypv*1000
        #     displayyp = displayyp/0.4788
    else:
        if(muddata.well.well_type == 'PLAN'):
            rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname='powerlaw')
            selected_model=sections.selected_model
        else:
            selected_model='3'
        
        if unit == 'API':
            plastic_viscosity = muddata.plastic_viscosity
            yield_point = muddata.yield_point
            t300=muddata.plastic_viscosity+muddata.yield_point
            t600=t300+muddata.plastic_viscosity
        else :
            plastic_viscosity = muddata.plastic_viscosity*1000
            yield_point = muddata.yield_point/0.4788
            t300=plastic_viscosity+yield_point
            t600=t300+plastic_viscosity

        n=3.32*log10(t600/t300)
        k_pl=t300/pow(511,n)
        K=k_pl
        displaypv = muddata.plastic_viscosity
        displayyp = muddata.yield_point
    data={
        'K':K,
        'n':n,
        'plastic_viscosity':plastic_viscosity,
        'yieldpoint':yield_point,
        'selected_modal':selected_model,
        # 'selected_modal':sections.selected_model,
        'displaypv':displaypv,
        'displayyp':displayyp
    }
    return data

def calculate_increased_mudweight(well_id,flowrate,cased_hole_size,od,rop,slipvelocityvalue,mud_weight,cuttings_density):
    # print(f"slipvelocityvalue {slipvelocityvalue}")
    unit = getprojectunit(well_id)
    flowrate = calculate_flowrate(flowrate,unit)
    cased_hole_size = calculate_holesize(cased_hole_size,unit)
    od=calculate_od(converttofloat(od),unit)
    mud_weights = calculate_mudweight(mud_weight,unit)
    rop=calculate_rop(converttofloat(rop),unit)

    vc=converttofloat(rop)/60*(0.7854*cased_hole_size**2)/144
    va=24.51*flowrate/(cased_hole_size**2-converttofloat(od)**2)
    vm=flowrate/7.48
    c=vc/vm
    ca=-0.5*(va/slipvelocityvalue-1)+(0.25*(va/slipvelocityvalue-1)**2+(va/slipvelocityvalue*c))**0.5
    vf=va*(1+ca*slipvelocityvalue/va)
    increased_mudweight=ca*(cuttings_density-mud_weight)+mud_weight
    data={'increased_mudweight':increased_mudweight}
    return data

def calculatetjpressureloss(bhalength,length,bhadata,rpm,flowrate,viscocity,mud_weight,cased_hole_size,typename):
    # print(f"typename {bhadata.type_name}")
    well_id = bhadata.bhadata.well_id
    unit=getprojectunit(well_id)
    length_of_drillpipebody=float(bhadata.onejoint_length)
    length_of_boxtj=float(bhadata.box_tj_length)
    length_of_pintj=float(bhadata.pin_tj_length)
    # print(f"length_of_boxtj {length_of_boxtj}")
    # print(f"length_of_pintj {length_of_pintj}")

    noof_pipe=length/length_of_drillpipebody
    noof_tj=noof_pipe*2
    box_number=noof_tj/2
    box_length=convert_box_pin(length_of_boxtj,box_number,unit)
    # box_length=length_of_boxtj*box_number/12
    pin_number=noof_tj-box_number
    pin_length=convert_box_pin(length_of_pintj,pin_number,unit)
    # pin_length=length_of_pintj*pin_number/12
    data={}
    pin_pressureloss=calculatepressloss(well_id,rpm,flowrate,mud_weight,bhadata.tool_id,pin_length,viscocity,'calculatetjpressureloss')
    box_pressureloss=calculatepressloss(well_id,rpm,flowrate,mud_weight,bhadata.tool_id,box_length,viscocity,'calculatetjpressureloss')
    pin_annular=calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,bhadata.tool_od,cased_hole_size,pin_length,'tjpressureloss')
    box_annular=calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,bhadata.tool_od,cased_hole_size,box_length,'tjpressureloss')
    # if(bhadata.type_name=='Drill Pipe'):
    #     print(f"length {length}")
    #     print(f"length_of_drillpipebody {length_of_drillpipebody}")
    #     print(f"pin_length {pin_length}")
    #     print(f"box_length {box_length}")
    #     print(f"noof_pipe {noof_pipe}")
    #     print(f"noof_tj {noof_tj}")
    #     print(f"casing_box_annular {box_annular}")
    #     print(f"pin_pressureloss {pin_pressureloss}")
    #     print(f"box_pressureloss {box_pressureloss}")
    #     print(f"casing_pin_annular {pin_annular}")
    
    data['tjpressureloss']=pin_pressureloss['pressureloss']+box_pressureloss['pressureloss']
    data['tjannularloss']=pin_annular['pressureloss']+box_annular['pressureloss']

    # print(f"data {data}")
     
    return data

def calculatecuttings_concentration(well_id,flowrate,rop,slipvelocity,bitelement,sectiontodepth):
    # print(f"slipvelocity {slipvelocity}")
    unit = getprojectunit(well_id)
    flowrate = calculate_flowrate(flowrate,unit)
    rop = calculate_rop(float(rop),unit)
    bitelement_od = calculate_od(float(bitelement.od),unit)
    vc=int(rop)/60*0.7854*float(bitelement_od)**2/144
    od=5
    vm=flowrate/7.48
    i=0
    allcuttingdata=[]
    for slipvelocity in slipvelocity:
        slipvelocity_od = calculate_od(float(slipvelocity["od"]),unit)
        slipvelocity_hole_size = calculate_holesize(float(slipvelocity['cased_hole_size']),unit)

        bhaelementcon=24.51*flowrate/(float(bitelement_od)**2-float(slipvelocity_od)**2)
        alldata_length=len(allcuttingdata)
        if(alldata_length>1):
            if(allcuttingdata[alldata_length-1]['y']%100!=0):
               i -=100
        while i<slipvelocity["y"]:
            i +=100
            if(i>slipvelocity["y"]):
                av=24.51*flowrate/(float(slipvelocity_hole_size)**2-float(slipvelocity_od)**2)
                conc=-0.5*(av/slipvelocity["x"]-1)+(0.25*(av/slipvelocity["x"]-1)**2+av/slipvelocity["x"]*vc/vm)**0.5
                allcuttingdata.append({'y':slipvelocity['y'],'av':av,'x':round(conc*100,2)})
            else:
                av=24.51*flowrate/(float(slipvelocity_hole_size)**2-float(slipvelocity_od)**2)
                conc=-0.5*(av/slipvelocity["x"]-1)+(0.25*(av/slipvelocity["x"]-1)**2+av/slipvelocity["x"]*vc/vm)**0.5
                allcuttingdata.append({'y':i,'av':av,'x':round(conc*100,2)}) 
    return allcuttingdata

def getsurfacelosses(rpm,flowrate,wellphase_id,section_name,mud_weight,wellphase,previous_wellphase,well_id,viscocity,typename):  
    surfacepipe=SurfacePipe.objects.getsurfacepipe(well_id)
    surfacepipedata=SurfacePipeData.objects.getsurfacepipedata(surfacepipe)
    allpressureloss=[]
    # if(typename=='viscocitychange'):
    #     print(f"viscocity {viscocity}")
    for surfacedata in surfacepipedata:
        if(surfacedata.length !='' and surfacedata.identity !=''):
            pressureloss=calculatepressloss(well_id,rpm,flowrate,mud_weight,surfacedata.identity,surfacedata.length,viscocity,typename)
            # if(typename=='check'):
            #     print(f"pressureloss {pressureloss}")
            allpressureloss.append({
                'pressureloss' :round(pressureloss['pressureloss'],2),
                'type':surfacedata.name,
                'id':surfacedata.identity,
                'length':surfacedata.length
            })
    return allpressureloss  

def gettotalresult(pressureloss,surfaceloss):
    totalpressure_loss=0
    totalannular_pressureloss=0
    totaldrillstring_pressureloss=0
    for pressurelossdata in pressureloss['allpressureloss']:
        totalpressure_loss +=pressurelossdata['pressureloss']
        totalpressure_loss +=pressurelossdata['drillstringloss']
        totaldrillstring_pressureloss +=pressurelossdata['drillstringloss']
        totalannular_pressureloss +=pressurelossdata['pressureloss']

    for surfacelossdata in surfaceloss:
        totalpressure_loss +=surfacelossdata["pressureloss"]
    
    data={
        'totalpressure_loss':totalpressure_loss,
        'totaldrillstring_pressureloss':totaldrillstring_pressureloss,
        'totalannular_pressureloss':totalannular_pressureloss
       
    }

    return data

def getbitpressureloss(rpm,flowrate,wellphase_id,section_name,mudweight,wellphase,previous_wellphase,well_id):
    drillbit = DrillBit.objects.getdrillbit(well_id,wellphase_id)
    bittype = BitTypesNames.objects.getbittypesname(drillbit.bit_type_id)
    nozzle_size = DrillBitNozzle.objects.getdrillbitnozzle(drillbit,well_id)
    unit = getprojectunit(well_id)
    if(drillbit.external_nozzle == 1):
        cd_values = 0.95
    else:
        cd_values = bittype.bit_values
    tfa_value=drillbit.tfa

    hole_size = wellphase.hole_size
      
    bit_losses = bit_loss_conversion(flowrate,mudweight,tfa_value,cd_values,hole_size,unit)
    data=[]
    nozzles=[]
    for nozzle in nozzle_size:
        nozzles.append(nozzle.nozzle_size)
    data.append({
        'nozzle_size':nozzles,
        'tfa_value':tfa_value,
        'bit_pressure_loss':bit_losses[0]['bit_pressure_loss'],
        'bhhp':bit_losses[0]['bhhp'],
        'hsi':bit_losses[0]['hsi'],
        'impact_forces':bit_losses[0]['impact_forces'],
        'jet_velocity':bit_losses[0]['jet_velocity'],
        'cd_values':cd_values
    })
    return data

def calculatebitpressureloss(request):
    data = request.body
    json_data = json.loads(data)
    section_name=json_data.get('section_name')
    wellphase_id=json_data.get('wellphase_id')
    given_bitdepth=json_data.get('bitdepth')
    rpm=json_data.get('rpm')
    rop=json_data.get('rop')
    flowrate=int(json_data.get('flowrate'))
    muddata=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    sectiontodepth=muddata.todepth if(given_bitdepth=='') else int(given_bitdepth)
    wellphase = WellPhases.objects.getwellphase_byid(wellphase_id)
    well_id=request.session['well_id']
    previous_wellphase=WellPhases.objects.getprevious_wellphase(wellphase.id,well_id)
    section_details=Sections.objects.filter(section_name=section_name,well_phase_id=wellphase_id,well_id=well_id,status=1).first()
    selected_modal=getmodaltext(section_details.selected_model)
    viscocity=getviscocity(muddata)
    plastic_viscocity = app_filters.getpvyp(section_details,wellphase_id,'plastic_viscocity')
    yieldpoint = app_filters.getpvyp(section_details,wellphase_id,'yield_point')
    bit_losses=getbitpressureloss(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id)
    sectionfromdepth=muddata.from_depth
    fromdepthtvd=gettvd(sectionfromdepth,well_id,request,sectiontodepth)
    todepthtvd=gettvd(sectiontodepth,well_id,request,sectiontodepth)

    data={
        'bit_losses':bit_losses,
        'todepth':sectiontodepth,
        'mudweight':muddata.mud_weight,
        'pv':plastic_viscocity,
        'yp':yieldpoint if 'yieldpoint' in viscocity else '',
        'selected_modal':selected_modal,
        'K':round(viscocity["K"],2) if 'K' in viscocity else '',
        'm':round(viscocity["n"],2) if 'n' in viscocity else '',
        'fromdepth':sectionfromdepth,
        'fromdepthtvd':fromdepthtvd,
        'todepthtvd':todepthtvd
    }

    input_data={
        'flowrate':flowrate,
        'rpm':rpm,
        'rop':rop
    }
    Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'bitpressureloss',json.dumps(bit_losses),json.dumps(input_data))

    return JsonResponse(data,safe=False)

def calculatesurfacelosses(request):
    data = request.body
    json_data = json.loads(data)
    wellphase_id=json_data.get('wellphase_id')
    section_name=json_data.get('section_name')
    wellphase_id=json_data.get('wellphase_id')
    rpm=json_data.get('rpm')
    rop=json_data.get('rop')
    flowrate=int(json_data.get('flowrate'))
    well_id=request.session['well_id']
    wellphase = WellPhases.objects.getwellphase_byid(wellphase_id)
    previous_wellphase=WellPhases.objects.getprevious_wellphase(wellphase.id,well_id)
    muddata=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    viscocity=getviscocity(muddata)
    surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity,'check')
    input_data={
        'flowrate':flowrate,
        'rpm':rpm,
        'rop':rop
    }
    Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'surfacepressureloss',json.dumps(surface_losses),json.dumps(input_data))
    return JsonResponse(surface_losses,safe=False)

def getviscocity(muddata):
    sectionname=muddata.section
    well_phase_id = muddata.well_phase_id
    rheogramsections=RheogramSections.objects.filter(section_name=sectionname,status=1).first()
    sections=Sections.objects.filter(section_name=sectionname,well_phase_id=well_phase_id,status=1).first()
    if(sections.selected_model=="1"):
        data=calculate_viscocity_newtonian(rheogramsections,sections,muddata)
    elif(sections.selected_model=="2"):
        data=calculate_viscocity_bingham(rheogramsections,sections,muddata)
    elif(sections.selected_model=="4"):
        data=calculate_viscocity_hershel(rheogramsections,sections,muddata)
    elif(sections.selected_model=="3"):
        data=calculate_viscocity_powerlaw(rheogramsections,sections,muddata)
    return data

#calculate viscocity and yield point based on selected modal in rheogram
def getviscocity(muddata):
    sectionname=muddata.section
    well_phase_id = muddata.well_phase_id
    rheogramsections=RheogramSections.objects.filter(section_name=sectionname,status=1).first()
    sections=Sections.objects.filter(section_name=sectionname,well_phase_id=well_phase_id,status=1).first()
    if(sections.selected_model=="1"):
        data=calculate_viscocity_newtonian(rheogramsections,sections,muddata)
    elif(sections.selected_model=="2"):
        data=calculate_viscocity_bingham(rheogramsections,sections,muddata)
    elif(sections.selected_model=="4"):
        data=calculate_viscocity_hershel(rheogramsections,sections,muddata)
    elif(sections.selected_model=="3"):
        data=calculate_viscocity_powerlaw(rheogramsections,sections,muddata)
    return data

def gettvd(data,well_id,request,todepth): 
    welltrajectory=WellTrajectory.objects.filter(measured_depth=data,company=request.company,well_id=well_id)
    if(welltrajectory.count()>0):
        val=welltrajectory[0].true_vertical_depth
    else:
        if(data>todepth):
            trajectory=WellTrajectory.objects.filter(company=request.company,well_id=well_id).order_by('-id')[:1].first()
            val=trajectory.true_vertical_depth
        else:
            belowmd=WellTrajectory.objects.filter(measured_depth__lte=data,company=request.company,well_id=well_id).order_by('-measured_depth')[:1].first()
            abovemd=WellTrajectory.objects.filter(measured_depth__gte=data,company=request.company,well_id=well_id).order_by('measured_depth')[:1].first()
            previous_md=WellTrajectory.objects.filter(id=belowmd.id)
            next_md=WellTrajectory.objects.filter(id=abovemd.id)
            pre_md=previous_md[0].measured_depth
            n_md=next_md[0].measured_depth
            pre_inc=previous_md[0].inclination
            n_inc=next_md[0].inclination
            pre_azi=previous_md[0].azimuth
            n_azi=next_md[0].azimuth
            pre_tvd=previous_md[0].true_vertical_depth
            dl_inc = acos(sin(n_inc*pi/180)*sin(pre_inc*pi/180)+(cos(pre_inc*pi/180)*cos(n_inc*pi/180)))*180/pi
            dls_inc=round(dl_inc,2)*100/(n_md-pre_md)
            dl_azi=acos(cos((n_azi-pre_azi)*pi/180))*180/pi
            dls_azi=round(dl_azi,2)*100/(n_md-pre_md)
            target_inculination=dls_inc*(float(data)-pre_md)/100+pre_inc
            target_azimuth=pre_azi-dls_azi*(float(data)-pre_md)/100
            target_rf=tan(dl_inc/2*pi/180)*180/pi*2/dl_inc if dl_inc != 0 else 1
            val=(cos(pre_inc*pi/180)+cos(round(target_inculination,2)*pi/180))*round(target_rf)*(float(data)-pre_md)/2+pre_tvd
    return val

def pressurelosschart(request):
    rpm=request.GET['rpm']
    flowrate=int(request.GET['flowrate'])
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    surface_value=request.GET['surface_value']
    annular_value=request.GET['annular_value']
    drillstring_value=request.GET['drillstring_value']
    bit_value=request.GET['bit_value']
    well_id=request.session['well_id']
    torque=request.GET['torque'] if 'torque' in request.GET else ""
    wob=request.GET['wob'] if 'wob' in request.GET else ""
    rop=request.GET['rop']
    request.session['rop_input']=rop
    request.session['rpm_input']=rpm
    given_bitdepth=request.GET['bitdepth']  
    unit = getprojectunit(well_id)
    cuttings_density=converttofloat(request.GET['cuttings_density'])
    cuttings_size=converttofloat(request.GET['cuttings_size'])
    muddata=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    print(f"muddata {muddata.todepth}")
    viscocity=getviscocity(muddata)
    wellphase = WellPhases.objects.getwellphase_byid(wellphase_id)
    previous_wellphase=WellPhases.objects.getprevious_wellphase(wellphase.id,well_id)
    length_of_previous_casing_from_surface=0 if previous_wellphase==None else previous_wellphase.measured_depth
    wellphasefromdepth=0 if previous_wellphase==None else previous_wellphase.measured_depth
    wellphasetodepth= wellphase.measured_depth
    sectionfromdepth=muddata.from_depth
    sectiontodepth=muddata.todepth if(given_bitdepth=='') else int(given_bitdepth)
    liner_wellphase=WellPhases.objects.filter(well_id=well_id,status=1).values('lineartop')
    previous_measured_depth=0 if previous_wellphase==None else previous_wellphase.measured_depth
    previous_true_vertical_depth=0 if previous_wellphase==None else previous_wellphase.true_vertical_depth
    previous_linear=0 if previous_wellphase==None else previous_wellphase.measured_depth
    bitdepth=sectiontodepth if(given_bitdepth=='') else int(given_bitdepth)
    length_of_openhole_from_bitdepth=bitdepth-length_of_previous_casing_from_surface
    length_of_selected_section_from_surface=sectiontodepth
    hole_size=wellphase.hole_size
    id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
    allpressureloss={}
    checkliner=WellPhases.objects.checkliner(well_id,sectiontodepth)
    bhadata=BhaData.objects.getbha(wellphase_id)
    bore_pressure_loss=calculatepipe_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate)
    print('bore_loss',bore_pressure_loss)
    if(checkliner.count()>0):
        annular_pressure_loss=calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),wellphase_id,checkliner,well_id,cuttings_density,
        cuttings_size,torque,wob,rop,viscocity,'calculateallpressurelossliner')
    else:
        annular_pressure_loss=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity,'calculateallpressureloss')
    # print(f"annular_pressure_loss {annular_pressure_loss['allpressureloss']}")
    surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity,'check')
    section_details=Sections.objects.filter(section_name=section_name,well_phase_id=wellphase_id,well_id=well_id,status=1).first()
    selected_modal=getmodaltext(section_details.selected_model)
    bit_losses=getbitpressureloss(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id)
 
    viscocity=getviscocity(muddata)
    # print(f"viscocity {viscocity}")
    plastic_viscocity = app_filters.getpvyp(section_details,wellphase_id,'plastic_viscocity')
    yieldpoint = app_filters.getpvyp(section_details,wellphase_id,'yield_point')
    mudtvd=[]
    muddatas=MudData.objects.filter(well_id=well_id,status=1).order_by('todepth')
    i=0
    while(i<len(muddatas)):
        md=getmd(request,muddatas[i].todepth)
        mudtvd.append(md)
        i+=1
    bitelement=BhaElement.objects.filter(bhadata_id=bhadata.id,type_name='Bit',status=1).first()
    type_name=bitelement.type_name
    bit_od=bitelement.od
    bit_length=bitelement.length

    chartdata=getallpressurelosschartdata(bore_pressure_loss,annular_value,surface_value,bit_value,previous_wellphase,rpm,flowrate,muddata,bhadata,sectiontodepth,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),checkliner,wellphase_id,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity,drillstring_value)
    input_data={
        'flowrate':flowrate,
        'rpm':rpm,
        'rop':rop
    }
    Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'pressureloss',json.dumps(chartdata),json.dumps(input_data))

    data = {
        'previous_measured_depth':previous_measured_depth,
        'previous_linear':previous_linear,
        'chartdata':chartdata
    }

    return JsonResponse(data,safe=False)

def calculatepipe_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate):
    bhaelement=BhaElement.objects.filter(length_onejoint=sectiontodepth).first()
    # print(f"bhaelement {bhaelement}")
    # print(f"sectiontodepth {sectiontodepth}")
    allpressureloss=[]
    if(bhaelement==None):
        nextbhaelement=BhaElement.objects.filter(bhadata_id=bhadata.id,length_onejoint__gt=sectiontodepth).first()
        # print(f"nextbhaelement {nextbhaelement}")
        belowbha=BhaElement.objects.filter(bhadata_id=bhadata.id,id__lt=nextbhaelement.id).order_by("-id").first()
        previousbhaelement=BhaElement.objects.filter(Q(type_name='Drill Pipe') | Q(type_name='Heavy Weight Drill Pipe') | Q(type_name='Drill Collar') | Q(type_name='NMDC') | Q(type_name='Stabilizer') | Q(type_name='Jar')).filter(bhadata_id=bhadata.id,length_onejoint__lt=sectiontodepth)
        viscocity=getviscocity(muddata)
        for previousbha in previousbhaelement:
            pressureloss=calculatepressloss(well_id,rpm,flowrate,muddata.mud_weight,previousbha.identity,previousbha.length,viscocity,'calculatepipe_pressureloss')
            allpressureloss.append({
                'pressureloss' :pressureloss['pressureloss'],
                'viscocity':round(pressureloss['viscocity_si'],2),
                'flowrate':round(pressureloss['flowrate_si'],2),
                'mudweight':round(pressureloss['mudweight_si'],2),
                'ID':round(float(pressureloss['identity']),2),
                'length':round(float(pressureloss['originallength']),2),
                'velocity':round(pressureloss['velocity'],2),
                'reynolds':round(pressureloss['Re'],2),
                # 'flowregime':pressureloss['flowregime'],
                # 'frictionpressure':round(pressureloss['f'],2),
                'type':previousbha.type_name,
                'cumulative_length':previousbha.length_onejoint
            })
        newlength=sectiontodepth-belowbha.length_onejoint
        pressureloss=calculatepressloss(well_id,rpm,flowrate,muddata.mud_weight,nextbhaelement.identity,newlength,viscocity,'calculatepipe_pressureloss')
        allpressureloss.append({
            'pressureloss' :round(pressureloss['pressureloss'],2),
            'viscocity':round(pressureloss['viscocity_si'],2),
            'flowrate':round(pressureloss['flowrate_si'],2),
            'mudweight':round(pressureloss['mudweight_si'],2),
            'ID':round(float(pressureloss['identity']),2),
            'length':round(float(pressureloss['originallength']),2),
            'velocity':round(pressureloss['velocity'],2),
            'reynolds':round(pressureloss['Re'],2),
            # 'flowregime':pressureloss['flowregime'],
            # 'frictionpressure':round(pressureloss['f'],2),
            'type':nextbhaelement.type_name,
            'cumulative_length':nextbhaelement.length_onejoint

        })
    else:
        previousbhaelement=BhaElement.objects.filter(Q(type_name='Drill Pipe') | Q(type_name='Heavy Weight Drill Pipe') | Q(type_name='Drill Collar')  | Q(type_name='NMDC') | Q(type_name='Stabilizer') | Q(type_name='Jar')).filter(bhadata_id=bhadata.id,length_onejoint__lte=sectiontodepth)
        viscocity=getviscocity(muddata)

        for previousbha in previousbhaelement:
            pressureloss=calculatepressloss(well_id,rpm,flowrate,muddata.mud_weight,previousbha.identity,previousbha.length,viscocity,'calculatepipe_pressureloss')
            # print(pressureloss['identity'])
            allpressureloss.append({
                'pressureloss' :round(pressureloss['pressureloss'],2),
                'viscocity':round(pressureloss['viscocity_si'],2),
                'flowrate':round(pressureloss['flowrate_si'],2),
                'mudweight':round(pressureloss['mudweight_si'],2),
                'ID':round(float(pressureloss['identity']),2),
                'length':round(float(pressureloss['originallength']),2),
                'velocity':round(pressureloss['velocity'],2),
                'reynolds':round(pressureloss['Re'],2),
                # 'flowregime':pressureloss['flowregime'],
                # 'frictionpressure':round(pressureloss['f'],2),
                'type':previousbha.type_name,
                'cumulative_length':previousbha.length_onejoint

            })
    return allpressureloss

def calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity,typename):
    # print(f"length_of_previous_casing_from_surface {length_of_previous_casing_from_surface}")
    allpressureloss=[]
    increased_pressureloss=[]
    alllinerdata=[]
    allslipvelocity=[]
    slipvelocitychart=[]
    allslipvelocitychartdata=[]
    allslipvelocityanuulardata=[]

    slipvelocitychart_walker=[]
    annularvelocitychartdata_walker=[]

    annularvelocitychartdata=[]
    allslipvelocity_walker=[]
    calculate_tj_pressureloss =[]
    calculate_tj_pressureloss_increased=[]
    bitelement=BhaElement.objects.filter(bhadata_id=bhadata.id,type_name='Bit',status=1).first()

    length_of_open_hole=length_of_selected_section_from_surface-length_of_previous_casing_from_surface
    previousbhaelement=BhaElement.objects.getbhaelement(bhadata.id)
    bhacount=previousbhaelement.count()
    i=bhacount
    previous_length_against_casing=[]
    cumlativelength=0
    for previousbha in previousbhaelement:
        if(previousbha.length_onejoint<sectiontodepth):
            newlength=converttofloat(previousbha.length)
        else:
            belowbha=BhaElement.objects.getpreviousbhaelement(bhadata.id,previousbha.id)
            newlength=sectiontodepth-belowbha.length_onejoint
        od_of_pipe_element=previousbha.od
        if(i==bhacount):
            length_against_casing=length_of_previous_casing_from_surface if(converttofloat(newlength)>=length_of_previous_casing_from_surface) else newlength
            previous_length_against_casing.append(length_against_casing)
        else:
            sum_of_previous_against_casing=Sum = sum(previous_length_against_casing)
            if(sum_of_previous_against_casing==length_of_previous_casing_from_surface):
                length_against_casing=0
            if((sum_of_previous_against_casing<length_of_previous_casing_from_surface) and (sum_of_previous_against_casing+newlength<length_of_previous_casing_from_surface)):
                length_against_casing=newlength
            else:
                length_against_casing=length_of_previous_casing_from_surface-sum_of_previous_against_casing
            previous_length_against_casing.append(length_against_casing)
        length_against_open_hole=converttofloat(newlength)-length_against_casing
      
        if(length_against_casing!=0):
            # print("casing")
            # print(id_of_previous_casing)
            pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,muddata.mud_weight,previousbha.od,id_of_previous_casing,length_against_casing,'annularpressurelosscasing')
            if((previousbha.type_name=='RSS') or (previousbha.type_name=='MWD') or (previousbha.type_name=='LWD') or (previousbha.type_name=='Others') or (previousbha.type_name=='Mud Motor')):
                drillstringpressureloss=calculate_drillstringloss_downholetools(previousbha,flowrate,muddata.mud_weight,torque,wob)
            else:
                drillstringpressureloss=calculatepressloss(well_id,rpm,flowrate,muddata.mud_weight,previousbha.identity,length_against_casing,viscocity,'calculateannular_pressureloss')
            
            cumlativelength +=length_against_casing
            slipvelocity=calculateslipvelocitywithoutliner(well_id,rpm,flowrate,muddata.mud_weight,id_of_previous_casing,previousbha.od,viscocity,cuttings_density,cuttings_size,length_against_casing)
            slipvelocitywalker= slipvelocity_walker(muddata,id_of_previous_casing,rpm,previousbha.od,cuttings_density,cuttings_size,flowrate)
            # print(f'slipvelocity {slipvelocitywalker}')
            
            if(slipvelocity["slipvelocity"]>=slipvelocitywalker["slipvelocity"]):
                slipvelocityvalue=slipvelocity["slipvelocity"]
            else:
                slipvelocityvalue=slipvelocitywalker["slipvelocity"]
            
            allslipvelocitychartdata.append({'x':round(slipvelocityvalue),"y":cumlativelength,'od':previousbha.od,'cased_hole_size':id_of_previous_casing,'annular_velocity':round(slipvelocity["annular_velocity"]),'element_type':'CH'})
            allslipvelocityanuulardata.append({"x":round(slipvelocity["annular_velocity"]),"y":cumlativelength})

            increased_mudweight=calculate_increased_mudweight(well_id,flowrate,id_of_previous_casing,previousbha.od,rop,slipvelocityvalue,muddata.mud_weight,cuttings_density)
            # print(f"increased_mudweight {increased_mudweight}")

            increased_pressurelossvalue=calculate_annular_loss(well_id,viscocity,flowrate,rpm,increased_mudweight["increased_mudweight"],previousbha.od,id_of_previous_casing,length_against_casing,'calculateannular_pressureloss_increased')
            # print(f"increased_pressurelossvaluetest {increased_pressurelossvalue}")


            
            if((previousbha.type_name=='Drill Pipe') or (previousbha.type_name=='Heavy Weight Drill Pipe')):
                # print(f"pressureloss {increased_pressurelossvalue}")
                calculate_tj_pressureloss=calculatetjpressureloss(previousbha.length,length_against_casing,previousbha,rpm,flowrate,viscocity,muddata.mud_weight,id_of_previous_casing,'without')
                calculate_tj_pressureloss_increased=calculatetjpressureloss(previousbha.length,length_against_casing,previousbha,rpm,flowrate,viscocity,increased_mudweight["increased_mudweight"],id_of_previous_casing,'with')
                # print(f"calculate_tj_pressureloss_increased {calculate_tj_pressureloss_increased}")
           
                # calculate_tj_pressureloss=0
            # print(pressureloss["pressureloss"])
            # if(previousbha.type_name=='Drill Collar'):
            #     print("vdvdg")
            
            allpressureloss.append({
                'flowregime' : pressureloss["flowregime"],
                'od':round(converttofloat(od_of_pipe_element),2),
                'id':round(converttofloat(previousbha.identity),2),
                'type':previousbha.type_name,
                'element':previousbha.element,
                'length_against':length_against_casing,
                'pressureloss':round(pressureloss["pressureloss"]+calculate_tj_pressureloss["tjannularloss"],2),
                'element_type':'CH',
                'drillstringloss':round(drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"],2)  if 'pressureloss' in drillstringpressureloss else drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"],
                'mudweight':muddata.mud_weight,
                'cumlativelength':cumlativelength

            })
            increased_pressureloss.append({
                'flowregime' : increased_pressurelossvalue["flowregime"],
                'od':round(converttofloat(od_of_pipe_element),2),
                'id':round(converttofloat(previousbha.identity),2),
                'type':previousbha.type_name,
                'element':previousbha.element,
                'length_against':length_against_casing,
                'pressureloss':round(increased_pressurelossvalue["pressureloss"]+calculate_tj_pressureloss_increased["tjannularloss"],2),
                'element_type':'CH',
                'mudweight':increased_mudweight["increased_mudweight"]
            })
            # print(f"allpressureloss {allpressureloss}")

        
        if(length_against_open_hole!=0):
            # print(f"element {previousbha.type_name}")
            # print("openhole")
            pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,muddata.mud_weight,previousbha.od,hole_size,length_against_open_hole,'annularpressurelossnewtonian')
            if((previousbha.type_name=='RSS') or (previousbha.type_name=='MWD') or (previousbha.type_name=='LWD') or (previousbha.type_name=='Others') or (previousbha.type_name=='Mud Motor')):
                drillstringpressureloss=calculate_drillstringloss_downholetools(previousbha,flowrate,muddata.mud_weight,torque,wob)
            else:
                drillstringpressureloss=calculatepressloss(well_id,rpm,flowrate,muddata.mud_weight,previousbha.identity,length_against_open_hole,viscocity,'calculateannular_pressureloss')
            # print(f'drillstring hole {drillstringpressureloss}')
            cumlativelength +=length_against_open_hole
            
            if((previousbha.type_name=='Drill Pipe') or (previousbha.type_name=='Heavy Weight Drill Pipe')):
                calculate_tj_pressureloss=calculatetjpressureloss(previousbha.length,length_against_open_hole,previousbha,rpm,flowrate,viscocity,muddata.mud_weight,hole_size,'without')
           

            allpressureloss.append({
                'flowregime' : pressureloss["flowregime"],
                'od':round(converttofloat(od_of_pipe_element),2),
                'id':round(converttofloat(previousbha.identity),2),
                'type':previousbha.type_name,
                'element':previousbha.element,
                'length_against':length_against_open_hole,
                'pressureloss':round(pressureloss["pressureloss"]+calculate_tj_pressureloss['tjannularloss'],2),
                'element_type':'OH',
                'drillstringloss':round(drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"],2)  if 'pressureloss' in drillstringpressureloss else drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"],
                'mudweight':muddata.mud_weight,
                'cumlativelength':cumlativelength

            })
            # print(f"allpressureloss {allpressureloss}")
            slipvelocity=calculateslipvelocitywithoutliner(well_id,rpm,flowrate,muddata.mud_weight,hole_size,previousbha.od,viscocity,cuttings_density,cuttings_size,length_against_open_hole)
            # print(f"slipvelocity {slipvelocity}")
            slipvelocitywalker= slipvelocity_walker(muddata,hole_size,rpm,previousbha.od,cuttings_density,cuttings_size,flowrate)
            # print(f'slipvelocitywalker {slipvelocitywalker}')
            if(slipvelocity["slipvelocity"]>=slipvelocitywalker["slipvelocity"]):
                slipvelocityvalue=slipvelocity["slipvelocity"]
            else:
                slipvelocityvalue=slipvelocitywalker["slipvelocity"]
            allslipvelocitychartdata.append({'x':round(slipvelocityvalue),"y":cumlativelength,'od':previousbha.od,'cased_hole_size':hole_size,'annular_velocity':round(slipvelocity["annular_velocity"]),'element_type':'OH'})
            allslipvelocityanuulardata.append({"x":round(slipvelocity["annular_velocity"]),"y":cumlativelength})
            
            increased_mudweight=calculate_increased_mudweight(well_id,flowrate,hole_size,previousbha.od,rop,slipvelocityvalue,muddata.mud_weight,cuttings_density)
            # print(f"increased_mudweight {increased_mudweight}")
            increased_pressurelossvalue=calculate_annular_loss(well_id,viscocity,flowrate,rpm,increased_mudweight["increased_mudweight"],previousbha.od,hole_size,length_against_open_hole,'calculateannular_pressureloss_increased')
            # print(f"increased_pressurelossvalue {increased_pressurelossvalue}")
            
   
            if((previousbha.type_name=='Drill Pipe') or (previousbha.type_name=='Heavy Weight Drill Pipe')):
                calculate_tj_pressureloss_increased=calculatetjpressureloss(previousbha.length,length_against_open_hole,previousbha,rpm,flowrate,viscocity,increased_mudweight["increased_mudweight"],hole_size,'with')
                # print(f"calculate_tj_pressureloss_increased {calculate_tj_pressureloss_increased}")
            

            increased_pressureloss.append({
                'flowregime' : increased_pressurelossvalue["flowregime"],
                'od':round(converttofloat(od_of_pipe_element),2),
                'id':round(converttofloat(previousbha.identity),2),
                'type':previousbha.type_name,
                'element':previousbha.element,
                'length_against':length_against_open_hole,
                'pressureloss':round(increased_pressurelossvalue["pressureloss"]+calculate_tj_pressureloss_increased['tjannularloss'],2),
                'element_type':'OH',
                'mudweight':increased_mudweight["increased_mudweight"]
                
            })


    
        # if((previousbha.type_name=='Drill Pipe') or (previousbha.type_name=='Heavy Weight Drill Pipe')):
        #     calculate_tj_pressureloss=calculatetjpressureloss(previousbha.length,length_against_casing,length_against_open_hole,previousbha,rpm,flowrate,viscocity,muddata.mud_weight,hole_size,id_of_previous_casing)
        #     totaltjpressureloss +=calculate_tj_pressureloss['tjpressureloss']
        #     totaltjannularloss +=calculate_tj_pressureloss['tjannularloss']

        
        previouselement_length=previousbha.length_onejoint
        i -=1
    
    


    # print(f"allslipvelocitychartdata {allslipvelocitychartdata}")
    cuttingsconcentration=calculatecuttings_concentration(well_id,flowrate,rop,allslipvelocitychartdata,bitelement,sectiontodepth)
    if(typename !='displayallmodels'):
        transportratio=calculatetransportratio(well_id,allslipvelocitychartdata,viscocity,flowrate)
        # print(f"transportratio {transportratio}")
        cci=calculatecci(well_id,allslipvelocitychartdata,viscocity,flowrate,muddata.mud_weight)

    # print(f"allpressureloss {allpressureloss}")
    # print(f"increased_pressureloss {increased_pressureloss}")
    # if(typename=='displayallmodelsnewtonian'):
    #     print(f"allpressureloss {allpressureloss}")
    data={
        'allpressureloss':allpressureloss, 
        'slipvelocitychart':allslipvelocitychartdata,
        'annularvelocitychartdata':allslipvelocityanuulardata,
        'calculate_tj_pressureloss':calculate_tj_pressureloss,
        # 'totaltjpressureloss':totaltjpressureloss,
        # 'totaltjannularloss':totaltjannularloss,
        'cuttingsconcentration':cuttingsconcentration,
        'increased_pressureloss':increased_pressureloss
    }
    if(typename !='displayallmodels'):
        data['transportratio']=transportratio
        data['cci']=cci

        

    return data

def calculatetransportratio(well_id,allpressureloss,viscocity,flowrate):
    unit = getprojectunit(well_id)
    plastic_viscocity = viscocity['displaypv']
    if(viscocity['selected_modal']=="1"):
        yeildpoint=0
    else:
        yeildpoint = viscocity['yieldpoint']
    i=0
    # print(f"viscocitytransport {viscocity}")
    allcuttingdata=[]
    n=3.222*log10((2*plastic_viscocity+yeildpoint)/(plastic_viscocity+yeildpoint))
    K=511**(1-n)*(plastic_viscocity+yeildpoint)/1000/0.4788
    for slipvelocity in allpressureloss:
        alldata_length=len(allcuttingdata)
        if(alldata_length>1):   
            if(allcuttingdata[alldata_length-1]['y']%100!=0):
               i -=100
        while i<slipvelocity["y"]:
            i +=100
            
            tr=1-slipvelocity['x']/slipvelocity['annular_velocity'] if slipvelocity['annular_velocity'] else 0

            if(i>slipvelocity["y"]):
                allcuttingdata.append({'y':slipvelocity['y'],'x':round(tr*100),'av':slipvelocity['annular_velocity']})
            else:
                allcuttingdata.append({'y':i,'x':round(tr*100),'av':slipvelocity['annular_velocity']}) 
    
    return allcuttingdata
    
    # print(f"allcuttingdata {allcuttingdata}")

def calculatecci(well_id,allpressureloss,viscocity,flowrate,mudweight):
    unit=getprojectunit(well_id)
    mudweight=calculate_mudweight(mudweight,unit) 
    plastic_viscocity=viscocity['displaypv']
    if(viscocity['selected_modal']=="1"):
        yeildpoint=0
    else:
        yeildpoint=viscocity['yieldpoint']
    i=0
    # print(f"viscocitycci {viscocity}")
    allcuttingdata=[]
    n=3.222*log10((2*plastic_viscocity+yeildpoint)/(plastic_viscocity+yeildpoint))
    K=511**(1-n)*(plastic_viscocity+yeildpoint)
    # print(f"n {n}")
    # print(f"K {K}")
    # print(f'mudweight {mudweight}')
    # print(f'flowrate {flowrate}')
    # print(f'PV {plastic_viscocity}')
    # print(f'YP {yeildpoint}')

    # print(f"allpressureloss {allpressureloss}")

    for slipvelocity in allpressureloss:
        # print(f"slipvelocity {slipvelocity}")
        alldata_length=len(allcuttingdata)
        if(alldata_length>1):   
            if(allcuttingdata[alldata_length-1]['y']%100!=0):
               i -=100
        while i<slipvelocity["y"]:
            i +=100
         
            cci=mudweight*K*float(slipvelocity['annular_velocity'])/400000

            if(i>slipvelocity["y"]):
                allcuttingdata.append({'y':slipvelocity['y'],'x':cci,'av':slipvelocity['annular_velocity']})
            else:
                allcuttingdata.append({'y':i,'x':round(cci,2),'av':slipvelocity['annular_velocity']}) 
    # print(f'cci {allcuttingdata}')
    return allcuttingdata

def getallpressurelosschartdata(bore_pressure_loss,annular_pressure_loss,surface_losses,bit_losses,previous_wellphase,rpm,flowrate,muddata,bhadata,sectiontodepth,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,linercount,checkliner,wellphase_id,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity,drillstring_value):
    pressurelosschartdata=[]
    drillstringdata=[]
    surfaceloss = float(surface_losses)
    drillstringloss = float(drillstring_value)
    annularloss = float(annular_pressure_loss)
    bitloss = float(bit_losses)
    # print('flowrate',flowrate)
    # print('allloss',surfaceloss,drillstringloss,annularloss,bitloss)
    totalpressureloss=surfaceloss+drillstringloss+annularloss+bitloss
    # print('total_loss',totalpressureloss)
    
    circulationloss=totalpressureloss-surfaceloss
    insidesrillstring=calculatepipe_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate)
    if(linercount>0):
        annular_pressure_loss=calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),wellphase_id,checkliner,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity,'pressurelosschartdataliner')
    else:
        annular_pressure_loss=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity,'pressurelosschartdata')

    
    # print(f'annular_pressure_loss  {annular_pressure_loss}')
    drillstringdata.append({"length":0,"MD":0,"pressureloss":0,"calculated_pressureloss":0,'loss_alongwell':totalpressureloss})
    drillstringdata.append({"length":0,"MD":0,"pressureloss":surfaceloss,"calculated_pressureloss":surfaceloss,'loss_alongwell':totalpressureloss-surfaceloss})
    drillstringcumulativelength=0
    for drillstringloss in annular_pressure_loss['allpressureloss']:
        drillstringdata_length=len(drillstringdata)
        drillstringcumulativelength=drillstringcumulativelength+drillstringloss['length_against']
        previousdrillstringdata=drillstringdata[drillstringdata_length-1]
        new_loss_alongwell=previousdrillstringdata['loss_alongwell']-drillstringloss['drillstringloss']
        calculatedpressureloss=sum(drillstring['pressureloss'] for drillstring in drillstringdata)
        drillstringdata.append({"length":drillstringloss['length_against'],"MD":drillstringcumulativelength,"pressureloss":drillstringloss['drillstringloss'],"calculated_pressureloss":calculatedpressureloss+drillstringloss['drillstringloss'],'loss_alongwell':new_loss_alongwell})
    
    drillstringdata_length=len(drillstringdata)
    previousdrillstringdata=drillstringdata[drillstringdata_length-1]
    bitdetails=BhaElement.objects.filter(bhadata_id=bhadata.id,type_name="Bit").first()
    bitcumulative_len=converttofloat(previousdrillstringdata['MD'])+converttofloat(bitdetails.length)
    calculatedpressureloss=previousdrillstringdata['calculated_pressureloss']+bitloss
    
    drillstringdata.append({"length":converttofloat(bitdetails.length),"MD":bitcumulative_len,"pressureloss":bitloss,"calculated_pressureloss":calculatedpressureloss,'loss_alongwell':previousdrillstringdata['loss_alongwell']-bitloss})
    
    drillstringdata_length=len(drillstringdata)
    previousdata=drillstringdata[drillstringdata_length-1]
    bitcumulative_len=converttofloat(previousdata["MD"])-converttofloat(bitdetails.length)

    drillstringdata.append({"length":converttofloat(bitdetails.length),"MD":bitcumulative_len,"pressureloss":0,"calculated_pressureloss":previousdata['calculated_pressureloss'],'loss_alongwell':previousdata['loss_alongwell']})

    for annular in reversed(annular_pressure_loss['allpressureloss']):
        drillstringdata_length=len(drillstringdata)
        previousdrillstringdata=drillstringdata[drillstringdata_length-1]
        calculatedpressureloss=previousdrillstringdata['calculated_pressureloss']+annular["pressureloss"]
        annularcumulativelength=previousdrillstringdata["MD"]-annular["length_against"]
        drillstringdata.append({"length":annular["length_against"],"MD":annularcumulativelength,"pressureloss":annular["pressureloss"],"calculated_pressureloss":calculatedpressureloss,'loss_alongwell':round(previousdrillstringdata['loss_alongwell'],2)-annular["pressureloss"]})
        
    for alldata in drillstringdata:
        pressurelosschartdata.append({"x":round(alldata["loss_alongwell"]),"y":alldata["MD"]})
    

    return pressurelosschartdata

def calculate_annular_drillstring_loss(request):
    data = request.body
    json_data = json.loads(data)
    well_id=request.session['well_id']
    given_bitdepth=json_data.get('bitdepth')
    wellphase_id=json_data.get('wellphase_id')
    section_name=json_data.get('section_name')
    rpm=json_data.get('rpm')

    torque=json_data.get('torque') if 'torque' in json_data else ""
    wob=json_data.get('wob') if 'wob' in json_data else ""
    rop=json_data.get('rop')
    flowrate=int(json_data.get('flowrate'))
    muddata=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    cuttings_density=converttofloat(json_data.get('cuttings_density'))
    cuttings_size=converttofloat(json_data.get('cuttings_size'))
    sectiontodepth=muddata.todepth if(given_bitdepth=='') else int(given_bitdepth)
    bhadata=BhaData.objects.getbha(wellphase_id)
    wellphase = WellPhases.objects.getwellphase_byid(wellphase_id)
    previous_wellphase=WellPhases.objects.getprevious_wellphase(wellphase.id,well_id)
    checkliner=WellPhases.objects.checkliner(well_id,sectiontodepth)
    length_of_previous_casing_from_surface=0 if previous_wellphase==None else previous_wellphase.measured_depth
    length_of_selected_section_from_surface=sectiontodepth
    hole_size=wellphase.hole_size
    id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
    bitdepth=sectiontodepth if(given_bitdepth=='') else int(given_bitdepth)
    length_of_openhole_from_bitdepth=bitdepth-length_of_previous_casing_from_surface
    wellphasetodepth= wellphase.measured_depth
    viscocity=getviscocity(muddata)
    if(checkliner.count()>0):
        annular_pressure_loss=calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),wellphase_id,checkliner,well_id,cuttings_density,
        cuttings_size,torque,wob,rop,viscocity,'calculateallpressurelossliner')
    else:

        annular_pressure_loss=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity,'calculateallpressureloss')
    bitelement=BhaElement.objects.filter(bhadata_id=bhadata.id,type_name='Bit',status=1).first()
    type_name=bitelement.type_name
    bit_od=bitelement.od
    bit_length=bitelement.length 
    

    annular_pressure_loss['annularvelocitychartdata']= calculateannularvelocitychartnew(annular_pressure_loss['allpressureloss'],flowrate,id_of_previous_casing,hole_size,well_id)

    data = {
    'allpressureloss': annular_pressure_loss['allpressureloss'],
    'annularvelocitychartdata': annular_pressure_loss['annularvelocitychartdata'],
    'type_name':type_name,
    'bit_od':bit_od,
    'bit_length':bit_length,
    }
    input_data={
        'flowrate':flowrate,
        'rpm':rpm,
        'rop':rop
    }

    Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'annularvelocity',json.dumps(annular_pressure_loss['annularvelocitychartdata']),json.dumps(input_data))
    
    Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'annulardrillstringloss',json.dumps(annular_pressure_loss['allpressureloss']),json.dumps(input_data))
    
    return JsonResponse(data,safe=False)

def calculateannularvelocitychartnew(pressurelossdata,flowrate,id_of_previous_casing,hole_size,well_id):
    unit = getprojectunit(well_id)
    i=0
    alldata=[]
    if unit == 'API':
        holesize_convert=hole_size/12/3.281
        id_of_previous_casing_convert=id_of_previous_casing/12/3.281
        flowrate_convert=flowrate*0.000063
    else:
        holesize_convert=hole_size/1000
        id_of_previous_casing_convert=id_of_previous_casing/1000
        flowrate_convert=flowrate/3.78*0.000063
    for pressureloss in pressurelossdata:
        while i<=pressureloss['cumlativelength']:
            i +=100
            if(i<=pressureloss['cumlativelength']):
                i=i
                
                ID=odconversion(pressureloss['od'],unit)
                if(pressureloss['element_type']=="CH"):
                    av=flowrate_convert/(pi/4*(id_of_previous_casing_convert**2-ID**2))
                else:
                    av=flowrate_convert/(pi/4*(holesize_convert**2-ID**2))
                avconvert=calculate_annular(av,unit)
                alldata.append({"x":avconvert,"y":i})
            else:
                i=pressureloss['cumlativelength']
                ID=odconversion(pressureloss['od'],unit)
                if(pressureloss['element_type']=="CH"):
                    av=flowrate_convert/(pi/4*(id_of_previous_casing_convert**2-ID**2))
                else:
                    av=flowrate_convert/(pi/4*(holesize_convert**2-ID**2))
                avconvert=calculate_annular(av,unit)
                alldata.append({"x":avconvert,"y":i})
                if(i%100 != 0):
                    i=i-(i%100)
                else:
                   i=i-100 
                break
    return alldata                    

def calculate_cci_trans_cutting(request):
    slip_data = json.loads(request.GET.get('slip_data'))
    flowrate = int(request.GET.get('flowrate'))
    rop = request.GET.get('rop')
    rpm = request.GET.get('rpm')

    well_id=request.session['well_id']
    wellphase_id=request.GET.get('wellphase_id')
    section_name=request.GET.get('section_name')
    given_bitdepth=request.GET.get('bitdepth')
    muddata=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    viscocity=getviscocity(muddata)
    bhadata=BhaData.objects.getbha(wellphase_id)
    bitelement=BhaElement.objects.filter(bhadata_id=bhadata.id,type_name='Bit',status=1).first()
    sectiontodepth=muddata.todepth if(given_bitdepth=='') else int(given_bitdepth)
    print('flowratess',flowrate)
    cci=calculatecci(well_id,slip_data,viscocity,flowrate,muddata.mud_weight)
    transportratio=calculatetransportratio(well_id,slip_data,viscocity,flowrate)
    cuttingsconcentration=calculatecuttings_concentration(well_id,flowrate,rop,slip_data,bitelement,sectiontodepth)
    length_cci=len(cci)
    max_cci=cci[length_cci-1]['x']


    data = {
        'cci':cci,
        'transportratio':transportratio,
        'cuttingsconcentration':cuttingsconcentration,
        'maxcci':max_cci+1
        
    }
    input_data={
        'flowrate':flowrate,
        'rpm':rpm,
        'rop':rop
    }
    Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'cci',json.dumps(cci),json.dumps(input_data))
    Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'cuttingsconcentration',json.dumps(cuttingsconcentration),json.dumps(input_data))
    Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'transportratio',json.dumps(transportratio),json.dumps(input_data))


    return JsonResponse(data,safe=False)

def ecdbitdepth_calculation(request):
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    given_bitdepth=request.GET['bitdepth']  
    flowrate=int(request.GET['flowrate'])
    rpm=request.GET['rpm']
    rop=request.GET['rop']
    torque=request.GET.get('torque')
    wob=request.GET.get('wob')

    well_id=request.session['well_id']
    cuttings_density=converttofloat(request.GET['cuttings_density'])
    cuttings_size=converttofloat(request.GET['cuttings_size'])
    muddata=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    viscocity=getviscocity(muddata)
    sectionfromdepth=muddata.from_depth
    sectiontodepth=muddata.todepth if(given_bitdepth=='') else int(given_bitdepth)
    bhadata=BhaData.objects.getbha(wellphase_id)
    wellphase = WellPhases.objects.getwellphase_byid(wellphase_id)
    previous_wellphase=WellPhases.objects.getprevious_wellphase(wellphase.id,well_id)
    length_of_previous_casing_from_surface=0 if previous_wellphase==None else previous_wellphase.measured_depth
    hole_size=wellphase.hole_size
    id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
    length_of_selected_section_from_surface=sectiontodepth
    bitdepth=sectiontodepth if(given_bitdepth=='') else int(given_bitdepth)
    length_of_openhole_from_bitdepth=bitdepth-length_of_previous_casing_from_surface
    wellphasetodepth= wellphase.measured_depth
    previous_measured_depth=0 if previous_wellphase==None else previous_wellphase.measured_depth
    previous_true_vertical_depth=0 if previous_wellphase==None else previous_wellphase.true_vertical_depth
     
    checkliner=WellPhases.objects.checkliner(well_id,sectiontodepth)
    bhadata=BhaData.objects.getbha(wellphase_id)
    bore_pressure_loss=calculatepipe_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate)
    print('bore_loss',bore_pressure_loss)
    if(checkliner.count()>0):
        annular_pressure_loss=calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),wellphase_id,checkliner,well_id,cuttings_density,
        cuttings_size,torque,wob,rop,viscocity,'calculateallpressurelossliner')
    else:
        annular_pressure_loss=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity,'calculateallpressureloss')
    
    ecdalongwellincreased=ecdalongwellcalculation_increased(sectionfromdepth,sectiontodepth,bhadata,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,cuttings_size,rop)
    fracture_pressure = Pressure.objects.filter(well_id=well_id,status=1).values('fracture_pressure','measured_depth')
    fracture_chart=[]
    md=[]
    i=0
    while(i<len(fracture_pressure)):
        md.append(fracture_pressure[i]['measured_depth'])
        i+=1
    md_index = [n for n,k in enumerate(md) if k > previous_measured_depth]
    
    if not md_index:
        fracture_chart.append({"x":0,"y":0})
        middleValue=0
    else:
        j=0   
        while(j<len(fracture_pressure)):
            if(j>=md_index[0]):
                fracture_chart.append({"x":fracture_pressure[j]['fracture_pressure'],"y":fracture_pressure[j]['measured_depth']})
            j+=1
        fracture_max=fracture_pressure[md_index[0]]['fracture_pressure']
        fracture_min=fracture_pressure[md_index[0]-1]['fracture_pressure']
        middleValue =(fracture_max+fracture_min)/2

    ecdchartdata=ecdcalculation(wellphase.measured_depth,wellphase.true_vertical_depth,previous_measured_depth,previous_true_vertical_depth,muddata.mud_weight,annular_pressure_loss['allpressureloss'],well_id,request,'without')
    increasedecdchartdata=ecdcalculation(wellphase.measured_depth,wellphase.true_vertical_depth,previous_measured_depth,previous_true_vertical_depth,muddata.mud_weight,annular_pressure_loss['increased_pressureloss'],well_id,request,'with')
  


    bitdepth_csg_without=round(ecdchartdata[0]['x'],2)
    bitdepth_td_without=round(ecdchartdata[-1]['x'],2)

    bitdepth_csg_with=round(increasedecdchartdata[0]['x'],2)
    bitdepth_td_with=round(increasedecdchartdata[-1]['x'],2)


    data={
        'ecdchartdata':ecdchartdata,
        'previous_measured_depth':previous_measured_depth,
        'mudweight':muddata.mud_weight,
        'increasedecdchartdata':increasedecdchartdata,
        'ecd_fracturepressure':fracture_chart,
        'todepth':sectiontodepth,
        'ecdalongwellincreased':ecdalongwellincreased,
        'bitdepth_csg_without':bitdepth_csg_without,
        'bitdepth_td_without':bitdepth_td_without,
        'bitdepth_csg_with':bitdepth_csg_with,
        'bitdepth_td_with':bitdepth_td_with

    }
    bitdepthecd_data={
        'bitdepth_csg_without':bitdepth_csg_without,
        'bitdepth_td_without':bitdepth_td_without,
        'bitdepth_csg_with':bitdepth_csg_with,
        'bitdepth_td_with':bitdepth_td_with
    }
    input_data={
        'flowrate':flowrate,
        'rpm':rpm,
        'rop':rop,
        'cuttings_density':cuttings_density,
        'cuttings_size':cuttings_size
    }
    Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'bitdepthecd_data',json.dumps(bitdepthecd_data),json.dumps(input_data))

    Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'ecdbitdepth',json.dumps(ecdchartdata),json.dumps(input_data))
    return JsonResponse(data,safe=False)

def ecdalongwellcalculation_increased(sectionfromdepth,sectiontodepth,bhadata,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,cuttings_size,rop):
    unit = getprojectunit(well_id)
    apldata=[]
    ecdchartdata=[]
    viscocity=getviscocity(muddata)
    while sectionfromdepth<sectiontodepth:
        # print(f"sectionfromdepth {sectionfromdepth}")
        allcasing=0
        allopenhole=0
        casinglength=0
        openholelength=0
        totalapl=0
        sectionfromdepth +=100
        getavg_mudweight=calculate_avgmudweight(bhadata,sectionfromdepth,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,cuttings_size,rop,sectiontodepth,viscocity)
        for mudweight in getavg_mudweight:
            if(mudweight["element_type"]=='CH'):
                allcasing +=mudweight["length"]*mudweight['mudweight']
                casinglength +=mudweight["length"]
            else:
                allopenhole +=mudweight["length"]*mudweight['mudweight']
                openholelength +=mudweight["length"]

        avg_mudweight=(allcasing/casinglength+allopenhole)/openholelength if casinglength else 0

        totalapl=0
        for mudweight in getavg_mudweight:
            if(mudweight["element_type"]=='CH'):
                pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,avg_mudweight,mudweight["od"],id_of_previous_casing,mudweight["length"],'ecdalongwell')
                totalapl +=pressureloss['pressureloss']
            else:
                pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,avg_mudweight,mudweight["od"],hole_size,mudweight["length"],'ecdalongwell')
                totalapl +=pressureloss['pressureloss']
        
        apldata.append({'md':sectionfromdepth,'apl':totalapl,'mudweight':avg_mudweight})
    # print(f"apldata {apldata}")
    for data in apldata:
        tvd=gettvd(data["md"],well_id,request,sectiontodepth)
        if unit == 'API':
            ecd=data["mudweight"]+data['apl']/(0.052*tvd)
        else:
            ecd=(data["mudweight"])+data['apl']/(9.81*tvd)
        ecdchartdata.append({"x":ecd,"y":data["md"],'tvd':tvd})
        
    # print(f"ecdchartdata {ecdchartdata}")
    return ecdchartdata

def calculate_avgmudweight(bhadata,sectionfromdepth,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,cuttings_size,rop,sectiontodepth,viscocity):
    # print(muddata.mud_weight)
    bhaelement=BhaElement.objects.filter(bhadata_id=bhadata.id).exclude(type_name='Bit').order_by('-id')
    bhacount=bhaelement.count()
    i=bhacount
    previous_length_against_casing=[]
    allmudweightdata=[]

    for previousbha in bhaelement:
        if(previousbha.length_onejoint<sectionfromdepth):
            newlength=converttofloat(previousbha.length)
        else:
            belowbha=BhaElement.objects.filter(bhadata_id=bhadata.id,id__lt=previousbha.id).order_by('-id').first()
            newlength=sectionfromdepth-belowbha.length_onejoint

        od_of_pipe_element=previousbha.od
        if(i==bhacount):
            length_against_casing=length_of_previous_casing_from_surface if(converttofloat(newlength)>=length_of_previous_casing_from_surface) else newlength
            previous_length_against_casing.append(length_against_casing)
        else:
            sum_of_previous_against_casing=sum(previous_length_against_casing)
            if(sum_of_previous_against_casing==length_of_previous_casing_from_surface):
                length_against_casing=0
            if((sum_of_previous_against_casing<length_of_previous_casing_from_surface) and (sum_of_previous_against_casing+newlength<length_of_previous_casing_from_surface)):
                length_against_casing=newlength
            else:
                length_against_casing=length_of_previous_casing_from_surface-sum_of_previous_against_casing
            previous_length_against_casing.append(length_against_casing)
        length_against_open_hole=converttofloat(newlength)-length_against_casing
       
        if(length_against_casing!=0):
            slipvelocity=calculateslipvelocitywithoutliner(well_id,rpm,flowrate,muddata.mud_weight,id_of_previous_casing,previousbha.od,viscocity,cuttings_density,cuttings_size,length_against_casing)
            slipvelocitywalker= slipvelocity_walker(muddata,id_of_previous_casing,rpm,previousbha.od,cuttings_density,cuttings_size,flowrate)

            if(slipvelocity["slipvelocity"]>=slipvelocitywalker["slipvelocity"]):
                slipvelocityvalue=slipvelocity["slipvelocity"]
            else:
                slipvelocityvalue=slipvelocitywalker["slipvelocity"]
            
            increased_mudweight=calculate_increased_mudweight(well_id,flowrate,id_of_previous_casing,previousbha.od,rop,slipvelocityvalue,muddata.mud_weight,cuttings_density)
            allmudweightdata.append({'mudweight':increased_mudweight["increased_mudweight"],'length':length_against_casing,'element_type':'CH','od':od_of_pipe_element})
        
        if(length_against_open_hole!=0):
            slipvelocity=calculateslipvelocitywithoutliner(well_id,rpm,flowrate,muddata.mud_weight,hole_size,previousbha.od,viscocity,cuttings_density,cuttings_size,length_against_open_hole)
            slipvelocitywalker= slipvelocity_walker(muddata,hole_size,rpm,previousbha.od,cuttings_density,cuttings_size,flowrate)

            if(slipvelocity["slipvelocity"]>=slipvelocitywalker["slipvelocity"]):
                slipvelocityvalue=slipvelocity["slipvelocity"]
            else:
                slipvelocityvalue=slipvelocitywalker["slipvelocity"]
            
            increased_mudweight=calculate_increased_mudweight(well_id,flowrate,hole_size,previousbha.od,rop,slipvelocityvalue,muddata.mud_weight,cuttings_density)
            allmudweightdata.append({'mudweight':increased_mudweight["increased_mudweight"],'length':length_against_open_hole,'element_type':'OH','od':od_of_pipe_element})

        i -=1
    return allmudweightdata

def ecdalongwell_calculation(request):
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    given_bitdepth=request.GET['bitdepth']  
    flowrate=int(request.GET['flowrate'])
    rpm=request.GET['rpm']
    rop=request.GET['rop']

    well_id=request.session['well_id']
    cuttings_density=converttofloat(request.GET['cuttings_density'])
    cuttings_size=converttofloat(request.GET['cuttings_size'])

    muddata=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    sectionfromdepth=muddata.from_depth
    sectiontodepth=muddata.todepth if(given_bitdepth=='') else int(given_bitdepth)
    bhadata=BhaData.objects.getbha(wellphase_id)
    wellphase = WellPhases.objects.getwellphase_byid(wellphase_id)
    previous_wellphase=WellPhases.objects.getprevious_wellphase(wellphase.id,well_id)
    length_of_previous_casing_from_surface=0 if previous_wellphase==None else previous_wellphase.measured_depth
    hole_size=wellphase.hole_size
    id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
    length_of_selected_section_from_surface=sectiontodepth
    bitdepth=sectiontodepth if(given_bitdepth=='') else int(given_bitdepth)
    length_of_openhole_from_bitdepth=bitdepth-length_of_previous_casing_from_surface
    wellphasetodepth= wellphase.measured_depth
    previous_measured_depth=0 if previous_wellphase==None else previous_wellphase.measured_depth

    ecdalongwell=ecdalongwellcalculation(sectionfromdepth,sectiontodepth,bhadata,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,cuttings_size,rop)
    ecdalongwellincreased=ecdalongwellcalculation_increased(sectionfromdepth,sectiontodepth,bhadata,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,cuttings_size,rop)

    fracture_pressure = Pressure.objects.filter(well_id=well_id,status=1).values('fracture_pressure','measured_depth')
    fracture_chart=[]
    md=[]
    i=0
    while(i<len(fracture_pressure)):
        md.append(fracture_pressure[i]['measured_depth'])
        i+=1
    md_index = [n for n,k in enumerate(md) if k > previous_measured_depth] 
    if not md_index:
        fracture_chart.append({"x":0,"y":0})
        middleValue=0
    else:
        j=0   
        while(j<len(fracture_pressure)):
            if(j>=md_index[0]):
                fracture_chart.append({"x":fracture_pressure[j]['fracture_pressure'],"y":fracture_pressure[j]['measured_depth']})
            j+=1
    alongwell_td_without=round(ecdalongwell[-1]['x'],2)
    alongwell_csg_without=round(ecdalongwell[0]['x'],2)

    alongwell_csg_with=round(ecdalongwellincreased[0]['x'],2)
    alongwell_td_with=round(ecdalongwellincreased[-1]['x'],2)

    alongwellecd_data={
        'alongwell_td_without':alongwell_td_without,
        'alongwell_csg_without':alongwell_csg_without,
        'alongwell_csg_with':alongwell_csg_with,
        'alongwell_td_with':alongwell_td_with
    }



    data={
        'ecdalongwell':ecdalongwell,
        'previous_measured_depth':previous_measured_depth,
        'todepth':sectiontodepth,
        'mudweight':muddata.mud_weight,
        'ecd_fracturepressure':fracture_chart,
        'ecdalongwellincreased':ecdalongwellincreased,
        'alongwell_td_without':alongwell_td_without,
        'alongwell_csg_without':alongwell_csg_without,
        'alongwell_csg_with':alongwell_csg_with,
        'alongwell_td_with':alongwell_td_with


    }

    input_data={
        'flowrate':flowrate,
        'rpm':rpm,
        'rop':rop,
        'cuttings_density':cuttings_density,
        'cuttings_size':cuttings_size

    }
    Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'alongwellecd_data',json.dumps(alongwellecd_data),json.dumps(input_data))

    Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'ecdalongwellchartdata',json.dumps(ecdalongwell),json.dumps(input_data))

    return JsonResponse(data,safe=False)

def ecdalongwellcalculation(sectionfromdepth,sectiontodepth,bhadata,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,cuttings_size,rop):
    unit = getprojectunit(well_id)
    apldata=[]
    ecdchartdata=[]
    while sectionfromdepth<=sectiontodepth:
        annularloss=ecdannularcalculation(bhadata,sectionfromdepth,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,cuttings_size,rop,sectiontodepth)
        apldata.append({'md':annularloss['md'],'apl':annularloss['apl']})
        sectionfromdepth +=100

    # print(f"apldatanormal {apldata}")
    for data in apldata:
        tvd=gettvd(data["md"],well_id,request,sectiontodepth)
        if unit == 'API':
            ecd=muddata.mud_weight+data['apl']/(0.052*tvd)
        else:
            ecd=muddata.mud_weight+data['apl']/(9.81*tvd)
        ecdchartdata.append({"x":ecd,"y":data["md"],'tvd':tvd})

    return ecdchartdata

def ecdannularcalculation(bhadata,sectionfromdepth,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,cuttings_size,rop,sectiontodepth):
    bhaelement=BhaElement.objects.filter(bhadata_id=bhadata.id).exclude(type_name='Bit').order_by('-id')
    viscocity=getviscocity(muddata)
    bhacount=bhaelement.count()
    totalapl=0
    pressureloss=[]
    increasedpressureloss=[]

    i=bhacount
    previous_length_against_casing=[]
    cumulative_length=0
    for previousbha in bhaelement:
        if(previousbha.length_onejoint<sectionfromdepth):
            newlength=converttofloat(previousbha.length)
        else:
            belowbha=BhaElement.objects.filter(bhadata_id=bhadata.id,id__lt=previousbha.id).order_by('-id').first()
            newlength=sectionfromdepth-belowbha.length_onejoint

        od_of_pipe_element=previousbha.od
        if(i==bhacount):
            length_against_casing=length_of_previous_casing_from_surface if(converttofloat(newlength)>=length_of_previous_casing_from_surface) else newlength
            previous_length_against_casing.append(length_against_casing)
        else:
            sum_of_previous_against_casing=sum(previous_length_against_casing)
            if(sum_of_previous_against_casing==length_of_previous_casing_from_surface):
                length_against_casing=0
            if((sum_of_previous_against_casing<length_of_previous_casing_from_surface) and (sum_of_previous_against_casing+newlength<length_of_previous_casing_from_surface)):
                length_against_casing=newlength
            else:
                length_against_casing=length_of_previous_casing_from_surface-sum_of_previous_against_casing
            previous_length_against_casing.append(length_against_casing)
        length_against_open_hole=converttofloat(newlength)-length_against_casing
        
        if(length_against_casing!=0):
            pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,muddata.mud_weight,previousbha.od,id_of_previous_casing,length_against_casing,'ecdbitdepth')
            cumulative_length +=length_against_casing
            # print(f"pressureloss {pressureloss}")
            totalapl +=pressureloss['pressureloss']

        if(length_against_open_hole!=0):
            pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,muddata.mud_weight,previousbha.od,hole_size,length_against_open_hole,'ecdbitdepth')
            totalapl +=pressureloss['pressureloss']
        i -=1
    allapl={'md':sectionfromdepth,'apl':totalapl}


    return allapl

#ecd calculation
def ecdcalculation(holemd,holetvd,previousmd,previoustvd,mud_weight,annular_pressure_loss,well_id,request,typename):
    unit = getprojectunit(well_id)
    # print(f"previousmd {previousmd}")
    allecd_data=[]
    allannular_data=[]
    ecdchartdata=[]
    # print(f'annular_pressure_loss {annular_pressure_loss}')
    # print(f"holemd {holemd}")
    # totalannularloss=sum(annularloss['pressureloss'] for annularloss in annular_pressure_loss)
    # totalannularloss_withoutopenhole=sum(annularloss['pressureloss'] for annularloss in annular_pressure_loss if annularloss['element_type']!="OH")
    # casinglength=sum(annularloss['length_against'] for annularloss in annular_pressure_loss if annularloss['element_type']!="OH")
    revcum=0
    mudweightdata=[]
    alllength=[]
    cumulative_length=0
    for annular in annular_pressure_loss:
        cumulative_length +=annular['length_against']
        revcum +=annular['length_against']
        apl=annular['pressureloss']/annular['length_against']
        if(annular['length_against']<100):
            step_size=annular['length_against']
        else:
            step_size=100
        allannular_data.append({
            'length':annular['length_against'],
            'revcum':revcum,
            'apl':apl,
            'step_size':step_size
        })
        mudweightdata.append({'md':cumulative_length,'mudweight':annular['mudweight']})
        alllength.append(annular['length_against'])
   
  
    # print(f"allannular_data {allannular_data}")
    depth=0
    previous_depth=0
    startdepth=allannular_data[0]['revcum']
    todepth=holemd
    while depth<holemd:
        for annular in allannular_data:
            if(depth<=annular['revcum']):
                step_size=annular['step_size']
                break
        # print(f"step_size {step_size}")
        depth=depth+step_size
        if(depth<=startdepth):
            md=depth
        else:
            i=0
            while i<len(allannular_data)-1:
                remaining_element=(len(allannular_data)-1)-i
                if(remaining_element>1):
                    if(previous_depth<allannular_data[i]['revcum'] and (previous_depth+step_size)>allannular_data[i]['revcum']):
                        md=allannular_data[i]['revcum']
                        break
                    else:
                        if(depth>allannular_data[i]['revcum'] and depth<=allannular_data[i+1]['revcum']):
                           md=depth
                           break
                else:
                    if(previous_depth<allannular_data[i]['revcum'] and (previous_depth+step_size)>allannular_data[i]['revcum']):
                        md=allannular_data[i]['revcum']
                        break
                    else:
                        if(depth<=todepth and depth>allannular_data[i]['revcum']):
                           md=depth
                           break
                        else:
                            md=todepth
                            break
                i +=1
        previous_depth=depth

        if(md<=startdepth):
            calculatedapl=allannular_data[0]['apl']*md
        else:
            i=0
            while i<len(allannular_data)-1:
                remaining_element=(len(allannular_data)-1)-i
                if(i==0):
                    if(md>allannular_data[i]['revcum'] and md<=allannular_data[i+1]['revcum']):
                        calculatedapl=(md-allannular_data[i]['revcum'])*allannular_data[i+1]['apl']+allannular_data[i]['apl']*allannular_data[i]['revcum']
                        break
                elif(remaining_element>1):
                    if(md>allannular_data[i]['revcum'] and md<=allannular_data[i+1]['revcum']):
                        calculatedapl=(md-allannular_data[i]['revcum'])*allannular_data[i+1]['apl']
                        j=0
                        while j<=i:
                            calculatedapl=calculatedapl+allannular_data[j]['apl']*allannular_data[j]['length']
                            j +=1
                        break
                else:
                    calculatedapl=(md-allannular_data[i]['revcum'])*allannular_data[i+1]['apl']
                    j=0
                    while j<=i:
                        calculatedapl=calculatedapl+allannular_data[j]['apl']*allannular_data[j]['length']
                        j +=1
                    break
 
                
                i +=1
        allecd_data.append({'depth':depth,'md':md,'apl':calculatedapl})
    # print(f"allecd_data {allecd_data}")
    # print(f"mudweightdata {mudweightdata}")
    for data in allecd_data:
        if(data["md"]>=previousmd):
            tvd=gettvd(data["md"],well_id,request,holemd)
            mudweight=0
            for mud in mudweightdata:
                if(data["md"]<=mud['md']):
                    mudweight=mud['mudweight']
                    break
            if(mudweight!=0):
                ecd=calcualte_ecd(mudweight,data['apl'],tvd,unit)
                ecdchartdata.append({"x":ecd,"y":data["md"]})
    # print(f"ecdchartdata {ecdchartdata}")
    return ecdchartdata

def getallbingham(request):
    rpm=request.GET['rpm']
    flowrate=int(request.GET['flowrate'])
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    well_id=request.session['well_id']
    torque=request.GET['torque'] if 'torque' in request.GET else ""
    wob=request.GET['wob'] if 'wob' in request.GET else ""
    rop=request.GET['rop']
    muddata=MudData.objects.filter(well_phase_id=wellphase_id,section=section_name).first()
    sectionname=muddata.section
    rheogramsections=RheogramSections.objects.filter(section_name=sectionname).first()
    sections=Sections.objects.filter(section_name=sectionname).first()
    bhadata=BhaData.objects.filter(well_phases_id=wellphase_id,status=1).first()
    wellphase = WellPhases.objects.getwellphase_byid(wellphase_id)
    previous_wellphase=WellPhases.objects.filter(id__lt=wellphase.id,well_id=well_id).order_by('-id').first()
    length_of_previous_casing_from_surface=previous_wellphase.measured_depth
    wellphasefromdepth=0 if previous_wellphase==None else previous_wellphase.measured_depth
    wellphasetodepth= wellphase.measured_depth
    cuttings_density=21
    cuttings_size=0.25
    sectionfromdepth=muddata.from_depth
    sectiontodepth=muddata.todepth
    bitdepth=sectiontodepth
    length_of_openhole_from_bitdepth=bitdepth-length_of_previous_casing_from_surface
    length_of_selected_section_from_surface=sectiontodepth
    hole_size=wellphase.hole_size
    id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
    selected_viscocity=getviscocity(muddata)

    # print(f"selected_viscocity {selected_viscocity}")

    checkliner=WellPhases.objects.filter(Q(casing_type_id=7) | Q(casing_type_id=8) | Q(casing_type_id=11) | Q(casing_type_id=12)).filter(well_id=well_id,status=1,measured_depth__lt=sectiontodepth)
    if(checkliner.count()>0):
        alldata=display_bingham_liner(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,checkliner)
    else:
        alldata=display_bingham(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop)
    print('alldata',alldata)
    alldata_dict = {
    'data': alldata,
    'bitdepth':bitdepth,
    }


    return JsonResponse(alldata_dict, safe=False)
    
def getallpowerlaw(request):
    rpm=request.GET['rpm']
    flowrate=int(request.GET['flowrate'])
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    well_id=request.session['well_id']
    torque=request.GET['torque'] if 'torque' in request.GET else ""
    wob=request.GET['wob'] if 'wob' in request.GET else ""
    rop=request.GET['rop']
    muddata=MudData.objects.filter(well_phase_id=wellphase_id,section=section_name).first()
    sectionname=muddata.section
    rheogramsections=RheogramSections.objects.filter(section_name=sectionname).first()
    sections=Sections.objects.filter(section_name=sectionname).first()
    bhadata=BhaData.objects.filter(well_phases_id=wellphase_id,status=1).first()
    wellphase = WellPhases.objects.getwellphase_byid(wellphase_id)
    previous_wellphase=WellPhases.objects.filter(id__lt=wellphase.id,well_id=well_id).order_by('-id').first()
    length_of_previous_casing_from_surface=previous_wellphase.measured_depth
    wellphasefromdepth=0 if previous_wellphase==None else previous_wellphase.measured_depth
    wellphasetodepth= wellphase.measured_depth
    cuttings_density=21
    cuttings_size=0.25
    sectionfromdepth=muddata.from_depth
    sectiontodepth=muddata.todepth
    bitdepth=sectiontodepth
    length_of_openhole_from_bitdepth=bitdepth-length_of_previous_casing_from_surface
    length_of_selected_section_from_surface=sectiontodepth
    hole_size=wellphase.hole_size
    id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
    selected_viscocity=getviscocity(muddata)

    # print(f"selected_viscocity {selected_viscocity}")

    checkliner=WellPhases.objects.filter(Q(casing_type_id=7) | Q(casing_type_id=8) | Q(casing_type_id=11) | Q(casing_type_id=12)).filter(well_id=well_id,status=1,measured_depth__lt=sectiontodepth)
    if(checkliner.count()>0):
        alldata=display_powerlaw_liner(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,checkliner)
    else:
        alldata=display_powerlaw(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop)
    
    
    print('alldata',alldata)
    alldata_dict = {
    'data': alldata,
    'bitdepth':bitdepth,
    }


    return JsonResponse(alldata_dict, safe=False)


def display_bingham(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop):
    data={}
    bit_losses=getbitpressureloss(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,
    well_id)

    if(selected_viscocity['selected_modal']=="2"):
        selected_text='Bingham Plastic' 

    viscocity_bingham=calculate_viscocity_bingham(rheogramsections,sections,muddata)
    viscocity_bingham['selected_modal']="2"
    
    bingham_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_bingham,'displayallmodels') 


    bingham_annular_pressure_loss=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity_bingham,'displayallmodels')


    allbingham_pressureloss=gettotalresult(bingham_annular_pressure_loss,bingham_surface_losses)


    allbinghampressureloss=round(allbingham_pressureloss['totalpressure_loss']+bit_losses[0]['bit_pressure_loss'])

    data = {
        'bingham_surface_losses':bingham_surface_losses,
        'bingham_annular_pressure_loss':bingham_annular_pressure_loss,
        'allbingham_pressureloss':allbinghampressureloss,
        'allbingham':allbingham_pressureloss,

    }
    
    return data

#calculate viscocity and yield point for bingham plastic modal
def calculate_viscocity_bingham(rheogramsections,sections,muddata):
    well_id =muddata.well_id
    unit = getprojectunit(well_id)
    if(muddata.plastic_viscosity!=None and muddata.yield_point!=None):
        viscocity=muddata.plastic_viscosity
        yieldpoint=muddata.yield_point
        displaypv=muddata.plastic_viscosity
        displayyp=muddata.yield_point
        selected_model='2'
    else:
        if(muddata.well.well_type == 'PLAN'):
            rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=None)
            selected_model=sections.selected_model
        else:
            rheogram=Rheogram.objects.filter(rheogram_date_id=rheogramsections[0].id,status=1,modelname=None)
            selected_model='2'
        rpm=[]
        dial=[]
        for rheogramdata in rheogram:
            if rheogramdata.dial!='':
                rpm.append(rheogramdata.rpm)
                dial.append(float(rheogramdata.dial))
                if(rheogramdata.rpm==300):
                    dial300=float(rheogramdata.dial)
                if(rheogramdata.rpm==600):
                    dial600=float(rheogramdata.dial) 
        X=np.array(rpm).reshape(-1,1)
        Y=np.array(dial).reshape(-1,1)
        BP=LinearRegression()
        BP.fit(X,Y)
        yieldpoint=BP.intercept_[0]
        pv=BP.coef_[0]
        viscocity=np.around(pv,decimals=2).tolist()[0]
        viscocity=viscocity*1.066*0.4788*1000
        displaypv=dial600-dial300
        displayyp=dial300-displaypv
    data={
        'plastic_viscosity':viscocity,
        'sectionname':muddata.section,
        # 'selected_modal':sections.selected_model,
        'selected_modal':selected_model,
        'yieldpoint':yieldpoint,
        'displaypv':displaypv,
        'displayyp':displayyp
    }
    return data


#pressure loss calculation for bingham plastic modal
def calculate_bingham_pressureloss(unit,rpm,flowrate,mudweight,identity,length,viscocity,yieldpoint):

    flowrate_si=convertflowrate(flowrate,unit)
    mudweight_si=mudweight_conversion(mudweight,unit)
    identity_si=odconversion(float(identity),unit)
    length_si=odconversion(float(length),unit)

    average_velocity=flowrate_si/(pi/4*identity_si**2)*3.281
    headstrom_number=37000*(identity_si*12*3.281)**2*yieldpoint*(mudweight_si*8.33/1000)/viscocity**2
    Re=927*(identity_si*12*3.281)*average_velocity*(mudweight_si*8.33/1000)/viscocity
    Re_L=1000*(1+sqrt(1+headstrom_number/3000))
    Re_U=2000*(1+sqrt(1+headstrom_number/6000))
    def b_o(b):
        return 3*b**4-4*(1+6*Re/headstrom_number)*b**3+1
    
    def b_oprime(b):
        return 12*b**3-12*(1+6*Re/headstrom_number)*b**2

    if(headstrom_number<=10**5):
        if(Re<=Re_L):
            bo=root_scalar(b_o,x0=100,bracket=[1,10000],fprime=b_oprime,method='newton').root
            tw=0.4788*bo*yieldpoint
            dP=4*tw*length_si/(identity_si)
        if Re>Re_L:
            a=0.0786
            b=0.25
            f=a/Re**b
            dP=2*f*mudweight_si*(average_velocity/3.281)**2*length_si/identity_si
    else:
        if(Re<=Re_U):
            bo=root_scalar(b_o,x0=100,bracket=[1,10000],fprime=b_oprime,method='newton').root
            tw=0.4788*bo*yieldpoint
            dP=4*tw*length_si/(identity_si)
        if Re>Re_U:
            a=0.0786
            b=0.25
            f=a/Re**b
            dP=2*f*mudweight_si*(average_velocity/3.281)**2*length_si/identity_si
    
    pressureloss=pressureloss_conversion(dP,unit)
    
    data={
        'viscocity_si':viscocity,
        'flowrate_si':flowrate_si,
        'mudweight_si':mudweight_si,
        'ID':identity_si,
        'length':length_si,
        'velocity':0,
        'Re': Re,
        'flowregime':"",
        'f':"",
        'pressureloss':pressureloss,
        'dP':"",
        'flowrate':flowrate,
        'mudweight':mudweight,
        'identity':identity,
        'originallength':length,
        'originalviscocity':viscocity
    }
    return data


def calculate_bingham_annular(viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,typename,unit):
    # print(f"casing_hole_size {casing_hole_size}")
    yield_point=yieldpoint_conversion(viscocity['yieldpoint'],unit)
    viscocity=viscosity_conversion(viscocity['plastic_viscosity'],unit)
    mudweight_si=mudweight_conversion(mud_weight,unit)
    length_si=length_conversion(length,unit)
    flowrate_si=convertflowrate(flowrate,unit)
    casing_hole_size_si = convertcasing_hole_size(casing_hole_size,unit)
    od_of_pipe_element_si = odconversion(float(od_of_pipe_element),unit)
    rpm_si = rpm_convert(int(rpm))
   

    U = flowrate_si/(pi/4*(casing_hole_size_si**2-od_of_pipe_element_si**2))
    axial_shear_rate = 8*U/(2/3*(casing_hole_size_si-od_of_pipe_element_si))
    radial_shear_rate = rpm_si*od_of_pipe_element_si/(casing_hole_size_si-od_of_pipe_element_si)
    total_shear_rate = sqrt(axial_shear_rate**2+radial_shear_rate**2)

    Ts = yield_point*0.4788+viscocity/1000*total_shear_rate
    Eo = yield_point*0.4788/Ts
    He = 24900*(mudweight_si/1000*8.33)*yield_point*((casing_hole_size_si-od_of_pipe_element_si)*3.281*12)**2/viscocity**2 

    def E(a):
        return He/22400-(a/(1-a)**3)
    Eoc = fsolve(E,0)
  
    Rec = sqrt(2/3)*He*(1-3/2*Eoc+0.5*Eoc**3)/(8*Eoc)

    De = casing_hole_size_si*(1+(od_of_pipe_element_si/casing_hole_size_si)**2-((1-(od_of_pipe_element_si/casing_hole_size_si)**2)/(log(casing_hole_size_si/od_of_pipe_element_si))))**0.5
    Re = De*U*mudweight_si/(viscocity/1000)

    if Re<=Rec:
        flowregime="Laminar"
        dP=4*Ts/De*length_si
    else:
        flowregime="Turbulent"
        a=0.0786
        b=0.25
        f=a/Re**b
        dP=2*f*mudweight_si*(U)**2*length_si/(casing_hole_size_si-od_of_pipe_element_si)
    
    pressureloss = pressureloss_conversion(dP,unit)

    data={
        'pressureloss':pressureloss,
        'flowregime':flowregime

    }
    return data


def calculate_slipvelocity_bingham(unit,rpm,flowrate,mud_weight,cased_hole_size,od,viscocity,cuttings_density,cuttings_size):
    
    cased_hole_size = calculate_holesize(cased_hole_size,unit)
    od = calculate_od(converttofloat(od),unit)
    mud_weight = calculate_mudweight(mud_weight,unit)
    flowrate = calculate_flowrate(flowrate,unit)
    cuttings_density = calculate_cutting_density(cuttings_density,unit)
    cuttings_size = calculate_cutting_size(cuttings_size,unit)

    annular_velocity=24.51*flowrate/(cased_hole_size**2-converttofloat(od)**2)
    apparent_velocity=viscocity["plastic_viscosity"]
    turbulent_vs=9.24*sqrt(cuttings_size*(cuttings_density-mud_weight)/mud_weight)
    turbulent_nRe=15.47*mud_weight*cuttings_size*turbulent_vs/apparent_velocity
    
    stoke_vs=4972*cuttings_size**2/apparent_velocity*(cuttings_density-mud_weight)
    stoke_nRe=15.47*mud_weight*cuttings_size*stoke_vs/apparent_velocity

    transitional_vs=174*cuttings_size*(cuttings_density-mud_weight)**0.667/(mud_weight**0.333*apparent_velocity**0.333)
    transitional_nRe=15.47*mud_weight*cuttings_size*transitional_vs/apparent_velocity

    if(turbulent_nRe>2000):
        slip_velocity=turbulent_vs
    else:
        if(stoke_nRe<=1):
            slip_velocity=stoke_vs
        else:
            slip_velocity=transitional_vs
    
    slip_velocity = slipvelocity_conversion(slip_velocity,unit)

    data={
        'slip_velocity':slip_velocity,
        'annular_velocity':annular_velocity
    }
    return data


def display_powerlaw(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop):
    data={}
    bit_losses=getbitpressureloss(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,
    well_id)

    if(selected_viscocity['selected_modal']=="3"):
        selected_text='Powerlaw' 

    viscocity_powerlaw= calculate_viscocity_powerlaw(rheogramsections,sections,muddata)
    viscocity_powerlaw['selected_modal']="3"

    powerlaw_annular_pressure_loss=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity_powerlaw,'displayallmodels')
   
    powerlaw_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_powerlaw,'displayallmodels')

    allpowerlaw_pressureloss=gettotalresult(powerlaw_annular_pressure_loss,powerlaw_surface_losses)
    allpowerlawpressureloss=round(allpowerlaw_pressureloss['totalpressure_loss']+bit_losses[0]['bit_pressure_loss'])
    
    data = {
        'powerlaw_annular_pressure_loss':powerlaw_annular_pressure_loss,
        'powerlaw_surface_losses':powerlaw_surface_losses,
        'allpowerlaw_pressureloss':allpowerlawpressureloss,
        'allpowerlaw':allpowerlaw_pressureloss
    }
    return data

def sensitivity_calculation(request):
    rpm=request.GET['rpm']
    flowrate=int(request.GET['flowrate'])
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    calculation_type=request.GET['type']
    plastic_viscocity=float(request.GET['plastic_viscocity'])
    yp=request.GET['yp'] if 'yp' in request.GET else ""
    if(yp):
        yp=float(yp)
    else:
       yp=''
    changedtype=request.GET['changedtype']
    well_id=request.session['well_id']
    torque=request.GET['torque'] if 'torque' in request.GET else ""
    wob=request.GET['wob'] if 'wob' in request.GET else ""
    rop=request.GET['rop']
    givenbitdepth=request.GET['bitdepth']
    cuttings_density=converttofloat(request.GET['cuttings_density'])
    cuttings_size=converttofloat(request.GET['cuttings_size'])
    wellphase = WellPhases.objects.filter(id=wellphase_id).first()
    previous_wellphase=WellPhases.objects.filter(id__lt=wellphase.id,well_id=well_id).order_by('-id').first()
    muddata=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    sectionfromdepth=muddata.from_depth
    sectiontodepth=muddata.todepth if(givenbitdepth=='') else float(givenbitdepth)
    if(sectiontodepth>muddata.todepth):
        sectiontodepth=muddata.todepth
    bhadata=BhaData.objects.filter(well_phases_id=wellphase_id,status=1).first()
    length_of_previous_casing_from_surface=previous_wellphase.measured_depth
    data={}
    length_of_selected_section_from_surface=sectiontodepth

    hole_size=wellphase.hole_size
    id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
    bitdepth=sectiontodepth if(givenbitdepth=='') else float(givenbitdepth)
    if(bitdepth>muddata.todepth):
        bitdepth=muddata.todepth
    mudweight=float(request.GET['mudweight']) if request.GET['mudweight'] != ''  else muddata.mud_weight
    length_of_openhole_from_bitdepth=bitdepth-length_of_previous_casing_from_surface

    wellphasetodepth= wellphase.measured_depth
    if(changedtype == 'nochange'):
        viscocity=getviscocity(muddata)
    else:
        viscocity=getviscocity_sensitivity(muddata,plastic_viscocity,yp,well_id)
    if(changedtype=='pvchanged'):
       viscocity['plastic_viscosity']= plastic_viscocity    
    tvd=gettvd(sectiontodepth,well_id,request,sectiontodepth)
    print(f'viscocity {viscocity}')
    rheogramsections=RheogramSections.objects.filter(section_name=section_name).first()
    if(muddata.plastic_viscosity==None and muddata.yield_point==None and muddata.low_shear_rate==None):
        t300=rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=None,rpm=300).first()
        t600=rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=None,rpm=600).first()
        t3=rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=None,rpm=3).first()
        t6=rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=None,rpm=6).first()
    else:
        section_details=Sections.objects.filter(section_name=muddata.section).first()
        # print(f"section_details {section_details.selected_model}")
        if(section_details.selected_model=="1"):
            model_name='newtonian'
        elif(section_details.selected_model=="2"):
            model_name='bingham'
        elif(section_details.selected_model=="3"):
            model_name='powerlaw'
        else:
            model_name='hershel'
        t300=rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=model_name,rpm=300).first()
        t600=rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=model_name,rpm=600).first()
        t3=rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=model_name,rpm=3).first()
        t6=rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=model_name,rpm=6).first()


    input_data={
        'flowrate':flowrate,
        'rpm':rpm,
        'rop':rop
    }

    # print(f"calculation_type {calculation_type}")
    if(calculation_type == 'flowrate_pressure'):
        # print(f"changedtype {changedtype}")
        result=calculate_flowrate_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request,tvd)
        Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'flowrate_pressure',json.dumps(result['totalpressureloss']),json.dumps(input_data)) 
        Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'flowrate_ecd',json.dumps(result['ecd_without']),json.dumps(input_data))
        print('result_flowrate_pressure_AK',result)
    elif(calculation_type == 'mudweight_pressure'):
        result=calculate_mudweight_change(request,bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,tvd,sectionfromdepth)
        Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'mudweight_pressure',json.dumps(result['totalpressureloss']),json.dumps(input_data))
        Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'mudweight_ecd',json.dumps(result['ecd_without']),json.dumps(input_data))
    elif(calculation_type == 'tfa_pressure'):
        result=calculate_tfa_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request)
        Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'tfa_pressure',json.dumps(result['totalpressureloss']),json.dumps(input_data))
        Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'tfa_ecd',json.dumps(result['totalpressureloss']),json.dumps(input_data))
    elif(calculation_type == 'viscocity_pressure'):
        result=calculate_viscocity_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,t300,t600,t3,t6,tvd)
        Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'viscocity_pressure',json.dumps(result['totalpressureloss']),json.dumps(input_data)) 
        Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'viscocity_ecd',json.dumps(result['ecd_without']),json.dumps(input_data))
        
    elif(calculation_type == 'yieldpoint_pressure'):
        result=calculate_yieldpoint_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase)
        Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'yieldpoint_pressure',json.dumps(result['totalpressureloss']),json.dumps(input_data))

    elif(calculation_type == 'rop_ecd'):
        result=calculate_rop_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request,tvd,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth)
        Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'rop_ecd',json.dumps({'ecd_without': result['ecd_without'], 'ecd_with': result['ecd_with']}),json.dumps(input_data))
        print('rop_ecd_data',result)
    elif(calculation_type == 'cd_ecd'):
        result=calculate_cuttings_density(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request,tvd,rop,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth)
        Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'cuttings_density_ecd',json.dumps({'ecd_without': result['ecd_without'], 'ecd_with': result['ecd_with']}),json.dumps(input_data))
        print('cd_ecd_data',result)
    elif(calculation_type == 'cs_ecd'):
        result=calculate_cuttings_size(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request,tvd,rop,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth)
        Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'cuttings_size_ecd',json.dumps({'ecd_without': result['ecd_without'], 'ecd_with': result['ecd_with']}),json.dumps(input_data))
        print('cs_ecd_data',result)


    data['result']=result['totalpressureloss'] if 'totalpressureloss' in result else ""
    data['ecd_without']=result['ecd_without'] if 'ecd_without' in result else ""
    data['ecd_with']=result['ecd_with'] if 'ecd_with' in result else ""
    data['bit_pressure_chart']=result['bit_pressure_chart'] if 'bit_pressure_chart' in result else ""
    data['allmud_weight']=result['allmud_weight'] if 'allmud_weight' in result else ""

    
    return JsonResponse(data,safe=False)


def getviscocity_sensitivity(muddata,plastic_viscosity,yp,well_id):
    sectionname=muddata.section
    well_phase_id = muddata.well_phase_id
    rheogramsections=RheogramSections.objects.filter(section_name=sectionname,status=1).first()
    sections=Sections.objects.filter(section_name=sectionname,well_phase_id=well_phase_id,status=1).first()
    unit = getprojectunit(well_id)

    if(sections.selected_model=="4"):
        if unit == 'API':
            lsryp=muddata.low_shear_rate
        else:
            lsryp=muddata.low_shear_rate/0.4788
        t300=plastic_viscosity+yp
        t600=t300+plastic_viscosity
        m=3.32*log10((t600-lsryp)/(t300-lsryp))
        k_hb=(t300-lsryp)/pow(511,m)
        K=k_hb
        n=m
    elif(sections.selected_model=="1"):
        K=''
        n=''
    elif(sections.selected_model=="2"):
        K=''
        n=''
    elif(sections.selected_model=="3"):
        t300=plastic_viscosity+yp
        t600=t300+plastic_viscosity
        n=3.32*log10(t600/t300)
        k_pl=t300/pow(511,n)
        K=k_pl
   
    data={
        'K':K,
        'n':n,
        'plastic_viscosity':plastic_viscosity,
        'yieldpoint':yp,
        'selected_modal':sections.selected_model,
        'displaypv':plastic_viscosity,
        'displayyp':yp
    }
    return data

def calculate_flowrate_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request,tvd):
    print('well_id',well_id)
    unit = getprojectunit(well_id)

    # print(f"mud_weight {mud_weight}")
    allannularloss=[]
    alldrillstringloss=[]
    allbitloss=[]
    allsurfaceloss=[]
    totalpressureloss=[]
    allflowrate=[]
    flowrate_data=[]

    if not 'flowrate_range' in request.session:

        pressureoss=calculateapldrillstring_withoutanychart(bhadata,sectiontodepth,length_of_previous_casing_from_surface,muddata.mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,'flowratechange_findmaxflowrate')
        for pressure in pressureoss['allpressureloss']:
            if unit == 'API':
                flowrate=round(pressure['slipvelocityvalue']*(pressure["cased_hole_size"]**2-pressure['od']**2)/24.51)
            else:
                flowrate=round(pressure['slipvelocityvalue']*(pi/4*(pressure["cased_hole_size"]**2-pressure['od']**2))/1000)
            allflowrate.append(flowrate)
        
        checkdownhole_tools=BhaElement.objects.filter(Q(type_name='LWD') | Q(type_name='MWD') | Q(type_name='RSS') | Q(type_name='Mud Motor'),bhadata_id=bhadata.id)
        if(checkdownhole_tools.count()>0):
            for bhaelement in checkdownhole_tools:
                getspecifications=Specifications.objects.filter(bhadata_element_id=bhaelement.id).first()
                allflowrate.append(getspecifications.minimum_flowrate)
        print('flowrate_change_DD')
        minflowrate=max(allflowrate)
        mudpumpflowrate=MudPumpFlowRate.objects.filter(well_id=well_id).aggregate(Max('flowrate'))
        maxflowrate=mudpumpflowrate['flowrate__max']
        maxflowrate=maxflowrate*2
        print('flowrate_change_max_DD',maxflowrate)
        # print(f"maxflowrate {maxflowrate}")
        # print(f"minflowrate {minflowrate}")
        i=minflowrate
        while i<maxflowrate:
            flowrate_data.append(i)
            i +=50
        # print(f'flowrate_data {flowrate_data}')
        if(flowrate_data[-1]<maxflowrate):  
            flowrate_data.append(maxflowrate)
        
        request.session['flowrate_range']=flowrate_data
    else:
        flowrate_data=request.session['flowrate_range']

    flowrate_ecd=[]
    # print(f"flowrate_data {flowrate_data}")
    for flowratedata in flowrate_data:
        # print(f"flowratedata {flowratedata}")
        pressureoss=calculateapldrillstring_withoutanychart(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowratedata,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,'flowratechange')
        bit_losses=getbitpressureloss(rpm,flowratedata,wellphase_id,section_name,mud_weight,wellphase,previous_wellphase,
        well_id)
        surface_losses=getsurfacelosses(rpm,flowratedata,wellphase_id,section_name,mud_weight,wellphase,previous_wellphase,well_id,viscocity,'flowratechange')
        totalsurfaceloss=0
        for suface in surface_losses:
            totalsurfaceloss +=suface['pressureloss']
        totalpressure=pressureoss['totalannular_pressureloss']+pressureoss['totaldrillstring_loss']+bit_losses[0]['bit_pressure_loss']+totalsurfaceloss
        # print(f"totalpressure {totalpressure}")
        allannularloss.append({'x':flowratedata,'y':round(pressureoss['totalannular_pressureloss'])})
        alldrillstringloss.append({"x":flowratedata,'y':round(pressureoss['totaldrillstring_loss'])})
        allbitloss.append({'x':flowratedata,'y':round(bit_losses[0]['bit_pressure_loss'])})
        allsurfaceloss.append({'x':flowratedata,'y':round(totalsurfaceloss)})
        totalpressureloss.append({'x':flowratedata,'y':round(totalpressure)}) 
        ecd=calcualte_ecd(mud_weight,pressureoss['totalannular_pressureloss'],tvd,unit)
        flowrate_ecd.append({"x":flowratedata,"y":round(ecd,2) })

        
    # print(f"flowrate_ecd {flowrate_ecd}")
    data={
        'allannularloss':allannularloss,
        'alldrillstringloss':alldrillstringloss,
        'allbitloss':allbitloss,
        'allsurfaceloss':allsurfaceloss,
        'totalpressureloss':totalpressureloss,
        'ecd_without':flowrate_ecd

    }
    return data


def calculateapldrillstring_withoutanychart(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,typename,rop=''):
    # print(f"typename {typename}")
    # if(typename=='viscocitychange'):
    #     print(f"viscocity {viscocity}")
    previousbhaelement=BhaElement.objects.filter(bhadata_id=bhadata.id,status=1).exclude(type_name='Bit').order_by('-id')
    well_id = bhadata.well_id
    bhacount=previousbhaelement.count()
    i=bhacount
    totalannular_pressureloss=0
    totalincreasedannular_pressureloss=0
    totaldrillstring_loss=0
    allpressureloss=[]
    increased_pressureloss=[]
    previous_length_against_casing=[]
    print('calculate_MUD_DATA_BEFORECHANGE')
    for previousbha in previousbhaelement:
        print(f"typename {previousbha.type_name}")
        if(previousbha.length_onejoint<sectiontodepth):
            newlength=converttofloat(previousbha.length)
        else:
            belowbha=BhaElement.objects.filter(bhadata_id=bhadata.id,id__lt=previousbha.id).order_by('-id').first()
            newlength=sectiontodepth-belowbha.length_onejoint
        od_of_pipe_element=previousbha.od
        if(i==bhacount):
            length_against_casing=length_of_previous_casing_from_surface if(converttofloat(newlength)>=length_of_previous_casing_from_surface) else newlength
            previous_length_against_casing.append(length_against_casing)
        else:
            sum_of_previous_against_casing=Sum = sum(previous_length_against_casing)
            if(sum_of_previous_against_casing==length_of_previous_casing_from_surface):
                length_against_casing=0
            if((sum_of_previous_against_casing<length_of_previous_casing_from_surface) and (sum_of_previous_against_casing+newlength<length_of_previous_casing_from_surface)):
                length_against_casing=newlength
            else:
                length_against_casing=length_of_previous_casing_from_surface-sum_of_previous_against_casing
            previous_length_against_casing.append(length_against_casing)
        length_against_open_hole=converttofloat(newlength)-length_against_casing
        # print(f"length_against_open_hole {length_against_open_hole}")
        # print(f"length_against_casing {length_against_casing}")

        if(length_against_casing!=0):
            pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,previousbha.od,id_of_previous_casing,length_against_casing,typename)
            # if(typename=='viscocitychange'):
            #     print(f"pressurelosscasing {pressureloss}")
            
            if((previousbha.type_name=='RSS') or (previousbha.type_name=='MWD') or (previousbha.type_name=='LWD') or (previousbha.type_name=='Others') or (previousbha.type_name=='Mud Motor')):
                drillstringpressureloss=calculate_drillstringloss_downholetools(previousbha,flowrate,mud_weight,torque,wob)
            else:
                drillstringpressureloss=calculatepressloss(well_id,rpm,flowrate,mud_weight,previousbha.identity,length_against_casing,viscocity,'viscocitychange')

            slipvelocity=calculateslipvelocitywithoutliner(well_id,rpm,flowrate,mud_weight,id_of_previous_casing,previousbha.od,viscocity,cuttings_density,cuttings_size,length_against_casing)
            
            slipvelocitywalker= slipvelocity_walker(muddata,id_of_previous_casing,rpm,previousbha.od,cuttings_density,cuttings_size,flowrate)

            if(slipvelocity["slipvelocity"]>=slipvelocitywalker["slipvelocity"]):
                slipvelocityvalue=slipvelocity["slipvelocity"]
            else:
                slipvelocityvalue=slipvelocitywalker["slipvelocity"]

        
            if((previousbha.type_name=='Drill Pipe') or (previousbha.type_name=='Heavy Weight Drill Pipe')):
                calculate_tj_pressureloss=calculatetjpressureloss(previousbha.length,length_against_casing,previousbha,rpm,flowrate,viscocity,mud_weight,id_of_previous_casing,'without')
            else:
                calculate_tj_pressureloss=calculatetjpressure(previousbha.length,length_against_casing,previousbha,rpm,flowrate,viscocity,muddata.mud_weight,id_of_previous_casing,'without')

            allpressureloss.append({
                'flowregime' : pressureloss["flowregime"],
                'od':round(converttofloat(od_of_pipe_element),2),
                'id':round(converttofloat(previousbha.identity),2),
                'type':previousbha.type_name,
                'length_against':length_against_casing,
                'pressureloss':round(pressureloss["pressureloss"]+calculate_tj_pressureloss["tjannularloss"],2),
                'element_type':'CH',
                'drillstringloss':round(drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"],2)  if 'pressureloss' in drillstringpressureloss else drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"],
                'mudweight':mud_weight,
                'slipvelocityvalue':slipvelocityvalue,
                'cased_hole_size':id_of_previous_casing

            })
            totalannular_pressureloss +=pressureloss["pressureloss"]+calculate_tj_pressureloss["tjannularloss"]
            if 'pressureloss' in drillstringpressureloss:
                totaldrillstring_loss += drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"]
            else:
                totaldrillstring_loss +=drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"]

        if(length_against_open_hole!=0):
            pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,previousbha.od,hole_size,length_against_open_hole,'annularpressurelosscheck') 
            # print(f"pressurelossopenhole {pressureloss}")

            if((previousbha.type_name=='RSS') or (previousbha.type_name=='MWD') or (previousbha.type_name=='LWD') or (previousbha.type_name=='Others') or (previousbha.type_name=='Mud Motor')):
                drillstringpressureloss=calculate_drillstringloss_downholetools(previousbha,flowrate,mud_weight,torque,wob)
                # print(f"drillstringpressureloss {drillstringpressureloss}")
            else:
                drillstringpressureloss=calculatepressloss(well_id,rpm,flowrate,mud_weight,previousbha.identity,length_against_open_hole,viscocity,'calculateapldrillstring_withoutanychart')

            slipvelocity=calculateslipvelocitywithoutliner(well_id,rpm,flowrate,mud_weight,hole_size,previousbha.od,viscocity,cuttings_density,cuttings_size,length_against_open_hole)
            
            slipvelocitywalker= slipvelocity_walker(muddata,hole_size,rpm,previousbha.od,cuttings_density,cuttings_size,flowrate)

            if(slipvelocity["slipvelocity"]>=slipvelocitywalker["slipvelocity"]):
                slipvelocityvalue=slipvelocity["slipvelocity"]
            else:
                slipvelocityvalue=slipvelocitywalker["slipvelocity"]

            
            if((previousbha.type_name=='Drill Pipe') or (previousbha.type_name=='Heavy Weight Drill Pipe')):
                calculate_tj_pressureloss=calculatetjpressureloss(previousbha.length,length_against_open_hole,previousbha,rpm,flowrate,viscocity,mud_weight,hole_size,'without')
            else:
                calculate_tj_pressureloss=calculatetjpressure(previousbha.length,length_against_casing,previousbha,rpm,flowrate,viscocity,muddata.mud_weight,id_of_previous_casing,'without')

            allpressureloss.append({
                'flowregime' : pressureloss["flowregime"],
                'od':round(converttofloat(od_of_pipe_element),2),
                'id':round(converttofloat(previousbha.identity),2),
                'type':previousbha.type_name,
                'length_against':length_against_open_hole,
                'pressureloss':round(pressureloss["pressureloss"]+calculate_tj_pressureloss["tjannularloss"],2),
                'element_type':'OH',
                'drillstringloss':round(drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"],2)  if 'pressureloss' in drillstringpressureloss else drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"],
                'mudweight':mud_weight,
                'slipvelocityvalue':slipvelocityvalue,
                'cased_hole_size':hole_size

            })
            
            totalannular_pressureloss +=pressureloss["pressureloss"]+calculate_tj_pressureloss["tjannularloss"]
            if 'pressureloss' in drillstringpressureloss:
                totaldrillstring_loss += drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"]
            else:
                totaldrillstring_loss +=drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"]

        
        previouselement_length=previousbha.length_onejoint
        i -=1 
    print('calculate_MUD_DATA_CHANGE')
    data={
        'totaldrillstring_loss':totaldrillstring_loss,
        'totalannular_pressureloss':totalannular_pressureloss,
        'allpressureloss':allpressureloss,
    }
    return data


def calculate_viscocity_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,t300,t600,t3,t6,tvd):
    print(f"viscocitycheck {viscocity['selected_modal']}")
    if(viscocity['selected_modal'] == '1'):
       i=1
    else: 
     i=viscocity['yieldpoint']+1
    allannularloss=[]
    alldrillstringloss=[]
    allbitloss=[]
    allsurfaceloss=[]
    totalpressureloss=[]
    original_dial=[]

    original_viscocity=int(t600.dial)-int(t300.dial)
    yield_point=int(t300.dial)-original_viscocity
    rheogramdata=RheogramDate.objects.filter(well_phase_id=wellphase_id).first()
    rheogramdial=Rheogram.objects.filter(rheogram_date_id=rheogramdata.id)
    for rheodata in rheogramdial:
        original_dial.append(int(rheodata.dial))
    unit = getprojectunit(well_id)
    # print(f"original_dial {original_dial}")
    viscocity_ecd=[]
    print('VISCOCITY_CD_BEFORE')
    while i<50:
        viscocity=reverse_calculate_muddata(i,section_name,muddata,yield_point,t3,t6,original_dial,unit)
        print(f"reverse_calculate_muddata {viscocity}")


        pressureoss=calculateapldrillstring_withoutanychart(bhadata,sectiontodepth,length_of_previous_casing_from_surface,muddata.mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,'viscocitychange')
        
        # print(f"pressureossddd {pressureoss}")

        bit_losses=getbitpressureloss(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,
        well_id)
        # print(f"bit_lossefdsfsds {bit_losses}")

        surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity,'viscocitychange')
        totalsurfaceloss=0
        for suface in surface_losses:
            totalsurfaceloss +=suface['pressureloss']
        
        totalpressure=pressureoss['totalannular_pressureloss']+pressureoss['totaldrillstring_loss']+bit_losses[0]['bit_pressure_loss']
        allannularloss.append({'x':i,'y':round(pressureoss['totalannular_pressureloss'])})
        alldrillstringloss.append({"x":i,'y':round(pressureoss['totaldrillstring_loss'])})
        allbitloss.append({'x':i,'y':round(bit_losses[0]['bit_pressure_loss'])})
        allsurfaceloss.append({'x':i,'y':round(totalsurfaceloss)})
        totalpressureloss.append({'x':i,'y':round(totalpressure)})
        # ecd=muddata.mud_weight+pressureoss['totalannular_pressureloss']/(0.052*tvd)
        ecd=calcualte_ecd(muddata.mud_weight,pressureoss['totalannular_pressureloss'],tvd,unit)
        viscocity_ecd.append({'x':i,'y':round(ecd,2)})
        i +=5
    print(f"viscocity_ecd {viscocity_ecd}")
    print('VISCOCITY_CD_AFTER')
    data={
        'allannularloss':allannularloss,
        'alldrillstringloss':alldrillstringloss,
        'allbitloss':allbitloss,
        'allsurfaceloss':allsurfaceloss,
        'totalpressureloss':totalpressureloss,
        'ecd_without':viscocity_ecd
    }
    return data
      
def reverse_calculate_muddata(plastic_viscocity,section_name,muddata,yield_point,t3,t6,original_dial,unit):
    sections=Sections.objects.filter(section_name=section_name,status=1).first()
    print(f"reverse_calculate_muddatasections {sections.selected_model}")
    rheogramsections=RheogramSections.objects.filter(section_name=section_name).first()
    if(sections.selected_model=="1"):
        data={}
        data['plastic_viscosity']=plastic_viscocity
    elif(sections.selected_model=="2"):
        data={}
        data['plastic_viscosity']=plastic_viscocity
        data['yieldpoint']=yield_point
    elif(sections.selected_model=="4"):
        data=reverse_calculate_viscocity_hershel(plastic_viscocity,yield_point,t3,t6,original_dial,unit)
    elif(sections.selected_model=="3"):
        data=reverse_calculate_viscocity_powerlaw(plastic_viscocity,yield_point,unit)
    
    data['selected_modal']=sections.selected_model
    return data

def reverse_calculate_viscocity_hershel(plastic_viscocity,yield_point,t3,t6,original_dial,unit):
    rheogram_rpm= RheogramNameModels.objects.all()
    rpm=[int(rpm.rheogram_rpm) for rpm in rheogram_rpm]
    newdial=[]

    for i in rpm:
        viscocity=(plastic_viscocity/1000*0.02088*100*i*1.703)/1.066
        newdial.append(round(viscocity,2))
    # print(f"newdial {newdial}")
    t3=original_dial[0]
    t6=original_dial[1]
    t600=newdial[-1]
    t300=newdial[-2]
    ty=2*t3-t6
    plastic_viscocity = calculate_PV(plastic_viscocity,unit)
    yield_point = calculate_YP(yield_point,unit)
    ty = calculate_Ty(ty,unit)
    t300_data=plastic_viscocity+yield_point
    t600_data=t300_data+plastic_viscocity   
    m=3.32*log10((t600_data-ty)/(t300_data-ty)) 
    K=(t300_data-ty)/pow(511,m)

    data={
        'plastic_viscosity':plastic_viscocity,
        'yieldpoint':yield_point,
        'lsryp':ty,
        'K':K,
        'n':m,  
    }
    # print(f"data {data}")

    return data


def calculate_mudweight_change(request,bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,tvd,sectionfromdepth):
    unit = getprojectunit(well_id)
    if not 'mudweight_range' in request.session:
        pressure=Pressure.objects.filter(company=request.company,well=well_id,status=1,measured_depth__lte=sectiontodepth, measured_depth__gte=sectionfromdepth).all().aggregate(Min('fracture_pressure'))
        # print(f"pressure {pressure}")
        if(pressure['fracture_pressure__min']!=None):
            min_fracture_pressure=pressure['fracture_pressure__min']
        
            getpressure=Pressure.objects.filter(company=request.company,well=well_id,status=1,measured_depth__lte=sectiontodepth, measured_depth__gte=sectionfromdepth,fracture_pressure=pressure['fracture_pressure__min']).first()
            min_depth=getpressure.measured_depth
        
            totalapl=calculateapl_withoutanychart(bhadata,min_depth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity)
            
            min_tvd=gettvd(min_depth,well_id,request,sectiontodepth)
            if unit == 'API':
                mud_weight=min_fracture_pressure-totalapl/(0.052*min_tvd)
            else:
                mud_weight=min_fracture_pressure-totalapl/(9.81*min_tvd)
            maxpore_pressure=Pressure.objects.filter(company=request.company,well=well_id,status=1,measured_depth__lte=sectiontodepth, measured_depth__gte=sectionfromdepth).all().aggregate(Max('pore_pressure'))
            
            maximum_pore_pressure=maxpore_pressure['pore_pressure__max']
            if unit == 'API':
                i=maximum_pore_pressure
                allmud_weight=[]
                while i<min_fracture_pressure:
                    allmud_weight.append(i)
                    i +=0.5
            else:
                i=maximum_pore_pressure
                allmud_weight=[]
                while i<min_fracture_pressure:
                    allmud_weight.append(i)
                    i +=0.01
            if(allmud_weight[-1]<min_fracture_pressure):
                allmud_weight.append(min_fracture_pressure)
        else:
            i=8.33
            allmud_weight=[]
            while i<15:
                allmud_weight.append(i)
                i +=0.5
            if(allmud_weight[-1]<15):
                allmud_weight.append(15)
    else:
        allmud_weight=request.session['mudweight_range']
    
    totalpressureloss=[]
    mudweight_ecd=[]
    
    for mud_weight in allmud_weight:
        pressureoss=calculateapldrillstring_withoutanychart(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,'muddatachange')
        bit_losses=getbitpressureloss(rpm,flowrate,wellphase_id,section_name,mud_weight,wellphase,previous_wellphase,
        well_id)
        surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,mud_weight,wellphase,previous_wellphase,well_id,viscocity,"mudweightchange")
        totalsurfaceloss=0
        for suface in surface_losses:
            totalsurfaceloss +=suface['pressureloss']
        totalpressure=pressureoss['totalannular_pressureloss']+pressureoss['totaldrillstring_loss']+bit_losses[0]['bit_pressure_loss']+totalsurfaceloss
        # allannularloss.append({'x':mud_weight,'y':round(pressureoss['totalannular_pressureloss'])})
        # alldrillstringloss.append({"x":mud_weight,'y':round(pressureoss['totaldrillstring_loss'])})
        # allbitloss.append({'x':mud_weight,'y':round(bit_losses[0]['bit_pressure_loss'])})
        # allsurfaceloss.append({'x':mud_weight,'y':round(totalsurfaceloss)})
        totalpressureloss.append({'x':mud_weight,'y':round(totalpressure)})
        ecd=calcualte_ecd(mud_weight,pressureoss['totalannular_pressureloss'],tvd,unit)
        mudweight_ecd.append({'x':mud_weight,'y':round(ecd,2)})
    
    data={
        'totalpressureloss':totalpressureloss,
        'ecd_without':mudweight_ecd,
        'allmud_weight':allmud_weight
    }
    return data


def calculate_rop_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request,tvd,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth):
    unit=getprojectunit(well_id)
    allrop=np.arange(10, 210, 10)
    allrop=allrop.tolist()
    rop_ecd_with_chart=[]
    rop_ecd_without_chart=[]
    for i in allrop:
        # print(f"rop {i}")
        pressureoss=calculateapldrillstring_withoutanychart(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,'ropchange',i)
        allcasing=0
        casinglength=0
        allopenhole=0
        openholelength=0
        getavg_mudweight=calculate_avgmudweight(bhadata,sectiontodepth,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,cuttings_size,i,sectiontodepth,viscocity)
        for mudweight in getavg_mudweight:
            if(mudweight["element_type"]=='CH'):
                allcasing +=mudweight["length"]*mudweight['mudweight']
                casinglength +=mudweight["length"]
            else:
                allopenhole +=mudweight["length"]*mudweight['mudweight']
                openholelength +=mudweight["length"]
        avg_mudweight=(allcasing/casinglength+allopenhole)/openholelength
        # print(f"getavg_mudweight {avg_mudweight}")

        totalapl=0
        for mudweight in getavg_mudweight:
            if(mudweight["element_type"]=='CH'):
                pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,avg_mudweight,mudweight["od"],id_of_previous_casing,mudweight["length"],'ecdalongwell')
                totalapl +=pressureloss['pressureloss']
            else:
                pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,avg_mudweight,mudweight["od"],hole_size,mudweight["length"],'ecdalongwell')
                totalapl +=pressureloss['pressureloss']
        
        # print(f"avg_mudweight {avg_mudweight}")
        # print(f"totalapl {totalapl}")


        # ecd_with=avg_mudweight+totalapl/(0.052*tvd)
        # ecd_without=mud_weight+pressureoss['totalannular_pressureloss']/(0.052*tvd)
        ecd_with=calcualte_ecd(avg_mudweight,totalapl,tvd,unit)
        ecd_without=calcualte_ecd(mud_weight,pressureoss['totalannular_pressureloss'],tvd,unit)
        rop_ecd_without_chart.append({'x':i,"y":round(ecd_without,2)})
        rop_ecd_with_chart.append({'x':i,"y":round(ecd_with,2)})
    # return rop_ecd_chart
    data={
        'ecd_without':rop_ecd_without_chart,
        'ecd_with':rop_ecd_with_chart
    }
    # print(f"data {data}")
    return data

#calculate viscocity for newtonian modal
def calculate_viscocity_newtonian(rheogramsections,sections,muddata):
    if(muddata.plastic_viscosity!=None and muddata.yield_point!=None ):
        viscocity=muddata.plastic_viscosity/1000
        displaypv=muddata.plastic_viscosity
        selected_model='1'
    else:
        if(muddata.well.well_type == 'PLAN'):
            rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=None)
            selected_model=sections.selected_model
        else:
            rheogram=Rheogram.objects.filter(rheogram_date_id=rheogramsections[0].id,status=1,modelname=None)
            selected_model='1'
        rpm=[]
        dial=[]
        for rheogramdata in rheogram:
            if rheogramdata.dial!='':
                rpm.append(rheogramdata.rpm)
                dial.append(float(rheogramdata.dial))
                if(rheogramdata.rpm==300):
                    dial300=float(rheogramdata.dial)
                if(rheogramdata.rpm==600):
                    dial600=float(rheogramdata.dial) 

        X=np.array(rpm).reshape(-1,1)
        Y=np.array(dial).reshape(-1,1)
        Ne=LinearRegression(fit_intercept=False)
        Ne.fit(X,Y)
        mu=Ne.coef_[0]
        viscosity = np.around(mu, decimals=2).tolist()[0]
        viscocity=viscosity*1.066*0.4788/1.703
        displaypv=dial600-dial300
        displayyp=dial300-displaypv
    data={
        'plastic_viscosity':viscocity,
        'sectionname':muddata.section,
        'selected_modal':selected_model,
        # 'selected_modal':sections.selected_model,
        'displaypv':displaypv,
    }
    return data

def calculate_slipvelocity_newtonian(unit,rpm,flowrate,mud_weight,cased_hole_size,od,viscocity,cuttings_density,cuttings_size):

    cased_hole_size = calculate_holesize(cased_hole_size,unit)
    od = calculate_od(converttofloat(od),unit)
    mud_weight = calculate_mudweight(mud_weight,unit)
    flowrate = calculate_flowrate(flowrate,unit)
    cuttings_density = calculate_cutting_density(cuttings_density,unit)
    cuttings_size = calculate_cutting_size(cuttings_size,unit)

    annular_velocity=24.51*flowrate/(cased_hole_size**2-converttofloat(od)**2)
    apparent_velocity=viscocity["plastic_viscosity"]*1000

    turbulent_vs=9.24*sqrt(cuttings_size*(cuttings_density-mud_weight)/mud_weight)
    turbulent_nRe=15.47*mud_weight*cuttings_size*turbulent_vs/apparent_velocity
    
    stoke_vs=4972*cuttings_size**2/apparent_velocity*(cuttings_density-mud_weight)
    stoke_nRe=15.47*mud_weight*cuttings_size*stoke_vs/apparent_velocity

    transitional_vs=174*cuttings_size*(cuttings_density-mud_weight)**0.667/(mud_weight**0.333*apparent_velocity**0.333)
    transitional_nRe=15.47*mud_weight*cuttings_size*transitional_vs/apparent_velocity

    if(turbulent_nRe>2000):
        slip_velocity=turbulent_vs
    else:
        if(stoke_nRe<=1):
            slip_velocity=stoke_vs
        else:
            slip_velocity=transitional_vs

    slip_velocity = slipvelocity_conversion(slip_velocity,unit)

    data={
        'slip_velocity':slip_velocity,
        'annular_velocity':annular_velocity
    }
    return data

#pressure loss calculation for newtonian modal
def calculate_newtonian_pressureloss(unit,rpm,flowrate,mudweight,identity,length,viscocity):
    viscocity_si=viscocity
    flowrate_si=convertflowrate(flowrate,unit)
    mudweight_si=mudweight_conversion(mudweight,unit)
    identity_si=odconversion(float(identity),unit)
    length_si=odconversion(float(length),unit)

    velocity=flowrate_si/(pi/4*identity_si**2) 
    Re=mudweight_si*velocity*identity_si/viscocity_si
    def f_x(f):
        return 1/sqrt(f)+4*log10((e/identity_si)/3.7+1.255/(Re*sqrt(f)))
    if Re<=2100:
        flowregime="Laminar"
        f=16/Re
    elif Re>4100:
        e=0.000045
        f=newton(f_x,0.01)
        flowregime="Turbulent"
    else:
        flowregime="Transitional"
        e=0.000045
        f_l=16/2100
        def f_x(f):
            return 1/sqrt(f)+4*log10((e/identity_si)/3.7+1.255/(4100*sqrt(f)))
        f_turb=newton(f_x,0.01)
        x=(2100,4100)
        y=(f_l,f_turb)
        f_tran=interpolate.interp1d(x,y)
        f=f_tran(Re)
        f=f.tolist()
    dP=2*f*mudweight_si*velocity**2*length_si/identity_si
        
    dp_api=pressureloss_conversion(dP,unit)
    
    data={
        'viscocity_si':viscocity_si,
        'flowrate_si':flowrate_si,
        'mudweight_si':mudweight_si,
        'ID':identity_si,
        'length':length_si,
        'velocity':velocity,
        'Re': Re,
        'flowregime':flowregime,
        'f':f,
        'pressureloss':dp_api,
        'dP':dP,
        'flowrate':flowrate,
        'mudweight':mudweight,
        'identity':identity,
        'originallength':length,
        'originalviscocity':viscocity

    }
    return data


def calculate_newtonian_annular(viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,unit):
    # print(f"od_of_pipe_element {od_of_pipe_element}")
    # print(f'flowrate {flowrate}')
    # print(f'mud_weight {mud_weight}')
    # print(f'od_of_pipe_element {od_of_pipe_element}')
    # print(f'viscocity {viscocity["plastic_viscosity"]}')
    # print(f'length {length}')
    flowrate_si=convertflowrate(flowrate,unit)
    mudweight_si=mudweight_conversion(mud_weight,unit)
    rpm_si = rpm_convert(int(rpm))
    casing_hole_size_si = convertcasing_hole_size(float(casing_hole_size),unit)
    od_of_pipe_element_si = odconversion(float(od_of_pipe_element),unit)
    # viscocity_si=viscosity_conversion(viscocity['plastic_viscosity'],unit)
    length_si=length_conversion(length,unit)

    # print(f'flowrate_si {flowrate_si}')
    # print(f'mudweight_si {mudweight_si}')
    # print(f'casing_hole_size_si {casing_hole_size_si}')
    # print(f'od_of_pipe_element_si {od_of_pipe_element_si}')
    # print(f'viscocity_si {viscocity}')
    # print(f'length_si {length_si}')

    U=flowrate_si/(pi/4*(casing_hole_size_si**2-od_of_pipe_element_si**2))
    D_eq=(casing_hole_size_si**2+od_of_pipe_element_si**2-(casing_hole_size_si**2-od_of_pipe_element_si**2)/log(casing_hole_size_si/od_of_pipe_element_si))/(casing_hole_size_si-od_of_pipe_element_si)
    Re=mudweight_si*U*D_eq/converttofloat(viscocity['plastic_viscosity'])
   


    def f_x(f):
        return 1/sqrt(f)+4*log10((e/D_eq)/3.7+1.255/(Re*sqrt(f)))
    if Re<=2100:
        flowregime="Laminar"
        f=16/Re
    elif Re>4100:
        e=0.000045
        f=newton(f_x,0.01)
        flowregime="Turbulent"
    else:
        flowregime="Transitional"
        e=0.000045
        f_l=16/2100
        def f_x(f):
            return 1/sqrt(f)+4*log10((e/D_eq)/3.7+1.255/(4100*sqrt(f)))
        f_turb=newton(f_x,0.01)
        x=(2100,4100)
        y=(f_l,f_turb)
        f_tran=interpolate.interp1d(x,y)
        f=f_tran(Re)
        f=f.tolist()

    pl_without_string_rotation=2*f*mudweight_si*U**2*length_si/(casing_hole_size_si-od_of_pipe_element_si)
    
    lamda=sqrt(((od_of_pipe_element_si/casing_hole_size_si)**2-1)/(2*log(od_of_pipe_element_si/casing_hole_size_si)))

    t=pl_without_string_rotation*od_of_pipe_element_si/(2*length_si)*abs(lamda**2/1-1) if(length_si>0) else 0

    S_a=t/viscocity['plastic_viscosity']
    
    S_ta=rpm_si*od_of_pipe_element_si/(casing_hole_size_si-od_of_pipe_element_si)

    S_t=sqrt(S_a**2+S_ta**2)

    t_t=viscocity['plastic_viscosity']*S_t

    pressureloss=t_t*2*length_si/(od_of_pipe_element_si*abs(lamda**2/1-1))
    
    if unit == 'API':
        pressureloss =pressureloss * 3.28084
        
        pressureloss =pressureloss * 0.000145038
    else:
        dP_anno_SI = pl_without_string_rotation/0.000145038/1000
        pressureloss =pressureloss/1000

    data={
        'pressureloss':pressureloss,
        'flowregime':flowregime
    }
    return data


def calculate_cuttings_size(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request,tvd,rop,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth):
    unit=getprojectunit(well_id)
    allcutting_size=np.arange(0.05, 1.05, 0.05)
    allcutting_size=allcutting_size.tolist()
    cuttingsize_ecd_chart=[]
    cuttings_size_withecd=[]
    cuttings_size_withoutecd=[]
    for i in allcutting_size:
        pressureoss=calculateapldrillstring_withoutanychart(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,i,muddata,'cuttingsdensitychange',rop)
        allcasing=0
        casinglength=0
        allopenhole=0
        openholelength=0
        getavg_mudweight=calculate_avgmudweight(bhadata,sectiontodepth,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,i,rop,sectiontodepth,viscocity)
        for mudweight in getavg_mudweight:
            if(mudweight["element_type"]=='CH'):
                allcasing +=mudweight["length"]*mudweight['mudweight']
                casinglength +=mudweight["length"]
            else:
                allopenhole +=mudweight["length"]*mudweight['mudweight']
                openholelength +=mudweight["length"]
        avg_mudweight=(allcasing/casinglength+allopenhole)/openholelength
        # print(f"getavg_mudweight {avg_mudweight}")

        totalapl=0
        for mudweight in getavg_mudweight:
            if(mudweight["element_type"]=='CH'):
                pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,avg_mudweight,mudweight["od"],id_of_previous_casing,mudweight["length"],'ecdalongwell')
                totalapl +=pressureloss['pressureloss']
            else:
                pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,avg_mudweight,mudweight["od"],hole_size,mudweight["length"],'ecdalongwell')
                totalapl +=pressureloss['pressureloss']
        # print(f"cuttsize {i}")
        # print(f"totalapl {totalapl}")
        # print(f"avg_mudweight {avg_mudweight}")
        # ecd_with=avg_mudweight+totalapl/(0.052*tvd)
        # ecd_without=mud_weight+pressureoss['totalannular_pressureloss']/(0.052*tvd)
        ecd_with=calcualte_ecd(avg_mudweight,totalapl,tvd,unit)
        ecd_without=calcualte_ecd(mud_weight,pressureoss['totalannular_pressureloss'],tvd,unit)
        cuttings_size_withecd.append({"x":round(i,2),"y":round(ecd_with,2)})
        cuttings_size_withoutecd.append({"x":round(i,2),"y":round(ecd_without,2)})

    data={
        'ecd_without':cuttings_size_withoutecd,
        'ecd_with':cuttings_size_withecd
    }
    #     ecd=mud_weight+pressureoss['totalincreasedannular_pressureloss']/(0.052*tvd)
    #     cuttingsize_ecd_chart.append({'x':i,"y":ecd})
    # print(f"datacs {data}")
    return data


def calculate_yieldpoint_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase):
    i=1
    allannularloss=[]
    alldrillstringloss=[]
    allbitloss=[]
    allsurfaceloss=[]
    totalpressureloss=[]
    while i<50:
        viscocity['yield_point']=i
        pressureoss=calculateapldrillstring_withoutanychart(bhadata,sectiontodepth,length_of_previous_casing_from_surface,muddata.mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,'yieldpointchange')

        bit_losses=getbitpressureloss(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,
        well_id)
        surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity,'yieldpointchange')
        totalsurfaceloss=0
        for suface in surface_losses:
            totalsurfaceloss +=suface['pressureloss']
        
        totalpressure=pressureoss['totalannular_pressureloss']+pressureoss['totaldrillstring_loss']+bit_losses[0]['bit_pressure_loss']+totalsurfaceloss
        allannularloss.append({'x':i,'y':pressureoss['totalannular_pressureloss']})
        alldrillstringloss.append({"x":i,'y':pressureoss['totaldrillstring_loss']})
        allbitloss.append({'x':i,'y':bit_losses[0]['bit_pressure_loss']})
        allsurfaceloss.append({'x':i,'y':totalsurfaceloss})
        totalpressureloss.append({'x':i,'y':totalpressure})
        i +=5
    
    data={
        'allannularloss':allannularloss,
        'alldrillstringloss':alldrillstringloss,
        'allbitloss':allbitloss,
        'allsurfaceloss':allsurfaceloss,
        'totalpressureloss':totalpressureloss
    }
    return data    

def calculate_cuttings_density(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request,tvd,rop,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth):
    unit=getprojectunit(well_id)
    allcutting_density=np.arange(19, 25.5, 0.5)
    allcutting_density=allcutting_density.tolist()
    cuttings_density_withecd=[]
    cuttings_density_withoutecd=[]

    for i in allcutting_density:
        pressureoss=calculateapldrillstring_withoutanychart(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,i,cuttings_size,muddata,'cuttingsdensitychange',rop)
        allcasing=0
        casinglength=0
        allopenhole=0
        openholelength=0
        getavg_mudweight=calculate_avgmudweight(bhadata,sectiontodepth,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,i,rop,sectiontodepth,viscocity)
        for mudweight in getavg_mudweight:
            if(mudweight["element_type"]=='CH'):
                allcasing +=mudweight["length"]*mudweight['mudweight']
                casinglength +=mudweight["length"]
            else:
                allopenhole +=mudweight["length"]*mudweight['mudweight']
                openholelength +=mudweight["length"]
        avg_mudweight=(allcasing/casinglength+allopenhole)/openholelength
        # print(f"getavg_mudweight {avg_mudweight}")

        totalapl=0
        for mudweight in getavg_mudweight:
            if(mudweight["element_type"]=='CH'):
                pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,avg_mudweight,mudweight["od"],id_of_previous_casing,mudweight["length"],'ecdalongwell')
                totalapl +=pressureloss['pressureloss']
            else:
                pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,avg_mudweight,mudweight["od"],hole_size,mudweight["length"],'ecdalongwell')
                totalapl +=pressureloss['pressureloss']
      
        # ecd_with=avg_mudweight+totalapl/(0.052*tvd)
        # ecd_without=mud_weight+pressureoss['totalannular_pressureloss']/(0.052*tvd)
        ecd_with=calcualte_ecd(avg_mudweight,totalapl,tvd,unit)
        ecd_without=calcualte_ecd(mud_weight,pressureoss['totalannular_pressureloss'],tvd,unit)

        cuttings_density_withecd.append({"x":i,"y":round(ecd_with,2)})
        cuttings_density_withoutecd.append({"x":i,"y":round(ecd_without,2)})

    data={
        'ecd_with':cuttings_density_withecd,
        'ecd_without':cuttings_density_withoutecd
    }
             
    return data

def calculate_tfa_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request):
    unit=getprojectunit(well_id)
    # bit_losses=getbitpressureloss(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id)
    drillbit = DrillBit.objects.filter(well_id=well_id,well_phases_id=wellphase_id,status=1).first()
    bittype = BitTypesNames.objects.get(id=drillbit.bit_type_id)
    nozzle_size = DrillBitNozzle.objects.filter(drillbit_id=drillbit,well_id=well_id,status=1)
    bit_pressure_chart=[]
    allchart_data=[]
    if(drillbit.external_nozzle == 1):
        cd_values = 0.95
    else:
        cd_values = bittype.bit_values
    hole_size = wellphase.hole_size
    alltfa=[]
    if not 'tfa_range' in request.session:
        i=0.1
        while i<=5:
            if unit == 'API':
                bhhp=i*pi/4*hole_size**2
                bit_pressure_loss=bhhp*1714/flowrate
                tfa=sqrt(mud_weight*flowrate**2/(12042*cd_values**2*bit_pressure_loss))
            else:
                bhhp=i/1.34*(pi/4*(hole_size/1000*12*3.281)**2)
                bit_pressure_loss=bhhp*1000/0.435*(3.7854/flowrate/0.145038)
                tfa = sqrt(mud_weight*1000*(flowrate/3.7854*0.000063)**2/(2*cd_values**2*bit_pressure_loss*1000))*1000000
            i=round(i,1)+float(0.1)
            alltfa.append(round(tfa,2))
    
        min_tfa=min(alltfa)
        max_tfa=max(alltfa)
        if unit == 'API':
            i=min_tfa
            newtfa=[]
            while i<=max_tfa:
                newtfa.append(round(i,2))
                i +=0.1
        else:
            i=min_tfa
            newtfa=[]
            while i<=max_tfa:
                newtfa.append(round(i,2))
                i += 10
        if(newtfa[-1]<max_tfa):
            newtfa.append(max_tfa)
        request.session['tfa_range']=newtfa

    else:
        newtfa=request.session['tfa_range']
    

    for tfa in newtfa:
        # bit_pressure_loss=getbitpressureloss_manual_values(mud_weight,flowrate,cd_values,tfa,hole_size,unit)
        bit_pressure_loss=bit_loss_conversion(flowrate,mud_weight,tfa,cd_values,hole_size,unit)
        pressureoss=calculateapldrillstring_withoutanychart(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,'muddatachange')
        surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,mud_weight,wellphase,previous_wellphase,well_id,viscocity,"mudweightchange")
        totalsurfaceloss=0
        for suface in surface_losses:
            totalsurfaceloss +=suface['pressureloss']
        # totalpressure=pressureoss['totalannular_pressureloss']+pressureoss['totaldrillstring_loss']+bit_pressure_loss+totalsurfaceloss
        # bit_pressure_chart.append({'x':tfa,'y':round(bit_pressure_loss)})
        totalpressure=pressureoss['totalannular_pressureloss']+pressureoss['totaldrillstring_loss']+bit_pressure_loss[0]['bit_pressure_loss']+totalsurfaceloss
        bit_pressure_chart.append({'x':tfa,'y':round(bit_pressure_loss[0]['bit_pressure_loss'])})
        allchart_data.append({'x':tfa,'y':round(totalpressure)})
    data={
        'bit_pressure_chart':bit_pressure_chart,
        'totalpressureloss':allchart_data
    }
    return data


def calculate_slipvelocity(request):
    
    rpm=request.GET['rpm']
    flowrate=int(request.GET['flowrate'])
    print('flowrate',flowrate)
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    well_id=request.session['well_id']
    rop=request.GET['rop']
    request.session['rop_input']=rop
    request.session['rpm_input']=rpm
    given_bitdepth=request.GET['bitdepth'] 
    cuttings_density=converttofloat(request.GET['cuttings_density'])
    cuttings_size=converttofloat(request.GET['cuttings_size'])

    muddata=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    viscocity=getviscocity(muddata)

    allslipvelocity=[]
    slipvelocitychart=[]
    allslipvelocitychartdata=[]
    allslipvelocityanuulardata=[]

    slipvelocitychart_walker=[]
    annularvelocitychartdata_walker=[]

    annularvelocitychartdata=[]
    allslipvelocity_walker=[]
    bhadata=BhaData.objects.getbha(wellphase_id)
    
    wellphase = WellPhases.objects.getwellphase_byid(wellphase_id)
    previous_wellphase=WellPhases.objects.getprevious_wellphase(wellphase.id,well_id)
    length_of_previous_casing_from_surface=0 if previous_wellphase==None else previous_wellphase.measured_depth
    sectiontodepth=muddata.todepth if(given_bitdepth=='') else int(given_bitdepth)
    previousbhaelement=BhaElement.objects.getbhaelement(bhadata.id)
    bhacount=previousbhaelement.count()
    i=bhacount
    previous_length_against_casing=[]
    hole_size=wellphase.hole_size
    id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
    cumlativelength=0
    for previousbha in previousbhaelement:
        if(previousbha.length_onejoint<sectiontodepth):
            newlength=converttofloat(previousbha.length)
        else:
            belowbha=BhaElement.objects.getpreviousbhaelement(bhadata.id,previousbha.id)
            newlength=sectiontodepth-belowbha.length_onejoint
        od_of_pipe_element=previousbha.od
        if(i==bhacount):
            length_against_casing=length_of_previous_casing_from_surface if(converttofloat(newlength)>=length_of_previous_casing_from_surface) else newlength
            previous_length_against_casing.append(length_against_casing)
        else:
            sum_of_previous_against_casing=Sum = sum(previous_length_against_casing)
            if(sum_of_previous_against_casing==length_of_previous_casing_from_surface):
                length_against_casing=0
            if((sum_of_previous_against_casing<length_of_previous_casing_from_surface) and (sum_of_previous_against_casing+newlength<length_of_previous_casing_from_surface)):
                length_against_casing=newlength
            else:
                length_against_casing=length_of_previous_casing_from_surface-sum_of_previous_against_casing
            previous_length_against_casing.append(length_against_casing)
        length_against_open_hole=converttofloat(newlength)-length_against_casing
      
        if(length_against_casing!=0):
            cumlativelength +=length_against_casing
            slipvelocity=calculateslipvelocitywithoutliner(well_id,rpm,flowrate,muddata.mud_weight,id_of_previous_casing,previousbha.od,viscocity,cuttings_density,cuttings_size,length_against_casing)
            slipvelocitywalker= slipvelocity_walker(muddata,id_of_previous_casing,rpm,previousbha.od,cuttings_density,cuttings_size,flowrate)
           
            
            if(slipvelocity["slipvelocity"]>=slipvelocitywalker["slipvelocity"]):
                slipvelocityvalue=slipvelocity["slipvelocity"]
            else:
                slipvelocityvalue=slipvelocitywalker["slipvelocity"]
            
            allslipvelocitychartdata.append({'x':round(slipvelocityvalue),"y":cumlativelength,'od':previousbha.od,'cased_hole_size':id_of_previous_casing,'annular_velocity':round(slipvelocity["annular_velocity"]),'element_type':'CH'})
           
        if(length_against_open_hole!=0):
            cumlativelength +=length_against_open_hole
            slipvelocity=calculateslipvelocitywithoutliner(well_id,rpm,flowrate,muddata.mud_weight,hole_size,previousbha.od,viscocity,cuttings_density,cuttings_size,length_against_open_hole)

            slipvelocitywalker= slipvelocity_walker(muddata,hole_size,rpm,previousbha.od,cuttings_density,cuttings_size,flowrate)

            if(slipvelocity["slipvelocity"]>=slipvelocitywalker["slipvelocity"]):
                slipvelocityvalue=slipvelocity["slipvelocity"]
            else:
                slipvelocityvalue=slipvelocitywalker["slipvelocity"]
            allslipvelocitychartdata.append({'x':round(slipvelocityvalue),"y":cumlativelength,'od':previousbha.od,'cased_hole_size':hole_size,'annular_velocity':round(slipvelocity["annular_velocity"]),'element_type':'OH'})
           
        previouselement_length=previousbha.length_onejoint
        i -=1
    
    
    data={
        'slipvelocitychart':allslipvelocitychartdata,

    }
    input_data={
        'flowrate':flowrate,
        'rpm':rpm,
        'rop':rop
    }
    Calculationchartdata.objects.create_calculation_result(well_id,wellphase_id,section_name,'slipvelocity',json.dumps(allslipvelocitychartdata),json.dumps(input_data))

    return JsonResponse(data,safe=False)

def reverse_calculate_viscocity_powerlaw(plastic_viscocity,yield_point,unit):
    rheogram_rpm= RheogramNameModels.objects.all()
    rpm=[int(rpm.rheogram_rpm) for rpm in rheogram_rpm]
    newdial=[]
    for i in rpm:
        viscocity=(plastic_viscocity/1000*0.02088*100*i*1.703)/1.066
        newdial.append(round(viscocity,2))
    if unit == 'API':
        t300_data=plastic_viscocity+yield_point
        t600_data=t300_data+plastic_viscocity
    else :
        pv = plastic_viscocity*1000
        yp = yield_point/0.4788
        t300_data=pv+yp
        t600_data=t300_data+pv

    n=3.32*log10(t600_data/t300_data)
    K=t300_data/pow(511,n)
    data={
        'plastic_viscosity':plastic_viscocity,
        'yieldpoint':yield_point,
        'K':K,
        'n':n,  
    }
    return data




class DownloadPressurelossChart(View):
    template_name = 'generate_pressureloss_chart_pdf.html'
    def get(self,request,chart_type,wellphase_id):
        well_id=request.session['well_id']
        section_details=Sections.objects.getsection_bywellphase_id(wellphase_id)
        if(chart_type=='ecdalonghole'):
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'ecdalongwellchartdata',section_details.section_name)
            data=json.loads(result.result) 
            print('ecdalonghole_diag',section_details.section_name)
            chart_name="ECD Alonehole PDF.pdf"
            image_name='ecdalonghole-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)

        elif(chart_type=='pressureloss'):
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'pressureloss',section_details.section_name)
            print('pressureloss_result',result)
            data=json.loads(result.result) 
            print('pressureloss_diag',data)
            chart_name="Pressureloss PDF.pdf"
            image_name='pressure_chart-'+str(wellphase_id)+'-'+section_details.section_name+'.png'  
            encoded_image =   base64image(image_name)

        elif(chart_type=='ecdbitdepth'):
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'ecdbitdepth',section_details.section_name)
            data=json.loads(result.result) 
            chart_name="ECD Bitdepth PDF.pdf"
            print('ecdbitdepth',section_details.section_name)
            image_name='ecdbitdepth-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name) 
            
        elif(chart_type=='slip_velocity'):
            chart_name="Slip Velocity PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'slipvelocity',section_details.section_name)
            print('slip_result',result)
            data=json.loads(result.result)
            print('slip_velocity_chart',result)
            image_name='slip_velocity-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)

        elif(chart_type=='annular_velocity'):
            chart_name="Annular Velocity PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'annularvelocity',section_details.section_name)
            data=json.loads(result.result)
            print('annular_velocity_diag',data)
            print('annular_velocity_chart',section_details.section_name)
            image_name='slip_velocity-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)

        elif(chart_type=='cuttings_concentration'):
            chart_name="Cuttings Concentration PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'cuttingsconcentration',section_details.section_name)
            data=json.loads(result.result)
            print('cuttings_concentration_chart',section_details.section_name,data)
            image_name='cuttings_concentration-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)

            
            
        elif(chart_type=='transport_ratio'):
            chart_name="Transport Ratio PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'transportratio',section_details.section_name)
            data=json.loads(result.result)
            image_name='transport_ratio-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)
            
            
        elif(chart_type=='cci'):
            chart_name="CCI PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'cci',section_details.section_name)
            data=json.loads(result.result)
            print('cci_views',data)
            image_name='cci-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)
            
        elif(chart_type=='mudweight_pressure'):
            chart_name="MudweightPressure PDF.pdf" 
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'mudweight_pressure',section_details.section_name)
            data=json.loads(result.result)
            image_name='mudweight_pressure-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)
            
        elif(chart_type=='mudweight_ecd'):
            chart_name="MudweightECD PDF.pdf" 
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'mudweight_ecd',section_details.section_name)
            data=json.loads(result.result)
            image_name='mudweight_ecd-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)
            
        elif(chart_type=='tfa_pressure'):
            chart_name="TFA PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'tfa_pressure',section_details.section_name)
            data=json.loads(result.result)
            image_name='tfa_pressure-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)
            
        elif(chart_type=='yieldpoint_pressure'):
            chart_name="Yieldpoint PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'yieldpoint_pressure',section_details.section_name)
            data=json.loads(result.result)
            image_name='yieldpoint_pressure-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)
            
        elif(chart_type=='flowrate_pressure'):
            chart_name="FlowratePressure PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'flowrate_pressure',section_details.section_name)
            data=json.loads(result.result)
            image_name='flowrate_pressure_chart-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)
        
        elif(chart_type=='flowrate_ecd'):
            chart_name="FlowrateECD PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'flowrate_ecd',section_details.section_name)
            data=json.loads(result.result)
            image_name='flowrate_ecd_chart-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)
            
        elif(chart_type=='viscocity_pressure'):
            chart_name="ViscocityPressure PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'viscocity_pressure',section_details.section_name)
            data=json.loads(result.result)
            image_name='viscocity_pressure_chart-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)
            
        elif(chart_type=='viscocity_ecd'):
            chart_name="ViscocityECD PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'viscocity_ecd',section_details.section_name)
            data=json.loads(result.result)
            image_name='viscocity_ecd_chart-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)
            
            
        
        elif(chart_type == 'cs_ecdwith'):
            chart_name="CuttingsSizeECD PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'cuttings_size_ecd',section_details.section_name)
            data=json.loads(result.result)
            print('inside_cs_ecdwith',data)
            image_name='cuttings_size_ecd-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)
            
        elif(chart_type == 'cd_ecdwith'):
            chart_name="CuttingDensityECD PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'cuttings_density_ecd',section_details.section_name)
            data=json.loads(result.result)
            print('inside_cd_ecdwith',data)
            image_name='cuttings_density_ecd-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)
            
            
        elif(chart_type == 'rop_ecdwith'):
            chart_name="ROPECD PDF.pdf"
            result = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'rop_ecd',section_details.section_name)
            data=json.loads(result.result)
            print('inside_rop_ecdwith',data)
            image_name='rop_ecd-'+str(wellphase_id)+'-'+section_details.section_name+'.png'
            encoded_image =   base64image(image_name)
       
        print(f"image_name {image_name}")
        context = {
            'data': data,
            'chart_type':chart_type,
            'image_name':image_name,
            'wellphase_id':wellphase_id,
            'section_name':section_details.section_name

        }
        # return render(request,self.template_name,context)
        image_name='test.png'

        pressureloss_chart = render_to_string(self.template_name,context,request)
        pressureloss_chart_style = pressurelosschart_pdfstyle(encoded_image)
        css = CSS(string=pressureloss_chart_style)
        pdf_buffer = BytesIO()
        HTML(string=pressureloss_chart).write_pdf(pdf_buffer, stylesheets=[css])
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{chart_name}"'
        return response

def setsession(request):
    data=request.POST.get('data')
    data_json=json.loads(data)
    typename = data_json['typename']
    value=data_json['val']
    request.session[typename]=value

    return JsonResponse({"status": "true"})

def base64image(image_name):
    try:
        with open('media/'+image_name, 'rb') as f:
            image_data = f.read()
        image = Image.open(BytesIO(image_data))
        image = image.convert('RGB')  
        image = image.resize((120, 80))  
        buffered = BytesIO()
        image.save(buffered, format="JPEG")      
        encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return encoded_image
    except FileNotFoundError:
        return None


def generate_phase_report(request,wellphase_id):
    template_name = 'hydraulics_report_pdf.html'
    wellphase_details=WellPhases.objects.getwellphase_byid(wellphase_id)
    well_and_project_details=Wells.objects.getwell_and_project_byid(wellphase_details.well_id)
    current_date = timezone.now().date()
    formatted_date = current_date.strftime('%d %B %Y')
    section_name=request.GET['section_name']
    calculation_chartdata=Calculationchartdata.objects.get_calculation_inputdata(wellphase_details.well_id,wellphase_id,section_name)
    input_data=json.loads(calculation_chartdata.input_data)
    muddetails=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    # print(f"muddetails {muddetails}")
    rheogram_sections=RheogramSections.objects.getrheogramsections(section_name,wellphase_id)

    try:
        rehogram_details=RheogramDate.objects.getrheogramdate_byid(rheogram_sections.rheogram_date_id)
    except RheogramDate.DoesNotExist:
        rehogram_details = None
    
    if(rehogram_details):
        if(rehogram_details.selected_model):
            if(rehogram_details.selected_model=="1"):
                rheogram_datas=Rheogram.objects.getrheogram_byselectedmodel(rehogram_details.id,'newtonian',rheogram_sections.id)
            elif(rehogram_details.selected_model=="2"):
                rheogram_datas=Rheogram.objects.getrheogram_byselectedmodel(rehogram_details.id,'bingham',rheogram_sections.id)
            elif(rehogram_details.selected_model=="3"):
                rheogram_datas=Rheogram.objects.getrheogram_byselectedmodel(rehogram_details.id,'powerlaw',rheogram_sections.id)
            else:
                rheogram_datas=Rheogram.objects.getrheogram_byselectedmodel(rehogram_details.id,'hershel',rheogram_sections.id)
        else:
            rheogram_datas=Rheogram.objects.getrheogram(rehogram_details.id)
    else:
        rheogram_datas=[]


    annular_drillingstringloss = Calculationchartdata.objects.get_calculation_result(wellphase_details.well_id,wellphase_id,'annulardrillstringloss',section_name)

    bitpressure_loss = Calculationchartdata.objects.get_calculation_result(wellphase_details.well_id,wellphase_id,'bitpressureloss',section_name)
    surfacepressure_loss = Calculationchartdata.objects.get_calculation_result(wellphase_details.well_id,wellphase_id,'surfacepressureloss',section_name)


    totalsurfacelosses=0
    for surfaceloss in json.loads(surfacepressure_loss.result):
        totalsurfacelosses +=surfaceloss['pressureloss']
    
    totaldrillstringlosses=0
    totalannularlosses=0

    for pressureloss in json.loads(annular_drillingstringloss.result):
        totaldrillstringlosses +=pressureloss['drillstringloss']
        totalannularlosses +=pressureloss['pressureloss']

    totalpressureloss=totalsurfacelosses+json.loads(bitpressure_loss.result)[0]['bit_pressure_loss']+totaldrillstringlosses+totalannularlosses
  
    viscocity=getviscocity(muddetails)

    alongwellecd_data =  Calculationchartdata.objects.get_calculation_result(wellphase_details.well_id,wellphase_id,'alongwellecd_data',section_name)

    bitdepthecd_data = Calculationchartdata.objects.get_calculation_result(wellphase_details.well_id,wellphase_id,'bitdepthecd_data',section_name)

    context={
        'formatted_date':formatted_date,
        'well_and_project_details':well_and_project_details,
        'wellphase_details':wellphase_details,
        'section_name':section_name,
        'input_data':input_data,
        'muddetails':muddetails,
        'rheogram_datas':rheogram_datas,
        'annular_drillingstringloss':json.loads(annular_drillingstringloss.result),
        'bitpressure_loss':json.loads(bitpressure_loss.result),
        'surfacepressure_loss':json.loads(surfacepressure_loss.result),
        'totalsurfacelosses':totalsurfacelosses,
        'totaldrillstringlosses':round(totaldrillstringlosses),
        'totalannularlosses':round(totalannularlosses),
        'totalbitpressureloss':round(json.loads(bitpressure_loss.result)[0]['bit_pressure_loss']),
        'totalpressureloss':round(totalpressureloss),
        'viscocity':viscocity,
        'user':request.user,
        'alongwellecd_data':json.loads(alongwellecd_data.result),
        'bitdepthecd_data':json.loads(bitdepthecd_data.result)
        
    }

    hydraulics_report = render_to_string(template_name,context,request)
    hydraulics_report_style = hydraulics_report_pdfstyle()
    css = CSS(string=hydraulics_report_style)
    pdf_buffer = BytesIO()
    HTML(string=hydraulics_report).write_pdf(pdf_buffer, stylesheets=[css])
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Phase Report Format.pdf"'
    return response

def sensitivity_report(request,wellphase_id):
    template_name = 'sensitivity_report_pdf.html'
    wellphase_details=WellPhases.objects.getwellphase_byid(wellphase_id)
    section_name=request.GET['section_name']
    well_and_project_details=Wells.objects.getwell_and_project_byid(wellphase_details.well_id)
    current_date = timezone.now().date()
    formatted_date = current_date.strftime('%d %B %Y')
    muddetails=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)

    context={
        'formatted_date':formatted_date,
        'well_and_project_details':well_and_project_details,
        'wellphase_details':wellphase_details,
        'section_name':section_name,
        'well_id':wellphase_details.well_id,
        'muddetails':muddetails
    }
    sensitivity_report = render_to_string(template_name,context,request)
    sensitivity_report_style = sensitivity_report_pdfstyle()
    css = CSS(string=sensitivity_report_style)
    pdf_buffer = BytesIO()
    HTML(string=sensitivity_report).write_pdf(pdf_buffer, stylesheets=[css])
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Sensitivity Phase Report.pdf"'
    return response

def generate_totalwell_report(request,wellphase_id):
    template_name = 'totalwell_report_pdf.html'
    wellphase_details=WellPhases.objects.getwellphase_byid(wellphase_id)
    well_and_project_details=Wells.objects.getwell_and_project_byid(wellphase_details.well_id)
    current_date = timezone.now().date()
    formatted_date = current_date.strftime('%d %B %Y')
    section_name=request.GET['section_name']

    context={
        'formatted_date':formatted_date,
        'well_and_project_details':well_and_project_details,
        'wellphase_details':wellphase_details,
        'section_name':section_name,
        'well_id':wellphase_details.well_id
        
        
    }

    hydraulics_report = render_to_string(template_name,context,request)
    hydraulics_report_style = totalwell_report_pdfstyle()
    css = CSS(string=hydraulics_report_style)
    pdf_buffer = BytesIO()
    HTML(string=hydraulics_report).write_pdf(pdf_buffer, stylesheets=[css])
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Total Well Hydraulics Report Format.pdf"'
    return response

def calculateoptimization(request):  
    optimization_code=request.GET["optimization_code"]
    pump_spm=request.GET["pump_spm"]
    maximum_pressure=int(request.GET["maximum_pressure"])
    rpm=request.GET["rpm_input"]
    rop=request.GET["rop_input"]
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    torque=request.GET['torque'] if 'torque' in request.GET else ""
    wob=request.GET['wob'] if 'wob' in request.GET else ""
    alldata={}
    # print(f"get {request.GET}")
    pump_efficiency=request.GET["pump_efficiency"]
    mechanical_efficiency=request.GET["mechanical_efficiency"]
    max_flowrate=int(request.GET["max_flowrate"])
    min_flowrate=int(request.GET["min_flowrate"])
    wellphase = WellPhases.objects.filter(id=wellphase_id).first()
    well_id=wellphase.well_id
    surfacepipe=SurfacePipe.objects.filter(well_id=well_id).first()
    no_of_nozzle=int(request.GET["no_of_nozzle"])
    typename=request.GET["type"]


    # print(f"wellphase {wellphase}")
    previous_wellphase=WellPhases.objects.filter(id__lt=wellphase.id,well_id=well_id).order_by('-id').first()
    # print(f"previous_wellphase {previous_wellphase}")
    drillbit = DrillBit.objects.filter(well_id=well_id,well_phases_id=wellphase_id,status=1).first()

    original_tfa=float(request.GET['original_tfa'])

    muddata=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    bhadata=BhaData.objects.filter(well_phases_id=wellphase_id,status=1).first()
    length_of_previous_casing_from_surface=previous_wellphase.measured_depth
    mud_weight=muddata.mud_weight
    hole_size=wellphase.hole_size
    # print(f"hole_size {hole_size}")
    # print(f"previous_wellphase {previous_wellphase}")

    id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
    # print(f"id_of_previous_casing {id_of_previous_casing}")
    sectiontodepth=muddata.todepth
    viscocity=getviscocity(muddata)
    allflowrate=np.arange(min_flowrate-10, max_flowrate+10, 10)
    allflowrate=allflowrate.tolist()
    i=0
    alloptimization=[]
    cd_value=None
    for flowrate in allflowrate:
        totalpressureloss=0
        totalpf=0
        totalbit=0
        pressureloss=calculateapldrillstring(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,muddata,'calculateoptimization')
        totalpf +=pressureloss["totaldrillstring_loss"]+pressureloss["totalannular_pressureloss"]
        surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity,'calculateallpressureloss')
        totalsurfaceloss=0
        for surface in surface_losses:
            totalsurfaceloss +=surface["pressureloss"]
        totalpf +=totalsurfaceloss
        bit_losses=getbitpressureloss_optimization(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,original_tfa)
        totalbit +=bit_losses[0]["bit_pressure_loss"]
        cd_value=bit_losses[0]["cd_values"]
        totalpressureloss +=totalbit+totalpf
        if(i>0):
            m=round(log(totalpressureloss/previous_total_pressureloss)/log(flowrate/previous_flowrate),1)
            pressureloss_impactforce=2*int(maximum_pressure)/(m+2)
            pressurelossbit_impactforce=int(maximum_pressure)-pressureloss_impactforce
            total_impactforce=(pressureloss_impactforce/totalpf)*flowrate**m
            ofr_impactforce=total_impactforce**(1/m)
            pressureloss_hhp=int(maximum_pressure)/(m+1)
            pressurelossbit_hhp=int(maximum_pressure)-pressureloss_hhp
            total_hhp=(pressureloss_hhp/totalpf)*flowrate**m
            ofr_hhp=total_hhp**(1/m)
            alloptimization.append({"flowrate":flowrate,"totalpf":totalpf,'totalbit':totalbit,"m":m,"pressureloss_impactforce":pressureloss_impactforce,"pressurelossbit_impactforce":pressurelossbit_impactforce,'total_impactforce':total_impactforce,'ofr_impactforce':ofr_impactforce,'pressureloss_hhp':pressureloss_hhp,'pressurelossbit_hhp':pressurelossbit_hhp,'total_hhp':total_hhp,'ofr_hhp':ofr_hhp})
        previous_total_pressureloss=totalpressureloss
        previous_flowrate=flowrate
        i +=1
    alloptimization_count=len(alloptimization)
    
    #calculation for impact force upto step 1
    avg_orf_if=(alloptimization[0]["ofr_impactforce"]+alloptimization[alloptimization_count-1]['ofr_impactforce'])/2
    tfa_if=sqrt(mud_weight*avg_orf_if**2/(0.95**2*alloptimization[alloptimization_count-1]['pressurelossbit_impactforce']*12042))
    if(typename=='increased'):
        pb_if=muddata.mud_weight*avg_orf_if**2/(12042*cd_value**2*float(request.GET['increased_tfa'])**2)
    else:
        pb_if=muddata.mud_weight*avg_orf_if**2/(12042*cd_value**2*tfa_if**2)
    total_pf_avgorf_if =0
    pressureloss_avgorf_if=calculateapldrillstring(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,avg_orf_if,rpm,hole_size,viscocity,torque,wob,muddata,'calculateoptimization')
    total_pf_avgorf_if +=pressureloss_avgorf_if["totaldrillstring_loss"]+pressureloss_avgorf_if["totalannular_pressureloss"]
    surface_losses_avgorf_if=getsurfacelosses(rpm,avg_orf_if,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity,'calculateallpressureloss')
    totalsurfaceloss_avgorf_if=0
    for surface in surface_losses_avgorf_if:
        totalsurfaceloss_avgorf_if +=surface["pressureloss"]
    total_pf_avgorf_if +=totalsurfaceloss_avgorf_if
    total_if=total_pf_avgorf_if+pb_if
    bhhp_if = pb_if*avg_orf_if/1714
    hsi_if = bhhp_if/(pi/4*hole_size**2)
    impact_forces_if = 0.01823*cd_value*avg_orf_if*sqrt(mud_weight*pb_if)

    #calculation for HHP upto step 1
    avg_orf_hhp=(alloptimization[0]["ofr_hhp"]+alloptimization[alloptimization_count-1]['ofr_hhp'])/2
    tfa_hhp=sqrt(mud_weight*avg_orf_hhp**2/(0.95**2*alloptimization[alloptimization_count-1]['pressurelossbit_hhp']*12042))
    if(typename=='increased'):
        pb_hhp=muddata.mud_weight*avg_orf_hhp**2/(12042*cd_value**2*float(request.GET['increased_tfa'])**2)
    else:
        pb_hhp=muddata.mud_weight*avg_orf_hhp**2/(12042*cd_value**2*tfa_hhp**2)
    total_pf_avgorf_hhp=0
    pressureloss_avgorf_hhp=calculateapldrillstring(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,avg_orf_hhp,rpm,hole_size,viscocity,torque,wob,muddata,'calculateoptimization')
    total_pf_avgorf_hhp +=pressureloss_avgorf_hhp["totaldrillstring_loss"]+pressureloss_avgorf_hhp["totalannular_pressureloss"]
    surface_losses_avgorf_hhp=getsurfacelosses(rpm,avg_orf_hhp,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity,'calculateallpressureloss')
    totalsurfaceloss_avgorf_hhp=0
    for surface in surface_losses_avgorf_hhp:
        totalsurfaceloss_avgorf_hhp +=surface["pressureloss"]
    total_pf_avgorf_hhp +=totalsurfaceloss_avgorf_hhp
    total_hhp=total_pf_avgorf_hhp+pb_hhp
    bhhp_hhp = pb_hhp*avg_orf_hhp/1714
    hsi_hhp = bhhp_hhp/(pi/4*hole_size**2)
    impact_forces_hhp = 0.01823*cd_value*avg_orf_hhp*sqrt(mud_weight*pb_hhp)
  
    all_max_pressureloss=[]
    all_max_hsi=[]
    all_max_IF=[]
  
    allmax_flowrate=[]

    alldata['opt_flowrate']=round(avg_orf_if) if(optimization_code=='Impact Force') else round(avg_orf_hhp)

    alldata['impact_force']=round(impact_forces_if) if(optimization_code=='Impact Force') else round(impact_forces_hhp)
    allmax_flowrate.append(alldata['opt_flowrate'])
    allmax_flowrate.append(max_flowrate)
    maximum_flowrate=round(max(allmax_flowrate))
    alldata['min_flowrate_chart']=min_flowrate-50
    alldata['max_flowrate_chart']=maximum_flowrate+50
    all_max_pressureloss.append(maximum_pressure)
    maximum_pressureloss=round(max(all_max_pressureloss))
    alldata['maxlimit']=max_flowrate+100
    alldata['minlimit']=min_flowrate-100
    alldata['max_pressureloss']=maximum_pressureloss+100

    if(optimization_code=='Impact Force'):
        if(avg_orf_if<=max_flowrate and avg_orf_if>=min_flowrate):
            final_opt_flowrate=avg_orf_if
            method='avg_orf_if'
        else:
            if(avg_orf_if<min_flowrate):
                final_opt_flowrate=min_flowrate
                method='min'
              
            else:
                final_opt_flowrate=max_flowrate
                method='max'      
    else:
        if(avg_orf_hhp<=max_flowrate and avg_orf_hhp>=min_flowrate):
            final_opt_flowrate=avg_orf_hhp
            method='avg_orf_hhp'
           
        else:
            if(avg_orf_hhp<min_flowrate):
                final_opt_flowrate=min_flowrate
                method='min'
               
            else:
                final_opt_flowrate=max_flowrate
                method='max'
               
    alldata['final_opt_flowrate']=round(final_opt_flowrate)
    getdata = [data for data in alloptimization if data['flowrate'] == final_opt_flowrate]
    if(len(getdata) != 0):
        bitpressure= getdata[0]['pressurelossbit_impactforce'] if optimization_code=='Impact Force' else getdata[0]['pressurelossbit_hhp']
       
    elif(final_opt_flowrate>max_flowrate):
        alloptimization_count=len(alloptimization)
        bitpressure= alloptimization[alloptimization_count-1]['pressurelossbit_impactforce'] if optimization_code=='Impact Force' else alloptimization[alloptimization_count-1]['pressurelossbit_hhp']
    else:
        mod=final_opt_flowrate%5
        final_opt_flowrate=final_opt_flowrate-mod
        getdata = [data for data in alloptimization if data['flowrate'] == flowrate]
        bitpressure= getdata[0]['pressurelossbit_impactforce'] if optimization_code=='Impact Force' else getdata[0]['pressurelossbit_hhp']

    # print(f"bitpressure {bitpressure}")
    if(typename=='increased'):
        final_tfa=float(request.GET['increased_tfa'])
    else:
        final_tfa=sqrt(mud_weight*final_opt_flowrate**2/(0.95**2*bitpressure*12042))
    
    pb=mud_weight*final_opt_flowrate**2/(12042*cd_value**2*final_tfa**2)
    bhhp = pb*final_opt_flowrate/1714
    final_hsi = bhhp/(pi/4*hole_size**2)
    final_impact_forces = 0.01823*cd_value*final_opt_flowrate*sqrt(mud_weight*pb)

    alldata['final_tfa']=round(final_tfa,2)

    bitpressure_chartdata=[]
    original_bitpressure_chartdata=[]
    totalpressure_chartdata=[]
    original_totalpressure_chartdata=[]
    impactforce_chartdata=[]
    original_impactforce_chartdata=[]
    hsi_chartdata=[]
    original_hsi_chartdata=[]

    # print(f"alloptimization {alloptimization}")
    for data in alloptimization:
        # print(f"data['flowrate'] {data['flowrate']}")
        bit_pressure_loss = mud_weight*data['flowrate']**2/(12042*cd_value**2*final_tfa**2)
        # print(f"bit_pressure_loss {bit_pressure_loss}")
        bhhp = bit_pressure_loss*data['flowrate']/1714
        original_bhhp=data['totalbit']*data['flowrate']/1714
        # print(f"original_bhhp {original_bhhp}")
        original_hsi=original_bhhp/(pi/4*hole_size**2)
        # print(f"bhhp {bhhp}")
        hsi = bhhp/(pi/4*hole_size**2)
        impact_forces = 0.01823*cd_value*data['flowrate']*sqrt(mud_weight*bit_pressure_loss)
        original_impact_forces = 0.01823*cd_value*data['flowrate']*sqrt(mud_weight*data['totalbit'])
        original_impactforce_chartdata.append({'x':data['flowrate'],'y':round(original_impact_forces)})
        original_hsi_chartdata.append({'x':data['flowrate'],'y':round(original_hsi,2)})


        hsi_chartdata.append({'x':data['flowrate'],'y':round(hsi,2)})
        impactforce_chartdata.append({'x':data['flowrate'],'y':round(impact_forces)})
        bitpressure_chartdata.append({'x':data['flowrate'],'y':round(bit_pressure_loss)})
        original_bitpressure_chartdata.append({'x':data['flowrate'],'y':round(data['totalbit'])})

        totalpressure_chartdata.append({'x':data['flowrate'],'y':round(data['totalpf']+bit_pressure_loss)})
        original_totalpressure_chartdata.append({'x':data['flowrate'],'y':round(data['totalpf']+data['totalbit'])})


    alldata['hsi_chartdata']=hsi_chartdata
    alldata['impactforce_chartdata']=impactforce_chartdata
    alldata['bitpressure_chartdata']=bitpressure_chartdata
    alldata['totalpressure_chartdata']=totalpressure_chartdata
    all_max_hsi.append(hsi_chartdata[-1]['y'])
    all_max_IF.append(impactforce_chartdata[-1]['y'])
    all_max_pressureloss.append(bitpressure_chartdata[-1]['y'])
    all_max_pressureloss.append(totalpressure_chartdata[-1]['y'])
    alldata['original_totalpressure_chartdata']=original_totalpressure_chartdata
    all_max_pressureloss.append(original_totalpressure_chartdata[-1]['y'])
    alldata['original_bitpressure_chartdata']=original_bitpressure_chartdata
    all_max_pressureloss.append(original_bitpressure_chartdata[-1]['y'])
    alldata['original_hsi_chartdata']=original_hsi_chartdata
    all_max_hsi.append(original_hsi_chartdata[-1]['y'])
    maximum_hsi=round(max(all_max_hsi))
    alldata['original_impactforce_chartdata']=original_impactforce_chartdata
    all_max_IF.append(original_impactforce_chartdata[-1]['y'])
    max_IF=round(max(all_max_IF))
    alldata['maximum_hsi']=maximum_hsi+10
    alldata['max_IF']=max_IF+100

    alldata['final_hsi']=round(final_hsi)
    alldata['final_impact_forces']=round(final_impact_forces)

    optimum_result=calculate_optimum_nozzle_size(no_of_nozzle,final_tfa)
    if(optimum_result['optimum_nozzle_size'] !=''):
        values, counts = np.unique(optimum_result['optimum_nozzle_size'], return_counts=True)
        # dict(zip(unique, counts))
        final_nozzle_list=[]
        optimum_nozzle_size_dict=dict(zip(values, counts))
        [[final_nozzle_list.append({'nozzle_size':str(k),'countt':str(v)})] for k,v in optimum_nozzle_size_dict.items()]
    else:
        final_nozzle_list=[]

    alldata['final_optimum_nozzle_size']=final_nozzle_list
    alldata['calculated_nozzle_count']=len(optimum_result['optimum_nozzle_size'])

    #calculate pressureloss for minimum flowrate
    pb_minflowrate=muddata.mud_weight*min_flowrate**2/(12042*cd_value**2*final_tfa**2)
    pressureloss_minflowrate=calculateapldrillstring(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,min_flowrate,rpm,hole_size,viscocity,torque,wob,muddata,'calculateoptimization')
    totalpf_minflowrate =pressureloss_minflowrate["totaldrillstring_loss"]+pressureloss_minflowrate["totalannular_pressureloss"]
    surface_losses_minflowrate=getsurfacelosses(rpm,min_flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity,'calculateallpressureloss')
    totalsurfaceloss_minflowrate=0
    for surface in surface_losses_minflowrate:
        totalsurfaceloss_minflowrate +=surface["pressureloss"]
    totalpf_minflowrate +=totalsurfaceloss_minflowrate
    totalpb_minflowrate=totalpf_minflowrate+pb_minflowrate

    #calculate pressureloss for maximum flowrate
    pb_maxflowrate=muddata.mud_weight*max_flowrate**2/(12042*cd_value**2*final_tfa**2)
    pressureloss_maxflowrate=calculateapldrillstring(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,max_flowrate,rpm,hole_size,viscocity,torque,wob,muddata,'calculateoptimization')
    totalpf_maxflowrate =pressureloss_maxflowrate["totaldrillstring_loss"]+pressureloss_maxflowrate["totalannular_pressureloss"]
    surface_losses_maxflowrate=getsurfacelosses(rpm,max_flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity,'calculateallpressureloss')
    totalsurfaceloss_maxflowrate=0
    for surface in surface_losses_maxflowrate:
        totalsurfaceloss_maxflowrate +=surface["pressureloss"]
    totalpf_maxflowrate +=totalsurfaceloss_minflowrate
    totalpb_maxflowrate=totalpf_maxflowrate+pb_maxflowrate


    if(method=='avg_orf_if'):
        final_pump_pressure=total_if
    elif(method=='avg_orf_hhp'):
        final_pump_pressure=total_hhp
    elif(method=='min'):
        final_pump_pressure=totalpb_minflowrate
    elif(method=='max'):
        final_pump_pressure=totalpb_maxflowrate
   


    alldata['final_pump_pressure']=round(final_pump_pressure)
    alldata['surface_rating']=surfacepipe.rating

    opt_flowrate_pressureloss=calculateapldrillstring(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,alldata['final_opt_flowrate'],rpm,hole_size,viscocity,torque,wob,muddata,'calculateoptimization')
    total_optimum_flowrate_pressure = opt_flowrate_pressureloss["totaldrillstring_loss"]+opt_flowrate_pressureloss["totalannular_pressureloss"]
    surface_losses=getsurfacelosses(rpm,alldata['final_opt_flowrate'],wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity,'calculateallpressureloss')
    totalsurfaceloss=0
    for surface in surface_losses:
        totalsurfaceloss +=surface["pressureloss"]
    total_optimum_flowrate_pressure +=totalsurfaceloss
    bit_losses=getbitpressureloss_optimization(rpm,alldata['final_opt_flowrate'],wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,original_tfa)
    # print(f"bit_losses {bit_losses}")
    total_optimum_flowrate_pressure +=bit_losses[0]["bit_pressure_loss"]

    optimum_flowrate_bhhp = bit_losses[0]["bit_pressure_loss"]*alldata['final_opt_flowrate']/1714
    # print(f"optimum_flowrate_bhhp {optimum_flowrate_bhhp}")
    optimum_flowrate_hsi=optimum_flowrate_bhhp/(pi/4*hole_size**2)
    optimum_flowrate_impact_forces = 0.01823*cd_value*alldata['final_opt_flowrate']*sqrt(mud_weight*bit_losses[0]["bit_pressure_loss"])

    alldata["total_optimum_flowrate_pressure"]=total_optimum_flowrate_pressure
    alldata["optimum_flowrate_pressure"]=total_optimum_flowrate_pressure-bit_losses[0]["bit_pressure_loss"]

    alldata["optimum_flowrate_bit"]=bit_losses[0]["bit_pressure_loss"]
    alldata["optimum_flowrate_hsi"]=optimum_flowrate_hsi
    alldata["optimum_flowrate_impact_forces"]=optimum_flowrate_impact_forces

    alldata['nozzle_size']=no_of_nozzle

    # print(f"original_tfa {original_tfa}")

    # print(f"bit_losses {bit_losses[0]['bit_pressure_loss']}")


    # print(f"optimum_flowrate_impact_forces {optimum_flowrate_impact_forces}")

    # print(f"optimum_flowrate_hsi {optimum_flowrate_hsi}")

    # print(f"total_optimum_flowrate_pressure {total_optimum_flowrate_pressure}")


    

    return JsonResponse(alldata,safe=False)

def calculateapldrillstring(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,muddata,typename):
    previousbhaelement=BhaElement.objects.filter(bhadata_id=bhadata.id,status=1).exclude(type_name='Bit').order_by('-id')
    bhacount=previousbhaelement.count()
    i=bhacount
    totalannular_pressureloss=0
    totalincreasedannular_pressureloss=0
    totaldrillstring_loss=0
    allpressureloss=[]
    increased_pressureloss=[]
    previous_length_against_casing=[]
    well_id = bhadata.well_id
    for previousbha in previousbhaelement:
        # print(f"typename {previousbha.type_name}")
        if(previousbha.length_onejoint<sectiontodepth):
            newlength=converttofloat(previousbha.length)
        else:
            belowbha=BhaElement.objects.filter(bhadata_id=bhadata.id,id__lt=previousbha.id).order_by('-id').first()
            newlength=sectiontodepth-belowbha.length_onejoint
        od_of_pipe_element=previousbha.od
        if(i==bhacount):
            length_against_casing=length_of_previous_casing_from_surface if(converttofloat(newlength)>=length_of_previous_casing_from_surface) else newlength
            previous_length_against_casing.append(length_against_casing)
        else:
            sum_of_previous_against_casing=Sum = sum(previous_length_against_casing)
            if(sum_of_previous_against_casing==length_of_previous_casing_from_surface):
                length_against_casing=0
            if((sum_of_previous_against_casing<length_of_previous_casing_from_surface) and (sum_of_previous_against_casing+newlength<length_of_previous_casing_from_surface)):
                length_against_casing=newlength
            else:
                length_against_casing=length_of_previous_casing_from_surface-sum_of_previous_against_casing
            previous_length_against_casing.append(length_against_casing)
        length_against_open_hole=converttofloat(newlength)-length_against_casing
        # print(f"length_against_open_hole {length_against_open_hole}")
        # print(f"length_against_casing {length_against_casing}")

        if(length_against_casing!=0):
            pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,previousbha.od,id_of_previous_casing,length_against_casing,typename)
            # print(f"pressurelosscasing {pressureloss}")
            
            if((previousbha.type_name=='RSS') or (previousbha.type_name=='MWD') or (previousbha.type_name=='LWD') or (previousbha.type_name=='Others') or (previousbha.type_name=='Mud Motor')):
                drillstringpressureloss=calculate_drillstringloss_downholetools(previousbha,flowrate,mud_weight,torque,wob)
            else:
                drillstringpressureloss=calculatepressloss(well_id,rpm,flowrate,mud_weight,previousbha.identity,length_against_casing,viscocity,'checkvalue')

         
        
            if((previousbha.type_name=='Drill Pipe') or (previousbha.type_name=='Heavy Weight Drill Pipe')):
                calculate_tj_pressureloss=calculatetjpressureloss(previousbha.length,length_against_casing,previousbha,rpm,flowrate,viscocity,mud_weight,id_of_previous_casing,'without')
            else:
                calculate_tj_pressureloss=calculatetjpressure(previousbha.length,length_against_casing,previousbha,rpm,flowrate,viscocity,muddata.mud_weight,id_of_previous_casing,'without')
                # calculate_tj_pressureloss_increased=calculatetjpressure(previousbha.length,length_against_casing,previousbha,rpm,flowrate,viscocity,increased_mudweight["increased_mudweight"],id_of_previous_casing,'with')   
            allpressureloss.append({
                'flowregime' : pressureloss["flowregime"],
                'od':round(converttofloat(od_of_pipe_element),2),
                'id':round(converttofloat(previousbha.identity),2),
                'type':previousbha.type_name,
                'length_against':length_against_casing,
                'pressureloss':round(pressureloss["pressureloss"]+calculate_tj_pressureloss["tjannularloss"],2),
                'element_type':'CH',
                'drillstringloss':round(drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"],2)  if 'pressureloss' in drillstringpressureloss else drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"],
                'mudweight':mud_weight,
                'cased_hole_size':id_of_previous_casing

            })
            totalannular_pressureloss +=pressureloss["pressureloss"]+calculate_tj_pressureloss["tjannularloss"]
            if 'pressureloss' in drillstringpressureloss:
                totaldrillstring_loss += drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"]
            else:
                totaldrillstring_loss +=drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"]

        if(length_against_open_hole!=0):
            pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,previousbha.od,hole_size,length_against_open_hole,'annularpressurelosscheck') 
            # print(f"pressurelossopenhole {pressureloss}")

            if((previousbha.type_name=='RSS') or (previousbha.type_name=='MWD') or (previousbha.type_name=='LWD') or (previousbha.type_name=='Others') or (previousbha.type_name=='Mud Motor')):
                drillstringpressureloss=calculate_drillstringloss_downholetools(previousbha,flowrate,mud_weight,torque,wob)
                # print(f"drillstringpressureloss {drillstringpressureloss}")
            else:
                drillstringpressureloss=calculatepressloss(well_id,rpm,flowrate,mud_weight,previousbha.identity,length_against_open_hole,viscocity,'calculateapldrillstring_withoutanychart')


            
            if((previousbha.type_name=='Drill Pipe') or (previousbha.type_name=='Heavy Weight Drill Pipe')):
                calculate_tj_pressureloss=calculatetjpressureloss(previousbha.length,length_against_open_hole,previousbha,rpm,flowrate,viscocity,mud_weight,hole_size,'without')
            else:
                calculate_tj_pressureloss=calculatetjpressure(previousbha.length,length_against_casing,previousbha,rpm,flowrate,viscocity,muddata.mud_weight,id_of_previous_casing,'without')
                # calculate_tj_pressureloss_increased=calculatetjpressure(previousbha.length,length_against_casing,previousbha,rpm,flowrate,viscocity,increased_mudweight["increased_mudweight"],id_of_previous_casing,'with')  
            allpressureloss.append({
                'flowregime' : pressureloss["flowregime"],
                'od':round(converttofloat(od_of_pipe_element),2),
                'id':round(converttofloat(previousbha.identity),2),
                'type':previousbha.type_name,
                'length_against':length_against_open_hole,
                'pressureloss':round(pressureloss["pressureloss"]+calculate_tj_pressureloss["tjannularloss"],2),
                'element_type':'OH',
                'drillstringloss':round(drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"],2)  if 'pressureloss' in drillstringpressureloss else drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"],
                'mudweight':mud_weight,
                'cased_hole_size':hole_size

            })
            
            totalannular_pressureloss +=pressureloss["pressureloss"]+calculate_tj_pressureloss["tjannularloss"]
            if 'pressureloss' in drillstringpressureloss:
                totaldrillstring_loss += drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"]
            else:
                totaldrillstring_loss +=drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"]

        
        previouselement_length=previousbha.length_onejoint
        i -=1
    data={
        'totaldrillstring_loss':totaldrillstring_loss,
        'totalannular_pressureloss':totalannular_pressureloss,
        'allpressureloss':allpressureloss,
    }
    return data

def getbitpressureloss_optimization(rpm,flowrate,wellphase_id,section_name,mudweight,wellphase,previous_wellphase,well_id,tfa_value):
    drillbit = DrillBit.objects.filter(well_id=well_id,well_phases_id=wellphase_id,status=1).first()
    bittype = BitTypesNames.objects.get(id=drillbit.bit_type_id)
    nozzle_size = DrillBitNozzle.objects.filter(drillbit_id=drillbit,well_id=well_id,status=1)
    unit = getprojectunit(well_id)
    if(drillbit.external_nozzle == 1):
        cd_values = 0.95
    else:
        cd_values = bittype.bit_values

    # flowrate = convertflowrate(flowrate,unit)
    # mudweight = mudweight_conversion(mudweight,unit)
    hole_size = wellphase.hole_size
    # print(f"flowrate {flowrate}")
    # print(f"mudweight {mudweight}")

    bit_pressure_loss = mudweight*flowrate**2/(12042*cd_values**2*tfa_value**2)
    # print(f"bit_pressure_loss {bit_pressure_loss}")
    bhhp = bit_pressure_loss*500/1714
    hsi = bhhp/(pi/4*hole_size**2)
    impact_forces = 0.01823*cd_values*flowrate*sqrt(mudweight*bit_pressure_loss)
    jet_velocity = 0.32086*flowrate/tfa_value
    data=[]
    nozzles=[]
    for nozzle in nozzle_size:
        nozzles.append(nozzle.nozzle_size)
    data.append({
        'nozzle_size':nozzles,
        'tfa_value':tfa_value,
        'bit_pressure_loss':bit_pressure_loss,
        'bhhp':bhhp,
        'hsi':hsi,
        'impact_forces':impact_forces,
        'jet_velocity':jet_velocity,
        'cd_values':cd_values
    })
    return data

def calculate_optimum_nozzle_size(no_of_nozzle,Opt_TFA):
    N_n=no_of_nozzle
    N=[]
    TFA=[]
    for i in range(10,33):
        N.append(i)
        TFA.append(np.round(pi/4*(i/32)**2,2))
    TFA_n = np.round(np.multiply(TFA,N_n),2)


    if Opt_TFA<=TFA_n[len(TFA_n)-1] and Opt_TFA>=TFA_n[0]:
        TFA_min=TFA_n[np.where(TFA_n<Opt_TFA)[-1][-1]]
        N_min=N[np.where(TFA_n<Opt_TFA)[-1][-1]]
        TFA_max=TFA_n[np.where(TFA_n>Opt_TFA)[0][0]]
        N_max=N[np.where(TFA_n>Opt_TFA)[0][0]]

    elif Opt_TFA<TFA_n[0]:
        for i in range(N_n-1,0,-1):
            TFA_ni = np.round(np.multiply(TFA,i),2)
            
            if Opt_TFA<=TFA_ni[len(TFA_ni)-1] and Opt_TFA>=TFA_ni[0]:
                TFA_min=TFA_ni[np.where(TFA_ni<Opt_TFA)[-1][-1]]
                N_min=N[np.where(TFA_ni<Opt_TFA)[-1][-1]]
                TFA_max=TFA_ni[np.where(TFA_ni>Opt_TFA)[0][0]]
                N_max=N[np.where(TFA_ni>Opt_TFA)[0][0]]
                N_n=i
                break
    else:
        for i in range(N_n,33,1):
            TFA_ni = np.round(np.multiply(TFA,i),2)
            
            if Opt_TFA<=TFA_ni[len(TFA_ni)-1] and Opt_TFA>=TFA_ni[0]:
                TFA_min=TFA_ni[np.where(TFA_ni<Opt_TFA)[-1][-1]]
                N_min=N[np.where(TFA_ni<Opt_TFA)[-1][-1]]
                TFA_max=TFA_ni[np.where(TFA_ni>Opt_TFA)[0][0]]
                N_max=N[np.where(TFA_ni>Opt_TFA)[0][0]]
                N_n=i
                break


    N_i=np.repeat(N_min,N_n)
    Opt_N=''

    i=1
    for i in range(len(N_i)):
        N_i[i]=N_i[i]+1
        TFA_i=np.pi/4*(np.sum(np.square(N_i/32)))

        if TFA_i>Opt_TFA or TFA_i==Opt_TFA:
            Opt_N=N_i
            break
    

    data={
        'optimum_nozzle_size':Opt_N,
        'optimum_tfa':round(TFA_i,3)
    }
    return data



