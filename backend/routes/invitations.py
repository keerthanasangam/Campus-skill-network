from fastapi import APIRouter
from database.databricks import get_connection

router = APIRouter(
    prefix="/invitations",
    tags=["Invitations"]
)


@router.get("/{user_id}")
def get_invitations(user_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
        SELECT
            invitation_id,
            team_id,
            sender_id,
            receiver_id,
            message,
            status,
            created_at,
            responded_at
        FROM workspace.default.invitations
        WHERE receiver_id = ?
        ORDER BY created_at DESC
        """

        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        invitations = []

        for row in rows:
            invitations.append({
                "invitation_id": row[0],
                "team_id": row[1],
                "sender_id": row[2],
                "receiver_id": row[3],
                "message": row[4],
                "status": row[5],
                "created_at": row[6],
                "responded_at": row[7]
            })

        return {
            "success": True,
            "message": "Invitations retrieved successfully",
            "data": {
                "user_id": user_id,
                "count": len(invitations),
                "invitations": invitations
            }
        }

    finally:
        cursor.close()
        connection.close()


@router.patch("/{invitation_id}/accept")
def accept_invitation(invitation_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT invitation_id, status
            FROM workspace.default.invitations
            WHERE invitation_id = ?
        """, (invitation_id,))

        row = cursor.fetchone()

        if not row:
            return {
                "success": False,
                "message": "Invitation not found",
                "data": {
                    "invitation_id": invitation_id
                }
            }

        if row[1] != "PENDING":
            return {
                "success": False,
                "message": "Invitation has already been processed",
                "data": {
                    "invitation_id": invitation_id,
                    "status": row[1]
                }
            }

        cursor.execute("""
            UPDATE workspace.default.invitations
            SET status = 'ACCEPTED',
                responded_at = current_timestamp()
            WHERE invitation_id = ?
        """, (invitation_id,))

        return {
            "success": True,
            "message": "Invitation accepted successfully",
            "data": {
                "invitation_id": invitation_id,
                "status": "ACCEPTED"
            }
        }

    finally:
        cursor.close()
        connection.close()


@router.patch("/{invitation_id}/reject")
def reject_invitation(invitation_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT invitation_id, status
            FROM workspace.default.invitations
            WHERE invitation_id = ?
        """, (invitation_id,))

        row = cursor.fetchone()

        if not row:
            return {
                "success": False,
                "message": "Invitation not found",
                "data": {
                    "invitation_id": invitation_id
                }
            }

        if row[1] != "PENDING":
            return {
                "success": False,
                "message": "Invitation has already been processed",
                "data": {
                    "invitation_id": invitation_id,
                    "status": row[1]
                }
            }

        cursor.execute("""
            UPDATE workspace.default.invitations
            SET status = 'REJECTED',
                responded_at = current_timestamp()
            WHERE invitation_id = ?
        """, (invitation_id,))

        return {
            "success": True,
            "message": "Invitation rejected successfully",
            "data": {
                "invitation_id": invitation_id,
                "status": "REJECTED"
            }
        }

    finally:
        cursor.close()
        connection.close()