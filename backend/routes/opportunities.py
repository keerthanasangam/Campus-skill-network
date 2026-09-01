from fastapi import APIRouter

router = APIRouter(
    prefix="/opportunities",
    tags=["Opportunities"]
)


# Temporary sample data
opportunities = [
    {
        "opportunity_id": "H001",
        "title": "AI Innovation Challenge",
        "description": "Build an AI-powered solution for a real-world problem.",
        "required_skills": ["Python", "Machine Learning", "Databricks"],
        "deadline": "2026-09-15",
        "team_size": "3-5"
    },
    {
        "opportunity_id": "H002",
        "title": "Smart Campus Hackathon",
        "description": "Create a technology solution to improve campus life.",
        "required_skills": ["React", "Python", "UI/UX"],
        "deadline": "2026-09-20",
        "team_size": "2-4"
    },
    {
        "opportunity_id": "H003",
        "title": "Data Science Challenge",
        "description": "Use data and AI to solve a meaningful problem.",
        "required_skills": ["Python", "SQL", "Data Science"],
        "deadline": "2026-09-25",
        "team_size": "3-4"
    }
]


@router.get("/")
def get_opportunities():

    return {
        "success": True,
        "message": "Opportunities retrieved successfully",
        "data": {
            "count": len(opportunities),
            "opportunities": opportunities
        }
    }


@router.get("/{opportunity_id}")
def get_opportunity(opportunity_id: str):

    for opportunity in opportunities:
        if opportunity["opportunity_id"] == opportunity_id:

            return {
                "success": True,
                "message": "Opportunity retrieved successfully",
                "data": opportunity
            }

    return {
        "success": False,
        "message": "Opportunity not found",
        "data": {
            "opportunity_id": opportunity_id
        }
    }