import uuid
import sqlite3
import src.exceptions as exceptions
from typing import Any, Optional
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
    existing_account = get_account_by_id(db, account_id)
    if not existing_account:
        raise exceptions.AccountNotFoundException(f"Account with ID {account_id} not found")
    if update_data.name is not None:
        fields.append("name = ?")
        values.append(update_data.name)
    if update_data.status is not None:
        fields.append("status = ?")
        values.append(update_data.status)
    if not fields:
        raise exceptions.NoFieldsToUpdateException("No fields to update")
    values.append(datetime.now(timezone.utc).isoformat())
    values.append(account_id)
    cursor = db.execute(f"""
        UPDATE accounts SET {', '.join(fields)}, updated_at = ?
        WHERE id = ?
    """, tuple(values))
    return cursor.rowcount > 0

def deactivate_account(db: sqlite3.Connection, account_id: str) -> bool:
    existing_account = get_account_by_id(db, account_id)
    if not existing_account:
        raise exceptions.AccountNotFoundException(f"Account with ID {account_id} not found")
    cursor = db.execute("""
        UPDATE accounts SET status = 'inactive', updated_at = ?
        WHERE id = ?
    """, (datetime.now(timezone.utc).isoformat(), account_id))
    return cursor.rowcount > 0

def create_transaction(db: sqlite3.Connection, account_id: str, transaction_type: str, amount: float, new_balance: float) -> dict[str, Any]:
    transaction_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    db.execute("""
        INSERT INTO transactions (id, account_id, transaction_type, amount, new_balance, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (transaction_id, account_id, transaction_type, amount, new_balance, timestamp))
    cursor = db.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
    row = cursor.fetchone()
    return dict(row)

def deposit(db: sqlite3.Connection, account_id: str, amount: float) -> dict[str, Any]:
    account = get_account_by_id(db, account_id)
    if not account:
        raise exceptions.AccountNotFoundException(f"Account with ID {account_id} not found")
    if account['status'] != 'active':
        raise exceptions.InvalidAccountStatusException(f"Account with ID {account_id} is not active")
    new_balance = account['balance'] + amount
    db.execute("UPDATE accounts SET balance = ?, updated_at = ? WHERE id = ?", (new_balance, datetime.now(timezone.utc).isoformat(), account_id))
    return create_transaction(db, account_id, 'deposit', amount, new_balance)

def withdraw(db: sqlite3.Connection, account_id: str, amount: float) -> dict[str, Any]:
    account = get_account_by_id(db, account_id)
    if not account:
        raise exceptions.AccountNotFoundException(f"Account with ID {account_id} not found")
    if account['status'] != 'active':
        raise exceptions.InvalidAccountStatusException(f"Account with ID {account_id} is not active")
    if account['balance'] < amount:
        raise exceptions.InsufficientFundsException(f"Account with ID {account_id} has insufficient funds")
    new_balance = account['balance'] - amount
    db.execute("UPDATE accounts SET balance = ?, updated_at = ? WHERE id = ?", (new_balance, datetime.now(timezone.utc).isoformat(), account_id))
    return create_transaction(db, account_id, 'withdrawal', amount, new_balance)

def transfer(db: sqlite3.Connection, source_account_id: str, target_account_id: str, amount: float) -> dict[str, Any]:
    source_account = get_account_by_id(db, source_account_id)
    target_account = get_account_by_id(db, target_account_id)
    if not source_account or not target_account:
        raise exceptions.AccountNotFoundException(f"One or both accounts not found")
    if source_account['status'] != 'active':
        raise exceptions.InvalidAccountStatusException(f"Source account with ID {source_account_id} is not active")
    if target_account['status'] != 'active':
        raise exceptions.InvalidAccountStatusException(f"Target account with ID {target_account_id} is not active")
    if source_account['balance'] < amount:
        raise exceptions.InsufficientFundsException(f"Source account with ID {source_account_id} has insufficient funds")
    new_source_balance = source_account['balance'] - amount
    new_target_balance = target_account['balance'] + amount
    db.execute("UPDATE accounts SET balance = ?, updated_at = ? WHERE id = ?", (new_source_balance, datetime.now(timezone.utc).isoformat(), source_account_id))
    db.execute("UPDATE accounts SET balance = ?, updated_at = ? WHERE id = ?", (new_target_balance, datetime.now(timezone.utc).isoformat(), target_account_id))
    create_transaction(db, source_account_id, 'transfer_out', amount, new_source_balance)
    return create_transaction(db, target_account_id, 'transfer_in', amount, new_target_balance)

def get_transactions_by_account_id(
        db: sqlite3.Connection,
        account_id: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        transaction_type: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None) -> list[dict[str, Any]]:
    account = get_account_by_id(db, account_id)
    if not account:
        raise exceptions.AccountNotFoundException(f"Account with ID {account_id} not found")
    cursor = db.execute("""
                        SELECT * FROM transactions
                        WHERE account_id = ?
                        AND (? IS NULL OR timestamp >= ?)
                        AND (? IS NULL OR timestamp <= ?)
                        AND (? IS NULL OR transaction_type = ?)
                        AND (? IS NULL OR amount >= ?)
                        AND (? IS NULL OR amount <= ?)
                        ORDER BY timestamp DESC
                        """,
                        (account_id,
                         date_from, date_from,
                         date_to, date_to,
                         transaction_type, transaction_type,
                         min_amount, min_amount,
                         max_amount, max_amount))
    return [dict(row) for row in cursor.fetchall()]