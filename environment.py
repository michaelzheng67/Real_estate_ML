
# Generic imports
from copy import deepcopy

# Modular imports
from simulation import Simulation, Property, mortgage_financials, decision, update_properties
from taxes import Taxes


# Probably want to make this a class to allow for multiple agents to run concurrent

class Environment:
    def __init__(self):
        self.owned_properties = []

        self.post_tax_money = 100_000
        self.pre_tax_money = 0
        self.saved_monthly_income = 5_000  # placeholder
        self.annual_net_income = 0

        self.Sim = Simulation()
        self.personal_finances = Taxes(100_000, 0.02, 0.3)

    def update_environment(self, months):
        # ---Updates Variables ---
        update_properties(self.owned_properties)
        temporary_list = deepcopy(self.owned_properties)

        available_property = self.Sim.new_properties()

        self.pre_tax_money += self.saved_monthly_income
        self.annual_net_income += self.saved_monthly_income

        self.interest_rate = self.Sim.interest_rate[months]
        self.stock_appreciation = self.Sim.cash_appreciation[months]
        self.inflation_rate = self.Sim.cash_appreciation[months]


        n_dels = 0

        # Taxes
        if (months + 1) % 12 == 0:
            self.personal_finances.update_taxes(self.annual_net_income, 0.015, 0.3)
            print(self.annual_net_income)
            print(self.personal_finances.tfsa)
            print(self.personal_finances.rrsp)
            print(self.personal_finances.investing_account)
            print(self.personal_finances.cash_account)
            #self.post_tax_money = self.personal_finances.tfsa + self.personal_finances.rrsp + self.personal_finances.investing_account + self.personal_finances.cash_account
            self.annual_net_income = 0

        # Prints Global Simulation Attributes for User
        print("Month:", months + 1, "Interest Rate: {0:.2f}%".format(self.interest_rate * 100),
              "Cash: ${0:,.2f}".format(self.post_tax_money))

        # Properties Owned
        for i in range(len(temporary_list)):
            capital_gains = 0
            self.annual_net_income = self.annual_net_income + temporary_list[i].cash_flow + temporary_list[
                i].monthly_principal_payments
            self.pre_tax_money += temporary_list[i].cash_flow
            print(
                "Property: {0} | Price: ${1:,.2f} | Mortgage Payment: ${2:,.2f} | Principal Payment: ${3:,.2f} | Interest Payment: ${4:,.2f} | Loan Outstanding ${5:,.2f}".format(
                    i + 1,
                    temporary_list[i].price, temporary_list[i].total_monthly_payments,
                    temporary_list[i].monthly_principal_payments, temporary_list[i].monthly_interest_payments,
                    temporary_list[i].loan_outstanding))
            self.post_tax_money, n_dels, self.capital_gains = decision(temporary_list[i], self.personal_finances.tfsa, self.personal_finances.rrsp, self.personal_finances.investing_account, self.personal_finances.cash_account, self.interest_rate,
                                                                       self.owned_properties, i, n_dels)

            self.post_tax_money -= self.capital_gains
            self.pre_tax_money += self.capital_gains

            self.annual_net_income += capital_gains * 0.5

        # Properties to Buy
        for i in range(3):
            print(
                "Purchase Price: {0:0.2f}, Rental Yield: {1:0.2f}%, Expenses Rate: {2:0.2f}%, Appreciation Rate: {3:0.4f}% ".format(
                    available_property[i].purchase_price, available_property[i].rent_yield * 100,
                                                          available_property[i].expenses_rate * 100, available_property[i].appreciation_rate * 100 * 12))
            self.post_tax_money, n_dels, self.capital_gains = decision(available_property[i], self.personal_finances.tfsa, self.personal_finances.rrsp, self.personal_finances.investing_account, self.personal_finances.cash_account, self.interest_rate,
                                                                       self.owned_properties, i, n_dels)

