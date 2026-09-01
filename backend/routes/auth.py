from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field

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

    return {
        "success": True,
        "message": "Login request received successfully",
        "data": {
            "email": user.email
        }
    }