from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String, nullable=False)

    author: Mapped[str] = mapped_column(String, nullable=False)

    prev: Mapped[str] = mapped_column(String, nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    categories = relationship("Cat", back_populates="games")

    users = relationship("Favorite", backref='game')
# class Category(Base):
#     __tablename__ = "categories"

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

#     name: Mapped[str] = mapped_column(String, nullable=False)

#     games = relationship("Game", back_populates="categories")
