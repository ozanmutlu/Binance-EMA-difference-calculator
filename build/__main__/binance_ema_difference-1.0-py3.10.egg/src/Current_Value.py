import requests

def currentValue(coin):
    field = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=" + coin)
    field =field.json()
    field = float(field["price"])
    return field