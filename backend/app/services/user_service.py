from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

# ─── What is a Service? ───────────────────────────────────────────────────────
#
# The service layer sits between your API endpoints and the database.
# Endpoints handle HTTP (requests, responses, status codes).
# Services handle BUSINESS LOGIC (what actually happens to the data).
#
# This separation means:
# - Your endpoints stay thin and readable
# - Your business logic can be tested without HTTP
# - If you ever switch from FastAPI to something else, the logic is reusable
#
# Think of it like a restaurant again:
#   Endpoint = waiter (takes the order, delivers the food)
#   Service  = chef (actually prepares it)
# ─────────────────────────────────────────────────────────────────────────────


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Look up a user by email address.
    Returns the User object if found, None if not.

    Used during login to find who's trying to authenticate.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """
    Look up a user by their UUID.
    Used when decoding a JWT to load the full user profile.
    """
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create a new user in the database.

    Steps:
    1. Hash the plain text password (NEVER store it raw)
    2. Create a User model instance with the hashed password
    3. Add it to the session (queued for insert)
    4. Commit the transaction (actually writes to DB)
    5. Refresh to get the generated id, created_at, etc.
    6. Return the full User object
    """
    db_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),  # ← hash here, never store plain
        full_name=user_in.full_name,
        role=user_in.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # re-reads the row from DB so we get the auto-generated fields
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Verify a login attempt. Returns the User if credentials are valid, None if not.

    This is the core of the login flow:
    1. Find the user by email
    2. If not found → fail (but don't say "email not found" — that leaks info)
    3. Compare the submitted password against the stored hash
    4. If match → return the user
    5. If no match → return None

    Note: We never tell the client WHETHER the email or the password was wrong.
    Always say "invalid credentials" — otherwise an attacker can enumerate
    valid email addresses by watching which error they get.
    """
    from app.core.security import verify_password

    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_all_users(db: Session) -> list[User]:
    """Return all users. Admin-only endpoint will call this."""
    return db.query(User).filter(User.is_active == True).all()
