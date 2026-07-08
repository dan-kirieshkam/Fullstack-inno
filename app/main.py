from fastapi import FastAPI
from app.api.health import router as health_router
from app.config.config import get_settings
from app.database import Base, engine

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)
Base.metadata.create_all(bind=engine)
app.include_router(health_router)

@app.get("/")
def root():
    return {
"message": f"{settings.app_name} is running",
}
