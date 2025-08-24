from fastapi import APIRouter, HTTPException, Depends, status
from typing import Optional

from account_service.models.account import Account, AccountCreate, AccountUpdate

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)

# Placeholder database (replace with actual database interaction)
accounts_db = {}
account_id_counter = 1


def get_account_by_username(username: str):
    for account_id in accounts_db:
        if accounts_db[account_id].username == username:
            return accounts_db[account_id]
    return None


@router.post("/", response_model=Account, status_code=status.HTTP_201_CREATED)
async def create_account(account: AccountCreate):
    """
    Creates a new user account.
    """
    global account_id_counter
    if get_account_by_username(account.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    accounts_db[account_id_counter] = new_account
    account_id_counter += 1
    return new_account


@router.get("/", response_model=list[Account])
async def list_accounts():
    """
    Retrieves a list of all user accounts.
    """
    return list(accounts_db.values())


@router.get("/{username}", response_model=Account)
async def get_account(username: str):
    """
    Retrieves a user account by username.
    """
    account = get_account_by_username(username)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


@router.put("/{username}", response_model=Account)
async def update_account(username: str, account_update: AccountUpdate):
    """
    Updates an existing user account.
    """
    account = get_account_by_username(username)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    updated_account = account.copy(update=account_update.dict(exclude_unset=True))

    for account_id in accounts_db:
        if accounts_db[account_id].username == username:
            accounts_db[account_id] = updated_account
            break

    return updated_account


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(username: str):
    """
    Deletes a user account.
    """
    account = get_account_by_username(username)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    for account_id in accounts_db:
        if accounts_db[account_id].username == username:
            del accounts_db[account_id]
            break

    return None
