from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    publisher: Mapped[str] = mapped_column(String, nullable=False)
    short_description: Mapped[str] = mapped_column(String, nullable=False)
    genre: Mapped[str] = mapped_column(String, nullable=False)
    release_date: Mapped[int] = mapped_column(String, nullable=False)
    thumbnail: Mapped[str] = mapped_column(String, nullable=False)
    
    # categories = relationship("Cat", back_populates="games")
    
    # ИЗМЕНЕНО: было users = relationship("Favorite", backref='game')
    # favorites = relationship("Favorite", back_populates="game", cascade="all, delete-orphan")
    
    favorites = relationship('app.models.favorite.Favorite', back_populates='game', cascade="all, delete-orphan")
    favorited_by = relationship("User", secondary="favorites", viewonly=True)