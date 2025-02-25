import pandas as pd
import numpy as np

def generate_fake_data():
    """Generate fake historical price data for backtesting."""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    prices = np.cumsum(np.random.randn(100)) + 50  # Simulating price movements
    return pd.DataFrame({'Date': dates, 'Price': prices})

def simple_moving_average_strategy(data, short_window=5, long_window=20):
    """Backtest a simple moving average crossover strategy."""
    data['Short_MA'] = data['Price'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Price'].rolling(window=long_window).mean()
    data['Signal'] = np.where(data['Short_MA'] > data['Long_MA'], 1, 0)
    data['Positions'] = data['Signal'].diff()
    return data

def run_backtest():
    """Run backtest and return results."""
    data = generate_fake_data()
    data = simple_moving_average_strategy(data)
    
    initial_balance = 1000  # USD
    position = 0
    balance = initial_balance
    
    for i in range(1, len(data)):
        if data['Positions'].iloc[i] == 1:  # Buy Signal
            position = balance / data['Price'].iloc[i]
            balance = 0
        elif data['Positions'].iloc[i] == -1 and position > 0:  # Sell Signal
            balance = position * data['Price'].iloc[i]
            position = 0
    
    final_balance = balance if balance > 0 else position * data['Price'].iloc[-1]
    profit = final_balance - initial_balance
    
    return {
        "Final Balance": round(final_balance, 2),
        "Profit/Loss": round(profit, 2),
        "Trades Executed": data['Positions'].abs().sum()
    }
