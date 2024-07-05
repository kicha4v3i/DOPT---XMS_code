from django import template
from helpers.allmodels import ProjectBlock,ProjectField,MudType,WellPhases,MudData,Calculationchartdata,Rheogram,RheogramDate,RheogramSections
from helpers.commonimport import Image,base64,json,io
from pressureloss.views import getviscocity,base64image


register = template.Library()

@register.simple_tag 
def getblockdetails_bywell(block_id):
    block=ProjectBlock.objects.getblock_byid(block_id)
    return block

@register.simple_tag 
def getfielddetails_bywell(field_id):
    field=ProjectField.objects.getfield_byid(field_id)
    return field

@register.simple_tag 
def getmudtype_byid(mudtype_id):
    print(f"mudtype_id {mudtype_id}")
    mud_type=MudType.objects.getmudtype_byid(mudtype_id)
    return mud_type

@register.simple_tag 
def getpressureloss_percentage(totalpressureloss,pressureloss):
    return round(pressureloss/totalpressureloss*100)
  
@register.simple_tag 
def getroundvalue_withdecimal(value):
    return round(value,2)

@register.simple_tag 
def getroundvalue(value):
    return round(value)

@register.simple_tag 
def getallwellphases_bywellid(well_id):
    print(f"well_id {well_id}")
    print(f"WellPhases.objects.getallwellphases_bywellid(well_id) {WellPhases.objects.getallwellphases_bywellid(well_id)}")
    return WellPhases.objects.getallwellphases_bywellid(well_id)

@register.simple_tag 
def getmuddata_by_wellphase(wellphase_id):
    print(f"wellphase_id {wellphase_id}")
    print(f"MudData.objects.getallmuddata_bywellphase(wellphase_id) {MudData.objects.getallmuddata_bywellphase(wellphase_id)}")
    return MudData.objects.getallmuddata_bywellphase(wellphase_id)

@register.simple_tag 
def getinputdata_bywellphase(wellphase,section_name):
    print(f"section_name getinputdata_bywellphase {section_name}")
    input_data=Calculationchartdata.objects.get_calculation_inputdata(wellphase.well_id,wellphase.id,section_name)
    return json.loads(input_data.input_data)

@register.simple_tag 
def getrheogram_data_bywellphase(wellphase_id,muddata_id,section_name):
    rheogram_sections=RheogramSections.objects.getrheogramsections(section_name,wellphase_id)

    try:
        rehogram_details=RheogramDate.objects.getrheogramdate_byid(rheogram_sections.rheogram_date_id)
    except RheogramDate.DoesNotExist:
        return None


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
    return rheogram_datas

@register.simple_tag 
def getrheogram_chart_bywellphase(wellphase_id,section_name):
    image_name='rheogramchart-'+str(wellphase_id)+'-'+section_name+'.png'
    return getbase64image(image_name,'rheogramchart')

@register.simple_tag 
def getecdalongwell_chart_bywellphase(wellphase_id,section_name):
    image_name='ecdalonghole-'+str(wellphase_id)+'-'+section_name+'.png'
    return getbase64image(image_name,'ecdalongwell')


@register.simple_tag 
def getecdbitdepth_chart_bywellphase(wellphase_id,section_name):
    image_name='ecdbitdepth-'+str(wellphase_id)+'-'+section_name+'.png'
    return getbase64image(image_name,'ecdbitdepth')
   
@register.simple_tag 
def getpressureloss_chart_bywellphase(wellphase_id,section_name):
    image_name='pressure_chart-'+str(wellphase_id)+'-'+section_name+'.png'
    return getbase64image(image_name,'pressureloss')

@register.simple_tag 
def getmudweight_sensitivity_chart(wellphase_id,section_name):
    mudweight_pressure='mudweight_pressure-'+str(wellphase_id)+'-'+section_name+'.png'
    mudweight_ecd='mudweight_ecd-'+str(wellphase_id)+'-'+section_name+'.png'
    data={
        'mudweight_pressure': getbase64image(mudweight_pressure,'sensitivity_chart'),
        'mudweight_ecd': getbase64image(mudweight_ecd,'sensitivity_chart') 
    }
    return data

@register.simple_tag 
def getplasticviscocity_sensitivity_chart(wellphase_id,section_name):
    plastic_viscocity_pressure='viscocity_pressure_chart-'+str(wellphase_id)+'-'+section_name+'.png'
    plastic_viscocity_ecd='viscocity_ecd_chart-'+str(wellphase_id)+'-'+section_name+'.png'
    data={
        'plastic_viscocity_pressure': getbase64image(plastic_viscocity_pressure,'sensitivity_chart'),
        'plastic_viscocity_ecd': getbase64image(plastic_viscocity_ecd,'sensitivity_chart') 
    }
    return data


@register.simple_tag 
def getflowrate_sensitivity_chart(wellphase_id,section_name):
    flowrate_pressure_chart='flowrate_pressure_chart-'+str(wellphase_id)+'-'+section_name+'.png'
    flowrate_ecd_chart='viscocity_ecd_chart-'+str(wellphase_id)+'-'+section_name+'.png'
    data={
        'flowrate_pressure_chart': getbase64image(flowrate_pressure_chart,'sensitivity_chart'),
        'flowrate_ecd_chart': getbase64image(flowrate_ecd_chart,'sensitivity_chart') 
    }
    return data

