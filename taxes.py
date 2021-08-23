
# Note: takes inflation in decimal form. Split variable used to determine split between cash account
# and investing account (e.g 0.2 means 20% cash, 80% investing)
class Taxes:
    def __init__(self, cash, inflation, split):
        self.remaining_cash = cash - self.pay_tax_federal(cash) - self.pay_tax_provincial(cash)
        self.tfsa =  self.tfsa_tax_free(self.remaining_cash, inflation)
        self.rrsp = self.rrsp_tax_free(inflation) if cash > 216511 else 0 # no rrsp contrib unless in highest bracket
        self.cash_account = self.remaining_cash * split
        self.investing_account = self.remaining_cash * (1 - split)

        # 2021 figures for contribution room (initialize)
        self.rrsp_contrib_room = 27830
        self.tfsa_contrib_room = 6000

        # reflect the change in cash account after depositing into tfsa
        self.remaining_cash -= self.tfsa_tax_free(self.remaining_cash)

    def update_taxes(self, cash, inflation, split):
            self.remaining_cash = self.remaining_cash + cash - self.pay_tax_federal(cash) - self.pay_tax_provincial(cash)
            self.tfsa = self.tfsa + self.tfsa_tax_free(self.remaining_cash, inflation)
            self.rrsp = self.rrsp + (
            self.rrsp_tax_free(inflation) if cash > 216511 else 0)  # no rrsp contrib unless in highest bracket
            self.cash_account = self.cash_account + self.remaining_cash * split
            self.investing_account = self.investing_account + self.remaining_cash * (1 - split)

            # reflect the change in cash account after depositing into tfsa
            self.remaining_cash -= self.tfsa_tax_free(self.remaining_cash)



    def tfsa_tax_free(self, cash, inflation):
        # update contribution room with inflation
        self.tfsa_contrib_room = self.tfsa_contrib_room * (1 + inflation)

        return self.tfsa_contrib_room if cash >= self.tfsa_contrib_room else cash

    def rrsp_tax_free(self, inflation):
        # update contrib room
        self.rrsp_contrib_room = self.rrsp_contrib_room * (1 + inflation)
        return self.rrsp_contrib_room

    @staticmethod
    def pay_tax_federal(cash):
        # These represent the 5 tax brackets
        first, second, third, fourth, fifth = 0, 0, 0, 0, 0

        if cash > 216511:      # If in highest tax bracket, deduct rrsp contribution amount
            cash -= 27830

        if cash <= 13000:
            return 0
        elif cash <= 49020:
            first = cash
        elif cash <= 98040:
            first = 49020
            second = cash - 49020
        elif cash <= 151978:
            first = 49020
            second = 49020
            third = cash - 98040
        elif cash <= 216511:
            first = 49020
            second = 49020
            third = 53939
            fourth = cash - 151978
        else:
            first = 49020
            second = 49020
            third = 53939
            fourth = 64533
            fifth = cash - 216511

        return 0.15 * first + 0.205 * second + 0.26 * third + 0.29 * fourth + 0.33 * fifth

    @staticmethod
    def pay_tax_provincial(cash):

        if cash > 216511:      # If in highest tax bracket, deduct rrsp contribution amount
            cash -= 27830

        if cash <= 45142:
            first = cash
        elif cash <= 90287:
            first = 49020
            second = cash - 49020
        elif cash <= 150000:
            first = 49020
            second = 49020
            third = cash - 98040
        elif cash <= 220000:
            first = 49020
            second = 49020
            third = 53939
            fourth = cash - 151978
        else:
            first = 49020
            second = 49020
            third = 53939
            fourth = 64533
            fifth = cash - 216511

        return 0.0505 * first + 0.0915 * second + 0.1116 * third + 0.1216 * fourth + 0.1316 * fifth


