from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def home(request):
    return render(request,"form_app/index.html")

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exist!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            return redirect('register')

        if len(username)>10:
            messages.error(request,"Username must be under 10 characters")
            return redirect('register')

        if pass1 != pass2:
            messages.error(request,"Password didn't match!!")
            return redirect('register')

        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric!")
            return redirect('register')

        
        myuser = User.objects.create_user(username,email,pass1)

        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request,"Your Account has been successfully created.")
        return redirect('signin')

    return render(request,"form_app/register.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,"form_app/index.html",{'fname':fname})

        else:
            messages.error(request,"Bad Credentials!")
            return redirect('home')

    return render(request,"form_app/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect('home')