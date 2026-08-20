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

from BatkaAI.services.history_service import (
    show_history,
    add_history_entry,
)

import time


def get_file_search_term(
    action_data
):
    filename = str(
        action_data.get(
            "filename",
            ""
        )
        or ""
    ).strip()

    query = str(
        action_data.get(
            "query",
            ""
        )
        or ""
    ).strip()

    return (
        filename
        or query
    )


def describe_action(
    action_data
):
    action = action_data.get(
        "action",
        ""
    )

    filename = action_data.get(
        "filename",
        ""
    )

    operation = action_data.get(
        "operation",
        ""
    )

    if action == "FIND_FILE":
        return (
            f"Ищу файл "
            f"{get_file_search_term(action_data)}"
        )

    if action == "WORD_EDIT":
        return (
            f"Word: "
            f"{operation} "
            f"({filename})"
        )

    if action == "EXCEL_EDIT":
        return (
            f"Excel: "
            f"{operation} "
            f"({filename})"
        )

    descriptions = {
        "OPEN_APP": (
            "Открываю программу"
        ),

        "OPEN_BROWSER": (
            "Открываю браузер"
        ),

        "SEARCH_WEB": (
            "Ищу информацию"
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

        "OPEN_FOLDER": (
            "Открываю папку"
        ),

        "CREATE_FOLDER": (
            "Создаю папку"
        ),

        "LIST_FILES": (
            "Читаю папку"
        ),

        "HELLO": (
            "Приветствие"
        ),

        "HELP": (
            "Показываю возможности"
        ),

        "EXIT": (
            "Завершаю работу"
        )
    }

    return descriptions.get(
        action,
        action
    )


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

    for index, path in enumerate(
        matches,
        start=1
    ):
        print(
            f"{index}. {path}"
        )

    return True


def execute_action(
    action_data
):
    action = action_data.get(
        "action",
        ""
    )

    filename = action_data.get(
        "filename",
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

    if action == "OPEN_APP":
        open_app(
            action_data.get(
                "app",
                ""
            )
        )

        return True

    if action == "OPEN_BROWSER":
        open_browser()

        return True

    if action == "SEARCH_WEB":
        search_web(
            action_data.get(
                "query",
                ""
            )
        )

        return True

    if action == "CREATE_FILE":
        create_file(
            filename,
            action_data.get(
                "content",
                ""
            )
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
            action_data.get(
                "content",
                ""
            )
        )

        return True

    if action == "FIND_FILE":
        return execute_find_file(
            action_data
        )

    if action == "OPEN_LATEST_FILE":
        open_latest_file(
            action_data.get(
                "folder",
                ""
            ),

            action_data.get(
                "extension",
                ""
            )
        )

        return True

    if action == "OPEN_FOLDER":
        open_folder(
            action_data.get(
                "folder",
                ""
            )
        )

        return True

    if action == "CREATE_FOLDER":
        create_folder(
            action_data.get(
                "folder",
                ""
            ),

            action_data.get(
                "folder_name",
                ""
            )
        )

        return True

    if action == "LIST_FILES":
        list_files(
            action_data.get(
                "folder",
                ""
            )
        )

        return True

    if action == "WORD_EDIT":
        return (
            word_edit(
                filename,
                operation,
                data
            )
            is not None
        )

    if action == "EXCEL_EDIT":
        return (
            excel_edit(
                filename,
                operation,
                data
            )
            is not None
        )

    if action == "HELLO":
        print(
            "Привет! Batka AI на связи."
        )

        return True

    if action == "HELP":
        print(
            "Batka AI умеет работать "
            "с Windows, файлами, Word, Excel "
            "и анализировать документы."
        )

        return True

    if action == "EXIT":
        return "EXIT"

    return False


def is_analysis_command(
    command
):
    lowered = command.lower()

    return (
        (
            ".xlsx" in lowered
            or ".docx" in lowered
        )
        and any(
            word in lowered
            for word in [
                "проанализируй",
                "анализируй",
                "посмотри структуру",
                "анализ документа",
            ]
        )
    )


def is_improvement_command(
    command
):
    lowered = command.lower()

    return (
        (
            ".xlsx" in lowered
            or ".docx" in lowered
        )
        and any(
            word in lowered
            for word in [
                "улучши",
                "исправь",
                "приведи в порядок",
                "сделай аккуратным",
                "сделай нормальным",
            ]
        )
    )


def is_history_command(
    command
):
    lowered = command.lower().strip()

    return lowered in [
        "история",
        "покажи историю",
        "история задач",
        "покажи историю задач",
    ]


def execute_normal_task(
    command,
    actions
):
    started = time.time()

    task = TaskManager(
        command
    )

    steps = [
        task.add_step(
            describe_action(
                action
            )
        )
        for action in actions
    ]

    task.start()

    for step, action in zip(
        steps,
        actions
    ):
        result = task.run_step(
            step,
            execute_action,
            action
        )

        if result == "EXIT":
            task.finish()

            return "EXIT"

        if result is False:
            task.finish()

            add_history_entry(
                command,
                "error",
                "general",
                duration=(
                    time.time()
                    - started
                )
            )

            return False

    task.finish()

    add_history_entry(
        command,
        "success",
        "general",
        duration=(
            time.time()
            - started
        )
    )

    return True


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

        lowered = (
            command.lower()
        )

        # =============================================
        # CONFIRM PLAN
        # =============================================

        if pending_plan:
            if lowered in [
                "да",
                "давай",
                "выполняй",
                "выполни",
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
                    "Документ не изменён."
                )

                pending_plan = None

                continue

        # =============================================
        # HISTORY
        # =============================================

        if is_history_command(
            command
        ):
            show_history(
                20
            )

            continue

        # =============================================
        # IMPROVEMENT
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
        # ANALYSIS
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
                f"Ошибка мозга Batka: "
                f"{type(e).__name__}: "
                f"{e}"
            )

            continue

        actions = result.get(
            "actions",
            []
        )

        if not actions:
            print(
                "Не удалось понять команду."
            )

            continue

        result = execute_normal_task(
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