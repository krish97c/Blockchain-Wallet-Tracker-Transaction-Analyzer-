# Entry point for debugging and testing the blockchain dashboard
import streamlit as st
import subprocess
import os

# Define functions to run individual components and check for errors

def run_app():
    """Run the main Streamlit app and display logs."""
    try:
        st.title('Blockchain Dashboard Debugging')
        st.subheader('Running Streamlit Application...')
        process = subprocess.Popen(['streamlit', 'run', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in process.stdout:
            st.text(line.decode('utf-8'))
    except Exception as e:
        st.error(f'Error running app: {e}')


def run_bot():
    """Run the monitoring bot and show output."""
    st.subheader('Running Monitoring Bot...')
    try:
        process = subprocess.Popen(['python', 'monitoring_bot.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in process.stdout:
            st.text(line.decode('utf-8'))
    except Exception as e:
        st.error(f'Error running monitoring bot: {e}')


def test_database_connection():
    """Test connection to the SQLite database."""
    import sqlite3
    try:
        conn = sqlite3.connect('wallet_tracking.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
        tables = cursor.fetchall()
        st.success(f'Database connected. Tables: {tables}')
        conn.close()
    except Exception as e:
        st.error(f'Error connecting to database: {e}')


if st.button('Run App'):
    run_app()

if st.button('Run Monitoring Bot'):
    run_bot()

if st.button('Test Database Connection'):
    test_database_connection()
