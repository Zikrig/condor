import psycopg2
from psycopg2 import Error
from work_all import Logger

class DBLow:
    def __init__(self, params, logger: Logger.Logger):
        self.db_name, self.user, self.password, self.host, self.port = params
        self.logger = logger
        self._create_if_not_exist()
        
    def _makezap(self, basename=False):
        zap_db_name = 'postgres' if basename else self.db_name
        
        conn = psycopg2.connect(
                dbname = zap_db_name,
                user = self.user,
                password = self.password,
                host = self.host,
                port = self.port
            )
        conn.autocommit = True
        return conn

    def _test(self):
        try:
            conn = self._makezap(True)
            cursor = conn.cursor()
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.db_name}';")
            exists = cursor.fetchone()
            cursor.close()
            conn.close()
            if exists is not None:
                return exists[0] == 1
            return False
        except (Exception, Error) as error:
            self.logger.log_to_file(f'Ошибка подключения: {error}')
            return False

    def _create_if_not_exist(self):
        bd_existance = self._test()
        if not bd_existance:
            try:
                conn = self._makezap(True)
                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE {self.db_name};")
                cursor.close()
                conn.close()
                self.logger.log_to_file(f'База данных {self.db_name} создана')
            except (Exception, Error) as error:
                self.logger.log_to_file(f'Ошибка создания БД: {error}')
            

    def get(self, zap):
        try:
            conn = self._makezap()
            
            cursor = conn.cursor()
            cursor.execute(zap)
            conn.commit()  
            res = cursor.fetchone()
            if res == None:
                res = []
            cursor.close()
            conn.close()
        except (Exception, Error) as error:
            res = []
            self.logger.log_to_file(f'Ошибка {error}')
            # res = error
        finally:
            return res

    def get_many(self, zap):
        try:
            conn = self._makezap()
            
            cursor = conn.cursor()
            cursor.execute(zap)
            conn.commit()  
            res = cursor.fetchall()
            if res == None:
                res = []
            cursor.close()
            conn.close()
        except (Exception, Error) as error:
            res = []
            self.logger.log_to_file(f'Ошибка {error}')
            # res = error
        finally:
            return res
        
    def send(self, zap):
        try:
            conn = self._makezap()
            
            cursor = conn.cursor()
            cursor.execute(zap)
            conn.commit()
            return True
        except (Exception, Error) as error:
            res = error
            self.logger.log_to_file(f'Ошибка {error}')
            return res