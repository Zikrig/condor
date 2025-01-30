from os import getenv
from dotenv import load_dotenv
import asyncio

from work_all.db_work import DBLow, Posts, Consts

from work_all import FolderManager, Logger, GetNewMes, TelegramSender
from work_all.Scheduler import Scheduler
from schedule_config import SCHEDULE_CONFIG

# TODO
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

# Создание, если нет:
# /data
# /data/content
#               /images
#               /logs
#               /textes
# /data/to_add
#               /images
#               /textes
#               /table_update.csv
foldman = FolderManager.FolderManager(logger, posts)

# Вывод числа строк в таблице
posts_count = posts._get_count()
logger.log_to_file(f"В таблице сначала {posts_count}")

# Если textes непустой, то по папкам
#   Сохранить название папки как тему
#   По теме сохранить в таблицу тексты в папке
#   Если файл уже есть - лог
# слить textes с data/content/textes
foldman.process_texts()
# слить images ...
foldman.process_images()

# Создание csv
# foldman.put_data_to_csv(foldman.textes_to, foldman.images_to)


# Обойти csv построчно
#   Если картинки / текста нет - лог
#   обновить данные картинок к постам
# Удалить csv
foldman.add_images_paths()

# Вывод числа строк в таблице
posts_count = posts._get_count()
logger.log_to_file(f"В таблице в итоге {posts_count}")


# Получение из posts списка тем
# Если какой-то темы нет в Consts - добавлям ее туда
# Получаем все значения из Consts
getnewmes = GetNewMes.GetNewMes(posts, consts, logger)

# Реализуем функцию "Сделать шаг" - получить сообщение

# плюсануть константу
# getnewmes.increment_theme_position('content')



telegram_params = {
    'token': getenv('TOKEN'),
    'group_id': getenv('GROUP_ID'),
}

# print(telegram_params)
telegram = TelegramSender.TelegramSender(telegram_params['token'], telegram_params['group_id'], logger, foldman, getnewmes)
scheduler = Scheduler(telegram, logger)

# Добавляем задачи из конфигурации
for task_config in SCHEDULE_CONFIG:
    scheduler.add_task(
        task_config['schedule'],
        task_config['task_type'],
        task_config['params']
    )

if __name__ == "__main__":
    async def main():
        # Запускаем планировщик и бота одновременно
        await asyncio.gather(
            scheduler.run_schedule(),
            telegram.dp.start_polling(telegram.bot)
        )
    
    asyncio.run(main())

# telegram = TelegramWork.TelegramWork(telegram_params)

