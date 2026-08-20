import subprocess
import webbrowser
import os
from pathlib import Path
from urllib.parse import quote_plus

from BatkaAI.services.paths import get_folder_path


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


def find_start_menu_app(app_name):
    app_name = app_name.lower()

    start_menu_paths = [
        Path(os.environ["APPDATA"])
        / "Microsoft/Windows/Start Menu/Programs",

        Path(os.environ["PROGRAMDATA"])
        / "Microsoft/Windows/Start Menu/Programs"
    ]

    for start_menu in start_menu_paths:
        if not start_menu.exists():
            continue

        for shortcut in start_menu.rglob("*.lnk"):
            shortcut_name = shortcut.stem.lower()

            if app_name in shortcut_name:
                return shortcut

    return None


def open_app(app):
    system_apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "explorer": "explorer.exe"
    }

    try:
        if app in system_apps:
            subprocess.Popen([system_apps[app]])
            print(f"Программа запущена: {app}")
            return

        shortcut = find_start_menu_app(app)

        if shortcut:
            os.startfile(shortcut)
            print(f"Программа запущена: {shortcut.stem}")
            return

        print(f"Не удалось найти программу: {app}")

    except Exception as e:
        print(f"Ошибка при запуске программы {app}: {e}")


def open_folder(folder):
    try:
        folder_path = get_folder_path(folder)

        if not folder_path:
            print(f"Неизвестная папка: {folder}")
            return

        if not folder_path.exists():
            print(f"Папка не найдена: {folder_path}")
            return

        os.startfile(folder_path)
        print(f"Папка открыта: {folder_path}")

    except Exception as e:
        print(f"Ошибка при открытии папки: {e}")