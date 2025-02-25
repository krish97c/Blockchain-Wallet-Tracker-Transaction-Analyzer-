import time
import schedule
from wallet_registration_tracker import detect_new_wallet_activity
from notifications import send_daily_report, send_trade_alerts

def run_monitoring():
    """Continuously check for new wallets and send alerts."""
    print("🔍 Checking for new wallets...")
    result = detect_new_wallet_activity()
    print("✅ Monitoring Completed:", result)

# Schedule the monitoring tasks
schedule.every(10).minutes.do(run_monitoring)
schedule.every().hour.do(send_trade_alerts)
schedule.every().day.at("00:00").do(send_daily_report)

if __name__ == "__main__":
    print("🚀 Monitoring Bot Started")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Sleep for 1 minute
