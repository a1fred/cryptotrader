from decimal import Decimal


btc_amount = Decimal("0.001")  # btc amount for buy order per coin
profit = Decimal("0.02")  # profit perc for sell order, 0.02 is 2%

# Get api key and secret from your bittrex profile page
BITTREX = {
    'key': '123',
    'secret': '321',
}
