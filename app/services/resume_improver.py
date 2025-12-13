import os
import google.generativeai as genai
from app.schemas.llm_response import ResumeImprovement
import json

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"

def improve_resume(resume_text: str, jd_text: str) -> ResumeImprovement:
    prompt = f"""
You are an ATS optimization expert.

TASK:
1. Analyze the resume against the job description.
2. Identify missing or weak skills.
3. Suggest improvements.
4. Rewrite the resume to better match the JD.

RULES:
- Output MUST be valid JSON
- Do NOT add explanations
- Do NOT hallucinate experience
- Improve wording and alignment only

JSON FORMAT:
{{
  "missing_skills": ["skill1", "skill2"],
  "improvement_suggestions": ["suggestion1", "suggestion2"],
  "improved_resume_text": "full improved resume text"
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}
"""

    response = genai.GenerativeModel(MODEL_NAME).generate_content(prompt)

    # Gemini may wrap JSON in markdown → strip safely
    raw_text = response.text.strip()
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    parsed = json.loads(raw_text)

    return ResumeImprovement(**parsed)
