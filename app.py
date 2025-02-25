import streamlit as st
import plotly.express as px
import datetime
import sqlite3
import pandas as pd
from wallet_tracker import detect_and_identify_wallets, get_wallet_balance
import time
from trade_recommender import recommend_trade, execute_trade
from notifications import send_email_alert, send_telegram_alert, send_discord_alert
from user_tracking import register_new_user, load_users
from backtesting_module import run_backtest
from highest_spenders import identify_highest_spenders
from spending_analysis import analyze_spending
from market_data import get_historical_prices, get_crypto_prices, get_real_time_data
from ai_trading import predict_trade_signal
from datetime import date, timedelta
from datetime import datetime, timedelta
import plotly.graph_objects as go
from historical_tracking import get_historical_prices
from wallet_analysis import analyze_spending
import requests
from dotenv import load_dotenv
from risk_management import calculate_risk_metrics

st.set_page_config(page_title="Crypto Wallet Tracker", layout="wide")
st.title("🚀 Blockchain Wallet Tracker & Transaction Analyzer 🚀")

# Initialize Database
def initialize_database():
    conn = sqlite3.connect("wallet_tracking.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS wallets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wallet_address TEXT,
        blockchain TEXT,
        total_received REAL,
        transaction_count INTEGER,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

initialize_database()

# Mapping function to convert our selection to CoinGecko coin ID
def get_coin_id(blockchain):
    mapping = {
        "bitcoin": "bitcoin",
        "ethereum": "ethereum",
        "solana": "solana",
        "binancecoin": "binancecoin"
    }
    return mapping.get(blockchain, blockchain)

# Helper function: Try fetching historical prices; if empty, try with a longer period.
def safe_get_historical_prices(coin_id, days=1):
    df = get_historical_prices(coin_id, days)
    if df.empty and days < 30:
        df = get_historical_prices(coin_id, days=7)
    return df

# Sidebar Configuration
st.sidebar.header("🔍 Blockchain Selection & Settings")
blockchain = st.sidebar.selectbox(
    "Select Blockchain",
    ["bitcoin", "ethereum", "solana", "binancecoin"],
    key="sidebar_blockchain_select"
)

# Display current cryptocurrency price
crypto_prices = get_crypto_prices()
if isinstance(crypto_prices, dict) and blockchain in crypto_prices:
    st.sidebar.metric(f"💲 {blockchain.capitalize()} Price", f"${crypto_prices.get(blockchain, {}).get('usd', 'N/A')}")

max_wallets = st.sidebar.slider("Number of Wallets to Retrieve", min_value=10, max_value=500, value=150)
filter_type = st.sidebar.radio("Filter by Wallet Type", ["all", "new", "potential"], index=0)
skip_demo = st.sidebar.checkbox("Skip Demo Wallets (Low Balance)")

page = st.sidebar.radio("Go to", ["Home", "Wallet Tracking", "Historical Tracking","Wallet Analysis","AI Trading"])

if page == "Home":
    st.subheader("💰 Blockchain Balance & Real-Time Analytics")
    wallet_address = st.text_input("Enter Wallet Address")
    
    if st.button("Check Balance") and wallet_address:
        balance = get_wallet_balance(wallet_address, blockchain)
        if balance is not None:
            st.success(f"Balance: {balance} {blockchain.upper()}")
        else:
            st.error("Invalid Wallet Address")
    
    # Real-Time Analytics (Only for Bitcoin)
    if blockchain == "bitcoin":
        st.subheader("📊 Real-Time Blockchain Analytics")
        real_time_data = get_real_time_data(blockchain)
        if isinstance(real_time_data, dict):
            total_transactions = real_time_data.get("total_transactions", "N/A")
            total_volume = real_time_data.get("total_volume", "N/A")
            active_wallets = real_time_data.get("active_wallets", "N/A")
            st.metric("Total Transactions", total_transactions)
            st.metric("Total Volume", f"{total_volume} {blockchain.upper()}")
            st.metric("Active Wallets", active_wallets)
            
            # Visualization
            if isinstance(real_time_data.get("transactions"), list):
                df = pd.DataFrame(real_time_data["transactions"])
                if not df.empty and "timestamp" in df.columns and "value" in df.columns:
                    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
                    st.subheader("📈 Real-Time Transaction Trends")
                    fig = px.line(df, x="timestamp", y="value", title=f"Real-Time {blockchain.capitalize()} Transaction Volume")
                    st.plotly_chart(fig)


# Last 24 Hours Price Trend Graph
    st.subheader("📉 Last 24 Hours Price Trend")

# Ensure coin_id is properly retrieved
    coin_id = get_coin_id(blockchain)

    if not coin_id:
        st.error(f"Error: Could not fetch CoinGecko ID for {blockchain}")
    else:
    # Calculate timestamps
        end_timestamp = int(time.time())  # Current time in seconds
        days = 7 if blockchain in ["solana", "binancecoin"] else 1
        start_timestamp = end_timestamp - (days * 24 * 60 * 60)  # Subtract days in seconds

    # Fetch historical price data
        try:
            historical_data = get_historical_prices(coin_id, start_timestamp, end_timestamp)

            if isinstance(historical_data, pd.DataFrame) and not historical_data.empty:
                fig = px.line(historical_data, x="timestamp", y="price",
                            title=f"{blockchain.capitalize()} Price Trend (Last {days} Day{'s' if days > 1 else ''})")
                st.plotly_chart(fig)
            else:
                st.warning(f"No historical price data available for {blockchain.capitalize()} for the last {days} day{'s' if days > 1 else ''}.")
        except Exception as e:
            st.error(f"Error retrieving price data: {e}")

elif page == "Wallet Tracking":
    st.subheader("💰 Enhanced Wallet Tracking & Visualization")
    
    wallet_data = detect_and_identify_wallets(blockchain, max_wallets, filter_type, skip_demo)
    if wallet_data and "all_wallets" in wallet_data:
        st.subheader("📊 Wallet Data Visualization & Insights")
        tab1, tab2, tab3 = st.tabs(["All Wallets", "New Wallets", "Repeated Buyers"])
        with tab1:
            st.metric("Total Wallets Found", len(wallet_data["all_wallets"]))
            # Convert to DataFrame for visualization purposes
            df_all = pd.DataFrame(wallet_data["all_wallets"])
            st.dataframe(df_all)
            # Bar Chart: Total Received by each Wallet (if data available)
            if not df_all.empty and "wallet_address" in df_all.columns and "total_received" in df_all.columns:
                fig = px.bar(df_all, x="wallet_address", y="total_received", color="transaction_count",
                             title="Total Received by Wallets")
                st.plotly_chart(fig)
        with tab2:
            st.metric("New Wallets Found", len(wallet_data["potential_new_wallets"]))
            st.dataframe(pd.DataFrame(wallet_data["potential_new_wallets"]))
        with tab3:
            st.metric("Repeated Buyers Detected", len(wallet_data["potential_repeated_buyers"]))
            st.dataframe(pd.DataFrame(wallet_data["potential_repeated_buyers"]))
    else:
        st.warning("No wallet data found on this blockchain.")

elif page == "AI Trading":
    st.subheader("📈 AI Trading Predictions")
    wallet_address = st.text_input("Enter Wallet Address")
    if st.button("Get AI Trade Signal") and wallet_address:
        signal = predict_trade_signal(blockchain)
        if signal:
            st.success(f"🛖 Trade Signal: **{signal}** for {blockchain.upper()}")
        else:
            st.error("Could not generate trade signal.")

# ===================== 📅 HISTORICAL TRACKING PAGE =====================


# 📊 Historical Price Tracking
# ==============================
elif page == "Historical Tracking":
    st.sidebar.subheader("📈 Historical Price Tracking")
    
    # User Inputs for Crypto Price Analysis
    blockchain = st.sidebar.selectbox("Select Cryptocurrency", ["bitcoin", "ethereum", "solana", "binancecoin"])
    from datetime import datetime, timedelta

    start_date = st.date_input("Start Date", value=datetime.now().date() - timedelta(days=7), key="risk_start")

    end_date = st.sidebar.date_input("End Date", value=date.today())

    # Convert dates to timestamps
    start_timestamp = int(pd.to_datetime(start_date).timestamp())
    end_timestamp = int(pd.to_datetime(end_date).timestamp())

    def historical_price_tracking():
        """Fetches and displays historical price data for selected cryptocurrency."""
        st.subheader("📊 Historical Price Tracking")

        def get_coin_id(crypto):
            mapping = {"bitcoin": "bitcoin", "ethereum": "ethereum", "solana": "solana", "binancecoin": "binancecoin"}
            return mapping.get(crypto.lower(), "bitcoin")

        def get_historical_prices(coin_id, start_timestamp, end_timestamp):
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range?vs_currency=usd&from={start_timestamp}&to={end_timestamp}"
            response = requests.get(url)
            data = response.json()
            if "prices" in data:
                df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
                return df
            return pd.DataFrame()

        coin_id = get_coin_id(blockchain)
        historical_data = get_historical_prices(coin_id, start_timestamp, end_timestamp)

        if not historical_data.empty:
            fig = px.line(historical_data, x="timestamp", y="price", title=f"{blockchain.capitalize()} Price Trend")

            # Add Technical Indicators
            historical_data["SMA_10"] = historical_data["price"].rolling(window=10).mean()
            historical_data["SMA_20"] = historical_data["price"].rolling(window=20).mean()

            fig.add_trace(go.Scatter(x=historical_data["timestamp"], y=historical_data["SMA_10"], mode='lines', name="10-Day SMA"))
            fig.add_trace(go.Scatter(x=historical_data["timestamp"], y=historical_data["SMA_20"], mode='lines', name="20-Day SMA"))

            st.plotly_chart(fig)

            # Key Statistics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📈 Highest Price", f"${historical_data['price'].max():.2f}")
            col2.metric("📉 Lowest Price", f"${historical_data['price'].min():.2f}")
            col3.metric("📊 Avg Price", f"${historical_data['price'].mean():.2f}")
            col4.metric("📉 % Change", f"{((historical_data['price'].iloc[-1] - historical_data['price'].iloc[0]) / historical_data['price'].iloc[0]) * 100:.2f}%")

            # Export Data
            csv_data = historical_data.to_csv(index=False).encode("utf-8")
            st.download_button(label="⬇ Download CSV", data=csv_data, file_name=f"{blockchain}_historical_data.csv", mime="text/csv")
        else:
            st.warning(f"No historical data available for {blockchain.capitalize()} in the selected range.")

    historical_price_tracking()

# ==============================
# 💳 Wallet Spending Analysis
# ==============================
elif page == "Wallet Analysis":
    st.sidebar.subheader("💳 Wallet Spending Analysis")

    # User Inputs for Wallet Analysis
    wallet_address = st.sidebar.text_input("Enter Wallet Address")
    wallet_chain = st.sidebar.selectbox("Select Blockchain", ["Bitcoin", "Ethereum", "Solana", "Binance Smart Chain"])
    wallet_start_date = st.sidebar.date_input("Wallet Start Date", value=date.today() - timedelta(days=30))
    wallet_end_date = st.sidebar.date_input("Wallet End Date", value=date.today())

    # Convert wallet dates to timestamps
    wallet_start_timestamp = int(pd.to_datetime(wallet_start_date).timestamp())
    wallet_end_timestamp = int(pd.to_datetime(wallet_end_date).timestamp())

    def wallet_spending_analysis():
        """Analyzes wallet spending trends."""
        st.subheader("💳 Wallet Spending Patterns")

        if wallet_address and st.button("Analyze Spending"):
            spending_data = analyze_spending(wallet_address, wallet_chain.lower())

            if spending_data:
                st.subheader("📊 Spending Analysis")
                st.write(spending_data)

                df = pd.DataFrame([spending_data])
                fig = px.bar(df, x="large_spends", y="frequent_small_trades", title="Spending Pattern Overview")
                st.plotly_chart(fig)
            else:
                st.warning("No data found for the given wallet.")

    wallet_spending_analysis()




