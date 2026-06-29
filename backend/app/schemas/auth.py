from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin, UserOut
from app.services.user_service import authenticate_user, create_user, get_user_by_email
from app.core.security import create_access_token

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.

    Flow:
    1. Check the email isn't already registered
    2. Hash the password
    3. Write the user to the DB
    4. Return the new user (without the password hash)
    """
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists",
        )

    user = create_user(db, user_in)
    return user


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Log in and receive a JWT access token.

    Flow:
    1. Find the user by email
    2. Verify the password against the stored hash
    3. If valid, create and return a signed JWT
    4. If invalid, return 401 (same message whether email or password was wrong)
    """
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.email)
    return Token(access_token=access_token)


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_active_user)):
    """
    Return the currently logged-in user's profile.

    The heavy lifting is done by the `get_current_active_user` dependency:
    - Reads the JWT from the Authorization header
    - Decodes and validates it
    - Fetches the user from the DB
    - Passes them in as `current_user`

    This endpoint itself just returns what it receives.
    That's intentional — keep endpoints thin.
    """
    return current_user


@router.post("/logout")
def logout():
    """
    JWT logout note:

    JWTs are stateless — the server doesn't store them, so there's nothing
    to "invalidate" server-side. The standard approach is:

    Option A (simple): Short expiry (we use 24h). Token expires on its own.
    Option B (robust): Maintain a token blocklist in Redis. On logout, add
                       the token's JTI (unique ID) to the blocklist and check
                       it on every request. We can add this later.

    For now, the frontend just deletes the token from localStorage.
    """
    return {"message": "Logged out. Delete your token on the client side."}
