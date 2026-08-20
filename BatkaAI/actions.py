import subprocess
import webbrowser
from urllib.parse import quote_plus


def open_notepad():
    try:
        subprocess.Popen(["notepad.exe"])
        print("Блокнот успешно открыт.")
    except Exception as e:
        print(f"Ошибка при открытии блокнота: {e}")


def open_browser():
    try:
        subprocess.Popen(["cmd", "/c", "start", "https://www.google.com"])
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