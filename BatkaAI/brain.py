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
OPEN_FILE
READ_FILE
APPEND_FILE
FIND_FILE
OPEN_LATEST_FILE

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
    "folder_name": "",
    "extension": ""
}}

Правила:

1. Если пользователь хочет открыть или запустить программу:
   action = "OPEN_APP"
   app = короткое название программы.

Примеры:
блокнот -> notepad
калькулятор -> calculator
paint -> paint
проводник -> explorer
steam -> steam


2. Если пользователь просто хочет открыть браузер:
   action = "OPEN_BROWSER"


3. Если пользователь хочет найти информацию В ИНТЕРНЕТЕ:
   action = "SEARCH_WEB"
   query = поисковый запрос

Важно:
"найди в интернете Audi Q3" -> SEARCH_WEB
"найди файл диплом" -> НЕ SEARCH_WEB


4. Если пользователь просит создать новый текстовый файл:
   action = "CREATE_FILE"
   filename = имя файла
   content = текст, который нужно записать

Если расширение не указано, добавь .txt.


5. Если пользователь хочет открыть существующий файл:
   action = "OPEN_FILE"
   filename = имя файла или часть имени

Пример:
"открой файл Проверка.txt"

Ответ:
{{
    "action": "OPEN_FILE",
    "query": "",
    "filename": "Проверка.txt",
    "content": "",
    "app": "",
    "folder": "",
    "folder_name": "",
    "extension": ""
}}


6. Если пользователь хочет прочитать содержимое текстового файла:
   action = "READ_FILE"
   filename = имя файла или часть имени

Пример:
"прочитай файл Проверка.txt"


7. Если пользователь хочет ДОБАВИТЬ текст в существующий файл:
   action = "APPEND_FILE"
   filename = имя файла
   content = текст, который нужно добавить

Важно:
НЕ использовать CREATE_FILE для команды "добавь".

Пример:

Пользователь:
добавь в Проверка.txt текст Купить молоко

Ответ:
{{
    "action": "APPEND_FILE",
    "query": "",
    "filename": "Проверка.txt",
    "content": "Купить молоко",
    "app": "",
    "folder": "",
    "folder_name": "",
    "extension": ""
}}


8. Если пользователь хочет найти ФАЙЛ на компьютере:
   action = "FIND_FILE"
   filename = имя файла или часть имени

Пример:

Пользователь:
найди файл диплом

Ответ:
{{
    "action": "FIND_FILE",
    "query": "",
    "filename": "диплом",
    "content": "",
    "app": "",
    "folder": "",
    "folder_name": "",
    "extension": ""
}}


9. Если пользователь хочет открыть самый новый файл определенного типа:
   action = "OPEN_LATEST_FILE"
   extension = расширение файла без точки
   folder = папка, если она указана

Стандартные папки:

рабочий стол -> desktop
загрузки -> downloads
документы -> documents
изображения -> pictures
музыка -> music
видео -> videos

Пример:

Пользователь:
открой последний PDF из Загрузок

Ответ:
{{
    "action": "OPEN_LATEST_FILE",
    "query": "",
    "filename": "",
    "content": "",
    "app": "",
    "folder": "downloads",
    "folder_name": "",
    "extension": "pdf"
}}


10. Если пользователь хочет открыть папку:
    action = "OPEN_FOLDER"
    folder = стандартная папка

Пример:
"открой Загрузки" -> folder = "downloads"


11. Если пользователь хочет создать папку:
    action = "CREATE_FOLDER"
    folder = где создать папку
    folder_name = название новой папки


12. Если пользователь хочет посмотреть содержимое папки:
    action = "LIST_FILES"
    folder = стандартная папка


13. Если пользователь приветствует:
    action = "HELLO"


14. Если пользователь просит помощь:
    action = "HELP"


15. Если пользователь хочет завершить программу:
    action = "EXIT"


16. Если намерение непонятно:
    action = "UNKNOWN"


ВАЖНО:

Для всех полей, которые не используются в конкретной команде,
возвращай пустую строку.

Не путай:
SEARCH_WEB = поиск информации в интернете.
FIND_FILE = поиск файла на компьютере.
CREATE_FILE = создание нового файла.
APPEND_FILE = добавление текста в существующий файл.
OPEN_FILE = открытие существующего файла.

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
    print("Расширение:", result.get("extension", ""))