import re
import time

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

from BatkaAI.services.semantic_analyzer import (
    analyze_semantics,
)

from BatkaAI.services.document_planner import (
    build_improvement_plan,
)

from BatkaAI.services.backup_service import (
    create_backup,
)

from BatkaAI.services.history_service import (
    add_history_entry,
)

from BatkaAI.actions.excel_actions import (
    excel_edit,
)

from BatkaAI.actions.office_actions import (
    word_edit,
)


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

        lowered = filename.lower()

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


def print_semantic_analysis(
    semantic
):
    if not semantic:
        return

    print()
    print("Содержательный анализ:")

    purpose = semantic.get(
        "document_purpose",
        "Не определено"
    )

    confidence = semantic.get(
        "confidence",
        0
    )

    description = semantic.get(
        "description",
        ""
    )

    print(
        f"  Тип/назначение: "
        f"{purpose}"
    )

    try:
        confidence_percent = (
            float(confidence)
            * 100
        )

        print(
            f"  Уверенность: "
            f"{confidence_percent:.0f}%"
        )

    except Exception:
        pass

    if description:
        print(
            f"  Описание: "
            f"{description}"
        )

    recommendations = semantic.get(
        "semantic_recommendations",
        []
    )

    if recommendations:
        print()
        print(
            "  Рекомендации по содержанию:"
        )

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):
            print(
                f"    {index}. "
                f"{recommendation}"
            )


def print_analysis(
    analysis,
    semantic=None
):
    print()
    print("=" * 65)
    print(
        f"АНАЛИЗ "
        f"{analysis['document_type'].upper()}"
    )
    print("=" * 65)

    print(
        f"Файл: "
        f"{analysis['filename']}"
    )

    if (
        analysis[
            "document_type"
        ]
        == "Excel"
    ):
        print(
            f"Листов: "
            f"{analysis['sheet_count']}"
        )

        print(
            f"Строк: "
            f"{analysis['total_rows']}"
        )

        print(
            f"Столбцов: "
            f"{analysis['total_columns']}"
        )

        print(
            f"Формул: "
            f"{analysis['formula_count']}"
        )

        print(
            f"Дубликатов: "
            f"{analysis['duplicate_rows']}"
        )

        print()

        for sheet in analysis.get(
            "sheets",
            []
        ):
            print(
                f"• {sheet['name']}: "
                f"{sheet['max_row']} × "
                f"{sheet['max_column']}"
            )

            headers = [
                str(item)
                for item in sheet.get(
                    "headers",
                    []
                )
                if item is not None
            ]

            if headers:
                print(
                    "  Заголовки: "
                    + ", ".join(
                        headers[:15]
                    )
                )

    else:
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

    warnings = analysis.get(
        "warnings",
        []
    )

    if warnings:
        print()
        print("Проблемы:")

        for item in warnings:
            print(
                f"  ! {item}"
            )

    recommendations = analysis.get(
        "recommendations",
        []
    )

    if recommendations:
        print()
        print(
            "Технические рекомендации:"
        )

        for index, item in enumerate(
            recommendations,
            start=1
        ):
            print(
                f"  {index}. {item}"
            )

    print_semantic_analysis(
        semantic
    )

    print("=" * 65)


def full_analyze_document(
    filename
):
    file_path = find_document(
        filename
    )

    if not file_path:
        return None

    raw_document = read_document(
        filename
    )

    if not raw_document:
        return None

    structural = (
        analyze_document_structure(
            raw_document
        )
    )

    if not structural:
        return None

    semantic = analyze_semantics(
        raw_document,
        structural
    )

    return {
        "file_path": str(
            file_path
        ),

        "raw_document": raw_document,

        "analysis": structural,

        "semantic": semantic
    }


def analyze_document(
    filename
):
    result = full_analyze_document(
        filename
    )

    if not result:
        return None

    return result[
        "analysis"
    ]


def analyze_document_command(
    command
):
    started = time.time()

    filename = extract_document_filename(
        command
    )

    if not filename:
        print(
            "Не удалось определить "
            "имя документа."
        )

        return False

    task = TaskManager(
        f"Анализ документа {filename}"
    )

    steps = [
        task.add_step(
            f"Ищу {filename}"
        ),

        task.add_step(
            "Читаю структуру"
        ),

        task.add_step(
            "Выполняю технический анализ"
        ),

        task.add_step(
            "Определяю назначение документа"
        ),

        task.add_step(
            "Формирую отчёт"
        )
    ]

    task.start()

    file_path = task.run_step(
        steps[0],
        find_document,
        filename
    )

    if not file_path:
        task.finish()

        add_history_entry(
            command,
            "error",
            "analysis",
            filename,
            time.time() - started
        )

        return False

    raw_document = task.run_step(
        steps[1],
        read_document,
        filename
    )

    if not raw_document:
        task.finish()

        return False

    analysis = task.run_step(
        steps[2],
        analyze_document_structure,
        raw_document
    )

    if not analysis:
        task.finish()

        return False

    semantic = task.run_step(
        steps[3],
        analyze_semantics,
        raw_document,
        analysis
    )

    def report():
        print_analysis(
            analysis,
            semantic
        )

        return True

    task.run_step(
        steps[4],
        report
    )

    task.finish()

    duration = (
        time.time()
        - started
    )

    add_history_entry(
        command,
        "success",
        "analysis",
        filename,
        duration,
        details={
            "semantic": semantic
        }
    )

    return {
        "analysis": analysis,
        "semantic": semantic
    }


