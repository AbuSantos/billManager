from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Bills
from .forms import BillForm  # Create a BillForm
from .task import send_bill_reminders 
from datetime import timedelta, datetime 
from django.utils import timezone 
from django.core import serializers
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import UserProfile, WalletTransaction
from django.core.exceptions import ObjectDoesNotExist
from .utils import generate_virtual_account_number
from decimal import Decimal
from .models import BillPayment
from .forms import BillPaymentForm 
from django.db.models import Q
from django.db.models import F  # Add this import



# @login_required
def home(request):
    if request.user.is_authenticated:
        # Retrieve bills associated with the logged-in user
        user_bills = Bills.objects.filter(Q(user=request.user) & Q(status='Unpaid'))

        if request.method == 'POST':
            # Mark bills as paid if their due date is in the past
            current_date = timezone.now().date()
            overdue_bills = user_bills.filter(Q(bill_due_date__lt=current_date) & Q(status='Unpaid'))
            overdue_bills.update(status='Paid')

            # Handle the form submission to mark bills as manually paid
            for bill in user_bills:
                manually_paid = request.POST.get(f"bill_{bill.id}")
                if manually_paid:
                    bill.manually_paid = True
                else:
                    bill.manually_paid = False
                bill.save()

        # Render the user's bills in the template
        return render(request, 'home.html', {'user_bills': user_bills})
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            # Authenticate
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You've been logged in!")
                return redirect('home')
            else:
                messages.error(request, "There was an error logging in, please try again...")

    return render(request, 'home.html')

@login_required
def dashboard(request):


    # return render(request, 'dashboard.html', context)
    upcoming_bills = Bills.objects.filter(user=request.user, bill_due_date__gt=timezone.now().date())

    # Fetch payment history (bill payments and wallet transactions)
    payment_history = list(BillPayment.objects.filter(user=request.user).order_by('-bill_due_date')) + \
                     list(WalletTransaction.objects.filter(user=request.user).order_by('-timestamp'))

    # Get user's wallet balance
    user_profile = UserProfile.objects.get(user=request.user)
    wallet_balance = user_profile.wallet_balance

    context = {
        'upcoming_bills': upcoming_bills,
        'payment_history': payment_history,
        'wallet_balance': wallet_balance,
    }

    return render(request, 'dashboard.html', context)


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
            user = form.save()

            # Create a UserProfile for the new user
            virtual_account_number = generate_virtual_account_number()
            user_profile = UserProfile.objects.create(user=user, virtual_account_number=virtual_account_number)  # Create the UserProfile
            user_profile.save()

            # Authenticate and log in the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, "You've successfully registered!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def add_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            # Create a new bill instance with the user field set to the currently authenticated user
            bill_instance = form.save(commit=False)
            bill_instance.user = request.user  # Set the user field
            bill_instance.save()

            # Calculating the reminder date (e.g., one day before the due date)
            reminder_date = bill_instance.bill_due_date - timezone.timedelta(days=1)

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
        #  Bills.objects.filter(user=request.user)
        bills = Bills.objects.filter(user=request.user)

    return render(request, 'search_bills.html', {
        'bills': bills,
        'search_query': search_query,
    })

def send_test_email(request):
    try:
        send_mail(
            'Test Email',
            'This is a test email message.',
            'abusomwansantos@gmail.com', 
            ['winozee@gmail.com'],  
            fail_silently=False,
        )
        return HttpResponse('Test email sent successfully!')
    except Exception as e:
        return HttpResponse(f'Error sending test email: {str(e)}')
    
@login_required
def wallet(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        wallet_transactions = WalletTransaction.objects.filter(user=request.user)
        context = {
            'user_profile': user_profile,
            'wallet_transactions': wallet_transactions,
        }

        for transaction in wallet_transactions:
            print(f"Transaction Timestamp: {transaction.timestamp}")

        return render(request, 'wallet.html', context)
    except ObjectDoesNotExist:
        # Handle the case where UserProfile or wallet transactions don't exist
        return redirect('home') 

@login_required
def deposit(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        account_number = user_profile.virtual_account_number
    except UserProfile.DoesNotExist:
        account_number = None

    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        if amount >= 100:
            if account_number:
                user_profile.wallet_balance += amount
                user_profile.save()
                WalletTransaction.objects.create(user=request.user, amount=amount, transaction_type='deposit')
                messages.success(request, f'You have successfully deposited ${amount} into your wallet.')
            else:
                messages.error(request, 'User profile not found. Please try again later.')
        else:
            messages.error(request, 'Amount should be greater than 100N')

    return render(request, 'deposit.html', {'account_number': account_number})


@login_required
def withdrawal(request):
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        user_profile = UserProfile.objects.get(user=request.user)
        if amount > 0 and user_profile.wallet_balance >= amount:
            user_profile.wallet_balance -= amount
            user_profile.save()
            WalletTransaction.objects.create(user=request.user, amount=amount, transaction_type='withdrawal')
    return redirect('wallet')




def bill_payments(request):
    user = request.user
    user_profile = user.userprofile  

    if request.method == 'POST':
        form = BillPaymentForm(request.POST)
        if form.is_valid():
            bill_payment = form.save(commit=False)
            bill_payment.user = user
            wallet_balance_before_payment = user_profile.wallet_balance

            if wallet_balance_before_payment >= bill_payment.bill_amount:
                bill_payment.wallet_balance_before_payment = wallet_balance_before_payment
                bill_payment.save()

                # Deducting the bill amount from the user's wallet balance
                user_profile.wallet_balance -= bill_payment.bill_amount
                user_profile.save()

                form = BillPaymentForm()  
                return redirect('bill_payments')
            else:
                messages.error(request, "Insufficient funds in your wallet.")
        else:
            messages.error(request, "Invalid form data. Please check the inputs.")

    else:
        form = BillPaymentForm()

    bill_payments = BillPayment.objects.filter(user=user)
    return render(request, 'bill_payments.html', {'bill_payments': bill_payments, 'form': form})
