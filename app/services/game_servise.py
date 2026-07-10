from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.game import Game
from app.repositories.game_repository import GameRepository
from app.repositories.cat_repository import CatRepository
from app.schemas.game import GameCreate, GameUpdate


class GameService:

    def __init__(self, db: Session):
        self.repository = GameRepository(db)
        self.cat_repository = CatRepository(db)

    def create_game(self, schema: GameCreate) -> Game:
        game = Game(
            title=schema.title,
            author=schema.author,
            prev=schema.prev,
            category_id=schema.category_id,
        )

        return self.repository.create(game)

    def get_games(self) -> list[Game]:
        return self.repository.get_all()

    def get_game(self, game_id: int) -> Game:
        game = self.repository.get_by_id(game_id)

        if game is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found",
            )

        return game
    def update_game(
        self,
        game_id: int,
        schema: GameUpdate,
    ) -> Game:

        game = self.get_game(game_id)

        if schema.title is None and schema.author is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.title is not None:
            game.title = schema.title

        if schema.author is not None:
            game.author = schema.author

        if schema.prev is not None:
            game.prev = schema.prev
        """дипсик"""
        if schema.category_id is not None:
            # Проверяем, существует ли категория
            category = self.cat_repository.get_by_id(schema.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with id {schema.category_id} not found"
                )
            game.category_id = schema.category_id

        """дипсик"""
        return self.repository.update(game)

    def delete_game(self, game_id: int) -> None:
        game = self.get_game(game_id)

        self.repository.delete(game)