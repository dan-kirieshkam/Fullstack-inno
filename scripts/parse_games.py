import json
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.game import Game  # или from app.models import Game

# Путь к вашему JSON файлу
JSON_FILE_PATH = Path("data/games.json")  # укажите правильный путь

def load_json_data(file_path: Path) -> list[dict]:
    """Загружает данные из JSON файла"""
    if not file_path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден!")
    
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    
    # Если JSON это список
    if isinstance(data, list):
        return data
    # Если JSON это словарь с ключами
    elif isinstance(data, dict):
        # Если есть ключ с данными (например, "games" или "results")
        if "games" in data:
            return data["games"]
        elif "results" in data:
            return data["results"]
        else:
            # Возвращаем все значения словаря, если это похоже на данные
            first_key = next(iter(data))
            if isinstance(data[first_key], dict):
                return list(data.values())
            else:
                return [data]
    else:
        raise ValueError("Неизвестный формат JSON")

def parse_game_data(game_data: dict) -> dict:
    """Преобразует данные из JSON в формат для модели Game"""
    
    # Обработка жанра - если приходит строка, оставляем как есть
    genre = game_data.get("genre", "Unknown")
    
    # Обработка даты выпуска
    release_date = game_data.get("release_date")
    if release_date:
        # Если дата в формате "2022-10-04"
        try:
            # Преобразуем в строку, так как в модели release_date: Mapped[str]
            release_date = str(release_date)
        except:
            release_date = "Unknown"
    else:
        release_date = "Unknown"
    
    # Формируем данные для модели
    return {
        "id": game_data.get("id"),  # Если хотим использовать внешний ID
        "title": game_data.get("title", "Unknown"),
        "publisher": game_data.get("publisher", "Unknown"),
        "short_description": game_data.get("short_description", ""),
        "genre": genre,  # У вас genre: Mapped[int], но в данных это строка
        "release_date": release_date,
    }

def import_games_to_db(json_data: list[dict], session: Session) -> tuple[int, int]:
    """Импортирует игры в базу данных"""
    
    games_created = 0
    games_updated = 0
    games_skipped = 0
    
    for item in json_data:
        try:
            # Парсим данные
            game_data = parse_game_data(item)
            
            # Проверяем, существует ли игра с таким ID
            existing_game = session.query(Game).filter_by(id=game_data["id"]).first()
            
            if existing_game:
                # Обновляем существующую запись
                for key, value in game_data.items():
                    if key != "id":  # Не обновляем ID
                        setattr(existing_game, key, value)
                games_updated += 1
            else:
                # Создаем новую запись
                new_game = Game(**game_data)
                session.add(new_game)
                games_created += 1
            
            # Коммитим каждые 100 записей для оптимизации
            if (games_created + games_updated) % 100 == 0:
                session.commit()
                
        except Exception as e:
            print(f"Ошибка при импорте игры {item.get('id', 'Unknown')}: {e}")
            games_skipped += 1
    
    # Финальный коммит
    session.commit()
    
    return games_created, games_updated, games_skipped

def main():
    print("🔄 Начинаю импорт данных...")
    
    # Загружаем JSON
    try:
        json_data = load_json_data(JSON_FILE_PATH)
        print(f"✅ Загружено записей из JSON: {len(json_data)}")
    except Exception as e:
        print(f"❌ Ошибка загрузки JSON: {e}")
        return
    
    # Создаем сессию БД
    session = SessionLocal()
    
    try:
        # Импортируем данные
        created, updated, skipped = import_games_to_db(json_data, session)
        
        print("\n📊 Результаты импорта:")
        print(f"   ✅ Создано новых игр: {created}")
        print(f"   🔄 Обновлено существующих: {updated}")
        print(f"   ⚠️ Пропущено с ошибками: {skipped}")
        print(f"   📈 Всего обработано: {created + updated + skipped}")
        
    except Exception as e:
        print(f"❌ Ошибка при импорте: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()