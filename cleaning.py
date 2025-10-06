import shutil
import os

def clear_folder(folder_path):
    # Проверяем, существует ли папка
    if not os.path.exists(folder_path):
        print(f"Папка {folder_path} не существует")
        return
    
    # Проходим по всем элементам в папке
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            # Если это файл - удаляем
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Удален файл: {item_path}")
            # Если это папка - удаляем рекурсивно
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Удалена папка: {item_path}")
        except Exception as e:
            print(f"Ошибка при удалении {item_path}: {str(e)}")

# Пути к папкам
folder1_path = r"D:\cf"
folder2_path = r"D:\dt"

# Очищаем первую папку
print("Очистка cf папки:")
clear_folder(folder1_path)

# Очищаем вторую папку
print("\nОчистка dt папки:")
clear_folder(folder2_path)