from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_users():
    """
    TODO: Return all users (admin only).
    Supports filtering by role (admin / manager / sales_rep).
    """
    return {"message": "list users stub — not yet implemented"}


@router.get("/{user_id}")
def get_user(user_id: str):
    """
    TODO: Return a single user by UUID.
    """
    return {"message": f"get user {user_id} stub — not yet implemented"}


@router.patch("/{user_id}")
def update_user(user_id: str):
    """
    TODO: Update full_name, role, or is_active for a user.
    Admin only for role changes.
    """
    return {"message": f"update user {user_id} stub — not yet implemented"}


@router.delete("/{user_id}")
def deactivate_user(user_id: str):
    """
    TODO: Soft-delete — set is_active = False rather than
    actually deleting the row (preserves audit history).
    """
    return {"message": f"deactivate user {user_id} stub — not yet implemented"}
