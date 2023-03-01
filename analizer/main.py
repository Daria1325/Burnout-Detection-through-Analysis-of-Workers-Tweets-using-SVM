from analizer.analizer import analize_tweets 
from personal.models import Username, State


def run_anilizer(date):
    employees = Username.objects.all().values()
    
    analize_tweets(employees[0],date)

