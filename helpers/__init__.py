from math import pi,sqrt
import datetime
from projects.models import Projects,ProjectUsers
from wells.models import Wells,WellUsers
from wellphases.models import WellPhases


from custom_auth.models import User,Rights,Modules
from rig.models import Rig

#  flowrate conversion 
def convertflowrate(flowrate,unit):
    if(unit=='API'):
        return flowrate*0.000063
    else:
        return flowrate/3.7854*0.000063

#  casing hole size conversion 
def convertcasing_hole_size(casing_hole_size,unit):
    if(unit=='API'):
        return casing_hole_size/12/3.281
    else:
        return casing_hole_size/1000

#  od conversion 
def odconversion(od,unit):
    if(unit=='API'):
        return od/12/3.281
    else:
        return od/1000

#  mudweight conversion 
def mudweight_conversion(mudweight,unit):
    if(unit=='API'):
        return mudweight/8.33*1000
    else:
        return mudweight*1000

#  Length conversion 
def length_conversion(length,unit):
    if(unit=='API'):
        return length/3.281
    else:
        return length

#convert rpm
def rpm_convert(rpm):
    return rpm*2*pi/60

#  Ty conversion 
def ty_conversion(ty,unit):
    if(unit=='API'):
        return ty*1.066*0.4788
    else:
        return ty*1.066*0.4788

#  K conversion 
def k_conversion(k,m,unit):
    if(unit=='API'):
        return k*1.066*0.4788/(1.703**m)
    else:
        return k*1.066*0.4788/(1.703**m)

#  Pressureloss conversion 
def pressureloss_conversion(pressureloss,unit):
    if(unit=='API'):
        return pressureloss*0.000145038
    else:
        return pressureloss/1000

#  Yeildpoint conversion 
def yieldpoint_conversion(yield_point,unit):
    if(unit == 'API'):
        return yield_point
    else:
        return yield_point*0.4788

#  Plastic viscosity conversion 
def viscosity_conversion(plastic_viscosity,unit):
    if(unit == 'API'):
        return plastic_viscosity
    else:
        return plastic_viscosity/1000

#  ROP conversion 
def rop_conversion(rop,unit):
    if(unit == 'API'):
        return rop
    else:
        return rop*3.281

#  Cutting density conversion 
def cuttings_density_conversion(cuttings_density,unit):
    if(unit == 'API'):
        return cuttings_density
    else:
        return cuttings_density*8.33

#  Cutting Size conversion 
def cuttings_size_conversion(cuttings_size,unit):
    if(unit == 'API'):
        return cuttings_size
    else:
        return cuttings_size/1000*3.281*12

#  Box Pin conversion 
def convert_box_pin(length_of_tj,number_of_tj,unit):
    if(unit=='API'):
        return length_of_tj*number_of_tj/12
    else:
        return length_of_tj*number_of_tj/12/3.281

#  Slipvelocity conversion 
def slipvelocity_conversion(slip_velocity,unit):
    if(unit=='API'):
        return slip_velocity
    else:
        return slip_velocity/3.281

# Bit Pressure loss
def bit_loss_conversion(flowrate,mud_weight,tfa_value,cd_values,hole_size,unit):
    data=[]
    if unit =='API':
        bit_pressure_loss = mud_weight*flowrate**2/(12042*cd_values**2*tfa_value**2)
        bhhp = bit_pressure_loss*500/1714
        hsi = bhhp/(pi/4*hole_size**2)
        impact_forces = 0.01823*cd_values*flowrate*sqrt(mud_weight*bit_pressure_loss)
        jet_velocity = 0.32086*flowrate/tfa_value

        data.append({
            'bit_pressure_loss':bit_pressure_loss,
            'bhhp':bhhp,
            'hsi':hsi,
            'impact_forces':impact_forces,
            'jet_velocity':jet_velocity
        })
        return data
    else:
        bit_pressure_loss = (mud_weight*1000*(flowrate/3.7854*0.000063)**2/(2000*cd_values**2*(tfa_value/1000000)**2))
        bhhp = (flowrate/3.7854*bit_pressure_loss*0.145038)*0.435/1000
        hsi = bhhp/hole_size**2*1101.628
        impact_forces = 0.02353*cd_values*flowrate*sqrt(mud_weight*bit_pressure_loss)
        jet_velocity = 16.6428*flowrate/tfa_value

        data.append({
            'bit_pressure_loss':bit_pressure_loss,
            'bhhp':bhhp,
            'hsi':hsi,
            'impact_forces':impact_forces,
            'jet_velocity':jet_velocity
        })
        return data

def dateconversion(date):
    # date_time=datetime.datetime.combine(datetime.datetime.strptime(date, "%d-%m-%Y"), datetime.datetime.strptime(time,"%H:%M").time())
    timestamp = datetime.datetime.timestamp(datetime.datetime.strptime(date, "%d-%m-%Y"))
    return int(timestamp)

