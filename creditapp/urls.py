# creditapp/urls.py
from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

# Apis
# /regster - Add a new customer
# /check-eligibility - Check loan eligibility based on credit score of customer
# /create-loan - Process a new loan based on eligibility.
# /view-loan/loan_id - View loan details and customer details
# /view-loans/customer_id - View all current loan details by customer id

router = DefaultRouter()

router.register('customer', views.CustomerView)

urlpatterns = [
  path('', views.index, name='index'),
  path('register', views.register_customer, name='register_customer'),
  path('create-loan', views.create_loan, name='create-loan'),
  path('check-eligibility', views.check_eligibility_api, name='check_eligibility'),
  path('view-loan/<int:loan_id>', views.view_loan, name='view_loan'),
  path('view-loans/<int:customer_id>', views.view_loans, name='view_loans'),
  *router.urls
]
