# This will be the area where code from all other files will be imported and utilized to test AI

# Generic imports


# Modular imports
from simulation import Simulation, Property, mortgage_financials, update_properties


owned_properties = []

cash = 0
saved_monthly_income = 5_000 # placeholder

for months in range(241):
    cash = cash + saved_monthly_income
    Sim = Simulation()
    print("Month:", months+1, "Interest Rate: {0:.2f}%".format(Sim.interest_rate*100), "Cash: ${0:,.2f}".format(cash))

    # Properties Owned
    for i in range(len(owned_properties)):
        cash = cash + owned_properties[i].cash_flow
        print(
            "Property: {0} | Price: ${1:,.2f} | Mortgage Payment: ${2:,.2f} | Principal Payment: ${3:,.2f} | Interest Payment: ${4:,.2f} | Loan Outstanding ${5:,.2f}".format(
                i + 1,
                owned_properties[i].price, owned_properties[i].total_monthly_payments,
                owned_properties[i].monthly_principal_payments, owned_properties[i].monthly_interest_payments,
                owned_properties[i].loan_outstanding))

    # Properties to Buy
    for i in range(3):
        print("Purchase Price: {0:0.2f}, Rental Yield: {1:0.2f}%, Expenses Rate: {2:0.2f}%, Appreciation Rate: {3:0.4f}% ".format(Sim.available_property[i].purchase_price, Sim.available_property[i].rent_yield*100, Sim.available_property[i].expenses_rate*100, Sim.available_property[i].appreciation_rate*100*12))

        print("""
        1. Mortgage, 20 year + 20% down payment
        2. Mortgage, 30 year + 20% down payment
        3. Buy Outright
        4. Sell
        5. Refinance
                    """)
        decision = input("Decision:")
        if decision == '1' and Sim.available_property[i].status == 0:
            Sim.available_property[i].interest_rate = Sim.interest_rate  # can add 1% onto rate due to fixed rates being higher, number is placeholder
            Sim.available_property[i].down_payment = Sim.available_property[i].purchase_price * 0.2
            Sim.available_property[i].loan_outstanding = Sim.available_property[i].purchase_price - Sim.available_property[i].down_payment
            Sim.available_property[i].term_length = 240

            owned_properties.append(Sim.available_property[i])

        elif decision == '2' and Sim.available_property[i].status == 0:
            Sim.available_property[i].interest_rate = Sim.interest_rate  # can add 1% onto rate due to fixed rates being higher, number is placeholder
            Sim.available_property[i].down_payment = Sim.available_property[i].purchase_price * 0.2
            Sim.available_property[i].loan_outstanding = Sim.available_property[i].purchase_price - Sim.available_property[i].down_payment
            Sim.available_property[i].term_length = 360

            owned_properties.append(Sim.available_property[i])
        elif decision == '3' and Sim.available_property[i].status == 0:
            Sim.available_property[i].interest_rate = Sim.interest_rate  # can add 1% onto rate due to fixed rates being higher, number is placeholder
            Sim.available_property[i].down_payment = Sim.available_property[i].purchase_price
            Sim.available_property[i].loan_outstanding = 0
            Sim.available_property[i].term_length = 360

            owned_properties.append(Sim.available_property[i])

        elif decision == '4' and Sim.available_property[i].status == 1:
            pass

        elif decision == '5' and Sim.available_property[i].status == 1:
            pass

        else:
            print("Invalid Choice")

    update_properties(owned_properties)












