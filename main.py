# This will be the area where code from all other files will be imported and utilized to test AI

# Generic imports
from copy import deepcopy

# Modular imports
from simulation import Simulation, Property, mortgage_financials, update_properties, decision
from taxes import Taxes


# Probably want to make this a class to allow for multiple agents to run concurrent

# __init__
owned_properties = []

post_tax_money = 100_000
pre_tax_money = 0
saved_monthly_income = 5_000 # placeholder
annual_net_income = 0


Sim = Simulation()
personal_finances = Taxes(100_000,0.02,0.3)

#def simulation, probably can remove loop later

for months in range(240):

    #---Updates Variables ---
    update_properties(owned_properties)
    temporary_list = deepcopy(owned_properties)

    available_property = Sim.new_properties()

    pre_tax_money += saved_monthly_income
    annual_net_income += saved_monthly_income

    interest_rate = Sim.interest_rate[months]
    stock_appreciation = Sim.cash_appreciation[months]
    inflation_rate = Sim.cash_appreciation[months]

    n_dels = 0

    # Taxes
    if (months+1) % 12 == 0:
        personal_finances.update_taxes(annual_net_income, 0.015, 0.3)
        print(annual_net_income)
        print(personal_finances.tfsa)
        print(personal_finances.rrsp)
        print(personal_finances.investing_account)
        print(personal_finances.cash_account)
        annual_net_income = 0



    # Prints Global Simulation Attributes for User
    print("Month:", months + 1, "Interest Rate: {0:.2f}%".format(interest_rate * 100),
          "Cash: ${0:,.2f}".format(post_tax_money))

    # Properties Owned
    for i in range(len(temporary_list)):
        capital_gains = 0
        annual_net_income = annual_net_income + temporary_list[i].cash_flow + temporary_list[i].monthly_principal_payments
        pre_tax_money += temporary_list[i].cash_flow
        print(
            "Property: {0} | Price: ${1:,.2f} | Mortgage Payment: ${2:,.2f} | Principal Payment: ${3:,.2f} | Interest Payment: ${4:,.2f} | Loan Outstanding ${5:,.2f}".format(
                i + 1,
                temporary_list[i].price, temporary_list[i].total_monthly_payments,
                temporary_list[i].monthly_principal_payments, temporary_list[i].monthly_interest_payments,
                temporary_list[i].loan_outstanding))
        post_tax_money, n_dels, capital_gains = decision(temporary_list[i], post_tax_money, interest_rate, owned_properties, i, n_dels)
        annual_net_income += capital_gains * 0.5

    # Properties to Buy
    for i in range(3):
        print("Purchase Price: {0:0.2f}, Rental Yield: {1:0.2f}%, Expenses Rate: {2:0.2f}%, Appreciation Rate: {3:0.4f}% ".format(available_property[i].purchase_price, available_property[i].rent_yield*100, available_property[i].expenses_rate*100, available_property[i].appreciation_rate*100*12))
        post_tax_money, n_dels, capital_gains = decision(available_property[i], post_tax_money, interest_rate, owned_properties, i, n_dels)













