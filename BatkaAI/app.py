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

    result = understand_command(command)

    actions = result.get("actions", [])

    if not actions:
        print("Не удалось понять команду.")
        continue

    should_exit = False

    for action_data in actions:
        action = action_data.get("action", "")

        query = action_data.get("query", "")
        filename = action_data.get("filename", "")
        content = action_data.get("content", "")
        app = action_data.get("app", "")
        folder = action_data.get("folder", "")
        folder_name = action_data.get("folder_name", "")
        extension = action_data.get("extension", "")

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
            print("- выполнить несколько действий одной командой")
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
            should_exit = True
            break

        elif action == "UNKNOWN":
            print("Не удалось понять часть команды.")

        else:
            print(f"Неизвестное действие: {action}")

    if should_exit:
        break