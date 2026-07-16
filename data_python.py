import json
from app.models.game import Game
from app.database import SessionLocal
from app.models.favorite import Favorite
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ВАЖНО: импортируйте все модели ДО создания сессии
from app.models import User, Game, Favorite  # или импортируйте все модели
# from app.db.session import SessionLocal

db = SessionLocal()
with open("books_with_working_images.json", "r", encoding="utf-8") as file:
    data = json.load(file)

db = SessionLocal()

try:
    for item in data:
        existing = db.query(Game).filter_by(id=item["id"]).first()
        
        if existing:
            existing.title = item.get("title", "Unknown")
            existing.publisher = item.get("publisher", "Unknown")
            existing.short_description = item.get("short_description", "")
            existing.genre = item.get("genre", "Unknown")
            existing.release_date = str(item.get("release_date", "Unknown"))
            existing.thumbnail = str(item.get("thumbnail", "Unknown"))
        else:
            game = Game(
                id=item["id"],
                title=item.get("title", "Unknown"),
                publisher=item.get("publisher", "Unknown"),
                short_description=item.get("short_description", ""),
                genre=item.get("genre", "Unknown"),
                release_date=str(item.get("release_date", "Unknown")),
                thumbnail=str(item.get("thumbnail", "Unknown")),
            )
            db.add(game)
    
    db.commit()

except Exception as e:
    db.rollback()
    raise e

finally:
    db.close()