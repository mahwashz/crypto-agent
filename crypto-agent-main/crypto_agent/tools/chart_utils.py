# tools/chart_utils.py

import matplotlib.pyplot as plt
import os
import datetime
import random

def generate_fake_price_data(symbol="BTC"):
    return [random.uniform(20000, 60000) for _ in range(30)]

def generate_price_chart(symbol="BTC"):
    prices = generate_fake_price_data(symbol)
    dates = [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(len(prices))]
    dates.reverse()

    plt.figure(figsize=(10, 4))
    plt.plot(dates, prices, marker="o", linestyle="-", color="#0099FF")
    plt.title(f"{symbol} Price Trend (Last 30 Days)")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    os.makedirs("data/charts", exist_ok=True)
    filepath = f"data/charts/{symbol}_chart.png"
    plt.savefig(filepath)
    plt.close()

    return filepath
