import logging

def setup_logging():
    """Set up logging for the bot."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger("TradingBot")

def format_price(price):
    """Format price to 2 decimal places."""
    return f"${price:.2f}"
