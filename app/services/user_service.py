from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import UserCreate, UserInDB
from app.utils.security import get_password_hash
from datetime import datetime, timezone

class UserService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        return await self.collection.find_one({"email": email})

    async def get_user_by_username(self, username: str) -> Optional[dict]:
        return await self.collection.find_one({"username": username})

    async def create_user(self, user_in: UserCreate) -> dict:
        hashed_password = get_password_hash(user_in.password)
        user_dict = user_in.model_dump()
        del user_dict["password"]
        user_dict["hashed_password"] = hashed_password
        user_dict["is_active"] = True
        user_dict["created_at"] = datetime.now(timezone.utc)
        
        result = await self.collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        return user_dict
