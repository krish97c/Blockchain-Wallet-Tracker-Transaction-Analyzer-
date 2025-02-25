from wallet_tracker import get_wallet_balance

from notifications import notify_wallet_event

BUY_THRESHOLD_BTC = 0.1  # Example threshold for BTC
BUY_THRESHOLD_SOL = 5  # Example threshold for SOL

import requests

def get_market_trend(coin):
    """Fetch real-time market trends for a given coin."""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&include_24hr_change=true"
    try:
        response = requests.get(url).json()
        price = response[coin]["usd"]
        change_24h = response[coin]["usd_24h_change"]
        return price, change_24h
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return None, None

def recommend_trade(wallet_address, blockchain):
    """Generate trade recommendations based on wallet balance and market trends."""
    price, change_24h = get_market_trend(blockchain.lower())
    
    if price is None:
        return "Error fetching market data. Unable to provide a recommendation."
    
    # Fetch wallet balance using the unified function
    balance = get_wallet_balance(wallet_address, blockchain.lower())
    if balance is None:
        return f"Unable to retrieve balance for {wallet_address} on {blockchain}."

    recommendation = "HOLD"
    if change_24h is not None:
        if change_24h < -2 and balance < 10:  # Recommend buying if price dropped and balance is low
            recommendation = "BUY"
        elif change_24h > 2:  # Recommend selling if price increased significantly
            recommendation = "SELL"

    # Send a notification for the trade recommendation
    notify_wallet_event(wallet_address, f"Trade Recommendation: {recommendation}")

    return f"Trade Recommendation for {wallet_address} on {blockchain}: {recommendation} (24h Change: {change_24h:.2f}%)"


def execute_trade(wallet_address, coin, price, change_percentage):
    """Simulate trade execution based on price movements."""
    action = "BUY" if change_percentage < 0 else "SELL"
    trade_info = f"Executed {action} trade for {wallet_address} on {coin} at ${price:.2f}"
    return trade_info

# Example test case
if __name__ == "__main__":
    test_wallet = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    print(recommend_trade(test_wallet, "bitcoin"))
