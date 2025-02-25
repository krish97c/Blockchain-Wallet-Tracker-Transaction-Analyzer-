import time
from data_fetch import get_bitcoin_price

ALERT_THRESHOLD = 1.5  # Alert if price moves by 1.5% within 5 minutes

def track_price_changes():
    """Track BTC price and alert on significant changes."""
    last_price = get_bitcoin_price()
    
    while True:
        time.sleep(300)  # Check every 5 minutes
        new_price = get_bitcoin_price()
        
        if last_price and new_price:
            price_change = ((new_price - last_price) / last_price) * 100
            
            if abs(price_change) >= ALERT_THRESHOLD:
                alert_msg = f"⚠️ Bitcoin Price Alert! Price moved by {price_change:.2f}% in 5 minutes. Current Price: ${new_price:.2f}"
                print(alert_msg)  # Can be replaced with a notification system
            
            last_price = new_price
