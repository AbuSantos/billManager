from django.db import models

# Create your models here.
class SubCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Bills(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    bill_name = models.CharField(max_length=200)
    bill_due_date = models.DateField()
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.bill_name} ")