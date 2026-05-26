from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class AccountCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    account_type: Literal['checking', 'savings', 'investment']
    initial_balance: float = Field(0.0, ge=0.0)

class AccountUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[Literal['active', 'inactive']] = None

class AccountResponse(BaseModel):
    id: str
    name: str
    account_type: str
    balance: float
    status: str
    created_at: datetime
    updated_at: datetime
    
class PaginatedAccounts(BaseModel):
    accounts: list[AccountResponse]
    total: int
    limit: int
    offset: int

class DepositRequest(BaseModel):
    amount: float = Field(..., gt=0.0)

class WithdrawalRequest(BaseModel):
    amount: float = Field(..., gt=0.0)

class TransferRequest(BaseModel):
    source_account_id: str
    target_account_id: str
    amount: float = Field(..., gt=0.0)

class TransactionResponse(BaseModel):
    id: str
    account_id: str
    transaction_type: str
    amount: float
    new_balance: float
    timestamp: datetime