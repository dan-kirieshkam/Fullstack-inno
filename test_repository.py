from app.database import Base, SessionLocal, engine
from app.models.game import Game
from app.repositories.game_repository import GameRepository

Base.metadata.create_all(bind=engine)

db = SessionLocal()

repository = GameRepository(db)

game = Game(
    title="halyl",
    previe="третьей халвы не будет",
)

repository.create(game)

games = repository.get_all()

for game in games:
    print(game.id, game.title, game.previe)

db.close()