from fastapi import APIRouter
from database.databricks import get_connection

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.get("/{opportunity_id}")
def get_recommendations(opportunity_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
        SELECT
            u.user_id,
            u.full_name,
            s.skill_name
        FROM workspace.default.users u
        JOIN workspace.default.user_skills us
            ON u.user_id = us.user_id
        JOIN workspace.default.skills s
            ON us.skill_id = s.skill_id
        JOIN workspace.default.opportunity_skills os
            ON us.skill_id = os.skill_id
        WHERE os.opportunity_id = ?
          AND u.account_status = 'ACTIVE'
          AND u.availability_status = 'LOOKING_FOR_TEAM'
        ORDER BY u.user_id
        """

        cursor.execute(query, (opportunity_id,))
        rows = cursor.fetchall()

        # Group matching skills by user
        users = {}

        for row in rows:
            user_id = row[0]
            name = row[1]
            skill = row[2]

            if user_id not in users:
                users[user_id] = {
                    "user_id": user_id,
                    "name": name,
                    "matching_skills": []
                }

            users[user_id]["matching_skills"].append(skill)

        recommendations = []

        for user in users.values():

            matching_count = len(user["matching_skills"])

            # Simple matching score
            match_score = min(100, matching_count * 25)

            recommendations.append({
                "user_id": user["user_id"],
                "name": user["name"],
                "match_score": match_score,
                "matching_skills": user["matching_skills"],
                "reason": (
                    f"Matches {matching_count} required skill(s) "
                    f"for this opportunity."
                )
            })

        # Highest match first
        recommendations.sort(
            key=lambda x: x["match_score"],
            reverse=True
        )

        if not recommendations:
            return {
                "success": False,
                "message": "No recommendations found",
                "data": {
                    "opportunity_id": opportunity_id,
                    "recommendations": []
                }
            }

        return {
            "success": True,
            "message": "Recommendations retrieved successfully",
            "data": {
                "opportunity_id": opportunity_id,
                "recommendations": recommendations
            }
        }

    finally:
        cursor.close()
        connection.close()