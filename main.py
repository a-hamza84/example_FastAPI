from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from fastapi import FastAPI, Header

from login import login
from task_mngt import task_mngt
import uvicorn

api_router = APIRouter()
api_router.include_router(login.router, prefix="/onboarding", tags=["login"])
api_router.include_router(task_mngt.router, prefix="/tasks", tags=["task_mngt"])

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
