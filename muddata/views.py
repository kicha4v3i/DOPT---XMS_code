from urllib import response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from muddata.models import MudData,Rheogram,RheogramNameModels,RheogramDate,MudType,Sections,RheogramSections,HydraulicData,Planwell_data,Pressureloss_data
from bhadata.models import BhaData,BhaElement,Drillcollers,Drillpipe,DrillpipeHWDP
from mud.models import MudPumpFlowRate,MudPumpData,MudPump

from surfacepipe.models import SurfacePipe,SurfacePipeData
from wells.models import Wells
from wellphases.models import WellPhases
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MudDataForm,RheogramForm,RheogramdateForm
from django.views.generic import ListView, DetailView, DeleteView
from django.forms import formset_factory
from django.http import JsonResponse,HttpResponse
from django.core import serializers
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit,fsolve
import math
from math import pi,sqrt,pow,log10,log,acos,sin,cos,tan
from django.db.models import Q
from django.db.models import Sum
from scipy.optimize import newton,root_scalar
from scipy import interpolate
import json
from custom_auth.getunit import getprojectunit,adduserlog,converttofloat,getmodaltext,getcountries
from drillbitdata.models import DrillBit,DrillBitNozzle,BitTypesNames
from welltrajectory.models import WellTrajectory
from bhadata.models import BhaData,BhaElement,Drillcollers,Drillpipe,DrillpipeHWDP,Specifications,Pressuredroptool,Empirical,Differential_pressure
from custom_auth.getunit import getmd,getcountries
from django.db.models import Count, Min, Sum, Avg , Max
import warnings
warnings.filterwarnings('ignore', 'The iteration is not making good progress')
warnings.filterwarnings('ignore', 'divide by zero encountered in true_divide')
from helpers import *
from helpers.unit_calculation import *
import datetime
from dateutil import parser
from django.db.models.functions import TruncDate,TruncMonth
from django.db.models.functions import ExtractMonth
import pandas as pd
from tablib import Dataset
from projects.templatetags import app_filters
from django.core.paginator import Paginator
# from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from easy_pdf.rendering import render_to_pdf_response
import base64
from PIL import Image
import io
from django.templatetags.static import static  
from django.middleware.csrf import get_token
from django.contrib import messages

# Create your views here.
class IndexView(ListView):
    template_name = 'muddata/list.html'
    context_object_name = 'muddata'


def create(request,wellphase_id):
    well_id=request.session['well_id']
    request.session['wellphasetab']=wellphase_id
    well = Wells.objects.get(id=well_id)
    project_id = well.project_id
    currentwellphase=WellPhases.objects.filter(id=wellphase_id).values('measured_depth','id','well_id').first()
    previouswellphase=WellPhases.objects.filter(id__lt=currentwellphase['id']).filter(well_id=currentwellphase['well_id']).order_by("-id").values('measured_depth','id')[:1]
    fromdepth=0 if previouswellphase.count()==0 else previouswellphase[0]['measured_depth']
    todepth= currentwellphase['measured_depth']
    welltype = well.well_type
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    mudtype=MudType.objects.all()
    if request.method == 'POST':
        # print(f"post {request.POST}")
        section=request.POST.getlist('section')
        from_depth=request.POST.getlist('from_depth')
        to_depth=request.POST.getlist('to_depth')
        mud_weight=request.POST.getlist('mud_weight')
        mudtype=request.POST.getlist('mudtype')
        plastic_viscosity=request.POST.getlist('plastic_viscosity')
        yield_point=request.POST.getlist('yield_point')
        low_shear_rate=request.POST.getlist('low_shear_rate')
        gel_strength_0sec=request.POST.getlist('gel_strength_0sec')
        gel_strength_10min=request.POST.getlist('gel_strength_10min')
        gel_strength_30min=request.POST.getlist('gel_strength_30min')
        # muddata_date=request.POST.getlist('muddata_date')
        # muddata_time=request.POST.getlist('muddata_time')
        depth=request.POST.getlist('depth')
        rpm_parameter=request.POST.getlist('rpm_parameter')
        allmuddata={}

        for rpmdata in rpm_parameter:
            allmuddata[rpmdata]=request.POST.getlist('dial_'+str(rpmdata))
        
        # print(f"allmuddata {allmuddata}")
            

        i=0
        muddata_ids = []
        while i < len(mud_weight):
            gel_strength_0sec_data=gel_strength_0sec[i] if(gel_strength_0sec[i]!='') else None  
            gel_strength_10min_data=gel_strength_10min[i] if(gel_strength_10min[i]!='') else None    
            gel_strength_30min_data=gel_strength_30min[i] if(gel_strength_30min[i]!='') else None 
            plastic_viscosity_data=plastic_viscosity[i] if(plastic_viscosity[i]!='') else None 
            yield_point_data=yield_point[i] if(yield_point[i]!='') else None 
            low_shear_rate_data=low_shear_rate[i] if(low_shear_rate[i]!='') else None 
            
            if(request.session['welltype']=='PLAN'):
                if(from_depth[i]!='' and to_depth[i]!=''):
                    Sections.objects.create(section_name=section[i],company=request.company,well_phase_id=wellphase_id,well_id=well_id,from_depth=from_depth[i],todepth=to_depth[i])
                    muddata_create = MudData.objects.create(section=section[i],from_depth=from_depth[i],todepth=to_depth[i],well_id=well_id,company=request.company,mud_weight=mud_weight[i],mudtype_id=mudtype[i],plastic_viscosity=plastic_viscosity_data,yield_point=yield_point_data,low_shear_rate=low_shear_rate_data,gel_strength_0sec=gel_strength_0sec_data,gel_strength_10min=gel_strength_10min_data,gel_strength_30min=gel_strength_30min_data,well_phase_id=wellphase_id)
                    muddata_ids.append(muddata_create.id)
            else:
                if(depth[i]):
                    # timestamp=dateconversion(muddata_date[i],muddata_time[i])
                    Sections.objects.create(company=request.company,well_phase_id=wellphase_id,well_id=well_id,todepth=depth[i])
                    muddata_create=MudData.objects.create(todepth=depth[i],well_id=well_id,company=request.company,mud_weight=mud_weight[i],mudtype_id=mudtype[i],plastic_viscosity=plastic_viscosity_data,yield_point=yield_point_data,low_shear_rate=low_shear_rate_data,gel_strength_0sec=gel_strength_0sec_data,gel_strength_10min=gel_strength_10min_data,gel_strength_30min=gel_strength_30min_data,well_phase_id=wellphase_id)
                    muddata_ids.append(muddata_create.id)
                    rheogram_date = RheogramDate.objects.create(company=request.company,well_id=well_id,well_phase_id=wellphase_id,status=1,muddata_id=muddata_create.id)
       
                    for rpmdata in rpm_parameter:
                        if(allmuddata[rpmdata][i]):
                            Rheogram.objects.create(rpm=rpmdata,dial=allmuddata[rpmdata][i],rheogram_date_id=rheogram_date.id,well_id=well_id,company=request.company)
            i += 1
        source_id=muddata_ids
        userlog=adduserlog('Mud Data Created',request,source_id,'Mud Data',request.user.licence_type,project_id,well_id,wellphase_id,'create')
        return redirect('muddata:muddatarheogramlist', wellphase_id=wellphase_id)
    form = MudDataForm()
    return render(request,'muddata/muddatarheogramlist.html',{'form': form,'well_id':well_id,'welltype':welltype,'wellphases':wellphase,'mudtype':mudtype,'wellphase_id':wellphase_id,'fromdepth':fromdepth,'todepth':todepth})


def list(request,wellphase_id):
    # wellphase_id=request.session['wells']
    request.session['wellphasetab']=wellphase_id
    wellphasebyid = WellPhases.objects.filter(id=wellphase_id).first()
    well_id=wellphasebyid.well_id
    data = MudData.objects.filter(company=request.company,well_id=well_id,well_phase_id=wellphase_id,status=1)
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    request.session['submenu']='muddata'
    well = Wells.objects.get(id=well_id)
    welltype = well.well_type
    if(len(data) == 0):
        return redirect('muddata:muddatarheogramlist',wellphase_id=wellphase_id)
    return render(request,'muddata/list.html',{'data':data,'well_id':well_id,'welltype':welltype,'wellphases':wellphase,'wellphase_id':wellphase_id})


def edit(request,well_phase_id,template_name='muddata/edit.html',queryset=None):
    request.session['submenu']='muddata'
    form = MudData.objects.filter(well_phase_id=well_phase_id,status=1).values()
    well_id=form[0]['well_id']
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    sections = Sections.objects.filter(well_id=well_id, company=request.company,well_phase_id=well_phase_id,status=1)
    well = Wells.objects.get(id=well_id)
    welltype = well.well_type
    mudtype=MudType.objects.all()
    currentwellphase=WellPhases.objects.filter(id=well_phase_id).values('measured_depth','id','well_id').first()
    previouswellphase=WellPhases.objects.filter(id__lt=currentwellphase['id']).filter(well_id=currentwellphase['well_id']).order_by("-id").values('measured_depth','id')[:1]
    fromdepth=0 if previouswellphase.count()==0 else previouswellphase[0]['measured_depth']
    todepth= currentwellphase['measured_depth']
    rheogram_date=RheogramDate.objects.filter(company=request.company,well_phase_id=well_phase_id,status=1)
    rheogram_id=[]
    for date in rheogram_date:
        rheogram_id.append(date.id)
    rheogram=Rheogram.objects.filter(rheogram_date_id__in=rheogram_id,status=1).values('rpm').distinct()

    # print(f"rheogram_dateount {rheogram_date.count()}")
    if request.method == 'POST':
        section=request.POST.getlist('section')
        from_depth=request.POST.getlist('from_depth')
        to_depth=request.POST.getlist('to_depth')
        mud_weight=request.POST.getlist('mud_weight')
        mudtype=request.POST.getlist('mudtype')
        plastic_viscosity=request.POST.getlist('plastic_viscosity')
        yield_point=request.POST.getlist('yield_point')
        low_shear_rate=request.POST.getlist('low_shear_rate')
        gel_strength_0sec=request.POST.getlist('gel_strength_0sec')
        gel_strength_10min=request.POST.getlist('gel_strength_10min')
        gel_strength_30min=request.POST.getlist('gel_strength_30min')
        muddata_id=request.POST.getlist('muddata_id')
        selected_model=request.POST.getlist('selected_model')
        section_id=request.POST.getlist('section_id')  
        rpm_parameter=request.POST.getlist('rpm_parameter')
        
        i=0
        currentsectionid=[]
        currentmuddataid=[]
        currentrheoid=[] 
        
        if(request.session['welltype']=='PLAN'):
            while i < len(from_depth):
                if(from_depth[i]):     
                    gel_strength_0sec_data=gel_strength_0sec[i] if(gel_strength_0sec[i]!='') else None  
                    gel_strength_10min_data=gel_strength_10min[i] if(gel_strength_10min[i]!='') else None    
                    gel_strength_30min_data=gel_strength_30min[i] if(gel_strength_30min[i]!='') else None 
                    plastic_viscosity_data=plastic_viscosity[i] if(plastic_viscosity[i]!='') else None 
                    yield_point_data=yield_point[i] if(yield_point[i]!='') else None 
                    low_shear_rate_data=low_shear_rate[i] if(low_shear_rate[i]!='') else None
                    sectionsdata=Sections.objects.filter(section_name=section[i],well_phase_id=well_phase_id,status=1).values()
                    if(rheogram_date.count()>0):
                        rheo_section=RheogramSections.objects.filter(rheogram_date_id=rheogram_date[0].id,status=1).values('id')                    
                        for j in range(len(rheo_section)):
                            if(to_depth[i]!='' and from_depth[i]!=''):
                                RheogramSections.objects.filter(id=rheo_section[j]['id']).update(section_name=section[j],from_depth=from_depth[j],todepth=to_depth[j],well_phase_id=well_phase_id,rheogram_date_id=rheogram_date[0].id)
                    if(sectionsdata.count()==0):
                        if(from_depth[i]!='' and to_depth[i]!=''):
                            if(section_id[i]):
                                Sections.objects.filter(id=section_id[i]).update(section_name=section[i],from_depth=from_depth[i],todepth=to_depth[i])
                                currentsectionid.append(section_id[i])
                            else:
                                Sections.objects.create(section_name=section[i],company=request.company,well_phase_id=well_phase_id,well_id=well_id,from_depth=from_depth[i],todepth=to_depth[i])
                                sectionid=Sections.objects.values('id').last()
                                currentsectionid.append(sectionid['id'])
                    elif(from_depth[i]!='' and to_depth[i]!=''):
                        Sections.objects.filter(id=sectionsdata[0]['id']).update(section_name=section[i],from_depth=from_depth[i],todepth=to_depth[i])
                        currentsectionid.append(sectionsdata[0]['id'])
                    if(muddata_id[i]):
                        currentmuddataid.append(muddata_id[i])
                        muddata = MudData.objects.filter(id=muddata_id[i]).update(section=section[i],from_depth=from_depth[i],todepth=to_depth[i],mud_weight=mud_weight[i],mudtype_id=mudtype[i],plastic_viscosity=plastic_viscosity_data,yield_point=yield_point_data,low_shear_rate=low_shear_rate_data,gel_strength_0sec=gel_strength_0sec_data,gel_strength_10min=gel_strength_10min_data,gel_strength_30min=gel_strength_30min_data)
                      
                    elif(from_depth[i]!='' and mud_weight[i]!=''):
                        MudData.objects.create(section=section[i],from_depth=from_depth[i],todepth=to_depth[i],well_id=well_id,company=request.company,mud_weight=mud_weight[i],mudtype_id=mudtype[i],plastic_viscosity=plastic_viscosity_data,yield_point=yield_point_data,low_shear_rate=low_shear_rate_data,gel_strength_0sec=gel_strength_0sec_data,gel_strength_10min=gel_strength_10min_data,gel_strength_30min=gel_strength_30min_data,well_phase_id=well_phase_id
                        )
                        muddataid=MudData.objects.values('id').last()
                        currentmuddataid.append(muddataid['id'])
                i += 1
        else:
            # muddata_date=request.POST.getlist('muddata_date')
            # muddata_time=request.POST.getlist('muddata_time')  
            depth=request.POST.getlist('depth') 
           
            i=0
            while i < len(depth):
                if(depth[i]):
                    gel_strength_0sec_data=gel_strength_0sec[i] if(gel_strength_0sec[i]!='') else None  
                    gel_strength_10min_data=gel_strength_10min[i] if(gel_strength_10min[i]!='') else None    
                    gel_strength_30min_data=gel_strength_30min[i] if(gel_strength_30min[i]!='') else None 
                    plastic_viscosity_data=plastic_viscosity[i] if(plastic_viscosity[i]!='') else None 
                    yield_point_data=yield_point[i] if(yield_point[i]!='') else None 
                    low_shear_rate_data=low_shear_rate[i] if(low_shear_rate[i]!='') else None
                    # timestamp=dateconversion(muddata_date[i],muddata_time[i])
                    if(muddata_id[i]):
                        currentmuddataid.append(muddata_id[i])
                        MudData.objects.filter(id=muddata_id[i]).update(todepth=depth[i],mud_weight=mud_weight[i],mudtype_id=mudtype[i],plastic_viscosity=plastic_viscosity_data,yield_point=yield_point_data,low_shear_rate=low_shear_rate_data,gel_strength_0sec=gel_strength_0sec_data,gel_strength_10min=gel_strength_10min_data,gel_strength_30min=gel_strength_30min_data)
                        RheogramDate.objects.filter(muddata_id=muddata_id[i])
                        rheo_id= RheogramDate.objects.filter(muddata_id=muddata_id[i]).first()
                        rheo_id=rheo_id.id
                        currentrheoid.append(rheo_id)
                    else:
                        muddata_create=MudData.objects.create(todepth=depth[i],well_id=well_id,company=request.company,mud_weight=mud_weight[i],mudtype_id=mudtype[i],plastic_viscosity=plastic_viscosity_data,yield_point=yield_point_data,low_shear_rate=low_shear_rate_data,gel_strength_0sec=gel_strength_0sec_data,gel_strength_10min=gel_strength_10min_data,gel_strength_30min=gel_strength_30min_data,well_phase_id=well_phase_id)
                        muddataid=MudData.objects.values('id').last()
                        currentmuddataid.append(muddataid['id'])
                        rheogram_date = RheogramDate.objects.create(company=request.company,well_id=well_id,well_phase_id=well_phase_id,status=1,muddata_id=muddata_create.id)
                        rheo_id=rheogram_date.id
                        currentrheoid.append(rheo_id)


                    if(section_id[i]):
                        Sections.objects.filter(id=section_id[i]).update(todepth=depth[i])
                        currentsectionid.append(section_id[i])
                    else:
                        Sections.objects.create(company=request.company,well_phase_id=well_phase_id,well_id=well_id,todepth=depth[i])
                        sectionid=Sections.objects.values('id').last()
                        currentsectionid.append(sectionid['id'])
                    
                    current_rheogram_id=[]
                    for rpmdata in rpm_parameter:
                        # print(f"rpmdata {rpmdata}")
                        dial=request.POST.getlist('dial_'+str(rpmdata))[i]
                        # print(f"dial {dial}")
                        rheogram_id=request.POST.getlist('rheogram_id_'+str(rpmdata))[i]
                        # print(f"rheogram_id {rheogram_id}")
                        if(rheogram_id):
                            Rheogram.objects.filter(id=rheogram_id).update(rpm=rpmdata,dial=dial)
                            current_rheogram_id.append(rheogram_id)
                        else:
                            rheogram_create=Rheogram.objects.create(rpm=rpmdata,dial=dial,rheogram_date_id=rheo_id,well_id=well_id,company=request.company)
                            current_rheogram_id.append(rheogram_create.id)
                    
                    Rheogram.objects.filter(rheogram_date_id=rheo_id).exclude(id__in=current_rheogram_id).update(status=0)

                i +=1
            
        source_id=currentmuddataid
        userlog=adduserlog('Mud Data Edited',request,source_id,'Mud Data',request.user.licence_type,well.project_id,well_id,well_phase_id,'edit')
        MudData.objects.filter(well_phase_id=well_phase_id).exclude(id__in=currentmuddataid).update(status=0)
        RheogramDate.objects.filter(well_phase_id=well_phase_id).exclude(id__in=currentrheoid).update(status=0)

        Sections.objects.filter(well_phase_id=well_phase_id).exclude(id__in=currentsectionid).update(status=0)
        return redirect('muddata:muddatarheogramlist', wellphase_id=well_phase_id)
    if(request.session['welltype']=='PLAN'):
        return render(request, template_name, {'form':form,'welltype':welltype,'wellphases':wellphase,'mudtype':mudtype,'fromdepth':fromdepth,'todepth':todepth,'sections':sections,'wellphase_id':well_phase_id,'rheogram_date':rheogram_date,'well_id':well_id,'well':well,'countries':getcountries(request.company),'company':request.company,})
    else:
        return render(request, 'muddata/edit_actual.html', {'form':form,'welltype':welltype,'wellphases':wellphase,'mudtype':mudtype,'fromdepth':fromdepth,'todepth':todepth,'sections':sections,'wellphase_id':well_phase_id,'rheogram_date':rheogram_date,'well_id':well_id,'well':well,'countries':getcountries(request.company),'company':request.company,'rheogram':rheogram})

def delete(request, well_phase_id,template_name='crudapp/confirm_delete.html'):
    muddata=MudData.objects.filter(well_phase_id=well_phase_id)
    current_mudids = [muddata.id for muddata in muddata] 

    well_id=muddata[0].well_id
    wellphase_id=muddata[0].well_phase_id
    muddata=MudData.objects.filter(well_phase_id=well_phase_id).update(status=0)
    sections=Sections.objects.filter(well_phase_id=well_phase_id).update(status=0)
    rheogram_sections=RheogramSections.objects.filter(well_phase_id=well_phase_id).update(status=0)
    rheogram_date=RheogramDate.objects.filter(well_phase_id=wellphase_id).update(status=0)
    # muddata.delete()
    well = Wells.objects.get(id=well_id)
    source_id=current_mudids
    userlog=adduserlog('Mud Data Deleted',request,source_id,'Mud Data',request.user.licence_type,well.project_id,well_id,well_phase_id,'delete')

    return redirect('muddata:muddatarheogramlist',wellphase_id=wellphase_id)
    # return render(request, "muddata/delete_confirm.html")

def rheogramcreate_actual(request,wellphase_id):
    well_id=request.session['well_id']
    well = Wells.objects.get(id=well_id)
    request.session['wellphasetab']=wellphase_id
    request.session['submenu']='rheogram'
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    muddata = MudData.objects.filter(well_phase_id=wellphase_id,status=1).values()
    sections = Sections.objects.filter(well_id=well_id, company=request.company,well_phase_id=wellphase_id,status=1)
    rheogram_rpm= RheogramNameModels.objects.all()
    checkrheogram = RheogramDate.objects.filter(well_phase_id=wellphase_id,status=1)

    if request.method == 'POST':
        date=request.POST.getlist('date')
        time=request.POST.getlist('time')
        timestamp=request.POST.getlist('timestamp')
        muddata_id=request.POST.getlist('muddata_id')

        i=0
        while(i<len(date)):
            rheogram_date = RheogramDate.objects.create(company=request.company,well_id=well_id,well_phase_id=wellphase_id,status=1,date=date[i],time=time[i],timestamp=timestamp[i],muddata_id=muddata_id[i])
            rpm=request.POST.getlist('rpm'+str(i))
            dial=request.POST.getlist('dial'+str(i))
            j=0
            while j < len(rpm):
                Rheogram.objects.create(rpm=rpm[j],dial=dial[j],rheogram_date=rheogram_date,well_id=well_id,company=request.company)
                j +=1

            i += 1
        return redirect('muddata:rheogram_actual',wellphase_id=wellphase_id)
    if(checkrheogram.count()==0):
        return render(request,'muddata/rheogramcreate_actual.html',{'well_id':well_id,'wellphases':wellphase,'muddata':muddata,'sections':sections,'wellphase_id':wellphase_id,'rheogram_rpm':rheogram_rpm,'countries':getcountries(request.company),'company':request.company,})
    else:
        return redirect('muddata:rheogram_actual',wellphase_id=wellphase_id)


def rheogram_actual(request,wellphase_id):   
    well_id=request.session['well_id']
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    muddata = MudData.objects.filter(well_phase_id=wellphase_id,status=1).values()


    checkrheogram = RheogramDate.objects.filter(well_phase_id=wellphase_id,status=1)
    return render(request,'muddata/rheogramlist_actual.html',{'well_id':well_id,'wellphases':wellphase,'wellphase_id':wellphase_id,'countries':getcountries(request.company),'company':request.company,'rheogram':checkrheogram,'muddata':muddata})

def rheogramedit_actual(request,wellphase_id):
    well_id=request.session['well_id']
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    sections = Sections.objects.filter(well_id=well_id, company=request.company,well_phase_id=wellphase_id,status=1)
    muddata = MudData.objects.filter(well_phase_id=wellphase_id,status=1).values()
    if request.method == 'POST':
        date=request.POST.getlist('date')
        time=request.POST.getlist('time')
        timestamp=request.POST.getlist('timestamp')
        muddata_id=request.POST.getlist('muddata_id')
        i=0
        while(i<len(date)):
            rheogram_date = RheogramDate.objects.filter(muddata_id=muddata_id[i]).update(date=date[i],time=time[i],timestamp=timestamp[i])
            rpm=request.POST.getlist('rpm'+str(i))
            dial=request.POST.getlist('dial'+str(i))
            rheogram_id=request.POST.getlist('rheogram_id'+str(i))

            j=0
            while j < len(rpm):
                if(rheogram_id[j]):
                    Rheogram.objects.filter(id=rheogram_id[j]).update(rpm=rpm[j],dial=dial[j])
                else:
                    Rheogram.objects.create(rpm=rpm[j],dial=dial[j],rheogram_date=rheogram_date,well_id=well_id,company=request.company)

                j +=1
            i += 1
        return redirect('muddata:rheogram_actual',wellphase_id=wellphase_id)


    checkrheogram = RheogramDate.objects.filter(well_phase_id=wellphase_id,status=1)
    return render(request,'muddata/rheogramedit_actual.html',{'well_id':well_id,'wellphases':wellphase,'wellphase_id':wellphase_id,'countries':getcountries(request.company),'company':request.company,'rheogram':checkrheogram,'sections':sections,'muddata':muddata})


def rheogramcreate(request,wellphase_id):
    well_id=request.session['well_id']
    well = Wells.objects.get(id=well_id)
    request.session['wellphasetab']=wellphase_id
    request.session['submenu']='rheogram'
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    muddata = MudData.objects.filter(well_phase_id=wellphase_id,status=1).values()
    sections = Sections.objects.filter(well_id=well_id, company=request.company,well_phase_id=wellphase_id,status=1)
    currentwellphase=WellPhases.objects.filter(id=wellphase_id).values('measured_depth','id','well_id').first()
    previouswellphase=WellPhases.objects.filter(id__lt=currentwellphase['id']).filter(well_id=currentwellphase['well_id']).order_by("-id").values('measured_depth','id')[:1]
    fromdepth=0 if previouswellphase.count()==0 else previouswellphase[0]['measured_depth']
    todepth= currentwellphase['measured_depth']
    welltype = well.well_type
    if request.method == 'POST':
        sections=request.POST.getlist('section')
        wellphase=request.POST.getlist('well_phase')
        well_id=request.POST.get('well')
        form = RheogramdateForm(request.POST)
        if form.is_valid():
            rheogram_date=form.save()
            rheogram_date.company=request.company
            rheogram_date.well_phase_id=wellphase_id
            if(len(request.POST.getlist('selected_model'))!=0):
                rheogram_date.selected_model=request.POST.getlist('selected_model')[0]
            rheogram_date.save()
            i = 0
            while i < len(sections):
                sectionsdata=Sections.objects.filter(section_name=sections[i],well_phase_id=wellphase_id,status=1).values()
                fromdepth=request.POST.get('from_depth'+ str(i))
                todepth=request.POST.get('todepth'+ str(i))
                if(sectionsdata.count()==0):
                    Sections.objects.create(section_name=sections[i],company=request.company,well_phase_id=wellphase_id,well_id=well_id,from_depth=fromdepth,todepth=todepth,selected_model='')
                else:
                    Sections.objects.filter(id=sectionsdata[0]['id']).update(section_name=sections[i],from_depth=fromdepth,todepth=todepth)
                
                rheogramsections=RheogramSections.objects.create(section_name=sections[i],from_depth=fromdepth,todepth=todepth,rheogram_date=rheogram_date,well_phase_id=wellphase_id)
                rheogramsection_id=RheogramSections.objects.values('id').last()
                rpm=request.POST.getlist('rpm'+str(i))
                dial=request.POST.getlist('dial'+str(i))
                # calculateddial=request.POST.getlist('calculateddial'+str(i))
                muddata=MudData.objects.filter(section=sections[i],well_phase_id=wellphase_id,status=1).first()
                if(muddata.plastic_viscosity == None and muddata.yield_point == None and muddata.low_shear_rate == None):
                    j=0
                    while j < len(rpm):
                        Rheogram.objects.create(rpm=rpm[j],dial=dial[j],rheogram_date=rheogram_date,well_id=well_id,company=request.company,rheogram_sections=rheogramsections)
                        j +=1
                else:
                    newtonianrpm=request.POST.getlist('newtonianrpm'+str(i))
                    newtoniandial=request.POST.getlist('newtoniandial'+str(i))
                    j=0
                    while j < len(newtonianrpm):
                        Rheogram.objects.create(rpm=newtonianrpm[j],dial=newtoniandial[j],rheogram_date=rheogram_date,well_id=well_id,company=request.company,rheogram_sections=rheogramsections,modelname="newtonian")
                        j +=1
                    binghamrpm=request.POST.getlist('binghamrpm'+str(i))
                    binghamdial=request.POST.getlist('binghamdial'+str(i))
                    j=0
                    while j < len(binghamrpm):
                        Rheogram.objects.create(rpm=binghamrpm[j],dial=binghamdial[j],rheogram_date=rheogram_date,well_id=well_id,company=request.company,rheogram_sections=rheogramsections,modelname="bingham")
                        j +=1
                    powerlawrpm=request.POST.getlist('powerlawrpm'+str(i))
                    powerlawdial=request.POST.getlist('powerlawdial'+str(i))
                    j=0
                    while j < len(powerlawrpm):
                        Rheogram.objects.create(rpm=powerlawrpm[j],dial=powerlawdial[j],rheogram_date=rheogram_date,well_id=well_id,company=request.company,rheogram_sections=rheogramsections,modelname="powerlaw")
                        j +=1
                    hershelrpm=request.POST.getlist('hershelrpm'+str(i))
                    hersheldial=request.POST.getlist('hersheldial'+str(i))
                    j=0
                    while j < len(hershelrpm):
                        Rheogram.objects.create(rpm=hershelrpm[j],dial=hersheldial[j],rheogram_date=rheogram_date,well_id=well_id,company=request.company,rheogram_sections=rheogramsections,modelname="hershel")
                        j +=1
                i +=1
            source_id=wellphase_id
            userlog=adduserlog('Rheogram Created',request,source_id,'Rheogram',request.user.licence_type,well.project_id,well_id,wellphase_id,'create')
            return redirect('muddata:muddatarheogramlist',wellphase_id=wellphase_id)    
    form = RheogramdateForm()
    rheogram_rpm= RheogramNameModels.objects.all()
    rheogram=Rheogram.objects.all()
    return render(request,'muddata/rheogramcreate.html',{'form':form,'well_id':well_id,'rheogram_rpm':rheogram_rpm,'rheogram':rheogram,'welltype':welltype,'wellphases':wellphase,'muddata':muddata,'fromdepth':fromdepth,'todepth':todepth,'sections':sections,'wellphase_id':wellphase_id})
        

def rheogramdetails(request,pk):
    wellphase_id=request.GET['wellphase']
    rheogram_date=RheogramDate.objects.get(pk=pk)
    request.session['submenu']='rheogram'
    well_id=rheogram_date.well_id
    rheogram_sections=RheogramSections.objects.filter(rheogram_date=rheogram_date,status=1)

    rheogram=Rheogram.objects.filter(rheogram_date=rheogram_date,well_id=well_id,status=1)

    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    rheogram_rpm= RheogramNameModels.objects.all()
    sections = Sections.objects.filter(well_id=well_id, company=request.company,well_phase_id=wellphase_id,status=1).order_by('todepth')

    well = Wells.objects.get(id=well_id)
    welltype = well.well_type
    selected_model=rheogram_date.selected_model
    currentwellphase=WellPhases.objects.filter(id=wellphase_id).values('measured_depth','id','well_id').first()
    previouswellphase=WellPhases.objects.filter(id__lt=currentwellphase['id']).filter(well_id=currentwellphase['well_id']).order_by("-id").values('measured_depth','id')[:1]
    fromdepth=0 if previouswellphase.count()==0 else previouswellphase[0]['measured_depth']
    todepth= currentwellphase['measured_depth']
    muddata = MudData.objects.filter(well_phase_id=wellphase_id,status=1).values()
    mudtype=MudType.objects.all()
    
    return render(request,'muddata/rheogramview.html',{'rheogram_date': rheogram_date,'rheogram':rheogram,'welltype':welltype,'rheogram_sections':rheogram_sections,'wellphases':wellphase,'sections':sections,'rheogram_rpm':rheogram_rpm,'wellphase_id':wellphase_id,'selected_model':selected_model,'fromdepth':fromdepth,'todepth':todepth,'muddata':muddata,'mudtype':mudtype,'well_id':well_id,'countries':getcountries(request.company),'company':request.company,'well':well})

def rheogramlist(request,wellphase_id):
    well_id=request.session['well_id']
    request.session['wellphasetab']=wellphase_id
    rheogram_date = RheogramDate.objects.filter(company=request.company,well_id=well_id,well_phase_id=wellphase_id,status=1)
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    well = Wells.objects.get(id=well_id)
    request.session['submenu']='rheogram'
    welltype = well.well_type
    if(len(rheogram_date) == 0):
        return redirect('muddata:rheogramcreate',wellphase_id=wellphase_id)
    return render(request,'muddata/rheogramlist.html',{'rheogram_date': rheogram_date,'well_id':well_id,'welltype':welltype,'wellphases':wellphase,'wellphase_id':wellphase_id})

def rheogramlist_actual(request,wellphase_id):
    well_id=request.session['well_id']
    request.session['wellphasetab']=wellphase_id
    rheogram_date = RheogramDate.objects.filter(company=request.company,well_id=well_id,well_phase_id=wellphase_id,status=1)
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    well = Wells.objects.get(id=well_id)
    request.session['submenu']='rheogram'
    welltype = well.well_type
    if(len(rheogram_date) == 0):
        return redirect('muddata:rheogramcreate_actual',wellphase_id=wellphase_id)
    else:
        return redirect('muddata:rheogram_actual',wellphase_id=wellphase_id)

  
