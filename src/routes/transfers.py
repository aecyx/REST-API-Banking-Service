import src.database.queries as queries
import src.models.schemas as schemas
import src.exceptions as exceptions
from fastapi import APIRouter, HTTPException
from src.database.connection import get_db_connection

router = APIRouter(prefix="/transfers", tags=["transfers"])

@router.post("", response_model=schemas.TransactionResponse, status_code=201)
def transfer(transfer_request: schemas.TransferRequest):
    with get_db_connection() as db:
        try:
            transaction = queries.transfer(db, transfer_request.source_account_id, transfer_request.target_account_id, transfer_request.amount)
        except exceptions.AccountNotFoundException:
            raise HTTPException(status_code=404, detail="Account not found")
        except exceptions.InvalidAccountStatusException:
            raise HTTPException(status_code=409, detail="Invalid account status")
        except exceptions.InsufficientFundsException:
            raise HTTPException(status_code=409, detail="Insufficient funds")
    return transaction
