from math import pi,sqrt
from bhadata.models import BhaData,BhaElement
from custom_auth.getunit import getprojectunit,adduserlog,converttofloat,getmodaltext,getcountries
from helpers.allmodels import User,CountryUsers

#  mudweight conversion
def calculate_mudweight(mudweight,unit):
    if(unit=='API'):
        return mudweight
    else:
        return mudweight*8.33

#  Plastic viscosity conversion
def calculate_PV(plastic_viscosity,unit):
    if(unit == 'API'):
        return plastic_viscosity
    else:
        return plastic_viscosity*1000

#  Yeildpoint conversion
def calculate_YP(yield_point,unit):
    if(unit == 'API'):
        return yield_point
    else:
        return yield_point/0.4788

# Flowrate conversion
def calculate_flowrate(flowrate,unit):
    if(unit=='API'):
        return flowrate
    else:
        return flowrate/3.78

# OD conversion
def calculate_od(od,unit):
    if(unit=='API'):
        return od
    else:
        return od/1000*3.281*12

# Cased hole size conversion
def calculate_holesize(cased_hole_size,unit):
    if(unit=='API'):
        return cased_hole_size
    else:
        return cased_hole_size/1000*3.281*12

# ROP conversion
def calculate_rop(rop,unit):
    if(unit=='API'):
        return rop
    else:
        return rop*3.281

# Cutting density
def calculate_cutting_density(cuttings_density,unit):
    if(unit=='API'):
        return cuttings_density
    else:
        return cuttings_density*8.33

# Cutting size
def calculate_cutting_size(cuttings_size,unit):
    if(unit=='API'):
        return cuttings_size
    else:
        return cuttings_size/1000*3.281*12

def calculate_Ty(ty,unit):
    if (unit == 'API'):
        return ty
    else:
        return ty/0.4788

def calculate_annular(av,unit):
    if(unit == 'API'):
        return av*3.281*60
    else:
        return av*60

def calcualte_ecd(mud_weight,pressure,tvd,unit):
    if(unit == 'API'):
        return mud_weight+pressure/(0.052*tvd)
    else:
        return mud_weight+pressure/(9.81*tvd)

def getassigneusers_tickets(country_id):
    allusers=[]
    getmainpoa=User.objects.getmainpoa()
    users=CountryUsers.objects.getcountry_allcountry_user(country_id)
    allusers.append({
        'id':getmainpoa.id,
        'name':getmainpoa.name,
        'lastname':getmainpoa.lastname,
        'email':getmainpoa.email,

    })
    for user in users:
        allusers.append({
            'id':user.userid.id,
            'name':user.userid.name,
            'lastname':user.userid.lastname,
            'email':user.userid.email,
        })
    allcountryusers=User.objects.getallcountryusers()
    for allcountryuser in allcountryusers:
        allusers.append({
            'id':allcountryuser.id,
            'name':allcountryuser.name,
            'lastname':allcountryuser.lastname,
            'email':allcountryuser.email,
        })
    return allusers

def getassigneusers_tickets_excludepoa(country_id):
    allusers=[]
    users=CountryUsers.objects.getcountry_allcountry_user(country_id)
    for user in users:
        allusers.append({
            'id':user.userid.id,
            'name':user.userid.name,
            'lastname':user.userid.lastname,
            'email':user.userid.email,
        })
    allcountryusers=User.objects.getallcountryusers()
    for allcountryuser in allcountryusers:
        allusers.append({
            'id':allcountryuser.id,
            'name':allcountryuser.name,
            'lastname':allcountryuser.lastname,
            'email':allcountryuser.email,
        })
    return allusers