from random import randint, seed
from os import remove
from os import path as p

from work_all.db_work.DBLow import DBLow
from work_all import Logger

class Posts:
    def __init__(self, db: DBLow, name: str, logger: Logger.Logger):
        # создаем messages
        self.name = name
        self.db = db
        
        self.logger = logger
        
        self._create_if_not_exist()
        seed()

    def _is_exist(self):
        result = self.db.get(f"SELECT to_regclass('{self.name}')")[0]
        self.logger.log_to_file(str(result))
        if result is None:
            return False
        if len(result) == 0:
            return False
        return bool(result)

    def _create_if_not_exist(self):
        self.logger.log_to_file(f'Надо ли создавать таблицу {self.name}')
        if not self._is_exist():
            self.logger.log_to_file(f'Да, надо')
            self.db.send(f"""
            CREATE TABLE {self.name} (
                id SERIAL PRIMARY KEY,
                txt_path TEXT,
                img_path TEXT,
                theme TEXT,
                text TEXT
            )
            """)

    def _get_count(self):
        # Получение количества записей в таблице
        result = self.db.get(f"""
        SELECT COUNT(*)
        FROM {self.name}
        """)
        return result[0] if result else 0

    def add(self, theme: str, text: str, txt_path: str = None):
        self.logger.log_to_file(f'Добавляем элемент с путем {txt_path}')
        # Добавляем запись в таблицу
        return self.db.send(f"""
        INSERT INTO {self.name} (theme, text, txt_path)
        VALUES ('{theme}', '{text}', '{txt_path}')
        """)

    def add_img_path(self, txt_path: str, img_path: str):
        # Добавляем путь к изображению по пути к тексту
        return self.db.send(f"""
        UPDATE {self.name}
        SET img_path = '{img_path}'
        WHERE txt_path = '{txt_path}'
        """)

    def get_by_id(self, id: int):
        # Получение записи по id
        result = self.db.get(f"""
        SELECT id, txt_path, img_path, theme, text
        FROM {self.name}
        WHERE id = {id}
        """)
        
        if not result:
            return None
            
        return {
            "id": result[0],
            "txt_path": result[1], 
            "img_path": result[2],
            "theme": result[3],
            "text": result[4]
        }

    def get_by_theme(self, theme: str):
        # Получение записей по теме
        result = self.db.get_many(f"""
        SELECT id, txt_path, img_path, theme, text
        FROM {self.name}
        WHERE theme = '{theme}'
        """)
        
        if not result:
            return []
            
        return [
            {
                "id": row[0],
                "txt_path": row[1],
                "img_path": row[2], 
                "theme": row[3],
                "text": row[4]
            }
            for row in result
        ]

    def get_last_n(self, n: int):
        # Получение последних n записей
        result = self.db.get_many(f"""
        SELECT id, txt_path, img_path, theme, text
        FROM {self.name}
        ORDER BY id DESC
        LIMIT {n}
        """)
        
        if not result:
            return []
            
        return [
            {
                "id": row[0],
                "txt_path": row[1],
                "img_path": row[2],
                "theme": row[3],
                "text": row[4]
            }
            for row in result
        ]

    def delete(self, id: int):
        # Удаление записи по id
        return self.db.send(f"""
        DELETE FROM {self.name}
        WHERE id = {id}
        """)

    def get_unique_themes(self):
        # Получение всех уникальных тем и количества постов для каждой темы
        result = self.db.get_many(f"""
        SELECT theme, COUNT(*) as count
        FROM {self.name}
        GROUP BY theme
        ORDER BY theme
        """)
        
        if not result:
            return []
            
        return [{"theme": row[0], "count": row[1]} for row in result]
    
    def get_next_by_theme(self, theme: str, last_id: int):
        # Получение следующей записи по теме после указанного id
        result = self.db.get(f"""
        SELECT id, txt_path, img_path, theme, text
        FROM {self.name}
        WHERE theme = '{theme}' AND id >= {last_id}
        ORDER BY id
        LIMIT 1
        """)
        
        if not result:
            return None
            
        return {
            "id": result[0],
            "txt_path": result[1],
            "img_path": result[2],
            "theme": result[3], 
            "text": result[4]
        }