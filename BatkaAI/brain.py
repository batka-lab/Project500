import requests
import json


def understand_command(command):
    prompt = f"""
Ты — мозг локального помощника Batka AI.

Твоя задача — понять команду пользователя и разбить её
на одно или несколько последовательных действий.

Верни ТОЛЬКО JSON.
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


ФОРМАТ ОТВЕТА:

{{
    "actions": [
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
    ]
}}


ПРАВИЛА:


1. ОТКРЫТИЕ ПРОГРАММЫ

Если пользователь хочет открыть или запустить программу:

action = "OPEN_APP"

app = короткое название программы.

Примеры:

блокнот -> notepad
калькулятор -> calculator
paint -> paint
проводник -> explorer
steam -> steam


2. БРАУЗЕР

Если пользователь просто хочет открыть браузер:

action = "OPEN_BROWSER"


3. ПОИСК В ИНТЕРНЕТЕ

Если пользователь хочет найти информацию в интернете:

action = "SEARCH_WEB"

query = поисковый запрос

Пример:

найди в интернете Audi Q3 Sportback 2026

->

SEARCH_WEB
query = Audi Q3 Sportback 2026


4. СОЗДАНИЕ ФАЙЛА

Если пользователь хочет создать новый текстовый файл:

action = "CREATE_FILE"

filename = имя файла

content = текст, который нужно записать

Если расширение файла не указано,
добавь .txt.


5. ОТКРЫТИЕ ФАЙЛА

Если пользователь хочет открыть существующий файл:

action = "OPEN_FILE"

filename = имя файла или часть имени


6. ЧТЕНИЕ ФАЙЛА

Если пользователь хочет прочитать существующий текстовый файл:

action = "READ_FILE"

filename = имя файла или часть имени


7. ДОБАВЛЕНИЕ ТЕКСТА В ФАЙЛ

Если пользователь хочет добавить текст в существующий файл:

action = "APPEND_FILE"

filename = имя файла

content = текст, который нужно добавить

НЕ использовать CREATE_FILE для команды "добавь".


8. ПОИСК ФАЙЛА

Если пользователь хочет найти файл на компьютере:

action = "FIND_FILE"

filename = имя файла или часть имени

НЕ использовать SEARCH_WEB.


9. ПОСЛЕДНИЙ ФАЙЛ

Если пользователь хочет открыть самый новый файл
определенного типа:

action = "OPEN_LATEST_FILE"

extension = расширение без точки

folder = папка, если пользователь её указал


10. СТАНДАРТНЫЕ ПАПКИ

Используй:

рабочий стол -> desktop
загрузки -> downloads
документы -> documents
изображения -> pictures
музыка -> music
видео -> videos


11. ОТКРЫТИЕ ПАПКИ

action = "OPEN_FOLDER"

folder = стандартная папка


12. СОЗДАНИЕ ПАПКИ

action = "CREATE_FOLDER"

folder = где создать

folder_name = название новой папки


13. СПИСОК ФАЙЛОВ

Если пользователь хочет увидеть содержимое папки:

action = "LIST_FILES"

folder = стандартная папка


14. ПРИВЕТСТВИЕ

action = "HELLO"


15. ПОМОЩЬ

action = "HELP"


16. ВЫХОД

action = "EXIT"


17. НЕПОНЯТНАЯ КОМАНДА

action = "UNKNOWN"


МНОГОШАГОВЫЕ КОМАНДЫ:

Если пользователь просит выполнить несколько действий,
создай несколько объектов внутри массива "actions".

Порядок действий должен соответствовать порядку,
в котором их нужно выполнять.


ПРИМЕР 1:

Пользователь:

открой калькулятор

Ответ:

{{
    "actions": [
        {{
            "action": "OPEN_APP",
            "query": "",
            "filename": "",
            "content": "",
            "app": "calculator",
            "folder": "",
            "folder_name": "",
            "extension": ""
        }}
    ]
}}


ПРИМЕР 2:

Пользователь:

создай папку Отчёты на рабочем столе
и открой Загрузки

Ответ:

{{
    "actions": [
        {{
            "action": "CREATE_FOLDER",
            "query": "",
            "filename": "",
            "content": "",
            "app": "",
            "folder": "desktop",
            "folder_name": "Отчёты",
            "extension": ""
        }},
        {{
            "action": "OPEN_FOLDER",
            "query": "",
            "filename": "",
            "content": "",
            "app": "",
            "folder": "downloads",
            "folder_name": "",
            "extension": ""
        }}
    ]
}}


ПРИМЕР 3:

Пользователь:

найди в интернете Audi Q3
и открой калькулятор

Ответ:

{{
    "actions": [
        {{
            "action": "SEARCH_WEB",
            "query": "Audi Q3",
            "filename": "",
            "content": "",
            "app": "",
            "folder": "",
            "folder_name": "",
            "extension": ""
        }},
        {{
            "action": "OPEN_APP",
            "query": "",
            "filename": "",
            "content": "",
            "app": "calculator",
            "folder": "",
            "folder_name": "",
            "extension": ""
        }}
    ]
}}


ВАЖНО:

Всегда возвращай поле "actions".

Даже если действие только одно,
оно всё равно должно находиться внутри массива "actions".

Для неиспользуемых параметров возвращай пустую строку.

Не придумывай дополнительных действий,
которых пользователь не просил.


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

    print("Результат:")
    print(result)

    actions = result.get("actions", [])

    print()
    print(f"Количество действий: {len(actions)}")

    for number, action_data in enumerate(actions, start=1):
        print()
        print(f"Действие {number}:")
        print("Тип:", action_data.get("action", ""))
        print("Программа:", action_data.get("app", ""))
        print("Запрос:", action_data.get("query", ""))
        print("Имя файла:", action_data.get("filename", ""))
        print("Содержимое:", action_data.get("content", ""))
        print("Папка:", action_data.get("folder", ""))
        print(
            "Название новой папки:",
            action_data.get("folder_name", "")
        )
        print(
            "Расширение:",
            action_data.get("extension", "")
        )