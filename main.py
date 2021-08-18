# This will be the area where code from all other files will be imported and utilized to test AI

# Generic imports
from copy import deepcopy

# Modular imports
from simulation import Simulation, Property, mortgage_financials, update_properties, decision


# Probably want to make this a class to allow for multiple agents to run concurrent

owned_properties = []

cash = 100_000
saved_monthly_income = 5_000 # placeholder


for months in range(241):
    cash = cash + saved_monthly_income
    Sim = Simulation()
    temporary_list = deepcopy(owned_properties)
    n_dels = 0

    print("Month:", months + 1, "Interest Rate: {0:.2f}%".format(Sim.interest_rate * 100),
          "Cash: ${0:,.2f}".format(cash))
    # Properties Owned
    for i in range(len(temporary_list)):
        cash = cash + temporary_list[i].cash_flow
        print(
            "Property: {0} | Price: ${1:,.2f} | Mortgage Payment: ${2:,.2f} | Principal Payment: ${3:,.2f} | Interest Payment: ${4:,.2f} | Loan Outstanding ${5:,.2f}".format(
                i + 1,
                temporary_list[i].price, temporary_list[i].total_monthly_payments,
                temporary_list[i].monthly_principal_payments, temporary_list[i].monthly_interest_payments,
                temporary_list[i].loan_outstanding))
        cash, n_dels = decision(temporary_list[i], cash, Sim.interest_rate, owned_properties,i, n_dels)

    # Properties to Buy
    for i in range(3):
        print("Purchase Price: {0:0.2f}, Rental Yield: {1:0.2f}%, Expenses Rate: {2:0.2f}%, Appreciation Rate: {3:0.4f}% ".format(Sim.available_property[i].purchase_price, Sim.available_property[i].rent_yield*100, Sim.available_property[i].expenses_rate*100, Sim.available_property[i].appreciation_rate*100*12))
        cash, n_dels = decision(Sim.available_property[i],cash,Sim.interest_rate,owned_properties,i,n_dels)

    update_properties(owned_properties)












