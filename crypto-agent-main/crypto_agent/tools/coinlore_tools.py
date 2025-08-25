# tools/coinlore_tools.py
import requests

def get_crypto_price(symbol="BTC"):
    url = "https://api.coinlore.net/api/tickers/"
    res = requests.get(url).json()
    coins = res.get("data", [])

    for coin in coins:
        if coin["symbol"].upper() == symbol.upper():
            return float(coin["price_usd"])

    raise ValueError("Coin not found")
