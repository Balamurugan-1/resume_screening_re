from bson import ObjectId
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.db.mongo import users_collection
from app.dependencies.auth import get_current_user
from app.schemas.user import UserCreate, UserResponse
from app.utils.jwt import create_access_token
from app.utils.object_id import serialize_object_id
from app.utils.security import hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/me")
async def read_current_user(
    current_user: dict = Depends(get_current_user)
):
    return {
        "id": str(current_user["_id"]),
        "email": current_user["email"],
        "created_at": current_user["created_at"]
    }


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

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await users_collection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(user["_id"])}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }