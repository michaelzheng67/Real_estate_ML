
# Note: takes inflation in decimal form. Split variable used to determine split between cash account
# and investing account (e.g 0.2 means 20% cash, 80% investing)
# we should add saving ratio and subtract from remaining cash. can be pre-tax or post-tax

# Include assets growing in accounts
# Include capital gains member (Investing account)
# Make update investment accounts to update investment accounts monthly

class Taxes:
    def __init__(self, cash, inflation, split):  # Should consider replacing init class with manual entry of allocations

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

        self.rrsp_annual_contrib_room = 27830
        self.rrsp_total_contrib_room = 0
        self.tfsa_annual_contrib_room = 6000
        self.tfsa_total_contrib_room = 0

        # Create method to factor in appreciation for investing accounts
        #self.remaining_cash = cash - self.pay_tax_federal(cash) - self.pay_tax_provincial(cash)
        # After-tax money for first payment
        self.remaining_cash = cash
        #self.rrsp = self.rrsp_tax_free(inflation) if cash > self.prov_fourth_divider else 0 # no rrsp contrib unless in highest bracket
        self.rrsp = 0
        tfsa_used = self.tfsa_tax_free(self.remaining_cash, inflation, new_year=1)
        print("TFSA Contribution Room", self.tfsa_total_contrib_room)
        print("Annual Contribution Room", self.tfsa_annual_contrib_room)
        self.tfsa = tfsa_used

        # reflect the change in cash account after depositing into tfsa
        self.remaining_cash -= tfsa_used

        self.cash_account = self.remaining_cash * split
        self.investing_account = self.remaining_cash * (1 - split)
        self.remaining_cash = 0

        # keep track of paid taxes for year
        self.taxes_paid = 0

        #accrued income
        self.accrued_net_income = 0

        # money that is taxable, but not liquid or to avoid double counting. Ex: principal repayments/capital gains
        self.income_deduction = 0

# keep track of taxes already paid and add back?
# add parameter in update_taxes to see if it is a new year or not. If so, increase brackets for inflation and raise contribution limits.
    def update_taxes(self, new_monthly_income, inflation, split, new_year):
            self.accrued_net_income += new_monthly_income
            # determines how much to reduce net income by
            rrsp_used = self.rrsp_tax_free(self.accrued_net_income, inflation, new_year)
            self.rrsp += rrsp_used
            self.accrued_net_income = self.accrued_net_income - rrsp_used


            taxes_payable = self.pay_tax_federal(self.accrued_net_income) + self.pay_tax_provincial(self.accrued_net_income)

            self.remaining_cash = self.remaining_cash + new_monthly_income - (taxes_payable - self.taxes_paid) - self.income_deduction # add new monthly income to remaining cash, subtract new taxes
            # update taxes paid
            self.taxes_paid = self.pay_tax_federal(self.accrued_net_income) + self.pay_tax_provincial(self.accrued_net_income)

            # Adds new amount deposited into TFSA
            tfsa_used = self.tfsa_tax_free(self.remaining_cash, inflation, new_year)

            self.tfsa = self.tfsa + tfsa_used

            # reflect the change in cash account after depositing into tfsa
            self.remaining_cash -= tfsa_used

            self.cash_account = self.cash_account + self.remaining_cash * split
            self.investing_account = self.investing_account + self.remaining_cash * (1 - split)


            self.income_deduction = 0

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

    # returns how much of TFSA we use that month
    def tfsa_tax_free(self, cash, inflation, new_year):
        # update contribution room with inflation, if year end
        if new_year == 1:
            self.tfsa_annual_contrib_room = self.tfsa_annual_contrib_room * (1 + inflation)
            self.tfsa_total_contrib_room = self.tfsa_total_contrib_room + self.tfsa_annual_contrib_room

        if cash < self.tfsa_total_contrib_room: # Not enough to fill up all of TFSA room
            self.tfsa_total_contrib_room = self.tfsa_total_contrib_room - cash
            return cash
        elif cash >= self.tfsa_total_contrib_room: # More than enough to fill up TFSA room
            total_contrib_room = self.tfsa_total_contrib_room
            self.tfsa_total_contrib_room = 0
            return total_contrib_room # Use all of contrib room

    # returns how much of RRSP we use that month
    def rrsp_tax_free(self, cash, inflation, new_year):
        # update contrib room every year including inflation
        if new_year == 1:
            self.rrsp_annual_contrib_room = self.rrsp_annual_contrib_room * (1 + inflation)
            # 18% of income or rrsp annual contribution room, which ever is less
            if self.rrsp_annual_contrib_room <= cash * 0.18:
                self.rrsp_total_contrib_room += self.rrsp_annual_contrib_room
            else:
                self.rrsp_total_contrib_room += cash * 0.18

        # if we fall into highest tax bracket
        if cash > self.prov_fourth_divider:
            high_tax_money = cash - self.prov_fourth_divider    # money that falls into the highest bracket

            if high_tax_money < self.rrsp_total_contrib_room:   # Not enough to fill up all of RRSP room (only use until we're out of top tax bracket)
                self.rrsp_total_contrib_room = self.rrsp_total_contrib_room - high_tax_money
                return high_tax_money
            elif high_tax_money >= self.rrsp_total_contrib_room:    # More than enough to fill up RRSP room
                self.rrsp_total_contrib_room = 0
                return self.rrsp_total_contrib_room     # Use all of contrib room
        else:
            return 0


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


