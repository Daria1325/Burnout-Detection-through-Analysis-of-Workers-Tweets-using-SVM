from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def home_screen_view(request):
    context = {}

    
    
    context['accounts'] = ["HI"]

    return render(request, 'personal/home.html',context)