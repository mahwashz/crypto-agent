# alerts/alerts.py
from tools.coinlore_tools import get_crypto_price

alerts = []

def add_alert(symbol, operator, threshold, email):
    alerts.append({
        "symbol": symbol,
        "op": operator,
        "threshold": threshold,
        "email": email
    })

def check_alerts():
    for alert in alerts:
        try:
            price = get_crypto_price(alert["symbol"])
        except:
            print(f"⚠️ Invalid symbol: {alert['symbol']}")
            continue

        symbol = alert["symbol"]
        op = alert["op"]
        target = alert["threshold"]

        if (op == ">" and price > target) or (op == "<" and price < target):
            print(f"🚨 {symbol} is {op} {target}. Current: {price}")
