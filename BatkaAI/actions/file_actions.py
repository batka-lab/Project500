import subprocess
import os
from pathlib import Path

from BatkaAI.services.paths import (
    get_folder_path,
    get_search_locations
)


def normalize_text(text):
    return (
        str(text)
        .lower()
        .replace("ё", "е")
        .strip()
    )


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


def find_file(filename):
    if not filename or not filename.strip():
        print("Не указано имя файла для поиска.")
        return []

    search_text = normalize_text(filename)
    search_words = [
        word
        for word in search_text.replace(".", " ").split()
        if word
    ]

    matches = []

    try:
        for location in get_search_locations():
            if not location.exists():
                continue

            for item in location.rglob("*"):
                if not item.is_file():
                    continue

                # Игнорируем временные файлы Microsoft Office
                if item.name.startswith("~$"):
                    continue

                item_name = normalize_text(item.name)

                # Сначала точное/частичное совпадение
                direct_match = search_text in item_name

                # Затем умный поиск по отдельным словам
                words_match = (
                    search_words
                    and all(
                        word in item_name
                        for word in search_words
                    )
                )

                if direct_match or words_match:
                    matches.append(item)

        # Более точные совпадения ставим выше
        matches.sort(
            key=lambda item: (
                search_text not in normalize_text(item.name),
                len(normalize_text(item.name)),
                normalize_text(item.name)
            )
        )

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

        if not extension or not extension.strip():
            print("Не указано расширение файла.")
            return

        extension = extension.lower().lstrip(".")

        files = [
            item
            for item in folder_path.iterdir()
            if item.is_file()
            and not item.name.startswith("~$")
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