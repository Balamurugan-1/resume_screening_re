from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from bson import ObjectId

from app.schemas.resume import ResumeUpload
from app.dependencies.auth import get_current_user
from app.db.mongo import resumes_collection

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_resume(
    resume: ResumeUpload,
    current_user=Depends(get_current_user)
):
    user_id = ObjectId(current_user["_id"])

    existing = await resumes_collection.find_one({"user_id": user_id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume already uploaded"
        )

    doc = {
        "user_id": user_id,
        "resume_text": resume.resume_text,
        "created_at": datetime.utcnow()
    }

    await resumes_collection.insert_one(doc)

    return {"message": "Resume uploaded successfully"}
