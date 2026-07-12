# app/schemas/favorite.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FavoriteBase(BaseModel):
    """Базовая схема для избранного"""
    extra_data: Optional[str] = Field(None, max_length=100, description="Дополнительные данные")

class FavoriteCreate(FavoriteBase):
    """Схема для создания избранного"""
    user_id: int = Field(..., description="ID пользователя")
    game_id: int = Field(..., description="ID игры")

class FavoriteResponse(FavoriteBase):
    """Схема для ответа с избранным"""
    id: int
    user_id: int
    game_id: int
    created_at: Optional[datetime] = None  # если добавите поле в модель
    
    class Config:
        from_attributes = True

class FavoriteGameInfo(BaseModel):
    """Схема для информации об игре в избранном"""
    id: int
    title: str
    author: str
    prev: str
    extra_data: Optional[str] = None

class UserFavoriteResponse(BaseModel):
    """Схема для ответа со всеми избранными играми пользователя"""
    user_id: int
    favorites: list[FavoriteGameInfo]
    total: int