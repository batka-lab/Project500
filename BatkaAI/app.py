from actions import (
    open_browser,
    search_web,
    create_file,
    open_app,
    open_folder,
    create_folder,
    list_files
)
from brain import understand_command


print("Batka AI запущен!")


while True:
    command = input("Что нужно сделать? ").strip().lower()

    intent = understand_command(command)

    action = intent.get("action", "")
    query = intent.get("query", "")
    filename = intent.get("filename", "")
    content = intent.get("content", "")
    app = intent.get("app", "")
    folder = intent.get("folder", "")
    folder_name = intent.get("folder_name", "")

    if action == "HELP":
        print("Доступные команды:")
        print("- открыть программу")
        print("- открыть браузер")
        print("- найти что-нибудь в интернете")
        print("- создать текстовый файл")
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