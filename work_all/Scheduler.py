from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from work_all import Logger, TelegramSender

import asyncio

class Scheduler:
    def __init__(self, telegram: TelegramSender.TelegramSender, logger: Logger.Logger):
        self.telegram = telegram
        self.logger = logger
        self.scheduler = AsyncIOScheduler()
        
    def add_task(self, schedule: dict, task_type: str, params: dict):
        """
        Добавляет задачу в расписание
        schedule: словарь с параметрами расписания (hour, minute, day_of_week)
        task_type: тип задачи ('theme' или 'post_id')
        params: параметры задачи (например {'theme': 'content'} или {'post_id': 186})
        """
        if task_type == 'theme':
            job = self.scheduler.add_job(
                self.telegram.send_next_message_by_theme,
                CronTrigger(
                    hour=schedule.get('hour'),
                    minute=schedule.get('minute'),
                    day_of_week=schedule.get('day_of_week')
                ),
                args=[params['theme']]
            )
        elif task_type == 'post_id':
            job = self.scheduler.add_job(
                self.telegram.send_message_by_id,
                CronTrigger(
                    hour=schedule.get('hour'),
                    minute=schedule.get('minute'),
                    day_of_week=schedule.get('day_of_week')
                ),
                args=[params['post_id']]
            )
            
        self.logger.log_to_file(f"Добавлена задача {task_type} с расписанием {schedule}")
        
    async def run_schedule(self):
        self.scheduler.start()
        # Держим планировщик запущенным
        while True:
            await asyncio.sleep(60) 