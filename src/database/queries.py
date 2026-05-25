import uuid
import sqlite3
from typing import Any
from datetime import datetime, timezone
from src.models.schemas import AccountCreate, AccountUpdate

def create_account(db: sqlite3.Connection, account_data: AccountCreate) -> dict[str, Any]:
    account_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    db.execute("""
        INSERT INTO accounts (id, name, account_type, balance, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, 'active', ?, ?)
    """, (account_id, account_data.name, account_data.account_type, account_data.initial_balance, now, now))
    cursor = db.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
    row = cursor.fetchone()
    return dict(row)

def get_account_by_id(db: sqlite3.Connection, account_id: str) -> dict[str, Any] | None:
    cursor = db.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
    row = cursor.fetchone()
    return dict(row) if row else None

def get_accounts(db: sqlite3.Connection, limit: int, offset: int) -> tuple[list[dict[str, Any]], int]:
    cursor = db.execute("SELECT * FROM accounts LIMIT ? OFFSET ?", (limit, offset))
    accounts = [dict(row) for row in cursor.fetchall()]
    total_cursor = db.execute("SELECT COUNT(*) FROM accounts")
    total = total_cursor.fetchone()[0]
    return accounts, total

def update_account(db: sqlite3.Connection, account_id: str, update_data: AccountUpdate) -> bool:
    fields: list[str] = []
    values: list[Any] = []
    if update_data.name is not None:
        fields.append("name = ?")
        values.append(update_data.name)
    if update_data.status is not None:
        fields.append("status = ?")
        values.append(update_data.status)
    if not fields:
        return False
    values.append(datetime.now(timezone.utc).isoformat())
    values.append(account_id)
    cursor = db.execute(f"""
        UPDATE accounts SET {', '.join(fields)}, updated_at = ?
        WHERE id = ?
    """, tuple(values))
    return cursor.rowcount > 0

def deactivate_account(db: sqlite3.Connection, account_id: str) -> bool:
    cursor = db.execute("""
        UPDATE accounts SET status = 'inactive', updated_at = ?
        WHERE id = ?
    """, (datetime.now(timezone.utc).isoformat(), account_id))
    return cursor.rowcount > 0
