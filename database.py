import sqlite3
import logging

logger = logging.getLogger("JARVIS_LOGGER")

def init_db():
    """Создает базу данных и таблицу пользователей, если их нет."""
    try:
        with sqlite3.connect("jarvis_memory.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logger.info("База данных успешно инициализирована.")
    except Exception as e:
        logger.error(f"Ошибка при инициализации БД: {e}")

def set_owner_name(name):
    """Записывает имя владельца в базу."""
    with sqlite3.connect("jarvis_memory.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('owner_name', ?)", (name,))
        conn.commit()

def get_owner_name():
    """Возвращает имя владельца или None."""
    with sqlite3.connect("jarvis_memory.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = 'owner_name'")
        result = cursor.fetchone()
        return result[0] if result else None