from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from src.auth.models import User
from src.accounts.models import AccountCreate
from passlib.context import CryptContext

# to get auto completion
from typing import Optional

# This can be set in the .env file
SECRET_KEY = "09d25e094faa6ca25563b9ac81dd345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        # Ideally, you'd inject dependencies like a database connection here
        pass

    def authenticate_user(self, username, password):
        """Authenticates a user. Placeholder implementation."""
        # This is a simplified example. In a real app, you'd:
        # 1. Query a database to find the user by username.
        # 2. Verify the password hash against the stored hash.

        # Dummy user for demonstration
        if username == "testuser":
            # Verify Password
            if not self.verify_password(password, "$2b$12$d60a9MuFFxPzBzE2W1W3Lu1k8QG/0RWHmKjmwOxWzUUmWqYpI9/d6"):
                return None
            return User(username="testuser", full_name="Test User", email="test@example.com")
        return None

    def register_user(self, username, password):
        """Registers a new user. Placeholder implementation."""
        # In a real application, you would:
        # 1. Check if the username already exists.
        # 2. Hash the password.
        # 3. Store the user in the database.

        # For now, let's just hash the password and return a dummy user
        hashed_password = self.get_password_hash(password)
        print(f"User {username} registered with password {hashed_password} (placeholder)")
        return User(username=username, full_name="New User", email="new@example.com")

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Creates a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
