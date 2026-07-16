# app/models/__init__.py
from .user import User
from .favorite import Favorite
from .game import Game

__all__ = ['User', 'Favorite', 'Game']