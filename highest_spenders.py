import requests
import json
import datetime
from notifications import send_email_alert, send_telegram_alert, send_discord_alert

SPENDING_DATA_FILE = "highest_spenders.json"

def load_spending_data():
    """Load stored highest spending data."""
    try:
        with open(SPENDING_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_spending_data(data):
    """Save updated highest spending data."""
    with open(SPENDING_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def fetch_transactions(blockchain):
    """Fetch transactions for a given blockchain."""
    api_urls = {
        "solana": "https://api.solscan.io/transactions?limit=100",
        "ethereum": "https://api.etherscan.io/api?module=account&action=txlist&sort=desc",
        "bsc": "https://api.bscscan.com/api?module=account&action=txlist&sort=desc",
        "bitcoin": "https://blockchain.info/unconfirmed-transactions?format=json"
    }

    try:
        response = requests.get(api_urls[blockchain.lower()]).json()
        return response
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return None

def identify_highest_spenders(blockchain, selected_date=None):
    """Identify the highest spending wallets for a given date."""
    transactions = fetch_transactions(blockchain)
    if not transactions:
        return None

    daily_spending = {}
    today = selected_date if selected_date else datetime.datetime.utcnow().strftime("%Y-%m-%d")

    for tx in transactions[:200]:  # Analyze last 200 transactions
        timestamp = int(tx.get("timeStamp", 0))
        tx_date = datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
        if tx_date != today:
            continue  # Skip transactions from other dates

        wallet = tx.get("from", "Unknown")
        amount = float(tx.get("value", 0)) / 10**18 if blockchain != "bitcoin" else float(tx.get("value", 0))

        if wallet not in daily_spending:
            daily_spending[wallet] = 0
        daily_spending[wallet] += amount

    if not daily_spending:
        return None

    highest_spender = max(daily_spending, key=daily_spending.get)
    highest_amount = daily_spending[highest_spender]

    # Store highest spender data
    spending_data = load_spending_data()
    spending_data[today] = {
        "blockchain": blockchain,
        "wallet": highest_spender,
        "amount": highest_amount
    }
    save_spending_data(spending_data)

    # Send alerts for highest spender
    message = f"🔥 Highest spender on {blockchain} for {today}: {highest_spender} spent {highest_amount:.2f} {blockchain.upper()}"
    send_email_alert("Highest Spending Wallet Detected", message)
    send_telegram_alert(message)
    send_discord_alert(message)

    return spending_data[today]

# Run analysis every hour
if __name__ == "__main__":
    for chain in ["solana", "ethereum", "bsc", "bitcoin"]:
        identify_highest_spenders(chain)
