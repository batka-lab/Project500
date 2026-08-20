def build_excel_plan(
    analysis
):
    plan = []

    sheets = analysis.get(
        "sheets",
        []
    )

    for sheet in sheets:
        sheet_name = sheet.get(
            "name"
        )

        max_row = int(
            sheet.get(
                "max_row",
                0
            )
            or 0
        )

        max_column = int(
            sheet.get(
                "max_column",
                0
            )
            or 0
        )

        if (
            max_row > 0
            and max_column > 0
        ):
            # =========================================
            # ОФОРМЛЕНИЕ ЗАГОЛОВКОВ
            # =========================================

            last_column = (
                sheet.get(
                    "columns",
                    []
                )
            )

            if last_column:
                last_letter = (
                    last_column[-1]
                    .get(
                        "letter"
                    )
                )

                if last_letter:
                    plan.append(
                        {
                            "title": (
                                f"Оформить заголовки "
                                f"на листе "
                                f"'{sheet_name}'"
                            ),

                            "engine": "excel",

                            "operation": (
                                "format_header"
                            ),

                            "data": {
                                "sheet_name": (
                                    sheet_name
                                ),

                                "range": (
                                    f"A1:"
                                    f"{last_letter}1"
                                )
                            }
                        }
                    )

            # =========================================
            # AUTOFIT
            # =========================================

            plan.append(
                {
                    "title": (
                        f"Подобрать ширину "
                        f"столбцов на листе "
                        f"'{sheet_name}'"
                    ),

                    "engine": "excel",

                    "operation": (
                        "autofit"
                    ),

                    "data": {
                        "sheet_name": (
                            sheet_name
                        )
                    }
                }
            )

        # =============================================
        # FREEZE HEADER
        # =============================================

        if (
            max_row > 5
            and not sheet.get(
                "freeze_panes"
            )
        ):
            plan.append(
                {
                    "title": (
                        f"Закрепить строку "
                        f"заголовков на листе "
                        f"'{sheet_name}'"
                    ),

                    "engine": "excel",

                    "operation": (
                        "freeze_panes"
                    ),

                    "data": {
                        "sheet_name": (
                            sheet_name
                        ),

                        "cell": "A2"
                    }
                }
            )

        # =============================================
        # FILTER
        # =============================================

        if (
            max_row > 1
            and max_column > 0
            and not sheet.get(
                "auto_filter"
            )
            and not sheet.get(
                "tables"
            )
        ):
            columns = sheet.get(
                "columns",
                []
            )

            if columns:
                last_letter = (
                    columns[-1]
                    .get(
                        "letter"
                    )
                )

                if last_letter:
                    plan.append(
                        {
                            "title": (
                                f"Добавить фильтр "
                                f"на лист "
                                f"'{sheet_name}'"
                            ),

                            "engine": "excel",

                            "operation": (
                                "add_filter"
                            ),

                            "data": {
                                "sheet_name": (
                                    sheet_name
                                ),

                                "range": (
                                    f"A1:"
                                    f"{last_letter}"
                                    f"{max_row}"
                                )
                            }
                        }
                    )

    return plan


def build_word_plan(
    analysis
):
    plan = []

    # =============================================
    # ОСНОВНОЙ ШРИФТ
    # =============================================

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

    # =============================================
    # ЗАГОЛОВКИ
    # =============================================

    headings = analysis.get(
        "headings",
        []
    )

    for heading in headings:
        text = heading.get(
            "text",
            ""
        )

        if not text:
            continue

        plan.append(
            {
                "title": (
                    f"Привести заголовок "
                    f"к единому оформлению: "
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

    return plan


def build_improvement_plan(
    analysis
):
    if not analysis:
        return []

    document_type = analysis.get(
        "document_type"
    )

    if document_type == "Excel":
        return build_excel_plan(
            analysis
        )

    if document_type == "Word":
        return build_word_plan(
            analysis
        )

    return []