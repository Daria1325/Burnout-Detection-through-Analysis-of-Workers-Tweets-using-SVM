from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ScanFrom
from analizer import main as analizer

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
    context = {'form':form}
    
    

    return render(request, 'personal/home.html',context)
