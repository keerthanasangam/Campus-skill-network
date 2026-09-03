from fastapi import APIRouter
import os
import requests

router = APIRouter(
    prefix="/genie",
    tags=["Genie"]
)

DATABRICKS_HOST = os.getenv("DATABRICKS_SERVER_HOSTNAME")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
GENIE_SPACE_ID = os.getenv("GENIE_SPACE_ID")


@router.post("/ask")
def ask_genie(question: str):

    url = (
        f"https://{DATABRICKS_HOST}"
        f"/api/2.0/genie/spaces/{GENIE_SPACE_ID}/start-conversation"
    )

    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "content": question
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return {
            "success": False,
            "message": "Genie request failed",
            "status_code": response.status_code,
            "details": response.text
        }

    return {
        "success": True,
        "message": "Question sent to Genie successfully",
        "data": response.json()
    }