def muddatarheogramlist(request,wellphase_id):
    sections = Sections.objects.filter(company=request.company,well_phase_id=wellphase_id,status=1).order_by('todepth')
    wellphase = WellPhases.objects.filter(id=wellphase_id, company=request.company,status=1).values('well_id')
    well_id=wellphase[0]['well_id']
    muddata = MudData.objects.filter(well_id=well_id,well_phase_id=wellphase_id,status=1)
    paginator = Paginator(muddata, 10)
    page = request.GET.get('page', 1)
    muddata_paginater = paginator.page(page)
    wellphases = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    request.session['wellphasetab']=wellphase_id
    request.session['submenu']='muddata'
    currentwellphase=WellPhases.objects.filter(id=wellphase_id).values('measured_depth','id','well_id').first()
    previouswellphase=WellPhases.objects.filter(id__lt=currentwellphase['id']).filter(well_id=currentwellphase['well_id']).order_by("-id").values('measured_depth','id')[:1]
    fromdepth=0 if previouswellphase.count()==0 else previouswellphase[0]['measured_depth']
    todepth= currentwellphase['measured_depth']
    mudtype=MudType.objects.all()
    rheogram_date=RheogramDate.objects.filter(company=request.company,well_phase_id=wellphase_id,status=1)
    rheogram_rpm= RheogramNameModels.objects.all()
    well = Wells.objects.get(id=well_id)
    rheogram_id=[]
    for date in rheogram_date:
        rheogram_id.append(date.id)
    rheogram=Rheogram.objects.filter(rheogram_date_id__in=rheogram_id,status=1).values('rpm').distinct()
    
    val=f
    data={
        'wellphase_id':wellphase_id,
        'sections':sections,
        'wellphases':wellphases,
        'muddata':muddata_paginater,
        'muddatacount':muddata.count(),
        'rheogram_date':rheogram_date,
        'fromdepth':fromdepth,
        'todepth':todepth,
        'mudtype':mudtype,
        'rheogram_rpm':rheogram_rpm,
        'well_id':well_id,
        'val':val,
        'countries':getcountries(request.company),
        'company':request.company,
        'well':well,
        'rheogram':rheogram,
        'project_id':well.project_id,
        'user_id':request.user,
        'module_id':5,
        'request':request
    }
    if(request.session['welltype']=='PLAN'):
        if muddata.count()== 0:
            checkpermission=user_rights_permission('Create Data',request)
            if(checkpermission != True):
                messages.error(request,'No Access to create!')
                return redirect(request.META.get('HTTP_REFERER'))
            return render(request,'muddata/muddatarheogramlist.html',data)
        else:
            checkpermission=user_rights_permission('View Data',request)
            if(checkpermission != True):
                messages.error(request,'No Access to view!')
                return redirect(request.META.get('HTTP_REFERER'))
            return render(request,'muddata/muddatarheogramlist.html',data)
    else: 
        return render(request,'muddata/muddata_actual.html',data)

def actual_well_view(request,wellphase_id):
    csrf_token = get_token(request)
    print(f"csrf_token {csrf_token}")
    well_id=request.session['well_id']
    previouswellphase=WellPhases.objects.filter(id__lt=wellphase_id,well_id=well_id,status=1).order_by("-id").values('measured_depth','id')[:1]
    fromdepth=0 if previouswellphase.count()==0 else previouswellphase[0]['measured_depth']
    todepth=WellPhases.objects.filter(id=wellphase_id,well_id=well_id, company=request.company,status=1).last()
    # print(f"todepth {todepth.measured_depth}")
    alldepth=HydraulicData.objects.filter(well_id=well_id,status=1,measured_depth__lte=todepth.measured_depth,measured_depth__gte=fromdepth).values('measured_depth')
    # print(f"alldepth {alldepth}")
    # print(f"fromdepth {fromdepth}")
    depth=[data["measured_depth"] for data in alldepth]
    # allecd=HydraulicData.objects.filter(well_id=well_id,status=1).values('ecd')
    alldata=HydraulicData.objects.filter(well_id=well_id,status=1).values_list('ecd','flowrate','rpm','rop','pump_pressure')
    ecd=[]
    flowrate=[]
    rpm=[]
    rop=[]
    pump_pressure=[]
    for data in alldata:
        if data[0]!=None:
            ecd.append(data[0])
        if data[1]!=None:
            flowrate.append(data[1])
        if data[2]!=None:
            rpm.append(data[2])
        if data[3]!=None:
            rop.append(data[3])
        if data[4]!=None:
            pump_pressure.append(data[4])

    # ecd=[data["ecd"] for data in allecd if data["ecd"]!=None]
    # print(f'ecd {ecd}')
    # allflowrate=HydraulicData.objects.filter(well_id=well_id,status=1).values('flowrate')
    # flowrate=[data["flowrate"] for data in allflowrate]
    # print(f'flowrate {flowrate}')
    # allrpm=HydraulicData.objects.filter(well_id=well_id,status=1).values('rpm')
    # rpm=[data["rpm"] for data in allrpm]
    # print(f'rpm {rpm}')
    # allrop=HydraulicData.objects.filter(well_id=well_id,status=1).values('rop')
    # rop=[data["rop"] for data in allrop]
    # print(f'rop {rop}')
    # allpump_pressure=HydraulicData.objects.filter(well_id=well_id,status=1).values('pump_pressure')
    # pump_pressure=[data["pump_pressure"] for data in allpump_pressure]
    # print(f'pump_pressure {pump_pressure}')
    # alltime=HydraulicData.objects.filter(well_phase_id=wellphase_id).values('timestamp')
    # timestamp=[data["timestamp"] for data in alltime]
    # alltime=HydraulicData.objects.filter(well_phase_id=wellphase_id).values('time')
    # time=[]
    # for data in alltime:
    #     time.append(datetime.time.strftime(data['time'], '%H:%M'))
    
    well = Wells.objects.get(id=well_id)
    planwell_id = well.plan_well_list_id
    wellphases = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    data={
      'depth':depth,
      'ecd':ecd,
      'flowrate':flowrate,
      'rpm':rpm,
      'rop':rop,
      'pump_pressure':pump_pressure,
      'planwell_id':planwell_id,
      'well_id':well_id,
      'wellphases':wellphases,
      'countries':getcountries(request.company),
      'company':request.company,
      'well':well,
      'wellphase_id':wellphase_id,
      'csrf_token':csrf_token
    }
    # print(f'data {data}')
    return render(request,'muddata/actualwell_output.html',data)

def importmuddata(request,wellphase_id):
    well_id=request.session['well_id']
    muddata_header_list=['Depth','MudWeight','PV','YP','LSRYP','Gel Strength(0sec)','Gel Strength(10min)','Gel Strength(30min)']
    allmuddata={}
    if request.method == 'POST' and 'myfile' in request.FILES:
        dataset = Dataset()
        new_datas = request.FILES['myfile']
        data = pd.read_excel(new_datas,keep_default_na=False)
        columns=data.columns

        for col in columns:
            appendlist=[]
            for alldata in data[col]:
                appendlist.append(alldata)
            allmuddata[col]=appendlist

        previous_date=''
        previous_time=''
        muddata_ids=[]
        rheogram_date_id=[]
        sections_list=[]
        muddata_list=[]
        i=0
        while i<len(allmuddata['MudWeight']):
            mudweight_data=allmuddata['MudWeight'][i]
            gel_strength_0sec_data=allmuddata['Gel Strength(0sec)'][i] if(allmuddata['Gel Strength(0sec)'][i]!='') else None  
            gel_strength_10min_data=allmuddata['Gel Strength(10min)'][i] if(allmuddata['Gel Strength(10min)'][i]!='') else None    
            gel_strength_30min_data=allmuddata['Gel Strength(30min)'][i] if(allmuddata['Gel Strength(30min)'][i]!='') else None 
            plastic_viscosity_data=allmuddata['PV'][i] if(allmuddata['PV'][i]!='') else None 
            yield_point_data=allmuddata['YP'][i] if(allmuddata['YP'][i]!='') else None 
            low_shear_rate_data=allmuddata['LSRYP'][i] if(allmuddata['LSRYP'][i]!='') else None 
            depth_data=allmuddata['Depth'][i] if(allmuddata['Depth'][i]!='') else None 
            section_data = Sections(company=request.company,well_phase_id=wellphase_id,well_id=well_id,todepth=depth_data)
            sections_list.append(section_data)

            muddata_data=MudData(
                well_id=well_id,company=request.company,todepth=depth_data,mud_weight=allmuddata['MudWeight'][i],plastic_viscosity=plastic_viscosity_data,yield_point=yield_point_data,low_shear_rate=low_shear_rate_data,gel_strength_0sec=gel_strength_0sec_data,gel_strength_10min=gel_strength_10min_data,gel_strength_30min=gel_strength_30min_data,well_phase_id=wellphase_id 
            )

            muddata_list.append(muddata_data)
         
            i += 1
        
        MudData.objects.bulk_create(muddata_list)
        Sections.objects.bulk_create(sections_list)
        
        
        rpm_keys=[]
        for rpm,dial in allmuddata.items():
            if rpm not in muddata_header_list:
                rpm_keys.append(rpm)
        
        if(len(rpm_keys)>0):
            rheogram_date_list=[]
            newmuddata=MudData.objects.filter(well_phase_id=wellphase_id,status=1)
            for mud in newmuddata:
                rheogram_date_data=RheogramDate(
                    company=request.company,well_id=well_id,well_phase_id=wellphase_id,status=1,muddata_id=mud.id
                )
                rheogram_date_list.append(rheogram_date_data)

            RheogramDate.objects.bulk_create(rheogram_date_list)
        
            rheogram_list=[]
            newrheogram_date_id=RheogramDate.objects.filter(well_phase_id=wellphase_id,status=1)

            m=0
            while m<len(allmuddata['MudWeight']): 
                for rpmdata in rpm_keys:
                    rheogram_data=Rheogram(
                    rpm=rpmdata,dial=allmuddata[rpmdata][m],rheogram_date_id=newrheogram_date_id[m].id,well_id=well_id,company=request.company
                    )
                    rheogram_list.append(rheogram_data)
                m += 1
            
            Rheogram.objects.bulk_create(rheogram_list)

        return redirect('muddata:muddatarheogramlist', wellphase_id=wellphase_id)

    return render(request, 'muddata/importmuddata.html', {'wellphase_id':wellphase_id})

def getmdtvd_actualwell(selected_date,selected_time,previous_date,previous_time,well_id):   
    timestamp=dateconversion_welltrajectory(selected_date,selected_time)

    if(previous_date!=''):
        previous_timestamp=dateconversion_welltrajectory(previous_date,previous_time)
        mdtvd=WellTrajectory.objects.filter(timestamp__gte=previous_timestamp,timestamp__lte=timestamp,well_id=well_id).order_by('-id')[:1].first()
    else:
        mdtvd=WellTrajectory.objects.filter(timestamp__lte=timestamp,well_id=well_id).order_by('-id')[:1].first()
    data={
        'md':mdtvd.measured_depth,
        'tvd':mdtvd.true_vertical_depth,
        'id':mdtvd.id
    }
    return data

def rheogramedit(request, pk, template_name='muddata/rheogramedit.html'):
    wellphase_id=request.GET['wellphase']
    request.session['submenu']='rheogram'
    request.session['wellphasetab']=int(wellphase_id)
    rheogram_date = get_object_or_404(RheogramDate, pk=pk)
    form = RheogramdateForm(request.POST or None, instance=rheogram_date)
    rheogram = Rheogram.objects.filter(rheogram_date=pk,status=1)
    well_id=rheogram_date.well_id
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    sections = Sections.objects.filter(well_id=well_id, company=request.company,well_phase_id=wellphase_id,status=1).order_by('todepth')
    well = Wells.objects.get(id=well_id)
    currentwellphase=WellPhases.objects.filter(id=wellphase_id).values('measured_depth','id','well_id').first()
    previouswellphase=WellPhases.objects.filter(id__lt=currentwellphase['id']).filter(well_id=currentwellphase['well_id']).order_by("-id").values('measured_depth','id')[:1]
    fromdepth=0 if previouswellphase.count()==0 else previouswellphase[0]['measured_depth']
    todepth= currentwellphase['measured_depth']
    rheogram_rpm= RheogramNameModels.objects.all()
    mudtype=MudType.objects.all()
    welltype = well.well_type
    selected_model=rheogram_date.selected_model
    if form.is_valid():
        rheogram_date=form.save()
        rheogram_date.company=request.company
        if(len(request.POST.getlist('selected_model'))!=0):
            rheogram_date.selected_model=request.POST.getlist('selected_model')[0]
        rheogram_date.save()
        sections=request.POST.getlist('section')
        wellphase=request.POST.getlist('well_phase')
        rheogram_sections=request.POST.getlist('rheogram_sections')
        i = 0
        currentsectionid=[]
        rheogramsection_ids=[]
        currentrheogramids=[]
        while i < len(sections):
            sectionsdata=Sections.objects.filter(section_name=sections[i],well_phase_id=request.POST['well_phase'],status=1).values()
            fromdepth=request.POST.get('from_depth'+ str(i))
            todepth=request.POST.get('todepth'+ str(i))
            if(sectionsdata.count()==0):
                Sections.objects.create(section_name=sections[i],company=request.company,well_phase_id=request.POST['well_phase'],well_id=well_id,from_depth=fromdepth,todepth=todepth)
                sectionid=Sections.objects.values('id').last()
                currentsectionid.append(sectionid['id'])
            else:
                Sections.objects.filter(id=sectionsdata[0]['id']).update(section_name=sections[i],from_depth=fromdepth,todepth=todepth)
                currentsectionid.append(sectionsdata[0]['id'])
            if(rheogram_sections[i]):
                rheogramsections=RheogramSections.objects.filter(id=rheogram_sections[i]).update(section_name=sections[i],from_depth=fromdepth,todepth=todepth)
                rheogramsection_id=rheogram_sections[i]
                rheogramsection_ids.append(rheogramsection_id)
            else:
                rheogramsections=RheogramSections.objects.create(section_name=sections[i],from_depth=fromdepth,todepth=todepth,rheogram_date=rheogram_date,well_phase_id=request.POST['well_phase'])
                rheogramsection_data=RheogramSections.objects.values('id').last()
                rheogramsection_id=rheogramsection_data['id']
                rheogramsection_ids.append(rheogramsection_data['id'])

            rpm=request.POST.getlist('rpm'+str(i))
            dial=request.POST.getlist('dial'+str(i))
            rheogram_id=request.POST.getlist('rheogram_id'+str(i))
            muddata=MudData.objects.filter(section=sections[i],well_phase_id=wellphase_id).first()
            if(muddata== None or (muddata.plastic_viscosity == None and muddata.yield_point == None and muddata.low_shear_rate == None)):
                j=0
                while j < len(rpm):
                    if(rheogram_id[j]):
                        Rheogram.objects.filter(id=rheogram_id[j]).update(rpm=rpm[j],dial=dial[j])
                        currentrheogramids.append(rheogram_id[j])
                    else:
                        Rheogram.objects.create(rpm=rpm[j],dial=dial[j],rheogram_date=rheogram_date,well_id=well_id,company=request.company,rheogram_sections_id=rheogramsection_id)
                        lastrheogramid=Rheogram.objects.values('id').last()
                        currentrheogramids.append(lastrheogramid['id'])
                    j +=1
            else:
                all_mud=MudData.objects.filter(well_id=well_id,well_phase_id=wellphase_id,status=1).values_list('section', flat=True)
                a=0
                while a < len(rpm):
                    if sections[i] != all_mud:
                        MudData.objects.create(section=sections[i],from_depth=fromdepth,todepth=todepth,well_id=well_id,company=request.company,well_phase_id=request.POST['well_phase'])
                    Rheogram.objects.create(rpm=rpm[a],dial=dial[a],rheogram_date=rheogram_date,well_id=well_id,company=request.company,rheogram_sections_id=rheogramsection_id)
                    a+=1
            i +=1
        # RheogramSections.objects.filter(well_phase_id=wellphase_id).exclude(id__in=rheogramsection_ids).update(status=0)
        # Rheogram.objects.filter(rheogram_date=pk).exclude(id__in=currentrheogramids).update(status=0)
        # Sections.objects.filter(well_phase_id=wellphase_id).exclude(id__in=currentsectionid).update(status=0)
        
        # RheogramSections.objects.filter(well_id=well_id).exclude(id__in=rheogramsection_ids).update(status=0)
        # Rheogram.objects.filter(well_id=well_id).exclude(id__in=currentrheogramids).update(status=0)
        # Sections.objects.filter(well_id=well_id).exclude(id__in=currentsectionid).update(status=0)
        source_id=pk
        userlog=adduserlog('Rheogram Edited',request,source_id,'Rheogram',request.user.licence_type,
                           well.project_id,well_id,wellphase_id,'edit')
        return redirect('muddata:muddatarheogramlist', wellphase_id=wellphase_id)
    else:
        print(f"errors {form.errors}")
    data={
        'form':form,
        'rheogram':rheogram,
        'well_id':well_id,
        'welltype':welltype,
        'wellphases':wellphase,
        'sections':sections,
        'fromdepth':fromdepth,
        'todepth':todepth,
        'wellphase_id':wellphase_id,
        'pk':pk,
        'rheogram_rpm':rheogram_rpm,
        'selected_model':selected_model,
        'mudtype':mudtype,
        'countries':getcountries(request.company),
        'company':request.company,
        'well':well
        }
    return render(request, template_name, data)


def rheogramdelete(request, pk, template_name='crudapp/confirm_delete.html'):
    rheogram_date = get_object_or_404(RheogramDate, pk=pk)
    rheogram_date.status=0
    rheogram_date.save()
    source_id=pk
    well_id=rheogram_date.well_id
    well = Wells.objects.get(id=well_id)
    wellphase_id=rheogram_date.well_phase_id
    userlog=adduserlog('Rheogram Deleted',request,source_id,'Rheogram',request.user.licence_type,well.project_id,well_id,wellphase_id,'delete')
    return redirect('muddata:muddatarheogramlist',wellphase_id)


def muddata_value(request):
    wellphase = request.GET['wellphase']
    wellphase_date = request.GET['date']
    mud_datas=MudData.objects.filter(well_phase_id=wellphase,date=wellphase_date) 
    return JsonResponse({"data": list(mud_datas)})

def storewellphase_session(request):
    well_phase = request.GET['well_phase']
    currentwellphase=WellPhases.objects.filter(id=well_phase).values('measured_depth','id','well_id').first()
    previouswellphase=WellPhases.objects.filter(id__lt=currentwellphase['id']).filter(well_id=currentwellphase['well_id']).order_by("-id").values('measured_depth','id')[:1]
    fromdepth=0 if previouswellphase.count()==0 else previouswellphase[0]['measured_depth']
    todepth= currentwellphase['measured_depth']
    request.session['wells']=well_phase
    return JsonResponse({"status": "true",'fromdepth':fromdepth,'todepth':todepth})

def getstorewellphase(request):
    well_phases= request.session['wells']
    return JsonResponse({"well_phase": well_phases})

def getrheogramrpm(request):
    rheogram_rpm= RheogramNameModels.objects.only('id','rheogram_rpm')
    rheogram_rpm_json = serializers.serialize('json', rheogram_rpm)
    return HttpResponse(rheogram_rpm_json, content_type='application/json')

def gethydraulicsmenu(request,well_id):
    request.session['mainmenu']='wells'
    request.session['wellmenu']='hydraulics'
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    # print(f"wellphase {wellphase}")
    well = Wells.objects.get(id=well_id)
    return render(request,'muddata/wellphasemenu.html',{'wellphases':wellphase,'well_id':well_id,'countries':getcountries(request.company),'company':request.company,'well':well})

def getoptimization(request,well_id):
    request.session['mainmenu']='wells'
    request.session['wellmenu']='optimization'
    
    rpm_input=request.session["rpm_input"] if "rpm_input" in request.session else None
    rop_input=request.session["rop_input"] if "rop_input" in request.session else None
    section_name=request.session["section_name"] if "section_name" in request.session else None
    wellphase_id=int(request.session["wellphase_id"]) if "wellphase_id" in request.session else None
    mudpump_linersize=MudPumpData.objects.filter(well_id=well_id)
    well = Wells.objects.get(id=well_id)
    liner_length=MudPump.objects.filter(well_id=well_id).values('stroke_length')
    if(liner_length.count()>0):
        liner_length=liner_length[0]['stroke_length']
    else:
        liner_length=''
    drillbit = DrillBit.objects.filter(well_id=well_id,well_phases_id=wellphase_id,status=1).first()


    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)

    return render(request,'muddata/optimization.html',{'wellphases':wellphase,'well_id':well_id,'rpm_input':rpm_input,'rop_input':rop_input,'section_name':section_name,'wellphase_id':wellphase_id,"mudpump_linersize":mudpump_linersize,'liner_length':liner_length,'drillbit':drillbit,'countries':getcountries(request.company),'company':request.company,'well':well})

def getwellphasemenubyid(request,wellphase_id):
    wellphase = WellPhases.objects.filter(id=wellphase_id).first()
    request.session['wellphasetab']=wellphase_id
    wellphases = WellPhases.objects.filter(well_id=wellphase.well_id, company=request.company,status=1)
    well = Wells.objects.get(id=wellphase.well_id)
    return render(request,'muddata/wellphasesubmenu.html',{'wellphase_id':wellphase_id,'well_id':wellphase.well_id,'wellphases':wellphases,'countries':getcountries(request.company),'company':request.company,'well':well})

def insertmudtype(request):
    others_mudtype=request.GET['mudtype']
    mudtypedata=MudType.objects.filter(mud_name=others_mudtype)
    if(len(mudtypedata)==0):
        MudType.objects.create(mud_name=others_mudtype)
        mudtype=MudType.objects.values('id').last()
        status="true"
    else:
        status="false"
    return JsonResponse({"status": status,"mudtype":mudtype})

def getdialrpm(request):
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    muddata=MudData.objects.filter(well_phase_id=wellphase_id,section=section_name).first()
    plastic_viscosity=muddata.plastic_viscosity 
    rheogramsections=RheogramSections.objects.filter(well_phase_id=wellphase_id,section_name=section_name).first()
    rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id)
    if(plastic_viscosity==None):
        rpm = [rheo.rpm for rheo in rheogram]
        dial=[float(rheo.dial) for rheo in rheogram]
        X=np.array(rpm).reshape(-1,1)
        Y=np.array(dial).reshape(-1,1)
        Ne=LinearRegression(fit_intercept=False)
        Ne.fit(X,Y)
        mu=Ne.coef_[0]
        viscosity = np.around(mu, decimals=2).tolist()[0]
    else:
        viscosity=plastic_viscosity 
    newdial=[]
    for rheo in rheogram:
        newdial.append(viscosity * rheo.rpm)
    rpm = [rheo.rpm for rheo in rheogram]
    dial = [float(rheo.dial) for rheo in rheogram]
    data={
        'rpm':rpm,
        'dial':dial,
        'calculateddial':newdial
    }
    return JsonResponse(data,safe=False)

def get_bingham_plastic(request):
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    rheogramsections=RheogramSections.objects.filter(well_phase_id=wellphase_id,section_name=section_name).first()
    rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id)
    muddata=MudData.objects.filter(well_phase_id=wellphase_id,section=section_name).first()
    plastic_viscosity=muddata.plastic_viscosity 
    rpm = [rheo.rpm for rheo in rheogram]
    dial=[float(rheo.dial) for rheo in rheogram]
    if(plastic_viscosity==None):
        X=np.array(rpm).reshape(-1,1)
        Y=np.array(dial).reshape(-1,1)
        BP=LinearRegression()
        BP.fit(X,Y)
        yieldpoint=BP.intercept_[0]
        pv=BP.coef_[0]
        viscocity=np.around(pv,decimals=2).tolist()[0]
    else:
        yieldpoint=muddata.yield_point
        viscocity=muddata.plastic_viscosity
    avg_rpm=sum(rpm)/len(rpm)
    avg_dial=sum(dial)/len(dial)
    y_Y= [y - avg_rpm for y in rpm]
    x_X= [x - avg_dial for x in dial]
    z_Z=[(x_X[i])*(y_Y[i]) for i in range(len(y_Y))]
    total_z=sum(z_Z)
    squre_X=[num ** 2 for num in y_Y]
    total_squre_X=sum(squre_X)
    last_rpm=rpm[-1:]
    return JsonResponse({"yield_point":round(yieldpoint,2),"plastic_viscosity":viscocity,'last_rpm':last_rpm})

def getdirectchart(request):
    rpm=request.GET.getlist('rpm[]')
    dial=request.GET.getlist('dial[]')
    userrpm=[int(i) for i in rpm]
    userdial=[float(j) for j in dial]
    section_name=request.GET['section_name']
    wellphase_id=request.GET['wellphase_id']
    well_id=request.GET['well_id']
    unit=getprojectunit(well_id)
    muddata=MudData.objects.filter(well_phase_id=wellphase_id,section=section_name,well_id=well_id,status=1).first()
    plastic_viscosity=muddata.plastic_viscosity
    userenterdial=[]
    dial_300=0
    dial_600=0
    i=0
    while i < len(userrpm):
        userenterdial.append([userrpm[i],userdial[i]])
        i += 1
    newtoniondial=getnewtonialmodal(unit,plastic_viscosity,userrpm,userdial)
    binghammodal=getbinghammodal(unit,plastic_viscosity,muddata.yield_point,userrpm,userdial)
    powerlawmodal=getpowerlawmodal(unit,userrpm,userdial,plastic_viscosity,muddata.yield_point,dial_300,dial_600)
    if(len(userrpm)>2):
        hershelmodal=gethershelmodal(unit,userrpm,userdial,plastic_viscosity,muddata.yield_point,muddata.low_shear_rate,dial_300,dial_600)
        hershel=hershelmodal['modal']
    else:
        hershel=''
    data={
        'rpm':userrpm,
        'userenterdial':userdial,
        'newtoniondial':newtoniondial['modal'],
        'binghammodal':binghammodal['modal'],
        'powerlawmodal':powerlawmodal['modal'],
        'hershelmodal':hershel,
        'userdial':userenterdial
    }
    return JsonResponse(data)

def getrheogrammodals(request):
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    well_id = request.GET['well_id']
    selected_model=RheogramDate.objects.filter(well_phase_id=wellphase_id).filter(status=1).values('selected_model')
    rheogram_model=selected_model[0]['selected_model']
    rheogramsections=RheogramSections.objects.filter(well_phase_id=wellphase_id,section_name=section_name,status=1).first()
    rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id)
    section_modelselect = Sections.objects.filter(section_name=section_name,well_phase_id=wellphase_id,status=1).values('selected_model')
    section_model = section_modelselect[0]['selected_model']
    unit = getprojectunit(well_id)
    userenterdial=[]
    rpm=[]
    dial_600=0
    dial_300=0
    for rheo in rheogram:
        if(rheo.dial):
            if(rheo.rpm==300):
                dial_300=float(rheo.dial)
            elif(rheo.rpm==600):
                dial_600=float(rheo.dial)
            userenterdial.append(float(rheo.dial))
    for rheo in rheogram:
        if(rheo.dial):

            rpm.append(rheo.rpm)
    # rpm=[rheo.rpm for rheo in rheogram]
    muddata=MudData.objects.filter(well_phase_id=wellphase_id,section=section_name,well_id=well_id,status=1).first()
    if(muddata==None):
        plastic_viscosity=None
        yield_point=None
        low_shear_rate=None
    else:
        plastic_viscosity=muddata.plastic_viscosity
        yield_point=muddata.yield_point
        low_shear_rate=muddata.low_shear_rate
    # yield_point=muddata.yield_point
    newtoniondial=getnewtonialmodal(unit,plastic_viscosity,rpm,userenterdial,rheogramsections.id)
    binghammodal=getbinghammodal(unit,plastic_viscosity,yield_point,rpm,userenterdial,rheogramsections.id)
    powerlawmodal=getpowerlawmodal(unit,rpm,userenterdial,plastic_viscosity,yield_point,rheogramsections.id,dial_300,dial_600)
    if(low_shear_rate):
        hershelmodal=gethershelmodal(unit,rpm,userenterdial,plastic_viscosity,yield_point,low_shear_rate,rheogramsections.id,dial_300,dial_600)


    userdial=[]
    i=0
    while i < len(rpm):
        if(userenterdial[i]!=0):
            userdial.append([rpm[i],userenterdial[i]])
        i += 1
    allrmsvalue={
        'Newtonian Fluid':newtoniondial['rmsvalue'],
        'Bingham Plastic':binghammodal['rmsvalue'],
        'Powerlaw':powerlawmodal['rmsvalue'],
    }
    if(low_shear_rate):
        allrmsvalue['Hershel Bulkley']=hershelmodal['rmsvalue']
    
    temp = min(allrmsvalue.values())
    minimumrmsmodal = [key for key in allrmsvalue if allrmsvalue[key] == temp][0]
    modalparameters={}
    allmodalparameters={}
    modalkey={'1':"Newtonian Fluid",'2':"Bingham Plastic",'3':'Powerlaw','4':'Hershel Bulkley'}
    if(section_model==None):
        checkmodal=minimumrmsmodal
    else:
        checkmodal=modalkey[section_model]

    if(checkmodal=="Newtonian Fluid"):
        plastic_viscocity=(dial_600-dial_300)
        viscocity=(dial_600-dial_300)
        yield_point=(dial_300-viscocity)
        modalparameters['plastic_viscocity']=viscosity_conversion(plastic_viscocity,unit)
        modalparameters['yield_point']=yieldpoint_conversion(yield_point,unit)
    elif(checkmodal=="Bingham Plastic"):
        plastic_viscocity=(dial_600-dial_300)
        viscocity=(dial_600-dial_300)
        yield_point=(dial_300-viscocity)
        modalparameters['plastic_viscocity']=viscosity_conversion(plastic_viscocity,unit)
        modalparameters['yield_point']=yieldpoint_conversion(yield_point,unit)
    elif(checkmodal=="Powerlaw"):
        modalparameters['K']=round(powerlawmodal['K'],2)
        modalparameters['n']=round(powerlawmodal['n'],2)
        plastic_viscocity=(dial_600-dial_300)
        viscocity=(dial_600-dial_300)
        yield_point=(dial_300-viscocity)
        modalparameters['plastic_viscocity']=viscosity_conversion(plastic_viscocity,unit)
        modalparameters['yield_point']=yieldpoint_conversion(yield_point,unit)
    else:
        modalparameters['K']=round(hershelmodal['K'],2)
        modalparameters['n']=round(hershelmodal['n'],2)
        modalparameters['Ty']=round(hershelmodal['Ty'],2)
        plastic_viscocity=(dial_600-dial_300)
        viscocity=(dial_600-dial_300)
        yield_point=(dial_300-viscocity)
        modalparameters['plastic_viscocity']=viscosity_conversion(plastic_viscocity,unit)
        modalparameters['yield_point']=yieldpoint_conversion(yield_point,unit)
    
    allmodalparameters['plastic_viscocity']=dial_600-dial_300
    allmodalparameters['yield_point']=dial_300-modalparameters['plastic_viscocity']
    allmodalparameters['powerlaw_K']=round(powerlawmodal['K'],2)
    allmodalparameters['powerlaw_n']=round(powerlawmodal['n'],2)
    if(low_shear_rate):
        allmodalparameters['hershel_K']=round(hershelmodal['K'],2)
        allmodalparameters['hershel_n']=round(hershelmodal['n'],2)
        allmodalparameters['hershel_Ty']=round(hershelmodal['Ty'],2)
    # pv_value = dial_600-dial_300
    # yp_value = dial_300-modalparameters['plastic_viscocity']

    if(muddata==None or (muddata.plastic_viscosity == None and muddata.yield_point == None and muddata.low_shear_rate == None)):
        # MudData.objects.filter(well_phase_id=wellphase_id,section=section_name).update(plastic_viscosity=pv_value,yield_point=yp_value,low_shear_rate=14)
        data={
            'rpm':rpm,
            'userenterdial':userenterdial,
            'newtoniondial':newtoniondial,
            'binghammodal':binghammodal,
            'powerlawmodal':powerlawmodal,
            'userdial':userdial,
            'minimumrmsmodal':minimumrmsmodal,
            'last_rpm':rpm[-1:],
            'charttype':'direct',
            'section_model':section_model,
            'modalparameters':modalparameters,
            'allmodalparameters':allmodalparameters,
            'low_shear_rate':low_shear_rate

        }
        if(low_shear_rate):
            data['hershelmodal']=hershelmodal
        else:
            data['hershelmodal'] = {'modal': []}

    else:
        data={
            'userenterdial':userenterdial,
            'newtoniondial':newtoniondial,
            'binghammodal':binghammodal,
            'powerlawmodal':powerlawmodal,
            'charttype':'indirect',
            'rheogram_model':rheogram_model,
            'modalparameters':modalparameters,
            'allmodalparameters':allmodalparameters,
            'low_shear_rate':low_shear_rate

        }
        if(low_shear_rate):
            data['hershelmodal']=hershelmodal
        else:
            data['hershelmodal'] = {'modal': []}   
    return JsonResponse(data)

