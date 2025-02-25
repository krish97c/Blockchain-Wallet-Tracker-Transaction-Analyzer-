import requests
import datetime
import pandas as pd
from notifications import send_email_alert, send_telegram_alert, send_discord_alert

# Example API URLs (You need actual blockchain API keys)
SOLANA_API_URL = "https://api.solana.com/getTransactions"
ETHEREUM_API_URL = "https://api.etherscan.io/api"
BINANCE_API_URL = "https://api.bscscan.com/api"
BITCOIN_API_URL = "https://api.blockchain.com/v3/exchange/tickers"

def fetch_transactions(wallet_address, blockchain):
    """Fetch transaction history for a given wallet."""
    if blockchain == "solana":
        url = f"{SOLANA_API_URL}?wallet={wallet_address}"
    elif blockchain == "ethereum":
        url = f"{ETHEREUM_API_URL}?module=account&action=txlist&address={wallet_address}"
    elif blockchain == "binance":
        url = f"{BINANCE_API_URL}?module=account&action=txlist&address={wallet_address}"
    elif blockchain == "bitcoin":
        url = f"{BITCOIN_API_URL}?symbol=BTC-USD"
    else:
        return []

    response = requests.get(url).json()
    return response.get("transactions", [])

def analyze_spending(wallet_address, blockchain):
    """Analyze spending patterns & detect demo accounts."""
    transactions = fetch_transactions(wallet_address, blockchain)
    
    if not transactions:
        return "No transaction data available."

    df = pd.DataFrame(transactions)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s')
    
    # Track first-time purchase
    first_purchase = df.iloc[0] if not df.empty else None
    
    # Check for demo account pattern (many small transactions)
    small_tx_count = len(df[df["amount"] < 0.01])  
    demo_account = small_tx_count > 5  # If >5 small transactions, flag as demo

    # Highest spender of the day
    today = datetime.datetime.utcnow().date()
    daily_transactions = df[df["timestamp"].dt.date == today]
    highest_spender = daily_transactions.loc[daily_transactions["amount"].idxmax()] if not daily_transactions.empty else None

    # Remaining balance check
    remaining_balance = df["balance"].iloc[-1] if not df.empty else 0

    # Alerts
    if demo_account:
        message = f"⚠️ **Demo Account Detected!**\n🔗 Wallet: {wallet_address}\n📊 Too many small transactions!"
        send_email_alert("Demo Account Alert", message)
        send_telegram_alert(message)
        send_discord_alert(message)

    return {
        "first_purchase": first_purchase.to_dict() if first_purchase is not None else "No purchases",
        "demo_account": demo_account,
        "highest_spender": highest_spender.to_dict() if highest_spender is not None else "No transactions today",
        "remaining_balance": remaining_balance
    }
