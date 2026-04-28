import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def debug_db():
    load_dotenv()
    mongodb_url = os.getenv("MONGODB_URL")
    db_name = os.getenv("DATABASE_NAME", "auracare_db")
    client = AsyncIOMotorClient(mongodb_url)
    db = client.get_database(db_name)
    
    print("--- Users ---")
    async for user in db["users"].find():
        print(f"User: {user.get('email')}, _id type: {type(user.get('_id'))}, _id: {user.get('_id')}")
        
    print("\n--- Medicines ---")
    async for med in db["medicines"].find():
        print(f"Med: {med.get('name')}, user_id type: {type(med.get('user_id'))}, user_id: {med.get('user_id')}, _id: {med.get('_id')}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_db())
