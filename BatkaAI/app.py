from actions import (
    open_browser,
    search_web,
    create_file,
    open_app,
    open_folder,
    create_folder,
    list_files,
    show_found_files,
    open_file,
    read_file,
    append_file,
    open_latest_file
)
from brain import understand_command


print("Batka AI запущен!")


while True:
    command = input("Что нужно сделать? ").strip()

    intent = understand_command(command)

    action = intent.get("action", "")
    query = intent.get("query", "")
    filename = intent.get("filename", "")
    content = intent.get("content", "")
    app = intent.get("app", "")
    folder = intent.get("folder", "")
    folder_name = intent.get("folder_name", "")
    extension = intent.get("extension", "")

    if action == "HELP":
        print("Доступные команды:")
        print("- открыть программу")
        print("- открыть браузер")
        print("- найти что-нибудь в интернете")
        print("- создать текстовый файл")
        print("- открыть файл")
        print("- прочитать файл")
        print("- добавить текст в файл")
        print("- найти файл")
        print("- открыть последний файл нужного типа")
        print("- открыть папку")
        print("- создать папку")
        print("- показать файлы в папке")
        print("- привет")
        print("- выйти")

    elif action == "OPEN_APP":
        open_app(app)

    elif action == "OPEN_BROWSER":
        open_browser()

    elif action == "SEARCH_WEB":
        search_web(query)

    elif action == "CREATE_FILE":
        create_file(filename, content)

    elif action == "OPEN_FILE":
        open_file(filename)

    elif action == "READ_FILE":
        read_file(filename)

    elif action == "APPEND_FILE":
        append_file(filename, content)

    elif action == "FIND_FILE":
        show_found_files(filename)

    elif action == "OPEN_LATEST_FILE":
        open_latest_file(folder, extension)

    elif action == "OPEN_FOLDER":
        open_folder(folder)

    elif action == "CREATE_FOLDER":
        create_folder(folder, folder_name)

    elif action == "LIST_FILES":
        list_files(folder)

    elif action == "HELLO":
        print("Привет! Batka AI на связи.")

    elif action == "EXIT":
        print("Завершение работы программы...")
        break

    else:
        print("Не удалось понять команду.")