# app/api/endpoints/fav.py
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.favorite_repository import FavoriteRepository
from app.repositories.user_repository import UserRepository
from app.repositories.game_repository import GameRepository
from app.services.fav import FavoriteService
from app.schemas.fav import (
    FavoriteCreate, 
    FavoriteResponse, 
    UserFavoriteResponse,
    FavoriteGameInfo
)
from app.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/favorites", tags=["favorites"])


def get_favorite_service(db: Session = Depends(get_db)) -> FavoriteService:
    favorite_repo = FavoriteRepository(db)
    user_repo = UserRepository(db)
    game_repo = GameRepository(db)
    return FavoriteService(favorite_repo, user_repo, game_repo)


@router.post(
    "/",
    response_model=FavoriteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить игру в избранное",
    description="Добавляет игру в избранное указанного пользователя"
)
async def add_to_favorites(
    favorite_data: FavoriteCreate,
    service: FavoriteService = Depends(get_favorite_service)
) -> FavoriteResponse:
    return await service.add_to_favorites(favorite_data)


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Удалить игру из избранного",
    description="Удаляет игру из избранного пользователя"
)
async def remove_from_favorites(
    user_id: int = Query(..., description="ID пользователя"),
    game_id: int = Query(..., description="ID игры"),
    service: FavoriteService = Depends(get_favorite_service)
) -> Dict[str, str]:
    return await service.remove_from_favorites(user_id, game_id)


@router.get(
    "/user/{user_id}",
    response_model=UserFavoriteResponse,
    summary="Получить избранные игры пользователя",
    description="Возвращает все избранные игры указанного пользователя"
)
async def get_user_favorites(
    user_id: int,
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(100, ge=1, le=100, description="Максимальное количество записей"),
    service: FavoriteService = Depends(get_favorite_service)
) -> Dict[str, Any]:
    return await service.get_user_favorites(user_id, skip, limit)


@router.get(
    "/me/",
    response_model=UserFavoriteResponse,
    summary="Получить избранные игры текущего пользователя",
    description="Возвращает все избранные игры авторизованного пользователя"
)
async def get_my_favorites(
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(100, ge=1, le=100, description="Максимальное количество записей"),
    service: FavoriteService = Depends(get_favorite_service)
) -> Dict[str, Any]:
    return await service.get_user_favorites(current_user.id, skip, limit)


@router.get(
    "/check/",
    summary="Проверить наличие игры в избранном",
    description="Проверяет, находится ли игра в избранном у пользователя"
)
async def check_is_favorite(
    user_id: int = Query(..., description="ID пользователя"),
    game_id: int = Query(..., description="ID игры"),
    service: FavoriteService = Depends(get_favorite_service)
) -> Dict[str, bool]:
    return await service.check_is_favorite(user_id, game_id)


@router.get(
    "/{favorite_id}",
    response_model=FavoriteResponse,
    summary="Получить запись избранного по ID",
    description="Возвращает информацию о записи избранного по её ID"
)
async def get_favorite_by_id(
    favorite_id: int,
    service: FavoriteService = Depends(get_favorite_service)
) -> FavoriteResponse:
    favorite = await service.get_favorite_by_id(favorite_id)
    return favorite


@router.delete(
    "/user/{user_id}/clear",
    status_code=status.HTTP_200_OK,
    summary="Очистить все избранные игры пользователя",
    description="Удаляет все игры из избранного указанного пользователя"
)
async def clear_user_favorites(
    user_id: int,
    service: FavoriteService = Depends(get_favorite_service)
) -> Dict[str, str]:
    return await service.clear_user_favorites(user_id)