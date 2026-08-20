def build_excel_plan(
    analysis,
    semantic=None
):
    plan = []

    for sheet in analysis.get(
        "sheets",
        []
    ):
        name = sheet.get(
            "name"
        )

        rows = int(
            sheet.get(
                "max_row",
                0
            )
            or 0
        )

        columns = sheet.get(
            "columns",
            []
        )

        if not columns:
            continue

        last_letter = (
            columns[-1]
            .get(
                "letter"
            )
        )

        if not last_letter:
            continue

        if rows >= 1:
            plan.append(
                {
                    "title": (
                        f"Оформить заголовки "
                        f"на листе '{name}'"
                    ),

                    "engine": "excel",

                    "operation": (
                        "format_header"
                    ),

                    "data": {
                        "sheet_name": name,

                        "range": (
                            f"A1:"
                            f"{last_letter}1"
                        )
                    }
                }
            )

        plan.append(
            {
                "title": (
                    f"Подобрать ширину "
                    f"столбцов на листе "
                    f"'{name}'"
                ),

                "engine": "excel",

                "operation": "autofit",

                "data": {
                    "sheet_name": name
                }
            }
        )

        if (
            rows > 5
            and not sheet.get(
                "freeze_panes"
            )
        ):
            plan.append(
                {
                    "title": (
                        f"Закрепить строку "
                        f"заголовков на листе "
                        f"'{name}'"
                    ),

                    "engine": "excel",

                    "operation": (
                        "freeze_panes"
                    ),

                    "data": {
                        "sheet_name": name,
                        "cell": "A2"
                    }
                }
            )

        if (
            rows > 1
            and not sheet.get(
                "auto_filter"
            )
            and not sheet.get(
                "tables"
            )
        ):
            plan.append(
                {
                    "title": (
                        f"Добавить фильтр "
                        f"на лист '{name}'"
                    ),

                    "engine": "excel",

                    "operation": (
                        "add_filter"
                    ),

                    "data": {
                        "sheet_name": name,

                        "range": (
                            f"A1:"
                            f"{last_letter}"
                            f"{rows}"
                        )
                    }
                }
            )

    return plan


def build_word_plan(
    analysis,
    semantic=None
):
    plan = []

    # Основной текст
    plan.append(
        {
            "title": (
                "Привести основной текст "
                "к единому шрифту"
            ),

            "engine": "word",

            "operation": (
                "set_default_font"
            ),

            "data": {
                "font_name": (
                    "Times New Roman"
                ),

                "font_size": 14
            }
        }
    )

    # Заголовки
    for heading in analysis.get(
        "headings",
        []
    ):
        text = str(
            heading.get(
                "text",
                ""
            )
        ).strip()

        if not text:
            continue

        plan.append(
            {
                "title": (
                    f"Оформить заголовок: "
                    f"{text}"
                ),

                "engine": "word",

                "operation": (
                    "format_text"
                ),

                "data": {
                    "target": text,

                    "bold": True,

                    "font_size": 18,

                    "alignment": (
                        "center"
                    )
                }
            }
        )

    # Пока таблицы не перестраиваем,
    # чтобы не рисковать содержимым.
    # Только выводим рекомендацию,
    # но не исполняем автоматически.

    return plan


def build_improvement_plan(
    analysis,
    semantic=None
):
    if not analysis:
        return []

    document_type = analysis.get(
        "document_type"
    )

    if document_type == "Excel":
        return build_excel_plan(
            analysis,
            semantic
        )

    if document_type == "Word":
        return build_word_plan(
            analysis,
            semantic
        )

    return []