import requests
import json
import time
import pandas as pd
import streamlit as st
from notifications import send_email_alert, send_telegram_alert, send_discord_alert
from dotenv import load_dotenv
import os
SPENDING_PATTERN_FILE = "spending_patterns.json"


load_dotenv()

# Retrieve API keys
SOLANA_API_KEY = os.getenv("SOLANA_API_KEY")
BSC_API_KEY = os.getenv("BSC_API_KEY")

def load_spending_patterns():
    """Load stored spending patterns."""
    try:
        with open(SPENDING_PATTERN_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_spending_patterns(patterns):
    """Save updated spending patterns."""
    with open(SPENDING_PATTERN_FILE, "w") as file:
        json.dump(patterns, file, indent=4)

def fetch_transactions(wallet_address, blockchain):
    """Fetch recent transactions for a wallet with API key authentication."""
    api_urls = {
        "solana": f"https://api.solana.fm/v0/accounts/{wallet_address}/transactions",
        "ethereum": f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&sort=desc&apikey={BSC_API_KEY}",
        "bsc": f"https://api.bscscan.com/api?module=account&action=txlist&address={wallet_address}&sort=desc&apikey={BSC_API_KEY}",
        "bitcoin": f"https://blockchain.info/rawaddr/{wallet_address}"
    }

    headers = {}
    if blockchain.lower() == "solana":
        headers = {"Authorization": f"Bearer {SOLANA_API_KEY}"}

    try:
        response = requests.get(api_urls[blockchain.lower()], headers=headers)
        response_json = response.json()

        print(f"🔍 API Response for {wallet_address} ({blockchain}):\n{json.dumps(response_json, indent=4)}")

        if blockchain.lower() in ["ethereum", "bsc"]:
            return response_json.get("result", [])  # Extract transactions list
        elif blockchain.lower() == "solana":
            return response_json.get("transactions", [])  # Adjust based on actual API response
        elif blockchain.lower() == "bitcoin":
            return response_json.get("txs", [])

        return []
    except Exception as e:
        print(f"🚨 Error fetching transactions: {e}")
        return []


def analyze_spending(wallet_address, blockchain, start_timestamp=None, end_timestamp=None):
    """Detect suspicious spending patterns."""
    transactions = fetch_transactions(wallet_address, blockchain)

    if not isinstance(transactions, list) or len(transactions) == 0:
        print(f"🚨 No transactions found for {wallet_address} on {blockchain}.")
        return None

    spending_data = []
    frequent_small_trades = 0
    repeated_token_trades = {}
    large_spends = 0

    transactions = transactions[:50]  # ✅ Safe slicing now

    for tx in transactions:
        timestamp = int(tx.get("timeStamp", 0) if "timeStamp" in tx else tx.get("time", 0))

        # Filter transactions by date range
        if start_timestamp and end_timestamp and not (start_timestamp <= timestamp <= end_timestamp):
            continue

        # Handle Solana transactions (No `value` field)
        if blockchain == "solana":
            pre_balances = tx.get("transaction", {}).get("meta", {}).get("preBalances", [0])
            post_balances = tx.get("transaction", {}).get("meta", {}).get("postBalances", [0])
            amount = (pre_balances[0] - post_balances[0]) / 10**9  # Convert lamports to SOL
        else:
            amount = float(tx.get("value", 0)) / 10**18 if blockchain != "bitcoin" else float(tx.get("value", 0))

        token = tx.get("tokenSymbol", "Unknown") if "tokenSymbol" in tx else "Native"

        spending_data.append({"Amount": amount, "Token": token, "Time": timestamp})

        if amount < 0.01:
            frequent_small_trades += 1
        if token not in repeated_token_trades:
            repeated_token_trades[token] = 0
        repeated_token_trades[token] += 1
        if amount > 10:
            large_spends += 1

    # Store analysis results
    spending_patterns = load_spending_patterns()
    spending_patterns[wallet_address] = {
        "frequent_small_trades": frequent_small_trades,
        "repeated_token_trades": repeated_token_trades,
        "large_spends": large_spends,
        "is_demo": frequent_small_trades > 10 or any(v > 5 for v in repeated_token_trades.values())
    }

    save_spending_patterns(spending_patterns)
    return spending_patterns[wallet_address]
