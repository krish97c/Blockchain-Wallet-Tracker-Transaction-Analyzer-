import streamlit as st  # Streamlit must be imported first
st.set_page_config(page_title="Automated Wallet Monitoring", layout="wide")  # Must be the first Streamlit command

from wallet_registration_tracker import detect_new_wallet_activity
import subprocess
import os
import signal

st.title("🚀 Automated Wallet Monitoring")

# Function to check if the monitoring bot is running
def is_bot_running():
    if os.path.exists("monitoring_bot.pid"):
        with open("monitoring_bot.pid", "r") as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, 0)  # Check if the process exists
            return True
        except OSError:
            os.remove("monitoring_bot.pid")  # Clean up if the process is dead
    return False

# Start monitoring
if st.button("Start Monitoring"):
    if not is_bot_running():
        process = subprocess.Popen(["python", "monitoring_bot.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open("monitoring_bot.pid", "w") as f:
            f.write(str(process.pid))
        st.success("✅ Monitoring Started!")
    else:
        st.warning("⚠️ Monitoring is already running.")

# Check for new wallets
if st.button("Check for New Wallets"):
    result = detect_new_wallet_activity()
    st.success(result)

# Stop monitoring
if st.button("Stop Monitoring"):
    if is_bot_running():
        with open("monitoring_bot.pid", "r") as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, signal.SIGTERM)  # Terminate process safely
            os.remove("monitoring_bot.pid")
            st.success("❌ Monitoring Stopped!")
        except OSError:
            st.error("⚠️ Failed to stop monitoring. Process may have already exited.")
    else:
        st.warning("⚠️ No active monitoring process found.")
