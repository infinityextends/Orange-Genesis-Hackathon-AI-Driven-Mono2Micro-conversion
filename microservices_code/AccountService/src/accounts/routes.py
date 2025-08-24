from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

from src.accounts.models import Account, AccountCreate, AccountUpdate
from src.accounts.service import AccountService  # Import the service

accounts_router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)


# Dependency
def get_account_service() -> AccountService:
    return AccountService()  # Instantiate the AccountService

@accounts_router.post("", response_model=Account, status_code=status.HTTP_201_CREATED)
async def create_account(account: AccountCreate, account_service: AccountService = Depends(get_account_service)):
    """Creates a new user account."""
    return account_service.create_account(account)

@accounts_router.get("", response_model=List[Account])
async def list_accounts(account_service: AccountService = Depends(get_account_service)):
    """Retrieves all user accounts."""
    return account_service.get_accounts()


@accounts_router.get("/{account_id}", response_model=Account)
async def get_account(account_id: int, account_service: AccountService = Depends(get_account_service)):
    """Retrieves a specific user account by ID."""
    account = account_service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account

@accounts_router.put("/{account_id}", response_model=Account)
async def update_account(account_id: int, account: AccountUpdate, account_service: AccountService = Depends(get_account_service)):
    """Updates a user account."""
    existing_account = account_service.get_account(account_id)
    if not existing_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    updated_account = account_service.update_account(account_id, account)
    return updated_account

@accounts_router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(account_id: int, account_service: AccountService = Depends(get_account_service)):
    """Deletes a user account."""
    existing_account = account_service.get_account(account_id)
    if not existing_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    account_service.delete_account(account_id)
    return
