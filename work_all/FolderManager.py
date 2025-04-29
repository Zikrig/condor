from os import makedirs, path, remove
from pathlib import Path
import csv
from shutil import copytree, move

from work_all import Logger
from work_all.db_work import Posts

class FolderManager:
    def __init__(self, logging: Logger.Logger, posts: Posts.Posts):
        self.base_path = 'data'
        self.content_path = self.base_path + '/content'
        self.to_add_path = self.base_path + '/to_add'
        self.table_path = self.to_add_path + '/table_update.csv'

        # self.logpath = self.content_path + '/logs' 
        
        self.images_to = self.content_path + '/images'
        self.textes_to = self.content_path + '/textes'
        self.images_from = self.to_add_path + '/images'
        self.textes_from = self.to_add_path + '/textes'
        
        self._ensure_folders()
        self.log = logging
        self.posts = posts
        
    def _ensure_folders(self):
        folders = [
            self.images_to,
            self.textes_to,
            self.images_from,
            self.textes_from
        ]
        
        for folder in folders:
            makedirs(folder, exist_ok=True)
            
        if not path.exists(self.table_path):
            with open(self.table_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['txt_path', 'img_path'])
                
    def process_texts(self):
        textpath = Path(self.textes_from)
        if not textpath.exists() or not textpath.is_dir():
            return
            
        for theme_folder in textpath.iterdir():
            if not theme_folder.is_dir():
                continue
            
            theme = theme_folder.name
            
            copytree(self.textes_from, self.textes_to, dirs_exist_ok=True)
            
            for text_file in theme_folder.iterdir():
                if not text_file.is_file():
                    continue
                try:
                    with open(text_file, 'r', encoding='utf-8') as f:
                        text = f.read()
                    self.posts.add(theme=theme, text=text, txt_path=text_file.name)
                    remove(text_file)
                except Exception as e:
                    self.log.log_to_file(f"Ошибка при обработке {text_file}: {str(e)}")
    
    def process_images(self):
        imgpath = Path(self.images_from)
        if not imgpath.exists() or not imgpath.is_dir():
            return
        
        copytree(self.images_from, self.images_to, dirs_exist_ok=True)
        for img in imgpath.iterdir():
            remove(img)
            
    def put_data_to_csv(self, texts_dir: str, images_dir: str):
        text_files = []
        for theme_folder in Path(texts_dir).iterdir():
            if theme_folder.is_dir():
                text_files.extend([str(f) for f in theme_folder.iterdir() if f.is_file()])
                
        image_files = [str(f) for f in Path(images_dir).iterdir() if f.is_file()]
        
        self.log.log_to_file(f"Найдено текстовых файлов: {len(text_files)}")
        self.log.log_to_file(f"Найдено изображений: {len(image_files)}")
        
        if not text_files or not image_files:
            self.log.log_to_file("Не найдены файлы для создания пар")
            return
            
        pairs = []
        for i, text_file in enumerate(text_files):
            img_file = image_files[i % len(image_files)]
            pairs.append([text_file, img_file])
            
        try:
            with open(self.table_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['txt_path', 'img_path'])
                writer.writerows(pairs)
            self.log.log_to_file(f"Создано пар текст-изображение: {len(pairs)}")
        except Exception as e:
            self.log.log_to_file(f"Ошибка при записи в CSV: {str(e)}")
            
            
    def add_images_paths(self):
        if not path.exists(self.table_path):
            self.log.log_to_file(f"Файл с парами не найден: {self.table_path}")
            return
            
        try:
            with open(self.table_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    txt_path = row['txt_path']
                    img_path = row['img_path']
                    
                    img_full_path = path.join(self.images_to, img_path)
                    if not path.exists(img_full_path):
                        self.log.log_to_file(f"Изображение не найдено: {img_full_path}")
                        continue
                        
                    self.posts.add_img_path(txt_path, img_path)
                    
        except Exception as e:
            self.log.log_to_file(f"Ошибка при обработке пар из CSV: {str(e)}")