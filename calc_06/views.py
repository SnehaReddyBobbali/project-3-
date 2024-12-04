from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

# User registration view
def registerPage(request): 
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.success(request, "Password does not follow the rules.")
    context = {'form': form}
    return render(request, 'register.html', context)

# Home page view for logged-in users
@login_required(login_url='login') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def home(request): 
    print("Home view is being rendered")  # Debugging line to check if the view is being hit
    context = {'name': 'sneha'}  # Sending 'name' to the template
    return render(request, 'home.html', context)

# User login page
def loginPage(request):
    if request.user.is_authenticated: 
        return redirect('home') 
    else:
        if request.method == 'POST': 
            username = request.POST.get('username') 
            password = request.POST.get('password') 
            print(username, password)  # Debugging login inputs
            user = authenticate(request, username=username, password=password) 
            if user is not None: 
                login(request, user) 
                return redirect('home') 
            else: 
                messages.success(request, "Username or Password is incorrect") 
    context = {} 
    return render(request, 'login.html', context) 

# User logout page
@login_required(login_url='login') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def logoutPage(request): 
    logout(request) 
    return redirect('login')