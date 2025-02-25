import requests

BINANCE_TRADE_HISTORY_URL = "https://api.binance.com/api/v3/trades?symbol=BTCUSDT"

def get_trade_history(limit=10):
    """Fetch recent Bitcoin trades from Binance."""
    try:
        response = requests.get(BINANCE_TRADE_HISTORY_URL, params={"limit": limit})
        trades = response.json()
        trade_data = [
            {
                "price": float(trade["price"]),
                "quantity": float(trade["qty"]),
                "timestamp": trade["time"],
                "buyer": trade["isBuyerMaker"],
            }
            for trade in trades
        ]
        return trade_data
    except Exception as e:
        print(f"Error fetching trade history: {e}")
        return []
