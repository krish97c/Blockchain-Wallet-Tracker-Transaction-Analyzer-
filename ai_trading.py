import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from market_data import get_historical_prices

def generate_features(df):
    """Generate additional features from raw price data."""
    df["price_change"] = df["price"].pct_change()
    df["volatility"] = df["price"].rolling(window=3).std()
    df["momentum"] = df["price"] - df["price"].shift(3)
    df["SMA_5"] = df["price"].rolling(window=5).mean()
    df["EMA_5"] = df["price"].ewm(span=5, adjust=False).mean()
    df["RSI"] = compute_rsi(df["price"])
    
    df.fillna(method="bfill", inplace=True)  # Fill missing values
    df["label"] = np.where(df["price_change"] > 0, 1, 0)
    return df

def compute_rsi(prices, window=14):
    """Compute the Relative Strength Index (RSI) for given prices."""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def train_model(crypto):
    """Train a trading model using historical data."""
    df = get_historical_prices(crypto, days=180)
    if df is None or df.empty:
        print(f"🚨 Error: No historical data returned for {crypto}")
        return None, None
    df = generate_features(df)
    
    features = ["price_change", "volatility", "momentum", "SMA_5", "EMA_5", "RSI"]
    df.dropna(inplace=True)  # Drop any remaining NaNs
    X = df[features]
    y = df["label"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    return model, scaler

def predict_trade_signal(crypto):
    """Predict trade signal (Buy/Sell) using AI model."""
    model, scaler = train_model(crypto)
    df = get_historical_prices(crypto, days=1)
    if df.empty:
        print(f"🚨 Error: No data retrieved for {crypto}.")
        return "Error: No data available"
    df = generate_features(df)
    
    required_columns = ["price_change", "volatility", "momentum", "SMA_5", "EMA_5", "RSI"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"🚨 Error: Missing columns {missing_columns} in DataFrame!")
        return f"Error: Missing required features {missing_columns}"
    
    latest_data = scaler.transform(df[required_columns].iloc[-1:].values)
    prediction = model.predict(latest_data)
    return "BUY" if prediction[0] == 1 else "SELL"
