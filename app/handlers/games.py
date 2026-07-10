from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.game import GameCreate, GameResponse, GameUpdate
from app.services.game_servise import GameService

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


def get_game_service(
    db: Session = Depends(get_db),
) -> GameService:
    return GameService(db)


@router.post(
    "/",
    response_model=GameResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_game(
    schema: GameCreate,
    service: GameService = Depends(get_game_service),
):
    return service.create_game(schema)


@router.get(
    "/",
    response_model=list[GameResponse],
)
def get_games(
    service: GameService = Depends(get_game_service),
):
    return service.get_games()


@router.get(
    "/{game_id}",
    response_model=GameResponse,
)
def get_game(
    game_id: int,
    service: GameService = Depends(get_game_service),
):
    return service.get_game(game_id)


@router.patch(
    "/{game_id}",
    response_model=GameResponse,
)
def update_game(
    game_id: int,
    schema: GameUpdate,
    service: GameService = Depends(get_game_service),
):
    return service.update_game(game_id, schema)


@router.delete(
    "/{game_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_game(
    game_id: int,
    service: GameService = Depends(get_game_service),
) -> None:
    service.delete_game(game_id)