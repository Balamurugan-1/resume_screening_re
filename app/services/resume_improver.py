import json
from app.utils.retry import retry_llm
from app.schemas.llm_response import ResumeImprovement
import google.generativeai as genai

def improve_resume(resume_text: str, jd_text: str) -> ResumeImprovement:
    def call_llm():
        prompt = f"""
You are an ATS optimization expert.

STRICT RULES:
- Output ONLY valid JSON
- No markdown
- No explanation
- No hallucinated experience

JSON FORMAT:
{{
  "missing_skills": [],
  "improvement_suggestions": [],
  "improved_resume_text": ""
}}

RESUME:
{resume_text[:5000]}

JOB DESCRIPTION:
{jd_text[:3000]}
"""
        response = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)
        raw = response.text.strip()
        return json.loads(raw)

    parsed = retry_llm(call_llm)

    return ResumeImprovement(**parsed)
