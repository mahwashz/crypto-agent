# agent/crypto_agent.py

import re
from tools.coinlore_tools import get_crypto_price
from tools.chart_utils import generate_price_chart
from alerts.alerts import add_alert, check_alerts
from google.generativeai import GenerativeModel

model = GenerativeModel("models/gemini-1.5-flash")

async def run_agent(user_input: str):
    user_input = user_input.lower()

    alert_pattern = r"alert.*?(?P<symbol>btc|eth|sol|xrp|doge)\b.*?(?P<op>>|<)\s?(?P<price>\d+\.?\d*)"
    match = re.search(alert_pattern, user_input)

    if match:
        symbol = match.group("symbol").upper()
        operator = match.group("op")
        threshold = float(match.group("price"))
        user_email = "your_email@example.com"
        add_alert(symbol, operator, threshold, user_email)
        return f"🔔 Alert set: {symbol} {operator} {threshold}"

    chart_pattern = r"(chart|graph|plot).*?\b(btc|eth|sol|xrp|doge)\b"
    chart_match = re.search(chart_pattern, user_input)

    if chart_match:
        symbol = chart_match.group(2).upper()
        chart_path = generate_price_chart(symbol)
        price = get_crypto_price(symbol)

        gemini_reply = model.generate_content(
            f"Current price of {symbol} is ${price}. Should I invest in it?"
        )
        return (
            f"💰 {symbol} price: ${price}\n\n🧠 Gemini says:\n{gemini_reply.text}",
            chart_path
        )

    symbol = next((sym for sym in ["BTC", "ETH", "SOL", "DOGE", "XRP"] if sym.lower() in user_input), None)
    if not symbol:
        return "❌ Unknown coin. Try: BTC, ETH, SOL, DOGE, XRP"

    price = get_crypto_price(symbol)
    check_alerts()

    gemini_reply = model.generate_content(
        f"Current price of {symbol} is ${price}. Would you recommend investing in {symbol}?"
    )

    return f"💰 {symbol} price: ${price}\n\n🧠 Gemini says:\n{gemini_reply.text}"
