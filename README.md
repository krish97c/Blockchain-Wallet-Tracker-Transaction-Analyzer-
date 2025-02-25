
# Blockchain Wallet Tracker & Transaction Analyzer

## 🚀 Overview
This project is a **Blockchain Wallet Tracker & Transaction Analyzer** that monitors wallet transactions across multiple blockchains, including **Bitcoin, Ethereum, Solana, and Binance Smart Chain (BSC)**. It retrieves transaction history, analyzes wallet activity, and stores data in an SQLite database.

## 🛠 Features
- **Multi-Blockchain Support**: Supports Bitcoin, Ethereum, Solana, and BSC.
- **Real-time Transaction Fetching**: Retrieves transactions using public APIs.
- **Wallet Balance Calculation**: Fetches wallet balances for supported blockchains.
- **SQLite Database Integration**: Stores and updates wallet transactions.
- **Filtering & Categorization**: Identifies new wallets and potential repeat buyers.
- **Environment Variables Support**: Uses `.env` for API keys security.
- **Enhanced Visualization**: Generates insights and reports on wallet activity.

## 📦 Installation
### 1. Clone the Repository
```sh
git clone https://github.com/your-repo/blockchain-wallet-tracker.git
cd blockchain-wallet-tracker
```

### 2. Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory and add:
```ini
ETHERSCAN_API_KEY=your_etherscan_api_key
SOLANA_API_KEY=your_solana_api_key
BSC_API_KEY=your_bsc_api_key
```

## 🚀 Usage
### Run the Tracker
```sh
python app.py
```

### Example Function Calls
#### Get Wallet Balance
```python
balance = get_wallet_balance("0xYourWalletAddress", "ethereum")
print(f"Ethereum Wallet Balance: {balance} ETH")
```

#### Detect and Identify Wallets
```python
wallets = detect_and_identify_wallets("ethereum", max_wallets=100, filter_type="all")
print(wallets)
```

## 📊 API Endpoints Used
- **Bitcoin**: `https://blockchain.info/unconfirmed-transactions?format=json`
- **Ethereum**: `https://api.etherscan.io/api?module=account&action=txlist&apikey=YOUR_API_KEY&address=YOUR_WALLET`
- **Solana**: `https://api.solscan.io/transactions?limit=100&apikey=YOUR_API_KEY`
- **BSC**: `https://api.bscscan.com/api?module=account&action=txlist&apikey=YOUR_API_KEY&address=YOUR_WALLET`

## 🛠 Technologies Used
- **Python**
- **SQLite**
- **Requests (API Calls)**
- **Dotenv (Environment Variables)**
- **Streamlit (Visualization Dashboard)**

## 📌 Future Enhancements
- **Web Dashboard for Visualization**
- **Alert System for Large Transactions**
- **Machine Learning for Wallet Behavior Analysis**
- **Multi-User Authentication for Secure Access**

## 📄 License
This project is licensed under the MIT License.

---
**Happy Tracking! 🚀**

