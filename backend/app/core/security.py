from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# ─── Password Hashing ─────────────────────────────────────────────────────────
#
# CryptContext tells passlib WHICH algorithm to use.
# "bcrypt" is the industry standard for passwords — it's intentionally slow
# so that brute-forcing millions of guesses takes years instead of seconds.
#
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    Turn a plain text password into a bcrypt hash.
    Called once when a user registers. The result is what gets stored in the DB.

    Example:
        hash_password("mypassword123")
        → "$2b$12$eW5KrST1jP8vX3Qz2Nm7Pu..."
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if a plain password matches a stored hash.
    Called every time a user tries to log in.

    Never compares plain text to plain text.
    Never stores the plain text password anywhere.

    Example:
        verify_password("mypassword123", "$2b$12$eW5K...") → True
        verify_password("wrongpassword", "$2b$12$eW5K...") → False
    """
    return pwd_context.verify(plain_password, hashed_password)


# ─── JWT Tokens ───────────────────────────────────────────────────────────────
#
# A JWT has three parts: header.payload.signature
#
# The PAYLOAD is a dict (called "claims") that we choose.
# We store the user's email in "sub" (subject) and an expiry in "exp".
#
# The SIGNATURE is created by hashing the header+payload with our SECRET_KEY.
# Anyone can READ a JWT (it's just base64), but they can't FORGE one without
# knowing the secret key.
#


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a signed JWT access token.

    Args:
        subject: Usually the user's email or user ID — identifies WHO this token belongs to.
        expires_delta: How long until the token expires. Defaults to the setting in config.

    Returns:
        A signed JWT string to send to the client.
    """
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": subject,   # "sub" = subject (who this token is for)
        "exp": expire,    # "exp" = expiry (when this token stops working)
        "iat": datetime.utcnow(),  # "iat" = issued at (when this token was created)
    }

    # jwt.encode signs the payload with our SECRET_KEY using the ALGORITHM (HS256)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    """
    Decode and verify a JWT token.

    Returns the subject (user email) if valid, None if invalid or expired.

    This is called on every protected route to identify the current user.
    The library automatically checks the expiry — expired tokens are rejected.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        subject: str = payload.get("sub")
        return subject
    except JWTError:
        # JWTError covers: bad signature, expired token, malformed token
        return None
