from fastapi import APIRouter, HTTPException
from account_service.models import AccountLogin
from account_service.routes import accounts  # Import accounts module for DB lookup

router = APIRouter(
    prefix="/accounts/login",
    tags=["login"],
    responses={401: {"description": "Authentication failed"}},
)

# Placeholder function for user authentication
def authenticate_user(account: AccountLogin):
    # In a real implementation, this would:
    # 1. Retrieve the user from the database using AccountDao
    # 2. Verify the password against the stored hash.

    db_account = accounts.get_account_from_db(account.username)

    if db_account and db_account.password == account.password:  # Simplified comparison
        return True
    else:
        return False


@router.post("/")
async def login(account: AccountLogin):
    """
    Authenticate user credentials.
    """
    if authenticate_user(account):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
