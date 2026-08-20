import re

from BatkaAI.services.task_manager import (
    TaskManager
)

from BatkaAI.services.document_reader import (
    find_document,
    read_document,
)

from BatkaAI.services.document_analyzer import (
    analyze_document_structure,
)

from BatkaAI.services.document_planner import (
    build_improvement_plan,
)

from BatkaAI.services.backup_service import (
    create_backup,
)

from BatkaAI.actions.excel_actions import (
    excel_edit,
)

from BatkaAI.actions.office_actions import (
    word_edit,
)


# =========================================================
# ИМЯ ФАЙЛА
# =========================================================


def extract_document_filename(
    command
):
    pattern = (
        r'([A-Za-zА-Яа-яЁё0-9_'
        r'\-\(\) ]+\.(?:xlsx|docx))'
    )

    matches = re.findall(
        pattern,
        command,
        flags=re.IGNORECASE,
    )

    if not matches:
        return None

    filename = (
        matches[-1]
        .strip()
    )

    prefixes = [
        "проанализируй ",
        "проанализировать ",
        "анализируй ",
        "улучши ",
        "исправь ",
        "приведи в порядок ",
        "приведи ",
        "посмотри ",
        "изучи ",
        "проверь ",
        "excel ",
        "word ",
        "файл ",
        "документ ",
    ]

    changed = True

    while changed:
        changed = False

        lowered = (
            filename.lower()
        )

        for prefix in prefixes:
            if lowered.startswith(
                prefix
            ):
                filename = (
                    filename[
                        len(prefix):
                    ]
                    .strip()
                )

                changed = True
                break

    return filename


# =========================================================
# ПЕЧАТЬ EXCEL АНАЛИЗА
# =========================================================


def print_excel_analysis(
    analysis
):
    print()
    print("=" * 60)
    print("АНАЛИЗ EXCEL")
    print("=" * 60)

    print(
        f"Файл: "
        f"{analysis['filename']}"
    )

    print(
        f"Листов: "
        f"{analysis['sheet_count']}"
    )

    print(
        f"Строк суммарно: "
        f"{analysis['total_rows']}"
    )

    print(
        f"Столбцов суммарно: "
        f"{analysis['total_columns']}"
    )

    print(
        f"Формул: "
        f"{analysis['formula_count']}"
    )

    print(
        f"Строк-дубликатов: "
        f"{analysis['duplicate_rows']}"
    )

    print(
        f"Чисел как текст: "
        f"{analysis['text_number_cells']}"
    )

    print()

    print("Листы:")

    for sheet in analysis[
        "sheets"
    ]:
        print()

        print(
            f"• {sheet['name']}"
        )

        print(
            f"  Размер: "
            f"{sheet['max_row']} × "
            f"{sheet['max_column']}"
        )

        headers = [
            str(header)
            for header
            in sheet[
                "headers"
            ]
            if header is not None
        ]

        if headers:
            print(
                "  Заголовки: "
                + ", ".join(
                    headers[:20]
                )
            )

        if sheet[
            "formula_count"
        ]:
            print(
                f"  Формул: "
                f"{sheet['formula_count']}"
            )

    print()

    if analysis[
        "warnings"
    ]:
        print(
            "Обнаруженные проблемы:"
        )

        for warning in analysis[
            "warnings"
        ]:
            print(
                f"  ! {warning}"
            )

    else:
        print(
            "Критических проблем "
            "не обнаружено."
        )

    print()

    if analysis[
        "recommendations"
    ]:
        print(
            "Рекомендации:"
        )

        for index, item in enumerate(
            analysis[
                "recommendations"
            ],
            start=1,
        ):
            print(
                f"  {index}. {item}"
            )

    print("=" * 60)


# =========================================================
# ПЕЧАТЬ WORD АНАЛИЗА
# =========================================================


def print_word_analysis(
    analysis
):
    print()
    print("=" * 60)
    print("АНАЛИЗ WORD")
    print("=" * 60)

    print(
        f"Файл: "
        f"{analysis['filename']}"
    )

    print(
        f"Абзацев: "
        f"{analysis['paragraph_count']}"
    )

    print(
        f"Заголовков: "
        f"{analysis['heading_count']}"
    )

    print(
        f"Таблиц: "
        f"{analysis['table_count']}"
    )

    print(
        f"Изображений: "
        f"{analysis['image_count']}"
    )

    if analysis[
        "headings"
    ]:
        print()
        print(
            "Структура заголовков:"
        )

        for heading in analysis[
            "headings"
        ]:
            print(
                f"  • "
                f"{heading['text']}"
            )

    print()

    if analysis[
        "warnings"
    ]:
        print(
            "Обнаруженные проблемы:"
        )

        for warning in analysis[
            "warnings"
        ]:
            print(
                f"  ! {warning}"
            )

    if analysis[
        "recommendations"
    ]:
        print()
        print(
            "Рекомендации:"
        )

        for index, item in enumerate(
            analysis[
                "recommendations"
            ],
            start=1,
        ):
            print(
                f"  {index}. {item}"
            )

    print("=" * 60)


# =========================================================
# БАЗОВЫЙ АНАЛИЗ
# =========================================================


def analyze_document(
    filename,
):
    file_path = find_document(
        filename
    )

    if not file_path:
        return None

    document = read_document(
        filename
    )

    if not document:
        return None

    analysis = (
        analyze_document_structure(
            document
        )
    )

    return analysis


# =========================================================
# КОМАНДА АНАЛИЗА
# =========================================================


