import requests
import json


def understand_command(command):
    prompt = f"""
Ты — мозг локального помощника Batka AI.

Определи намерение пользователя и верни ТОЛЬКО JSON.
Никакого дополнительного текста.

Доступные действия:

OPEN_NOTEPAD
OPEN_BROWSER
SEARCH_WEB
CREATE_FILE
HELLO
HELP
EXIT
UNKNOWN

Формат ответа:

{{
    "action": "НАЗВАНИЕ_ДЕЙСТВИЯ",
    "query": "",
    "filename": "",
    "content": ""
}}

Правила:

1. Если пользователь хочет что-либо найти в интернете:
   action = "SEARCH_WEB"
   query = то, что нужно найти.
   filename = ""
   content = ""

2. Если пользователь просто хочет открыть браузер:
   action = "OPEN_BROWSER"
   query = ""
   filename = ""
   content = ""

3. Если пользователь хочет открыть блокнот:
   action = "OPEN_NOTEPAD"
   query = ""
   filename = ""
   content = ""

4. Если пользователь приветствует:
   action = "HELLO"
   query = ""
   filename = ""
   content = ""

5. Если пользователь просит показать помощь:
   action = "HELP"
   query = ""
   filename = ""
   content = ""

6. Если пользователь хочет завершить работу программы:
   action = "EXIT"
   query = ""
   filename = ""
   content = ""

7. Если пользователь просит создать текстовый файл:
   action = "CREATE_FILE"
   filename = имя файла, которое указал пользователь
   content = текст, который нужно записать в файл
   query = ""

Если пользователь не указал расширение файла, добавь .txt.

Пример 1:

Пользователь:
найди в интернете Audi Q3 Sportback 2026

Ответ:
{{
    "action": "SEARCH_WEB",
    "query": "Audi Q3 Sportback 2026",
    "filename": "",
    "content": ""
}}

Пример 2:

Пользователь:
создай файл заметка.txt и напиши туда купить продукты

Ответ:
{{
    "action": "CREATE_FILE",
    "query": "",
    "filename": "заметка.txt",
    "content": "купить продукты"
}}

Пример 3:

Пользователь:
создай файл идеи и напиши туда разработать Batka AI

Ответ:
{{
    "action": "CREATE_FILE",
    "query": "",
    "filename": "идеи.txt",
    "content": "разработать Batka AI"
}}

8. Если намерение пользователя непонятно:
   action = "UNKNOWN"
   query = ""
   filename = ""
   content = ""

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
    print("Действие:", result["action"])
    print("Запрос:", result.get("query", ""))
    print("Имя файла:", result.get("filename", ""))
    print("Содержимое:", result.get("content", ""))