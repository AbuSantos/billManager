from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from . forms import SignUpForm
from .models import Bills
from .forms import BillForm  # Create a BillForm
from .task import send_bill_reminders 
from datetime import timedelta, datetime 
from django.utils import timezone 
from django.core import serializers

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

def add_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill_instance = form.save()

            # Calculate the reminder date (e.g., one day before the due date)
            reminder_date = bill_instance.bill_due_date - timezone.timedelta(days=1)

            # Serialize the bill_instance to a dictionary
            bill_dict = serializers.serialize('python', [bill_instance])[0]['fields']

            # Trigger the reminder task with the serialized bill_dict and reminder_date
            send_bill_reminders.apply_async(args=[bill_instance.id, reminder_date])
            messages.success(request, "Bill added successfully registered!")
            return redirect('home')  
    else:
        form = BillForm()

    return render(request, 'add_bill.html', {'form': form})



def edit_bill(request, bill_id):
    bill = get_object_or_404(Bills, pk=bill_id)
    
    if request.method == 'POST':
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            # Redirect to the home page
            messages.success(request, "Successfully updated")
            return redirect('home')  
    else:
        form = BillForm(instance=bill)
    return render(request, 'edit_bill.html', {'form': form, 'bill': bill})

def delete_bill(request, bill_id):
    bill = get_object_or_404(Bills, pk=bill_id)

    if request.method == 'POST':
        bill.delete()
        messages.success(request, "Successfully deleted")
        return redirect('home') 
    
    return render(request, 'confirm_delete_bill.html', {'bill': bill})

def search_bills(request):
    search_query = request.GET.get('q')

    if search_query:
        bills = Bills.objects.filter(bill_name__icontains=search_query)
    else:
        bills = Bills.objects.all()

    return render(request, 'search_bills.html', {
        'bills': bills,
        'search_query': search_query,
    })