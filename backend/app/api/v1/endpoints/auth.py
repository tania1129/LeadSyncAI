from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
def login():
    """
    TODO: Accept email + password, verify against DB,
    return a signed JWT access token.
    """
    return {"message": "login stub — not yet implemented"}


@router.post("/register")
def register():
    """
    TODO: Accept new user details, hash the password,
    create a user row, return the created user.
    """
    return {"message": "register stub — not yet implemented"}


@router.post("/logout")
def logout():
    """
    TODO: Invalidate the token (e.g. add to a blocklist or
    rely on short expiry). For now JWTs are stateless.
    """
    return {"message": "logout stub — not yet implemented"}


@router.get("/me")
def get_current_user():
    """
    TODO: Decode the JWT from the Authorization header,
    look up the user in the DB, return their profile.
    """
    return {"message": "me stub — not yet implemented"}
