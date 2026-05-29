def format_currency(amount, currency_symbol='$'):
    return f"{currency_symbol}{amount:,.2f}"
print(format_currency(1234567.896))