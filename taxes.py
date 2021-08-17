class Taxes:

    def __init__(self, income):
        self.tax_free = self.tax_free_amount(income)
        self.taxable = income - self.tax_free

    @staticmethod
    def tax_free_amount(cash):
        return 6000 if cash >= 6000 else cash

    def pay_tax_provincial(self):
        # These represent the 5 tax brackets
        first, second, third, fourth, fifth = 0

        if self.taxable <= 49020:
            first = self.taxable
        elif self.taxable <= 98040:
            first = 49020
            second = self.taxable - 49020
        elif self.taxable <= 151978:
            first = 49020
            second = 49020
            third = self.taxable - 98040
        elif self.taxable <= 216511:
            first = 49020
            second = 49020
            third = 53939
            fourth = self.taxable - 151978
        else:
            first = 49020
            second = 49020
            third = 53939
            fourth = 64533
            fifth = self.taxable - 216511
        return 0.15 * first + 0.205 * second + 0.26 * third + 0.29 * fourth + 0.33 * fifth

