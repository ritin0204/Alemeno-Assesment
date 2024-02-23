from .models import Customer, Loan
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class CustomerSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()
    approved_limit = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    customer_id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'customer_id',
            'name',
            'first_name',
            'last_name',
            'age',
            'monthly_salary',
            'phone_number',
            'approved_limit',
        ]

    def get_name(self, instance):
        return f"{instance.first_name} {instance.last_name}"

    
class LoanCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'age',
        ]

class LoanSerializer(ModelSerializer):
    customer = LoanCustomerSerializer()
    
    class Meta:
        model = Loan
        fields = [
            'loan_id',
            'customer',
            'loan_amount',
            'interest_rate',
            'monthly_repayment',
            'tenure',
        ]


class ListLoanSerializer(ModelSerializer):
    repayments_left = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Loan
        fields = [
            'loan_id',
            'loan_amount',
            'interest_rate',
            'monthly_repayment',
            'repayments_left',
        ]
        
    def get_repayments_left(self, loan_instance):
        tenure_months = loan_instance.tenure
        emis_paid = loan_instance.emis_paid_on_time
        
        remaining_emis = max(tenure_months - emis_paid, 0)
        
        return remaining_emis
