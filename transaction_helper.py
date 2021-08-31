# Withdraws money from accounts when making a purchase
# Order of choice is tax based
def payment_selection(financial_accounts, price):
    if price > financial_accounts.cash_account:
        price -= financial_accounts.cash_account
        financial_accounts.cash_account = 0
    else:
        financial_accounts.cash_account -= price
        price = 0

    if price > financial_accounts.tfsa:
        tfsa_used = financial_accounts.tfsa
        price -= financial_accounts.tfsa
        financial_accounts.tfsa = 0
    else:
        tfsa_used = price
        financial_accounts.tfsa -= price
        price = 0

    if price > financial_accounts.investing_account:
        investment_used = financial_accounts.investing_account
        price -= financial_accounts.investing_account
        financial_accounts.investing_account = 0
    else:
        investment_used = price
        financial_accounts.investing_account -= price
        price = 0

    rrsp_used = price
    financial_accounts.rrsp -= price

    financial_accounts.carry_tfsa_room += tfsa_used
    #financial_accounts.rrsp_carry_room += rrsp_used

    return financial_accounts, investment_used, rrsp_used






