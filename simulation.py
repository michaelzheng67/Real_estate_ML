# imports
import numpy as np
import random

# Define a simulation environment


class Simulation:

    def __init__(self, interest_rate, inflation, cash_appreciation):
        self.interest_rate = self.__random_interest_rate()
        self.inflation = self.__random_inflation()
        self.cash_appreciation = self.__random_cash_appreciation() - self.__random_inflation() - self.__black_swan()

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


