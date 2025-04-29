from work_all.db_work.DBLow import DBLow
from work_all import Logger

class Consts:
    def __init__(self, db: DBLow, name: str, logger: Logger.Logger):
        self.name = name
        self.db = db
        self.logger = logger
        
        self._create_if_not_exist()

    def _is_exist(self):
        result = self.db.get(f"SELECT to_regclass('{self.name}')")
        if not result:
            return False
        if not result[0]:
            return False 
        result = result[0]
        
        if len(result) == 0:
            return False
        return bool(result)

    def _create_if_not_exist(self):
        # Создание таблицы, если её нет
        if not self._is_exist():
            self.db.send(f"""
            CREATE TABLE {self.name} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                opt VARCHAR(255),
                meaning INTEGER
            )
            """)

    def add_const(self, name: str, opt: str, meaning: int):
        # Добавление новой константы
        return self.db.send(f"""
        INSERT INTO {self.name} (name, opt, meaning)
        VALUES ('{name}', '{opt}', {meaning})
        """)

    def get_const_by_name_and_opt(self, name: str, opt: str):
        # Получение значения константы по имени
        result = self.db.get(f"""
        SELECT meaning FROM {self.name} WHERE name = '{name}' AND opt = '{opt}'
        """)
        return result[0] if result != None else None

    def get_all_consts(self):
        # Получение всех констант
        result = self.db.get_many(f"""
        SELECT id, name, opt, meaning
        FROM {self.name}
        """)
        
        if not result:
            return []
            
        return [
            {
                "id": row[0],
                "name": row[1],
                "opt": row[2],
                "meaning": row[3]
            }
            for row in result
        ]

    def get_consts_by_opt(self, opt: str):
        # Получение констант по opt
        result = self.db.get_many(f"""
        SELECT id, name, opt, meaning
        FROM {self.name}
        WHERE opt = '{opt}'
        """)
        
        if not result:
            return []
            
        return [
            {
                "id": row[0],
                "name": row[1],
                "opt": row[2],
                "meaning": row[3]
            }
            for row in result
        ]

    def update_const(self, name: str, opt: str, meaning: int):
        # Обновление значения константы
        return self.db.send(f"""
        UPDATE {self.name} SET meaning = {meaning}
        WHERE name = '{name}' and opt = '{opt}'
        """)

    def delete_const(self, name: str):
        # Удаление константы
        return self.db.send(f"""
        DELETE FROM {self.name} WHERE name = '{name}'
        """)
