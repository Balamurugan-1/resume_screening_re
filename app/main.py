from fastapi import FastAPI
from app.api.routes import router
from app.core.config import APP_NAME
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
import time
from app.api.auth.routes import router as auth_router
from app.api.resume.routes import router as resume_router
from app.api.analysis.routes import router as analysis_router


app = FastAPI(title=APP_NAME)
app.include_router(router)
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(analysis_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Resume Screening API is running 🚀"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc)
        }
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = round(time.time() - start_time, 3)

    print(f"{request.method} {request.url.path} - {response.status_code} - {duration}s")
    return response
