from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URI, MONGO_DB_NAME

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# Ensure email is unique
async def init_indexes():
    await db["users"].create_index("email", unique=True)