def getnewtonialmodal(unit,plastic_viscosity,rpm,userenterdial,rheogramsectionsid=''):
    newdial=[]
    calculateddial=[]
    if(plastic_viscosity==None):
        X=np.array(rpm).reshape(-1,1)
        Y=np.array(userenterdial).reshape(-1,1)
        Ne=LinearRegression(fit_intercept=False)
        Ne.fit(X,Y)
        mu=Ne.coef_[0]
        viscosity = np.around(mu, decimals=2).tolist()[0]
        i=0
        while i < len(rpm):
            newdial.append([rpm[i],viscosity * rpm[i]])
            calculateddial.append(viscosity * rpm[i])
            i += 1
        rms=0
        j=0
        while j < len(calculateddial):
            difference=(userenterdial[j]-calculateddial[j])**2
            rms +=difference
            j += 1
        rmsvalue=round((sqrt(rms/len(rpm))),2)
    else:

        viscosity=viscosity_conversion(plastic_viscosity,unit)

        last_rpm=rpm[-1]
        rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsectionsid,modelname='newtonian')
        for i in range(0,last_rpm+1):
                viscocity=(viscosity/1000*0.02088*100*i*1.703)/1.066
                newdial.append([i,round((viscocity),2)])
        rmsvalue=''
    data={
        'modal':newdial,
        'rmsvalue':rmsvalue,
        'viscosity':viscosity
    }
    return data

def getbinghammodal(unit,plastic_viscosity,yield_point,rpm,userenterdial,rheogramsectionsid=''):
    newdial=[]
    if(plastic_viscosity==None):
        X=np.array(rpm).reshape(-1,1)
        Y=np.array(userenterdial).reshape(-1,1)
        BP=LinearRegression()
        BP.fit(X,Y)
        yieldpoint=BP.intercept_[0]
        pv=BP.coef_[0]
        viscocity=np.around(pv,decimals=2).tolist()[0]
        avg_rpm=sum(rpm)/len(rpm)
        avg_dial=sum(userenterdial)/len(userenterdial)
        y_Y= [y - avg_rpm for y in rpm]
        x_X= [x - avg_dial for x in userenterdial]
        z_Z=[(x_X[i])*(y_Y[i]) for i in range(len(y_Y))]
        total_z=sum(z_Z)
        squre_X=[num ** 2 for num in y_Y]
        total_squre_X=sum(squre_X)
        last_rpm=rpm[-1:]
        for i in range(last_rpm[0]+1):
            calculateddial=yieldpoint+i*viscocity
            newdial.append([i,round(calculateddial,2)])
        rms=0
        j=0
        while j < len(rpm):
            new_dial=round(yieldpoint,2)+viscocity*rpm[j]
            difference=(userenterdial[j]-new_dial)**2
            rms +=difference
            j += 1
        rmsvalue=round((sqrt(rms/len(rpm))),2)
    else:
        yieldpoint=yieldpoint_conversion(yield_point,unit)
        viscocity=viscosity_conversion(plastic_viscosity,unit)
        
        last_rpm=rpm[-1]
        rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsectionsid,modelname='bingham')
        for i in range(0,last_rpm+1):
                viscocity_new=(viscocity/1000*0.02088*100*i*1.703/1.066+yieldpoint)
                # calculateddial=yieldpoint+i*viscocity_new
                newdial.append([i,round(viscocity_new,2)])
        rmsvalue=''
    
    data={
        'modal':newdial,
        'rmsvalue':rmsvalue,
        'viscocity':viscocity,
        'yieldpoint':yieldpoint
    }
    return data

def getpowerlawmodal(unit,rpm,userenterdial,plastic_viscosity,yield_point,dial_300,dial_600,rheogramsectionsid=''):
    newdial=[]
    if(plastic_viscosity==None):
        X=np.array(rpm).reshape(-1,1)
        Y=np.array(userenterdial).reshape(-1,1)
        X_PL=np.log10(X)
        Y_PL=np.log10(Y)
        PL=LinearRegression()
        PL.fit(X_PL,Y_PL)
        K,n=10**PL.intercept_[0],PL.coef_[0][0]
        last_rpm=rpm[-1:]
        for i in range(last_rpm[0]+1):
            calculateddial=round((K*i**n),2)
            newdial.append([i,calculateddial])
            if(i==300):
                dial_300=calculateddial
            elif(i==600):
                dial_600=calculateddial
        rms=0
        j=0
        plastic_viscosity=dial_600-dial_300
        yield_point=dial_300-round(plastic_viscosity,2)
        while j < len(rpm):
            new_dial=K*pow(rpm[j],n)
            difference=(userenterdial[j]-new_dial)**2
            rms +=difference
            j += 1
        rmsvalue=round((sqrt(rms/len(rpm))),2)
    else:
        rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsectionsid,modelname='powerlaw')
        last_rpm=rpm[-1]
        plastic_viscosity=viscosity_conversion(plastic_viscosity,unit)
        yield_point=yieldpoint_conversion(yield_point,unit)
        t300=plastic_viscosity*1000+yield_point/0.4788
        t600=t300+plastic_viscosity*1000
        n=3.32*log10(t600/t300)
        k_pl=t300/pow(511,n)
        K=k_pl
        for i in range(0,last_rpm+1):
            calculateddial=round((k_pl*i**n),2)
            newdial.append([i,calculateddial])
        rmsvalue=''
    data={
        'modal':newdial,
        'rmsvalue':rmsvalue,
        'K':K,
        'n':n,
        'plastic_viscosity':plastic_viscosity,
        'yield_point':yield_point
    }
    return data

def f(x,n,Ty,K):
    return Ty+K*x**n

def gethershelmodal(unit,rpm,userenterdial,plastic_viscosity,yieldpoint,low_shear_rate,dial_300,dial_600,rheogramsectionsid=''):
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
        print(f"t300 {t300}")
        t600=t300+plastic_viscosity
        print(f"t600 {t600}")

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

# def gethershelmodal():
def get_porepressure_md(request):
    from_depth = request.GET['from']
    to_depth = request.GET['to']
    well_id=request.GET['well_id']
    from_pressure_id=Pressure.objects.filter(well_id=well_id,measured_depth=from_depth)
    to_pressure_id=Pressure.objects.filter(well_id=well_id,measured_depth=to_depth)    
    data={
        'from':from_pressure_id[0].fracture_pressure,
        'to':to_pressure_id[0].fracture_pressure
    }
    return JsonResponse(data)

def calculatedial(request):
    section_name=request.GET['section_name']
    wellphase_id=request.GET['wellphase_id']
    modal=request.GET['modal']
    well_id = request.GET['well_id']
    rheogram_rpm= RheogramNameModels.objects.all()
    rpm=[int(rpm.rheogram_rpm) for rpm in rheogram_rpm]
    last_rpm=rpm[-1]
    new_dial=[]
    unit = getprojectunit(well_id)
    if(modal=='newtonian'):
        muddata=MudData.objects.filter(section=section_name,well_phase_id=wellphase_id).first()
        if(muddata.plastic_viscosity != None):
            if unit == 'API':
                plastic_viscosity = muddata.plastic_viscosity
            else:
                plastic_viscosity = muddata.plastic_viscosity*1000
            for i in range(0,last_rpm+1):
                viscocity=(plastic_viscosity/1000*0.02088*100*i*1.703)/1.066
                new_dial.append([i,round((viscocity),2)])

    elif(modal=='bingham'):
        muddata=MudData.objects.filter(section=section_name,well_phase_id=wellphase_id).first()
        if(muddata.plastic_viscosity != None and muddata.yield_point != None):
            if unit == 'API':
                plastic_viscosity = muddata.plastic_viscosity
                yield_point = muddata.yield_point
            else:
                plastic_viscosity = muddata.plastic_viscosity*1000
                yield_point = muddata.yield_point/0.4788
            for i in range(0,last_rpm+1):
                viscocity=(plastic_viscosity/1000*0.02088*100*i*1.703/1.066+yield_point)
                new_dial.append([i,round(viscocity,2)])
    elif(modal=='powerlaw'):
        muddata=MudData.objects.filter(section=section_name,well_phase_id=wellphase_id).first()
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
            for i in range(0,last_rpm+1):
                calculateddial=round((k_pl*i**n),2)
                new_dial.append([i,calculateddial])
    elif(modal=='hershel'):
        muddata=MudData.objects.filter(section=section_name,well_phase_id=wellphase_id).first()
        if(muddata.plastic_viscosity != None and muddata.yield_point != None and muddata.low_shear_rate != None):
            if unit == 'API':
                plastic_viscosity = muddata.plastic_viscosity
                yield_point = muddata.yield_point
                low_shear_rate = muddata.low_shear_rate
            else:
                plastic_viscosity = muddata.plastic_viscosity*1000
                yield_point = muddata.yield_point/0.4788
                low_shear_rate = muddata.low_shear_rate/0.4788
            
            t300=plastic_viscosity+yield_point
            t600=t300+plastic_viscosity
            m=3.32*log10((t600-muddata.low_shear_rate)/(t300-muddata.low_shear_rate))
            k_hb=(t300-muddata.low_shear_rate)/pow(511,m)
            for i in range(0,last_rpm+1):
                y=round(low_shear_rate+k_hb*i**m,2)
                new_dial.append([i, y])
                
    data={
           'new_dial':new_dial 
        }
    return JsonResponse(data)
def modelselected(request):
    selected_model=request.GET['selected_model']
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    # RheogramDate.objects.filter(well_phase_id=wellphase_id,section_name=section_name).filter(status=1).update(selected_model=selected_model)
    Sections.objects.filter(well_phase_id=wellphase_id,section_name=section_name,status=1).update(selected_model=selected_model)
    
    return JsonResponse({"data": selected_model})

def pressurelawcalculation(request,wellphase_id):
    bhadata=BhaData.objects.filter(well_phases_id=wellphase_id,status=1).first()
    well_id=bhadata.well_id
    bhaelement=BhaElement.objects.filter(Q(type_name='Drill Pipe') | Q(type_name='Heavy Weight Drill Pipe') |Q(type_name='Drill Collar'),bhadata_id=bhadata.id)
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    data={
      'bhaelement':bhaelement,
      'wellphase_id':wellphase_id,
      'wellphases':wellphase,
      'bhadataid':bhadata.id
    }
    return render(request,'muddata/pressurelaw.html',data)

def annuluspressureloss(request,wellphase_id):
    well_id=request.session['well_id']
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    data={
      'wellphase_id':wellphase_id,
      'wellphases':wellphase,
    }
    return render(request,'muddata/annuluspressureloss.html',data)

def calculateallpressureloss(request,wellphase_id):
    checkpermission=user_rights_permission('Perform Calculations',request)
    if(checkpermission != True):
        messages.error(request,'No Access to perform calculations!')
        return redirect(request.META.get('HTTP_REFERER'))
    
    well_id=request.session['well_id']
    request.session['submenu']='pressureloss'
    well = Wells.objects.get(id=well_id)
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    section=Sections.objects.filter(well_id=well_id,well_phase_id=wellphase_id,company=request.company,status=1).last()
    pressure=Pressureloss_data.objects.filter(well_id=well_id,well_phase_id=wellphase_id,status=1).last()
    # print(f"pressure {pressure.all_data}")
    pressure_count=Pressureloss_data.objects.filter(well_id=well_id,well_phase_id=wellphase_id,status=1).count()
    data={
      'wellphase_id':wellphase_id,
      'wellphases':wellphase,
      'well_id':well_id,
      'countries':getcountries(request.company),
      'company':request.company,
      'well':well,
      'pressure_count':pressure_count,
      'pressure':pressure,
      'section_name':section.section_name if section else '',
      'project_id':well.project_id,
      'module_id':7,
      'user_id':request.user
    }
    # access=input_access(request.user,well.project_id,6,well_id,'create')
    # if access == 1:
    #     return render(request,'muddata/allpressureloss.html',data)
    # else:
    #     messages.error(request,'No Access to create!')
    #     return redirect(request.META.get('HTTP_REFERER'))
    return render(request,'muddata/allpressureloss.html',data)

#calculate bore pressure loss based on user select modal for future calculation in rheogram
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


#calculate hershel bore pressure loss
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
    t_w=newton(f_x,ty+1)  # t_w=newton(f_x,ty) changed this to t_w=newton(f_x,ty+1) when Tolerance of 0.0008656012000001212 reached. Failed to converge after 1 iterations, value is 7.656877601200001,client give this correction.
    print(f"m {m} flowrate {flowrate}")
    print(f"t_w {t_w} flowrate {flowrate}")
    print(f"ty {ty} flowrate {flowrate}")

    A=((1-2*m)*t_w+3*m*ty)/(m*(t_w-ty))+((2*m*(1+m))*((1+2*m)*t_w**2+m*ty*t_w))/(m*(1+m)*(1+2*m)*t_w**2+2*m**2*(1+m)*ty*t_w+2*m**3*ty**2)
    N=1/A
    print(f"A {A} flowrate {flowrate}")

    print(f"N {N} flowrate {flowrate}")


    K_g=t_w/(8*U/identity_si)**N

    Re=mudweight_si*U**(2-N)*identity_si**N/(K_g*8**(N-1))
    # if(typename=='flowrate_pressure'):
    print(f"Re {Re} flowrate {flowrate}")
    # print(f"N {N}")

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
        print(f"Re_L {Re_L} flowrate {flowrate}")

        f_l=16/Re_L

        print(f"f_l {f_l} flowrate {flowrate}")

        Re_turb=4150-1150*N
        print(f" f_x(f_l) {f_x(f_l)} flowrate {flowrate}")
        print(f"Re_turb {Re_turb} flowrate {flowrate}")

        f_turb=newton(f_x,f_l)

        print(f"f_turb {f_turb} flowrate {flowrate}")

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

#calculate surface pressure loss
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


#calculate bit pressure loss
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



def calculatenewoptimization(request):    
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
    pump_efficiency=request.GET["pump_efficiency"]
    mechanical_efficiency=request.GET["mechanical_efficiency"]
    max_flowrate=int(request.GET["max_flowrate"])
    min_flowrate=int(request.GET["min_flowrate"])
    wellphase = WellPhases.objects.filter(id=wellphase_id).first()
    well_id=wellphase.well_id
    surfacepipe=SurfacePipe.objects.filter(well_id=well_id).first()
    no_of_nozzle=int(request.GET["no_of_nozzle"])
    previous_wellphase=WellPhases.objects.filter(id__lt=wellphase.id,well_id=well_id).order_by('-id').first()
    drillbit = DrillBit.objects.filter(well_id=well_id,well_phases_id=wellphase_id,status=1).first()

    original_tfa=float(request.GET['original_tfa'])
    increated_tfa=float(request.GET['increased_tfa'])
    optimum_flowrate=request.GET['optimum_flowrate']

    muddata=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    bhadata=BhaData.objects.filter(well_phases_id=wellphase_id,status=1).first()
    length_of_previous_casing_from_surface=previous_wellphase.measured_depth
    mud_weight=muddata.mud_weight
    hole_size=wellphase.hole_size
    id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
    sectiontodepth=muddata.todepth
    viscocity=getviscocity(muddata)
    bittype = BitTypesNames.objects.get(id=drillbit.bit_type_id)
    if(drillbit.external_nozzle == 1):
        cd_values = 0.95
    else:
        cd_values = bittype.bit_values

    bit_pressure_loss = mud_weight*int(optimum_flowrate)**2/(12042*float(cd_values)**2*increated_tfa**2)
    pressureloss=bit_pressure_loss+float(request.GET['optimum_flowrate_pressure'])
    alldata['pressureloss']=pressureloss
    return JsonResponse(alldata,safe=False)









def calculatepressureloss(request):
    # print(f"data {request}")
    rpm=request.GET['rpm']
    flowrate=int(request.GET['flowrate'])
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
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
    # print(f"muddata {muddata.todepth}")
    viscocity=getviscocity(muddata)
    # print( f"viscocity {viscocity}")

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





   


 

def ecdalongwell_calculationincreased(request):
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


    data={
        'ecdalongwellincreased':ecdalongwellincreased,
        'mudweight':muddata.mud_weight,
        'ecd_fracturepressure':fracture_chart
    }
    return JsonResponse(data,safe=False)

def calculateallpressure_loss(request):
    rpm=request.GET['rpm']
    flowrate=int(request.GET['flowrate'])
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
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
    # print(f"muddata {muddata.todepth}")
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
    # print(f"bit_losses {bit_losses}")

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
    allpressureloss['borepressureloss']=bore_pressure_loss
    allpressureloss['annularpressureloss']=annular_pressure_loss['allpressureloss']
    allpressureloss['surfacelosses']=surface_losses
    allpressureloss['bitpressurelosses']=bit_losses
    allpressureloss['fromdepth']=sectionfromdepth
    allpressureloss['todepth']=sectiontodepth
    # print(f"sectionfromdepth {sectionfromdepth}")
    # print(f"sectiontodepth {sectiontodepth}")

    allpressureloss['fromdepthtvd']=gettvd(sectionfromdepth,well_id,request,sectiontodepth)
    allpressureloss['todepthtvd']=gettvd(sectiontodepth,well_id,request,sectiontodepth)
    allpressureloss['selected_modal']=selected_modal
    allpressureloss['linercount']=checkliner.count()
    allpressureloss['mudweight']=muddata.mud_weight
    allpressureloss['plastic_viscocity']=round(viscocity["displaypv"],2)
    allpressureloss['yieldpoint']=round(viscocity["displayyp"],2) if 'displayyp' in viscocity else ''
    allpressureloss['pv']=plastic_viscocity
    allpressureloss['yp']=yieldpoint if 'yieldpoint' in viscocity else ''
    allpressureloss['previous_measured_depth']=previous_measured_depth
    allpressureloss['previous_linear']=previous_linear
    allpressureloss['K']=round(viscocity["K"],2) if 'K' in viscocity else ''
    allpressureloss['m']=round(viscocity["n"],2) if 'n' in viscocity else ''
    
    # print(f"withoutpressure {annular_pressure_loss['allpressureloss']}")
    # print(f"with {annular_pressure_loss['increased_pressureloss']}")
    allpressureloss['ecdchartdata']=ecdcalculation(wellphase.measured_depth,wellphase.true_vertical_depth,previous_measured_depth,previous_true_vertical_depth,muddata.mud_weight,annular_pressure_loss['allpressureloss'],well_id,request,'without')

    bitdepth_csg_without = [ecd['x'] for ecd in allpressureloss['ecdchartdata'] if ecd['y'] == allpressureloss['fromdepth']]
    bitdepth_td_without = [ecd['x'] for ecd in allpressureloss['ecdchartdata'] if ecd['y'] == allpressureloss['todepth']]

    # print(f"allpressureloss['ecdchartdata'] {allpressureloss['ecdchartdata']}")
    allpressureloss['increasedecdchartdata']=ecdcalculation(wellphase.measured_depth,wellphase.true_vertical_depth,previous_measured_depth,previous_true_vertical_depth,muddata.mud_weight,annular_pressure_loss['increased_pressureloss'],well_id,request,'with')

    bitdepth_csg_with = [ecd['x'] for ecd in allpressureloss['increasedecdchartdata'] if ecd['y'] == allpressureloss['fromdepth']]
    # bitdepth_td_with = [ecd['x'] for ecd in allpressureloss['increasedecdchartdata'] if ecd['y'] == allpressureloss['todepth']]
    # print(f"allpressureloss['todepth'] {allpressureloss['todepth']}")
    # print(f"allpressureloss['increasedecdchartdata'] {allpressureloss['increasedecdchartdata']}")
    # print(f'bitdepth_csg_with {bitdepth_csg_with}')
    # print(f'bitdepth_td_with {bitdepth_td_with}')
    # print(f"allpressureloss['increasedecdchartdata'] {allpressureloss['increasedecdchartdata']}")

    
    allpressureloss['cuttings_density']=cuttings_density
    allpressureloss['cuttings_size']=cuttings_size

    allpressureloss['bitdepth_csg_without']=round(allpressureloss['ecdchartdata'][0]['x'],2)
    allpressureloss['bitdepth_td_without']=round(allpressureloss['ecdchartdata'][-1]['x'],2)

    allpressureloss['bitdepth_csg_with']=round(allpressureloss['increasedecdchartdata'][0]['x'],2)
    allpressureloss['bitdepth_td_with']=round(allpressureloss['increasedecdchartdata'][-1]['x'],2)


    allpressureloss['ecdalongwell']=ecdalongwellcalculation(sectionfromdepth,sectiontodepth,bhadata,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,cuttings_size,rop)

    allpressureloss['alongwell_csg_without']=round(allpressureloss['ecdalongwell'][0]['x'],2)
    allpressureloss['alongwell_td_without']=round(allpressureloss['ecdalongwell'][-1]['x'],2)

    allpressureloss['ecdalongwellincreased']=ecdalongwellcalculation_increased(sectionfromdepth,sectiontodepth,bhadata,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,cuttings_size,rop)

    
    allpressureloss['alongwell_csg_with']=round(allpressureloss['ecdalongwellincreased'][0]['x'],2)
    allpressureloss['alongwell_td_with']=round(allpressureloss['ecdalongwellincreased'][-1]['x'],2)

    # print(f"allpressureloss {allpressureloss['ecdalongwellincreased']}")


    allpressureloss['ecd_fracturepressure']=fracture_chart
    allpressureloss['middleValue']=middleValue     
    # allpressureloss['all_bore_pressure_loss']=all_bore_pressure_loss
    # allpressureloss['all_annular_pressure_loss']=all_annular_pressure_loss
    # allpressureloss['allsurface_loss']=allsurface_loss
    allpressureloss['chartdata']=getallpressurelosschartdataold(bore_pressure_loss,annular_pressure_loss['allpressureloss'],surface_losses,bit_losses,previous_wellphase,rpm,flowrate,muddata,bhadata,sectiontodepth,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),checkliner,wellphase_id,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity)
    allpressureloss['slipvelocitychart']=annular_pressure_loss['slipvelocitychart']
    # allpressureloss['totaltjpressureloss']=annular_pressure_loss['totaltjpressureloss']
    # allpressureloss['totaltjannularloss']=annular_pressure_loss['totaltjannularloss']
    allpressureloss['cuttingsconcentration']=annular_pressure_loss['cuttingsconcentration']

    allpressureloss['annularvelocitychartdata']=calculateannularvelocitychartnew(annular_pressure_loss['allpressureloss'],flowrate,id_of_previous_casing,hole_size,well_id)
    # allpressureloss['annularvelocitychartdata']=annular_pressure_loss['annularvelocitychartdata']
    allpressureloss['mudtvd']=mudtvd
    allpressureloss['type_name']=type_name
    allpressureloss['bit_od']=bit_od
    allpressureloss['bit_length']=bit_length
    allpressureloss['transportratio']=annular_pressure_loss['transportratio']
    allpressureloss['cci']=annular_pressure_loss['cci']
    allpressureloss['unit']=unit
    allpressureloss['flowrate']=flowrate
    allpressureloss['rpm']=rpm
    allpressureloss['rop']=rop
    allpressureloss['section_name']=section_name

    # print(f"cci {annular_pressure_loss['cci']}")
    length_cci=len(annular_pressure_loss['cci'])
    max_cci=annular_pressure_loss['cci'][length_cci-1]['x']
    # print(f"max_cci {max_cci}")
    allpressureloss['maxcci']=max_cci+1
    data=Pressureloss_data.objects.filter(well_id=well_id,well_phase_id=wellphase_id,section_name=section_name)
    if (data.count()==0):
        Pressureloss_data.objects.create(all_data={
            'data':allpressureloss
        },well_id=well_id,well_phase_id=wellphase_id,section_name=section_name,company=request.company)
    else:
        Pressureloss_data.objects.filter(well_id=well_id,well_phase_id=wellphase_id,section_name=section_name).update(all_data={
            'data':allpressureloss
        })


    return JsonResponse(allpressureloss,safe=False)


       


def ecdannularcalculation_increased(bhadata,sectionfromdepth,muddata,length_of_previous_casing_from_surface,flowrate,rpm,hole_size,id_of_previous_casing,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,well_id,request,cuttings_density,cuttings_size,rop,sectiontodepth,avg_mudweight):
    bhaelement=BhaElement.objects.filter(bhadata_id=bhadata.id).exclude(type_name='Bit').order_by('-id')
    viscocity=getviscocity(muddata)
    bhacount=bhaelement.count()
    totalapl=0
    allpressureloss=[]
    allincreasedpressureloss=[]

    i=bhacount
    previous_length_against_casing=[]
    cumulative_length=0
    length_check=[]
    # print(f"sectionfromdepth {sectionfromdepth}")
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
        length_check.append({'casing':length_against_casing,'openhole':length_against_open_hole})
        if(length_against_casing!=0):
            slipvelocity=calculateslipvelocitywithoutliner(well_id,rpm,flowrate,muddata.mud_weight,id_of_previous_casing,previousbha.od,viscocity,cuttings_density,cuttings_size,length_against_casing)
            slipvelocitywalker= slipvelocity_walker(muddata,id_of_previous_casing,rpm,previousbha.od,cuttings_density,cuttings_size,flowrate)

            if(slipvelocity["slipvelocity"]>=slipvelocitywalker["slipvelocity"]):
                slipvelocityvalue=slipvelocity["slipvelocity"]
            else:
                slipvelocityvalue=slipvelocitywalker["slipvelocity"]
            
            increased_mudweight=calculate_increased_mudweight(well_id,flowrate,id_of_previous_casing,previousbha.od,rop,slipvelocityvalue,muddata.mud_weight,cuttings_density)
            
            increased_pressurelossvalue=calculate_annular_loss(well_id,viscocity,flowrate,rpm,increased_mudweight["increased_mudweight"],previousbha.od,id_of_previous_casing,length_against_casing,'increasedalongwell')

            allincreasedpressureloss.append({
                'pressure_loss':increased_pressurelossvalue['pressureloss'],
                'mudweight':increased_mudweight["increased_mudweight"],
                'length':length_against_casing,
                'element_type':"CH",
                'type':previousbha.type_name
            })

        if(length_against_open_hole!=0):
            slipvelocity=calculateslipvelocitywithoutliner(well_id,rpm,flowrate,muddata.mud_weight,hole_size,previousbha.od,viscocity,cuttings_density,cuttings_size,length_against_open_hole)
            slipvelocitywalker= slipvelocity_walker(muddata,hole_size,rpm,previousbha.od,cuttings_density,cuttings_size,flowrate)

            if(slipvelocity["slipvelocity"]>=slipvelocitywalker["slipvelocity"]):
                slipvelocityvalue=slipvelocity["slipvelocity"]
            else:
                slipvelocityvalue=slipvelocitywalker["slipvelocity"]
            
            increased_mudweight=calculate_increased_mudweight(well_id,flowrate,hole_size,previousbha.od,rop,slipvelocityvalue,muddata.mud_weight,cuttings_density)
            
            increased_pressurelossvalue=calculate_annular_loss(well_id,viscocity,flowrate,rpm,increased_mudweight["increased_mudweight"],previousbha.od,hole_size,length_against_open_hole,'increasedalongwell')
            # if(sectionfromdepth==2700):
            #     print(f"increased_pressurelossvalue {increased_pressurelossvalue}")

            allincreasedpressureloss.append({
                'pressure_loss':increased_pressurelossvalue['pressureloss'],
                'mudweight':increased_mudweight["increased_mudweight"],
                'length':length_against_open_hole,
                'element_type':"OH",
                'type':previousbha.type_name
            })
        i -=1
    # print(f"length_check {length_check}")
    data={
        'allincreasedpressureloss':allincreasedpressureloss,
    }

    # print(f"data {data}")
    return data






def allmodel_surface(request):
    
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



    alldata=display_surface(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop)


    return JsonResponse(alldata,safe=False)

def allmodel_annular(request):
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


    checkliner=WellPhases.objects.filter(Q(casing_type_id=7) | Q(casing_type_id=8) | Q(casing_type_id=11) | Q(casing_type_id=12)).filter(well_id=well_id,status=1,measured_depth__lt=sectiontodepth)
    if(checkliner.count()>0):
        alldata=display_annular_liner(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,checkliner)
    else:
        alldata=display_annular(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop)


    return JsonResponse(alldata,safe=False)










def display_powerlaw_liner(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,checkliner):
    data={}
    bit_losses=getbitpressureloss(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,
    well_id)
 
    if(selected_viscocity['selected_modal']=="3"):
        selected_text='Powerlaw' 

    viscocity_powerlaw= calculate_viscocity_powerlaw(rheogramsections,sections,muddata)
    viscocity_powerlaw['selected_modal']="3"

    powerlaw_annular_pressure_loss=calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),wellphase_id,checkliner,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity_powerlaw,'displayallmodelsliner')

    powerlaw_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_powerlaw,'displayallmodels')
    
    allpowerlaw_pressureloss=gettotalresult(powerlaw_annular_pressure_loss,powerlaw_surface_losses)

    allpowerlaw_pressureloss=round(allpowerlaw_pressureloss['totalpressure_loss']+bit_losses[0]['bit_pressure_loss'])

    data = {
        'powerlaw_annular_pressure_loss':powerlaw_annular_pressure_loss,
        'powerlaw_surface_losses':powerlaw_surface_losses,
        'allpowerlaw_pressureloss':allpowerlaw_pressureloss
    }
    return data



def display_bingham_liner(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,checkliner):
    
    data={}
    bit_losses=getbitpressureloss(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,
    well_id)
    if(selected_viscocity['selected_modal']=="2"):
        selected_text='Bingham Plastic' 

    viscocity_bingham=calculate_viscocity_bingham(rheogramsections,sections,muddata)
    viscocity_bingham['selected_modal']="2"

    bingham_annular_pressure_loss=calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),wellphase_id,checkliner,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity_bingham,'displayallmodelsliner')

    bingham_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_bingham,'displayallmodelsliner')
    
    allbingham_pressureloss=gettotalresult(bingham_annular_pressure_loss,bingham_surface_losses)

    allbingham_pressureloss=round(allbingham_pressureloss['totalpressure_loss']+bit_losses[0]['bit_pressure_loss'])

    data = {
        'bingham_surface_losses':bingham_surface_losses,
        'bingham_annular_pressure_loss':bingham_annular_pressure_loss,
        'allbingham_pressureloss':allbingham_pressureloss
    }
    
    return 
    




def getallmodels(request):
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
        alldata=displayallmodalsliner(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,checkliner)
    else:
        alldata=displayallmodals(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop)



    return JsonResponse(alldata,safe=False)


def display_surface(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop):
    data={}

    if(selected_viscocity['selected_modal']=="1"):
        selected_text='Newtonion'
    elif(selected_viscocity['selected_modal']=="2"):
        selected_text='Bingham Plastic' 
    elif(selected_viscocity['selected_modal']=="3"):
        selected_text='Powerlaw' 
    elif(selected_viscocity['selected_modal']=="4"):
        selected_text='Hershel Bulkley' 


    viscocity_newtonian=calculate_viscocity_newtonian(rheogramsections,sections,muddata)
    viscocity_newtonian['selected_modal']="1"

    viscocity_bingham=calculate_viscocity_bingham(rheogramsections,sections,muddata)
    viscocity_bingham['selected_modal']="2"

    viscocity_powerlaw= calculate_viscocity_powerlaw(rheogramsections,sections,muddata)
    viscocity_powerlaw['selected_modal']="3"

    viscocity_hershel=calculate_viscocity_hershel(rheogramsections,sections,muddata)
    viscocity_hershel['selected_modal']="4"

    newtonion_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_newtonian,'displayallmodels')
    bingham_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_bingham,'displayallmodels') 
    powerlaw_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_powerlaw,'displayallmodels') 

    # if(viscocity_hershel['lsryp']>0):
    #     print('lsryp',viscocity_hershel['lsryp'])
    #     hershel_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_hershel,'displayallmodels')
    
    # else:
    #     hershel_surface_losses={}

    allmodalsurface=[]
    i=0
    while i<len(bingham_surface_losses):
        allmodalsurface.append({
            'element':powerlaw_surface_losses[i]['type'],
            'id':powerlaw_surface_losses[i]['id'],
            'length':powerlaw_surface_losses[i]['length'],
            'newtonion':newtonion_surface_losses[i]['pressureloss'],
            'bingham':bingham_surface_losses[i]['pressureloss'],
            'powerlaw':powerlaw_surface_losses[i]['pressureloss'],
            # 'hershel':hershel_surface_losses[i]['pressureloss']
        })
        # if(viscocity_hershel['lsryp']>0):
        #     allmodalsurface[i]['hershel']=hershel_surface_losses[i]['pressureloss']
        
        i +=1
    
    
  
    data["allmodalsurface"]=allmodalsurface

    return data



