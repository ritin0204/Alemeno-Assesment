from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Customer  # Replace with your model name


class CustomerTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        
    # Successful registration test
    def test_register_customer_success(self):
        test_data = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "monthly_salary": 150000,
            "phone_number": "1234567890",
        }
        response = self.client.post('/register',data=test_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("name", response.json())
        self.assertEqual(response.json()["approved_limit"], '5400000.00')
        # Optional: Check database
        customer = Customer.objects.get(pk=response.json()["customer_id"])
        self.assertEqual(customer.first_name + " " + customer.last_name, "John Doe")
        self.assertEqual(customer.monthly_salary, 150000)
        self.assertEqual(customer.approved_limit, 5400000)
        
        loan = {
            "customer_id": customer.customer_id,
            "loan_amount": 20000,
            "interest_rate": 12,
            "tenure": 20
        }
        self.client.post('/create-loan', data=loan)
        self.assertEqual(response.status_code, 201)
