from fastapi import FastAPI

from routes.auth import router as auth_router
from routes.users import router as users_router
from routes.opportunities import router as opportunities_router
from routes.recommendations import router as recommendations_router
from routes.invitations import router as invitations_router
from routes.teams import router as teams_router

app = FastAPI(
    title="Campus Skill Network API",
    description="AI-powered platform for finding the right project teammates across campus.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Campus Skill Network API is running 🚀",
        "status": "success"
    }


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(opportunities_router)
app.include_router(recommendations_router)
app.include_router(invitations_router)  
app.include_router(teams_router)