def display_annular_liner(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,checkliner):
    
    data={}
    if(selected_viscocity['selected_modal']=="1"):
        selected_text='Newtonion'
    elif(selected_viscocity['selected_modal']=="2"):
        selected_text='Bingham Plastic' 
    elif(selected_viscocity['selected_modal']=="3"):
        selected_text='Powerlaw' 
    # elif(selected_viscocity['selected_modal']=="4"):
    #     selected_text='Hershel Bulkley' 
    
    viscocity_newtonian=calculate_viscocity_newtonian(rheogramsections,sections,muddata)
    viscocity_newtonian['selected_modal']="1"

    viscocity_bingham=calculate_viscocity_bingham(rheogramsections,sections,muddata)
    viscocity_bingham['selected_modal']="2"

    viscocity_powerlaw= calculate_viscocity_powerlaw(rheogramsections,sections,muddata)
    viscocity_powerlaw['selected_modal']="3"

    # viscocity_hershel=calculate_viscocity_hershel(rheogramsections,sections,muddata)
    # viscocity_hershel['selected_modal']="4"

    newtonian_annular_pressure_loss=calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),wellphase_id,checkliner,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity_newtonian,'displayallmodelsliner')
    bingham_annular_pressure_loss=calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),wellphase_id,checkliner,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity_bingham,'displayallmodelsliner')
    powerlaw_annular_pressure_loss=calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),wellphase_id,checkliner,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity_powerlaw,'displayallmodelsliner')

    
    
    # print('lsryp',viscocity_hershel)
    # if(viscocity_hershel['lsryp']>0):
    #     print('lsryp',viscocity_hershel)
    #     hershel_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_hershel,'displayallmodels')
    # else:
    #     hershel_surface_losses={}
    
    alldrillstringloss=[]
    allannularloss=[]
    i=0
    while i<len(newtonian_annular_pressure_loss['allpressureloss']):
        alldrillstringloss.append({
            'type':newtonian_annular_pressure_loss['allpressureloss'][i]['type'],
            'element':newtonian_annular_pressure_loss['allpressureloss'][i]['element'],
            'element_type':newtonian_annular_pressure_loss['allpressureloss'][i]['element_type'],
            'id':newtonian_annular_pressure_loss['allpressureloss'][i]['id'],
            'od':newtonian_annular_pressure_loss['allpressureloss'][i]['od'],
            'length':newtonian_annular_pressure_loss['allpressureloss'][i]['length_against'],
            'newtonion':newtonian_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
            'bingham':bingham_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
            'powerlaw':powerlaw_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
            # 'hershel':hershel_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
        })
        allannularloss.append({
            'type':newtonian_annular_pressure_loss['allpressureloss'][i]['type'],
            'element':newtonian_annular_pressure_loss['allpressureloss'][i]['element'],
            'element_type':newtonian_annular_pressure_loss['allpressureloss'][i]['element_type'],
            'id':newtonian_annular_pressure_loss['allpressureloss'][i]['id'],
            'od':newtonian_annular_pressure_loss['allpressureloss'][i]['od'],
            'length':newtonian_annular_pressure_loss['allpressureloss'][i]['length_against'],
            'newtonion':newtonian_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
            'bingham':bingham_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
            'powerlaw':powerlaw_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
            # 'hershel':hershel_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
        })
        i +=1
    data["all_annular_pressure_loss"]=allannularloss
    data["alldrillstringloss"]=alldrillstringloss
    return data

    

def display_annular(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop):
    data={}

    if(selected_viscocity['selected_modal']=="1"):
        selected_text='Newtonion'
    elif(selected_viscocity['selected_modal']=="2"):
        selected_text='Bingham Plastic' 
    elif(selected_viscocity['selected_modal']=="3"):
        selected_text='Powerlaw' 
    # elif(selected_viscocity['selected_modal']=="4"):
    #     selected_text='Hershel Bulkley' 


    viscocity_newtonian=calculate_viscocity_newtonian(rheogramsections,sections,muddata)
    viscocity_newtonian['selected_modal']="1"

    viscocity_bingham=calculate_viscocity_bingham(rheogramsections,sections,muddata)
    viscocity_bingham['selected_modal']="2"

    viscocity_powerlaw= calculate_viscocity_powerlaw(rheogramsections,sections,muddata)
    viscocity_powerlaw['selected_modal']="3"

    # viscocity_hershel=calculate_viscocity_hershel(rheogramsections,sections,muddata)
    # viscocity_hershel['selected_modal']="4"

    newtonian_annular_pressure_loss=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity_newtonian,'displayallmodelsnewtonian')
    bingham_annular_pressure_loss=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity_bingham,'displayallmodels')
    powerlaw_annular_pressure_loss=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity_powerlaw,'displayallmodels')

    # if(viscocity_hershel['lsryp']>0):
    #     print('lsryp',viscocity_hershel['lsryp'])
    #     hershel_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_hershel,'displayallmodels')
    
    # else:
    #     hershel_surface_losses={}


    alldrillstringloss=[]
    allannularloss=[]
    i=0
    while i<len(newtonian_annular_pressure_loss['allpressureloss']):
        alldrillstringloss.append({
            'type':newtonian_annular_pressure_loss['allpressureloss'][i]['type'],
            'element':newtonian_annular_pressure_loss['allpressureloss'][i]['element'],
            'element_type':newtonian_annular_pressure_loss['allpressureloss'][i]['element_type'],
            'id':newtonian_annular_pressure_loss['allpressureloss'][i]['id'],
            'od':newtonian_annular_pressure_loss['allpressureloss'][i]['od'],
            'length':newtonian_annular_pressure_loss['allpressureloss'][i]['length_against'],
            'newtonion':newtonian_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
            'bingham':bingham_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
            'powerlaw':powerlaw_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
            # 'hershel':hershel_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
        })
       
        allannularloss.append({
            'type':newtonian_annular_pressure_loss['allpressureloss'][i]['type'],
            'element':newtonian_annular_pressure_loss['allpressureloss'][i]['element'],
            'element_type':newtonian_annular_pressure_loss['allpressureloss'][i]['element_type'],
            'id':newtonian_annular_pressure_loss['allpressureloss'][i]['id'],
            'od':newtonian_annular_pressure_loss['allpressureloss'][i]['od'],
            'length':newtonian_annular_pressure_loss['allpressureloss'][i]['length_against'],
            'newtonion':newtonian_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
            'bingham':bingham_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
            'powerlaw':powerlaw_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
            # 'hershel':hershel_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
        })
        i +=1

    
  
    data["all_annular_pressure_loss"]=allannularloss
    data["alldrillstringloss"]=alldrillstringloss
    return data






def displayallmodalsliner(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,checkliner):
    data={}
    bit_losses=getbitpressureloss(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,
    well_id)
    if(selected_viscocity['selected_modal']=="1"):
        selected_text='Newtonion'
    elif(selected_viscocity['selected_modal']=="2"):
        selected_text='Bingham Plastic' 
    elif(selected_viscocity['selected_modal']=="3"):
        selected_text='Powerlaw' 
    elif(selected_viscocity['selected_modal']=="4"):
        selected_text='Hershel Bulkley' 
    
    viscocity_newtonian=calculate_viscocity_newtonian(rheogramsections,sections,muddata)
    viscocity_newtonian['selected_modal']="1"

    viscocity_bingham=calculate_viscocity_bingham(rheogramsections,sections,muddata)
    viscocity_bingham['selected_modal']="2"

    viscocity_powerlaw= calculate_viscocity_powerlaw(rheogramsections,sections,muddata)
    viscocity_powerlaw['selected_modal']="3"

    viscocity_hershel=calculate_viscocity_hershel(rheogramsections,sections,muddata)
    viscocity_hershel['selected_modal']="4"

    newtonian_annular_pressure_loss=calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),wellphase_id,checkliner,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity_newtonian,'displayallmodelsliner')

    newtonion_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_newtonian,'displayallmodelsliner')

    bingham_annular_pressure_loss=calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),wellphase_id,checkliner,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity_bingham,'displayallmodelsliner')

    bingham_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_bingham,'displayallmodelsliner')

    powerlaw_annular_pressure_loss=calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),wellphase_id,checkliner,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity_powerlaw,'displayallmodelsliner')

    powerlaw_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_powerlaw,'displayallmodels')

    if(viscocity_hershel['lsryp']>0):
        hershel_annular_pressure_loss=calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,checkliner.count(),wellphase_id,checkliner,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity_hershel,'displayallmodelsliner')
        
        hershel_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_hershel,'displayallmodels')
        allhershel_pressureloss=gettotalresult(hershel_annular_pressure_loss,hershel_surface_losses)
    else:
        hershel_annular_pressure_loss={}
        hershel_surface_losses={}
        allhershel_pressureloss={}
    
    allnewtonion_pressureloss=gettotalresult(newtonian_annular_pressure_loss,newtonion_surface_losses)
    allbingham_pressureloss=gettotalresult(bingham_annular_pressure_loss,bingham_surface_losses)
    allpowerlaw_pressureloss=gettotalresult(powerlaw_annular_pressure_loss,powerlaw_surface_losses)

    allmodalsurface=[]
    i=0
    while i<len(bingham_surface_losses):
        allmodalsurface.append({
            'element':powerlaw_surface_losses[i]['type'],
            'id':powerlaw_surface_losses[i]['id'],
            'length':powerlaw_surface_losses[i]['length'],
            'newtonion':newtonion_surface_losses[i]['pressureloss'],
            'bingham':bingham_surface_losses[i]['pressureloss'],
            'powerlaw':powerlaw_surface_losses[i]['pressureloss'],
            # 'hershel':hershel_surface_losses[i]['pressureloss']
        })
        if(viscocity_hershel['lsryp']>0):
            allmodalsurface[i]['hershel']=hershel_surface_losses[i]['pressureloss']
        i +=1

    alldrillstringloss=[]
    allannularloss=[]
    i=0
    while i<len(newtonian_annular_pressure_loss['allpressureloss']):
        alldrillstringloss.append({
            'type':newtonian_annular_pressure_loss['allpressureloss'][i]['type'],
            'element':newtonian_annular_pressure_loss['allpressureloss'][i]['element'],
            'element_type':newtonian_annular_pressure_loss['allpressureloss'][i]['element_type'],
            'id':newtonian_annular_pressure_loss['allpressureloss'][i]['id'],
            'od':newtonian_annular_pressure_loss['allpressureloss'][i]['od'],
            'length':newtonian_annular_pressure_loss['allpressureloss'][i]['length_against'],
            'newtonion':newtonian_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
            'bingham':bingham_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
            'powerlaw':powerlaw_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
            # 'hershel':hershel_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
        })
        if(viscocity_hershel['lsryp']>0):
            alldrillstringloss[i]['hershel']=hershel_annular_pressure_loss['allpressureloss'][i]['drillstringloss']
       
        allannularloss.append({
            'type':newtonian_annular_pressure_loss['allpressureloss'][i]['type'],
            'element':newtonian_annular_pressure_loss['allpressureloss'][i]['element'],
            'element_type':newtonian_annular_pressure_loss['allpressureloss'][i]['element_type'],
            'id':newtonian_annular_pressure_loss['allpressureloss'][i]['id'],
            'od':newtonian_annular_pressure_loss['allpressureloss'][i]['od'],
            'length':newtonian_annular_pressure_loss['allpressureloss'][i]['length_against'],
            'newtonion':newtonian_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
            'bingham':bingham_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
            'powerlaw':powerlaw_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
            # 'hershel':hershel_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
        })
        if(viscocity_hershel['lsryp']>0):
            allannularloss[i]['hershel']=hershel_annular_pressure_loss['allpressureloss'][i]['pressureloss']
        i +=1
    plastic_viscocity = app_filters.getpvyp(sections,wellphase_id,'plastic_viscocity')
    yieldpoint = app_filters.getpvyp(sections,wellphase_id,'yield_point')
    data["all_annular_pressure_loss"]=allannularloss
    data["alldrillstringloss"]=alldrillstringloss
    # data["allannularloss"]=allannularloss
    data["newtonianannular"]=round(allnewtonion_pressureloss["totalannular_pressureloss"])
    data["newtoniandrillstring"]=round(allnewtonion_pressureloss["totaldrillstring_pressureloss"])
    data["allmodalsurface"]=allmodalsurface
    data["binghamannular"]=round(allbingham_pressureloss['totalannular_pressureloss'])
    data["binghamdrillstring"]=round(allbingham_pressureloss['totaldrillstring_pressureloss'])
    data["powerlawannular"]=round(allpowerlaw_pressureloss['totalannular_pressureloss'])
    data["powerlawdrillstring"]=round(allpowerlaw_pressureloss['totaldrillstring_pressureloss'])
    if(viscocity_hershel['lsryp']>0):
        data["hershelannular"]=round(allhershel_pressureloss['totalannular_pressureloss'])
        data["hersheldrillstring"]=round(allhershel_pressureloss['totaldrillstring_pressureloss'])
        data["allhershel_pressureloss"]=round(allhershel_pressureloss['totalpressure_loss']+bit_losses[0]['bit_pressure_loss'])

    else:
        data["hershelannular"]=0
        data["hersheldrillstring"]=0
        data["allhershel_pressureloss"]=0

    data['flowrate']=flowrate
    data['todepth']=sectiontodepth

    data['rpm']=rpm
    data['rop']=rop
    data['bit_losses']=bit_losses
    data['mudweight']=muddata.mud_weight
    data['selected_modal']=selected_text
    # print(f"selected_viscocity {selected_viscocity}")
    data['plastic_viscocity']=round(selected_viscocity["plastic_viscosity"],2)
    data['yieldpoint']=round(selected_viscocity["yieldpoint"],2)
    data['pv']=plastic_viscocity
    data['yp']=yieldpoint
    data['K']=round(selected_viscocity["K"],2) if 'K' in selected_viscocity else ""
    
    data['m']=round(selected_viscocity["n"],2) if 'n' in selected_viscocity else ""
    data['ty']=viscocity_hershel['lsryp']

    data["allnewtonion_pressureloss"]=round(allnewtonion_pressureloss['totalpressure_loss']+bit_losses[0]['bit_pressure_loss'])
    data["allbingham_pressureloss"]=round(allbingham_pressureloss['totalpressure_loss']+bit_losses[0]['bit_pressure_loss'])
    data["allpowerlaw_pressureloss"]=round(allpowerlaw_pressureloss['totalpressure_loss']+bit_losses[0]['bit_pressure_loss'])
    return data







def displayallmodals(rpm,flowrate,wellphase_id,section_name,well_id,muddata,wellphase,previous_wellphase,selected_viscocity,rheogramsections,sections,length_of_previous_casing_from_surface,length_of_openhole_from_bitdepth,bhadata,sectionfromdepth,sectiontodepth,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,wellphasefromdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop):
    data={}
    bit_losses=getbitpressureloss(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,
    well_id)
    if(selected_viscocity['selected_modal']=="1"):
        selected_text='Newtonion'
    elif(selected_viscocity['selected_modal']=="2"):
        selected_text='Bingham Plastic' 
    elif(selected_viscocity['selected_modal']=="3"):
        selected_text='Powerlaw' 
    elif(selected_viscocity['selected_modal']=="4"):
        selected_text='Hershel Bulkley' 


    viscocity_newtonian=calculate_viscocity_newtonian(rheogramsections,sections,muddata)
    viscocity_newtonian['selected_modal']="1"

    viscocity_bingham=calculate_viscocity_bingham(rheogramsections,sections,muddata)
    viscocity_bingham['selected_modal']="2"

    viscocity_powerlaw= calculate_viscocity_powerlaw(rheogramsections,sections,muddata)
    viscocity_powerlaw['selected_modal']="3"

    viscocity_hershel=calculate_viscocity_hershel(rheogramsections,sections,muddata)
    viscocity_hershel['selected_modal']="4"
    # viscocity_hershel['lsryp']=-6.5

    # print(f"viscocity_newtonian {viscocity_newtonian}")
    
    newtonian_annular_pressure_loss=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity_newtonian,'displayallmodelsnewtonian')
    

    newtonion_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_newtonian,'displayallmodels')
    # print(f"newtonian_annular_pressure_loss {newtonian_annular_pressure_loss['allpressureloss']}")



    bingham_annular_pressure_loss=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity_bingham,'displayallmodels')

    bingham_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_bingham,'displayallmodels')

    powerlaw_annular_pressure_loss=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity_powerlaw,'displayallmodels')

    powerlaw_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_powerlaw,'displayallmodels')
    if(viscocity_hershel['lsryp']>0):
        hershel_annular_pressure_loss=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,rop,viscocity_hershel,'displayallmodels')
        
        hershel_surface_losses=getsurfacelosses(rpm,flowrate,wellphase_id,section_name,muddata.mud_weight,wellphase,previous_wellphase,well_id,viscocity_hershel,'displayallmodels')
        allhershel_pressureloss=gettotalresult(hershel_annular_pressure_loss,hershel_surface_losses)


    else:
        hershel_annular_pressure_loss={}
        hershel_surface_losses={}
        allhershel_pressureloss={}



    allnewtonion_pressureloss=gettotalresult(newtonian_annular_pressure_loss,newtonion_surface_losses)
    allbingham_pressureloss=gettotalresult(bingham_annular_pressure_loss,bingham_surface_losses)
    allpowerlaw_pressureloss=gettotalresult(powerlaw_annular_pressure_loss,powerlaw_surface_losses)

    allmodalsurface=[]
    i=0
    while i<len(bingham_surface_losses):
        allmodalsurface.append({
            'element':powerlaw_surface_losses[i]['type'],
            'id':powerlaw_surface_losses[i]['id'],
            'length':powerlaw_surface_losses[i]['length'],
            'newtonion':newtonion_surface_losses[i]['pressureloss'],
            'bingham':bingham_surface_losses[i]['pressureloss'],
            'powerlaw':powerlaw_surface_losses[i]['pressureloss'],
            # 'hershel':hershel_surface_losses[i]['pressureloss']
        })
        if(viscocity_hershel['lsryp']>0):
            allmodalsurface[i]['hershel']=hershel_surface_losses[i]['pressureloss']
        
        i +=1
    
    # print(f"allmodalsurface {allmodalsurface}")
    
    alldrillstringloss=[]
    allannularloss=[]
    i=0
    while i<len(newtonian_annular_pressure_loss['allpressureloss']):
        alldrillstringloss.append({
            'type':newtonian_annular_pressure_loss['allpressureloss'][i]['type'],
            'element':newtonian_annular_pressure_loss['allpressureloss'][i]['element'],
            'element_type':newtonian_annular_pressure_loss['allpressureloss'][i]['element_type'],
            'id':newtonian_annular_pressure_loss['allpressureloss'][i]['id'],
            'od':newtonian_annular_pressure_loss['allpressureloss'][i]['od'],
            'length':newtonian_annular_pressure_loss['allpressureloss'][i]['length_against'],
            'newtonion':newtonian_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
            'bingham':bingham_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
            'powerlaw':powerlaw_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
            # 'hershel':hershel_annular_pressure_loss['allpressureloss'][i]['drillstringloss'],
        })
        if(viscocity_hershel['lsryp']>0):
            alldrillstringloss[i]['hershel']=hershel_annular_pressure_loss['allpressureloss'][i]['drillstringloss']
       
        allannularloss.append({
            'type':newtonian_annular_pressure_loss['allpressureloss'][i]['type'],
            'element':newtonian_annular_pressure_loss['allpressureloss'][i]['element'],
            'element_type':newtonian_annular_pressure_loss['allpressureloss'][i]['element_type'],
            'id':newtonian_annular_pressure_loss['allpressureloss'][i]['id'],
            'od':newtonian_annular_pressure_loss['allpressureloss'][i]['od'],
            'length':newtonian_annular_pressure_loss['allpressureloss'][i]['length_against'],
            'newtonion':newtonian_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
            'bingham':bingham_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
            'powerlaw':powerlaw_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
            # 'hershel':hershel_annular_pressure_loss['allpressureloss'][i]['pressureloss'],
        })
        if(viscocity_hershel['lsryp']>0):
            allannularloss[i]['hershel']=hershel_annular_pressure_loss['allpressureloss'][i]['pressureloss']
        i +=1
    plastic_viscocity = app_filters.getpvyp(sections,wellphase_id,'plastic_viscocity')
    yieldpoint = app_filters.getpvyp(sections,wellphase_id,'yield_point')
    data["all_annular_pressure_loss"]=allannularloss
    data["alldrillstringloss"]=alldrillstringloss
    # data["allannularloss"]=allannularloss
    data["newtonianannular"]=round(allnewtonion_pressureloss["totalannular_pressureloss"])
    data["newtoniandrillstring"]=round(allnewtonion_pressureloss["totaldrillstring_pressureloss"])
    data["allmodalsurface"]=allmodalsurface
    data["binghamannular"]=round(allbingham_pressureloss['totalannular_pressureloss'])
    data["binghamdrillstring"]=round(allbingham_pressureloss['totaldrillstring_pressureloss'])
    data["powerlawannular"]=round(allpowerlaw_pressureloss['totalannular_pressureloss'])
    data["powerlawdrillstring"]=round(allpowerlaw_pressureloss['totaldrillstring_pressureloss'])
    if(viscocity_hershel['lsryp']>0):
        data["hershelannular"]=round(allhershel_pressureloss['totalannular_pressureloss'])
        data["hersheldrillstring"]=round(allhershel_pressureloss['totaldrillstring_pressureloss'])
        data["allhershel_pressureloss"]=round(allhershel_pressureloss['totalpressure_loss']+bit_losses[0]['bit_pressure_loss'])

    else:
        data["hershelannular"]=0
        data["hersheldrillstring"]=0
        data["allhershel_pressureloss"]=0

    data['flowrate']=flowrate
    data['todepth']=sectiontodepth

    data['rpm']=rpm
    data['rop']=rop
    data['bit_losses']=bit_losses
    data['mudweight']=muddata.mud_weight
    data['selected_modal']=selected_text
    # print(f"selected_viscocitytestallmodal {selected_viscocity}")
    data['plastic_viscocity']=round(selected_viscocity["displaypv"],2)
    data['yieldpoint']=round(selected_viscocity["displayyp"],2) if 'displayyp' in selected_viscocity else ""
    data['pv']=plastic_viscocity
    data['yp']=yieldpoint
    data['K']=round(selected_viscocity["K"],2) if 'K' in selected_viscocity else ""
    
    data['m']=round(selected_viscocity["n"],2) if 'n' in selected_viscocity else ""
    data['ty']=viscocity_hershel['lsryp']

    data["allnewtonion_pressureloss"]=round(allnewtonion_pressureloss['totalpressure_loss']+bit_losses[0]['bit_pressure_loss'])
    data["allbingham_pressureloss"]=round(allbingham_pressureloss['totalpressure_loss']+bit_losses[0]['bit_pressure_loss'])
    data["allpowerlaw_pressureloss"]=round(allpowerlaw_pressureloss['totalpressure_loss']+bit_losses[0]['bit_pressure_loss'])
    
    return data


def gettotalresult(pressureloss,surfaceloss):
    totalpressure_loss=0
    totalannular_pressureloss=0
    totaldrillstring_pressureloss=0
    for pressurelossdata in pressureloss['allpressureloss']:
        totalpressure_loss +=pressurelossdata['pressureloss']
        totalpressure_loss +=pressurelossdata['drillstringloss']
        totalannular_pressureloss +=pressurelossdata['pressureloss']
        totaldrillstring_pressureloss +=pressurelossdata['drillstringloss']
    for surfacelossdata in surfaceloss:
        totalpressure_loss +=surfacelossdata["pressureloss"]
    
    data={
        'totalpressure_loss':totalpressure_loss,
        'totalannular_pressureloss':totalannular_pressureloss,
        'totaldrillstring_pressureloss':totaldrillstring_pressureloss
    }

    return data


def checkmudmotor(request):
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    bhadata=BhaData.objects.filter(well_phases_id=wellphase_id,status=1).first()
    checkmudmotor=BhaElement.objects.filter(bhadata_id=bhadata.id,type_name='Mud Motor')
    muddata=MudData.objects.filter(well_phase_id=wellphase_id,section=section_name,status=1).first()
    sectionfromdepth=round(muddata.from_depth)
    sectiontodepth=round(muddata.todepth)
    rangelabels=[]
    i=sectionfromdepth
    while i<sectiontodepth:
        rangelabels.append(i)
        i +=1000
    lastrange=rangelabels[-1]
    if(lastrange<sectiontodepth):
        rangelabels.append(sectiontodepth)

    response={}
    if(checkmudmotor.count()>0):
        response['status']="true"
    else:
        response['status']="false"
    response['sectionfromdepth']=sectionfromdepth
    response['sectiontodepth']=sectiontodepth
    response['rangelabels']=rangelabels

    return JsonResponse(response,safe=False)
   

def calculatepressloss(well_id,rpm,flowrate,mudweight,identity,length,viscocity,typename):
    unit = getprojectunit(well_id)
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



def getallpressurelosschartdataold(bore_pressure_loss,annular_pressure_loss,surface_losses,bit_losses,previous_wellphase,rpm,flowrate,muddata,bhadata,sectiontodepth,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,linercount,checkliner,wellphase_id,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity):
    pressurelosschartdata=[]
    drillstringdata=[]
    surfaceloss =sum(surface['pressureloss'] for surface in surface_losses)
    drillstringloss=sum(annularloss['drillstringloss'] for annularloss in annular_pressure_loss)
    annularloss=sum(annularloss['pressureloss'] for annularloss in annular_pressure_loss)
    bitloss=sum(bit['bit_pressure_loss'] for bit in bit_losses)
    # surfaceloss = float(surface_losses)
    # drillstringloss = float(drillstring_value)
    # annularloss = float(annular_pressure_loss)
    # bitloss = float(bit_losses)
    print('flowrate',flowrate)
    print('allloss',surfaceloss,drillstringloss,annularloss,bitloss)

    totalpressureloss=surfaceloss+drillstringloss+annularloss+bitloss
    
    print('flowrate',flowrate,'surfaceloss',surfaceloss,'drillstringloss',drillstringloss,'annularloss',annularloss,'bitloss',bitloss,'totalloss',totalpressureloss)
    # print(bore_pressure_loss,previous_wellphase,rpm,flowrate,muddata,bhadata,sectiontodepth,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,linercount,checkliner,wellphase_id,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity)

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
        
    print(f"drillstringdata {drillstringdata}")
    for alldata in drillstringdata:
       
        pressurelosschartdata.append({"x":round(alldata["loss_alongwell"]),"y":alldata["MD"]})

    return pressurelosschartdata




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

def calculatetjpressurelossliner(length,alllinerdata,bhadata,rpm,flowrate,viscocity,mud_weight,hole_size,id_of_previous_casing,checkliner):
    well_id = bhadata.bhadata.well_id
    unit=getprojectunit(well_id)
    length_of_drillpipebody=float(bhadata.onejoint_length)
    tjpressureloss=0
    tjannularloss=0
    length_of_boxtj=float(bhadata.box_tj_length)
    length_of_pintj=float(bhadata.pin_tj_length)
    noof_pipe_casing=alllinerdata["length_inside_casing"]/length_of_drillpipebody
    noof_pipe_openhole=alllinerdata["length_inside_openhole"]/length_of_drillpipebody
    noof_tj_casing=noof_pipe_casing*2
    noof_tj_openhole=noof_pipe_openhole*2
    casing_box_number=noof_tj_casing/2
    # casing_box_length=length_of_boxtj*casing_box_number/12
    casing_box_length=convert_box_pin(length_of_boxtj,casing_box_number,unit)
    casing_pin_number=noof_tj_casing-casing_box_number
    # casing_pin_length=length_of_pintj*casing_pin_number/12
    casing_pin_length=convert_box_pin(length_of_pintj,casing_pin_number,unit)
    openhole_box_number=noof_tj_openhole/2
    # openhole_box_length=length_of_boxtj*openhole_box_number/12
    openhole_box_length=convert_box_pin(length_of_boxtj,openhole_box_number,unit)
    openhole_pin_number=noof_tj_openhole-openhole_box_number
    # openhole_pin_length=length_of_pintj*openhole_pin_number/12
    openhole_pin_length=convert_box_pin(length_of_pintj,openhole_pin_number,unit)
    i=1
    for liner in checkliner:
        noof_pipe_liner=alllinerdata["length_inside_liner"+str(i)]/length_of_drillpipebody
        noof_tj_liner=noof_pipe_liner*2
        liner_box_number=noof_tj_liner/2
        liner_box_length=length_of_boxtj*liner_box_number/12
        liner_pin_number=noof_tj_liner-liner_box_number
        liner_pin_length=length_of_pintj*liner_pin_number/12
        liner_pin_pressureloss=calculatepressloss(well_id,rpm,flowrate,mud_weight,bhadata.tool_id,liner_pin_length,viscocity,'calculatetjpressurelossliner')
        liner_box_pressureloss=calculatepressloss(well_id,rpm,flowrate,mud_weight,bhadata.tool_id,liner_box_length,viscocity,'calculatetjpressurelossliner')

        liner_pin_annular=calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,bhadata.tool_od,hole_size,openhole_pin_length)
        liner_box_annular=calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,bhadata.tool_od,hole_size,openhole_box_length)



        i +=1


    openhole_pin_pressureloss=calculatepressloss(well_id,rpm,flowrate,mud_weight,bhadata.tool_id,openhole_pin_length,viscocity,'calculatetjpressurelossliner')
    openhole_box_pressureloss=calculatepressloss(well_id,rpm,flowrate,mud_weight,bhadata.tool_id,openhole_box_length,viscocity,'calculatetjpressurelossliner')

    casing_pin_pressureloss=calculatepressloss(well_id,rpm,flowrate,mud_weight,bhadata.tool_id,casing_pin_length,viscocity,'calculatetjpressurelossliner')
    casing_box_pressureloss=calculatepressloss(well_id,rpm,flowrate,mud_weight,bhadata.tool_id,casing_box_length,viscocity,'calculatetjpressurelossliner')




    
    openhole_pin_annular=calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,bhadata.tool_od,hole_size,openhole_pin_length)
    openhole_box_annular=calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,bhadata.tool_od,hole_size,openhole_box_length)

    casing_pin_annular=calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,bhadata.tool_od,id_of_previous_casing,casing_pin_length)
    casing_box_annular=calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,bhadata.tool_od,id_of_previous_casing,casing_box_length)


  


    data={
        'tjpressureloss':casing_pin_pressureloss['pressureloss']+casing_box_pressureloss['pressureloss']+openhole_pin_pressureloss['pressureloss']+openhole_box_pressureloss['pressureloss'],
        'tjannularloss':openhole_pin_annular['pressureloss']+openhole_box_annular['pressureloss']+casing_pin_annular['pressureloss']+casing_box_annular['pressureloss']

    }
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

def calculatetjpressure(bhalength,length,bhadata,rpm,flowrate,viscocity,mud_weight,cased_hole_size,typename):
    data={}
    data['tjpressureloss']=0
    data['tjannularloss']=0
    return data



def calculate_annular_loss(well_id,viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,typename):
    # print(f'mud_weight {mud_weight}')
    unit = getprojectunit(well_id)
    if(viscocity['selected_modal']=="4"):
        pressureloss=calculate_hersel_annular(viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,typename,unit)
    elif(viscocity['selected_modal']=="3"):
        pressureloss=calculate_powerlaw_annular(viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,unit)
    elif(viscocity['selected_modal']=="2"):
        pressureloss=calculate_bingham_annular(viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,typename,unit)
    else:
        # print("vdgf")
        pressureloss=calculate_newtonian_annular(viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,unit)

    # print(f"pressureloss {pressureloss}")

    return pressureloss



def calculate_powerlaw_annular(viscocity,flowrate,rpm,mud_weight,od_of_pipe_element,casing_hole_size,length,unit):
    k=viscocity['K']
    m=viscocity['n']
    n=m
    K=k*0.4788*1.066  
    # print(f'K {K}')
    print(f"n {n}")
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
    print(f'Re {Re}')

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
    if(typename=='annularpressureloss_liner'):
        print(f"pressurelosslinernew {pressureloss}")
        print(f"fclinernew {fc}")
        print(f"casing_hole_size_silinernew {casing_hole_size_si}")
        print(f"od_of_pipe_element_silinernew {od_of_pipe_element_si}")



    
    pressureloss=pressureloss_conversion(pressureloss,unit)
    data={
        'pressureloss':pressureloss,
        'flowregime':flowregime,
        'id':casing_hole_size,
        'length':length,
        'od':od_of_pipe_element
    }
    return data



