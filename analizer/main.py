from analizer.analizer import analize_tweets 
from personal.models import Username, State
from datetime import datetime


def run_anilizer(date):
    employees = Username.objects.all().values()
    date = datetime.strptime(date, "%Y-%m-%d").date()
    
    analize_tweets([employees[0]],date)

