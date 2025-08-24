from fastapi import APIRouter, HTTPException
from account_service.models import AccountCreate, Account

router = APIRouter(
    prefix="/accounts/register",
    tags=["register"],
    responses={400: {"description": "Invalid input"}},
)

# Placeholder function for registering a new user
def register_new_user(account: AccountCreate):
    # In a real implementation, this would:
    # 1. Validate the input (e.g., using AccountValidator)
    # 2. Hash the password
    # 3. Store the account in the database using AccountDao

    # Dummy implementation - just returns a new Account object
    return Account(username=account.username, password="hashed_password", email=account.email)


@router.post("/", response_model=Account)
async def register_account(account: AccountCreate):
    """
    Register a new user account.
    """
    try:
        new_account = register_new_user(account)  # Call registration function
        return new_account
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