def calculate_drillstringloss_downholetools(bhaelement,flowrate,mudweight,torque,wob):
    calculationtype=bhaelement.calculation_type
    type_name=bhaelement.type_name
    specification=Specifications.objects.filter(bhadata_element_id=bhaelement.id).first()
    allpressuredrop={}
    if(type_name!='Mud Motor'):
        if(calculationtype==1):
            pressuredroptool=Pressuredroptool.objects.filter(bhadata_element_id=bhaelement.id)
            allflowrate=[]
            pressuredrop=[]
        
            for pressure in pressuredroptool:
                allflowrate.append(pressure.flowrate)
                pressuredrop.append(pressure.pressure_drop)
            pressuredroptool=Pressuredroptool.objects.filter(bhadata_element_id=bhaelement.id,flowrate=flowrate).first()
            interpolation = interpolate.interp1d(allflowrate, pressuredrop,fill_value='extrapolate')
            pressuredrop=interpolation(flowrate)
            pressuredrop=pressuredrop.tolist()
            allpressuredrop['pressuredrop']=pressuredrop

        elif(calculationtype==2):
            empiricaldata=Empirical.objects.filter(bhadata_element_id=bhaelement.id).first()
            ID=float(bhaelement.identity)
            empirical_formula=empiricaldata.formula_python_text
            empirical_formula=empirical_formula.replace('mudweight',str(mudweight))
            empirical_formula=empirical_formula.replace('flowrate',str(flowrate))
            empirical_formula=empirical_formula.replace('ID',str(bhaelement.identity))
            empirical_formula=empirical_formula.replace('²',('**2'))
            empirical_formula=empirical_formula.replace('³',('**3'))
            pressuredrop=eval(empirical_formula)
            allpressuredrop['pressuredrop']=pressuredrop
    else:
        alldifferential_pressure=[]
        alltorque=[]
        differential_pressure=Differential_pressure.objects.filter(bhadata_element_id=bhaelement.id)
        for pressure in differential_pressure:
            alldifferential_pressure.append(pressure.diff_pressure)
            alltorque.append(pressure.torque)
        interpolation = interpolate.interp1d(alltorque, alldifferential_pressure)   
        pressuredrop=interpolation(torque).tolist()
        if(wob==0):
            pressureloss=0
        else:
            if(float(wob)/specification.max_wob<1):
                pressureloss=specification.no_load_diff_pressure+float(wob)/specification.max_wob*pressuredrop
            else:
                pressureloss=specification.max_dp-specification.no_load_diff_pressure
        allpressuredrop['pressuredrop']=pressureloss
    return allpressuredrop

def calculate_drillstringloss_splitcasing(rpm,flowrate,viscocity,mud_weight,identity,length_against_casing,length_against_open_hole):
    data={}
    openholesrillstring_loss=calculatepressloss(well_id,rpm,flowrate,mud_weight,identity,length_against_open_hole,viscocity,'calculate_drillstringloss_splitcasing')
    data["pressureloss_openhole"]=openholesrillstring_loss['pressureloss']
    casedholesrillstring_loss=calculatepressloss(well_id,rpm,flowrate,mud_weight,identity,length_against_casing,viscocity,'calculate_drillstringloss_splitcasing')
    data["pressureloss_openhole"]=openholesrillstring_loss['pressureloss']
    data["pressureloss_casedhole"]=casedholesrillstring_loss['pressureloss']
    return data


#calculate drill string loss based on length split
def calculate_drillstringloss_split(alllinerdata,rpm,flowrate,viscocity,mud_weight,type_name,identity,checkliner):
    data={}
    openholesrillstring_loss=calculatepressloss(well_id,wellrpm,flowrate,mud_weight,identity,alllinerdata['length_inside_openhole'],viscocity,'calculate_drillstringloss_split')
    data["pressureloss_openhole"]=openholesrillstring_loss['pressureloss']
    casedholesrillstring_loss=calculatepressloss(well_id,rpm,flowrate,mud_weight,identity,alllinerdata['length_inside_casing'],viscocity,'calculate_drillstringloss_split')
    data["pressureloss_casedhole"]=casedholesrillstring_loss['pressureloss']

    i=1
    for liner in checkliner:
        linersrillstring_loss=calculatepressloss(well_id,rpm,flowrate,mud_weight,identity,alllinerdata['length_inside_liner'+str(i)],viscocity,'calculate_drillstringloss_split')
        data["pressureloss_liner"+str(i)]=linersrillstring_loss['pressureloss']
        i +=1
    return data
    
#calculate pressure loss for liner
def calculateannular_pressureloss_liner(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,linercount,wellphase_id,checkliner,well_id,cuttings_density,cuttings_size,torque,wob,rop,viscocity,typename):
    # print(f"typename {typename}")
    allpressureloss=[]
    increased_pressureloss=[]
    length_of_open_hole=length_of_selected_section_from_surface-length_of_previous_casing_from_surface
    allbha=BhaElement.objects.getbhaelement(bhadata.id)
    i=0
    bhacount=allbha.count()
    cumulative_length=0
    sum_length_inside_casing=0
    previous_length=0
    linerdata={}
    alllinerdata=[]
    allslipvelocity=[]
    slipvelocitychart=[]
    annularvelocitychartdata=[]
    # viscocity=getviscocity(muddata)
    bitelement=BhaElement.objects.filter(bhadata_id=bhadata.id,type_name='Bit',status=1).first()

    cumlativelength=0
    for bha in allbha:
        #calculation for one liner
        # print(bha.element)
        if(linercount<=1):
            length_float=converttofloat(bha.length)
            liner=WellPhases.objects.filter(Q(casing_type_id=7) | Q(casing_type_id=8) | Q(casing_type_id=11) | Q(casing_type_id=12)).filter(measured_depth__lt=sectiontodepth,well_id=well_id,status=1).first()
            if(i==0):
                cumulative_length=cumulative_length+converttofloat(bha.length)
                if(length_float<=liner.lineartop):
                    length_inside_casing=length_float
                else:
                    length_inside_casing= liner.lineartop if(length_float>liner.lineartop and length_float<=liner.measured_depth) else liner.lineartop
            
                if(length_inside_casing>=length_float):
                    length_inside_linear=0
                else:
                    if(length_float<=liner.measured_depth):
                        length_inside_linear=length_float-length_inside_casing
                    else:
                        length_inside_linear=liner.measured_depth-length_inside_casing

                if(length_float<=liner.measured_depth):
                    length_inside_openhole=0
                else:
                    length_inside_openhole=length_float-(length_inside_casing+length_inside_linear)
                sum_length_inside_casing +=length_inside_casing
                previous_length +=converttofloat(bha.length)
                previous_linear_value=length_inside_linear
                alllinerdata={
                    'type':bha.type_name+str(i),
                    'length_inside_casing':length_inside_casing,
                    'length_inside_openhole':length_inside_openhole,
                    'length_inside_liner1':length_inside_linear
                }
               
            else:
                cumulative_length=cumulative_length+converttofloat(bha.length)
                if(sum_length_inside_casing<=liner.lineartop and cumulative_length<=liner.lineartop):
                    length_inside_casing=length_float
                else:
                    if(sum_length_inside_casing<liner.lineartop and cumulative_length>liner.lineartop):
                        length_inside_casing=liner.lineartop-previous_length
                    else:
                        length_inside_casing=0
                
                if(cumulative_length<=liner.lineartop or previous_length>liner.measured_depth):
                    length_inside_linear=0
                else:
                    if(previous_linear_value==0 and cumulative_length<=liner.measured_depth):
                        length_inside_linear=cumulative_length-liner.lineartop
                    else:
                        if(previous_linear_value==0 and cumulative_length>liner.measured_depth):
                            length_inside_linear=liner.measured_depth-liner.lineartop
                        else:
                            if(previous_linear_value>0 and cumulative_length<=liner.measured_depth):
                                length_inside_linear=length_float
                            else:
                                length_inside_linear = liner.measured_depth-previous_length
                if((length_float-length_inside_casing-length_inside_linear)<0):
                    length_inside_openhole=0
                else:
                    length_inside_openhole=length_float-length_inside_casing-length_inside_linear
            
                previous_linear_value=length_inside_linear
                previous_length +=converttofloat(bha.length)
                sum_length_inside_casing +=length_inside_casing
                alllinerdata={
                    'type':bha.type_name+str(i),
                    'length_inside_casing':length_inside_casing,
                    'length_inside_openhole':length_inside_openhole,
                    'length_inside_liner1':length_inside_linear
                }
                
        #multiple liner calculation
        else:
            length_float=converttofloat(bha.length)
            liner=WellPhases.objects.filter(Q(casing_type_id=7) | Q(casing_type_id=8) | Q(casing_type_id=11) | Q(casing_type_id=12)).filter(measured_depth__lt=sectiontodepth,well_id=well_id,status=1).first()
            #liner calculation for first element from last
            if(i==0):
                if(length_float<=liner.lineartop):
                    length_inside_casing=length_float
                else:
                    if(length_float>liner.lineartop and length_float<=liner.measured_depth):
                        length_inside_casing=liner.lineartop
                    else:
                        length_inside_casing=liner.lineartop
                j=1
                for liner in checkliner:
                    if(j==1):
                        nextliner=WellPhases.objects.filter(Q(casing_type_id=7) | Q(casing_type_id=8) | Q(casing_type_id=11) | Q(casing_type_id=12)).filter(id__gt=liner.id).first()
                        if(length_inside_casing<liner.lineartop):
                            linerdata['length_inside_liner'+str(j)] = 0
                        else:
                            if(length_float<=nextliner.lineartop):
                                linerdata['length_inside_liner'+str(j)] = length_float-liner.lineartop

                            else:
                                linerdata['length_inside_liner'+str(j)] = nextliner.lineartop-liner.lineartop

                    else:
                        if(length_float<=liner.lineartop):
                            linerdata['length_inside_liner'+str(j)] = 0
                        else:
                            if(length_float<=liner.measured_depth):
                                linerdata['length_inside_liner'+str(j)] = length_float-liner.lineartop
                            else:
                                linerdata['length_inside_liner'+str(j)] = liner.measured_depth-liner.lineartop  

                    j +=1
                lastliner=WellPhases.objects.filter(Q(casing_type_id=7) | Q(casing_type_id=8) | Q(casing_type_id=11) | Q(casing_type_id=12)).filter(measured_depth__lt=sectiontodepth,well_id=well_id,status=1).order_by('-id').first()
                if(length_float<=lastliner.measured_depth):
                    length_inside_openhole=0
                else:
                    length_inside_openhole=length_float-lastliner.measured_depth

                cumulative_length=cumulative_length+converttofloat(bha.length)
                previous_length +=converttofloat(bha.length)
                sum_length_inside_casing +=length_inside_casing
                alllinerdata.append={
                    'type':bha.type_name+str(i),
                    'length_inside_casing':length_inside_casing,
                    'length_inside_openhole':length_inside_openhole
                }
                for key, value in linerdata.items():
                    alllinerdata[key]=value
            #calculate liner loss for other bha element
            else:
                cumulative_length=cumulative_length+converttofloat(bha.length)
                if(sum_length_inside_casing<=liner.lineartop and cumulative_length<=liner.lineartop):
                    length_inside_casing=length_float
                else:
                    if(sum_length_inside_casing<liner.lineartop and cumulative_length>liner.lineartop):
                        length_inside_casing=liner.lineartop-previous_length
                    else:
                        length_inside_casing=0

                j=1
                previous_liner_values=0
                for liner in checkliner:
                    nextliner=WellPhases.objects.filter(Q(casing_type_id=7) | Q(casing_type_id=8) | Q(casing_type_id=11) | Q(casing_type_id=12)).filter(id__gt=liner.id,well_id=well_id,status=1).first()
                    if(j==1):
                        if(cumulative_length<=liner.lineartop):
                            linerdata['length_inside_liner'+str(j)] = 0
                        else:
                            if(cumulative_length<=nextliner.lineartop):
                                linerdata['length_inside_liner'+str(j)] = cumulative_length-previous_length
                            else:
                                if(nextliner.lineartop-previous_length<=0):
                                    linerdata['length_inside_liner'+str(j)] = 0
                                else:
                                    linerdata['length_inside_liner'+str(j)] = nextliner.lineartop-previous_length-length_inside_casing
                        previous_liner_values +=linerdata['length_inside_liner'+str(j)]
                    else:
                        if(cumulative_length<=liner.lineartop):
                            linerdata['length_inside_liner'+str(j)] = 0
                        else:
                            if(previous_length>liner.measured_depth):
                                linerdata['length_inside_liner'+str(j)] = 0
                            else:
                                if(cumulative_length<=liner.measured_depth):
                                    linerdata['length_inside_liner'+str(j)] = length_float-length_inside_casing-previous_liner_values
                                else:
                                    linerdata['length_inside_liner'+str(j)]=liner.measured_depth-previous_length-length_inside_casing-previous_liner_values
                        previous_liner_values +=linerdata['length_inside_liner'+str(j)]
                    j +=1
                alllinervalue=0
                for k in range(len(checkliner)):
                    alllinervalue +=linerdata['length_inside_liner'+str(k+1)]
                if(length_float-length_inside_casing-alllinervalue<0):
                    length_inside_openhole=0
                else:
                    length_inside_openhole=length_float-length_inside_casing-alllinervalue
                sum_length_inside_casing +=length_inside_casing
                previous_length +=converttofloat(bha.length)
                alllinerdata={
                    'type':bha.type_name+str(i),
                    'length_inside_casing':length_inside_casing,
                    'length_inside_openhole':length_inside_openhole
                }
                for key, value in linerdata.items():
                    alllinerdata[key]=value
        print(f"alllinerdata {alllinerdata}")
        if(alllinerdata["length_inside_casing"]!=0):
            cumlativelength +=alllinerdata["length_inside_casing"]
            pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,muddata.mud_weight,bha.od,id_of_previous_casing,alllinerdata["length_inside_casing"],'annularpressureloss_liner')
            # print(f"typename {bha.type_name}")
            # print(f"pressureloss {pressureloss}")
            if((bha.type_name=='RSS') or (bha.type_name=='MWD') or (bha.type_name=='LWD') or (bha.type_name=='Others') or (bha.type_name=='Mud Motor')):
                drillstringpressureloss=calculate_drillstringloss_downholetools(bha,flowrate,muddata.mud_weight,torque,wob)
            else:
                drillstringpressureloss=calculatepressloss(well_id,rpm,flowrate,muddata.mud_weight,bha.identity,alllinerdata["length_inside_casing"],viscocity,'calculateannular_pressureloss_liner')
            
            slipvelocity=calculateslipvelocitywithoutliner(well_id,rpm,flowrate,muddata.mud_weight,id_of_previous_casing,bha.od,viscocity,cuttings_density,cuttings_size,alllinerdata["length_inside_casing"])
            slipvelocitywalker= slipvelocity_walker(muddata,id_of_previous_casing,rpm,bha.od,cuttings_density,cuttings_size,flowrate)

            if(slipvelocity["slipvelocity"]>=slipvelocitywalker["slipvelocity"]):
                slipvelocityvalue=slipvelocity["slipvelocity"]
            else:
                slipvelocityvalue=slipvelocitywalker["slipvelocity"]

            slipvelocitychart.append({'x':slipvelocityvalue,"y":cumlativelength,'od':bha.od,'cased_hole_size':id_of_previous_casing,'annular_velocity':round(slipvelocity["annular_velocity"]),'element_type':'CH'})
            annularvelocitychartdata.append({"x":slipvelocity["annular_velocity"],"y":cumlativelength})
            
            increased_mudweight=calculate_increased_mudweight(well_id,flowrate,id_of_previous_casing,bha.od,rop,slipvelocityvalue,muddata.mud_weight,cuttings_density)

            increased_pressurelossvalue=calculate_annular_loss(well_id,viscocity,flowrate,rpm,increased_mudweight["increased_mudweight"],bha.od,id_of_previous_casing,alllinerdata["length_inside_casing"],'annularpressureloss_liner_increased')

            if((bha.type_name=='Drill Pipe') or (bha.type_name=='Heavy Weight Drill Pipe')):
                calculate_tj_pressureloss=calculatetjpressureloss(bha.length,alllinerdata["length_inside_casing"],bha,rpm,flowrate,viscocity,muddata.mud_weight,id_of_previous_casing,'withoutcheck')
                
                # print(f"calculate_tj_pressureloss {calculate_tj_pressureloss}")
                
                calculate_tj_pressureloss_increased=calculatetjpressureloss(bha.length,alllinerdata["length_inside_casing"],bha,rpm,flowrate,viscocity,increased_mudweight["increased_mudweight"],id_of_previous_casing,'with')
                

            allpressureloss.append({
                'flowregime' : pressureloss["flowregime"],
                'od':round(converttofloat(bha.od),2),
                'id':round(converttofloat(bha.identity),2),
                'type':bha.type_name,
                'element':bha.element,
                'length_against':alllinerdata["length_inside_casing"],
                'pressureloss':round(pressureloss["pressureloss"]+calculate_tj_pressureloss["tjannularloss"],2),
                'element_type':'CH',
                'drillstringloss':round(drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"],2)  if 'pressureloss' in drillstringpressureloss else drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"],
                'mudweight':muddata.mud_weight,
                'cumlativelength':cumlativelength


            })

            increased_pressureloss.append({
                'flowregime' : increased_pressurelossvalue["flowregime"],
                'od':round(converttofloat(bha.od),2),
                'id':round(converttofloat(bha.identity),2),
                'type':bha.type_name,
                'element':bha.element,
                'length_against':alllinerdata["length_inside_casing"],
                'pressureloss':round(increased_pressurelossvalue["pressureloss"]+calculate_tj_pressureloss_increased["tjannularloss"],2),
                'element_type':'CH',
                'mudweight':increased_mudweight["increased_mudweight"]
            })
        
        j=1
        for liner in checkliner:
            if(alllinerdata["length_inside_liner"+str(j)]!=0):
                cumlativelength +=alllinerdata["length_inside_liner"+str(j)]
                if((bha.type_name=='RSS') or (bha.type_name=='MWD') or (bha.type_name=='LWD') or (bha.type_name=='Others') or (bha.type_name=='Mud Motor')):
                    drillstringpressureloss=calculate_drillstringloss_downholetools(bha,flowrate,muddata.mud_weight,torque,wob)
                else:
                    drillstringpressureloss=calculatepressloss(well_id,rpm,flowrate,muddata.mud_weight,bha.identity,alllinerdata["length_inside_liner"+str(j)],viscocity,'calculateannular_pressureloss_liner')
                
                pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,muddata.mud_weight,bha.od,liner.drift_id,alllinerdata["length_inside_liner"+str(j)],'annularpressureloss_liner')

                slipvelocity=calculateslipvelocitywithoutliner(well_id,rpm,flowrate,muddata.mud_weight,liner.drift_id,bha.od,viscocity,cuttings_density,cuttings_size,alllinerdata["length_inside_liner"+str(j)])

                slipvelocitywalker= slipvelocity_walker(muddata,liner.drift_id,rpm,bha.od,cuttings_density,cuttings_size,flowrate)

                if(slipvelocity["slipvelocity"]>=slipvelocitywalker["slipvelocity"]):
                    slipvelocityvalue=slipvelocity["slipvelocity"]
                else:
                    slipvelocityvalue=slipvelocitywalker["slipvelocity"]
                
                slipvelocitychart.append({'x':slipvelocityvalue,"y":cumlativelength,'od':bha.od,'cased_hole_size':liner.drift_id,'annular_velocity':round(slipvelocity["annular_velocity"]),'element_type':'LI'})
                annularvelocitychartdata.append({"x":slipvelocity["annular_velocity"],"y":cumlativelength})
                
                increased_mudweight=calculate_increased_mudweight(well_id,flowrate,liner.drift_id,bha.od,rop,slipvelocityvalue,muddata.mud_weight,cuttings_density)

                increased_pressurelossvalue=calculate_annular_loss(well_id,viscocity,flowrate,rpm,increased_mudweight["increased_mudweight"],bha.od,liner.drift_id,alllinerdata["length_inside_liner"+str(j)],'annularpressureloss_liner')

                if((bha.type_name=='Drill Pipe') or (bha.type_name=='Heavy Weight Drill Pipe')):
                    calculate_tj_pressureloss=calculatetjpressureloss(bha.length,alllinerdata["length_inside_liner"+str(j)],bha,rpm,flowrate,viscocity,muddata.mud_weight,liner.drift_id,'without')
                    
                    calculate_tj_pressureloss_increased=calculatetjpressureloss(bha.length,alllinerdata["length_inside_liner"+str(j)],bha,rpm,flowrate,viscocity,increased_mudweight["increased_mudweight"],liner.drift_id,'with')


                allpressureloss.append({
                    'flowregime' : pressureloss["flowregime"],
                    'od':round(converttofloat(bha.od),2),
                    'id':round(converttofloat(bha.identity),2),
                    'type':bha.type_name,
                    'element':bha.element,
                    'length_against':alllinerdata["length_inside_liner"+str(j)],
                    'pressureloss':round(pressureloss['pressureloss']+calculate_tj_pressureloss['tjannularloss'],2),
                    'element_type':'LI',
                    'drillstringloss':round(drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"],2) if 'pressureloss' in drillstringpressureloss else
                    drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"],
                    'mudweight':muddata.mud_weight,
                    'cumlativelength':cumlativelength


                })
                increased_pressureloss.append({
                    'flowregime' : increased_pressurelossvalue["flowregime"],
                    'od':round(converttofloat(bha.od),2),
                    'id':round(converttofloat(bha.identity),2),
                    'type':bha.type_name,
                    'element':bha.element,
                    'length_against':alllinerdata["length_inside_liner"+str(j)],
                    'pressureloss':round(increased_pressurelossvalue["pressureloss"]+calculate_tj_pressureloss_increased['tjannularloss'],2),
                    'element_type':'CH',
                    'mudweight':increased_mudweight["increased_mudweight"]
                })
            j +=1

        
        if(alllinerdata["length_inside_openhole"]!=0):
            cumlativelength +=alllinerdata["length_inside_openhole"]
            # print(f"typename {bha.type_name}")
            pressureloss=calculate_annular_loss(well_id,viscocity,flowrate,rpm,muddata.mud_weight,bha.od,hole_size,alllinerdata["length_inside_openhole"],'annularpressureloss_liner')
            print(f"pressurelossliner {pressureloss}")
            if((bha.type_name=='RSS') or (bha.type_name=='MWD') or (bha.type_name=='LWD') or (bha.type_name=='Others') or (bha.type_name=='Mud Motor')):
                drillstringpressureloss=calculate_drillstringloss_downholetools(bha,flowrate,muddata.mud_weight,torque,wob)
            else:
                drillstringpressureloss=calculatepressloss(well_id,rpm,flowrate,muddata.mud_weight,bha.identity,alllinerdata["length_inside_openhole"],viscocity,'calculateannular_pressureloss_liner')
            
            slipvelocity=calculateslipvelocitywithoutliner(well_id,rpm,flowrate,muddata.mud_weight,hole_size,bha.od,viscocity,cuttings_density,cuttings_size,alllinerdata["length_inside_openhole"])
            
            slipvelocitywalker= slipvelocity_walker(muddata,hole_size,rpm,bha.od,cuttings_density,cuttings_size,flowrate)

            if(slipvelocity["slipvelocity"]>=slipvelocitywalker["slipvelocity"]):
                slipvelocityvalue=slipvelocity["slipvelocity"]
            else:
                slipvelocityvalue=slipvelocitywalker["slipvelocity"]
            
            slipvelocitychart.append({'x':slipvelocityvalue,"y":cumlativelength,'od':bha.od,'cased_hole_size':hole_size,'annular_velocity':round(slipvelocity["annular_velocity"]),'element_type':'OH'})
            annularvelocitychartdata.append({"x":slipvelocity["annular_velocity"],"y":cumlativelength})

            increased_mudweight=calculate_increased_mudweight(well_id,flowrate,hole_size,bha.od,rop,slipvelocityvalue,muddata.mud_weight,cuttings_density)

            increased_pressurelossvalue=calculate_annular_loss(well_id,viscocity,flowrate,rpm,increased_mudweight["increased_mudweight"],bha.od,hole_size,alllinerdata["length_inside_openhole"],'annularpressureloss_liner_increased')

            if((bha.type_name=='Drill Pipe') or (bha.type_name=='Heavy Weight Drill Pipe')):
                calculate_tj_pressureloss=calculatetjpressureloss(bha.length,alllinerdata["length_inside_openhole"],bha,rpm,flowrate,viscocity,muddata.mud_weight,hole_size,'without')
                
                calculate_tj_pressureloss_increased=calculatetjpressureloss(bha.length,alllinerdata["length_inside_openhole"],bha,rpm,flowrate,viscocity,increased_mudweight["increased_mudweight"],hole_size,'with')

            allpressureloss.append({
                'flowregime' : pressureloss["flowregime"],
                'od':round(converttofloat(bha.od),2),
                'id':round(converttofloat(bha.identity),2),
                'type':bha.type_name,
                'element':bha.element,
                'length_against':alllinerdata["length_inside_openhole"],
                'pressureloss':round(pressureloss["pressureloss"]+calculate_tj_pressureloss['tjannularloss'],2),
                'element_type':'OH',
                'drillstringloss':round(drillstringpressureloss["pressureloss"]+calculate_tj_pressureloss["tjpressureloss"],2) if 'pressureloss' in drillstringpressureloss else drillstringpressureloss['pressuredrop']+calculate_tj_pressureloss["tjpressureloss"],
                'mudweight':muddata.mud_weight,
                'cumlativelength':cumlativelength


            })

            increased_pressureloss.append({
                'flowregime' : increased_pressurelossvalue["flowregime"],
                'od':round(converttofloat(bha.od),2),
                'id':round(converttofloat(bha.identity),2),
                'type':bha.type_name,
                'element':bha.element,
                'length_against':alllinerdata["length_inside_openhole"],
                'pressureloss':round(increased_pressurelossvalue["pressureloss"]+calculate_tj_pressureloss_increased['tjannularloss'],2),
                'element_type':'CH',
                'mudweight':increased_mudweight["increased_mudweight"]
            })






        # slipvelocity=calculateslipvelocity(alllinerdata,rpm,flowrate,muddata.mud_weight,hole_size,bha.od,viscocity,bha.type_name+str(i),id_of_previous_casing,checkliner,cuttings_density,cuttings_size)
        # allslipvelocity.append(slipvelocity)
        # if((bha.type_name=='Drill Pipe') or (bha.type_name=='Heavy Weight Drill Pipe')):
        #     calculate_tj_pressureloss=calculatetjpressurelossliner(bha.length,alllinerdata,bha,rpm,flowrate,viscocity,muddata.mud_weight,hole_size,id_of_previous_casing,checkliner)

        i +=1

    cuttingsconcentration=calculatecuttings_concentration(well_id,flowrate,rop,slipvelocitychart,bitelement,sectiontodepth)
    # print(f"cuttingsconcentration {cuttingsconcentration}")
   
    # print(f"allpressureloss {allpressureloss['pressureloss']}")

    data={
        'allpressureloss':allpressureloss,
        'slipvelocitychart':slipvelocitychart,
        'annularvelocitychartdata':annularvelocitychartdata,
        'increased_pressureloss':increased_pressureloss,
        'cuttingsconcentration':cuttingsconcentration,
    }
    # print(f"annulardata {data}")
    if(typename != 'displayallmodelsliner'):
        transportratio=calculatetransportratio(well_id,slipvelocitychart,viscocity,flowrate)
        cci=calculatecci(well_id,slipvelocitychart,viscocity,flowrate,muddata.mud_weight)
        data['transportratio']=transportratio
        data['cci']=cci

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




        
def calculate_pressureloss_liner(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,alllinerdata,typename,linercount,checkliner,wellphasetodepth):
    if(viscocity['selected_modal']=="1"):
        pressureloss=calculate_newtonian_linerpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,alllinerdata,typename,linercount,checkliner)
    elif(viscocity['selected_modal']=="2"):
        pressureloss=calculate_bingham_linerpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,alllinerdata,typename,linercount,checkliner,wellphasetodepth)
    if(viscocity['selected_modal']=="4"):
        pressureloss=calculate_hershel_linerpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,alllinerdata,typename,linercount,checkliner,wellphasetodepth)
    if(viscocity['selected_modal']=="3"):
        pressureloss=calculate_powerlaw_linerpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,alllinerdata,typename,linercount,checkliner,wellphasetodepth)
    return pressureloss

