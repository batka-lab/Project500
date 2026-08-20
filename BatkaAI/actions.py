import subprocess
import webbrowser
from pathlib import Path
from urllib.parse import quote_plus


def open_notepad():
    try:
        subprocess.Popen(["notepad.exe"])
        print("Блокнот успешно открыт.")
    except Exception as e:
        print(f"Ошибка при открытии блокнота: {e}")


def open_browser():
    try:
        subprocess.Popen(
            ["cmd", "/c", "start", "https://www.google.com"]
        )
        print("Браузер успешно открыт.")
    except Exception as e:
        print(f"Ошибка при открытии браузера: {e}")


def search_web(query):
    try:
        url = "https://www.google.com/search?q=" + quote_plus(query)

        webbrowser.open(url)

        print(f"Ищу в интернете: {query}")

    except Exception as e:
        print(f"Ошибка при поиске: {e}")


def create_file(filename, content):
    try:
        # Рабочий стол текущего пользователя
        desktop = Path.home() / "Desktop"

        # Полный путь к создаваемому файлу
        file_path = desktop / filename

        # Создаем файл и записываем текст
        file_path.write_text(
            content,
            encoding="utf-8"
        )

        # Сразу открываем созданный файл в Блокноте
        subprocess.Popen(
            ["notepad.exe", str(file_path)]
        )

        print(f"Файл создан и открыт: {file_path}")

    except Exception as e:
        print(f"Ошибка при создании файла: {e}")