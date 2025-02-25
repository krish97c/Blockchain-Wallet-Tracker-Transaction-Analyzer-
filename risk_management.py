import numpy as np
import pandas as pd


def calculate_trailing_stop(price_history, trailing_percent=5):
    """Calculates the trailing stop price based on the highest price reached."""
    if not price_history:
        return None

    highest_price = max(price_history)
    trailing_stop = highest_price * (1 - trailing_percent / 100)
    return trailing_stop


def position_sizing(balance, risk_percentage, price):
    """Calculate position size based on risk management rules."""
    return (balance * risk_percentage) / price


def validate_investment(balance_btc, invest_btc):
    """Ensure the user has enough balance for investment."""
    if invest_btc > balance_btc:
        return "⚠️ Insufficient balance to invest."
    elif invest_btc < 0.001:
        return "⚠️ Minimum trade size is 0.001 BTC."
    else:
        return f"✅ Investment approved: {invest_btc:.6f} BTC"


def calculate_sharpe_ratio(price_history, risk_free_rate=0.01):
    """Calculate the Sharpe Ratio from historical price data."""
    if len(price_history) < 2:
        return 0  # Not enough data

    returns = pd.Series(price_history).pct_change().dropna()  # Convert prices to returns

    excess_returns = returns - (risk_free_rate / 252)  # Convert to daily rate
    std_dev = np.std(excess_returns)

    if std_dev == 0:
        return 0  # Avoid division by zero

    return np.mean(excess_returns) / std_dev


def calculate_max_drawdown(price_history):
    """Calculate the maximum drawdown in percentage."""
    if len(price_history) < 2:
        return 0  # Not enough data

    price_array = np.array(price_history)
    peak = np.maximum.accumulate(price_array)  # Track max value up to each point
    drawdown = (price_array - peak) / peak  # Compute drawdowns
    max_drawdown = np.min(drawdown) * 100  # Convert to percentage

    return max_drawdown


def portfolio_balancing(current_holdings, risk_allocation):
    """Adjusts portfolio based on risk levels."""
    total_value = sum(current_holdings.values())
    target_allocation = {asset: total_value * risk_allocation.get(asset, 0) for asset in current_holdings}

    adjustments = {asset: target_allocation[asset] - current_holdings[asset] for asset in current_holdings}
    return adjustments


def calculate_risk_metrics(historical_data, risk_free_rate=0.01):
    """
    Calculate various risk metrics such as Sharpe Ratio, Max Drawdown, and Trailing Stop.

    :param historical_data: DataFrame with a "price" column
    :param risk_free_rate: Risk-free rate (default 1%)
    :return: Dictionary containing risk metrics
    """
    if historical_data is None or historical_data.empty:
        return {
            "sharpe_ratio": None,
            "max_drawdown": None,
            "trailing_stop": None,
        }

    price_history = historical_data["price"].tolist()

    sharpe_ratio = calculate_sharpe_ratio(price_history, risk_free_rate)
    max_drawdown = calculate_max_drawdown(price_history)
    trailing_stop = calculate_trailing_stop(price_history)

    return {
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "trailing_stop": trailing_stop,
    }


# Example Usage
if __name__ == "__main__":
    # Simulated historical price data
    price_history = [100, 102, 105, 110, 107]

    # Calculate trailing stop
    trailing_stop = calculate_trailing_stop(price_history)
    print(f"Trailing Stop Price: {trailing_stop}")

    # Portfolio balancing example
    current_holdings = {"ETH": 5000, "BTC": 10000, "USDT": 5000}
    risk_allocation = {"ETH": 0.3, "BTC": 0.5, "USDT": 0.2}
    adjustments = portfolio_balancing(current_holdings, risk_allocation)
    print(f"Portfolio Adjustments: {adjustments}")