#calculate newtonian annulus pressure loss
def calculate_newtonian_linerpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,alllinerdata,typename,linercount,checkliner):
    index = next((index for (index, d) in enumerate(alllinerdata) if d["type"] == typename), None)

    data={}

    length_against_open_hole=alllinerdata[index]['length_inside_openhole']/3.281
    length_against_casing=alllinerdata[index]['length_inside_casing']/3.281
    viscocity_si=viscocity['plastic_viscosity']
    flowrate_si=flowrate*0.000063
    mudweight_si=mud_weight/8.33*1000
    rpm_si=int(rpm)*2*pi/60
    od_of_pipe_element_si=converttofloat(od_of_pipe_element)/12/3.281
    hole_size_si=hole_size/12/3.281
    id_of_previous_casing_si=id_of_previous_casing/12/3.281
    length_of_previous_casing_from_surface_si=length_of_previous_casing_from_surface/3.281
    length_of_open_hole_si=length_of_open_hole/3.281
    bitdepth_si=bitdepth/3.281
    length_of_openhole_from_bitdepth_si=length_of_openhole_from_bitdepth/3.281
    U_oh=flowrate_si/(pi/4*(hole_size_si**2-od_of_pipe_element_si**2))
    U_ch=flowrate_si/(pi/4*(id_of_previous_casing_si**2-od_of_pipe_element_si**2))
    D_eq_oh=(hole_size_si**2+od_of_pipe_element_si**2-(hole_size_si**2-od_of_pipe_element_si**2)/log(hole_size_si/od_of_pipe_element_si))/(hole_size_si-od_of_pipe_element_si)

    D_eq_ch=(id_of_previous_casing_si**2+od_of_pipe_element_si**2-(id_of_previous_casing_si**2-od_of_pipe_element_si**2)/log(id_of_previous_casing_si/od_of_pipe_element_si))/(id_of_previous_casing_si-od_of_pipe_element_si)
    
    Re_oh=mudweight_si*U_oh*D_eq_oh/converttofloat(viscocity_si)
    Re_ch=mudweight_si*U_ch*D_eq_ch/converttofloat(viscocity_si)

    def open_hole_f_x(f):
        return 1/sqrt(f)+4*log10((e/D_eq_oh)/3.7+1.255/(Re_oh*sqrt(f)))
    if Re_oh<=2100:
        flowregime="Laminar"
        open_hole_f=16/Re_oh
    elif Re_oh>4100:
        e=0.000045
        open_hole_f=newton(open_hole_f_x,0.01)
        flowregime="Turbulent"
    else:
        flowregime="Transitional"
        e=0.000045
        f_l=16/2100
        def open_hole_f_x(f):
            return 1/sqrt(f)+4*log10((e/D_eq_oh)/3.7+1.255/(4100*sqrt(f)))
        f_turb=newton(open_hole_f_x,0.01)
        x=(2100,4100)
        y=(f_l,f_turb)
        f_tran=interpolate.interp1d(x,y)
        f=f_tran(Re_oh)
        open_hole_f=f.tolist()

    def casing_f_x(f):
        return 1/sqrt(f)+4*log10((e/D_eq_ch)/3.7+1.255/(Re_ch*sqrt(f)))
    if Re_ch<=2100:
        flowregime="Laminar"
        casing_f=16/Re_ch
    elif Re_ch>4100:
        e=0.000045
        casing_f=newton(casing_f_x,0.01)
        flowregime="Turbulent"
    else:
        flowregime="Transitional"
        e=0.000045
        f_l=16/2100
        def casing_f_x(f):
            return 1/sqrt(f)+4*log10((e/D_eq_ch)/3.7+1.255/(4100*sqrt(f)))
        f_turb=newton(casing_f_x,0.01)
        x=(2100,4100)
        y=(f_l,f_turb)
        f_tran=interpolate.interp1d(x,y)
        f=f_tran(Re_ch)
        casing_f=f.tolist()
    i=1
    for liner in checkliner:
        inside_diameter_si=liner.drift_id/12/3.281
        length_inside_liner=alllinerdata[index]['length_inside_liner'+str(i)]/3.281
        U_liner=flowrate_si/(pi/4*(inside_diameter_si**2-od_of_pipe_element_si**2))
        D_eq_liner=(inside_diameter_si**2+od_of_pipe_element_si**2-(inside_diameter_si**2-od_of_pipe_element_si**2)/log(inside_diameter_si/od_of_pipe_element_si))/(inside_diameter_si-od_of_pipe_element_si)
        Re_liner=mudweight_si*U_liner*D_eq_liner/converttofloat(viscocity_si)
        def liner_f_x(f):
            return 1/sqrt(f)+4*log10((e/D_eq_liner)/3.7+1.255/(Re_liner*sqrt(f)))
        if Re_liner<=2100:
            flowregime="Laminar"
            liner_f=16/Re_liner
        elif Re_liner>4100:
            e=0.000045
            liner_f=newton(liner_f_x,0.01)
            flowregime="Turbulent"
        else:
            flowregime="Transitional"
            e=0.000045
            f_l=16/2100
            def liner_f_x(f):
                return 1/sqrt(f)+4*log10((e/D_eq_liner)/3.7+1.255/(4100*sqrt(f)))
            f_turb=newton(liner_f_x,0.01)
            x=(2100,4100)
            y=(f_l,f_turb)
            f_tran=interpolate.interp1d(x,y)
            f=f_tran(Re_oh)
            liner_f=f.tolist()
        liner_pl_without_string_rotation=2*liner_f*mudweight_si*U_liner**2*length_inside_liner/(inside_diameter_si-od_of_pipe_element_si)
        lamda_liner=sqrt(((od_of_pipe_element_si/inside_diameter_si)**2-1)/(2*log(od_of_pipe_element_si/inside_diameter_si)))
        t_liner=liner_pl_without_string_rotation*od_of_pipe_element_si/(2*length_inside_liner)*abs(lamda_liner**2/1-1) if(length_of_previous_casing_from_surface_si>0 and length_inside_liner>0) else 0
        S_al=t_liner/viscocity_si
        S_taliner=rpm_si*od_of_pipe_element_si/(inside_diameter_si-od_of_pipe_element_si)
        S_tl=sqrt(S_al**2+S_taliner**2)
        t_tl=viscocity_si*S_tl
        Pressure_Loss_liner=t_tl*2*length_inside_liner/(od_of_pipe_element_si*abs(lamda_liner**2/1-1))
        liner_conversion =Pressure_Loss_liner * 3.28084
        linerdata={'length_inside_liner'+str(i):length_inside_liner,'pressureloss_liner'+str(i):liner_conversion*0.000145038}
        data.update(linerdata)
        i +=1

    op_pl_without_string_rotation=2*open_hole_f*mudweight_si*U_oh**2*length_against_open_hole/(hole_size_si-od_of_pipe_element_si)
    casing_pl_without_string_rotation=2*casing_f*mudweight_si*U_ch**2*length_against_casing/(id_of_previous_casing_si-od_of_pipe_element_si)
    lamda_oh=sqrt(((od_of_pipe_element_si/hole_size_si)**2-1)/(2*log(od_of_pipe_element_si/hole_size_si)))
    lamda_ch=sqrt(((od_of_pipe_element_si/id_of_previous_casing_si)**2-1)/(2*log(od_of_pipe_element_si/id_of_previous_casing_si)))
    t_oh=op_pl_without_string_rotation*od_of_pipe_element_si/(2*length_against_open_hole)*abs(lamda_oh**2/1-1) if(length_against_open_hole>0) else 0
    t_ch=casing_pl_without_string_rotation*od_of_pipe_element_si/(2*length_against_casing)*abs(lamda_ch**2/1-1) if(length_of_previous_casing_from_surface_si>0 and length_against_casing>0) else 0



    S_ao=t_oh/viscocity_si

    S_ac=t_ch/viscocity_si

    S_ta=rpm_si*od_of_pipe_element_si/(hole_size_si-od_of_pipe_element_si)

    S_tac=rpm_si*od_of_pipe_element_si/(id_of_previous_casing_si-od_of_pipe_element_si)

    S_t=sqrt(S_ao**2+S_ta**2)

    S_tc=sqrt(S_ac**2+S_tac**2)

    t_t=viscocity_si*S_t
    
    t_tc=viscocity_si*S_tc

    Pressure_Loss_OpenHole=t_t*2*length_against_open_hole/(od_of_pipe_element_si*abs(lamda_oh**2/1-1))
    openhole_conversion =Pressure_Loss_OpenHole * 3.28084
    Pressure_Loss_CasedHole=t_tc*2*length_against_casing/(od_of_pipe_element_si*abs(lamda_ch**2/1-1))
    casedhole_conversion = Pressure_Loss_CasedHole * 3.28084
    apl_without_Rotation=(op_pl_without_string_rotation+casing_pl_without_string_rotation)*0.000145038

    apl_with_Rotation=(Pressure_Loss_OpenHole+Pressure_Loss_CasedHole)*0.000145038
    alldata={
        'length_against_open_hole':length_against_open_hole,
        'length_against_casing':length_against_casing,
        'pressureloss':apl_with_Rotation,
        'Pressure_Loss_OpenHole':openhole_conversion*0.000145038,
        'Pressure_Loss_CasedHole':casedhole_conversion*0.000145038,
        'flowregime':flowregime
    }
    data.update(alldata)
    return data

#calculate bingham annulus pressure loss liner
def calculate_bingham_linerpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,alllinerdata,typename,linercount,checkliner,wellphasetodepth):
    index = next((index for (index, d) in enumerate(alllinerdata) if d["type"] == typename), None)
    data={}
    P_viscocity=viscocity['plastic_viscosity']
    yield_point=viscocity['yieldpoint']
    length_of_phase=wellphasetodepth
    previous_casing_length=length_of_previous_casing_from_surface
    diameter_of_open_hole=hole_size
    id_of_previous_casing=id_of_previous_casing
    length_against_open_hole=alllinerdata[index]['length_inside_openhole']
    length_of_inside_casing=alllinerdata[index]['length_inside_casing']
    od_of_pipe_element=od_of_pipe_element
    rpm=rpm
   
    # conversion of SI
    flowrate_si = flowrate*0.000063
    mudweight_si = mud_weight/8.33*1000 

    length_of_phase_si = length_of_phase/3.281

    pre_casing_length_si = previous_casing_length/3.281

    diameter_of_open_hole_si = diameter_of_open_hole/12/3.281

    id_of_previous_casing_si = id_of_previous_casing/12/3.281

    length_of_open_hole_si = length_against_open_hole/3.281

    length_of_inside_casing_si = length_of_inside_casing/3.281

    od_of_pipe_element_si = converttofloat(od_of_pipe_element)/12/3.281

    rpm_si = int(rpm)*2*pi/60


    
    # open hole pressure loss
    Ua = flowrate_si/(pi/4*(diameter_of_open_hole_si**2-od_of_pipe_element_si**2))

    
    # calculation for shear rate
    axial_shear_rate = 8*Ua/(2/3*(diameter_of_open_hole_si-od_of_pipe_element_si))

    radial_shear_rate = rpm_si*od_of_pipe_element_si/(diameter_of_open_hole_si-od_of_pipe_element_si)

    total_shear_rate = sqrt(axial_shear_rate**2+radial_shear_rate**2)


    # Calculate Shear Stress
    Ts = yield_point*0.4788+P_viscocity/1000*total_shear_rate

    # Calculate Eo
    Eo = yield_point*0.4788/Ts

    
    # Calculate Headstrom Number
    He = 24900*(mudweight_si/1000*8.33)*yield_point*((diameter_of_open_hole_si-od_of_pipe_element_si)*3.281*12)**2/P_viscocity**2 
 

    
    def E(a):
        return He/22400-(a/(1-a)**3)
    Eoc = fsolve(E,0)
    

    # Calculate Critical Reynolds Number
    Rec = sqrt(2/3)*He*(1-3/2*Eoc+0.5*Eoc**3)/(8*Eoc)

    # Calculate Reynolds Number
    De = diameter_of_open_hole_si*(1+(od_of_pipe_element_si/diameter_of_open_hole_si)**2-((1-(od_of_pipe_element_si/diameter_of_open_hole_si)**2)/(log(od_of_pipe_element_si/diameter_of_open_hole_si))))**0.5
    Re = De*Ua*mudweight_si/(P_viscocity/1000)

    #Calculate Pressure Loss
    if Re<=Rec:
        flowregime="Laminar"
        dP=4*Ts/De*length_of_open_hole_si
    else:
        flowregime="Turbulent"
        a=0.0786
        b=0.25
        f=a/Re**b
        dP=2*f*mudweight_si*(Ua)**2*length_of_open_hole_si/(diameter_of_open_hole_si-od_of_pipe_element_si)

    # Convert to API Units
    Pressure_Loss_OpenHole = dP*0.000145038

    # Cased Hole Pressure Loss
    Uc = flowrate_si/(pi/4*(id_of_previous_casing**2-od_of_pipe_element_si**2))
    # calculation for shear rate
    axial_shear = 8*Uc/(2/3*(id_of_previous_casing-od_of_pipe_element_si))

    radial_shear = rpm_si*od_of_pipe_element_si/(id_of_previous_casing-od_of_pipe_element_si)

    total_shear = sqrt(axial_shear**2+radial_shear**2)

    # Calculate Shear Stress
    casing_Ts = yield_point*0.4788+P_viscocity/1000*total_shear

    # Calculate Eo
    casing_Eo = yield_point*0.4788/casing_Ts

    # Calculate Headstrom Number
    casing_He = 24900*(mudweight_si/1000*8.33)*yield_point*((id_of_previous_casing-od_of_pipe_element_si)*3.281*12)**2/P_viscocity**2 

    casing_He=int(str(casing_He)[:5])

    def E(a):
        return casing_He/22400-(a/(1-a)**3)
    casing_Eoc = fsolve(E,0)

    # Calculate Critical Reynolds Number
    casing_Rec = sqrt(2/3)*casing_He*(1-3/2*casing_Eoc+0.5*casing_Eoc**3)/(8*casing_Eoc)

    # Calculate Reynolds Number
    casing_De = id_of_previous_casing*(1+(od_of_pipe_element_si/id_of_previous_casing)**2-((1-(od_of_pipe_element_si/id_of_previous_casing)**2)/(log(od_of_pipe_element_si/id_of_previous_casing))))**0.5
    

    casing_Re = casing_De*Uc*mudweight_si/(P_viscocity/1000)

    #Calculate Pressure Loss
    if casing_Re<=casing_Rec:
        flowregime="Laminar"
        casing_dP=4*casing_Ts/casing_De*length_of_inside_casing_si

    else:
        flowregime="Turbulent"
        a=0.0786
        b=0.25
        f=a/casing_Re**b
        casing_dP=2*f*mudweight_si*(Uc)**2*length_of_inside_casing_si/(id_of_previous_casing-od_of_pipe_element_si)
    # Convert to API Units
    Casing_Pressure_Loss_OpenHole = casing_dP*0.000145038
    
    i=1
    for liner in checkliner:
        inside_diameter_si=liner.drift_id/12/3.281
        length_inside_liner=alllinerdata[index]['length_inside_liner'+str(i)]/3.281
        Ul = flowrate_si/(pi/4*(inside_diameter_si**2-od_of_pipe_element_si**2))
        axial_shear_liner = 8*Ul/(2/3*(inside_diameter_si-od_of_pipe_element_si))
        radial_shear_liner = rpm_si*od_of_pipe_element_si/(inside_diameter_si-od_of_pipe_element_si)
        total_shear_liner = sqrt(axial_shear_liner**2+radial_shear_liner**2)
        liner_Ts = yield_point*0.4788+P_viscocity/1000*total_shear_liner
        liner_Eo = yield_point*0.4788/liner_Ts
        liner_He = 24900*(mudweight_si/1000*8.33)*yield_point*((inside_diameter_si-od_of_pipe_element_si)*3.281*12)**2/P_viscocity**2 
        def E(a):
            return liner_He/22400-(a/(1-a)**3)
        liner_Eoc = fsolve(E,0)
        liner_Rec = sqrt(2/3)*liner_He*(1-3/2*liner_Eoc+0.5*liner_Eoc**3)/(8*liner_Eoc)
        liner_De = inside_diameter_si*(1+(od_of_pipe_element_si/inside_diameter_si)**2-((1-(od_of_pipe_element_si/inside_diameter_si)**2)/(log(od_of_pipe_element_si/inside_diameter_si))))**0.5
        liner_Re = liner_De*Ul*mudweight_si/(P_viscocity/1000)
        if casing_Re<=casing_Rec:
            flowregime="Laminar"
            liner_dP=4*liner_Ts/liner_De*length_inside_liner
        else:
            flowregime="Turbulent"
            a=0.0786
            b=0.25
            f=a/liner_Re**b
            liner_dP=2*f*mudweight_si*(Uc)**2*length_inside_liner/(inside_diameter_si-od_of_pipe_element_si)

        linerdata={'length_inside_liner'+str(i):length_inside_liner,'pressureloss_liner'+str(i):liner_dP*0.000145038}
        data.update(linerdata)
        i +=1

    alldata={
        'length_against_open_hole':length_of_open_hole_si,
        'length_against_casing':length_of_inside_casing_si,
        'pressureloss':Pressure_Loss_OpenHole,
        'Pressure_Loss_OpenHole':Pressure_Loss_OpenHole,
        'Pressure_Loss_CasedHole':Casing_Pressure_Loss_OpenHole,
        'flowregime':flowregime
    }
    data.update(alldata)
    return data

#calculate powerlaw annulus pressure loss
def calculate_powerlaw_linerpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,alllinerdata,typename,linercount,checkliner,wellphasetodepth):
    #1. Rheology Model Parameters
    index = next((index for (index, d) in enumerate(alllinerdata) if d["type"] == typename), None)
    data={}
    k=viscocity['K']
    m=viscocity['n']
    n=m
    K=k*0.4788*1.066       

    #2. Define Annular Geometry, SI Units
    Dc=id_of_previous_casing/12/3.281
    Dh=hole_size/12/3.281
    #3. Inputs, converted to SI Units
    Q=flowrate*0.000063
    MW=mud_weight/8.33*1000
    RPM=int(rpm)*2*math.pi/60
    Dp=converttofloat(od_of_pipe_element)/12/3.281
     
    L_o=alllinerdata[index]['length_inside_openhole']/3.281
    L_c=alllinerdata[index]['length_inside_casing']/3.281

    #4.1 Open Hole Annular Pressure Loss
    #4.1.1 Calculate Annular Velocity
    Ua_o=Q/(math.pi/4*(Dh**2-Dp**2))

    #4.1.2. Calculate effective diameter
    Y=0.37*n**-0.14
    Z=1-(1-(Dp/(Dh))**Y)**(1/Y)
    G=((1+Z/2)*((3-Z)*n+1))/(n*(4-Z))
    De=(Dh-Dp)/G

    #4.1.3 Calculate Shear Rate
    Ss=((12*Ua_o/(Dh-Dp)*(2*n+1)/(3*n))**2+(RPM*Dp/(Dh-Dp))**2)**0.5

    #4.1.4 Calculate Shear Stress
    Ts=K*Ss**n
    #4.1.5 Calculate Reynolds Number
    Re=De*MW*Ua_o/(Ts/Ss)

    #4.1.6 Calculate Friction Factor
    if Re<=3470-1370*n:
        flowregime='Laminar'
        f=24/Re
    
    elif Re>4150-1150*n:
        flowregime='Turbulent'
        def f_x(f):
            return 1/math.sqrt(f)-4/n**0.75*math.log10(Re*f**(1-n/2))+0.4/n**1.2
        f=newton(f_x,24/Re)
    else:
        flowregime='Transitional'
        f_l=24/(3470-1370*n)
        def f_x(f):
            return 1/math.sqrt(f)-4/n**0.75*math.log10((4150-1150*n)*f**(1-n/2))+0.4/n**1.2
        f_turb=newton(f_x,f_l)
        x=(3470-1370*n,4150-1150*n)
        y=(f_l,f_turb)
        f_tran=interpolate.interp1d(x,y)
        f=f_tran(Re)

    #4.1.7 Calculate Pressure Loss, API Units
    dP_o=2*f*MW*Ua_o**2*L_o/(Dh-Dp)*0.000145038    

    #5.1 Cased Hole Pressure Loss
    #5.1.1 Calculate Annular Velocity
    Uc_o=Q/(math.pi/4*(Dc**2-Dp**2))

    #5.1.2. Calculate effective diameter
    Yc=0.37*n**-0.14
    Zc=1-(1-(Dp/(Dc))**Y)**(1/Y)
    Gc=((1+Z/2)*((3-Z)*n+1))/(n*(4-Z))
    Dec=(Dc-Dp)/G

    #5.1.3 Calculate Shear Rate
    Ssc=((12*Uc_o/(Dc-Dp)*(2*n+1)/(3*n))**2+(RPM*Dp/(Dc-Dp))**2)**0.5

    #5.1.4 Calculate Shear Stress
    Tsc=K*Ssc**n
    
    #5.1.5 Calculate Reynolds Number
    Rec=Dec*MW*Uc_o/(Tsc/Ssc)

    #5.1.6 Calculate Friction Factor
    if Rec<=3470-1370*n:
        flowregime='Laminar'
        fc=24/Rec
    elif Rec>4150-1150*n:
        flowregime='Turbulent'
        def f_xc(f):
            return 1/math.sqrt(f)-4/n**0.75*math.log10(Rec*f**(1-n/2))+0.4/n**1.2
        fc=newton(f_xc,24/Rec)
    else:
        flowregime='Transitional'
        f_l=24/(3470-1370*n)
        def f_xc(f):
            return 1/math.sqrt(f)-4/n**0.75*math.log10((4150-1150*n)*f**(1-n/2))+0.4/n**1.2
        f_turb=newton(f_xc,f_l)
        x=(3470-1370*n,4150-1150*n)
        y=(f_l,f_turb)
        f_tran=interpolate.interp1d(x,y)
        fc=f_tran(Rec)
    
    #5.1.7 Calculate Pressure Loss, API Units
    dP_c=2*fc*MW*Uc_o**2*L_c/(Dc-Dp)*0.000145038

    i=1
    for liner in checkliner:
        inside_diameter_si=liner.drift_id/12/3.281
        length_inside_liner=alllinerdata[index]['length_inside_liner'+str(i)]/3.281
        Uc_liner=Q/(pi/4*(inside_diameter_si**2-Dp**2))
        Yc=0.37*n**-0.14
        Zc=1-(1-(Dp/(inside_diameter_si))**Yc)**(1/Yc)
        Gc=((1+Zc/2)*((3-Z)*n+1))/(n*(4-Z))
        Dec=(inside_diameter_si-Dp)/Gc
        Ssl=((12*Uc_liner/(inside_diameter_si-Dp)*(2*n+1)/(3*n))**2+(RPM*Dp/(inside_diameter_si-Dp))**2)**0.5
        Tsl=K*Ssl**n
        Rel=Dec*MW*Uc_liner/(Tsl/Ssl)
        
        if Rel<=3470-1370*n:
            flowregime='Laminar'
            fl=24/Rel
        elif Rec>4150-1150*n:
            flowregime='Turbulent'
            def f_xc(f):
                return 1/math.sqrt(f)-4/n**0.75*math.log10(Rel*f**(1-n/2))+0.4/n**1.2
            fl=newton(f_xc,24/Rel)
        else:
            flowregime='Transitional'
            f_l=24/(3470-1370*n)
            def f_xc(f):
                return 1/math.sqrt(f)-4/n**0.75*math.log10((4150-1150*n)*f**(1-n/2))+0.4/n**1.2
            f_turb=newton(f_xc,f_l)
            x=(3470-1370*n,4150-1150*n)
            y=(f_l,f_turb)
            f_tran=interpolate.interp1d(x,y)
            fl=f_tran(Rec)
    
        dP_l=2*fl*MW*Uc_liner**2*length_inside_liner/(inside_diameter_si-Dp)*0.000145038
        linerdata={'length_inside_liner'+str(i):length_inside_liner,'pressureloss_liner'+str(i):dP_l}
        data.update(linerdata)
        i +=1
    alldata={
        'length_against_open_hole':L_o,
        'length_against_casing':L_c,
        'pressureloss':2*f*MW*Ua_o**2*L_o/(Dh-Dp),
        'Pressure_Loss_OpenHole':dP_o,
        'Pressure_Loss_CasedHole':dP_c,
        'flowregime':flowregime
    }
    data.update(alldata)
    return data

#calculate Hershel annulus pressure loss
def calculate_hershel_linerpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,alllinerdata,typename,linercount,checkliner,wellphasetodepth):
    index = next((index for (index, d) in enumerate(alllinerdata) if d["type"] == typename), None)
    k=viscocity['K']
    ty=viscocity['lsryp']
    m=viscocity['n']
    K=k*1.066*0.4788/(1.703**m)
    LSRYP =ty*1.066*0.4788
    data={}
    Q=flowrate
    MW=mud_weight

    Lh=wellphasetodepth
    Lc=length_of_previous_casing_from_surface
    open_hole=hole_size
    id_of_previous_casing=id_of_previous_casing
    length_of_open_hole=alllinerdata[index]['length_inside_openhole']
    length_against_casing=alllinerdata[index]['length_inside_casing']

    od_of_pipe_element=converttofloat(od_of_pipe_element)
    rpm=rpm

    Q_si=Q*0.000063
    mw_si=MW/8.33*1000
    Lh_si = Lh/3.281
    Lc_si = Lc/3.281
    open_hole_si = open_hole/12/3.281
    id_of_previous_casing_si = id_of_previous_casing/12/3.281
    length_of_open_hole_si = length_of_open_hole/3.281
    length_against_casing_si = length_against_casing/3.281
    od_of_pipe_element_si = od_of_pipe_element/12/3.281
    rpm_si = int(rpm)*2*pi/60

    Ua = Q_si/(pi/4*(open_hole_si**2-od_of_pipe_element_si**2))

    ssz = 12*Ua/(open_hole_si-od_of_pipe_element_si)
    sso = rpm_si*(od_of_pipe_element_si/2)**2/((open_hole_si/2)**2-(od_of_pipe_element_si/2)**2)*((-2*(od_of_pipe_element_si/2)**2-((open_hole_si/2)**2-(od_of_pipe_element_si/2)**2))/(od_of_pipe_element_si/2)**2)
    sst = sqrt(ssz**2+sso**2)

    def t_xc(t):
        return sst-((t-LSRYP)**((m+1)/m)/(K**(1/m)*t**2))*(3*m/(1+2*m))*(t+m/(m+1)*LSRYP)

    tw=newton(t_xc,LSRYP+1)

    a=(3*m/(1+2*m))*(1-(1/(1+m))*LSRYP/tw-(m/(1+m))*(LSRYP/tw)**2)
    b=1/a
    N=1/(3*(b-2/3))

    sg=(1+2*N)/(3*N)*sst
    Re = 12*mw_si*Ua**2/(LSRYP+K*sg**m)

    if Re<=3470-1370*N:
        flowregime='Laminar'
        fc=24/Re
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
    
    pressureloss_openhole = 2*fc*mw_si*Ua**2*length_of_open_hole_si/(open_hole_si-od_of_pipe_element_si)

    dP = pressureloss_openhole*0.000145038
    if(typename=='MWD2'):
        print(f'fc {fc}')


    # Cased Hole Pressure Loss
    Uc = Q_si/(pi/4*(id_of_previous_casing_si**2-od_of_pipe_element_si**2))

    Ssz_casing = 12*Uc/(id_of_previous_casing_si-od_of_pipe_element_si)
    Sso_casing = rpm_si*(od_of_pipe_element_si/2)**2/((id_of_previous_casing_si/2)**2-(od_of_pipe_element_si/2)**2)*((-2*(od_of_pipe_element_si/2)**2-((id_of_previous_casing_si/2)**2-(od_of_pipe_element_si/2)**2))/(od_of_pipe_element_si/2)**2)
    Sst_casing = sqrt(Ssz_casing**2+Sso_casing**2)

    def t_xc(t):
        return Sst_casing-((t-LSRYP)**((m+1)/m)/(K**(1/m)*t**2))*(3*m/(1+2*m))*(t+m/(m+1)*LSRYP)

    tw_casing=newton(t_xc,LSRYP+1)

    a_casing = (3*m/(1+2*m))*(1-(1/(1+m))*LSRYP/tw_casing-(m/(1+m))*(LSRYP/tw_casing)**2)
    b_casing = 1/a_casing
    N_casing = 1/(3*(b_casing-2/3)) 

    sg_casing = (1+2*N_casing)/(3*N_casing)*Sst_casing

    Re_casing = 12*mw_si*Uc**2/(LSRYP+K*sg_casing**m)

    if Re_casing<=3470-1370*N_casing:
        flowregime='Laminar'
        fc_casing = 24/Re_casing
    
    elif Re_casing>4150-1150*N_casing:
        flowregime='Turbulent'
        def f_x(a):
            return 1/sqrt(a)-4/N_casing**0.75*log10(Re_casing*a**(1-N_casing/2))+0.4/N_casing**1.2
        
        fc_casing = newton(f_x,24/Re_casing)
    
    else:
        flowregime='Transitional'
        def f_x(f_turb):
            return 1/sqrt(f_turb)-4/N_casing**0.75*log10(Re_turb*f_turb**(1-N_casing/2))+0.4/N_casing**1.2
        
        #End of Laminar
        Re_L=3470-1370*N_casing
        f_l=24/Re_L
        
        #Start of Turbulent
        Re_turb=4150-1150*N_casing
        f_turb=newton(f_x,f_l)
        
        x=[3470-1370*N,4150-1150*N_casing]
        y=[f_l,f_turb]
        
        #Define the interpolate method
        i=interpolate.interp1d(x,y)
        
        fc_casing=i(Re_casing)

    pressureloss_casing = 2*fc_casing*mw_si*Uc**2*length_against_casing_si/(id_of_previous_casing_si-od_of_pipe_element_si)

    dp_casing = pressureloss_casing*0.000145038

    j=1
    for liner in checkliner:
        inside_diameter_si=liner.drift_id/12/3.281
        length_inside_liner=alllinerdata[index]['length_inside_liner'+str(j)]/3.281
        Ul = Q_si/(pi/4*(inside_diameter_si**2-od_of_pipe_element_si**2))
        Ssz_liner = 12*Ul/(inside_diameter_si-od_of_pipe_element_si)
        Sso_liner = rpm_si*(od_of_pipe_element_si/2)**2/((inside_diameter_si/2)**2-(od_of_pipe_element_si/2)**2)*((-2*(od_of_pipe_element_si/2)**2-((inside_diameter_si/2)**2-(od_of_pipe_element_si/2)**2))/(od_of_pipe_element_si/2)**2)
        Sst_liner = sqrt(Ssz_liner**2+Sso_liner**2)
        def t_xc(t):
            return Sst_liner-((t-LSRYP)**((m+1)/m)/(K**(1/m)*t**2))*(3*m/(1+2*m))*(t+m/(m+1)*LSRYP)
        tw_liner=newton(t_xc,LSRYP+1)
        a_liner = (3*m/(1+2*m))*(1-(1/(1+m))*LSRYP/tw_liner-(m/(1+m))*(LSRYP/tw_liner)**2)
        b_liner = 1/a_liner
        N_liner = 1/(3*(b_liner-2/3))
        sg_liner = (1+2*N_liner)/(3*N_liner)*Sst_liner
        Re_liner = 12*mw_si*Ul**2/(LSRYP+K*sg_liner**m) 
        
        if Re_liner<=3470-1370*N_liner:
            flowregime='Laminar'
            fc_liner = 24/Re_liner
        
        elif Re_liner>4150-1150*N_liner:
            flowregime='Turbulent'
            def f_x(a):
                return 1/sqrt(a)-4/N_liner**0.75*log10(Re_liner*a**(1-N_liner/2))+0.4/N_liner**1.2
            fc_liner = newton(f_x,24/Re_liner)
        
        else:
            flowregime='Transitional'
            def f_x(f_turb):
                return 1/sqrt(f_turb)-4/N_liner**0.75*log10(Re_turb*f_turb**(1-N_liner/2))+0.4/N_liner**1.2
            
            #End of Laminar
            Re_L=3470-1370*N_liner
            f_l=24/Re_L
            
            #Start of Turbulent
            Re_turb=4150-1150*N_liner
            f_turb=newton(f_x,f_l)
            
            x=[3470-1370*N,4150-1150*N_liner]
            y=[f_l,f_turb]
            
            #Define the interpolate method
            i=interpolate.interp1d(x,y)
            
            fc_liner=i(Re_liner)
        
        pressureloss_liner = 2*fc_liner*mw_si*Ul**2*length_inside_liner/(inside_diameter_si-od_of_pipe_element_si)
        dp_liner = pressureloss_liner*0.000145038

        linerdata={'length_inside_liner'+str(j):length_inside_liner,'pressureloss_liner'+str(j):dp_liner}
        data.update(linerdata)
        j += 1
    
    alldata={
        'length_against_open_hole':length_of_open_hole_si,
        'length_against_casing':length_against_casing_si,
        'pressureloss':pressureloss_openhole,
        'Pressure_Loss_OpenHole':dP,
        'Pressure_Loss_CasedHole':dp_casing,
        'flowregime':flowregime
    }
    data.update(alldata)
    return data

def calculateannularpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,length_against_casing,length_against_open_hole,wellphasetodepth,typename):
    if(viscocity['selected_modal']=="1"):
        pressureloss=calculate_newtonian_anuularpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,length_against_casing,length_against_open_hole)
    elif(viscocity['selected_modal']=="2"):
        pressureloss=calculate_bingham_anuularpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,length_against_casing,length_against_open_hole,wellphasetodepth)
    if(viscocity['selected_modal']=="4"):
        pressureloss=calculate_hershel_anuularpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,length_against_casing,length_against_open_hole,wellphasetodepth)
    if(viscocity['selected_modal']=="3"):
        pressureloss=calculate_powerlaw_anuularpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,length_against_casing,length_against_open_hole,wellphasetodepth)
    return pressureloss

#calculate newtonian annulus pressure loss
def calculate_newtonian_anuularpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,length_against_casing,length_against_open_hole):
    length_against_open_hole=length_against_open_hole/3.281
    length_against_casing=length_against_casing/3.281
    viscocity_si=viscocity['plastic_viscosity']
    flowrate_si=flowrate*0.000063
    mudweight_si=mud_weight/8.33*1000
    rpm_si=int(rpm)*2*pi/60
    od_of_pipe_element_si=converttofloat(od_of_pipe_element)/12/3.281
    hole_size_si=hole_size/12/3.281
    id_of_previous_casing_si=id_of_previous_casing/12/3.281
    length_of_previous_casing_from_surface_si=length_of_previous_casing_from_surface/3.281
    length_of_open_hole_si=length_of_open_hole/3.281
    bitdepth_si=bitdepth/3.281
    length_of_openhole_from_bitdepth_si=length_of_openhole_from_bitdepth/3.281
    U_oh=flowrate_si/(pi/4*(hole_size_si**2-od_of_pipe_element_si**2))
    U_ch=flowrate_si/(pi/4*(id_of_previous_casing_si**2-od_of_pipe_element_si**2))
    D_eq_oh=(hole_size_si**2+od_of_pipe_element_si**2-(hole_size_si**2-od_of_pipe_element_si**2)/log(hole_size_si/od_of_pipe_element_si))/(hole_size_si-od_of_pipe_element_si)

    D_eq_ch=(id_of_previous_casing_si**2+od_of_pipe_element_si**2-(id_of_previous_casing_si**2-od_of_pipe_element_si**2)/log(id_of_previous_casing_si/od_of_pipe_element_si))/(id_of_previous_casing_si-od_of_pipe_element_si)
    Re_oh=mudweight_si*U_oh*D_eq_oh/converttofloat(viscocity_si)
    Re_ch=mudweight_si*U_ch*D_eq_ch/converttofloat(viscocity_si)
    def open_hole_f_x(f):
        return 1/sqrt(f)+4*log10((e/D_eq_oh)/3.7+1.255/(Re_oh*sqrt(f)))
    if Re_oh<=2100:
        flowregime="Laminar"
        open_hole_f=16/Re_oh
    elif Re_oh>4100:
        e=0.000045
        open_hole_f=newton(open_hole_f_x,0.01)
        flowregime="Turbulent"
    else:
        flowregime="Transitional"
        e=0.000045
        f_l=16/2100
        def open_hole_f_x(f):
            return 1/sqrt(f)+4*log10((e/D_eq_oh)/3.7+1.255/(4100*sqrt(f)))
        f_turb=newton(open_hole_f_x,0.01)
        x=(2100,4100)
        y=(f_l,f_turb)
        f_tran=interpolate.interp1d(x,y)
        f=f_tran(Re_oh)
        open_hole_f=f.tolist()

    def casing_f_x(f):
        return 1/sqrt(f)+4*log10((e/D_eq_ch)/3.7+1.255/(Re_ch*sqrt(f)))
    if Re_ch<=2100:
        flowregime="Laminar"
        casing_f=16/Re_ch
    elif Re_ch>4100:
        e=0.000045
        casing_f=newton(casing_f_x,0.01)
        flowregime="Turbulent"
    else:
        flowregime="Transitional"
        e=0.000045
        f_l=16/2100
        def casing_f_x(f):
            return 1/sqrt(f)+4*log10((e/D_eq_ch)/3.7+1.255/(4100*sqrt(f)))
        f_turb=newton(casing_f_x,0.01)
        x=(2100,4100)
        y=(f_l,f_turb)
        f_tran=interpolate.interp1d(x,y)
        f=f_tran(Re_ch)
        casing_f=f.tolist()

    op_pl_without_string_rotation=2*open_hole_f*mudweight_si*U_oh**2*length_against_open_hole/(hole_size_si-od_of_pipe_element_si)
    casing_pl_without_string_rotation=2*casing_f*mudweight_si*U_ch**2*length_against_casing/(id_of_previous_casing_si-od_of_pipe_element_si)
    lamda_oh=sqrt(((od_of_pipe_element_si/hole_size_si)**2-1)/(2*log(od_of_pipe_element_si/hole_size_si)))
    lamda_ch=sqrt(((od_of_pipe_element_si/id_of_previous_casing_si)**2-1)/(2*log(od_of_pipe_element_si/id_of_previous_casing_si)))
    t_oh=op_pl_without_string_rotation*od_of_pipe_element_si/(2*length_against_open_hole)*abs(lamda_oh**2/1-1) if(length_against_open_hole>0) else 0
    t_ch=casing_pl_without_string_rotation*od_of_pipe_element_si/(2*length_against_casing)*abs(lamda_ch**2/1-1) if(length_of_previous_casing_from_surface_si>0 and length_against_casing>0) else 0


    S_ao=t_oh/viscocity_si

    S_ac=t_ch/viscocity_si

    S_ta=rpm_si*od_of_pipe_element_si/(hole_size_si-od_of_pipe_element_si)

    S_tac=rpm_si*od_of_pipe_element_si/(id_of_previous_casing_si-od_of_pipe_element_si)

    S_t=sqrt(S_ao**2+S_ta**2)

    S_tc=sqrt(S_ac**2+S_tac**2)

    t_t=viscocity_si*S_t
    
    t_tc=viscocity_si*S_tc

    Pressure_Loss_OpenHole=t_t*2*length_against_open_hole/(od_of_pipe_element_si*abs(lamda_oh**2/1-1))
    openhole_conversion =Pressure_Loss_OpenHole * 3.28084
    Pressure_Loss_CasedHole=t_tc*2*length_against_casing/(od_of_pipe_element_si*abs(lamda_ch**2/1-1))
    casedhole_conversion = Pressure_Loss_CasedHole * 3.28084
    apl_without_Rotation=(op_pl_without_string_rotation+casing_pl_without_string_rotation)*0.000145038

    apl_with_Rotation=(Pressure_Loss_OpenHole+Pressure_Loss_CasedHole)*0.000145038
    data={
        'length_against_open_hole':length_against_open_hole,
        'length_against_casing':length_against_casing,
        'pressureloss':apl_with_Rotation,
        'Pressure_Loss_OpenHole':openhole_conversion*0.000145038,
        'Pressure_Loss_CasedHole':casedhole_conversion*0.000145038,
        'flowregime':flowregime
    }
    return data

