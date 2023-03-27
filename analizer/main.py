from analizer.analizer import analize_tweets 
from personal.models import Username, State
from datetime import datetime


def run_anilizer(date,position):
    if position =="All":
        employees = Username.objects.all().values()
    else:
        employees = Username.objects.filter(employee_id__position=position).values()
    
    
    date = datetime.strptime(date, "%Y-%m-%d").date()
    
    

