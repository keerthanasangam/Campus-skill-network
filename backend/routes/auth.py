from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field

from database.databricks import get_connection

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class AuthRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


@router.post("/signup")
def signup(user: AuthRequest):

    return {
        "success": True,
        "message": "Signup request received successfully",
        "data": {
            "email": user.email
        }
    }


@router.post("/login")
def login(user: AuthRequest):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
        SELECT user_id, full_name, email, role
        FROM workspace.default.users
        WHERE LOWER(email) = LOWER(?)
        AND account_status = 'ACTIVE'
        """

        cursor.execute(query, (user.email,))
        row = cursor.fetchone()

        # User does not exist
        if not row:
            return {
                "success": False,
                "message": "Invalid email or password",
                "data": None
            }

        # Temporary hackathon authentication:
        # The users table currently has no password column.
        # Therefore we only verify that the email belongs
        # to an active user.
        
        return {
            "success": True,
            "message": "Login successful",
            "data": {
                "user_id": row[0],
                "full_name": row[1],
                "email": row[2],
                "role": row[3]
            }
        }

    finally:
        cursor.close()
        connection.close()