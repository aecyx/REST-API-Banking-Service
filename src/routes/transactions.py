import src.database.queries as queries
import src.models.schemas as schemas
import src.exceptions as exceptions
from typing import Optional
from fastapi import APIRouter, HTTPException
from src.database.connection import get_db_connection

router = APIRouter(prefix="/accounts", tags=["transactions"])

@router.post("/{account_id}/deposit", response_model=schemas.TransactionResponse)
def deposit(account_id: str, deposit_request: schemas.DepositRequest):
    with get_db_connection() as db:
        try:
            transaction = queries.deposit(db, account_id, deposit_request.amount)
        except exceptions.AccountNotFoundException:
            raise HTTPException(status_code=404, detail="Account not found")
        except exceptions.InvalidAccountStatusException:
            raise HTTPException(status_code=409, detail="Invalid account status")
        except exceptions.InsufficientFundsException:
            raise HTTPException(status_code=409, detail="Insufficient funds")
    return transaction

@router.post("/{account_id}/withdrawal", response_model=schemas.TransactionResponse)
def withdrawal(account_id: str, withdrawal_request: schemas.WithdrawalRequest):
    with get_db_connection() as db:
        try:
            transaction = queries.withdraw(db, account_id, withdrawal_request.amount)
        except exceptions.AccountNotFoundException:
            raise HTTPException(status_code=404, detail="Account not found")
        except exceptions.InvalidAccountStatusException:
            raise HTTPException(status_code=409, detail="Invalid account status")
        except exceptions.InsufficientFundsException:
            raise HTTPException(status_code=409, detail="Insufficient funds")
    return transaction

@router.get("/{account_id}/transactions", response_model=list[schemas.TransactionResponse])
def get_transactions(
    account_id: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    transaction_type: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None
):
    with get_db_connection() as db:
        try:
            transactions = queries.get_transactions_by_account_id(
                db,
                account_id,
                date_from,
                date_to,
                transaction_type,
                min_amount,
                max_amount
            )
        except exceptions.AccountNotFoundException:
            raise HTTPException(status_code=404, detail="Account not found")
        return transactions