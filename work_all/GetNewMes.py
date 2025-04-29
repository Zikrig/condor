from work_all import Logger
from work_all.db_work import Posts, Consts


class GetNewMes:
    def __init__(self, 
                posts: Posts.Posts,
                consts: Consts.Consts,
                logger: Logger.Logger):
        self.posts = posts
        self.consts = consts
        self.logger = logger
        
        self._get_actual_themes()
        
        
    def _get_actual_themes(self):
        themes_actual = self.posts.get_unique_themes()
        
        # Получает сведения из consts - последнее положение поста
        consts_actual = self.consts.get_consts_by_opt('now')
    
        # Получает количество сообщений по каждой теме
        consts_count = self.consts.get_consts_by_opt('count')
        
        # Проверяем каждую актуальную тему
        for theme in themes_actual:
            theme_name = theme["theme"]
            theme_count = theme["count"]
            
            # Проверяем есть ли тема в now
            theme_in_now = False
            for const in consts_actual:
                if const["name"] == theme_name:
                    theme_in_now = True
                    break
                    
            # Если темы нет в now, добавляем ее
            if not theme_in_now:
                self.consts.add_const(theme_name, 'now', -1)
                
            # Проверяем/обновляем количество постов для темы
            theme_in_count = False
            for const in consts_count:
                if const["name"] == theme_name:
                    theme_in_count = True
                    if const["meaning"] != theme_count:
                        self.consts.update_const(theme_name, 'count', theme_count)
                    break
                    
            # Если темы нет в count, добавляем ее
            if not theme_in_count:
                self.consts.add_const(theme_name, 'count', theme_count)
        
        self.themes_actual = self.posts.get_unique_themes()
        self.themes_actual = self.posts.get_unique_themes()
        self.consts_actual = self.consts.get_consts_by_opt('now')
        self.consts_count = self.consts.get_consts_by_opt('count')
                
    def increment_theme_position(self, theme_name: str) -> bool:
        # Получаем текущую позицию для темы
        current_pos = self.consts.get_const_by_name_and_opt(theme_name, 'now')
        
        if not current_pos and type(current_pos) != int:
            self.logger.log_to_file(f"Не удалось найти ничего по теме {theme_name} и 'now")
            return
        
        # Проверяем есть ли следующий пост
        next_post = self.posts.get_next_by_theme(theme_name, current_pos + 1)
        # print(next_post)
        # print(f'Это следующий пост после {current_pos}')
        
        if next_post is None:
            # Если следующего поста нет, обнуляем позицию
            self.consts.update_const(theme_name,'now', -1)
            self.logger.log_to_file(f"Следующий пост не найден для темы {theme_name}. Позиция обнулена.")
            return False
        else:
            # Если есть следующий пост, увеличиваем позицию
            self.consts.update_const(theme_name, 'now', next_post['id'])
            return True