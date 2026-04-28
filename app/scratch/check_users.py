import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Add parent directory to sys.path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def check_users():
    load_dotenv()
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    print(f"Connecting to {mongodb_url}")
    client = AsyncIOMotorClient(mongodb_url)
    db = client.get_database(os.getenv("DATABASE_NAME", "auracare_db"))
    users = await db["users"].find().to_list(10)
    print(f"Found {len(users)} users")
    for user in users:
        print(f"- {user.get('email')} (Name: {user.get('name')})")
    client.close()

if __name__ == "__main__":
    asyncio.run(check_users())