@register.simple_tag 
def gettfa_sensitivity_chart(wellphase_id,section_name):
    tfa_pressure='tfa_pressure-'+str(wellphase_id)+'-'+section_name+'.png'
    return getbase64image(tfa_pressure,'pressureloss')

@register.simple_tag 
def getyieldpoint_sensitivity_chart(wellphase_id,section_name):
    yieldpoint_pressure='yieldpoint_pressure-'+str(wellphase_id)+'-'+section_name+'.png'
    return getbase64image(yieldpoint_pressure,'pressureloss')

@register.simple_tag 
def getcs_sensitivity_chart(wellphase_id,section_name):
    cuttings_size_ecd='cuttings_size_ecd-'+str(wellphase_id)+'-'+section_name+'.png'
    return getbase64image(cuttings_size_ecd,'pressureloss')

@register.simple_tag 
def getcd_sensitivity_chart(wellphase_id,section_name):
    cuttings_density_ecd='cuttings_density_ecd-'+str(wellphase_id)+'-'+section_name+'.png'
    return getbase64image(cuttings_density_ecd,'pressureloss')

@register.simple_tag 
def getrop_sensitivity_chart(wellphase_id,section_name):
    rop_ecd='rop_ecd-'+str(wellphase_id)+'-'+section_name+'.png'
    return getbase64image(rop_ecd,'pressureloss')

@register.simple_tag 
def getviscocity_details(muddata):
    return getviscocity(muddata)

@register.simple_tag 
def get_annular_drillingstringloss(well_id,wellphase_id,section_name):
   annular_drillingstringloss = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'annulardrillstringloss',section_name)
   return json.loads(annular_drillingstringloss.result)

@register.simple_tag 
def get_bitpressure_loss(well_id,wellphase_id,section_name):
    bitpressure_loss = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'bitpressureloss',section_name)
    data={
      'bitpressure_loss':json.loads(bitpressure_loss.result),
      'totalbitpressureloss':round(json.loads(bitpressure_loss.result)[0]['bit_pressure_loss'])  
    }
    return data


@register.simple_tag 
def get_surfacepressure_loss(well_id,wellphase_id,section_name):
    surfacepressure_loss = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'surfacepressureloss',section_name)
    return json.loads(surfacepressure_loss.result)

@register.simple_tag 
def get_alongwellecd_data(well_id,wellphase_id,section_name):
    alongwellecd_data = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'alongwellecd_data',section_name)
    return alongwellecd_data

@register.simple_tag 
def get_bitdepthecd_data(well_id,wellphase_id,section_name):
    bitdepthecd_data = Calculationchartdata.objects.get_calculation_result(well_id,wellphase_id,'bitdepthecd_data',section_name)
    return bitdepthecd_data

@register.simple_tag 
def gettotalsurfaceloss(surfacelosses):
    totalsurfacelosses=0
    for surfaceloss in surfacelosses:
        totalsurfacelosses +=surfaceloss['pressureloss']
    return totalsurfacelosses

@register.simple_tag 
def gettotal_drillstring_annular_loss(annular_drillingstringloss):
    totaldrillstringlosses=0
    totalannularlosses=0

    for pressureloss in annular_drillingstringloss:
        totaldrillstringlosses +=pressureloss['drillstringloss']
        totalannularlosses +=pressureloss['pressureloss']
    pressurelossdata={
        'totaldrillstringlosses':totaldrillstringlosses,
        'totalannularlosses':totalannularlosses
    }
    return pressurelossdata

@register.simple_tag 
def gettotalpressureloss(totalannular_drillingstringloss,totalsurfaceloss,bitpressure_loss):
    totalpressureloss=totalsurfaceloss+bitpressure_loss['totalbitpressureloss']+totalannular_drillingstringloss['totaldrillstringlosses']+totalannular_drillingstringloss['totalannularlosses']
    return totalpressureloss

@register.simple_tag 
def checkcalculationdata_exist(wellphase_id,section_name):
    checkcalculationdata = Calculationchartdata.objects.get_allcalculationdata(wellphase_id,section_name)
    return checkcalculationdata

def getbase64image(image_name,chart_type):
    try:
        imagePath = ('media/'+image_name)
        image = Image.open(imagePath)
        if(chart_type=='rheogramchart'):
            desired_width = 400
            desired_height = 400
        elif(chart_type=='sensitivity_chart'):
            desired_width = 300
            desired_height = 350
        else:
            desired_width = 700
            desired_height = 500

        image = image.resize((desired_width, desired_height), Image.ANTIALIAS)
        image_buffer = io.BytesIO()
        image.save(image_buffer, format="PNG")
        encoded_image = base64.b64encode(image_buffer.getvalue()).decode("utf-8")
        return encoded_image
    except FileNotFoundError:
        return None


