import requests


def understand_command(command):
    prompt = f"""
Ты — мозг локального помощника Batka AI.

Определи намерение пользователя.

Разрешенные ответы:
OPEN_NOTEPAD
OPEN_BROWSER
HELLO
HELP
EXIT
UNKNOWN

Верни ТОЛЬКО один из этих вариантов.
Никаких объяснений.

Команда пользователя:
{command}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3:4b",
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["response"].strip()
