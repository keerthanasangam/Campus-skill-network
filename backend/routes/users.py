from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from database.databricks import get_connection


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# =========================
# GET USER PROFILE
# =========================

@router.get("/{user_id}")
def get_user(user_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
        SELECT
            user_id,
            full_name,
            email,
            role,
            institution,
            education_level,
            program,
            department,
            admission_year,
            graduation_year,
            current_year,
            experience_level,
            availability_status,
            account_status,
            bio
        FROM workspace.default.users
        WHERE user_id = ?
        """

        cursor.execute(query, (user_id,))
        row = cursor.fetchone()

        if not row:
            return {
                "success": False,
                "message": "User not found",
                "data": {
                    "user_id": user_id
                }
            }

        user = {
            "user_id": row[0],
            "full_name": row[1],
            "email": row[2],
            "role": row[3],
            "institution": row[4],
            "education_level": row[5],
            "program": row[6],
            "department": row[7],
            "admission_year": row[8],
            "graduation_year": row[9],
            "current_year": row[10],
            "experience_level": row[11],
            "availability_status": row[12],
            "account_status": row[13],
            "bio": row[14]
        }

        return {
            "success": True,
            "message": "User profile retrieved successfully",
            "data": user
        }

    finally:
        cursor.close()
        connection.close()


# =========================
# USER PROFILE UPDATE MODEL
# =========================

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    institution: Optional[str] = None
    department: Optional[str] = None
    current_year: Optional[int] = None
    availability_status: Optional[str] = None
    bio: Optional[str] = None


# =========================
# UPDATE USER PROFILE
# =========================

@router.put("/{user_id}")
def update_user(user_id: str, profile: UserProfileUpdate):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Check whether user exists
        cursor.execute(
            """
            SELECT user_id
            FROM workspace.default.users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        row = cursor.fetchone()

        if not row:
            return {
                "success": False,
                "message": "User not found",
                "data": {
                    "user_id": user_id
                }
            }

        # Update profile
        query = """
        UPDATE workspace.default.users
        SET
            full_name = ?,
            institution = ?,
            department = ?,
            current_year = ?,
            availability_status = ?,
            bio = ?
        WHERE user_id = ?
        """

        cursor.execute(
            query,
            (
                profile.full_name,
                profile.institution,
                profile.department,
                profile.current_year,
                profile.availability_status,
                profile.bio,
                user_id
            )
        )

        return {
            "success": True,
            "message": "User profile updated successfully",
            "data": {
                "user_id": user_id,
                "full_name": profile.full_name,
                "institution": profile.institution,
                "department": profile.department,
                "current_year": profile.current_year,
                "availability_status": profile.availability_status,
                "bio": profile.bio
            }
        }

    finally:
        cursor.close()
        connection.close()

        # =========================
# ADD USER SKILL
# =========================

class UserSkillRequest(BaseModel):
    skill_id: str
    proficiency_level: Optional[str] = "BEGINNER"
    years_experience: Optional[float] = 0.0


@router.post("/{user_id}/skills")
def add_user_skill(user_id: str, skill: UserSkillRequest):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Check if user exists
        cursor.execute(
            """
            SELECT user_id
            FROM workspace.default.users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            return {
                "success": False,
                "message": "User not found",
                "data": {
                    "user_id": user_id
                }
            }

        # Check if skill exists
        cursor.execute(
            """
            SELECT skill_id, skill_name
            FROM workspace.default.skills
            WHERE skill_id = ?
            """,
            (skill.skill_id,)
        )

        skill_row = cursor.fetchone()

        if not skill_row:
            return {
                "success": False,
                "message": "Skill not found",
                "data": {
                    "skill_id": skill.skill_id
                }
            }

        # Check whether user already has this skill
        cursor.execute(
            """
            SELECT user_skill_id
            FROM workspace.default.user_skills
            WHERE user_id = ?
              AND skill_id = ?
            """,
            (user_id, skill.skill_id)
        )

        existing = cursor.fetchone()

        if existing:
            return {
                "success": False,
                "message": "User already has this skill",
                "data": {
                    "user_id": user_id,
                    "skill_id": skill.skill_id
                }
            }

        # Generate user skill ID
        user_skill_id = f"US_{user_id}_{skill.skill_id}"

        # Insert skill
        cursor.execute(
            """
            INSERT INTO workspace.default.user_skills
            (
                user_skill_id,
                user_id,
                skill_id,
                proficiency_level,
                years_experience,
                is_verified
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_skill_id,
                user_id,
                skill.skill_id,
                skill.proficiency_level,
                skill.years_experience,
                False
            )
        )

        return {
            "success": True,
            "message": "Skill added successfully",
            "data": {
                "user_skill_id": user_skill_id,
                "user_id": user_id,
                "skill_id": skill.skill_id,
                "skill_name": skill_row[1],
                "proficiency_level": skill.proficiency_level,
                "years_experience": skill.years_experience,
                "is_verified": False
            }
        }

    finally:
        cursor.close()
        connection.close()