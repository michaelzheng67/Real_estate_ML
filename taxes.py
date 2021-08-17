class Taxes:
    def __init__(self, cash):
        self.remaining_cash = self.pay_tax_provincial(cash)
        self.tfsa = self.tfsa_tax_free(self.remaining_cash)
        self.rrsp = self.rrsp_tax_free()

        # reflect the change in cash account after depositing into tfsa
        self.remaining_cash -= self.tfsa_tax_free(self.remaining_cash)


    @staticmethod
    def tfsa_tax_free(cash):
        return 6000 if cash >= 6000 else cash # change to reflect growing contrib limit

    @staticmethod
    def rrsp_tax_free():
        return 27830 # change later on to reflect growing contribution limit

    @staticmethod
    def pay_tax_provincial(cash):
        # These represent the 5 tax brackets
        first, second, third, fourth, fifth = 0, 0, 0, 0, 0

        if cash > 216511:      # If in highest tax bracket, deduct rrsp contribution amount
            cash -= 27830

        if cash <= 49020:
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

