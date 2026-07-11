import sqlite3

def add_columns():
    conn = sqlite3.connect('data.db')  # укажите путь к вашей БД
    cursor = conn.cursor()
    
    # Проверяем существующие колонки
    cursor.execute("PRAGMA table_info(users)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    # Добавляем только те колонки, которых нет
    if 'name' not in existing_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN name VARCHAR")
        print("✓ Добавлена колонка name")
    
    if 'bursday' not in existing_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN bursday VARCHAR")
        print("✓ Добавлена колонка bursday")
    
    if 'prev' not in existing_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN prev VARCHAR")
        print("✓ Добавлена колонка prev")
    
    conn.commit()
    conn.close()
    print("✅ Все колонки добавлены!")

if __name__ == "__main__":
    add_columns()