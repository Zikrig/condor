from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from work_all import FolderManager, Logger, GetNewMes
import asyncio
from os import path

class TelegramSender:
    def __init__(self, 
                token: str,
                group_id: int,
                logger: Logger.Logger,
                foldman: FolderManager.FolderManager,
                getnewmes: GetNewMes.GetNewMes):
        
        self.token = token
        self.group_id = group_id
        
        self.logger = logger
        self.foldman = foldman
        self.getnewmes = getnewmes
        
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher()
        
        self.router = Router()
        
    async def main(self):
        self.dp.include_router(self.router)
        # await self.sendmes('test')
        await self.send_next_message_by_theme('content')
        await self.send_next_message_by_theme('content')
        # await self.send_next_message_by_theme('content')
        # await self.send_next_message_by_theme('content')
        # await self.send_next_message_by_theme('content')
        # await self.send_next_message_by_theme('content')
        # await self.send_next_message_by_theme('content')
        # await self.send_next_message_by_theme('content')
        # await self.send_next_message_by_theme('content')
        # await self.send_next_message_by_theme('content')
        # await self.send_next_message_by_theme('content')
        # await self.send_next_message_by_theme('content')
        
        await self.dp.start_polling(self.bot)
        
        
    async def sendmes(self, text):
        try:
            await self.bot.send_message(chat_id=self.group_id, text=text, parse_mode='MARKDOWN')
            self.logger.log_to_file(f"Сообщение отправлено в группу {self.group_id}")
        except Exception as e:
            self.logger.log_to_file(f"Ошибка при отправке в группу {self.group_id}: {e}")
    
    async def sendpic(self, text, image=''):
        if len(text) < 1024:    
            await self.sendpic_old(self, text, image='')
            return
         
        try:
            await self.sendmes(text)
            imgpath = self.foldman.images_to + '/' + image
            if not path.exists(imgpath):
                return
            await self.bot.send_photo(chat_id=self.group_id, photo=types.FSInputFile(imgpath))
            self.logger.log_to_file(f"Сообщение с фото отправлено")
        except Exception as e:
            self.logger.log_to_file(f"Ошибка при отправке с фото. Попробуем обычное: {e}")
            await self.sendmes(text)
    
    async def sendpic_old(self, text, image=''):
        try:
            imgpath = self.foldman.images_to + '/' + image
            if not path.exists(imgpath):
                raise Exception
                        
            await self.bot.send_photo(chat_id=self.group_id, photo=types.FSInputFile(imgpath), caption=text, parse_mode='MARKDOWN')
            self.logger.log_to_file(f"Сообщение с фото отправлено")
        except Exception as e:
            self.logger.log_to_file(f"Ошибка при отправке с фото. Попробуем обычное: {e}")
            await self.sendmes(text)
            
    async def send_next_message_by_theme(self, theme: str):
        try:
            last_by_theme = -50
            # Обновляем значения констант перед каждой отправкой
            self.getnewmes._get_actual_themes()
            
            for th in self.getnewmes.consts_actual:
               if th['name'] == theme:
                   last_by_theme = th['meaning']
                   break
               
            if last_by_theme == -50:
                self.logger.log_to_file(f"Почему-то не получается найти сообщения, хотя должны быть")
                raise Exception()
            
            mes = self.getnewmes.posts.get_next_by_theme(theme, last_by_theme)
            await self.sendpic(mes['text'], mes['img_path'])
            self.getnewmes.increment_theme_position(theme)
        except Exception as e:
            self.logger.log_to_file(f"Ошибка при попытке отправить сообщение по теме {theme} : {e}")
        
        