# from fastapi import APIRouter, Depends, status
# from sqlalchemy.orm import Session

# from app.database import get_db
# from app.schemas.fav import FavoriteCreate, FavoriteResponse
# from app.services.fav import FavoriteService

# router = APIRouter(
#     prefix="/favorites",
#     tags=["farites"],
# )


# def get_fav_service(
#     db: Session = Depends(get_db),
# ) -> FavoriteService:
#     return FavoriteService(db)


# @router.post(
#     "/",
#     response_model=FavoriteResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_fav(
#     schema: FavoriteCreate,
#     service: FavoriteService = Depends(get_fav_service),
# ):
#     return service.create_fav(schema)


# @router.get(
#     "/",
#     response_model=list[FavoriteResponse],
# )
# def get_games(
#     service: FavoriteService = Depends(get_fav_service),
# ):
#     return service.get_games()


# @router.get(
#     "/{game_id}",
#     response_model=FavoriteResponse,
# )
# def get_game(
#     game_id: int,
#     service: FavoriteService = Depends(get_game_service),
# ):
#     return service.get_game(game_id)


# @router.patch(
#     "/{game_id}",
#     response_model=GameResponse,
# )
# def update_game(
#     game_id: int,
#     schema: GameUpdate,
#     service: GameService = Depends(get_game_service),
# ):
#     return service.update_game(game_id, schema)


# @router.delete(
#     "/{game_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# def delete_game(
#     game_id: int,
#     service: GameService = Depends(get_game_service),
# ) -> None:
#     service.delete_game(game_id)