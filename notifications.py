import smtplib
import discord
import telebot
import os
import requests

# Load credentials from environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Function to handle wallet event notifications
def notify_wallet_event(event_details):
    """Send notifications for wallet events."""
    message = f"🔔 Wallet Event: {event_details}"
    print(message)
    send_email_alert("Wallet Event Notification", message)
    send_telegram_alert(message)
    send_discord_alert(message)


# Email Notification
def send_email_alert(subject, body):
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_USER, EMAIL_PASS)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(EMAIL_USER, EMAIL_USER, message)
        server.quit()
        print("📩 Email sent successfully!")
    except Exception as e:
        print(f"⚠️ Email sending failed: {e}")


# Telegram Notification
def send_telegram_alert(message):
    try:
        bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
        bot.send_message(TELEGRAM_CHAT_ID, message)
        print("📩 Telegram message sent!")
    except Exception as e:
        print(f"⚠️ Telegram message failed: {e}")


# Discord Notification
def send_discord_alert(message):
    try:
        data = {"content": message}
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("📩 Discord message sent!")
        else:
            print(f"⚠️ Discord message failed: {response.text}")
    except Exception as e:
        print(f"⚠️ Discord message failed: {e}")


# Example Alert
if __name__ == '__main__':
    notify_wallet_event("Test wallet event notification.")
