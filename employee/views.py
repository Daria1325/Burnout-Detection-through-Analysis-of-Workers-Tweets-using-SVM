from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

from personal.models import Employee, Result, State
# Create your views here.

def get_employee_info(id):
    employee = Employee.objects.get(pk=id)
    status = Employee.objects.filter(pk=id).values_list('state_id__status', flat=True)[0]
    if status:
        last_result = list(Result.objects.filter(employee_id=employee).order_by('-scan_date').values())[0]
        results = list(Result.objects.filter(employee_id=employee).order_by('scan_date').values())
        for result in results:
            result['scan_date'] = result['scan_date'].strftime("%Y/%m/%d")
    else:
        last_result=None
        results=[]


    if last_result:
        last_result = {'status': status,
                    'count': last_result['count_N']+last_result['count_S']+last_result['count_L'],
                    'percent_N': last_result['percent_N'],
                    'percent_S': last_result['percent_S'],
                    'percent_L': last_result['percent_L']}
    else:
        last_result = {'status': 'N',
                        'count': 0,
                        'percent_N': 0,
                        'percent_S': 0,
                        'percent_L': 0
        }
    ctx = {'employee' : employee,
            'last_results' : last_result,
            'results' : results}  

    return ctx

    


@login_required(login_url='login/')
def profile_screen_view(request,id):
    context = get_employee_info(id) 

    return render(request, 'profile/profile.html',context)