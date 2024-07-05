from django.shortcuts import render
from helpers.allmodels import Userlog,User,WellUsers,Wells,ProjectUsers,Projects
from helpers import dateformat,getuserlogsource
from helpers.commonimport import JsonResponse,datetime 
from django.core.paginator import Paginator
from django.core.serializers import serialize 
from django.template.loader import render_to_string
# Create your views here.
def user_list(request): 
    request.session['mainmenu'] = "userlog"
    if(request.user.licence_type == 'Individual'):
        projects = Projects.objects.getindividual_projects(request.user.id)
    else:
        projects = Projects.objects.getcompanies_projects(request.company.id)
    paginator = Paginator(projects,5) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'user_list.html',{'page_obj':page_obj}) 

def search_view(request):
    print('search_view_SS')
    search_value = request.GET.get('search_value', '')
    print('search_value',search_value)
    results = Projects.objects.filter(company_id=request.company.id) 
    print('results_search_view_s',results)
    results = Projects.objects.filter(company_id=request.company.id,project_name__icontains=search_value) 
    print('results_search_view_s',results)
    paginator = Paginator(results,5) 
    page_number = request.GET.get('pageNum')
    print('page_number',page_number)
    page_obj = paginator.get_page(page_number) 
    for page in page_obj:
        print('page_DATA',page)
    html = render_to_string('search-results.html',{'page_obj':page_obj,'search_value':search_value},request)
    return JsonResponse({'status':True,'html':html})
    
    


def proj_list(request):
    return render(request,'proj_list.html')

def well_list(request,proj_id):
    wells = Wells.objects.filter(company_id=request.company.id,project_id=proj_id)
    return render(request,'well_list.html',{'wells':wells})


def well_list_users(request,well_id):
    well_users = WellUsers.objects.filter(well_id=well_id,status=1)
    return render(request,'well_list_users.html',{'well_users':well_users})

def proj_list_users(request,proj_id):
    proj_users = ProjectUsers.objects.filter(project_id=proj_id,status=1)
    
    return render(request,'proj_list_users.html',{'proj_users':proj_users})

def getuserlog(request):
    activity = request.GET.get('activity')
    well_id = request.GET.get('well_id')
    user_id = request.GET.get('user_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if(start_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
    if(end_date):
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
   
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '') 
    if activity == "well":
        filtered_userlog = Userlog.objects.getwell_logs(well_id,user_id,start,length,start_date,end_date,search_value)
        total_records = Userlog.objects.getallwell_logs(well_id,user_id,start_date,end_date,search_value).count()
    elif activity == "project":
        filtered_userlog = Userlog.objects.getproj_logs(well_id,start,length,start_date,end_date,search_value,user_id)
        total_records = Userlog.objects.getallproj_logs(well_id,start_date,end_date,search_value,user_id).count()
        
    data = []
    for userlog in filtered_userlog:
        user=User.objects.getuserid(userlog.user_id)
        data.append({
            'id': userlog.id,
            'message': userlog.message,
            'user_name':user.name +" "+user.lastname,
            'time':dateformat(userlog.time),
            'name':getuserlogsource(userlog)
        })

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)