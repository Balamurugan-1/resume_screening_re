import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = AsyncIOMotorClient(MONGODB_URI)
db = client["resume_analyzer"]


users_collection = db["users"]
resumes_collection = db["resumes"]
analyses_collection = db["analyses"]
