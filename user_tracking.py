import json
import datetime
from notifications import send_email_alert, send_telegram_alert, send_discord_alert

USER_DATA_FILE = "registered_users.json"

def load_users():
    """Load stored registered users."""
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(data):
    """Save updated user data."""
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def register_new_user(username, wallet_address, blockchain):
    """Register a new user and send alerts."""
    users = load_users()
    
    if username in users:
        return f"User {username} is already registered."

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    users[username] = {
        "wallet_address": wallet_address,
        "blockchain": blockchain,
        "registered_at": timestamp
    }
    
    save_users(users)

    # Send alerts for new registration
    message = f"🆕 New User Registered!\n👤 **User:** {username}\n🔗 **Wallet:** {wallet_address}\n⏰ **Time:** {timestamp}\n🌐 **Blockchain:** {blockchain}"
    send_email_alert("New User Registration", message)
    send_telegram_alert(message)
    send_discord_alert(message)

    return f"✅ User {username} registered successfully!"
