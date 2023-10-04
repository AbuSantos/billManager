from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from . forms import SignUpForm
from .models import Bills
# Create your views here.




def home(request):

    bills = Bills.objects.all()




    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #authenticate
        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You've been logged in!")
            return redirect ('home')
        else:
            messages.success(request, "There was an error loggin in, please try again...")
            return redirect ('home')
    else:
        return render(request, 'home.html',{"bills":bills})


# def login_user(request):
#     pass

def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out!")
    return redirect ('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You've successfully registered!")
            return redirect('home')
    else:
        form= SignUpForm()
        return render(request, 'register.html',{'form':form})
    return render(request, 'register.html',{'form':form})

