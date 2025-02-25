import numpy as np
from data_fetch import fetch_price_history

def analyze_market():
    """Determine if BTC is in a good buying range."""
    history_df = fetch_price_history()
    recent_prices = history_df["price"].values

    if len(recent_prices) < 7:
        return "Not enough data", None  # Wait for more data

    avg_price_7d = np.mean(recent_prices[-7:])  # Average of last 7 entries
    current_price = recent_prices[-1]

    if current_price < avg_price_7d * 0.98:  # If current price is 2% lower than avg
        return "Buy", current_price
    elif current_price > avg_price_7d * 1.02:  # If price is 2% higher
        return "Hold", current_price
    else:
        return "Neutral", current_price

def recommend_investment(balance_btc, btc_price):
    """Suggest how much to invest based on balance and price trends."""
    market_signal, _ = analyze_market()

    if market_signal == "Buy":
        invest_amount = balance_btc * 0.3  # Suggest investing 30% of balance
        return f"Buy recommendation: Invest {invest_amount:.6f} BTC (~${invest_amount * btc_price:.2f})"
    elif market_signal == "Hold":
        return "Hold recommendation: Wait for a better entry price."
    else:
        return "Neutral: No strong signal to buy or sell."
