# app/api/v1/endpoints/favorite.py
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

router = APIRouter(prefix="/favorites", tags=["favorites"])


# Dependency для получения сервиса
def get_favorite_service(db: Session = Depends(get_db)) -> FavoriteService:
    """Dependency для FavoriteService"""
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
    """
    Добавление игры в избранное
    
    Args:
        favorite_data: Данные для создания избранного
        
    Returns:
        FavoriteResponse: Созданная запись
    """
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
    """
    Удаление игры из избранного
    
    Args:
        user_id: ID пользователя
        game_id: ID игры
        
    Returns:
        Dict: Сообщение об успешном удалении
    """
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
    """
    Получение всех избранных игр пользователя
    
    Args:
        user_id: ID пользователя
        skip: Количество пропускаемых записей
        limit: Максимальное количество записей
        
    Returns:
        UserFavoriteResponse: Список избранных игр
    """
    return await service.get_user_favorites(user_id, skip, limit)


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
    """
    Проверка наличия игры в избранном
    
    Args:
        user_id: ID пользователя
        game_id: ID игры
        
    Returns:
        Dict: Результат проверки
    """
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
    """
    Получение записи избранного по ID
    
    Args:
        favorite_id: ID записи избранного
        
    Returns:
        FavoriteResponse: Запись избранного
    """
    return await service.get_favorite_by_id(favorite_id)


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
    """
    Очистка всех избранных игр пользователя
    
    Args:
        user_id: ID пользователя
        
    Returns:
        Dict: Сообщение об успешной очистке
    """
    return await service.clear_user_favorites(user_id)