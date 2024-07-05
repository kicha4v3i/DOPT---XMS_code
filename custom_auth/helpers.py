from custom_auth.models import Companies
import re
import secrets
import string

def generatecin(companyname):
    max_id = Companies.objects.values('id').order_by('-id').first()
    if(max_id):
        next_id=int(max_id['id'])
    else:
        next_id=1
    companyname=re.sub('[^A-Za-z0-9]+', '', companyname)
    companynameshort=companyname[:3].upper()
    max_id_str=str((next_id+1))
    max_id_str=max_id_str.zfill(3)
    return companynameshort+"-"+max_id_str

def generate_random_password(length=6):
    alphabet = string.ascii_letters
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def getcurrenturl(request):
    current_url=f'{request.scheme}://{request.get_host()}'
    return current_url

