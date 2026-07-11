from sqlalchemy import String, ForeignKey, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    game_id = Column(Integer(), ForeignKey("games.id"))

    user_id = Column(Integer(), ForeignKey("userss.id"))

    extra_data = Column(String(100))