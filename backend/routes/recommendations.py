from fastapi import APIRouter

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


# Temporary sample recommendations
recommendations = {
    "H001": [
        {
            "user_id": "U004",
            "name": "Ananya",
            "match_score": 94,
            "matching_skills": [
                "Python",
                "Machine Learning"
            ],
            "reason": "Strong Python and Machine Learning skills with relevant project experience."
        },
        {
            "user_id": "U007",
            "name": "Rahul",
            "match_score": 88,
            "matching_skills": [
                "Python",
                "Databricks"
            ],
            "reason": "Good Databricks experience and currently available for collaboration."
        }
    ],

    "H002": [
        {
            "user_id": "U002",
            "name": "Priya",
            "match_score": 91,
            "matching_skills": [
                "React",
                "UI/UX"
            ],
            "reason": "Strong frontend and UI/UX skills that complement the project requirements."
        }
    ],

    "H003": [
        {
            "user_id": "U006",
            "name": "Arjun",
            "match_score": 93,
            "matching_skills": [
                "Python",
                "SQL",
                "Data Science"
            ],
            "reason": "Strong Data Science and SQL background suitable for this challenge."
        }
    ]
}

@router.get("/{opportunity_id}")
def get_recommendations(opportunity_id: str):

    if opportunity_id not in recommendations:
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
            "recommendations": recommendations[opportunity_id]
        }
    }