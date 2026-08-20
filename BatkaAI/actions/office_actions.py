import os
from pathlib import Path
from docx import Document

from BatkaAI.actions.file_actions import find_file


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


def read_word(filename):
    try:
        matches = find_file(filename)

        if not matches:
            print(f"Word-документ не найден: {filename}")
            return

        file_path = matches[0]

        if file_path.suffix.lower() != ".docx":
            print(f"Это не Word-документ: {file_path}")
            return

        document = Document(file_path)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        if not paragraphs:
            print("Документ пустой.")
            return

        print(f"Содержимое Word-документа {file_path}:")
        print("-" * 50)

        for paragraph in paragraphs:
            print(paragraph)

        print("-" * 50)

    except Exception as e:
        print(f"Ошибка при чтении Word-документа: {e}")


def append_word(filename, content):
    try:
        matches = find_file(filename)

        if not matches:
            print(f"Word-документ не найден: {filename}")
            return

        file_path = matches[0]

        if file_path.suffix.lower() != ".docx":
            print(f"Это не Word-документ: {file_path}")
            return

        document = Document(file_path)

        document.add_paragraph(content)

        document.save(file_path)

        print(f"Текст добавлен в Word-документ: {file_path}")

        os.startfile(file_path)

    except Exception as e:
        print(f"Ошибка при изменении Word-документа: {e}")