from fastapi import HTTPException, status
from app.services.medicine_service import MedicineService
from app.models.medicine import MedicineCreate, MedicineResponse, MedicineUpdate
from motor.motor_asyncio import AsyncIOMotorDatabase

class MedicineController:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.service = MedicineService(db)

    async def create_medicine(self, medicine: MedicineCreate, user_id: str):
        return await self.service.create_medicine(medicine, user_id)

    async def list_medicines(self, user_id: str):
        return await self.service.get_all_medicines(user_id)

    async def get_medicine(self, medicine_id: str, user_id: str):
        medicine = await self.service.get_medicine_by_id(medicine_id, user_id)
        if not medicine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicine not found")
        return medicine

    async def update_medicine(self, medicine_id: str, data: MedicineUpdate, user_id: str):
        medicine = await self.service.get_medicine_by_id(medicine_id, user_id)
        if not medicine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicine not found")
        
        return await self.service.update_medicine(medicine_id, data, user_id)

    async def delete_medicine(self, medicine_id: str, user_id: str):
        medicine = await self.service.get_medicine_by_id(medicine_id, user_id)
        if not medicine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicine not found")
        
        return await self.service.delete_medicine(medicine_id, user_id)

    async def get_medicines_today(self, user_id: str):
        return await self.service.get_medicines_today(user_id)
