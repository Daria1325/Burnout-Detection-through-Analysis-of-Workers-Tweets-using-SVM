from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from personal.models import Employee, Result, State
# Create your views here.

def get_enployee_info(id):
    employee = Employee.objects.get(pk=id)
    last_results = Result.objects.filter(employee_id=employee).order_by('-scan_date').values()
    if last_results:
        state = State.objects.get(state_id=1)
        last_results = last_results[0]
        last_results = {'status': state.get_status_display(),
                    'count': last_results['count_N']+last_results['count_S']+last_results['count_L'],
                    'percent_N': last_results['percent_N'],
                    'percent_S': last_results['percent_S'],
                    'percent_L': last_results['percent_L']}
    else:
        last_results = {'status': 'N',
                        'count': 0,
                        'percent_N': 0,
                        'percent_S': 0,
                        'percent_L': 0
        }
    return employee, last_results

    


@login_required(login_url='login/')
def profile_screen_view(request,id):
    emp, res = get_enployee_info(id)
    context = {'employee' : emp,
               'last_results' : res}  

    return render(request, 'profile/profile.html',context)