from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer, LoanSerializer, ListLoanSerializer
from .models import Customer, Loan
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ObjectDoesNotExist
from .calculate import check_eligibility
import datetime

# Create your views here.
def index(request):
    return HttpResponse("Hi there!")


@api_view(["GET"])
def view_loan(request, loan_id):
    """
    View loan details and customer details by loan id
    """
    try:
        loan = Loan.objects.get(pk=loan_id)
        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except BaseException as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def check_eligibility_api(request):
    customer_id = request.data['customer_id']
    loan_amount = request.data['loan_amount']
    interest_rate = request.data['interest_rate']
    tenure = request.data['tenure']
    customer = None
    try:
      customer = Customer.objects.get(pk=customer_id)
      if customer is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except ObjectDoesNotExist as e:
      return Response(status=status.HTTP_404_NOT_FOUND)
    
    eligibilty_status = check_eligibility(
      customer_id, loan_amount,interest_rate, tenure
    )
    
    return Response(eligibilty_status, status=status.HTTP_200_OK)


@api_view(["GET"])
def view_loans(request, customer_id):
    """
    View all current loan details by customer id
    """
    try:
        customer_id = Customer.objects.get(pk=customer_id)
        loans = Loan.objects.filter(customer=customer_id)
        serializer = ListLoanSerializer(loans, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except BaseException as e:
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def register_customer(request):
    """
    Add a new customer to the customer table with approved limit
    based on salary.
    """
    if request.method == "POST":
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                approved_limit=36 * serializer.validated_data["monthly_salary"]
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_loan(request):
  
  # Checking Eligibility Status
  customer_id = int(request.data['customer_id'])
  loan_amount = float(request.data['loan_amount'])
  interest_rate = float(request.data['interest_rate'])
  tenure = int(request.data['tenure'])
  customer = None
  try:
    customer = Customer.objects.get(pk=customer_id)
    if customer is None:
      return Response(status=status.HTTP_404_NOT_FOUND)
  except ObjectDoesNotExist as e:
    return Response(status=status.HTTP_404_NOT_FOUND)

  eligibilty_status = check_eligibility(
    customer_id, loan_amount,interest_rate, tenure
  )
  
  if eligibilty_status['approval']:
    loan = Loan.objects.create(
      customer=customer,
      loan_amount=loan_amount,
      tenure=eligibilty_status['tenure'],
      interest_rate=eligibilty_status['interest_rate'],
      monthly_repayment=eligibilty_status['monthly_repayment'],
      start_date=datetime.datetime.now(),
    )
    loan.save()
    return Response(status=status.HTTP_201_CREATED)
  return Response(eligibilty_status, status=status.HTTP_200_OK)


class CustomerView(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def perform_create(self, serializer):
        serializer.save(approved_limit=36 * serializer.validated_data["monthly_salary"])
