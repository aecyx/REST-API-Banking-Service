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