def dateconversion_welltrajectory(date):
    # date_time=datetime.datetime.combine(date,time)
    timestamp = datetime.datetime.timestamp(date)
    return int(timestamp)

def convertdateformat(date):
    converted_date=datetime.datetime.strptime(date, "%d-%m-%Y")
    converted_date=converted_date.strftime("%Y-%m-%d")
    return converted_date

def dateformat(date):
    converted_date=date.strftime("%d-%b-%Y %I.%M %p")
    return converted_date

# def input_access(userid,projectid,module,wellid,type):
#     print(userid,projectid,module,wellid,type)
#     permission=Userrights.objects.filter(user_id=userid,project_id=projectid,module_id=module,well_id=wellid,status=0).values(type).first()
#     if permission:
#         return permission[type]
#     else:
#         return ''


def user_rights_permission_projects(privilege,request,activity,activity_id):
    check_user_rights=user_rights_permission(privilege,request)
    
    if(check_user_rights):
        checkproject_well_access=check_useraccess(activity,activity_id,request)
        if(checkproject_well_access):
            return True
        else:
            return False
    else:
        return False

def user_rights_permission(privilege,request):
    user = User.objects.get(pk=request.user.id)
    group = user.groups.first()
    module = Modules.objects.filter(name=privilege).first()
    if module:
        module_id = module.id
    else:
        module_id=None
        
    check = Rights.objects.filter(company_id=request.user.company_id,module_id=module_id,role_id=group.id,status=1).exists()
    if group.name == "Admin":
        check = True
    return check


def check_useraccess(activity,activity_id,request):
    if request.user.individual_id:
        return True
    if activity == 'project':
        user_ids = ProjectUsers.objects.filter(project_id=activity_id,status=1).values_list('user_id', flat=True)
        print('check_useraccess',request.user.id,user_ids)
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



def poauser_rights_permission(privilege,request):
    user = User.objects.get(pk=request.user.id)
    module = Modules.objects.filter(name=privilege).first()
    check = Rights.objects.checkpoa_userrights(user.id,module.id).exists()
    if user.is_superadmin == 1:
        check = True
    return check

# def getuserlogsource(userlog):
#     source_id=userlog.source_id
#     source_type=userlog.source_Type 
#     well_id = userlog.well_id
#     wellphase_id = userlog.wellphase_id
#     well_datas = ['Well','Welltrajectory','Wellphases','Rig','SurfacePipe','Mud Pump','Pore and Fracture pressure']
#     well_phase_datas = ["Drillbit","Mud Data","BHA data","Rheogram"]

#     if(wellphase_id != None):
#         well_phase_details=WellPhases.objects.getwellphase_byid(wellphase_id)   
#     else:
#         well_phase_details = ""

#     if(source_type=='Project'):
#         project_details=Projects.objects.getproject_byid(source_id)
#         return project_details.project_name
#     elif(source_type in well_datas ):
#          well_details=Wells.objects.getwell_byid(well_id)
#          return well_details.name  
#     elif(source_type in well_phase_datas):
#         return well_phase_details.phase_name
#     elif(source_type=='User'):
#         user_details=User.objects.getuserid(source_id)
#         return user_details.name+" "+user_details.lastname                                                                 
#     else:
#         return ""
def getuserlogsource(userlog):
    try:
        source_id = userlog.source_id
        source_type = userlog.source_Type 
        well_id = userlog.well_id
        wellphase_id = userlog.wellphase_id
        well_datas = ['Well', 'Welltrajectory', 'Wellphases', 'Rig', 'SurfacePipe', 'Mud Pump', 'Pore and Fracture pressure']
        well_phase_datas = ["Drillbit", "Mud Data", "BHA data", "Rheogram"]

        if wellphase_id is not None:
            try:
                well_phase_details = WellPhases.objects.getwellphase_byid(wellphase_id)
            except WellPhases.DoesNotExist:
                well_phase_details = None
        else:
            well_phase_details = None

        if source_type == 'Project':
            try:
                project_details = Projects.objects.getproject_byid(source_id)
                return project_details.project_name
            except Projects.DoesNotExist:
                pass

        elif source_type in well_datas:
            try:
                well_details = Wells.objects.getwell_byid(well_id)
                print(well_details,"Well Details")
                return well_details.name
            except Wells.DoesNotExist:
                pass

        elif source_type in well_phase_datas:
            if well_phase_details:
                return well_phase_details.phase_name
        elif source_type == 'User':
            try:
                user_details = User.objects.getuserid(source_id)
                return user_details.name + " " + user_details.lastname
            except User.DoesNotExist:
                pass

        return ""
    except Exception as e:
        # Handle any other unexpected exceptions here
        print("An error occurred:", e)
        return ""
    
def getlogo():
    return "https://hydraulics.mo.vc/static/images/dopt_logo.png"