#calculate bingham annulus pressure loss
def calculate_bingham_anuularpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,length_against_casing,length_against_open_hole,wellphasetodepth):
    P_viscocity=viscocity['plastic_viscosity']
    yield_point=viscocity['yieldpoint']
    length_of_phase=wellphasetodepth
    previous_casing_length=length_of_previous_casing_from_surface
    diameter_of_open_hole=hole_size
    id_of_previous_casing=id_of_previous_casing
    length_against_open_hole=length_against_open_hole
    length_of_inside_casing=length_against_casing
    od_of_pipe_element=od_of_pipe_element
    rpm=rpm
 
# conversion of SI
    flowrate_si = flowrate*0.000063
    mudweight_si = mud_weight/8.33*1000 

    length_of_phase_si = length_of_phase/3.281

    pre_casing_length_si = previous_casing_length/3.281

    diameter_of_open_hole_si = diameter_of_open_hole/12/3.281

    id_of_previous_casing_si = id_of_previous_casing/12/3.281

    length_of_open_hole_si = length_against_open_hole/3.281

    length_of_inside_casing_si = length_of_inside_casing/3.281

    od_of_pipe_element_si = converttofloat(od_of_pipe_element)/12/3.281

    rpm_si = int(rpm)*2*pi/60


    
# open hole pressure loss
    Ua = flowrate_si/(pi/4*(diameter_of_open_hole_si**2-od_of_pipe_element_si**2))

    
    # calculation for shear rate
    axial_shear_rate = 8*Ua/(2/3*(diameter_of_open_hole_si-od_of_pipe_element_si))

    radial_shear_rate = rpm_si*od_of_pipe_element_si/(diameter_of_open_hole_si-od_of_pipe_element_si)

    total_shear_rate = sqrt(axial_shear_rate**2+radial_shear_rate**2)


    # Calculate Shear Stress
    Ts = yield_point*0.4788+P_viscocity/1000*total_shear_rate

    # Calculate Eo
    Eo = yield_point*0.4788/Ts

    
    # Calculate Headstrom Number
    He = 24900*(mudweight_si/1000*8.33)*yield_point*((diameter_of_open_hole_si-od_of_pipe_element_si)*3.281*12)**2/P_viscocity**2 
 

    
    def E(a):
        return He/22400-(a/(1-a)**3)
    Eoc = fsolve(E,0)
    

    # Calculate Critical Reynolds Number
    Rec = sqrt(2/3)*He*(1-3/2*Eoc+0.5*Eoc**3)/(8*Eoc)

    # Calculate Reynolds Number
    De = diameter_of_open_hole_si*(1+(od_of_pipe_element_si/diameter_of_open_hole_si)**2-((1-(od_of_pipe_element_si/diameter_of_open_hole_si)**2)/(log(od_of_pipe_element_si/diameter_of_open_hole_si))))**0.5
    Re = De*Ua*mudweight_si/(P_viscocity/1000)

    #Calculate Pressure Loss
    if Re<=Rec:
        flowregime="Laminar"
        dP=4*Ts/De*length_of_open_hole_si
    else:
        flowregime="Turbulent"
        a=0.0786
        b=0.25
        f=a/Re**b
        dP=2*f*mudweight_si*(Ua)**2*length_of_open_hole_si/(diameter_of_open_hole_si-od_of_pipe_element_si)

    # Convert to API Units
    Pressure_Loss_OpenHole = dP*0.000145038

# Cased Hole Pressure Loss
    Uc = flowrate_si/(pi/4*(id_of_previous_casing**2-od_of_pipe_element_si**2))
    # calculation for shear rate
    axial_shear = 8*Uc/(2/3*(id_of_previous_casing-od_of_pipe_element_si))

    radial_shear = rpm_si*od_of_pipe_element_si/(id_of_previous_casing-od_of_pipe_element_si)

    total_shear = sqrt(axial_shear**2+radial_shear**2)

    # Calculate Shear Stress
    casing_Ts = yield_point*0.4788+P_viscocity/1000*total_shear

    # Calculate Eo
    casing_Eo = yield_point*0.4788/casing_Ts

    # Calculate Headstrom Number
    casing_He = 24900*(mudweight_si/1000*8.33)*yield_point*((id_of_previous_casing-od_of_pipe_element_si)*3.281*12)**2/P_viscocity**2 

    casing_He=int(str(casing_He)[:5])

    def E(a):
        return casing_He/22400-(a/(1-a)**3)
    casing_Eoc = fsolve(E,0)

    # Calculate Critical Reynolds Number
    casing_Rec = sqrt(2/3)*casing_He*(1-3/2*casing_Eoc+0.5*casing_Eoc**3)/(8*casing_Eoc)

    # Calculate Reynolds Number
    casing_De = id_of_previous_casing*(1+(od_of_pipe_element_si/id_of_previous_casing)**2-((1-(od_of_pipe_element_si/id_of_previous_casing)**2)/(log(od_of_pipe_element_si/id_of_previous_casing))))**0.5
    

    casing_Re = casing_De*Uc*mudweight_si/(P_viscocity/1000)

    #Calculate Pressure Loss
    if casing_Re<=casing_Rec:
        flowregime="Laminar"
        casing_dP=4*casing_Ts/casing_De*length_of_inside_casing_si

    else:
        flowregime="Turbulent"
        a=0.0786
        b=0.25
        f=a/casing_Re**b
        casing_dP=2*f*mudweight_si*(Uc)**2*length_of_inside_casing_si/(id_of_previous_casing-od_of_pipe_element_si)
    # Convert to API Units
    Casing_Pressure_Loss_OpenHole = casing_dP*0.000145038
    data={
        'length_against_open_hole':length_of_open_hole_si,
        'length_against_casing':length_of_inside_casing_si,
        'pressureloss':Pressure_Loss_OpenHole,
        'Pressure_Loss_OpenHole':Pressure_Loss_OpenHole,
        'Pressure_Loss_CasedHole':Casing_Pressure_Loss_OpenHole,
        'flowregime':flowregime
    }
    return data

#calculate powerlaw annulus pressure loss
def calculate_powerlaw_anuularpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,length_against_casing,length_against_open_hole,wellphasetodepth):
    #1. Rheology Model Parameters

    k=viscocity['K']
    m=viscocity['n']
    n=m
    K=k*0.4788*1.066       

    #2. Define Annular Geometry, SI Units
    Dc=id_of_previous_casing/12/3.281
    Dh=hole_size/12/3.281
    #3. Inputs, converted to SI Units
    Q=flowrate*0.000063
    MW=mud_weight/8.33*1000
    RPM=int(rpm)*2*math.pi/60
    Dp=converttofloat(od_of_pipe_element)/12/3.281
    L_o=length_against_open_hole/3.281
    L_c=length_against_casing/3.281

    #4.1 Open Hole Annular Pressure Loss
    #4.1.1 Calculate Annular Velocity
    Ua_o=Q/(math.pi/4*(Dh**2-Dp**2))

    #4.1.2. Calculate effective diameter
    Y=0.37*n**-0.14
    Z=1-(1-(Dp/(Dh))**Y)**(1/Y)
    G=((1+Z/2)*((3-Z)*n+1))/(n*(4-Z))
    De=(Dh-Dp)/G

    #4.1.3 Calculate Shear Rate
    Ss=((12*Ua_o/(Dh-Dp)*(2*n+1)/(3*n))**2+(RPM*Dp/(Dh-Dp))**2)**0.5

    #4.1.4 Calculate Shear Stress
    Ts=K*Ss**n
    #4.1.5 Calculate Reynolds Number
    Re=De*MW*Ua_o/(Ts/Ss)

    #4.1.6 Calculate Friction Factor
    if Re<=3470-1370*n:
        flowregime='Laminar'
        f=24/Re
    
    elif Re>4150-1150*n:
        flowregime='Turbulent'
        def f_x(f):
            return 1/math.sqrt(f)-4/n**0.75*math.log10(Re*f**(1-n/2))+0.4/n**1.2
        f=newton(f_x,24/Re)
    else:
        flowregime='Transitional'
        f_l=24/(3470-1370*n)
        def f_x(f):
            return 1/math.sqrt(f)-4/n**0.75*math.log10((4150-1150*n)*f**(1-n/2))+0.4/n**1.2
        f_turb=newton(f_x,f_l)
        x=(3470-1370*n,4150-1150*n)
        y=(f_l,f_turb)
        f_tran=interpolate.interp1d(x,y)
        f=f_tran(Re)

    #4.1.7 Calculate Pressure Loss, API Units
    dP_o=2*f*MW*Ua_o**2*L_o/(Dh-Dp)*0.000145038    

    #5.1 Cased Hole Pressure Loss
    #5.1.1 Calculate Annular Velocity
    Uc_o=Q/(math.pi/4*(Dc**2-Dp**2))

    #5.1.2. Calculate effective diameter
    Yc=0.37*n**-0.14
    Zc=1-(1-(Dp/(Dc))**Y)**(1/Y)
    Gc=((1+Z/2)*((3-Z)*n+1))/(n*(4-Z))
    Dec=(Dc-Dp)/G

    #5.1.3 Calculate Shear Rate
    Ssc=((12*Uc_o/(Dc-Dp)*(2*n+1)/(3*n))**2+(RPM*Dp/(Dc-Dp))**2)**0.5

    #5.1.4 Calculate Shear Stress
    Tsc=K*Ssc**n
    
    #5.1.5 Calculate Reynolds Number
    Rec=Dec*MW*Uc_o/(Tsc/Ssc)

    #5.1.6 Calculate Friction Factor
    if Rec<=3470-1370*n:
        flowregime='Laminar'
        fc=24/Rec
    elif Rec>4150-1150*n:
        flowregime='Turbulent'
        def f_xc(f):
            return 1/math.sqrt(f)-4/n**0.75*math.log10(Rec*f**(1-n/2))+0.4/n**1.2
        fc=newton(f_xc,24/Rec)
    else:
        flowregime='Transitional'
        f_l=24/(3470-1370*n)
        def f_xc(f):
            return 1/math.sqrt(f)-4/n**0.75*math.log10((4150-1150*n)*f**(1-n/2))+0.4/n**1.2
        f_turb=newton(f_xc,f_l)
        x=(3470-1370*n,4150-1150*n)
        y=(f_l,f_turb)
        f_tran=interpolate.interp1d(x,y)
        fc=f_tran(Rec)
    
    #5.1.7 Calculate Pressure Loss, API Units
    dP_c=2*fc*MW*Uc_o**2*L_c/(Dc-Dp)*0.000145038
    data={
        'length_against_open_hole':L_o,
        'length_against_casing':L_c,
        'pressureloss':2*f*MW*Ua_o**2*L_o/(Dh-Dp),
        'Pressure_Loss_OpenHole':dP_o,
        'Pressure_Loss_CasedHole':dP_c,
        'flowregime':flowregime
    }
    return data

#calculate Hershel annulus pressure loss
def calculate_hershel_anuularpressureloss(viscocity,flowrate,mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,length_against_casing,length_against_open_hole,wellphasetodepth):
    k=viscocity['K']
    ty=viscocity['lsryp']
    m=viscocity['n']
    K=k*1.066*0.4788/(1.703**m)
    LSRYP =ty*1.066*0.4788

    Q=flowrate
    MW=mud_weight

    Lh=wellphasetodepth
    Lc=length_of_previous_casing_from_surface
    open_hole=hole_size
    id_of_previous_casing=id_of_previous_casing
    length_of_open_hole=length_against_open_hole
    length_against_casing=length_against_casing
    od_of_pipe_element=converttofloat(od_of_pipe_element)
    rpm=rpm

    Q_si=Q*0.000063
    mw_si=MW/8.33*1000
    Lh_si = Lh/3.281
    Lc_si = Lc/3.281
    open_hole_si = open_hole/12/3.281
    
    id_of_previous_casing_si = converttofloat(id_of_previous_casing)/12/3.281
    length_of_open_hole_si = length_of_open_hole/3.281
    length_against_casing_si = length_against_casing/3.281
    od_of_pipe_element_si = od_of_pipe_element/12/3.281
    rpm_si = int(rpm)*2*pi/60

    Ua = Q_si/(pi/4*(open_hole_si**2-od_of_pipe_element_si**2))

    ssz = 12*Ua/(open_hole_si-od_of_pipe_element_si)
    sso = rpm_si*(od_of_pipe_element_si/2)**2/((open_hole_si/2)**2-(od_of_pipe_element_si/2)**2)*((-2*(od_of_pipe_element_si/2)**2-((open_hole_si/2)**2-(od_of_pipe_element_si/2)**2))/(od_of_pipe_element_si/2)**2)
    sst = sqrt(ssz**2+sso**2)

    def t_xc(t):
        return sst-((t-LSRYP)**((m+1)/m)/(K**(1/m)*t**2))*(3*m/(1+2*m))*(t+m/(m+1)*LSRYP)

    tw=newton(t_xc,LSRYP+1)

    a=(3*m/(1+2*m))*(1-(1/(1+m))*LSRYP/tw-(m/(1+m))*(LSRYP/tw)**2)
    b=1/a
    N=1/(3*(b-2/3))

    sg=(1+2*N)/(3*N)*sst
    Re = 12*mw_si*Ua**2/(LSRYP+K*sg**m)

    if Re<=3470-1370*N:
        flowregime='Laminar'
        fc=24/Re
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
    
    pressureloss_openhole = 2*fc*mw_si*Ua**2*length_of_open_hole_si/(open_hole_si-od_of_pipe_element_si)

    dP = pressureloss_openhole*0.000145038

    # Cased Hole Pressure Loss
    Uc = Q_si/(pi/4*(id_of_previous_casing_si**2-od_of_pipe_element_si**2))

    Ssz_casing = 12*Uc/(id_of_previous_casing_si-od_of_pipe_element_si)
    Sso_casing = rpm_si*(od_of_pipe_element_si/2)**2/((id_of_previous_casing_si/2)**2-(od_of_pipe_element_si/2)**2)*((-2*(od_of_pipe_element_si/2)**2-((id_of_previous_casing_si/2)**2-(od_of_pipe_element_si/2)**2))/(od_of_pipe_element_si/2)**2)
    Sst_casing = sqrt(Ssz_casing**2+Sso_casing**2)

    def t_xc(t):
        return Sst_casing-((t-LSRYP)**((m+1)/m)/(K**(1/m)*t**2))*(3*m/(1+2*m))*(t+m/(m+1)*LSRYP)

    tw_casing=newton(t_xc,LSRYP+1)

    a_casing = (3*m/(1+2*m))*(1-(1/(1+m))*LSRYP/tw_casing-(m/(1+m))*(LSRYP/tw_casing)**2)
    b_casing = 1/a_casing
    N_casing = 1/(3*(b_casing-2/3)) 

    sg_casing = (1+2*N_casing)/(3*N_casing)*Sst_casing

    Re_casing = 12*mw_si*Uc**2/(LSRYP+K*sg_casing**m)

    if Re_casing<=3470-1370*N_casing:
        flowregime='Laminar'
        fc_casing = 24/Re_casing
    
    elif Re_casing>4150-1150*N_casing:
        flowregime='Turbulent'
        def f_x(a):
            return 1/sqrt(a)-4/N_casing**0.75*log10(Re_casing*a**(1-N_casing/2))+0.4/N_casing**1.2
        
        fc_casing = newton(f_x,24/Re_casing)
    
    else:
        flowregime='Transitional'
        def f_x(f_turb):
            return 1/sqrt(f_turb)-4/N_casing**0.75*log10(Re_turb*f_turb**(1-N_casing/2))+0.4/N_casing**1.2
        
        #End of Laminar
        Re_L=3470-1370*N_casing
        f_l=24/Re_L
        
        #Start of Turbulent
        Re_turb=4150-1150*N_casing
        f_turb=newton(f_x,f_l)
        
        x=[3470-1370*N,4150-1150*N_casing]
        y=[f_l,f_turb]
        
        #Define the interpolate method
        i=interpolate.interp1d(x,y)
        
        fc_casing=i(Re_casing)

    pressureloss_casing = 2*fc_casing*mw_si*Uc**2*length_against_casing_si/(id_of_previous_casing_si-od_of_pipe_element_si)

    dp_casing = pressureloss_casing*0.000145038

    data={
        'length_against_open_hole':length_of_open_hole_si,
        'length_against_casing':length_against_casing_si,
        'pressureloss':pressureloss_openhole,
        'Pressure_Loss_OpenHole':dP,
        'Pressure_Loss_CasedHole':dp_casing,
        'flowregime':flowregime
    }
    return data

def allannular_pressureloss(bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth):
    allpressureloss=[]
    length_of_open_hole=length_of_selected_section_from_surface-length_of_previous_casing_from_surface
    bhaelement=BhaElement.objects.filter(length_onejoint=sectiontodepth).first()
    previousbhaelement=BhaElement.objects.filter(Q(type_name='Drill Pipe') | Q(type_name='Heavy Weight Drill Pipe') | Q(type_name='Drill Collar') | Q(type_name='NMDC') | Q(type_name='Stabilizer') | Q(type_name='Jar')).filter(bhadata_id=bhadata.id).order_by('-id')
    bhacount=previousbhaelement.count()
    i=bhacount
    previous_length_against_casing=[]
    for previousbha in previousbhaelement:
        if(previousbha.length_onejoint<sectiontodepth):
            newlength=converttofloat(previousbha.length)
        else:
            belowbha=BhaElement.objects.filter(Q(type_name='Drill Pipe') | Q(type_name='Heavy Weight Drill Pipe') | Q(type_name='Drill Collar') | Q(type_name='NMDC') | Q(type_name='Stabilizer') | Q(type_name='Jar')).filter(bhadata_id=bhadata.id,id__lt=previousbha.id).order_by('-id').first()
            newlength=sectiontodepth-belowbha.length_onejoint
        viscocity=getallviscocity(muddata)
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
        sectionname=muddata.section
        rheogramsections=RheogramSections.objects.filter(section_name=sectionname).first()
        sections=Sections.objects.filter(section_name=sectionname).first()
        viscocity_newtonian=calculate_viscocity_newtonian(rheogramsections,sections,muddata)
        viscocity_bingham=calculate_viscocity_bingham(rheogramsections,sections,muddata)
        viscocity_powerlaw=calculate_viscocity_powerlaw(rheogramsections,sections,muddata)
        viscocity_hershel=calculate_viscocity_hershel(rheogramsections,sections,muddata) 
        
        pressureloss_newtonian=calculate_newtonian_anuularpressureloss(viscocity_newtonian,flowrate,muddata.mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,length_against_casing,length_against_open_hole)
        pressureloss_bingham=calculate_bingham_anuularpressureloss(viscocity_bingham,flowrate,muddata.mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,length_against_casing,length_against_open_hole,wellphasetodepth)
        pressureloss_powerlaw=calculate_powerlaw_anuularpressureloss(viscocity_powerlaw,flowrate,muddata.mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,length_against_casing,length_against_open_hole,wellphasetodepth)
        pressureloss_hershel=calculate_hershel_anuularpressureloss(viscocity_hershel,flowrate,muddata.mud_weight,rpm,od_of_pipe_element,hole_size,id_of_previous_casing,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,length_of_open_hole,bitdepth,length_of_openhole_from_bitdepth,length_against_casing,length_against_open_hole,wellphasetodepth)


        if(pressureloss_newtonian["length_against_casing"]!=0):
            allpressureloss.append({
                'type':previousbha.type_name,
                'od':round(converttofloat(od_of_pipe_element),2),
                'id':round(converttofloat(previousbha.identity),2),
                'length':round(converttofloat(newlength),2),
                'newtonion':pressureloss_newtonian["Pressure_Loss_CasedHole"],
                'bingham':pressureloss_bingham["Pressure_Loss_CasedHole"],
                'powerlaw':pressureloss_powerlaw["Pressure_Loss_CasedHole"],
                'hershel':pressureloss_hershel["Pressure_Loss_CasedHole"],
                'length_against':pressureloss_newtonian["length_against_casing"]*3.281,
                'element_type':'CH'
                })
        if(pressureloss_newtonian["length_against_open_hole"]!=0):
            allpressureloss.append({
                'type':previousbha.type_name,
                'od':round(converttofloat(od_of_pipe_element),2),
                'id':round(converttofloat(previousbha.identity),2),
                'length':round(converttofloat(newlength),2),
                'newtonion':pressureloss_newtonian["Pressure_Loss_OpenHole"],
                'bingham':pressureloss_bingham["Pressure_Loss_OpenHole"],
                'powerlaw':pressureloss_powerlaw["Pressure_Loss_OpenHole"],
                'hershel':pressureloss_hershel["Pressure_Loss_OpenHole"],
                'length_against':pressureloss_newtonian['length_against_open_hole']*3.281,
                'element_type':'OH'
                })
        previouselement_length=previousbha.length_onejoint
        i -=1
    return allpressureloss

def allsurface_losses(rpm,flowrate,wellphase_id,section_name,muddata,wellphase,previous_wellphase,wellphasefromdepth,wellphasetodepth,sectionfromdepth,sectiontodepth,well_id):
    surfacepipe=SurfacePipe.objects.filter(well_id=well_id).first()
    surfacepipedata=SurfacePipeData.objects.filter(surfacepipe_id=surfacepipe)
    sectionname=muddata.section
    rheogramsections=RheogramSections.objects.filter(section_name=sectionname).first()
    sections=Sections.objects.filter(section_name=sectionname).first()
    viscocity_newtonian=calculate_viscocity_newtonian(rheogramsections,sections,muddata)
    viscocity_bingham=calculate_viscocity_bingham(rheogramsections,sections,muddata)
    viscocity_powerlaw=calculate_viscocity_powerlaw(rheogramsections,sections,muddata)
    viscocity_hershel=calculate_viscocity_hershel(rheogramsections,sections,muddata)
    unit = getprojectunit(well_id)
    allpressureloss=[]
    for surfacedata in surfacepipedata:
        if(surfacedata.length !='' and surfacedata.identity !=''):
            pressureloss_newtonian=calculate_newtonian_pressureloss(unit,rpm,flowrate,muddata.mud_weight,surfacedata.identity,surfacedata.length,viscocity_newtonian['plastic_viscosity'])
            pressureloss_bingham=calculate_bingham_pressureloss(unit,rpm,flowrate,muddata.mud_weight,surfacedata.identity,surfacedata.length,viscocity_bingham['plastic_viscosity'],viscocity_bingham['yieldpoint'])
            pressureloss_powerlaw=calculate_powerlaw_pressureloss(unit,flowrate,muddata.mud_weight,surfacedata.identity,surfacedata.length,viscocity_powerlaw,'allsurfaceloss')
            pressureloss_hershel=calculate_hershel_pressureloss(unit,flowrate,muddata.mud_weight,surfacedata.identity,surfacedata.length,viscocity_hershel)
            allpressureloss.append({
                'type':surfacedata.name,
                'id':surfacedata.identity,
                'length':surfacedata.length,
                'newtonian_pressureloss':round(pressureloss_newtonian["pressureloss"],2),
                'bingham_pressureloss':round(pressureloss_bingham["pressureloss"],2),
                'powerlaw_pressureloss':round(pressureloss_powerlaw["pressureloss"],2),
                'hershel_pressureloss':round(pressureloss_hershel["pressureloss"],2)
            })
    return allpressureloss

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




def getallviscocity(muddata):
    sectionname=muddata.section
    data={}
    rheogramsections=RheogramSections.objects.filter(section_name=sectionname).first()
    sections=Sections.objects.filter(section_name=sectionname).first()
    data1=calculate_viscocity_newtonian(rheogramsections,sections,muddata)
    data2=calculate_viscocity_bingham(rheogramsections,sections,muddata)
    data3=calculate_viscocity_powerlaw(rheogramsections,sections,muddata)
    data4=calculate_viscocity_hershel(rheogramsections,sections,muddata)
    data={
        'data1':data1,
        'data2':data2,
        'data3':data3,
        'data4':data4
    }

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
def getsectionrange(request):
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    muddata=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    sectionfromdepth=round(muddata.from_depth)
    sectiontodepth=round(muddata.todepth)
    rangelabels=[]
    i=sectionfromdepth
    while i<sectiontodepth:
        rangelabels.append(i)
        i +=500
    lastrange=rangelabels[-1]
    if(lastrange<sectiontodepth):
        rangelabels.append(lastrange+500)
    data={}
    data['sectionfromdepth']=sectionfromdepth
    data['sectiontodepth']=rangelabels[-1]
    data['rangelabels']=rangelabels
    return JsonResponse(data,safe=False)


  
def calculatesensitivity(request):
    rpm=request.GET['rpm']
    flowrate=int(request.GET['flowrate'])
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    well_id=request.session['well_id']
    torque=request.GET['torque'] if 'torque' in request.GET else ""
    wob=request.GET['wob'] if 'wob' in request.GET else ""
    rop=request.GET['rop']
    givenbitdepth=request.GET['bitdepth']

    cuttings_density=converttofloat(request.GET['cuttings_density'])
    cuttings_size=converttofloat(request.GET['cuttings_size'])
    unit = getprojectunit(well_id)
    wellphase = WellPhases.objects.filter(id=wellphase_id).first()
    previous_wellphase=WellPhases.objects.filter(id__lt=wellphase.id,well_id=well_id).order_by('-id').first()
    muddata=MudData.objects.getmuddata_bywellphase(wellphase_id,section_name)
    sectionfromdepth=muddata.from_depth
    sectiontodepth=muddata.todepth if(givenbitdepth=='') else int(givenbitdepth)
    if(sectiontodepth>muddata.todepth):
        sectiontodepth=muddata.todepth
    # print(f"sectiontodepth {sectiontodepth}")
    bhadata=BhaData.objects.filter(well_phases_id=wellphase_id,status=1).first()
    length_of_previous_casing_from_surface=previous_wellphase.measured_depth
    data={}
    length_of_selected_section_from_surface=sectiontodepth

    hole_size=wellphase.hole_size
    id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
    bitdepth=sectiontodepth if(givenbitdepth=='') else int(givenbitdepth)
    if(bitdepth>muddata.todepth):
        bitdepth=muddata.todepth
    # print(f"bitdepth {bitdepth}")
    mudweight=float(request.GET['mudweight']) if request.GET['mudweight'] != ''  else muddata.mud_weight
    length_of_openhole_from_bitdepth=bitdepth-length_of_previous_casing_from_surface

    wellphasetodepth= wellphase.measured_depth
    viscocity=getviscocity(muddata)
    tvd=gettvd(sectiontodepth,well_id,request,sectiontodepth)
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

            i=maximum_pore_pressure
            allmud_weight=[]
            while i<min_fracture_pressure:
                allmud_weight.append(i)
                i +=0.5
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
    
   
    request.session['mudweight_range']=allmud_weight

    allmud_weight_pressureloss=[]
    allannularloss=[]
    alldrillstringloss=[]
    allbitloss=[]
    allsurfaceloss=[]
    totalpressureloss=[]
    rheogramsections=RheogramSections.objects.filter(section_name=section_name).first()
    t300=rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=None,rpm=300).first()
    t600=rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=None,rpm=600).first()
    t3=rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=None,rpm=3).first()
    t6=rheogram=Rheogram.objects.filter(rheogram_sections_id=rheogramsections.id,status=1,modelname=None,rpm=6).first()
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
        # ecd=mud_weight+pressureoss['totalannular_pressureloss']/(0.052*tvd)
        ecd = calcualte_ecd(mud_weight,pressureoss['totalannular_pressureloss'],tvd,unit)
        mudweight_ecd.append({'x':mud_weight,'y':round(ecd,2)})

    flowrate_values=calculate_flowrate_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request,tvd)

    plastic_viscocity_values=calculate_viscocity_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,t300,t600,t3,t6,tvd)

    yield_point_values=calculate_yieldpoint_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase)

    tfa_values=calculate_tfa_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request)

    
    rop_values=calculate_rop_change(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request,tvd,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth)

    cuttings_density_values=calculate_cuttings_density(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request,tvd,rop,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth)

    cuttings_size_values=calculate_cuttings_size(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mudweight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity,torque,wob,cuttings_density,cuttings_size,muddata,well_id,wellphase_id,section_name,wellphase,previous_wellphase,request,tvd,rop,length_of_selected_section_from_surface,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth)



        

    data['allannularloss']=allannularloss
    data['alldrillstringloss']=alldrillstringloss
    data['allbitloss']=allbitloss
    data['allsurfaceloss']=allsurfaceloss
    data['totalpressureloss']=totalpressureloss
    
    data['flowrateallannularloss']=flowrate_values["allannularloss"]
    data['flowrate']=flowrate
    data['rop']=rop
    data['mud_weight']=muddata.mud_weight

    data['cuttings_size']=cuttings_size
    data['cuttings_density']=cuttings_density
  

    data['flowratealldrillstringloss']=flowrate_values["alldrillstringloss"]
    data['flowrateallbitloss']=flowrate_values["allbitloss"]
    data['flowrateallsurfaceloss']=flowrate_values["allsurfaceloss"]
    data['flowratetotalpressureloss']=flowrate_values["totalpressureloss"]

    data['viscocityallannularloss']=plastic_viscocity_values["allannularloss"]
    data['viscocityalldrillstringloss']=plastic_viscocity_values["alldrillstringloss"]
    data['viscocityallbitloss']=plastic_viscocity_values["allbitloss"]
    data['viscocityallsurfaceloss']=plastic_viscocity_values["allsurfaceloss"]
    data['viscocitytotalpressureloss']=plastic_viscocity_values["totalpressureloss"]

    data['yieldallannularloss']=yield_point_values["allannularloss"]
    data['yieldalldrillstringloss']=yield_point_values["alldrillstringloss"]
    data['yieldallbitloss']=yield_point_values["allbitloss"]
    data['yieldallsurfaceloss']=yield_point_values["allsurfaceloss"]
    data['yieldtotalpressureloss']=yield_point_values["totalpressureloss"]
    data['tfa_chart']=tfa_values['bit_pressure_chart']
    data['allchart_bit']=tfa_values['allchart_data']
    data['flowrate_ecd']=flowrate_values['flowrate_ecd']
    data['mudweight_ecd']=mudweight_ecd
    data['viscocity_ecd']=plastic_viscocity_values['viscocity_ecd']
    data['cuttings_size_ecd']=cuttings_size_values
    data['cuttings_density_ecd']=cuttings_density_values
    data['rop_ecd_with']=rop_values['rop_ecd_with_chart']
    data['rop_ecd_without']=rop_values['rop_ecd_without_chart']
    data['cuttings_size_withoutecd']=cuttings_size_values['cuttings_size_withoutecd']
    data['cuttings_size_withecd']=cuttings_size_values['cuttings_size_withecd']
    data['cuttings_density_withecd']=cuttings_density_values['cuttings_density_withecd']
    data['cuttings_density_withoutecd']=cuttings_density_values['cuttings_density_withoutecd']


    # print(f"mudweight_ecd {mudweight_ecd}")
    rangelabels=[]
    i=round(sectionfromdepth)
    while i<round(sectiontodepth):
        rangelabels.append(i)
        i +=100
    lastrange=rangelabels[-1]
    if(lastrange<round(sectiontodepth)):
        rangelabels.append(round(sectiontodepth))
    
    # print(f"rangelabels {rangelabels}")
    data['sectionfromdepth']=sectionfromdepth
    data['sectiontodepth']=sectiontodepth
    data['rangelabels']=rangelabels


    return JsonResponse(data,safe=False)






