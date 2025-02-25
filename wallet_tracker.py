import requests
import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY")
SOLANA_API_KEY = os.getenv("SOLANA_API_KEY")

BLOCKCHAIN_APIS = {
    "bitcoin": "https://blockchain.info/unconfirmed-transactions?format=json",
    "solana": f"https://api.solscan.io/transactions?limit=100&apikey={SOLANA_API_KEY}",
    "ethereum": f"https://api.etherscan.io/api?module=account&action=txlist&sort=desc&apikey={ETHERSCAN_API_KEY}&address=",
    "binance smart chain": f"https://api.bscscan.com/api?module=account&action=txlist&sort=desc&apikey={BSCSCAN_API_KEY}&address="
}

DB_PATH = "wallet_tracking.db"

def initialize_database():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS wallets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wallet_address TEXT UNIQUE,
        blockchain TEXT,
        total_received REAL,
        transaction_count INTEGER,
        last_updated TIMESTAMP
    )''')
    conn.commit()
    conn.close()

initialize_database()

def get_wallet_balance(wallet_address, blockchain):
    try:
        if blockchain == "bitcoin":
            url = f"https://blockchain.info/balance?active={wallet_address}"
        elif blockchain == "solana":
            url = "https://api.mainnet-beta.solana.com"
            payload = {"jsonrpc": "2.0", "id": 1, "method": "getBalance", "params": [wallet_address]}
            response = requests.post(url, json=payload).json()
            return response.get("result", {}).get("value", 0) / 1e9
        elif blockchain in ["ethereum", "binance smart chain"]:
            url = BLOCKCHAIN_APIS[blockchain] + wallet_address
        else:
            return None
        
        response = requests.get(url).json()
        return int(response.get("result", 0)) / 1e18
    except Exception as e:
        print(f"Error fetching {blockchain} balance: {e}")
        return None


# Function to Detect and Identify Wallets
def detect_and_identify_wallets(blockchain, max_wallets=150, filter_type="all", skip_demo=False):
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        
        url = BLOCKCHAIN_APIS.get(blockchain.lower())
        if not url:
            print(f"Unsupported blockchain: {blockchain}")
            return {}

        response = requests.get(url)
        if response.status_code != 200:
            print(f"API request failed for {blockchain} with status {response.status_code}")
            return {}

        response = response.json()
        wallets = {}
        
        transactions = response.get("txs", [])[:max_wallets] if blockchain == "bitcoin" else response.get("result", [])[:max_wallets]
        if not transactions:
            print(f"No transactions found for {blockchain}.")
            return {}

        for tx in transactions:
            address = tx.get("to") if blockchain != "bitcoin" else next((out.get("addr") for out in tx.get("out", [])), None)
            value = float(tx.get("value", 0)) / 1e18 if blockchain != "bitcoin" else sum(out.get("value", 0) for out in tx.get("out", [])) / 1e8
            if address and address != "Unknown":
                if skip_demo and value < 0.01:
                    continue
                if address not in wallets:
                    wallets[address] = {"total_received": value, "transaction_count": 1}
                else:
                    wallets[address]["total_received"] += value
                    wallets[address]["transaction_count"] += 1

        wallet_data_list = [
            {
                "wallet_address": w,
                "total_received": v["total_received"],
                "transaction_count": v["transaction_count"],
                "blockchain": blockchain
            }
            for w, v in wallets.items()
        ]

        sorted_wallets = sorted(wallet_data_list, key=lambda x: (x["transaction_count"] > 2, x["total_received"]), reverse=True)
        potential_new_wallets = [w for w in sorted_wallets if w["transaction_count"] <= 2]
        potential_repeated_buyers = [w for w in sorted_wallets if w["transaction_count"] > 2]

        if filter_type == "new":
            sorted_wallets = potential_new_wallets
        elif filter_type == "potential":
            sorted_wallets = potential_repeated_buyers

        for wallet in sorted_wallets:
            cursor.execute('''INSERT OR REPLACE INTO wallets (wallet_address, blockchain, total_received, transaction_count, last_updated)
                              VALUES (?, ?, ?, ?, ?)''',
                           (wallet["wallet_address"], wallet["blockchain"], wallet["total_received"], wallet["transaction_count"], datetime.now()))

        conn.commit()
        conn.close()

        return {
            "all_wallets": sorted_wallets,
            "potential_new_wallets": potential_new_wallets,
            "potential_repeated_buyers": potential_repeated_buyers
        }
    except Exception as e:
        print(f"Error detecting wallets on {blockchain}: {e}")
        return {} 