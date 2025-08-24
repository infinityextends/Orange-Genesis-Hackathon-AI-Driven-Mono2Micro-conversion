from pydantic import BaseModel

class Account(BaseModel):
    username: str
    password: str
    email: str

class AccountCreate(BaseModel):
    username: str
    password: str
    email: str

class AccountLogin(BaseModel):
    username: str
    password: str
