from fastapi import APIRouter, status
from app.models.health import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", response_model=HealthResponse, status_code=status.HTTP_200_OK, summary="Health Check", description="Check if the API and database connection are healthy.")
async def health_check():
    return {"status": "ok"}
