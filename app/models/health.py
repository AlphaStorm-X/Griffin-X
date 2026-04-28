from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = Field(..., description="The status of the API", examples=["ok"])

    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok"
            }
        }
