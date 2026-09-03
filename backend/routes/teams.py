from fastapi import APIRouter
from pydantic import BaseModel
from database.databricks import get_connection

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)


class TeamRequest(BaseModel):
    team_name: str
    project_id: str
    team_leader_id: str
    max_size: int = 5


class TeamMemberRequest(BaseModel):
    user_id: str
    team_role: str = "MEMBER"


@router.get("/{team_id}")
def get_team(team_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
        SELECT
            team_id,
            project_id,
            team_name,
            team_leader_id,
            max_size,
            current_size,
            status
        FROM workspace.default.teams
        WHERE team_id = ?
        """

        cursor.execute(query, (team_id,))
        row = cursor.fetchone()

        if not row:
            return {
                "success": False,
                "message": "Team not found",
                "data": {
                    "team_id": team_id
                }
            }

        team = {
            "team_id": row[0],
            "project_id": row[1],
            "team_name": row[2],
            "team_leader_id": row[3],
            "max_size": row[4],
            "current_size": row[5],
            "status": row[6]
        }

        return {
            "success": True,
            "message": "Team retrieved successfully",
            "data": team
        }

    finally:
        cursor.close()
        connection.close()