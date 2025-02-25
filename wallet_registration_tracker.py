import streamlit as st  # Streamlit must be imported first
st.set_page_config(page_title="Automated Wallet Monitoring", layout="wide")  # Must be the first Streamlit command


import requests
import json
from datetime import datetime
from notifications import send_email_alert, send_telegram_alert, send_discord_alert

# Example API Endpoints (Replace with actual APIs)
SOLANA_NEW_WALLETS_API = "https://api.solana.com/getNewWallets"
ETHEREUM_NEW_WALLETS_API = "https://api.etherscan.io/api"
BINANCE_NEW_WALLETS_API = "https://api.bscscan.com/api"
BITCOIN_NEW_WALLETS_API = "https://api.blockchain.com/v3/exchange/accounts"

def fetch_historical_transactions(wallet_address, blockchain, start_date, end_date):
    """Fetch historical transactions for a given wallet (Stub function)."""
    # Replace with an actual API call to get transactions for the wallet
    return [
        {"amount": 0.5, "timestamp": "2024-07-10T12:30:00"},
        {"amount": 1.2, "timestamp": "2024-07-11T08:45:00"}
    ]

def check_new_wallets(blockchain):
    """Fetch new wallet addresses created on a given blockchain."""
    if blockchain == "solana":
        url = SOLANA_NEW_WALLETS_API
    elif blockchain == "ethereum":
        url = ETHEREUM_NEW_WALLETS_API
    elif blockchain == "binance":
        url = BINANCE_NEW_WALLETS_API
    elif blockchain == "bitcoin":
        url = BITCOIN_NEW_WALLETS_API
    else:
        return []

    try:
        response = requests.get(url, timeout=10)  # Add timeout to prevent hanging requests
        response.raise_for_status()  # Raise error for HTTP failures
        data = response.json()
        return data.get("new_wallets", [])
    except requests.RequestException as e:
        print(f"Error fetching new wallets for {blockchain}: {e}")
        return []

def track_first_fund_receipt(wallet_address, blockchain):
    """Check if a new wallet has received its first funds."""
    transactions = fetch_historical_transactions(wallet_address, blockchain, "2023-01-01", datetime.today().strftime('%Y-%m-%d'))
    
    if transactions:
        first_transaction = transactions[0]  # Oldest transaction
        return {
            "wallet": wallet_address,
            "amount": first_transaction["amount"],
            "timestamp": first_transaction["timestamp"]
        }
    return None

def detect_new_wallet_activity():
    """Detect and notify when new wallets receive funds."""
    detected_wallets = []

    for blockchain in ["solana", "ethereum", "binance", "bitcoin"]:
        new_wallets = check_new_wallets(blockchain)
        
        for wallet in new_wallets:
            first_funds = track_first_fund_receipt(wallet, blockchain)
            
            if first_funds:
                message = f"🆕 **New Wallet Alert!**\n🔗 Wallet: {wallet}\n💰 First Funds: {first_funds['amount']}\n📅 Date: {first_funds['timestamp']}"
                send_email_alert("New Wallet Alert", message)
                send_telegram_alert(message)
                send_discord_alert(message)
                detected_wallets.append(first_funds)

    return detected_wallets

# Example function call
if __name__ == "__main__":
    result = detect_new_wallet_activity()
    print(result)
