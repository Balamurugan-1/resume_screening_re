from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from app.schemas.user import UserCreate, UserResponse
from app.db.mongo import users_collection
from app.utils.security import hash_password
from app.utils.object_id import serialize_object_id

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    user_doc = {
        "email": user.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }

    result = await users_collection.insert_one(user_doc)

    user_doc["_id"] = result.inserted_id
    return serialize_object_id(user_doc)
