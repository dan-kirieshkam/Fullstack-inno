# app/services/favorite.py
from typing import List, Dict, Any
from fastapi import HTTPException, status

from app.repositories.favorite_repository import FavoriteRepository
from app.repositories.user_repository import UserRepository  # предположим, что есть
from app.repositories.game_repository import GameRepository   # предположим, что есть
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
        
        Args:
            favorite_data: Данные для создания избранного
            
        Returns:
            FavoriteResponse: Созданная запись
            
        Raises:
            HTTPException: Если пользователь или игра не найдены,
                          или запись уже существует
        """
        # Проверяем существование пользователя
        user = await self.user_repo.get_by_id(favorite_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {favorite_data.user_id} not found"
            )
        
        # Проверяем существование игры
        game = await self.game_repo.get_by_id(favorite_data.game_id)
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game with id {favorite_data.game_id} not found"
            )
        
        # Проверяем, не добавлена ли уже игра в избранное
        existing = self.favorite_repo.get_by_user_and_game(
            favorite_data.user_id, 
            favorite_data.game_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Game already in favorites"
            )
        
        # Создаем запись
        favorite = self.favorite_repo.create(
            user_id=favorite_data.user_id,
            game_id=favorite_data.game_id,
            extra_data=favorite_data.extra_data
        )
        
        return FavoriteResponse.model_validate(favorite)
    
    async def remove_from_favorites(self, user_id: int, game_id: int) -> Dict[str, str]:
        """
        Удалить игру из избранного пользователя
        
        Args:
            user_id: ID пользователя
            game_id: ID игры
            
        Returns:
            Dict: Сообщение об успешном удалении
            
        Raises:
            HTTPException: Если запись не найдена
        """
        # Проверяем существование записи
        favorite = self.favorite_repo.get_by_user_and_game(user_id, game_id)
        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite record not found"
            )
        
        # Удаляем запись
        self.favorite_repo.delete(favorite)
        
        return {"message": "Game removed from favorites successfully"}
    
    async def get_user_favorites(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Получить все избранные игры пользователя
        
        Args:
            user_id: ID пользователя
            skip: Количество пропускаемых записей
            limit: Максимальное количество записей
            
        Returns:
            Dict: Список избранных игр и общее количество
            
        Raises:
            HTTPException: Если пользователь не найден
        """
        # Проверяем существование пользователя
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        
        # Получаем избранные игры
        favorites = self.favorite_repo.get_user_favorites_with_games(user_id)
        
        # Преобразуем в нужный формат
        favorite_games = []
        for fav in favorites:
            favorite_games.append(FavoriteGameInfo(
                id=fav.game.id,
                title=fav.game.title,
                author=fav.game.author,
                prev=fav.game.prev,
                extra_data=fav.extra_data
            ))
        
        total = self.favorite_repo.count_user_favorites(user_id)
        
        return {
            "user_id": user_id,
            "favorites": favorite_games,
            "total": total
        }
    
    async def check_is_favorite(self, user_id: int, game_id: int) -> Dict[str, bool]:
        """
        Проверить, находится ли игра в избранном у пользователя
        
        Args:
            user_id: ID пользователя
            game_id: ID игры
            
        Returns:
            Dict: Результат проверки
        """
        is_favorite = self.favorite_repo.is_favorite(user_id, game_id)
        return {
            "user_id": user_id,
            "game_id": game_id,
            "is_favorite": is_favorite
        }
    
    async def get_favorite_by_id(self, favorite_id: int) -> FavoriteResponse:
        """
        Получить запись избранного по ID
        
        Args:
            favorite_id: ID записи избранного
            
        Returns:
            FavoriteResponse: Запись избранного
            
        Raises:
            HTTPException: Если запись не найдена
        """
        favorite = self.favorite_repo.get_by_id(favorite_id)
        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Favorite with id {favorite_id} not found"
            )
        
        return FavoriteResponse.model_validate(favorite)
    
    async def clear_user_favorites(self, user_id: int) -> Dict[str, str]:
        """
        Очистить все избранные игры пользователя
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Dict: Сообщение об успешной очистке
            
        Raises:
            HTTPException: Если пользователь не найден
        """
        # Проверяем существование пользователя
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        
        # Удаляем все избранные игры
        count = self.favorite_repo.delete_all_user_favorites(user_id)
        
        return {
            "message": f"All favorites cleared successfully",
            "deleted_count": count
        }