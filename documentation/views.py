from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def documentation_view(request):

    return render(request, 'documentation/documentation.html')
