import requests
import pandas as pd
import time

BLOCKCHAIN_API_URLS = {
    "bitcoin": "https://api.blockchain.info/stats",
    "ethereum": "https://api.etherscan.io/api?module=stats&action=ethprice",
    "solana": "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd",
    "binance smart chain": "https://api.bscscan.com/api?module=stats&action=bnbprice"
}

def get_real_time_data(blockchain):
    """Fetch real-time blockchain analytics (transactions, volume, active wallets)."""
    blockchain = blockchain.lower()
    
    if blockchain not in BLOCKCHAIN_API_URLS:
        return None
    
    response = requests.get(BLOCKCHAIN_API_URLS[blockchain])
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    
    if blockchain == "bitcoin":
        return {
            "total_transactions": data.get("n_tx", "N/A"),
            "total_volume": data.get("trade_volume_btc", "N/A"),  # Fixed this field
            "active_wallets": data.get("n_unique_addresses", "N/A"),
            "transactions": []
        }
    elif blockchain == "ethereum":
        return {
            "total_transactions": "N/A",  
            "total_volume": data["result"].get("ethusd", "N/A"),
            "active_wallets": "N/A",
            "transactions": []
        }
    elif blockchain == "solana":
        return {
            "total_transactions": "N/A",
            "total_volume": data.get("solana", {}).get("usd", "N/A"),  # Correct field for SOL price
            "active_wallets": "N/A",
            "transactions": []
        }
    elif blockchain == "binance smart chain":
        return {
            "total_transactions": "N/A",
            "total_volume": data["result"].get("bnbusd", "N/A"),  # Fixed wrong field
            "active_wallets": "N/A",
            "transactions": []
        }

    return None

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

def get_crypto_prices():
    """Fetch real-time crypto prices from CoinGecko."""
    params = {
        "ids": "bitcoin,ethereum,solana,binancecoin",
        "vs_currencies": "usd"
    }
    response = requests.get(COINGECKO_API_URL, params=params)
    return response.json()

def process_price_data(data):
    """Convert API response into a Pandas DataFrame."""
    prices = data.get("prices", [])
    
    if not prices:
        print("🚨 Error: No price data found!")
        return pd.DataFrame()
    
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    
    # Convert timestamp to datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    return df
def safe_get_historical_prices(crypto, days=180):
    return get_historical_prices(crypto, days=days)


def get_historical_prices(crypto, days=180, retries=3):
    """Fetch historical price data with retry mechanism."""
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart?vs_currency=usd&days={days}"
    
    for attempt in range(retries):
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return process_price_data(data)  # Convert API response to DataFrame
        
        elif response.status_code == 429:  # Rate limit exceeded
            wait_time = (2 ** attempt) * 5  # Exponential backoff
            print(f"🚨 API Rate Limit Exceeded! Retrying in {wait_time} seconds... (Attempt {attempt+1}/{retries})")
            time.sleep(wait_time)
        else:
            print(f"🚨 API Error {response.status_code}: {response.text}")
            break  # Stop retrying if it's another error
    
    print("🚨 Error: Unable to fetch historical data!")
    return pd.DataFrame()  # Return an empty DataFrame on failure

# Example Usage:
crypto = "bitcoin"
df = get_historical_prices(crypto, days=180)
print(df.head())  # Verify data output
