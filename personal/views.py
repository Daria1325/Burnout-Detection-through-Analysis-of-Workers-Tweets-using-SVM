from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import date as dt
from dateutil.relativedelta import relativedelta

from .forms import ScanFrom
from analizer import main as analizer
from personal.models import Employee, State, Result




def getLastResults():
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
    
    res = getLastResults()
    context = {'form':form,
                'all_results': res}  
    return render(request, 'personal/home.html',context)
    
def grouped_screen_view(request):
    if request.method == 'POST':
        form = ScanFrom(request.POST)
        if form.is_valid():
            date = request.POST['date']
            position = request.POST['position']

            analizer.run_anilizer(date)

            return redirect('/grouped')
    else:
        form = ScanFrom()
    
    res = getLastResults()
    context = {'form':form,
                'all_results': res}  
    return render(request, 'personal/grouped.html',context)
# date position ( date of start - today) status

def getStatistic(start_date, end_date, group, chart):
    # if date
    {
        'date':'',
        'count_L':'',
        'count_M':'',
        'count_H':'',
        'count_N':''
    }

    #if position
    {
        'position':'',
        'count_L':'',
        'count_M':'',
        'count_H':'',
        'count_N':''
    }
    #if time
    {
        'time':'',
        'count_L':'',
        'count_M':'',
        'count_H':'',
        'count_N':''
    }

def pairDateAndValue(dates, values):
    result = []
    if len(values)==0:
        result = [0]* len(dates)
        return result
    for i, date in enumerate(dates):
        for value in values:
            if date == value['scan_date']:
                result.append(value['status__count'])
        if i+1 != len(result):
            result.append(0)
    return result
        


def getStatistic(start_date, end_date, group, chart):
    if group == 'Date':
        if chart == 'Line' or chart == 'Column' or chart == 'Stucked':
            dates = list(set(Result.objects.filter(scan_date__gte=start_date).filter(scan_date__lte=end_date).order_by('scan_date').values_list('scan_date', flat=True)))
            count_L = list(Result.objects.filter(scan_date__gte=start_date).filter(scan_date__lte=end_date).filter(status='L').order_by('scan_date').values('scan_date').annotate(Count('status')))
            count_M = list(Result.objects.filter(scan_date__gte=start_date).filter(scan_date__lte=end_date).filter(status='M').order_by('scan_date').values('scan_date').annotate(Count('status')))
            count_H = list(Result.objects.filter(scan_date__gte=start_date).filter(scan_date__lte=end_date).filter(status='H').order_by('scan_date').values('scan_date').annotate(Count('status')))
            count_N = list(Result.objects.filter(scan_date__gte=start_date).filter(scan_date__lte=end_date).filter(status='N').order_by('scan_date').values('scan_date').annotate(Count('status')))
            count_L= pairDateAndValue(dates,count_L)
            count_H=pairDateAndValue(dates,count_H)
            count_N =pairDateAndValue(dates,count_N)
            count_M=pairDateAndValue(dates,count_M)

            for i, date in enumerate(dates):
                dates[i] = date.strftime("%Y/%m/%d")
            return {
                'start_date': start_date,
                'end_date': end_date,
                'chart': chart,
                'group': group,
                'labels':dates,
                'L':count_L,
                'H':count_H,
                'N':count_N,
                'M':count_M,
            }
        if chart =='Pie':
            count_L = Result.objects.filter(scan_date__gte=start_date).filter(scan_date__lte=end_date).filter(status='L').count()
            count_M = Result.objects.filter(scan_date__gte=start_date).filter(scan_date__lte=end_date).filter(status='M').count()
            count_H = Result.objects.filter(scan_date__gte=start_date).filter(scan_date__lte=end_date).filter(status='H').count()
            count_N = Result.objects.filter(scan_date__gte=start_date).filter(scan_date__lte=end_date).filter(status='N').count()
            return {
                'start_date': start_date,
                'end_date': end_date,
                'chart': chart,
                'group': group,
                'labels':['Low','Moderate','High','No data'],
                'count':[count_L,count_M,count_H,count_N],
                'backgroundColor':['#25BE4B','#FFA550','#BE253A','#282E30']
            }
    




def statistic_screen_view(request, start_date=None, end_date=None,group=None, chart=None):
    if request.method == 'POST':
        form = ScanFrom(request.POST)
        if form.is_valid():
            date = request.POST['date']
            position = request.POST['position']

            analizer.run_anilizer(date)

            return redirect('/statistic')
    else:
        form = ScanFrom()

    if request.path=='/statistic/':
        end_date = dt.today().strftime("%Y-%m-%d")
        start_date = (dt.today() + relativedelta(months=-6)).strftime("%Y-%m-%d")
        res = getStatistic(start_date,end_date,'Date','Line')
    else:
        res = getStatistic(start_date,end_date,group,chart)
    context = {'form':form,
                'results': res}  
    return render(request, 'personal/statistic.html',context)

