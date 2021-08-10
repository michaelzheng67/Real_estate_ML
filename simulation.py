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
        self.cash_appreciation = self.__random_cash_appreciation() - self.__random_inflation() - self.__black_swan()
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
        return np.random.normal(2, 3)

    @staticmethod
    def __random_cash_appreciation():
        return np.random.normal(10, 20)

    @staticmethod
    def __black_swan():
        if random.randint(1, 100) == 50:
            return np.random.normal(-15, 40)
        else:
            return 0


# Class to generate random real estate property

class Property:
    def __init__(self):
        self.purchase_price = abs(np.random.normal(700000,1000000))
        self.rent_yield = np.random.normal(5, 10)
        self.expenses_rate = abs(np.random.normal(1, 3))
        self.appreciation_rate = np.random.normal(7, 10)

