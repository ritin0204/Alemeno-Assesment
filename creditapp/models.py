from django.db import models
from django.db.models import Max
import datetime

class AutoIncrement():
    def __init__(self, class_name) -> None:
        self.model_name = class_name
        
    def get_last_id(self):
        model = globals()[self.model_name]
        primary_key_field = model._meta.pk
        primary_key_name = primary_key_field.name
        max_value = model.objects.aggregate(Max(primary_key_name))[f"{primary_key_name}__max"]
        return max_value if max_value != None else 0


class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    approved_limit = models.DecimalField(max_digits=10, decimal_places=2)
    current_debt = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def save(self, *args, **kwargs) -> None:
        auto_increment = AutoIncrement(self.__class__.__name__)
        self.customer_id =  auto_increment.get_last_id()
        return super().save(*args, **kwargs)


class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_id = models.IntegerField(primary_key=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    def save(self, *args, **kwargs) -> None:
        auto_increment = AutoIncrement(self.__class__.__name__)
        self.loan_id =  auto_increment.get_last_id()
        self.emis_paid_on_time = 0
        if not self.end_date:
            self.end_date = self.start_date + datetime.timedelta(days=30 * self.tenure)
        return super().save(*args, **kwargs)
