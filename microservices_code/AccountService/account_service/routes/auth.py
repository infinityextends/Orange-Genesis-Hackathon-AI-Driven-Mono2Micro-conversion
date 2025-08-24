from fastapi import APIRouter, HTTPException
from account_service.models.account import Account, AccountLogin
from account_service.daos.account_dao import AccountDAO

router = APIRouter(
    prefix="/accounts",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

account_dao = AccountDAO()


@router.post("/login", response_model=Account)
async def login(account_login: AccountLogin):
    """
    Authenticate user and return account details.
    """
    account = account_dao.authenticate(account_login.username, account_login.password)
    if not account:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return account


@router.post("/register", response_model=Account)
async def register(account: Account):
    """
    Register a new user account.
    """
    existing_account = account_dao.get_by_username(account.username)
    if existing_account:
        raise HTTPException(status_code=400, detail="Username already exists")
    return account_dao.create(account)
