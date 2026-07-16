# app/services/favorite.py
from typing import List, Dict, Any
from fastapi import HTTPException, status

from app.repositories.favorite_repository import FavoriteRepository
from app.repositories.user_repository import UserRepository
from app.repositories.game_repository import GameRepository
from app.schemas.fav import FavoriteCreate, FavoriteResponse, FavoriteGameInfo


class FavoriteService:
    """Сервис для работы с избранными играми"""
    
    def __init__(
        self,
        favorite_repo: FavoriteRepository,
        user_repo: UserRepository,
        game_repo: GameRepository
    ):
        self.favorite_repo = favorite_repo
        self.user_repo = user_repo
        self.game_repo = game_repo
    
    async def add_to_favorites(self, favorite_data: FavoriteCreate) -> FavoriteResponse:
        """
        Добавить игру в избранное пользователя
        """
        # Убираем await - методы синхронные
        user = self.user_repo.get_by_id(favorite_data.user_id)  # ✅
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {favorite_data.user_id} not found"
            )
        
        game = self.game_repo.get_by_id(favorite_data.game_id)  # ✅
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game with id {favorite_data.game_id} not found"
            )
        
        existing = self.favorite_repo.get_by_user_and_game(
            favorite_data.user_id, 
            favorite_data.game_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Game already in favorites"
            )
        
        favorite = self.favorite_repo.create(
            user_id=favorite_data.user_id,
            game_id=favorite_data.game_id,
            extra_data=favorite_data.extra_data
        )
        
        return FavoriteResponse.model_validate(favorite)
    
    async def remove_from_favorites(self, user_id: int, game_id: int) -> Dict[str, str]:
        """Удалить игру из избранного пользователя"""
        favorite = self.favorite_repo.get_by_user_and_game(user_id, game_id)  # ✅
        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite record not found"
            )
        
        self.favorite_repo.delete(favorite)
        
        return {"message": "Game removed from favorites successfully"}
    
    async def get_user_favorites(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> Dict[str, Any]:
        """Получить все избранные игры пользователя"""
        user = self.user_repo.get_by_id(user_id)  # ✅
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        
        favorites = self.favorite_repo.get_user_favorites_with_games(user_id)
        
        favorite_games = []
        for fav in favorites:
            favorite_games.append(FavoriteGameInfo(
                id=fav.game.id,
                title=fav.game.title,
                publisher=fav.game.publisher,
                short_description=fav.game.short_description,
                extra_data=fav.extra_data
            ))
        
        total = self.favorite_repo.count_user_favorites(user_id)
        
        return {
            "user_id": user_id,
            "favorites": favorite_games,
            "total": total
        }
    
    async def check_is_favorite(self, user_id: int, game_id: int) -> Dict[str, bool]:
        """Проверить, находится ли игра в избранном у пользователя"""
        is_favorite = self.favorite_repo.is_favorite(user_id, game_id)
        return {
            "user_id": user_id,
            "game_id": game_id,
            "is_favorite": is_favorite
        }
    
    async def get_favorite_by_id(self, favorite_id: int) -> FavoriteResponse:
        """Получить запись избранного по ID"""
        favorite = self.favorite_repo.get_by_id(favorite_id)
        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Favorite with id {favorite_id} not found"
            )
        
        return FavoriteResponse.model_validate(favorite)
    
    async def clear_user_favorites(self, user_id: int) -> Dict[str, str]:
        """Очистить все избранные игры пользователя"""
        user = self.user_repo.get_by_id(user_id)  # ✅
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        
        count = self.favorite_repo.delete_all_user_favorites(user_id)
        
        return {
            "message": f"All favorites cleared successfully",
            "deleted_count": count
        }