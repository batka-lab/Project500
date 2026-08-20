from BatkaAI.actions import (
    open_browser,
    search_web,
    create_file,
    open_app,
    open_folder,
    create_folder,
    list_files,
    find_file,
    open_file,
    read_file,
    append_file,
    open_latest_file,
    word_edit,
    excel_edit,
    analyze_document_command,
    prepare_improvement_plan,
    execute_improvement_plan,
)

from BatkaAI.brain import (
    understand_command,
)

from BatkaAI.services.task_manager import (
    TaskManager,
)


# =========================================================
# ПОИСКОВЫЙ ЗАПРОС ФАЙЛА
# =========================================================


def get_file_search_term(
    action_data
):
    filename = str(
        action_data.get(
            "filename",
            "",
        )
        or ""
    ).strip()

    query = str(
        action_data.get(
            "query",
            "",
        )
        or ""
    ).strip()

    if filename:
        return filename

    return query


# =========================================================
# ОПИСАНИЕ TASK
# =========================================================


def describe_action(
    action_data
):
    action = action_data.get(
        "action",
        "",
    )

    filename = action_data.get(
        "filename",
        "",
    )

    operation = action_data.get(
        "operation",
        "",
    )

    query = action_data.get(
        "query",
        "",
    )

    app = action_data.get(
        "app",
        "",
    )

    if action == "FIND_FILE":
        search_term = (
            get_file_search_term(
                action_data
            )
        )

        return (
            f"Ищу файл "
            f"{search_term}"
        )

    descriptions = {
        "OPEN_APP": (
            f"Открываю программу "
            f"{app}"
        ),

        "OPEN_BROWSER": (
            "Открываю браузер"
        ),

        "SEARCH_WEB": (
            f"Ищу в интернете: "
            f"{query}"
        ),

        "CREATE_FILE": (
            f"Создаю файл "
            f"{filename}"
        ),

        "OPEN_FILE": (
            f"Открываю файл "
            f"{filename}"
        ),

        "READ_FILE": (
            f"Читаю файл "
            f"{filename}"
        ),

        "APPEND_FILE": (
            f"Изменяю файл "
            f"{filename}"
        ),

        "WORD_EDIT": (
            f"Word: "
            f"{operation} "
            f"({filename})"
        ),

        "EXCEL_EDIT": (
            f"Excel: "
            f"{operation} "
            f"({filename})"
        ),

        "OPEN_FOLDER": (
            "Открываю папку"
        ),

        "CREATE_FOLDER": (
            "Создаю папку"
        ),

        "LIST_FILES": (
            "Читаю содержимое папки"
        ),

        "HELP": (
            "Показываю возможности"
        ),

        "HELLO": (
            "Приветствие"
        ),

        "EXIT": (
            "Завершаю работу"
        ),
    }

    return descriptions.get(
        action,
        f"Выполняю "
        f"{action}"
    )


# =========================================================
# FIND
# =========================================================


def execute_find_file(
    action_data
):
    search_term = (
        get_file_search_term(
            action_data
        )
    )

    if not search_term:
        print(
            "Не указано имя файла."
        )

        return False

    matches = find_file(
        search_term
    )

    if not matches:
        print(
            f"Файлы не найдены: "
            f"{search_term}"
        )

        return True

    print(
        f"Найдено файлов: "
        f"{len(matches)}"
    )

    for index, file_path in enumerate(
        matches,
        start=1,
    ):
        print(
            f"{index}. "
            f"{file_path}"
        )

    return True


# =========================================================
# ACTION
# =========================================================