# def getbitpressureloss_manual_values(mudweight,flowrate,cd_values,tfa_value,hole_size,unit):
#     if unit == 'API':
#         bit_pressure_loss = mudweight*flowrate**2/(12042*cd_values**2*tfa_value**2)
#         bhhp = bit_pressure_loss*500/1714
#         hsi = bhhp/(pi/4*hole_size**2)
#         impact_forces = 0.01823*cd_values*flowrate*sqrt(mudweight*bit_pressure_loss)
#         jet_velocity = 0.32086*flowrate/tfa_value
#     else:
#         bit_pressure_loss = (mudweight*1000*(3.7854/flowrate*0.000063)**2/(2000*cd_values**2*(tfa_value/1000000)**2))
#         print(f'bit_pressure_loss {bit_pressure_loss}')
#     return bit_pressure_loss



















def calculateapl_withoutanychart(bhadata,sectiontodepth,length_of_previous_casing_from_surface,mud_weight,id_of_previous_casing,flowrate,rpm,hole_size,viscocity):
    previousbhaelement=BhaElement.objects.filter(bhadata_id=bhadata.id).exclude(type_name='Bit').order_by('-id')
    bhacount=previousbhaelement.count()
    i=bhacount
    previous_length_against_casing=[]
    totalapl=0
    for previousbha in previousbhaelement:
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
        if(length_against_casing!=0):
            pressureloss=calculate_annular_loss(bhadata.well_id,viscocity,flowrate,rpm,mud_weight,previousbha.od,id_of_previous_casing,length_against_casing,'annularpressureloss')
            totalapl +=pressureloss['pressureloss']
        if(length_against_open_hole!=0):
            pressureloss=calculate_annular_loss(bhadata.well_id,viscocity,flowrate,rpm,mud_weight,previousbha.od,hole_size,length_against_open_hole,'annularpressureloss')
            totalapl +=pressureloss['pressureloss']
        previouselement_length=previousbha.length_onejoint
        i -=1
    return totalapl

def hydraulicdata(request,wellphase_id):
    well_id=request.session['well_id']
    if request.method == 'POST':
        md=request.POST.getlist('md')
        flowrate=request.POST.getlist('flowrate')
        rop=request.POST.getlist('rop')
        rpm=request.POST.getlist('rpm')
        pump_pressure=request.POST.getlist('pump_pressure')
        annular_pressure=request.POST.getlist('annular_pressure')
        ecd=request.POST.getlist('ecd')
        i=0
        while i < len(md):
            HydraulicData.objects.create(measured_depth=md[i],flowrate=flowrate[i],rop=rop[i],well_id=well_id,company=request.company,rpm=rpm[i],pump_pressure=pump_pressure[i],annular_pressure=annular_pressure[i],ecd=ecd[i])
            i += 1
        return redirect('muddata:hydraulic_data_view', wellphase_id=wellphase_id)
    
    hydraulic_data=HydraulicData.objects.filter(company=request.company,well_id=well_id,status=1)
    well=Wells.objects.get(id=well_id)
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    if(len(hydraulic_data) == 0):
        return render(request,'muddata/hydraulic_data.html',{'wellphase_id':wellphase_id,'well_id':well_id,'wellphases':wellphase,'countries':getcountries(request.company),'company':request.company,'well':well})
    else:
        return redirect('muddata:hydraulic_data_view', wellphase_id=wellphase_id)

def edit_hydraulic_data(request,wellphase_id):
    well_id=request.session['well_id']
    getdata=HydraulicData.objects.filter(company=request.company,well_id=well_id,status=1)
    if request.method == 'POST':
        i=0
        md=request.POST.getlist('md')
        flowrate=request.POST.getlist('flowrate')
        rop=request.POST.getlist('rop')
        rpm=request.POST.getlist('rpm')
        pump_pressure=request.POST.getlist('pump_pressure')
        annular_pressure=request.POST.getlist('annular_pressure')
        ecd=request.POST.getlist('ecd')
        hydraulic_id=request.POST.getlist('hydraulic_id')
        while i < len(md):
            if(hydraulic_id[i] ):
                HydraulicData.objects.filter(id=hydraulic_id[i]).update(measured_depth=md[i],flowrate=flowrate[i],rop=rop[i],well_id=well_id,company=request.company,rpm=rpm[i],pump_pressure=pump_pressure[i],annular_pressure=annular_pressure[i],ecd=ecd[i])
            else:
                HydraulicData.objects.create(measured_depth=md[i],flowrate=flowrate[i],rop=rop[i],well_id=well_id,company=request.company,rpm=rpm[i],pump_pressure=pump_pressure[i],annular_pressure=annular_pressure[i],ecd=ecd[i])
            i += 1
        return redirect('muddata:hydraulic_data_view', wellphase_id=wellphase_id)
    well=Wells.objects.get(id=well_id)
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    return render(request,'muddata/edit_hydraulic_data.html',{'wellphase_id':wellphase_id,'well_id':well_id,'hydraulic_data':getdata,'wellphases':wellphase,'countries':getcountries(request.company),'company':request.company,'well':well})

def hydraulic_data_view(request,wellphase_id):
    well_id=request.session['well_id']
    hydraulic_data=HydraulicData.objects.filter(well_id=well_id, company=request.company,status=1)
    paginator = Paginator(hydraulic_data, 10)
    page = request.GET.get('page', 1)
    pages = paginator.num_pages
    hydraulic = paginator.page(page)
    last_page=paginator.page(pages)
    wellphase = WellPhases.objects.filter(well_id=well_id, company=request.company,status=1)
    well=Wells.objects.get(id=well_id)
    return render(request,'muddata/hydraulic_data_view.html',{'wellphase_id':wellphase_id,'well_id':well_id,'hydraulic_data':hydraulic,'last_page':last_page,'wellphases':wellphase,'countries':getcountries(request.company),'company':request.company,'well':well})

def hydraulic_data_delete(request, wellphase_id, template_name='crudapp/confirm_delete.html'):
    well_id=request.session['well_id']
    getdata=HydraulicData.objects.filter(company=request.company,well_id=well_id).update(status=0)
    return redirect('muddata:hydraulicdata', wellphase_id=wellphase_id)

def import_hydraulic_data(request,wellphase_id):
    well_id=request.session['well_id']
    if request.method == 'POST' and 'myfile' in request.FILES:
        dataset = Dataset()
        new_datas = request.FILES['myfile']
        imported_data = dataset.load(new_datas.read(),format='xlsx')
        previous_date=''
        previous_time=''
        objs = [
            HydraulicData(
                measured_depth=data[0],flowrate=data[1],rop=data[2],well_id=well_id,company=request.company,rpm=data[3],pump_pressure=data[4],annular_pressure=data[5],ecd=data[6],well_phase_id=wellphase_id
                
            )
            for data in imported_data
        ]
        HydraulicData.objects.bulk_create(objs)

        #     HydraulicData.objects.create(measured_depth=data[0],flowrate=data[1],rop=data[2],well_id=well_id,company=request.company,rpm=data[3],pump_pressure=data[4],annular_pressure=data[5],ecd=data[6],well_phase_id=wellphase_id)
        return redirect('muddata:hydraulic_data_view', wellphase_id=wellphase_id)
    return render(request,'muddata/importdata.html',{'wellphase_id':wellphase_id,'well_id':well_id})

def downloadcsv(request,wellphase_id):
    df_output = pd.DataFrame({'MD':[],'Flowrate':[],'ROP':[],'RPM':[],'Pump_pressure':[],'Annular_pressure':[],'ECD':[]})
    
    excel_file = IO()

    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    
    df_output.to_excel(xlwriter, 'sheetname',index=False)

    xlwriter.save()
    xlwriter.close()

    excel_file.seek(0)

    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # set the file name in the Content-Disposition header
    response['Content-Disposition'] = 'attachment; filename=hydraulic_data.xlsx'

    return response

def downloadmuddatacsv(request,wellphase_id):
    df_output = pd.DataFrame({'Depth':[],'MudWeight':[],'PV':[],'YP':[],'LSRYP':[],'Gel Strength(0sec)':[],'Gel Strength(10min)':[],'Gel Strength(30min)':[]})
    # header = ['Name', 'M1 Score', 'M2 Score']
    # data = [['Alex', 62, 80], ['Brad', 45, 56], ['Joey', 85, 98]]
    # df_output = pd.DataFrame(data, columns=header)
    
    excel_file = IO()

    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    
    df_output.to_excel(xlwriter, 'sheetname',index=False)

    xlwriter.save()
    xlwriter.close()

    excel_file.seek(0)

    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # set the file name in the Content-Disposition header
    response['Content-Disposition'] = 'attachment; filename=muddata.xlsx'

    return response


# def get_all_unit(unit):
#     data={}
#     depth_unit = app_filters.display_depthunit(unit)
#     length_unit = app_filters.display_lengthunit(unit)
#     pressure_unit = app_filters.display_pressureunit(unit)
#     diameter_unit = app_filters.display_diameterunit(unit)
#     data['depth']=depth_unit
#     data['length']=length_unit
#     data['pressure']=pressure_unit
#     data['diameter']=diameter_unit
#     return JsonResponse(data)

def planfinal_data(request):
    flowrate=request.GET['flowrate']
    rpm=request.GET['rpm']
    rop=request.GET['rop']
    bitdepth=request.GET['bitdepth']
    surface_pressure=request.GET['surface_pressure']
    ecd=request.GET['ecd']
    well_id=request.GET['well_id']
    wellphase_id=request.GET['wellphase_id']
    section_name=request.GET['section_name']
    datas=Planwell_data.objects.filter(well_id=well_id,well_phase_id=wellphase_id,section_name=section_name,status=1,company=request.company)
    bitdepth_data = bitdepth if(bitdepth!='') else None  
    if(datas.count()==0):
        Planwell_data.objects.create(flowrate=flowrate,rpm=rpm,rop=rop,well_id=well_id,well_phase_id=wellphase_id,section_name=section_name,bitdepth=bitdepth_data,surface_pressure=surface_pressure,ecd=ecd,status=1,company=request.company)
    else:
        Planwell_data.objects.filter(well_id=well_id,well_phase_id=wellphase_id,section_name=section_name).update(flowrate=flowrate,rpm=rpm,rop=rop,bitdepth=bitdepth_data,surface_pressure=surface_pressure,ecd=ecd)
    Pressureloss_data.objects.filter(well_id=well_id,well_phase_id=wellphase_id,section_name=section_name).update(status=1)
    return JsonResponse({'data':flowrate})


def get_planwell_data(request):
    well_id=request.GET['well_id']
    planwell_id=request.GET['planwell_id']
    wellphase_id=request.GET['wellphase_id']
    last_depth=request.GET['last_depth']
    all_plandata={}
    plan_surface=[]

    previouswellphase=WellPhases.objects.filter(id__lt=wellphase_id,well_id=well_id,status=1).order_by("-id").values('measured_depth','id')[:1]
    fromdepth=0 if previouswellphase.count()==0 else previouswellphase[0]['measured_depth']
    todepth=WellPhases.objects.filter(id=wellphase_id,well_id=well_id, company=request.company,status=1).last()
    # print(f"todepth {todepth}")
    # print(f"fromdepth {fromdepth}")
    
    hydralics_data = HydraulicData.objects.filter(well_id=well_id,status=1,company=request.company,measured_depth__lte=todepth.measured_depth,measured_depth__gte=fromdepth)[:30]
    for data in hydralics_data:
        # print(data.measured_depth)
        wellphase=WellPhases.objects.filter(well_id=planwell_id,company=request.company,status=1,measured_depth__gte=data.measured_depth).order_by('measured_depth').first()
        # print(f"wellphase {wellphase}")
        bhadata=BhaData.objects.filter(well_phases_id=wellphase.id,status=1).first()
        sectiontodepth=data.measured_depth 
        section=Sections.objects.filter(well_id=planwell_id,company=request.company,status=1,well_phase_id=wellphase.id,from_depth__lte=sectiontodepth,todepth__gte=sectiontodepth).first()
        muddata=MudData.objects.filter(well_id=planwell_id,section=section.section_name,well_phase_id=wellphase.id,company=request.company,status=1).first()
        plan_data=Planwell_data.objects.filter(well_id=planwell_id,company=request.company,well_phase_id=wellphase.id,status=1,section_name=section.section_name).first()

        previous_wellphase=WellPhases.objects.filter(id__lt=wellphase.id,well_id=planwell_id).order_by('-id').first()
        length_of_previous_casing_from_surface=0 if previous_wellphase==None else previous_wellphase.measured_depth
        length_of_selected_section_from_surface=sectiontodepth
        hole_size=wellphase.hole_size
        id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
        bitdepth=sectiontodepth
        length_of_openhole_from_bitdepth=bitdepth-length_of_previous_casing_from_surface
        wellphasetodepth= wellphase.measured_depth

        cuttings_density=21
        cuttings_size=0.25
        torque=0
        wob=0
        viscocity=getviscocity(muddata)
        previous_measured_depth=0 if previous_wellphase==None else previous_wellphase.measured_depth
        previous_true_vertical_depth=0 if previous_wellphase==None else previous_wellphase.true_vertical_depth


        annular_pressure_loss=calculateannular_pressureloss(planwell_id,bhadata,sectiontodepth,muddata,plan_data.rpm,plan_data.flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,cuttings_density,cuttings_size,torque,wob,plan_data.rop,viscocity,'calculateallpressureloss')
        surface_losses=getsurfacelosses(plan_data.rpm,plan_data.flowrate,wellphase.id,section.section_name,muddata.mud_weight,wellphase,previous_wellphase,planwell_id,viscocity,'check')
        bit_losses=getbitpressureloss(plan_data.rpm,plan_data.flowrate,wellphase.id,section.section_name,muddata.mud_weight,wellphase,previous_wellphase,planwell_id)
        # if(data.measured_depth==7496):
        all_plandata['ecdchartdata']=ecdcalculation(int(last_depth),wellphase.true_vertical_depth,previous_measured_depth,previous_true_vertical_depth,muddata.mud_weight,annular_pressure_loss['allpressureloss'],well_id,request,'with')
        # print(f"all_plandata['ecdchartdata'] {all_plandata['ecdchartdata']}")

        all_plandata['surface_losses']=surface_losses
        all_plandata['bit_losses']=bit_losses

        annular_loss=0
        pipe_loss=0
        surface_loss=0
        bit_loss=0
        for annular in annular_pressure_loss['allpressureloss']:
            annular_loss+=annular['pressureloss']
            pipe_loss+=annular['drillstringloss']
        for surface in surface_losses:
            surface_loss+=surface['pressureloss']
        for bit in bit_losses:
            bit_loss+=bit['bit_pressure_loss']
        totalpressureloss= bit_loss+surface_loss+annular_loss+pipe_loss
        plan_surface.append(totalpressureloss)
    all_plandata['plan_surface']=plan_surface





    return JsonResponse(all_plandata)















  

# def get_planwell_data(request):
#     well_id=request.GET['well_id']
#     planwell_id=request.GET['planwell_id']
#     wellphase_id=request.GET['wellphase_id']
#     last_depth=request.GET['last_depth']
#     all_plandata={}
#     # plan_data=Planwell_data.objects.filter(well_id=planwell_id,company=request.company,well_phase_id=59)
#     # print(plan_data)
#     previouswellphase=WellPhases.objects.filter(id__lt=wellphase_id,well_id=well_id,status=1).order_by("-id").values('measured_depth','id')[:1]
#     fromdepth=0 if previouswellphase.count()==0 else previouswellphase[0]['measured_depth']
#     todepth=WellPhases.objects.filter(id=wellphase_id,well_id=well_id, company=request.company,status=1).last()
#     # alldepth=HydraulicData.objects.filter(well_id=well_id,status=1,measured_depth__lte=todepth.measured_depth,measured_depth__gte=fromdepth).values('measured_depth')
#     # print(alldepth)
#     hydralics_data = HydraulicData.objects.filter(well_id=well_id,status=1,company=request.company,measured_depth__lte=todepth.measured_depth,measured_depth__gte=fromdepth)
#     surface=[]
#     ecd=[]
#     plan_surface=[]
#     plan_ecd=[]
#     for data in hydralics_data:
#         # print(data.measured_depth)
#         wellphase=WellPhases.objects.filter(well_id=planwell_id,company=request.company,status=1,measured_depth__gte=data.measured_depth).order_by('measured_depth').last()
#         if(wellphase!= None):
#             section=Sections.objects.filter(well_id=planwell_id,company=request.company,status=1,well_phase_id=wellphase.id).order_by('todepth').first() 
#             plan_data=Planwell_data.objects.filter(well_id=planwell_id,company=request.company,well_phase_id=wellphase.id,status=1).first()
#             if(plan_data !=None and section!=None):
#                 # print(f'section {section.section_name}')
#                 # print(f'wellphase {wellphase}')
#                 # print(f'planwell_id {planwell_id}')
#                 # surface.append(plan_data.surface_pressure)
#                 # ecd.append(plan_data.ecd)
#                 muddata=MudData.objects.filter(well_id=planwell_id,section=section.section_name,well_phase_id=wellphase.id,company=request.company,status=1).first()
#                 # print(f'muddata {muddata}')
#                 previous_wellphase=WellPhases.objects.filter(id__lt=wellphase.id,well_id=planwell_id).order_by('-id').first()
#                 length_of_previous_casing_from_surface=0 if previous_wellphase==None else previous_wellphase.measured_depth
#                 wellphasefromdepth=0 if previous_wellphase==None else previous_wellphase.measured_depth
#                 wellphasetodepth= wellphase.measured_depth
#                 sectionfromdepth=muddata.from_depth
#                 sectiontodepth=data.measured_depth 
#                 liner_wellphase=WellPhases.objects.filter(well_id=planwell_id,status=1).values('lineartop')
#                 previous_measured_depth=0 if previous_wellphase==None else previous_wellphase.measured_depth
#                 previous_true_vertical_depth=0 if previous_wellphase==None else previous_wellphase.true_vertical_depth
#                 previous_linear=0 if previous_wellphase==None else previous_wellphase.measured_depth
#                 bitdepth=data.measured_depth 
#                 length_of_openhole_from_bitdepth=bitdepth-length_of_previous_casing_from_surface
#                 length_of_selected_section_from_surface=sectiontodepth
#                 hole_size=wellphase.hole_size
#                 id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
#                 checkliner=WellPhases.objects.filter(Q(casing_type_id=7) | Q(casing_type_id=8) | Q(casing_type_id=11) | Q(casing_type_id=12)).filter(well_id=planwell_id,status=1,measured_depth__lt=sectiontodepth)
#                 bhadata=BhaData.objects.filter(well_id=planwell_id,well_phases_id=wellphase.id,status=1).first()
#                 # plan_data=Planwell_data.objects.filter(well_id=planwell_id,well_phase_id=wellphase.id).last()
#                 torque_data=Differential_pressure.objects.filter(bhadata_id=bhadata.id) 
#                 wob_data=Specifications.objects.filter(bhadata_id=bhadata.id) 
#                 torque = torque_data if torque_data else 0
#                 wob = wob_data if wob_data else 0
#                 cuttings_density=21
#                 cuttings_size=0.25
#                 viscosity=getviscocity(muddata)
#                 annular_data=calculateannular_pressureloss(planwell_id,bhadata,sectiontodepth,muddata,plan_data.rpm,plan_data.flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,float(cuttings_density),float(cuttings_size),torque,wob,plan_data.rop,viscosity,'calculateannular_pressureloss')
#                 surface_losses=getsurfacelosses(plan_data.rpm,plan_data.flowrate,wellphase.id,section.section_name,muddata.mud_weight,wellphase,previous_wellphase,planwell_id,viscosity,'check')
#                 bit_losses=getbitpressureloss(plan_data.rpm,plan_data.flowrate,wellphase.id,section.section_name,muddata.mud_weight,wellphase,previous_wellphase,planwell_id)
#                 all_plandata['ecdchartdata']=ecdcalculation(int(last_depth),wellphase.true_vertical_depth,previous_measured_depth,previous_true_vertical_depth,muddata.mud_weight,annular_data['allpressureloss'],planwell_id,request,'with')
#                 all_plandata['surface_losses']=surface_losses
#                 all_plandata['bit_losses']=bit_losses
#                 annular_loss=0
#                 pipe_loss=0
#                 surface_loss=0
#                 bit_loss=0
#                 for annular in annular_data['allpressureloss']:
#                     annular_loss+=annular['pressureloss']
#                     pipe_loss+=annular['drillstringloss']
#                 for surface in surface_losses:
#                     surface_loss+=surface['pressureloss']
#                 for bit in bit_losses:
#                     bit_loss+=bit['bit_pressure_loss']
#                 totalpressureloss= bit_loss+surface_loss+annular_loss+pipe_loss
#                 plan_surface.append(totalpressureloss)
#     # print(f'totalpressureloss {plan_surface}')
#     # all_plandata['plan_data']=plan_data
#     all_plandata['surface_pressure']=surface
#     # all_plandata['ecd']=ecd
#     # print(f'plan_ecd {plan_ecd}')
#     all_plandata['plan_surface']=plan_surface
#     all_plandata['plan_ecd']=plan_ecd
#     # print(all_plandata)
#     # plan_wellphase = WellPhases.objects.filter(id=80,status=1).first()
#     # previous_wellphase=WellPhases.objects.filter(id__lt=plan_wellphase.id).order_by('-id').first()
#     # previous_measured_depth=0 if previous_wellphase==None else previous_wellphase.measured_depth
#     # previous_true_vertical_depth=0 if previous_wellphase==None else previous_wellphase.true_vertical_depth
#     # # muddatas=MudData.objects.filter(well_id=well_id,status=1).order_by('todepth')
#     # mudweight=10.43

#     # bhadata=BhaData.objects.filter(well_phases_id=plan_wellphase.id,status=1).first()
#     # section=Sections.objects.filter(well_id=planwell_id,company=request.company,status=1,well_phase_id=plan_wellphase.id).order_by('todepth').first() 
#     # muddata=MudData.objects.filter(well_phase_id=plan_wellphase.id,section=section.section_name,status=1).first()
#     # sectiontodepth=muddata.todepth
#     # length_of_selected_section_from_surface=sectiontodepth
#     # hole_size=plan_wellphase.hole_size
#     # bitdepth=plan_wellphase.measured_depth 
#     # length_of_previous_casing_from_surface=0 if previous_wellphase==None else previous_wellphase.measured_depth
#     # length_of_openhole_from_bitdepth=bitdepth-length_of_previous_casing_from_surface
#     # length_of_selected_section_from_surface=sectiontodepth
#     # hole_size=plan_wellphase.hole_size
#     # id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
#     # wellphasetodepth= plan_wellphase.measured_depth
#     # torque_data=Differential_pressure.objects.filter(bhadata_id=bhadata.id) 
#     # wob_data=Specifications.objects.filter(bhadata_id=bhadata.id) 
#     # torque = torque_data if torque_data else 0
#     # wob = wob_data if wob_data else 0
#     # cuttings_density=21
#     # cuttings_size=0.25
#     # flowrate=500
#     # rpm=120
#     # rop=50
#     # viscosity=getviscocity(muddata)
#     # plan_annular=calculateannular_pressureloss(planwell_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,float(cuttings_density),float(cuttings_size),torque,wob,rop,viscosity,'calculateannular_pressureloss')
#     # all_plandata['ecdchartdata']=ecdcalculation(int(last_depth),plan_wellphase.true_vertical_depth,previous_measured_depth,previous_true_vertical_depth,mudweight,plan_annular['increased_pressureloss'],planwell_id,request,'with')
#     print(all_plandata['ecdchartdata'])
#     return JsonResponse(all_plandata)

def addselected_data(request):
    selected_model=request.GET['selected_model']
    wellphase_id=request.GET['wellphase_id']
    well_id=request.GET['well_id']
    hydralics_data = HydraulicData.objects.filter(well_id=well_id,well_phase_id=wellphase_id,status=1,company=request.company).last()
    print(f"hydralics_data {hydralics_data}")

    muddata=MudData.objects.filter(well_id=well_id,well_phase_id=wellphase_id,todepth__lte=hydralics_data.measured_depth).last()
    RheogramDate.objects.filter(well_phase_id=wellphase_id,muddata_id=muddata.id,status=1).update(selected_model=selected_model)
    return JsonResponse({"data": selected_model})


def get_calculated_data(request):
    well_id=request.GET['well_id']
    planwell_id=request.GET['planwell_id']
    wellphase_id=request.GET['wellphase_id']
    cuttings_density =request.GET['cutting_density']
    cuttings_size =request.GET['cutting_size']
    last_depth=request.GET['user_depth']
    selected_model=request.GET['selected_model']
    hydralics_data = HydraulicData.objects.filter(well_id=well_id,status=1,company=request.company).last()
    muddata=MudData.objects.filter(well_id=well_id,well_phase_id=wellphase_id,todepth__lte=last_depth).last()
    bhadata=BhaData.objects.filter(well_id=well_id,well_phases_id=wellphase_id,depth__lte=last_depth,status=1).last()
    wellphase=WellPhases.objects.filter(id=wellphase_id,well_id=well_id).last()
    rheology_date=RheogramDate.objects.filter(well_id=well_id,well_phase_id=wellphase_id,muddata_id=muddata.id,status=1)
    sectiontodepth=muddata.todepth
    rpm=hydralics_data.rpm
    flowrate=hydralics_data.flowrate
    rop=hydralics_data.rop
    length_of_selected_section_from_surface=muddata.todepth
    previous_wellphase=WellPhases.objects.filter(id__lt=wellphase_id,well_id=well_id).order_by('-id').first()
    length_of_previous_casing_from_surface=previous_wellphase.measured_depth
    hole_size=wellphase.hole_size
    wellphasetodepth= wellphase.measured_depth
    id_of_previous_casing=hole_size if previous_wellphase==None else previous_wellphase.drift_id
    bitdepth=sectiontodepth
    length_of_openhole_from_bitdepth=bitdepth-length_of_previous_casing_from_surface
    
    torque_data=Differential_pressure.objects.filter(bhadata_id=bhadata.id) 
    wob_data=Specifications.objects.filter(bhadata_id=bhadata.id) 
    torque = torque_data if torque_data else 0
    wob = wob_data if wob_data else 0
    
    if(selected_model == '1'):
        viscosity = calculate_viscocity_newtonian(rheology_date,'sections',muddata)
    elif(selected_model == '2'):
        viscosity = calculate_viscocity_bingham(rheology_date,'sections',muddata)
    elif(selected_model == '3'):
        viscosity = calculate_viscocity_powerlaw(rheology_date,'sections',muddata)
    else:
        viscosity = calculate_viscocity_hershel(rheology_date,'sections',muddata)
    output_data={}
    annular_data=calculateannular_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate,length_of_previous_casing_from_surface,length_of_selected_section_from_surface,hole_size,id_of_previous_casing,bitdepth,length_of_openhole_from_bitdepth,wellphasetodepth,float(cuttings_density),float(cuttings_size),torque,wob,rop,viscosity,'calculateannular_pressureloss')
    # bore_pressure_loss=calculatepipe_pressureloss(well_id,bhadata,sectiontodepth,muddata,rpm,flowrate)
    # print(bore_pressure_loss)
    output_data['annular_data']=annular_data
    length_cci=len(annular_data['cci'])
    max_cci=annular_data['cci'][length_cci-1]['x']
    output_data['max_cci']=max_cci
    return JsonResponse(output_data)


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



def actualwell_generate_report(request,wellphase_id):
    well_id=request.session['well_id']
    flowrate=request.GET['Flowrate'] if 'Flowrate' in request.GET else 0
    rop=request.GET['ROP'] if 'ROP' in request.GET else 0
    rpm=request.GET['RPM'] if 'RPM' in request.GET else 0
    print(f"flowrate {flowrate}")
    print(f"rop {rop}")
    print(f"rop {rpm}")

    template= 'muddata/actualwell_report.html'
    filename="Phase Report.pdf"
    previouswellphase=WellPhases.objects.filter(id__lt=wellphase_id,well_id=well_id,status=1).order_by("-id").values('measured_depth','id','date','true_vertical_depth')[:1]
    fromdepth=0 if previouswellphase.count()==0 else previouswellphase[0]['measured_depth']
    fromtvd=0 if previouswellphase.count()==0 else previouswellphase[0]['true_vertical_depth']
    wellphase=WellPhases.objects.filter(id=wellphase_id,well_id=well_id, company=request.company,status=1).last()
    print(f'depth {wellphase.measured_depth}')
    print(f"fromdepth {fromdepth}")

    hydraulic_data=HydraulicData.objects.filter(well_id=well_id,status=1,measured_depth__lte=wellphase.measured_depth,measured_depth__gte=fromdepth)
    context={
        'fromdepth':fromdepth,
        'fromtvd':fromtvd,
        'wellphase':wellphase,
        'fromdate':previouswellphase[0]['date'],
        'hydraulic_data':hydraulic_data,
        'wellphase_id':wellphase_id,
        'flowrate':flowrate,
        'rop':rop,
        'rpm':rpm
    }
    response=render_to_pdf_response(request,template,context,filename=filename) 
    response['Content-Disposition'] = 'inline;filename='+filename+''
    return response   




def chart_image(request):
    images=request.POST.get('data[png]')
    filename=request.POST.get('data[filename]')
    image = base64.b64decode(images) 
    imagePath = ('media/'+filename+'.png')
    img = Image.open(io.BytesIO(image))
    img.save(imagePath, 'png') 
    return JsonResponse('success',safe=False)
    
def sensitivity_report(request,wellphase_id):
    well_id=request.session['well_id']
    section_name=request.GET['section_name']
    bhadata=BhaData.objects.filter(well_phases=wellphase_id,well=well_id,status=1).first()
    bhaelement=BhaElement.objects.filter(bhadata=bhadata.id,status=1)
    muddata=MudData.objects.filter(section=section_name,well_phase=wellphase_id,well=well_id,status=1)
    rheogram_section=RheogramSections.objects.filter(section_name=section_name,well_phase=wellphase_id,status=1).first()
    rheogram_data=Rheogram.objects.filter(rheogram_date=rheogram_section.rheogram_date_id,well=well_id,rheogram_sections=rheogram_section.id,status=1)
    drillbit=DrillBit.objects.filter(well_phases=wellphase_id,well=well_id,status=1).first()
    drillbit_nozzle=DrillBitNozzle.objects.filter(drillbit_id=drillbit.id,well=well_id,status=1)
    section=Sections.objects.filter(section_name=section_name,well=well_id,well_phase_id=wellphase_id,status=1)
    pressure=Pressureloss_data.objects.filter(well_id=well_id,section_name=section_name,well_phase_id=wellphase_id).first()
    total_surface=0
    total_annular=0
    total_drillstring=0
    total_bit=0
    annular_pressure=[]
    print('sensitivity_report',pressure.all_data['data']['surfacelosses'])
    for surface in pressure.all_data['data']['surfacelosses']:
       total_surface+=round(surface['pressureloss'])
    for annular in pressure.all_data['data']['annularpressureloss']:
        total_annular+=round(annular['pressureloss'])
        total_drillstring+=round(annular['drillstringloss'])
    for bit in pressure.all_data['data']['bitpressurelosses']:
        total_bit+=round(bit['bit_pressure_loss'])
    totalpressure_loss=total_surface+total_annular+total_drillstring+total_bit






















        
    





    




