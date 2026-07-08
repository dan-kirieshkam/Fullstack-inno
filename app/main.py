from fastapi import FastAPI
<<<<<<< HEAD
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
=======

from app.api.health import router as health_router
from app.config.config import get_settings


settings = get_settings()


app = FastAPI(
    title = settings.app_name,
    version = settings.app_version,
    debug = settings.debug,
)

>>>>>>> a612e787b71ad0443df6cf4cac1d699371ab7049
app.include_router(health_router)

@app.get("/")
def root():
    return {
<<<<<<< HEAD
"message": f"{settings.app_name} is running",
}
=======
        "message": f"{settings.app_name} is running",
    }

from app.schemas.game import GameCreate, GameResponse

@app.post("/games", response_model=GameResponse)
def create_book(game: GameCreate):
    return{
        "id": 1,
        "title": game.title,
        "author": game.author,
        "previe": game.previe,
    }
>>>>>>> a612e787b71ad0443df6cf4cac1d699371ab7049
