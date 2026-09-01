from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/invitations",
    tags=["Invitations"]
)


class InvitationRequest(BaseModel):
    sender_id: str
    receiver_id: str
    opportunity_id: str
    message: str = ""


# Temporary invitation storage
invitations = []


# Send invitation
@router.post("/")
def send_invitation(invitation: InvitationRequest):

    new_invitation = {
        "invitation_id": f"INV{len(invitations) + 1:03d}",
        "sender_id": invitation.sender_id,
        "receiver_id": invitation.receiver_id,
        "opportunity_id": invitation.opportunity_id,
        "message": invitation.message,
        "status": "pending"
    }

    invitations.append(new_invitation)

    return {
        "success": True,
        "message": "Invitation sent successfully",
        "data": {
            "invitation": new_invitation
        }
    }


# Get invitations received by a user
@router.get("/{user_id}")
def get_invitations(user_id: str):

    user_invitations = [
        invitation
        for invitation in invitations
        if invitation["receiver_id"] == user_id
    ]

    return {
        "success": True,
        "message": "Invitations retrieved successfully",
        "data": {
            "user_id": user_id,
            "count": len(user_invitations),
            "invitations": user_invitations
        }
    }


# Accept invitation
@router.patch("/{invitation_id}/accept")
def accept_invitation(invitation_id: str):

    for invitation in invitations:

        if invitation["invitation_id"] == invitation_id:

            if invitation["status"] != "pending":
                return {
                    "success": False,
                    "message": "Invitation has already been processed",
                    "data": {
                        "invitation_id": invitation_id,
                        "status": invitation["status"]
                    }
                }

            invitation["status"] = "accepted"

            return {
                "success": True,
                "message": "Invitation accepted successfully",
                "data": {
                    "invitation": invitation
                }
            }

    return {
        "success": False,
        "message": "Invitation not found",
        "data": {
            "invitation_id": invitation_id
        }
    }


# Reject invitation
@router.patch("/{invitation_id}/reject")
def reject_invitation(invitation_id: str):

    for invitation in invitations:

        if invitation["invitation_id"] == invitation_id:

            if invitation["status"] != "pending":
                return {
                    "success": False,
                    "message": "Invitation has already been processed",
                    "data": {
                        "invitation_id": invitation_id,
                        "status": invitation["status"]
                    }
                }

            invitation["status"] = "rejected"

            return {
                "success": True,
                "message": "Invitation rejected successfully",
                "data": {
                    "invitation": invitation
                }
            }

    return {
        "success": False,
        "message": "Invitation not found",
        "data": {
            "invitation_id": invitation_id
        }
    }