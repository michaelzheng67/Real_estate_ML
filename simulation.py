# imports
import numpy as np
import random

# Define a simulation environment


class Simulation:

    def __init__(self):
        self.interest_rate = self.__random_interest_rate()
        self.inflation = self.__random_inflation()
        self.cash_appreciation = self.__random_cash_appreciation()
        self.available_property = [Property(0.025) for i in range(3)]  # Returns list of 10 property objects

    # Return new value methods
    def new_interest_rate(self):
        self.interest_rate = self.__random_interest_rate()
        return self.interest_rate

    def new_inflation(self):
        self.inflation = self.__random_inflation()
        return self.inflation

    def new_cash_appreciation(self):
        self.cash_appreciation = self.__random_cash_appreciation() - self.__black_swan()
        return self.cash_appreciation

    # Private methods to generate random variables for environment

    @staticmethod
    def __random_interest_rate():
        return np.random.normal(.02, .02)

    @staticmethod
    def __random_inflation():
        return np.random.normal(.02, .01)

    @staticmethod
    def __random_cash_appreciation():
        return np.random.normal(.08, .10)

    @staticmethod
    def __black_swan():
        if random.randint(1, 100) == 50:
            return np.random.normal(-15, 40)
        else:
            return 0


# Class to generate random real estate property
# Remember to incorporate inflation and interest rates to these properties
class Property:
    def __init__(self, interest_rate):
        self.purchase_price = abs(np.random.normal(700000,1000000))
        self.price = self.purchase_price
        self.rent_yield = np.random.normal(.05, .10)
        self.expenses_rate = abs(np.random.normal(.3, .1)) # Might change
        #self.appreciation_rate = np.random.normal(.02, .4)
        self.appreciation_rate = 0.025/12

    # Assuming 30 Year Term Fixed Rate Mortgage for now, 20% down
        self.interest_rate = interest_rate  # can add 1% onto rate due to fixed rates being higher, number is placeholder
        self.down_payment = self.purchase_price * 0.2
        self.loan_outstanding = self.purchase_price - self.down_payment
        self.term_length = 240
        self.total_monthly_payments, self.monthly_interest_payments, self.monthly_principal_payments = mortgage_financials(self.purchase_price, self.down_payment, self.interest_rate, self.term_length, self.loan_outstanding)

        # important variables later, used when iterations are running (we could add a time arg to Property Class and re-initilize every time to change variables. Might be weird and confusing to read)

        # self.monthly_cash_flow = self.rent_yield * self.purchase_price * (1-self.expenses_rate) - self.total_monthly_payments
        # self.accrued_equity = self.accrued_equity + self.accrued_payments + self.price - self.purchase_price



# Can be used for multiple applications, aside from initilizing property class
def mortgage_financials(purchase_price, down_payment, interest_rate, months, loan_outstanding):
    original_loan = purchase_price - down_payment
    monthly_interest_rate = interest_rate/12
    total_monthly_payments = original_loan * monthly_interest_rate * ((1+monthly_interest_rate)**months/((1+monthly_interest_rate)**months-1))
    monthly_interest_payments = loan_outstanding * monthly_interest_rate
    monthly_principal_payments = total_monthly_payments - monthly_interest_payments
    return total_monthly_payments, monthly_interest_payments, monthly_principal_payments


def update_properties(owned_property_array):

    for i in range(len(owned_property_array)):
        # Updates pricing
        owned_property_array[i].price = owned_property_array[i].price * (1 + owned_property_array[i].appreciation_rate)

        if owned_property_array[i].loan_outstanding != 0: # If mortgage isn't paid off
            owned_property_array[i].total_monthly_payments, owned_property_array[i].monthly_interest_payments, owned_property_array[i].monthly_principal_payments = mortgage_financials(
                owned_property_array[i].purchase_price, owned_property_array[i].down_payment, owned_property_array[i].interest_rate,
                owned_property_array[i].term_length, owned_property_array[i].loan_outstanding)

            owned_property_array[i].loan_outstanding = owned_property_array[i].loan_outstanding - owned_property_array[
                i].monthly_principal_payments
        else: # Month after mortgage is paid off
            owned_property_array[i].total_monthly_payments = 0
            owned_property_array[i].monthly_principal_payments = 0
            owned_property_array[i].monthly_interest_payments = 0

        if owned_property_array[i].loan_outstanding < 10: # Rounds super small loan outstanding to 0, same month that mortgage finishes. Last month of term
            owned_property_array[i].loan_outstanding = 0


        #print("Property:", i+1, "Price:", owned_property_array[i].price, "Monthly Mortgage Payment", owned_property_array[i].total_monthly_payments,
              #owned_property_array[i].monthly_principal_payments, owned_property_array[i].monthly_interest_payments, owned_property_array[i].loan_outstanding)

        print("Property: {0}, Price: ${1:0.2f}, Mortgage Payment: ${2:0.2f}, Principal Payment: ${3:0.2f}, Interest Payment: ${4:0.2f}, Loan Outstanding ${5:0.2f}".format(i+1,
            owned_property_array[i].price, owned_property_array[i].total_monthly_payments,
            owned_property_array[i].monthly_principal_payments, owned_property_array[i].monthly_interest_payments, owned_property_array[i].loan_outstanding))










