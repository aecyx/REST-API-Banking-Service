import src.database.queries as queries
import src.models.schemas as schemas
import src.exceptions as exceptions
from fastapi import APIRouter, HTTPException
from src.database.connection import get_db_connection

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/", status_code=201, response_model=schemas.AccountResponse)
def create_account(account_data: schemas.AccountCreate):
    with get_db_connection() as db:
        account = queries.create_account(db, account_data)
        return account

@router.get("/{account_id}", response_model=schemas.AccountResponse)
def get_account(account_id: str):
    with get_db_connection() as db:
        account = queries.get_account_by_id(db, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

@router.get("/", response_model=schemas.PaginatedAccounts)
def list_accounts(limit: int = 10, offset: int = 0):
    with get_db_connection() as db:
        accounts, total = queries.get_accounts(db, limit, offset)
        return schemas.PaginatedAccounts(accounts=[schemas.AccountResponse.model_validate(account) for account in accounts], total=total, limit=limit, offset=offset)

@router.put("/{account_id}", response_model=schemas.AccountResponse)
def update_account(account_id: str, update_data: schemas.AccountUpdate):
    with get_db_connection() as db:
        try:
            queries.update_account(db, account_id, update_data)
        except exceptions.AccountNotFoundException:
            raise HTTPException(status_code=404, detail="Account not found")
        except exceptions.NoFieldsToUpdateException:
            raise HTTPException(status_code=400, detail="No fields to update")
        account = queries.get_account_by_id(db, account_id)
        return account

@router.delete("/{account_id}", status_code=204)
def delete_account(account_id: str):
    with get_db_connection() as db:
        account = queries.get_account_by_id(db, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        if not queries.deactivate_account(db, account_id):
            raise HTTPException(status_code=400, detail="Failed to deactivate account")
        return None