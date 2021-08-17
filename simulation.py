# imports
import numpy as np
import random

# Define a simulation environment


class Simulation:

    def __init__(self):
        self.interest_rate = self.__random_interest_rate()
        self.inflation = self.__random_inflation()
        self.cash_appreciation = self.__random_cash_appreciation()
        self.available_property = [Property() for i in range(3)]  # Returns list of 10 property objects

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
        return np.random.normal(.03, .01)

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
    def __init__(self):
        self.purchase_price = abs(np.random.normal(500000,200000))
        self.price = self.purchase_price
        self.rent_yield = np.random.normal(.075, .025)
        self.expenses_rate = abs(np.random.normal(.3, .1)) # Might change
        #self.appreciation_rate = np.random.normal(.02, .4)
        self.appreciation_rate = 0.025/12
        self.interest_rate = 1
        self.down_payment = 1
        self.loan_outstanding = 1
        self.term_length = 1
        self.status = 0 # 0 means can buy, 1 means owned
        self.cash_flow = 0

        self.total_monthly_payments, self.monthly_interest_payments, self.monthly_principal_payments = mortgage_financials(self.purchase_price, self.down_payment, self.interest_rate, self.term_length, self.loan_outstanding)

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
        # If mortgage isn't paid off
        if owned_property_array[i].loan_outstanding != 0:

            owned_property_array[i].total_monthly_payments, owned_property_array[i].monthly_interest_payments, owned_property_array[i].monthly_principal_payments = mortgage_financials(
                owned_property_array[i].purchase_price, owned_property_array[i].down_payment, owned_property_array[i].interest_rate,
                owned_property_array[i].term_length, owned_property_array[i].loan_outstanding)

            owned_property_array[i].loan_outstanding = owned_property_array[i].loan_outstanding - owned_property_array[
                i].monthly_principal_payments
        # Month after mortgage is paid off
        else:
            owned_property_array[i].total_monthly_payments = 0
            owned_property_array[i].monthly_principal_payments = 0
            owned_property_array[i].monthly_interest_payments = 0

        # Rounds small loan outstanding to 0, same month that mortgage finishes. Last month of term
        if owned_property_array[i].loan_outstanding < 10:
            owned_property_array[i].loan_outstanding = 0

        owned_property_array[i].cash_flow = owned_property_array[i].rent_yield/12 * owned_property_array[i].purchase_price*(1-owned_property_array[i].expenses_rate) - owned_property_array[i].total_monthly_payments


        #print("Property:", i+1, "Price:", owned_property_array[i].price, "Monthly Mortgage Payment", owned_property_array[i].total_monthly_payments,
              #owned_property_array[i].monthly_principal_payments, owned_property_array[i].monthly_interest_payments, owned_property_array[i].loan_outstanding)

        #print("Property: {0} | Price: ${1:,.2f} | Mortgage Payment: ${2:,.2f} | Principal Payment: ${3:,.2f} | Interest Payment: ${4:,.2f} | Loan Outstanding ${5:,.2f}".format(i+1,
            #owned_property_array[i].price, owned_property_array[i].total_monthly_payments,
            #owned_property_array[i].monthly_principal_payments, owned_property_array[i].monthly_interest_payments, owned_property_array[i].loan_outstanding))










