from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.medicine import MedicineCreate, MedicineUpdate
from datetime import datetime, timezone
from bson import ObjectId

class MedicineService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["medicines"]

    async def create_medicine(self, medicine: MedicineCreate, user_id: str) -> dict:
        medicine_dict = medicine.model_dump()
        medicine_dict["user_id"] = user_id
        medicine_dict["created_at"] = datetime.now(timezone.utc)

        if not medicine_dict.get("takenStatus") or len(medicine_dict["takenStatus"]) != len(medicine_dict.get("time", [])):
            medicine_dict["takenStatus"] = [False] * len(medicine_dict.get("time", []))

        result = await self.collection.insert_one(medicine_dict)
        medicine_dict["_id"] = str(result.inserted_id)
        return medicine_dict

    async def get_all_medicines(self, user_id: str) -> List[dict]:
        medicines = []
        async for doc in self.collection.find({"user_id": user_id}):
            doc["_id"] = str(doc["_id"])
            medicines.append(doc)
        return medicines

    async def get_medicine_by_id(self, medicine_id: str, user_id: Optional[str] = None) -> Optional[dict]:
        if not ObjectId.is_valid(medicine_id):
            return None

        query = {"_id": ObjectId(medicine_id)}
        if user_id:
            query["user_id"] = user_id

        doc = await self.collection.find_one(query)
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def update_medicine(self, medicine_id: str, data: MedicineUpdate, user_id: Optional[str] = None) -> Optional[dict]:
        if not ObjectId.is_valid(medicine_id):
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        if "time" in update_data and "takenStatus" not in update_data:
            update_data["takenStatus"] = [False] * len(update_data["time"])

        if not update_data:
            return await self.get_medicine_by_id(medicine_id, user_id)

        query = {"_id": ObjectId(medicine_id)}
        if user_id:
            query["user_id"] = user_id

        await self.collection.update_one(
            query,
            {"$set": update_data}
        )
        return await self.get_medicine_by_id(medicine_id, user_id)

    async def delete_medicine(self, medicine_id: str, user_id: Optional[str] = None) -> bool:
        if not ObjectId.is_valid(medicine_id):
            return False

        query = {"_id": ObjectId(medicine_id)}
        if user_id:
            query["user_id"] = user_id

        result = await self.collection.delete_one(query)
        return result.deleted_count > 0

    async def get_medicines_today(self, user_id: str) -> List[dict]:
        """
        Retrieves medicines that are scheduled for today based on dateStart and dateEnd.
        If date fields are missing, they are considered active.
        """
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        # Query for medicines belonging to the user
        # We look for medicines where:
        # 1. dateStart <= today AND dateEnd >= today
        # 2. OR dateStart/dateEnd are null (assuming perpetual or unspecified)
        query = {
            "user_id": user_id,
            "$or": [
                {
                    "dateStart": {"$lte": today_str},
                    "dateEnd": {"$gte": today_str}
                },
                {
                    "dateStart": None,
                    "dateEnd": None
                },
                {
                    "dateStart": "",
                    "dateEnd": ""
                }
            ]
        }
        
        medicines = []
        async for doc in self.collection.find(query):
            doc["_id"] = str(doc["_id"])
            medicines.append(doc)
        return medicines
