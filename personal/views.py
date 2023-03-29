from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import date as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random
import numpy as np

from .forms import ScanFrom
from analizer.analizer import analize_tweets
from personal.models import Employee, State, Result, Username

from django_celery_results.models import TaskResult




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
    context = {}
    if request.method == 'POST':
        form = ScanFrom(request.POST)
        if form.is_valid():
            date = request.POST['date']
            position = request.POST['position']
            if position =="All":
                employees = list(Username.objects.all().values())
            else:
                employees = list(Username.objects.filter(employee_id__position=position).values())

            task = analize_tweets.delay(employees,date)
            context['task_id']=task.task_id
            redirect('/')
    else:
        form = ScanFrom()
    res = getLastResults()
    if context == {}:
        tasks = TaskResult.objects.filter(status = "PROGRESS") | TaskResult.objects.filter(status = "STARTED")
        if len(tasks)!=0:
            context['task_id']=tasks[0].task_id

    context['form']=form
    context['all_results']= res  
    return render(request, 'personal/home.html',context)
    
def grouped_screen_view(request):
    context = {}
    if request.method == 'POST':
        form = ScanFrom(request.POST)
        if form.is_valid():
            date = request.POST['date']
            position = request.POST['position']

            if position =="All":
                employees = list(Username.objects.all().values())
            else:
                employees = list(Username.objects.filter(employee_id__position=position).values())

            
            task = analize_tweets.delay(employees,date)
            context['task_id']=task.task_id
    else:
        form = ScanFrom()
    
    if context == {}:
        tasks = TaskResult.objects.filter(status = "PROGRESS") | TaskResult.objects.filter(status = "STARTED")
        if len(tasks)!=0:
            context['task_id']=tasks[0].task_id

    res = getLastResults()
    context['form']=form
    context['all_results']= res
    return render(request, 'personal/grouped.html',context)

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
            dates= list(np.unique(np.array(Result.objects.filter(scan_date__gte=start_date).filter(scan_date__lte=end_date).order_by('scan_date').values_list('scan_date', flat=True))))

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
    if group == 'Position':
        if chart == 'Column' or chart == 'Stucked' or chart == 'Pie':
            query = Result.objects.filter(scan_date__range=[start_date, end_date]).values('status','employee_id__position')
            positions = list(set(query.values_list('employee_id__position', flat=True)))
            count_L = []
            count_H = []
            count_M = []
            count_N = []
            for position in positions:
                count_L.append(query.filter(status='L').filter(employee_id__position = position).count())
                count_H.append(query.filter(status='H').filter(employee_id__position = position).count())
                count_M.append(query.filter(status='M').filter(employee_id__position = position).count())
                count_N.append(query.filter(status='N').filter(employee_id__position = position).count())
            
            if chart =='Pie':
                colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(positions))]
                data = {"chart1":{
                    "labels": positions,
                    "count":count_L,
                    'backgroundColor':colors
                },
                "chart2":{
                    "labels": positions,
                    "count":count_M,
                    'backgroundColor':colors
                },
                "chart3":{
                    "labels": positions,
                    "count":count_H,
                    'backgroundColor':colors
                },
                "chart4":{
                    "labels": positions,
                    "count":count_N,
                    'backgroundColor':colors
                }}
                return{
                    'start_date': start_date,
                    'end_date': end_date,
                    'chart': chart,
                    'group': group,
                    'chartData':data
                }
            else:
                return {
                'start_date': start_date,
                'end_date': end_date,
                'chart': chart,
                'group': group,
                'labels':positions,
                'L':count_L,
                'H':count_H,
                'N':count_N,
                'M':count_M,
                }
        if chart == 'Line':
            query = Result.objects.filter(scan_date__range=[start_date, end_date]).order_by('scan_date').values('scan_date','status','employee_id__position')
            dates = list(set(query.values_list('scan_date', flat=True)))
            positions = list(set(query.values_list('employee_id__position', flat= True)))
            count_L = [[]]*len(positions)
            count_H = [[]]*len(positions)
            count_M = [[]]*len(positions)
            count_N = [[]]*len(positions)
            for i, position in enumerate(positions):
                count_L[i] = query.filter(employee_id__position = position).filter(status='L').values('scan_date').annotate(Count('status'))
                count_L[i]= pairDateAndValue(dates,count_L[i])
                count_M[i] = query.filter(employee_id__position = position).filter(status='M').values('scan_date').annotate(Count('status'))
                count_M[i]= pairDateAndValue(dates,count_M[i])
                count_H[i] = query.filter(employee_id__position = position).filter(status='H').values('scan_date').annotate(Count('status'))
                count_H[i]= pairDateAndValue(dates,count_H[i])
                count_N[i] = query.filter(employee_id__position = position).filter(status='N').values('scan_date').annotate(Count('status'))
                count_N[i]= pairDateAndValue(dates,count_N[i])
            for i, date in enumerate(dates):
                dates[i] = date.strftime("%Y/%m/%d")
            return {
                'start_date': start_date,
                'end_date': end_date,
                'chart': chart,
                'group': group,
                'labels':dates,
                'positions':positions,
                'L':count_L,
                'H':count_H,
                'N':count_N,
                'M':count_M,
            }
    if group == 'Time':
         if chart == 'Column' or chart == 'Stucked' or chart == 'Line' or chart == 'Pie':
            results = list(Result.objects.filter(scan_date__range=[start_date, end_date]).values('status','employee_id__join_date'))
            time = ['< 1 year', '1-2 years', '2-5 years', '> 5 years']
            count_L = [0]* len(time)
            count_H = [0]* len(time)
            count_M = [0]* len(time)
            count_N = [0]* len(time)
            today = dt.today()
            for result in results:
                difference_in_years = relativedelta(today, result['employee_id__join_date']).years
                index = 0
                if difference_in_years <1:
                    index=0
                elif difference_in_years <=2:
                    index = 1
                elif difference_in_years <=5:
                    index  = 2
                else:
                    index = 3

                if result['status'] == 'L':
                    count_L[index] +=1
                elif result['status'] == 'H':
                    count_H[index] +=1
                elif result['status'] == 'M':
                    count_M[index]+=1
                else:
                    count_N[index]+=1
            
            if chart =='Pie':
                colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(time))]
                data = {"chart1":{
                    "labels": time,
                    "count":count_L,
                    'backgroundColor':colors
                },
                "chart2":{
                    "labels": time,
                    "count":count_M,
                    'backgroundColor':colors
                },
                "chart3":{
                    "labels": time,
                    "count":count_H,
                    'backgroundColor':colors
                },
                "chart4":{
                    "labels": time,
                    "count":count_N,
                    'backgroundColor':colors
                }}
                return{
                    'start_date': start_date,
                    'end_date': end_date,
                    'chart': chart,
                    'group': group,
                    'chartData':data
                }
            else:       
                return {
                    'start_date': start_date,
                    'end_date': end_date,
                    'chart': chart,
                    'group': group,
                    'labels':time,
                    'L':count_L,
                    'H':count_H,
                    'N':count_N,
                    'M':count_M,
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

