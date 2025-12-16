from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from bson import ObjectId

from app.schemas.analysis import AnalysisRequest
from app.dependencies.auth import get_current_user
from app.db.mongo import resumes_collection, analyses_collection


from app.services.embedding_service import get_embedding
from app.utils.similarity import cosine_similarity
from app.services.resume_improver import improve_resume

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/run")
async def run_analysis(
    data: AnalysisRequest,
    current_user=Depends(get_current_user)
):
    user_id = ObjectId(current_user["_id"])

    resume = await resumes_collection.find_one({"user_id": user_id})
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No resume uploaded"
        )

    resume_text = resume["resume_text"]
    jd_text = data.job_description

    resume_emb = get_embedding(resume_text)
    jd_emb = get_embedding(jd_text)
    original_score = cosine_similarity(resume_emb, jd_emb)

    improvement = improve_resume(
        resume_text=resume_text,
        jd_text=jd_text
    )

    improved_text = improvement.improved_resume_text
    missing_skills = improvement.missing_skills
    suggestions = improvement.improvement_suggestions

    improved_emb = get_embedding(improved_text)
    improved_score = cosine_similarity(improved_emb, jd_emb)

    doc = {
        "user_id": user_id,
        "job_description": jd_text,
        "original_score": float(original_score),
        "improved_score": float(improved_score),
        "improved_resume_text": improved_text,
        "missing_skills": missing_skills,
        "improvement_suggestions": suggestions,
        "created_at": datetime.utcnow()
    }

    await analyses_collection.insert_one(doc)

    return {
        "original_score": original_score,
        "improved_score": improved_score,
        "improved_resume_text": improved_text,
        "missing_skills": missing_skills,
        "improvement_suggestions": suggestions
    }

