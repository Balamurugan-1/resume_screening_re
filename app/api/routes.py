from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.resume_parser import extract_text_from_pdf, extract_text_from_docx
from app.utils.text_cleaner import clean_text
from app.schemas.request import JDInput
from app.services.embedding_service import get_embedding
from app.utils.similarity import cosine_similarity
from app.schemas.request import JDInput
from pydantic import BaseModel
import traceback
from app.services.resume_improver import improve_resume
from app.services.embedding_service import get_embedding
from app.utils.similarity import cosine_similarity
from pydantic import BaseModel
from app.utils.latex_formatter import resume_text_to_latex
from app.db.mongo import db


router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    if file.filename.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file.file)
    elif file.filename.endswith(".docx"):
        raw_text = extract_text_from_docx(file.file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    cleaned_text = clean_text(raw_text)

    return {
        "filename": file.filename,
        "cleaned_resume_text": cleaned_text
    }

@router.post("/parse-jd")
async def parse_jd(jd: JDInput):
    cleaned_jd = clean_text(jd.job_description)

    if not cleaned_jd:
        raise HTTPException(status_code=400, detail="JD text is empty")

    return {
        "cleaned_jd_text": cleaned_jd
    }



class SimilarityRequest(BaseModel):
    resume_text: str
    job_description: str
@router.post("/score")
async def score_resume(payload: SimilarityRequest):
    try:
        resume_embedding = get_embedding(payload.resume_text)
        jd_embedding = get_embedding(payload.job_description)

        score = cosine_similarity(resume_embedding, jd_embedding)

        return {
            "similarity_score": round(score * 100, 2)
        }

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    

class ImproveRequest(BaseModel):
    resume_text: str
    job_description: str
@router.post("/improve")
async def improve_resume_endpoint(payload: ImproveRequest):
    original_score = cosine_similarity(
        get_embedding(payload.resume_text),
        get_embedding(payload.job_description)
    )

    improvement = improve_resume(
        payload.resume_text,
        payload.job_description
    )

    improved_score = cosine_similarity(
        get_embedding(improvement.improved_resume_text),
        get_embedding(payload.job_description)
    )

    latex_code = resume_text_to_latex(improvement.improved_resume_text)

    return {
        "original_score": round(original_score * 100, 2),
        "improved_score": round(improved_score * 100, 2),
        "score_delta": round((improved_score - original_score) * 100, 2),
        "missing_skills": improvement.missing_skills,
        "suggestions": improvement.improvement_suggestions,
        "improved_resume": improvement.improved_resume_text,
        "latex_resume": latex_code
    }


@router.get("/db-test")
async def db_test():
    collections = await db.list_collection_names()
    return {
        "status": "connected",
        "collections": collections
    }
