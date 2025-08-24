from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class AccountBase(BaseModel):
    username: str = Field(..., min_length=4, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None

class AccountCreate(AccountBase):
    password: str = Field(..., min_length=8)


class AccountUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class Account(AccountBase):
    id: int
    disabled: bool = False


class AccountLogin(BaseModel):
    username: str
    password: str
