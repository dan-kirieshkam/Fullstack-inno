from sqlalchemy.orm import Session

from app.models.game import Game
from app.models.user import User
from app.models.favorite import Favorite


class FavoriteRepository:

    def __init__(self, db: Session):
        self.db = db
        
    def create(self, fav: Favorite) -> Favorite:
        return self._upsert(fav)
    
    def delete(self, fav: Favorite) -> None:
        self.db.delete(fav)
        self.db.commit()