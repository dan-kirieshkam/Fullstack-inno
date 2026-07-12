from sqlalchemy import String, ForeignKey, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    extra_data = Column(String(100), nullable=True)

    # ДОБАВЛЕНО: связи для back_populates
    user = relationship("User", back_populates="favorites")
    game = relationship("Game", back_populates="favorites")