from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

from app.models.user import UserRole

# ─── What is a Pydantic Schema? ───────────────────────────────────────────────
#
# A schema defines the SHAPE of data at the API boundary.
# It's different from a SQLAlchemy model:
#
#   SQLAlchemy model  → maps to a database table (internal)
#   Pydantic schema   → describes what comes IN or goes OUT via the API (external)
#
# We keep them separate because:
# - We never want to expose `hashed_password` in an API response
# - The fields a user sends to CREATE an account differ from what we return
# - We get free input validation (email format, required fields, etc.)
#
# Naming convention used here:
#   UserCreate  → data the client sends when registering
#   UserLogin   → data the client sends when logging in
#   UserOut     → data we send BACK to the client (safe, no password)
#   Token       → the JWT response after a successful login
# ─────────────────────────────────────────────────────────────────────────────


class UserCreate(BaseModel):
    """What the client sends to POST /auth/register"""
    email: EmailStr          # Pydantic validates email format automatically
    password: str
    full_name: str
    role: Optional[UserRole] = UserRole.sales_rep


class UserLogin(BaseModel):
    """What the client sends to POST /auth/login"""
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """
    What we send back — notice: NO password field.
    The client never needs the hash, and we never want it leaking.
    """
    id: uuid.UUID
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Allows creating this from a SQLAlchemy model object


class UserUpdate(BaseModel):
    """Fields a user (or admin) can update — all optional"""
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class Token(BaseModel):
    """The response body after a successful login"""
    access_token: str
    token_type: str = "bearer"  # "bearer" is the standard OAuth2 token type name


class TokenData(BaseModel):
    """The decoded contents of a JWT — used internally, never sent to client"""
    email: Optional[str] = None
