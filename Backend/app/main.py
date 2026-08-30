from fastapi import FastAPI

from app.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for the FDO-Privacy prototype.",
)


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "ok",
        "service": "fdo-privacy-backend",
    }