def analyze_document_command(
    command
):
    filename = extract_document_filename(
        command
    )

    if not filename:
        print(
            "Не удалось определить "
            "имя Word или Excel файла."
        )

        return False

    task = TaskManager(
        f"Анализ документа {filename}"
    )

    step_find = task.add_step(
        f"Ищу {filename}"
    )

    step_read = task.add_step(
        "Читаю структуру документа"
    )

    step_analyze = task.add_step(
        "Анализирую содержимое"
    )

    step_report = task.add_step(
        "Формирую отчёт"
    )

    task.start()

    file_path = task.run_step(
        step_find,
        find_document,
        filename,
    )

    if not file_path:
        task.finish()
        return False

    document = task.run_step(
        step_read,
        read_document,
        filename,
    )

    if not document:
        task.finish()
        return False

    analysis = task.run_step(
        step_analyze,
        analyze_document_structure,
        document,
    )

    if not analysis:
        task.finish()
        return False

    def report():
        if (
            analysis[
                "document_type"
            ]
            == "Excel"
        ):
            print_excel_analysis(
                analysis
            )

        else:
            print_word_analysis(
                analysis
            )

        return True

    task.run_step(
        step_report,
        report,
    )

    task.finish()

    return analysis


# =========================================================
# ПОДГОТОВКА ПЛАНА УЛУЧШЕНИЯ
# =========================================================


def prepare_improvement_plan(
    command
):
    filename = extract_document_filename(
        command
    )

    if not filename:
        print(
            "Не удалось определить "
            "имя документа."
        )

        return None

    task = TaskManager(
        f"Подготовка улучшения "
        f"{filename}"
    )

    step_find = task.add_step(
        f"Ищу {filename}"
    )

    step_read = task.add_step(
        "Читаю документ"
    )

    step_analyze = task.add_step(
        "Анализирую структуру"
    )

    step_plan = task.add_step(
        "Формирую безопасный план"
    )

    task.start()

    file_path = task.run_step(
        step_find,
        find_document,
        filename,
    )

    if not file_path:
        task.finish()
        return None

    document = task.run_step(
        step_read,
        read_document,
        filename,
    )

    if not document:
        task.finish()
        return None

    analysis = task.run_step(
        step_analyze,
        analyze_document_structure,
        document,
    )

    if not analysis:
        task.finish()
        return None

    plan = task.run_step(
        step_plan,
        build_improvement_plan,
        analysis,
    )

    if plan is False:
        task.finish()
        return None

    task.finish()

    result = {
        "filename": filename,

        "file_path": str(
            file_path
        ),

        "analysis": analysis,

        "plan": plan,
    }

    print()
    print("=" * 60)
    print("ПЛАН ИЗМЕНЕНИЙ")
    print("=" * 60)

    if not plan:
        print(
            "Batka не нашёл безопасных "
            "автоматических улучшений."
        )

        print("=" * 60)

        return result

    for index, action in enumerate(
        plan,
        start=1,
    ):
        print(
            f"{index}. "
            f"{action['title']}"
        )

    print()
    print(
        "Данные удаляться не будут."
    )

    print(
        "Перед изменениями будет создана "
        "резервная копия."
    )

    print("=" * 60)

    print()
    print(
        "Выполнить этот план? "
        "да / нет"
    )

    return result


# =========================================================
# ВЫПОЛНЕНИЕ ПЛАНА
# =========================================================


def execute_improvement_plan(
    pending_plan
):
    if not pending_plan:
        print(
            "Нет ожидающего плана."
        )

        return False

    filename = pending_plan.get(
        "filename"
    )

    file_path = pending_plan.get(
        "file_path"
    )

    plan = pending_plan.get(
        "plan",
        []
    )

    if not plan:
        print(
            "В плане нет действий."
        )

        return False

    task = TaskManager(
        f"Улучшение документа "
        f"{filename}"
    )

    backup_step = task.add_step(
        "Создаю резервную копию"
    )

    action_steps = []

    for action in plan:
        action_steps.append(
            task.add_step(
                action[
                    "title"
                ]
            )
        )

    verify_step = task.add_step(
        "Проверяю результат"
    )

    task.start()

    backup_path = task.run_step(
        backup_step,
        create_backup,
        file_path,
    )

    if not backup_path:
        task.finish()
        return False

    for step, action in zip(
        action_steps,
        plan,
    ):

        def execute(
            action=action
        ):
            engine = action.get(
                "engine"
            )

            operation = action.get(
                "operation"
            )

            data = action.get(
                "data",
                {}
            )

            if engine == "excel":
                result = excel_edit(
                    filename,
                    operation,
                    data,
                )

                return (
                    result is not None
                )

            if engine == "word":
                result = word_edit(
                    filename,
                    operation,
                    data,
                )

                return (
                    result is not None
                )

            return False

        result = task.run_step(
            step,
            execute,
        )

        if result is False:
            print()
            print(
                "Выполнение остановлено."
            )

            print(
                f"Оригинальная версия "
                f"сохранена здесь:"
            )

            print(
                backup_path
            )

            task.finish()

            return False

    # =============================================
    # ПОВТОРНАЯ ПРОВЕРКА
    # =============================================

    def verify():
        result = analyze_document(
            filename
        )

        if not result:
            return False

        return True

    result = task.run_step(
        verify_step,
        verify,
    )

    task.finish()

    if result is False:
        return False

    print(
        f"Резервная копия: "
        f"{backup_path}"
    )

    return True