def prepare_improvement_plan(
    command
):
    started = time.time()

    filename = extract_document_filename(
        command
    )

    if not filename:
        return None

    task = TaskManager(
        f"Подготовка улучшения "
        f"{filename}"
    )

    steps = [
        task.add_step(
            f"Ищу {filename}"
        ),

        task.add_step(
            "Читаю документ"
        ),

        task.add_step(
            "Анализирую структуру"
        ),

        task.add_step(
            "Определяю назначение документа"
        ),

        task.add_step(
            "Формирую безопасный план"
        )
    ]

    task.start()

    file_path = task.run_step(
        steps[0],
        find_document,
        filename
    )

    if not file_path:
        task.finish()
        return None

    raw_document = task.run_step(
        steps[1],
        read_document,
        filename
    )

    if not raw_document:
        task.finish()
        return None

    analysis = task.run_step(
        steps[2],
        analyze_document_structure,
        raw_document
    )

    if not analysis:
        task.finish()
        return None

    semantic = task.run_step(
        steps[3],
        analyze_semantics,
        raw_document,
        analysis
    )

    plan = task.run_step(
        steps[4],
        build_improvement_plan,
        analysis,
        semantic
    )

    task.finish()

    result = {
        "filename": filename,

        "file_path": str(
            file_path
        ),

        "analysis": analysis,

        "semantic": semantic,

        "plan": plan,

        "original_command": command,

        "started": started
    }

    print()
    print("=" * 65)
    print("ПЛАН ИЗМЕНЕНИЙ")
    print("=" * 65)

    print_semantic_analysis(
        semantic
    )

    print()

    if not plan:
        print(
            "Безопасных автоматических "
            "изменений не найдено."
        )

    else:
        for index, item in enumerate(
            plan,
            start=1
        ):
            print(
                f"{index}. "
                f"{item['title']}"
            )

        print()
        print(
            "✓ Содержимое данных "
            "удаляться не будет."
        )

        print(
            "✓ Перед изменением будет "
            "создан backup."
        )

        print(
            "✓ После изменения документ "
            "будет повторно проверен."
        )

    print("=" * 65)

    if plan:
        print()
        print(
            "Выполнить план? да / нет"
        )

    return result


def execute_improvement_plan(
    pending_plan
):
    if not pending_plan:
        return False

    started = time.time()

    filename = pending_plan[
        "filename"
    ]

    file_path = pending_plan[
        "file_path"
    ]

    plan = pending_plan.get(
        "plan",
        []
    )

    if not plan:
        return False

    task = TaskManager(
        f"Улучшение документа "
        f"{filename}"
    )

    backup_step = task.add_step(
        "Создаю резервную копию"
    )

    action_steps = [
        task.add_step(
            item["title"]
        )
        for item in plan
    ]

    verify_step = task.add_step(
        "Повторно анализирую документ"
    )

    task.start()

    backup_path = task.run_step(
        backup_step,
        create_backup,
        file_path
    )

    if not backup_path:
        task.finish()
        return False

    for step, item in zip(
        action_steps,
        plan
    ):
        engine = item.get(
            "engine"
        )

        operation = item.get(
            "operation"
        )

        data = item.get(
            "data",
            {}
        )

        def execute(
            engine=engine,
            operation=operation,
            data=data
        ):
            if engine == "excel":
                return (
                    excel_edit(
                        filename,
                        operation,
                        data
                    )
                    is not None
                )

            if engine == "word":
                return (
                    word_edit(
                        filename,
                        operation,
                        data
                    )
                    is not None
                )

            return False

        result = task.run_step(
            step,
            execute
        )

        if result is False:
            task.finish()

            add_history_entry(
                pending_plan.get(
                    "original_command",
                    ""
                ),
                "error",
                "safe_edit",
                filename,
                time.time() - started,
                backup_path
            )

            return False

    verified = task.run_step(
        verify_step,
        full_analyze_document,
        filename
    )

    task.finish()

    duration = (
        time.time()
        - started
    )

    add_history_entry(
        pending_plan.get(
            "original_command",
            ""
        ),
        "success",
        "safe_edit",
        filename,
        duration,
        backup_path,
        details={
            "actions": [
                item["title"]
                for item in plan
            ]
        }
    )

    print()
    print(
        f"Резервная копия: "
        f"{backup_path}"
    )

    if verified:
        print(
            "✓ Повторная проверка "
            "документа завершена."
        )

    return True