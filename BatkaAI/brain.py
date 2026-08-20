import requests
import json


def understand_command(command):
    prompt = f"""
Ты — мозг локального помощника Batka AI.

Определи намерение пользователя и верни ТОЛЬКО JSON.
Никакого дополнительного текста.

Доступные действия:

OPEN_APP
OPEN_BROWSER
SEARCH_WEB
CREATE_FILE
OPEN_FOLDER
CREATE_FOLDER
LIST_FILES
HELLO
HELP
EXIT
UNKNOWN

Формат ответа:

{{
    "action": "",
    "query": "",
    "filename": "",
    "content": "",
    "app": "",
    "folder": "",
    "folder_name": ""
}}

ПРАВИЛА:

1. Если пользователь хочет открыть или запустить программу:
   action = "OPEN_APP"
   app = короткое название программы.

Примеры:
блокнот -> notepad
калькулятор -> calculator
paint -> paint
проводник -> explorer
steam -> steam


2. Если пользователь хочет открыть браузер:
   action = "OPEN_BROWSER"


3. Если пользователь хочет что-либо найти в интернете:
   action = "SEARCH_WEB"
   query = то, что нужно найти.


4. Если пользователь просит создать текстовый файл:
   action = "CREATE_FILE"
   filename = имя файла
   content = текст для файла

Если расширение файла не указано, добавь .txt.


5. Если пользователь хочет открыть папку:
   action = "OPEN_FOLDER"
   folder = название стандартной папки.

Используй следующие значения:

рабочий стол -> desktop
загрузки -> downloads
документы -> documents
изображения -> pictures
музыка -> music
видео -> videos

Пример:

Пользователь:
открой Загрузки

Ответ:
{{
    "action": "OPEN_FOLDER",
    "query": "",
    "filename": "",
    "content": "",
    "app": "",
    "folder": "downloads",
    "folder_name": ""
}}


6. Если пользователь хочет создать папку:
   action = "CREATE_FOLDER"
   folder = где создать папку
   folder_name = название новой папки

Пример:

Пользователь:
создай папку Тест на рабочем столе

Ответ:
{{
    "action": "CREATE_FOLDER",
    "query": "",
    "filename": "",
    "content": "",
    "app": "",
    "folder": "desktop",
    "folder_name": "Тест"
}}


7. Если пользователь хочет посмотреть список файлов в папке:
   action = "LIST_FILES"
   folder = название папки

Пример:

Пользователь:
покажи файлы в Загрузках

Ответ:
{{
    "action": "LIST_FILES",
    "query": "",
    "filename": "",
    "content": "",
    "app": "",
    "folder": "downloads",
    "folder_name": ""
}}


8. Если пользователь приветствует:
   action = "HELLO"


9. Если пользователь просит помощь:
   action = "HELP"


10. Если пользователь хочет завершить программу:
    action = "EXIT"


11. Если намерение пользователя непонятно:
    action = "UNKNOWN"


ВАЖНО:

Для всех полей, которые не нужны для конкретной команды,
возвращай пустую строку.

Команда пользователя:
{command}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3:4b",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    raw_result = data.get("response") or data.get("thinking", "")

    result = json.loads(raw_result)

    return result


if __name__ == "__main__":
    test_command = input("Тестовая команда: ")

    result = understand_command(test_command)

    print("Результат:", result)
    print("Действие:", result.get("action", ""))
    print("Программа:", result.get("app", ""))
    print("Запрос:", result.get("query", ""))
    print("Имя файла:", result.get("filename", ""))
    print("Содержимое:", result.get("content", ""))
    print("Папка:", result.get("folder", ""))
    print("Название новой папки:", result.get("folder_name", ""))