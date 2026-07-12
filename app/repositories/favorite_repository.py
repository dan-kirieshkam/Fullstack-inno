# app/repositories/favorite.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.favorite import Favorite
from app.models.user import User
from app.models.game import Game


class FavoriteRepository:
    """Репозиторий для работы с избранными играми"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, favorite_id: int) -> Optional[Favorite]:
        """Получить запись избранного по ID"""
        return self.db.query(Favorite).filter(Favorite.id == favorite_id).first()
    
    def get_by_user_and_game(self, user_id: int, game_id: int) -> Optional[Favorite]:
        """Получить запись избранного по пользователю и игре"""
        return self.db.query(Favorite).filter(
            and_(Favorite.user_id == user_id, Favorite.game_id == game_id)
        ).first()
    
    def get_user_favorites(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Favorite]:
        """Получить все избранные игры пользователя"""
        return self.db.query(Favorite).filter(
            Favorite.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_user_favorites_with_games(self, user_id: int) -> List[Favorite]:
        """Получить избранные игры пользователя с загрузкой данных игр"""
        return self.db.query(Favorite).filter(
            Favorite.user_id == user_id
        ).join(Game).all()
    
    def get_game_favorited_by_users(self, game_id: int) -> List[Favorite]:
        """Получить всех пользователей, которые добавили игру в избранное"""
        return self.db.query(Favorite).filter(Favorite.game_id == game_id).all()
    
    def create(self, user_id: int, game_id: int, extra_data: Optional[str] = None) -> Favorite:
        """Создать новую запись в избранном"""
        favorite = Favorite(
            user_id=user_id,
            game_id=game_id,
            extra_data=extra_data
        )
        self.db.add(favorite)
        self.db.commit()
        self.db.refresh(favorite)
        return favorite
    
    def delete(self, favorite: Favorite) -> bool:
        """Удалить запись из избранного"""
        self.db.delete(favorite)
        self.db.commit()
        return True
    
    def delete_by_user_and_game(self, user_id: int, game_id: int) -> bool:
        """Удалить запись из избранного по пользователю и игре"""
        favorite = self.get_by_user_and_game(user_id, game_id)
        if favorite:
            return self.delete(favorite)
        return False
    
    def delete_all_user_favorites(self, user_id: int) -> int:
        """Удалить все избранные игры пользователя"""
        favorites = self.get_user_favorites(user_id)
        count = len(favorites)
        for fav in favorites:
            self.db.delete(fav)
        self.db.commit()
        return count
    
    def count_user_favorites(self, user_id: int) -> int:
        """Подсчитать количество избранных игр пользователя"""
        return self.db.query(Favorite).filter(Favorite.user_id == user_id).count()
    
    def is_favorite(self, user_id: int, game_id: int) -> bool:
        """Проверить, находится ли игра в избранном у пользователя"""
        return self.get_by_user_and_game(user_id, game_id) is not None