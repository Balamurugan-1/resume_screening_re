from fastapi import FastAPI
from app.api.routes import router
from app.core.config import APP_NAME

app = FastAPI(title=APP_NAME)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Resume Screening API is running 🚀"}
