from src.database.connection import get_db_connection

def run_migrations():
    with get_db_connection() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id              TEXT PRIMARY KEY,
                name            TEXT NOT NULL,
                account_type    TEXT NOT NULL CHECK(account_type IN ('checking', 'savings', 'investment')),
                balance         REAL NOT NULL DEFAULT 0.0,
                status          TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'inactive')),
                created_at      TEXT NOT NULL,
                updated_at      TEXT NOT NULL
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                   id               TEXT PRIMARY KEY,
                   account_id       TEXT NOT NULL,
                   transaction_type TEXT NOT NULL CHECK(transaction_type IN ('deposit', 'withdrawal', 'transfer_in', 'transfer_out')),
                   amount           REAL NOT NULL,
                   new_balance      REAL NOT NULL,
                   timestamp        TEXT NOT NULL
            );
        """)