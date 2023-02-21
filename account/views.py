from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import AccountAuthenticationForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):

     context = {}

     user = request.user
     if user.is_authenticated:
         return redirect("home")

     if request.POST:
         form = AccountAuthenticationForm(request.POST)
         if form.is_valid():
             email = request.POST['email']
             password = request.POST['password']
             user = authenticate(email=email, password=password)

             if user:
                 login(request, user)
                 return redirect("home")

     else:
         form = AccountAuthenticationForm()

     context['login_form'] = form
     return render(request, 'account/login.html', context)