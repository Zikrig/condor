from os import getenv
from dotenv import load_dotenv
import asyncio

from work_all.db_work import DBLow, Posts, Consts

from work_all import FolderManager, Logger, GetNewMes, TelegramSender
from work_all.Scheduler import Scheduler
from schedule_config import SCHEDULE_CONFIG

logger = Logger.Logger('data/log')

# Создание, если нет:
# БД
load_dotenv('.env')

db_params = (
    getenv('DB_NAME'),
    getenv('DB_USER'), 
    getenv('DB_PASSWORD'),
    getenv('DB_HOST'),
    getenv('DB_PORT')
)

db = DBLow.DBLow(db_params)

#   Таблицы Posts
posts = Posts.Posts(db, 'posts')
#   Таблицы Consts
consts = Consts.Consts(db, 'consts')

print(posts.add('test', 'test', 'test'))
print(posts.get_last_n(5))