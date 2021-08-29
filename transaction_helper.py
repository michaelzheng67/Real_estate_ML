def payment_selection(tfsa,rrsp,cash,investment, price):

    if price > cash:
        price -= cash
        cash = 0
    else:
        cash -= price
        price = 0

    if price > tfsa:
        price -= tfsa
        tfsa = 0
    else:
        tfsa -= price
        price = 0

    if price > investment:
        investment_used = investment
        price -= investment
        investment = 0
    else:
        investment_used = price
        investment -= price
        price = 0

    rrsp_used = price
    rrsp -= price

    return tfsa, rrsp, cash, investment, investment_used, rrsp_used






