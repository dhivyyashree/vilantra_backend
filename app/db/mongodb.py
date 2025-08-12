from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")
print("📡 Connecting to MongoDB URI:", MONGO_URI)
client = AsyncIOMotorClient(MONGO_URI)
db = client["vilantra"]
print("🟢 Connected to database:", db.name)
collection = db["products"]

async def save_product_to_db(product_data: dict):
    print("📥 Inserting into MongoDB:", product_data)
    result = await collection.insert_one(product_data)
    print("✅ MongoDB Inserted ID:", result.inserted_id)
    return result.inserted_id
