import requests
import json
import time
from notifications import send_email_alert, send_telegram_alert, send_discord_alert

# API Endpoints for checking wallet transactions
BLOCKCHAIN_APIS = {
    "bitcoin": "https://blockchain.info/rawaddr/",
    "solana": "https://api.mainnet-beta.solana.com",
    "ethereum": "https://api.etherscan.io/api?module=account&action=txlist&address=",
    "binance": "https://api.bscscan.com/api?module=account&action=txlist&address="
}

# File paths for storing data
NEW_WALLETS_FILE = "new_wallets.json"
FIRST_DEPOSITS_FILE = "first_deposits.json"
TOKEN_PURCHASES_FILE = "first_token_purchases.json"
SOLANA_BALANCE_FILE = "solana_remaining_balances.json"

# Utility functions to handle JSON file operations
def load_json(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# Function to monitor new wallets on all blockchains
def monitor_new_wallets():
    existing_wallets = load_json(NEW_WALLETS_FILE)
    new_wallets_detected = []
    wallets_to_check = {
        "bitcoin": ["1ExampleBTCWallet123"],
        "solana": ["ExampleSolanaWalletXYZ"],
        "ethereum": ["0xExampleEthereumWallet456"],
        "binance": ["0xExampleBSCWallet789"]
    }

    for blockchain, wallets in wallets_to_check.items():
        for wallet in wallets:
            if wallet not in existing_wallets:
                existing_wallets[wallet] = blockchain
                new_wallets_detected.append((wallet, blockchain))

    if new_wallets_detected:
        save_json(NEW_WALLETS_FILE, existing_wallets)
        for wallet, blockchain in new_wallets_detected:
            message = f"🚀 New {blockchain.capitalize()} wallet detected: {wallet}"
            send_email_alert("New Wallet Detected", message)
            send_telegram_alert(message)
            send_discord_alert(message)

    return new_wallets_detected


# Function to track Solana wallet balances
def monitor_solana_balances():
    solana_balances = load_json(SOLANA_BALANCE_FILE)
    new_wallets = load_json(NEW_WALLETS_FILE)

    for wallet, blockchain in new_wallets.items():
        if blockchain == "solana" and wallet not in solana_balances:
            solana_balances[wallet] = "Simulated Solana Balance Data"
            message = f"🪙 Solana balance monitored for wallet {wallet}."
            send_email_alert("Solana Balance Alert", message)
            send_telegram_alert(message)
            send_discord_alert(message)

    save_json(SOLANA_BALANCE_FILE, solana_balances)
    return solana_balances


# Function to track first deposits in new wallets
def track_first_deposits():
    first_deposits = load_json(FIRST_DEPOSITS_FILE)
    new_wallets = load_json(NEW_WALLETS_FILE)

    for wallet, blockchain in new_wallets.items():
        if wallet not in first_deposits:
            first_deposits[wallet] = {
                "blockchain": blockchain,
                "first_deposit": "Simulated Deposit Data"
            }
            message = f"💸 First deposit detected in {wallet} on {blockchain}."
            send_email_alert("First Deposit Alert", message)
            send_telegram_alert(message)
            send_discord_alert(message)

    save_json(FIRST_DEPOSITS_FILE, first_deposits)
    return first_deposits


# Function to track first token purchases
def track_first_token_purchases():
    token_purchases = load_json(TOKEN_PURCHASES_FILE)
    new_wallets = load_json(NEW_WALLETS_FILE)

    for wallet, blockchain in new_wallets.items():
        if wallet not in token_purchases:
            token_purchases[wallet] = {
                "blockchain": blockchain,
                "first_purchase": "Simulated Token Purchase Data"
            }
            message = f"🛒 First token purchase detected in {wallet} on {blockchain}."
            send_email_alert("First Token Purchase Alert", message)
            send_telegram_alert(message)
            send_discord_alert(message)

    save_json(TOKEN_PURCHASES_FILE, token_purchases)
    return token_purchases


if __name__ == "__main__":
    while True:
        print("Checking for new wallets...")
        monitor_new_wallets()
        print("Tracking first deposits...")
        track_first_deposits()
        print("Tracking first token purchases...")
        track_first_token_purchases()
        print("Tracking Solana balances...")
        monitor_solana_balances()
        time.sleep(600)
