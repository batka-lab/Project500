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

CREATE_WORD

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


4. СОЗДАНИЕ ТЕКСТОВОГО ФАЙЛА

Если пользователь хочет создать обычный текстовый файл:

action = "CREATE_FILE"

filename = имя файла
content = текст

Если расширение не указано,
добавь .txt.


5. СОЗДАНИЕ WORD-ДОКУМЕНТА

Если пользователь просит создать документ Word,
файл DOCX или документ .docx:

action = "CREATE_WORD"

filename = имя документа
content = текст документа

Если расширение не указано,
добавь .docx.

НЕ использовать CREATE_FILE,
если пользователь явно просит Word или DOCX.


Пример:

Пользователь:

создай документ Word Отчёт.docx
и напиши туда Итоги работы за август

Ответ:

{{
    "actions": [
        {{
            "action": "CREATE_WORD",
            "query": "",
            "filename": "Отчёт.docx",
            "content": "Итоги работы за август",
            "app": "",
            "folder": "",
            "folder_name": "",
            "extension": ""
        }}
    ]
}}


6. ОТКРЫТИЕ ФАЙЛА

Если пользователь хочет открыть существующий файл:

action = "OPEN_FILE"

filename = имя файла или часть имени


7. ЧТЕНИЕ ФАЙЛА

Если пользователь хочет прочитать существующий текстовый файл:

action = "READ_FILE"

filename = имя файла или часть имени


8. ДОБАВЛЕНИЕ ТЕКСТА В ФАЙЛ

Если пользователь хочет добавить текст
в существующий текстовый файл:

action = "APPEND_FILE"

filename = имя файла
content = текст

НЕ использовать CREATE_FILE.


9. ПОИСК ФАЙЛА

Если пользователь хочет найти файл на компьютере:

action = "FIND_FILE"

filename = имя файла или часть имени

НЕ использовать SEARCH_WEB.


10. ПОСЛЕДНИЙ ФАЙЛ

Если пользователь хочет открыть самый новый файл
определенного типа:

action = "OPEN_LATEST_FILE"

extension = расширение без точки

folder = папка, если указана


11. СТАНДАРТНЫЕ ПАПКИ

рабочий стол -> desktop
загрузки -> downloads
документы -> documents
изображения -> pictures
музыка -> music
видео -> videos


12. ОТКРЫТИЕ ПАПКИ

action = "OPEN_FOLDER"

folder = стандартная папка


13. СОЗДАНИЕ ПАПКИ

action = "CREATE_FOLDER"

folder = где создать
folder_name = название новой папки


14. СПИСОК ФАЙЛОВ

Если пользователь хочет увидеть содержимое папки:

action = "LIST_FILES"

folder = стандартная папка


15. ПРИВЕТСТВИЕ

action = "HELLO"


16. ПОМОЩЬ

action = "HELP"


17. ВЫХОД

action = "EXIT"


18. НЕПОНЯТНАЯ КОМАНДА

action = "UNKNOWN"


МНОГОШАГОВЫЕ КОМАНДЫ:

Если пользователь просит выполнить несколько действий,
создай несколько объектов внутри массива "actions".

Порядок действий должен соответствовать порядку,
в котором их нужно выполнять.


ПРИМЕР:

Пользователь:

создай документ Word План.docx
и открой калькулятор

Ответ:

{{
    "actions": [
        {{
            "action": "CREATE_WORD",
            "query": "",
            "filename": "План.docx",
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

Даже если действие одно,
оно должно находиться внутри массива "actions".

Для всех неиспользуемых полей возвращай пустую строку.

Не придумывай действий,
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
        print("Название новой папки:", action_data.get("folder_name", ""))
        print("Расширение:", action_data.get("extension", ""))