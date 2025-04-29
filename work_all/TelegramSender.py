from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from work_all import FolderManager, Logger, GetNewMes
import asyncio
from os import path

class TelegramSender:
    def __init__(self, 
                token: str,
                group_ids: str,  # Строка с ID каналов через запятую
                group_codes: str,  # Строка с кодовыми словами для групп через запятую
                logger: Logger.Logger,
                foldman: FolderManager.FolderManager,
                getnewmes: GetNewMes.GetNewMes):
        
        self.token = token
        self.group_ids = [int(id.strip()) for id in group_ids.split(',')]  # Преобразуем строку в список ID
        self.group_codes = [code.strip() for code in group_codes.split(',')]  # Преобразуем строку в список кодовых слов
        
        # Создаем словарь для быстрого доступа к кодовому слову по ID группы
        self.group_id_to_code = {group_id: code for group_id, code in zip(self.group_ids, self.group_codes)}
        
        self.logger = logger
        self.foldman = foldman
        self.getnewmes = getnewmes
        
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher()
        
        self.router = Router()
        
    async def main(self):
        self.dp.include_router(self.router)
        # await self.send_message_by_id(6436, -1002389077797)
        
        await self.dp.start_polling(self.bot)
        
    async def sendmes(self, text, group_id=None):
        # Если указан конкретный group_id, отправляем только в него
        if group_id is not None:
            try:
                await self.bot.send_message(chat_id=group_id, text=text, parse_mode='MARKDOWN')
                self.logger.log_to_file(f"Сообщение отправлено в группу {group_id}")
            except Exception as e:
                self.logger.log_to_file(f"Ошибка при отправке в группу {group_id}: {e}")
            return
            
        # Иначе отправляем во все группы
        for group_id in self.group_ids:
            try:
                await self.bot.send_message(chat_id=group_id, text=text, parse_mode='MARKDOWN')
                self.logger.log_to_file(f"Сообщение отправлено в группу {group_id}")
            except Exception as e:
                self.logger.log_to_file(f"Ошибка при отправке в группу {group_id}: {e}")
    
    async def sendpic(self, text, image='', group_id=None):
        if not image:
            image = ''
            
        if len(text) < 1024:    
            await self.sendpic_old(text, image, group_id)
            return
         
        try:
            await self.sendmes(text, group_id)
            imgpath = self.foldman.images_to + '/' + image
            if not path.exists(imgpath):
                return
                
            # Если указан конкретный group_id, отправляем только в него
            if group_id is not None:
                try:
                    await self.bot.send_photo(chat_id=group_id, photo=types.FSInputFile(imgpath))
                    self.logger.log_to_file(f"Сообщение с фото отправлено в группу {group_id}")
                except Exception as e:
                    self.logger.log_to_file(f"Ошибка при отправке фото в группу {group_id}: {e}")
                return
                
            # Иначе отправляем во все группы
            for group_id in self.group_ids:
                try:
                    await self.bot.send_photo(chat_id=group_id, photo=types.FSInputFile(imgpath))
                    self.logger.log_to_file(f"Сообщение с фото отправлено в группу {group_id}")
                except Exception as e:
                    self.logger.log_to_file(f"Ошибка при отправке фото в группу {group_id}: {e}")
        except Exception as e:
            self.logger.log_to_file(f"Ошибка при отправке с фото. Попробуем обычное: {e}")
            await self.sendmes(text, group_id)
    
    async def sendpic_old(self, text, image='', group_id=None):
        try:
            imgpath = self.foldman.images_to + '/' + image
            if not path.exists(imgpath):
                raise Exception
                        
            # Если указан конкретный group_id, отправляем только в него
            if group_id is not None:
                try:
                    await self.bot.send_photo(chat_id=group_id, photo=types.FSInputFile(imgpath), caption=text, parse_mode='MARKDOWN')
                    self.logger.log_to_file(f"Сообщение с фото отправлено в группу {group_id}")
                except Exception as e:
                    self.logger.log_to_file(f"Ошибка при отправке фото в группу {group_id}: {e}")
                    await self.sendmes(text, group_id)
                return
                
            # Иначе отправляем во все группы
            for group_id in self.group_ids:
                try:
                    await self.bot.send_photo(chat_id=group_id, photo=types.FSInputFile(imgpath), caption=text, parse_mode='MARKDOWN')
                    self.logger.log_to_file(f"Сообщение с фото отправлено в группу {group_id}")
                except Exception as e:
                    self.logger.log_to_file(f"Ошибка при отправке фото в группу {group_id}: {e}")
                    await self.sendmes(text, group_id)
        except Exception as e:
            self.logger.log_to_file(f"Ошибка при отправке с фото. Попробуем обычное: {e}")
            await self.sendmes(text, group_id)
            
    async def send_next_message_by_theme(self, theme: str, group_id=None):
        try:
            
            self.logger.log_to_file(f"Отправлено {theme}: {group_id}")

            last_by_theme = -50
            # Обновляем значения констант перед каждой отправкой
            self.getnewmes._get_actual_themes()
            
            # Если указан конкретный group_id, используем его кодовое слово
            if group_id is not None and group_id in self.group_id_to_code:
                group_code = self.group_id_to_code[group_id]
                # theme_with_code = f"{theme}_{group_code}"
                theme_with_code = theme
            else:
                theme_with_code = theme
                
            self.logger.log_to_file(f"Отправлено {theme_with_code}: {group_id}")
            
            for th in self.getnewmes.consts_actual:
               if th['name'] == theme_with_code:
                    last_by_theme = th['meaning']
                    self.logger.log_to_file(f"Найдена константа")
                    break
               
            if last_by_theme == -50:
                self.logger.log_to_file(f"Почему-то не получается найти сообщения для темы {theme_with_code}, хотя должны быть")
                raise Exception()
            
            mes = self.getnewmes.posts.get_next_by_theme(theme_with_code, last_by_theme)
            await self.sendpic(mes['text'], mes['img_path'], group_id)
            self.getnewmes.increment_theme_position(theme_with_code)
        except Exception as e:
            self.logger.log_to_file(f"Ошибка при попытке отправить сообщение по теме {theme_with_code} : {e}")

    async def send_message_by_id(self, post_id: int, group_id=None):
        try:
            mes = self.getnewmes.posts.get_by_id(post_id)
            if mes is None:
                self.logger.log_to_file(f"Пост с id {post_id} не найден")
                return
                
            await self.sendpic(mes['text'], mes['img_path'], group_id)
            self.logger.log_to_file(f"Отправлен пост с id {post_id}")
        except Exception as e:
            self.logger.log_to_file(f"Ошибка при отправке поста с id {post_id}: {e}")