import sqlite3

def create_wallet_activity_table():
    """Creates a database table to store wallet activity."""
    conn = sqlite3.connect("wallet_tracking.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallet_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet_address TEXT,
            blockchain TEXT,
            first_funds_received REAL,
            first_token TEXT,
            first_token_amount REAL,
            remaining_balance REAL,
            spending_pattern TEXT,
            highest_spend REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def insert_wallet_activity(wallet_address, blockchain, first_funds_received, first_token, first_token_amount, remaining_balance, spending_pattern, highest_spend):
    """Insert wallet tracking data into the database."""
    conn = sqlite3.connect("wallet_tracking.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO wallet_activity (wallet_address, blockchain, first_funds_received, first_token, first_token_amount, remaining_balance, spending_pattern, highest_spend)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (wallet_address, blockchain, first_funds_received, first_token, first_token_amount, remaining_balance, spending_pattern, highest_spend))
    conn.commit()
    conn.close()


def fetch_all_trackers(blockchain):
    """Fetch all wallet trackers from the database for the selected blockchain."""
    conn = sqlite3.connect("wallet_tracking.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wallet_activity WHERE blockchain = ?", (blockchain,))
    rows = cursor.fetchall()
    conn.close()
    return rows


# Example usage
if __name__ == '__main__':
    create_wallet_activity_table()
    print(fetch_all_trackers("ethereum"))
