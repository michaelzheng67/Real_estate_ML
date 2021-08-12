# This will be the area where code from all other files will be imported and utilized to test AI

# Generic imports


# Modular imports
from simulation import Simulation, Property, mortgage_financials, update_properties

Sim = Simulation()
owned_properties = Sim.available_property # Temporary placeholder, before decision making is implemented

for t in range (241):
    print("Month:", t+1)
    Sim = Simulation()
    update_properties(owned_properties)


    #print("Month:", t+1)
    #for i in range(3):
        #print("Purchase Price: {0:0.2f}, Rental Yield: {1:0.2f}%, Expenses Rate: {2:0.2f}%, Appreciation Rate: {3:0.2f}% ".format(Sim.available_property[i].purchase_price, Sim.available_property[i].rent_yield, Sim.available_property[i].expenses_rate, Sim.available_property[i].appreciation_rate))

