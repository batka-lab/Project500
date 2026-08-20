from BatkaAI.actions import (
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
    open_latest_file,
    word_edit,
    create_word,
    read_word,
    append_word,
    add_word_heading
)

from BatkaAI.brain import understand_command


def main():
    print("Batka AI запущен!")

    while True:
        command = input(
            "Что нужно сделать? "
        ).strip()

        if not command:
            continue

        try:
            result = understand_command(command)

        except Exception as e:
            print(
                f"Ошибка при обработке команды: {e}"
            )
            continue

        actions = result.get(
            "actions",
            []
        )

        if not actions:
            print("Не удалось понять команду.")
            continue

        should_exit = False

        for action_data in actions:
            action = action_data.get(
                "action",
                ""
            )

            query = action_data.get(
                "query",
                ""
            )

            filename = action_data.get(
                "filename",
                ""
            )

            content = action_data.get(
                "content",
                ""
            )

            app = action_data.get(
                "app",
                ""
            )

            folder = action_data.get(
                "folder",
                ""
            )

            folder_name = action_data.get(
                "folder_name",
                ""
            )

            extension = action_data.get(
                "extension",
                ""
            )

            operation = action_data.get(
                "operation",
                ""
            )

            data = action_data.get(
                "data",
                {}
            )

            if action == "HELP":
                print("Доступные команды:")
                print("- открыть программу")
                print("- открыть браузер")
                print("- поиск в интернете")
                print("- создать файл")
                print("- найти файл")
                print("- открыть папку")
                print("- создать папку")
                print("- работать с Word")
                print("- выйти")

            elif action == "OPEN_APP":
                open_app(app)

            elif action == "OPEN_BROWSER":
                open_browser()

            elif action == "SEARCH_WEB":
                search_web(query)

            elif action == "CREATE_FILE":
                create_file(
                    filename,
                    content
                )

            elif action == "OPEN_FILE":
                open_file(filename)

            elif action == "READ_FILE":
                read_file(filename)

            elif action == "APPEND_FILE":
                append_file(
                    filename,
                    content
                )

            elif action == "FIND_FILE":
                show_found_files(filename)

            elif action == "OPEN_LATEST_FILE":
                open_latest_file(
                    folder,
                    extension
                )

            elif action == "OPEN_FOLDER":
                open_folder(folder)

            elif action == "CREATE_FOLDER":
                create_folder(
                    folder,
                    folder_name
                )

            elif action == "LIST_FILES":
                list_files(folder)

            # ---------------------------------
            # WORD ENGINE V2
            # ---------------------------------

            elif action == "WORD_EDIT":
                word_edit(
                    filename,
                    operation,
                    data
                )

            # ---------------------------------
            # Старые Word-команды
            # пока поддерживаем
            # ---------------------------------

            elif action == "CREATE_WORD":
                create_word(
                    filename,
                    content
                )

            elif action == "READ_WORD":
                read_word(filename)

            elif action == "APPEND_WORD":
                append_word(
                    filename,
                    content
                )

            elif action == "ADD_WORD_HEADING":
                add_word_heading(
                    filename,
                    content
                )

            elif action == "HELLO":
                print(
                    "Привет! Batka AI на связи."
                )

            elif action == "EXIT":
                print(
                    "Завершение работы Batka AI..."
                )

                should_exit = True
                break

            elif action == "UNKNOWN":
                print(
                    "Не удалось понять часть команды."
                )

            else:
                print(
                    f"Неизвестное действие: {action}"
                )

        if should_exit:
            break


if __name__ == "__main__":
    main()