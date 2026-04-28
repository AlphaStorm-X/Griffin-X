from fastapi import APIRouter, Depends, status, HTTPException
from app.controllers.medicine_controller import MedicineController
from app.models.medicine import MedicineCreate, MedicineResponse, MedicineUpdate
from app.database import get_database
from app.utils.security import get_current_user
from typing import List

router = APIRouter(
    prefix="/medicines", 
    tags=["Medicines"],
    dependencies=[Depends(get_current_user)]
)

async def get_controller():
    db = get_database()
    return MedicineController(db)

@router.post("/", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED, summary="Add new medicine", description="Create a new medicine record owned by the authenticated user.")
async def create_medicine(
    medicine: MedicineCreate,
    current_user: dict = Depends(get_current_user),
    controller: MedicineController = Depends(get_controller)
):
    return await controller.create_medicine(medicine, str(current_user["_id"]))

@router.get("/", response_model=List[MedicineResponse], summary="List my medicines", description="Retrieve all medicine records belonging to the authenticated user.")
async def list_medicines(
    current_user: dict = Depends(get_current_user),
    controller: MedicineController = Depends(get_controller)
):
    return await controller.list_medicines(str(current_user["_id"]))

@router.get("/today", response_model=List[MedicineResponse], summary="List today's medicines", description="Retrieve medicine records scheduled for today.")
async def list_today_medicines(
    current_user: dict = Depends(get_current_user),
    controller: MedicineController = Depends(get_controller)
):
    return await controller.get_medicines_today(str(current_user["_id"]))

@router.get("/{medicine_id}", response_model=MedicineResponse, summary="Get medicine details", description="Retrieve detailed information about a specific medicine, verifying ownership.")
async def get_medicine(
    medicine_id: str,
    current_user: dict = Depends(get_current_user),
    controller: MedicineController = Depends(get_controller)
):
    return await controller.get_medicine(medicine_id, str(current_user["_id"]))

@router.patch("/{medicine_id}", response_model=MedicineResponse, summary="Partially update medicine", description="Update specific fields of a medicine record, verifying ownership.")
async def update_medicine(
    medicine_id: str,
    medicine_update: MedicineUpdate,
    current_user: dict = Depends(get_current_user),
    controller: MedicineController = Depends(get_controller)
):
    return await controller.update_medicine(medicine_id, medicine_update, str(current_user["_id"]))

@router.delete("/{medicine_id}", status_code=status.HTTP_200_OK, summary="Delete medicine", description="Permanently delete a medicine record, verifying ownership.")
async def delete_medicine(
    medicine_id: str,
    current_user: dict = Depends(get_current_user),
    controller: MedicineController = Depends(get_controller)
):
    success = await controller.delete_medicine(medicine_id, str(current_user["_id"]))
    if success:
        return {"message": "Medicine deleted successfully"}
    raise HTTPException(status_code=500, detail="Failed to delete medicine")
