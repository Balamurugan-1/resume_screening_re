from pydantic import BaseModel

class JDInput(BaseModel):
    job_description: str
