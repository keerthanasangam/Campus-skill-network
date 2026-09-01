from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)


class TeamRequest(BaseModel):
    team_name: str
    opportunity_id: str
    created_by: str


class TeamMemberRequest(BaseModel):
    user_id: str


# Temporary team storage
teams = []


# Create a team
@router.post("/")
def create_team(team: TeamRequest):

    new_team = {
        "team_id": f"T{len(teams) + 1:03d}",
        "team_name": team.team_name,
        "opportunity_id": team.opportunity_id,
        "created_by": team.created_by,
        "members": [team.created_by]
    }

    teams.append(new_team)

    return {
        "success": True,
        "message": "Team created successfully",
        "data": {
            "team": new_team
        }
    }


# Get a team
@router.get("/{team_id}")
def get_team(team_id: str):

    for team in teams:

        if team["team_id"] == team_id:

            return {
                "success": True,
                "message": "Team retrieved successfully",
                "data": {
                    "team": team
                }
            }

    return {
        "success": False,
        "message": "Team not found",
        "data": {
            "team_id": team_id
        }
    }


# Add team member
@router.post("/{team_id}/members")
def add_team_member(team_id: str, member: TeamMemberRequest):

    for team in teams:

        if team["team_id"] == team_id:

            if member.user_id in team["members"]:

                return {
                    "success": False,
                    "message": "User is already a member of this team",
                    "data": {
                        "team": team
                    }
                }

            team["members"].append(member.user_id)

            return {
                "success": True,
                "message": "Member added successfully",
                "data": {
                    "team": team
                }
            }

    return {
        "success": False,
        "message": "Team not found",
        "data": {
            "team_id": team_id
        }
    }