# Calculation will be done here
from .models import Loan, Customer


def check_eligibility(customer_id,  loan_amount, interest_rate, tenure):
    credit_score = calculate_credit_score(customer_id)
    sum_of_current_emis = calculate_sum_of_current_emis(customer_id)
    customer = Customer.objects.get(pk=customer_id)
    approval = True
    if sum_of_current_emis > 0.5 * float(customer.monthly_salary):
        approval = False
        return {
            "customer_id": customer_id,
            "approval": approval,
            "interest_rate": None,
            "corrected_interest_rate": None,
            "tenure": None,
            "monthly_installment": None,
        }

    if credit_score > 50:
        approval = True
    elif 30 < credit_score <= 50:
        if interest_rate <= 12:
            corrected_interest_rate = 12
    elif 10 < credit_score <= 30:
        if interest_rate <= 16:
            corrected_interest_rate = 16
    else:
        approval = False
        return {
            "customer_id": customer_id,
            "approval": approval,
            "interest_rate": None,
            "corrected_interest_rate": None,
            "tenure": None,
            "monthly_installment": None,
        }
    

    if corrected_interest_rate:
        interest_rate = corrected_interest_rate

    monthly_repayment = calculate_monthly_installment(
        loan_amount, interest_rate, tenure
    )
    

    return {
        "customer_id": customer_id,
        "approval": approval,
        "interest_rate": interest_rate,
        "corrected_interest_rate": corrected_interest_rate,
        "tenure": tenure,
        "monthly_repayment": monthly_repayment,
    }


def calculate_credit_score(customer_id):
    credit_score = 50
    # Implement logic to calculate credit score based on historical loan data
    # You can use the components mentioned in the requirements
    # For example:
    # - Calculate past loans paid on time
    # - Calculate number of loans taken in the past
    # - Calculate loan activity in the current year
    # - Calculate loan approved volume
    # - Calculate other relevant factors

    # Return the calculated credit score
    return credit_score


def calculate_monthly_installment(loan_amount, interest_rate, tenure):
    # Convert the interest rate to decimal format
    interest_rate_decimal = interest_rate / 100

    # Calculate the monthly interest rate
    monthly_interest_rate = interest_rate_decimal / 12

    # Calculate the compound interest factor
    compound_interest_factor = (1 + monthly_interest_rate) ** tenure

    # Calculate the numerator and denominator
    numerator = loan_amount * monthly_interest_rate * compound_interest_factor
    denominator = compound_interest_factor - 1

    # Calculate the EMI
    emi = numerator / denominator

    return round(float(emi), 3)


def calculate_sum_of_current_emis(customer_id):
    loans = Loan.objects.filter(customer=customer_id)
    res = 0
    for loan in loans:
        res += loan.monthly_repayment
    return float(res)
