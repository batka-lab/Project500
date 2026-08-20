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
HELLO
HELP
EXIT
UNKNOWN

Формат ответа:

{{
    "action": "НАЗВАНИЕ_ДЕЙСТВИЯ",
    "query": ""
}}

Правила:

1. Если пользователь хочет что-либо найти в интернете:
   action = "SEARCH_WEB"
   query = то, что нужно найти.

2. Если пользователь просто хочет открыть браузер:
   action = "OPEN_BROWSER"

3. Если пользователь хочет открыть блокнот:
   action = "OPEN_NOTEPAD"

4. Для приветствия:
   action = "HELLO"

5. Для просьбы показать помощь:
   action = "HELP"

6. Для завершения программы:
   action = "EXIT"

7. Если намерение непонятно:
   action = "UNKNOWN"

Пример:

Пользователь:
найди в интернете Audi Q3 Sportback 2026

Ответ:
{{
    "action": "SEARCH_WEB",
    "query": "Audi Q3 Sportback 2026"
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

    

    result = json.loads(data["thinking"])

    return result

if __name__ == "__main__":
    test_command = input("Тестовая команда: ")
    result = understand_command(test_command)

    print("Результат:", result)
    print("Действие:", result["action"])
    print("Запрос:", result["query"])