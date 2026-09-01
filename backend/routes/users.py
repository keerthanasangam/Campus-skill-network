from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{user_id}")
def get_user(user_id: str):

    return {
        "success": True,
        "message": "User profile retrieved successfully",
        "data": {
            "user_id": user_id
        }
    }