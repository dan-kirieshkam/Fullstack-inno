from sqlalchemy.orm import Session

from app.models.game import Game


class GameRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, game: Game) -> Game:
        return self._upsert(game)

    def update(self, game: Game) -> Game:
        return self._upsert(game)

    def _upsert(self, game: Game) -> Game:
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)

        return game

    def get_all(self) -> list[Game]:
        return self.db.query(Game).all()

    def get_by_id(
        self,
        game_id: int,
    ) -> Game | None:

        return (
            self.db.query(Game)
            .filter(Game.id == game_id)
            .first()
        )

    def delete(self, game: Game) -> None:
        self.db.delete(game)
        self.db.commit()