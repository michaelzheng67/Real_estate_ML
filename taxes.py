
# Note: takes inflation in decimal form. Split variable used to determine split between cash account
# and investing account (e.g 0.2 means 20% cash, 80% investing)
# we should add saving ratio and subtract from remaining cash. can be pre-tax or post-tax

# Include assets growing in accounts
# Include capital gains member (Investing account)
# Make update investment accounts to update investment accounts monthly

class Taxes:
    def __init__(self, cash, inflation, split):

        # Initialize bracket amounts for federal and provincial taxes
        # Federal brackets
        self.fed_tax_free = 13000  # below this amount is tax free
        self.fed_first_divider = 49020
        self.fed_second_divider = 98040
        self.fed_third_divider = 151978
        self.fed_fourth_divider = 216511

        # Provincial brackets
        self.prov_first_divider = 45142
        self.prov_second_divider = 90287
        self.prov_third_divider = 150000
        self.prov_fourth_divider = 220000

        # 2021 figures for contribution room (initialize)
        self.rrsp_contrib_room = 27830
        self.tfsa_contrib_room = 6000
        self.carry_tfsa_room = 0
        self.carry_rrsp_room = 0

        # Create method to factor in appreciation for investing accounts
        #self.remaining_cash = cash - self.pay_tax_federal(cash) - self.pay_tax_provincial(cash)
        # After-tax money for first payment
        self.remaining_cash = cash
        self.rrsp = self.rrsp_tax_free(inflation) if cash > self.prov_fourth_divider else 0 # no rrsp contrib unless in highest bracket
        self.tfsa = self.tfsa_tax_free(self.remaining_cash, inflation)

        # reflect the change in cash account after depositing into tfsa
        self.remaining_cash -= self.tfsa_tax_free(self.remaining_cash, inflation)

        self.cash_account = self.remaining_cash * split
        self.investing_account = self.remaining_cash * (1 - split)
        self.remaining_cash = 0



    def update_taxes(self, cash, inflation, split):
            self.remaining_cash = self.remaining_cash + cash - self.pay_tax_federal(cash) - self.pay_tax_provincial(cash)
            self.rrsp = self.rrsp + (
                self.rrsp_tax_free(inflation) if cash > 216511 else 0)  # no rrsp contrib unless in highest bracket
            self.tfsa = self.tfsa + self.tfsa_tax_free(self.remaining_cash, inflation)

            # reflect the change in cash account after depositing into tfsa
            self.remaining_cash -= self.tfsa_tax_free(self.remaining_cash,inflation)

            self.cash_account = self.cash_account + self.remaining_cash * split
            self.investing_account = self.investing_account + self.remaining_cash * (1 - split)

            self.remaining_cash = 0

            # Update tax bracket figures
            # Federal brackets
            self.fed_tax_free *= inflation
            self.fed_first_divider *= inflation
            self.fed_second_divider *= inflation
            self.fed_third_divider *= inflation
            self.fed_fourth_divider *= inflation

            # Provincial brackets
            self.prov_first_divider *= inflation
            self.prov_second_divider *= inflation
            self.prov_third_divider *= inflation
            self.prov_fourth_divider *= inflation


    def tfsa_tax_free(self, cash, inflation):
        # update contribution room with inflation
        self.tfsa_contrib_room = self.tfsa_contrib_room * (1 + inflation)

        if cash < self.tfsa_contrib_room: # If we don't use all the contrib room, we carry forward
            self.carry_tfsa_room = self.carry_tfsa_room + self.tfsa_contrib_room - cash
            return cash
        elif cash >= self.tfsa_contrib_room + self.carry_tfsa_room:
            temp = self.carry_tfsa_room
            self.carry_tfsa_room = 0
            return self.tfsa_contrib_room + temp # Use all of contrib room + carry
        else:  # only other option is cash maxes out current contrib but is less than carry
            self.carry_tfsa_room = self.tfsa_contrib_room - (cash - self.tfsa_contrib_room)
            return cash  # Use carry room, can just return cash amount



    def rrsp_tax_free(self, cash, inflation):
        # update contrib room
        self.rrsp_contrib_room = self.rrsp_contrib_room * (1 + inflation)

        # Under the assumption that we will max out the rrsp contrib room for the year since we
        # will be in highest bracket when using

        if cash >= self.rrsp_contrib_room + self.carry_rrsp_room:
            temp = self.carry_rrsp_room
            self.carry_rrsp_room = 0
            return self.rrsp_contrib_room + temp
        else:
            # Cash more than contrib but less than carry room
            self.carry_rrsp_room = self.carry_rrsp_room - (cash - self.rrsp_contrib_room)

        return self.rrsp_contrib_room


    def pay_tax_federal(self, cash):
        # Update this and provincial to factor in inflation

        # These represent the 5 tax brackets
        first, second, third, fourth, fifth = 0, 0, 0, 0, 0

        if cash > self.fed_fourth_divider:      # If in highest tax bracket, deduct rrsp contribution amount
            cash -= 27830

        # Tax free
        if cash <= self.fed_tax_free:
            return 0

        # First tax bracket
        elif cash <= self.fed_first_divider:
            first = cash

        # Second bracket
        elif cash <= self.fed_second_divider:
            first = self.fed_first_divider
            second = cash - self.fed_first_divider

        # Third bracket
        elif cash <= self.fed_third_divider:
            first = self.fed_first_divider
            second = self.fed_second_divider
            third = cash - self.fed_second_divider

        # Fourth bracket
        elif cash <= self.fed_fourth_divider:
            first = self.fed_first_divider
            second = self.fed_second_divider
            third = self.fed_third_divider
            fourth = cash - self.fed_third_divider

        # Fifth bracket
        else:
            first = self.fed_first_divider
            second = self.fed_second_divider
            third = self.fed_third_divider
            fourth = self.fed_fourth_divider
            fifth = cash - self.fed_fourth_divider

        return 0.15 * first + 0.205 * second + 0.26 * third + 0.29 * fourth + 0.33 * fifth


    def pay_tax_provincial(self, cash):

        # These represent the 5 tax brackets
        first, second, third, fourth, fifth = 0, 0, 0, 0, 0

        if cash > self.prov_fourth_divider:      # If in highest tax bracket, deduct rrsp contribution amount
            cash -= 27830

        # First bracket
        if cash <= self.prov_first_divider:
            first = cash

        # Second bracket
        elif cash <= self.prov_second_divider:
            first = self.prov_first_divider
            second = cash - self.prov_first_divider

        # Third bracket
        elif cash <= self.prov_third_divider:
            first = self.prov_first_divider
            second = self.prov_second_divider
            third = cash - self.prov_second_divider

        # Fourth bracket
        elif cash <= self.prov_fourth_divider:
            first = self.prov_first_divider
            second = self.prov_second_divider
            third = self.prov_third_divider
            fourth = cash - self.prov_third_divider

        # Fifth bracket
        else:
            first = self.prov_first_divider
            second = self.prov_second_divider
            third = self.prov_third_divider
            fourth = self.prov_fourth_divider
            fifth = cash - self.prov_fourth_divider

        return 0.0505 * first + 0.0915 * second + 0.1116 * third + 0.1216 * fourth + 0.1316 * fifth


