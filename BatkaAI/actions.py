import subprocess
import webbrowser
import os
from pathlib import Path
from urllib.parse import quote_plus
from docx import Document


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


def create_file(filename, content):
    try:
        desktop = Path.home() / "Desktop"
        file_path = desktop / filename

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        subprocess.Popen(
            ["notepad.exe", str(file_path)]
        )

        print(f"Файл создан и открыт: {file_path}")

    except Exception as e:
        print(f"Ошибка при создании файла: {e}")


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


def get_folder_path(folder):
    folders = {
        "desktop": Path.home() / "Desktop",
        "downloads": Path.home() / "Downloads",
        "documents": Path.home() / "Documents",
        "pictures": Path.home() / "Pictures",
        "music": Path.home() / "Music",
        "videos": Path.home() / "Videos"
    }

    return folders.get(folder)


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


def create_folder(folder, folder_name):
    try:
        base_path = get_folder_path(folder)

        if not base_path:
            print(f"Неизвестное место: {folder}")
            return

        new_folder = base_path / folder_name

        new_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        print(f"Папка создана: {new_folder}")

    except Exception as e:
        print(f"Ошибка при создании папки: {e}")


def list_files(folder):
    try:
        folder_path = get_folder_path(folder)

        if not folder_path:
            print(f"Неизвестная папка: {folder}")
            return

        if not folder_path.exists():
            print(f"Папка не найдена: {folder_path}")
            return

        items = list(folder_path.iterdir())

        if not items:
            print("Папка пустая.")
            return

        print(f"Содержимое папки {folder_path}:")

        for item in items:
            if item.is_dir():
                print(f"[ПАПКА] {item.name}")
            else:
                print(f"[ФАЙЛ]  {item.name}")

    except Exception as e:
        print(f"Ошибка при чтении папки: {e}")


def get_search_locations():
    return [
        Path.home() / "Desktop",
        Path.home() / "Downloads",
        Path.home() / "Documents"
    ]


def find_file(filename):
    filename_lower = filename.lower()
    matches = []

    try:
        for location in get_search_locations():
            if not location.exists():
                continue

            for item in location.rglob("*"):
                if not item.is_file():
                    continue

                if filename_lower in item.name.lower():
                    matches.append(item)

        return matches

    except Exception as e:
        print(f"Ошибка при поиске файла: {e}")
        return []


def show_found_files(filename):
    matches = find_file(filename)

    if not matches:
        print(f"Файлы не найдены: {filename}")
        return

    print(f"Найдено файлов: {len(matches)}")

    for index, file_path in enumerate(matches, start=1):
        print(f"{index}. {file_path}")


def open_file(filename):
    try:
        matches = find_file(filename)

        if not matches:
            print(f"Файл не найден: {filename}")
            return

        file_path = matches[0]

        os.startfile(file_path)

        print(f"Файл открыт: {file_path}")

    except Exception as e:
        print(f"Ошибка при открытии файла: {e}")


def read_file(filename):
    try:
        matches = find_file(filename)

        if not matches:
            print(f"Файл не найден: {filename}")
            return

        file_path = matches[0]

        allowed_extensions = [
            ".txt",
            ".md",
            ".py",
            ".json",
            ".csv"
        ]

        if file_path.suffix.lower() not in allowed_extensions:
            print(
                f"Чтение этого типа файла пока не поддерживается: "
                f"{file_path.suffix}"
            )
            return

        content = file_path.read_text(
            encoding="utf-8",
            errors="replace"
        )

        print(f"Содержимое файла {file_path}:")
        print("-" * 50)
        print(content)
        print("-" * 50)

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")


def append_file(filename, content):
    try:
        matches = find_file(filename)

        if not matches:
            print(f"Файл не найден: {filename}")
            return

        file_path = matches[0]

        allowed_extensions = [
            ".txt",
            ".md"
        ]

        if file_path.suffix.lower() not in allowed_extensions:
            print(
                f"Добавление текста для этого типа файла "
                f"пока не поддерживается: {file_path.suffix}"
            )
            return

        with file_path.open(
            "a",
            encoding="utf-8"
        ) as file:
            file.write("\n")
            file.write(content)

        print(f"Текст добавлен в файл: {file_path}")

        subprocess.Popen(
            ["notepad.exe", str(file_path)]
        )

    except Exception as e:
        print(f"Ошибка при добавлении текста: {e}")


def open_latest_file(folder, extension):
    try:
        folder_path = get_folder_path(folder)

        if not folder_path:
            print(f"Неизвестная папка: {folder}")
            return

        if not folder_path.exists():
            print(f"Папка не найдена: {folder_path}")
            return

        extension = extension.lower().lstrip(".")

        files = [
            item
            for item in folder_path.iterdir()
            if item.is_file()
            and item.suffix.lower() == f".{extension}"
        ]

        if not files:
            print(
                f"Файлы .{extension} не найдены "
                f"в папке {folder_path}"
            )
            return

        latest_file = max(
            files,
            key=lambda item: item.stat().st_mtime
        )

        os.startfile(latest_file)

        print(f"Открыт последний файл: {latest_file}")

    except Exception as e:
        print(f"Ошибка при открытии последнего файла: {e}")


def create_word(filename, content):
    try:
        desktop = Path.home() / "Desktop"

        if not filename.lower().endswith(".docx"):
            filename += ".docx"

        file_path = desktop / filename

        document = Document()

        if content:
            document.add_paragraph(content)

        document.save(file_path)

        print(f"Документ Word создан: {file_path}")

        os.startfile(file_path)

    except Exception as e:
        print(f"Ошибка при создании Word-документа: {e}")