def execute_action(
    action_data
):
    action = action_data.get(
        "action",
        "",
    )

    query = action_data.get(
        "query",
        "",
    )

    filename = action_data.get(
        "filename",
        "",
    )

    content = action_data.get(
        "content",
        "",
    )

    app = action_data.get(
        "app",
        "",
    )

    folder = action_data.get(
        "folder",
        "",
    )

    folder_name = action_data.get(
        "folder_name",
        "",
    )

    extension = action_data.get(
        "extension",
        "",
    )

    operation = action_data.get(
        "operation",
        "",
    )

    data = action_data.get(
        "data",
        {},
    )

    if action == "OPEN_APP":
        open_app(
            app
        )

        return True

    if action == "OPEN_BROWSER":
        open_browser()

        return True

    if action == "SEARCH_WEB":
        search_web(
            query
        )

        return True

    if action == "CREATE_FILE":
        create_file(
            filename,
            content
        )

        return True

    if action == "OPEN_FILE":
        open_file(
            filename
        )

        return True

    if action == "READ_FILE":
        read_file(
            filename
        )

        return True

    if action == "APPEND_FILE":
        append_file(
            filename,
            content
        )

        return True

    if action == "FIND_FILE":
        return execute_find_file(
            action_data
        )

    if action == "OPEN_LATEST_FILE":
        open_latest_file(
            folder,
            extension
        )

        return True

    if action == "OPEN_FOLDER":
        open_folder(
            folder
        )

        return True

    if action == "CREATE_FOLDER":
        create_folder(
            folder,
            folder_name
        )

        return True

    if action == "LIST_FILES":
        list_files(
            folder
        )

        return True

    if action == "WORD_EDIT":
        result = word_edit(
            filename,
            operation,
            data
        )

        return (
            result is not None
        )

    if action == "EXCEL_EDIT":
        result = excel_edit(
            filename,
            operation,
            data
        )

        return (
            result is not None
        )

    if action == "HELP":
        print(
            "Batka AI умеет работать "
            "с файлами, Word, Excel "
            "и анализировать документы."
        )

        return True

    if action == "HELLO":
        print(
            "Привет! Batka AI на связи."
        )

        return True

    if action == "EXIT":
        return "EXIT"

    return False


# =========================================================
# ANALYSIS COMMAND
# =========================================================


def is_analysis_command(
    command
):
    lowered = command.lower()

    return (
        (
            ".xlsx"
            in lowered
            or ".docx"
            in lowered
        )
        and any(
            phrase in lowered
            for phrase in [
                "проанализируй",
                "анализируй",
                "анализ документа",
                "посмотри структуру",
            ]
        )
    )


# =========================================================
# IMPROVE COMMAND
# =========================================================


def is_improvement_command(
    command
):
    lowered = command.lower()

    has_document = (
        ".xlsx" in lowered
        or ".docx" in lowered
    )

    improve_words = [
        "улучши",
        "исправь",
        "приведи в порядок",
        "сделай нормальным",
        "сделай аккуратным",
        "приведи документ в порядок",
        "приведи excel в порядок",
        "приведи word в порядок",
    ]

    return (
        has_document
        and any(
            word in lowered
            for word in improve_words
        )
    )


# =========================================================
# NORMAL TASK
# =========================================================


def execute_task(
    command,
    actions
):
    if not actions:
        print(
            "Не удалось понять команду."
        )

        return False

    task = TaskManager(
        command
    )

    steps = [
        task.add_step(
            describe_action(
                action
            )
        )
        for action
        in actions
    ]

    task.start()

    for step, action in zip(
        steps,
        actions,
    ):
        result = task.run_step(
            step,
            execute_action,
            action,
        )

        if result == "EXIT":
            task.finish()

            return "EXIT"

        if result is False:
            print(
                "Остальные действия "
                "остановлены."
            )

            task.finish()

            return False

    task.finish()

    return True


# =========================================================
# MAIN
# =========================================================


def main():
    print(
        "Batka AI запущен!"
    )

    pending_plan = None

    while True:
        command = input(
            "Что нужно сделать? "
        ).strip()

        if not command:
            continue

        lowered = command.lower()

        # =============================================
        # ОЖИДАЕТСЯ ПОДТВЕРЖДЕНИЕ
        # =============================================

        if pending_plan:
            if lowered in [
                "да",
                "давай",
                "выполняй",
                "выполнить",
                "подтверждаю",
                "ок",
                "окей",
            ]:
                execute_improvement_plan(
                    pending_plan
                )

                pending_plan = None

                continue

            if lowered in [
                "нет",
                "отмена",
                "отмени",
                "не надо",
            ]:
                print(
                    "План отменён. "
                    "Файл не изменён."
                )

                pending_plan = None

                continue

        # =============================================
        # IMPROVE
        # =============================================

        if is_improvement_command(
            command
        ):
            pending_plan = (
                prepare_improvement_plan(
                    command
                )
            )

            continue

        # =============================================
        # ANALYZE
        # =============================================

        if is_analysis_command(
            command
        ):
            analyze_document_command(
                command
            )

            continue

        # =============================================
        # BRAIN
        # =============================================

        try:
            result = understand_command(
                command
            )

        except Exception as e:
            print(
                f"Ошибка понимания команды: "
                f"{type(e).__name__}: "
                f"{e}"
            )

            continue

        actions = result.get(
            "actions",
            []
        )

        result = execute_task(
            command,
            actions
        )

        if result == "EXIT":
            print(
                "Завершение Batka AI..."
            )

            break


if __name__ == "__main__":
    main()