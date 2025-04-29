import os
import shutil

def capitalize_filenames(directory_path):
    """
    Переименовывает все файлы в директории, делая их имена с большой буквы.
    Например, 'test_file.txt' станет 'Test_file.txt'
    
    Args:
        directory_path (str): Путь к директории для обработки
    """
    if not os.path.exists(directory_path):
        print(f"Директория {directory_path} не существует")
        return
    
    # Получаем список всех файлов в директории
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    if not files:
        print("В директории нет файлов")
        return
    
    # Создаем временную директорию для безопасного переименования
    temp_dir = os.path.join(directory_path, "temp_capitalize")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    try:
        # Переименовываем файлы во временную директорию
        for filename in files:
            # Разделяем имя файла и расширение
            name, ext = os.path.splitext(filename)
            
            # Делаем первую букву заглавной
            new_name = name.capitalize() + ext
            
            old_path = os.path.join(directory_path, filename)
            temp_path = os.path.join(temp_dir, new_name)
            
            shutil.move(old_path, temp_path)
            print(f"Файл {filename} временно переименован в {new_name}")
        
        # Перемещаем файлы обратно с новыми именами
        for filename in os.listdir(temp_dir):
            old_path = os.path.join(temp_dir, filename)
            new_path = os.path.join(directory_path, filename)
            
            shutil.move(old_path, new_path)
            print(f"Файл переименован в {filename}")
            
    except Exception as e:
        print(f"Произошла ошибка при переименовании: {str(e)}")
    finally:
        # Удаляем временную директорию
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    # Пример использования
    directory = "data/to_add_init/images"  # Текущая директория
    capitalize_filenames(directory) 