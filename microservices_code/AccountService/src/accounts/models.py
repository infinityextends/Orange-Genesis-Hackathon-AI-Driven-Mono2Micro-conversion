from pydantic import BaseModel
from typing import Optional

class Account(BaseModel):
    account_id: int
    username: str
    email: str
    full_name: str
    disabled: Optional[bool] = None

class AccountCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str

class AccountUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None
