from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import  auth,messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
#login
def login(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        if username and password:
            user = auth.authenticate(request, username=username, password=password)
            if user:
                auth.login(request,user)
                return redirect("dashboard")
            else:
                messages.error(request, "Incorrect Credentials")
                return render(request,"login.html",{"username" : username})
    return render(request, "login.html")

 #Register
def register(request):
    if request.method == "POST":
        email = request.POST.get("email", None)
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        # Check if a user with the provided email or username already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Username or email already exists"})
        
        user = User.objects.create_user(email=email, username=username, password=password)
        user.save()

        auth.login(request, user)
        return redirect("/")
    return render(request, "register.html")

# logout
def logout(request):
    auth.logout(request)
    return redirect("login")