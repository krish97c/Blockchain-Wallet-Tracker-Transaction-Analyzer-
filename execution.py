import ccxt

def execute_trade(decision, symbol="ETH/USDT", amount=0.1):
    exchange = ccxt.binance({
        'apiKey': 'YOUR_API_KEY',
        'secret': 'YOUR_SECRET_KEY',
    })

    try:
        if decision == "BUY":
            order = exchange.create_market_buy_order(symbol, amount)
            print(f"BUY order executed: {order}")
        elif decision == "SELL":
            order = exchange.create_market_sell_order(symbol, amount)
            print(f"SELL order executed: {order}")
        else:
            print("No trade executed. Decision was HOLD.")
            return "No trade executed"

        return order
    except Exception as e:
        print(f"Trade execution error: {e}")
        return None
