import shutil
import os
import sys

foldername = sys.argv[1]
version = sys.argv[2]


# Исходная папка и имя файла
source_folder = rf"{foldername}"
file_name = rf"{version}.cf"  # Укажите имя файла, который нужно скопировать

# Целевая папка
destination_folder = r"D:\cf"

try:
    # Формируем полный путь к исходному файлу
    source_path = os.path.join(source_folder, file_name)
    
    # Формируем полный путь к целевому файлу
    destination_path = os.path.join(destination_folder, file_name)
    
    # Проверяем существование исходной папки и файла
    if not os.path.exists(source_folder):
        print(f"Исходная папка не существует: {source_folder}")
    elif not os.path.exists(source_path):
        print(f"Файл не найден: {source_path}")
    else:
        # Создаем целевую папку, если она не существует
        os.makedirs(destination_folder, exist_ok=True)
        
        # Копируем файл
        shutil.copy2(source_path, destination_path)
        print(f"Файл успешно скопирован из {source_path} в {destination_path}")

except Exception as e:
    print(f"Произошла ошибка: {str(e)}")