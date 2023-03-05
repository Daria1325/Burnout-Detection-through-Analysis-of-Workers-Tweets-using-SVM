from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ScanFrom
from analizer import main as analizer
from personal.models import Employee, State






def getAllResultsForAMonth():
    results =[]
    employees = Employee.objects.all().values()
    for employee in employees:
        if employee['state_id_id'] is None:
            results.append({'id': employee['employee_id'],
                        'name':employee['name'],
                        'state': 'N',
                        'note':'No data'})
        else:
            state = State.objects.filter(state_id=employee['state_id_id']).values()[0]
            results.append({'id': employee['employee_id'],
                             'name':employee['name'],
                            'state':state['status'],
                            'progress': state['progress'],
                            'note':state['note']})
    return results




@login_required(login_url='login/')
def home_screen_view(request):
    if request.method == 'POST':
        form = ScanFrom(request.POST)
        if form.is_valid():
            date = request.POST['date']
            position = request.POST['position']

            analizer.run_anilizer(date)

            return redirect('/')
    else:
        form = ScanFrom()
    
    res = getAllResultsForAMonth()

    context = {'form':form,
               'all_results': res}  

    return render(request, 'personal/home.html',context)
