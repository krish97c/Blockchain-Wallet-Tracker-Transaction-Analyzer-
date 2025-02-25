import requests
import pandas as pd

def get_historical_prices(coin_id, start_timestamp, end_timestamp):
    """
    Fetch historical price data for a given cryptocurrency using the CoinGecko API.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range"
    params = {
        "vs_currency": "usd",  # Prices in USD
        "from": start_timestamp,
        "to": end_timestamp
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "prices" in data:
            df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')  # Convert to readable format
            return df

    return pd.DataFrame()  # Return empty DataFrame if no data is available
