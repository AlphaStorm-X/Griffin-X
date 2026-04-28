from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Annotated
from datetime import datetime, timezone
from bson import ObjectId
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: any, _handler: any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.is_instance_schema(ObjectId),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: any
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())

class MedicineBase(BaseModel):
    name: str = Field(
        ..., 
        description="The common name of the medicine", 
        examples=["Paracetamol"],
        min_length=1
    )
    dosage: str = Field(
        ..., 
        description="The concentration or amount (e.g., 500mg, 10ml)", 
        examples=["500mg"]
    )
    time: List[str] = Field(
        default_factory=lambda: ["08:00"],
        description="Scheduled reminder times for this medicine",
        examples=["08:00"]
    )
    condition: str = Field(
        default="after food",
        description="Instructions for when to take the medicine",
        examples=["after food"]
    )
    dateStart: Optional[str] = Field(
        None,
        description="Schedule start date in YYYY-MM-DD format",
        examples=["2026-04-19"]
    )
    dateEnd: Optional[str] = Field(
        None,
        description="Schedule end date in YYYY-MM-DD format",
        examples=["2026-04-25"]
    )
    takenStatus: Optional[List[bool]] = Field(
        default=None,
        description="Status indicating whether each scheduled dose has been taken"
    )
    frequency: Optional[str] = Field(
        None,
        description="How often the medicine should be taken",
        examples=["Every 8 hours"]
    )
    stock: Optional[int] = Field(
        default=0, 
        description="Current quantity available in stock", 
        examples=[15]
    )
    instructions: Optional[str] = Field(
        None, 
        description="Special instructions (e.g., take after meals)", 
        examples=["Take with water after breakfast"]
    )

class MedicineCreate(MedicineBase):
    """Schema for creating a new medicine entry"""
    pass

class MedicineUpdate(BaseModel):
    """Schema for partially updating a medicine entry"""
    name: Optional[str] = Field(None, examples=["Paracetamol"])
    dosage: Optional[str] = Field(None, examples=["650mg"])
    time: Optional[List[str]] = Field(None, examples=[["08:00"]])
    condition: Optional[str] = Field(None, examples=["after food"])
    dateStart: Optional[str] = Field(None, examples=["2026-04-19"])
    dateEnd: Optional[str] = Field(None, examples=["2026-04-25"])
    takenStatus: Optional[List[bool]] = Field(None, examples=[[False]])
    frequency: Optional[str] = Field(None, examples=["Once daily"])
    stock: Optional[int] = Field(None, examples=[20])
    instructions: Optional[str] = Field(None, examples=["Take before sleeping"])

class MedicineResponse(MedicineBase):
    """Schema for medicine data returned by the API"""
    id: str = Field(alias="_id", description="Unique MongoDB identifier", examples=["60d5ecfd63a2452da4c42d5a"])
    user_id: str = Field(..., description="ID of the owner user", examples=["60d5ecfd63a2452da4c42d5b"])
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp of when the entry was created"
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "_id": "60d5ecfd63a2452da4c42d5a",
                "name": "Paracetamol",
                "dosage": "500mg",
                "frequency": "Three times a day",
                "stock": 10,
                "instructions": "Take after meals",
                "created_at": "2024-04-19T12:00:00Z"
            }
        }
    )
