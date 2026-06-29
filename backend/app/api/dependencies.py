from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.services.user_service import get_user_by_email

# ─── What is a FastAPI Dependency? ────────────────────────────────────────────
#
# A dependency is a function FastAPI runs BEFORE your endpoint function.
# You declare it with `Depends(some_function)` in your route parameters.
#
# Think of it as a checkpoint:
#   Request comes in
#       → FastAPI runs get_current_user()
#           → if it fails, request is rejected with 401
#           → if it passes, the User object is injected into your endpoint
#
# This means you write the "who is this person?" logic ONCE and reuse it
# across every protected endpoint — no copy-pasting.
# ─────────────────────────────────────────────────────────────────────────────

# OAuth2PasswordBearer tells FastAPI:
# "Look for a Bearer token in the Authorization header"
# e.g.  Authorization: Bearer eyJhbGci...
#
# The tokenUrl tells Swagger UI where to get a token (for the "Authorize" button)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Decode the JWT, look up the user, and return them.
    Raises HTTP 401 if the token is missing, invalid, or expired.

    Add `current_user: User = Depends(get_current_user)` to any endpoint
    that requires authentication.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = decode_access_token(token)
    if email is None:
        raise credentials_exception

    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Like get_current_user but also checks the account isn't deactivated.
    Use this on most endpoints.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )
    return current_user


def require_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Only allows admins through. Use on admin-only endpoints.

    Example:
        @router.delete("/{user_id}")
        def delete_user(user_id: str, _: User = Depends(require_admin)):
            ...
    """
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def require_manager_or_above(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Allows managers and admins. Blocks sales reps."""
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager or admin access required",
        )
    return current_user
