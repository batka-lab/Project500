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
HELLO
HELP
EXIT
UNKNOWN

Формат ответа:

{{
    "action": "НАЗВАНИЕ_ДЕЙСТВИЯ",
    "query": "",
    "filename": "",
    "content": "",
    "app": ""
}}

Правила:

1. Если пользователь хочет открыть или запустить программу:
   action = "OPEN_APP"
   app = короткое название программы на английском.

Примеры:
блокнот -> notepad
калькулятор -> calculator
paint -> paint
проводник -> explorer

2. Если пользователь просто хочет открыть браузер:
   action = "OPEN_BROWSER"

3. Если пользователь хочет что-либо найти в интернете:
   action = "SEARCH_WEB"
   query = то, что нужно найти.

4. Если пользователь просит создать текстовый файл:
   action = "CREATE_FILE"
   filename = имя файла
   content = текст для файла

Если расширение файла не указано, добавь .txt.

5. Если пользователь приветствует:
   action = "HELLO"

6. Если пользователь просит помощь:
   action = "HELP"

7. Если пользователь хочет завершить программу:
   action = "EXIT"

8. Если намерение непонятно:
   action = "UNKNOWN"

Для всех неиспользуемых полей возвращай пустую строку.

Пример:

Пользователь:
открой калькулятор

Ответ:
{{
    "action": "OPEN_APP",
    "query": "",
    "filename": "",
    "content": "",
    "app": "calculator"
}}

Пример:

Пользователь:
запусти paint

Ответ:
{{
    "action": "OPEN_APP",
    "query": "",
    "filename": "",
    "content": "",
    "app": "paint"
}}

Пример:

Пользователь:
найди в интернете Audi Q3 Sportback 2026

Ответ:
{{
    "action": "SEARCH_WEB",
    "query": "Audi Q3 Sportback 2026",
    "filename": "",
    "content": "",
    "app": ""
}}

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