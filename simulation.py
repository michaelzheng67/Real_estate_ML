# imports
import numpy as np
import random

# Define a simulation environment


class Simulation:

    def __init__(self):
        self.interest_rate = self.__random_interest_rate()
        self.inflation = self.__random_inflation()
        self.cash_appreciation = self.__random_cash_appreciation()

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

    @ staticmethod
    def new_house_array():
        return [Property() for i in range(10)] # Returns list of 10 property objects

    # Private methods to generate random variables for environment

    @staticmethod
    def __random_interest_rate():
        return np.random.normal(2, 2)

    @staticmethod
    def __random_inflation():
        return np.random.normal(2, 1)

    @staticmethod
    def __random_cash_appreciation():
        return np.random.normal(8, 10)

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
        self.rent_yield = np.random.normal(5, 10)
        self.expenses_rate = abs(np.random.normal(1, 3)) # Might change
        self.appreciation_rate = np.random.normal(7, 10)

    # Assuming 30 Year Term Fixed Rate Mortgage for now, 20% down
        self.interest_rate = interest_rate + 0.01 # added 1% onto rate due to fixed rates being higher, number is placeholder
        self.down_payment = self.purchase_price * 0.2
        self.loan_outstanding = self.purchase_price - self.down_payment
        self.accrued_payments = 0
        self.term_length = 360

        self.total_monthly_payments, self.monthly_interest_payments, self.monthly_principal_payments = mortgage_financials(self.purchase_price, self.interest_rate, self.term_length, self.accrued_payments)

        # important variables later, used when iterations are running (we could add a time arg to Property Class and re-initilize every time to change variables. Might be weird and confusing to read)

        # self.monthly_cash_flow = self.rent_yield * self.purchase_price * (1-self.expenses_rate) - self.total_monthly_payments
        # self.accrued_equity = self.accrued_equity + self.accrued_payments + self.price - self.purchase_price



# Can be used for multiple applications, aside from initilizing property class
def mortgage_financials(purchase_price, down_payment, interest_rate, months, accrued_payments):
    original_loan = purchase_price - down_payment
    loan_outstanding = original_loan - accrued_payments
    monthly_interest_rate = interest_rate/12
    total_monthly_payments = original_loan * monthly_interest_rate * (1+monthly_interest_rate)**months/((1+monthly_interest_rate)**months-1)
    monthly_interest_payments = loan_outstanding * monthly_interest_rate
    monthly_principal_payments = total_monthly_payments - monthly_interest_payments

    return total_monthly_payments, monthly_interest_payments, monthly_principal_payments











