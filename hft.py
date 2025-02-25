import websocket
import json
import time

# WebSocket URL for exchange (e.g., Binance, Coinbase Pro)
WEBSOCKET_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"

def on_message(ws, message):
    """Handles incoming WebSocket messages (trade updates)."""
    trade = json.loads(message)
    price = float(trade['p'])
    quantity = float(trade['q'])
    print(f"Trade Update - Price: {price}, Quantity: {quantity}")
    # Implement HFT logic here (market-making, arbitrage, etc.)

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed")

def on_open(ws):
    print("WebSocket Connection Established")
    # Can send subscription messages if needed

if __name__ == "__main__":
    ws = websocket.WebSocketApp(WEBSOCKET_URL, 
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
