from fastapi import APIRouter
from database.databricks import get_connection

router = APIRouter(
    prefix="/opportunities",
    tags=["Opportunities"]
)


@router.get("/")
def get_opportunities():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
        SELECT
            o.opportunity_id,
            o.title,
            o.opportunity_type,
            o.organizer,
            o.description,
            o.registration_deadline,
            o.event_start_date,
            o.event_end_date,
            o.mode,
            o.location,
            o.min_team_size,
            o.max_team_size,
            o.status,
            o.registration_url
        FROM workspace.default.opportunities o
        ORDER BY o.registration_deadline
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        opportunities = []

        for row in rows:
            opportunities.append({
                "opportunity_id": row[0],
                "title": row[1],
                "opportunity_type": row[2],
                "organizer": row[3],
                "description": row[4],
                "registration_deadline": row[5],
                "event_start_date": row[6],
                "event_end_date": row[7],
                "mode": row[8],
                "location": row[9],
                "min_team_size": row[10],
                "max_team_size": row[11],
                "status": row[12],
                "registration_url": row[13]
            })

        return {
            "success": True,
            "message": "Opportunities retrieved successfully",
            "data": {
                "count": len(opportunities),
                "opportunities": opportunities
            }
        }

    finally:
        cursor.close()
        connection.close()


@router.get("/{opportunity_id}")
def get_opportunity(opportunity_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
        SELECT
            o.opportunity_id,
            o.title,
            o.opportunity_type,
            o.organizer,
            o.description,
            o.registration_deadline,
            o.event_start_date,
            o.event_end_date,
            o.mode,
            o.location,
            o.min_team_size,
            o.max_team_size,
            o.status,
            o.registration_url
        FROM workspace.default.opportunities o
        WHERE o.opportunity_id = ?
        """

        cursor.execute(query, (opportunity_id,))
        row = cursor.fetchone()

        if not row:
            return {
                "success": False,
                "message": "Opportunity not found",
                "data": {
                    "opportunity_id": opportunity_id
                }
            }

        opportunity = {
            "opportunity_id": row[0],
            "title": row[1],
            "opportunity_type": row[2],
            "organizer": row[3],
            "description": row[4],
            "registration_deadline": row[5],
            "event_start_date": row[6],
            "event_end_date": row[7],
            "mode": row[8],
            "location": row[9],
            "min_team_size": row[10],
            "max_team_size": row[11],
            "status": row[12],
            "registration_url": row[13]
        }

        return {
            "success": True,
            "message": "Opportunity retrieved successfully",
            "data": opportunity
        }

    finally:
        cursor.close()
        connection.close()