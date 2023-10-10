from django.db import models
from django.contrib.auth.models import User

class SubCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Bills(models.Model):
    STATUS_CHOICES = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    )
     
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    bill_name = models.CharField(max_length=200)
    bill_due_date = models.DateField()
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unpaid')
    manually_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return (f"{self.bill_name} ")
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    virtual_account_number = models.CharField(max_length=16, unique=True, null=True, blank=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username

class WalletTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20)  # e.g., 'deposit', 'withdrawal', 'transfer'
    timestamp = models.DateTimeField(auto_now_add=True)

class BillPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill_name = models.CharField(max_length=200)
    bill_due_date = models.DateField()
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    wallet_balance_before_payment = models.DecimalField(max_digits=10, decimal_places=2)
    is_scheduled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bill_name} - {self.bill_due_date}"