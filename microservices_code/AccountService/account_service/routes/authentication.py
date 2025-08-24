from fastapi import APIRouter, HTTPException, status
from account_service.models.account import Account, AccountCreate, AccountLogin

router = APIRouter(
    prefix="/accounts",
    tags=["authentication"],
)

# Placeholder user database (replace with actual database interaction)
users = {}

@router.post("/register", response_model=Account, status_code=status.HTTP_201_CREATED)
async def register_user(account: AccountCreate):
    """Registers a new user."""
    if account.username in users:
        raise HTTPException(status_code=400, detail="Username already registered")
    # In a real application, hash the password before storing
    users[account.username] = account.password
    return Account(id=len(users), username=account.username, email=account.email, full_name=account.full_name, disabled=False)


@router.post("/authenticate")
async def authenticate_user(account: AccountLogin):
    """Authenticates a user."""
    if account.username not in users or users[account.username] != account.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": "example_token", "token_type": "bearer"}  # Replace with actual token generation
