from pydantic import BaseModel, Field

class ResumeUpload(BaseModel):
    resume_text: str = Field(..., min_length=50)
