from pydantic import BaseModel
from typing import List

class ResumeImprovement(BaseModel):
    missing_skills: List[str]
    improvement_suggestions: List[str]
    improved_resume_text: str
