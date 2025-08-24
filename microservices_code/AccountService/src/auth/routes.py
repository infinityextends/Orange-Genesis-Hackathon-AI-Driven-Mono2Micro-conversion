from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.models import Token, User
from src.auth.service import AuthService  # Import the service

auth_router = APIRouter(
    prefix="/accounts",
    tags=["auth"],
)

# Dependency
def get_auth_service() -> AuthService:
    return AuthService()  # Instantiate the AuthService

@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    """Authenticates a user and returns a JWT token."""
    user = auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/register", response_model=User)
async def register(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    """Registers a new user."""
    user = auth_service.register_user(form_data.username, form_data.password)
    return user
