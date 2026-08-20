def analyze_excel(document):
    recommendations = []
    warnings = []

    total_rows = 0
    total_columns = 0
    total_formulas = 0
    total_duplicates = 0
    total_text_numbers = 0

    for sheet in document.get(
        "sheets",
        [],
    ):
        total_rows += int(
            sheet.get(
                "max_row",
                0,
            )
            or 0
        )

        total_columns += int(
            sheet.get(
                "max_column",
                0,
            )
            or 0
        )

        total_formulas += int(
            sheet.get(
                "formula_count",
                0,
            )
            or 0
        )

        total_duplicates += int(
            sheet.get(
                "duplicate_count",
                0,
            )
            or 0
        )

        text_numbers = sheet.get(
            "text_numbers",
            [],
        )

        total_text_numbers += len(
            text_numbers
        )

        sheet_name = sheet.get(
            "name",
            "Без имени",
        )

        # =============================================
        # ПУСТЫЕ ЗАГОЛОВКИ
        # =============================================

        headers = sheet.get(
            "headers",
            [],
        )

        empty_headers = []

        for index, header in enumerate(
            headers,
            start=1,
        ):
            if (
                header is None
                or str(header).strip() == ""
            ):
                empty_headers.append(
                    index
                )

        if empty_headers:
            warnings.append(
                f"Лист '{sheet_name}': "
                f"обнаружены пустые заголовки "
                f"в столбцах {empty_headers}."
            )

            recommendations.append(
                f"Заполнить пустые заголовки "
                f"на листе '{sheet_name}'."
            )

        # =============================================
        # ДУБЛИКАТЫ
        # =============================================

        duplicate_count = int(
            sheet.get(
                "duplicate_count",
                0,
            )
            or 0
        )

        if duplicate_count > 0:
            warnings.append(
                f"Лист '{sheet_name}': "
                f"обнаружено "
                f"{duplicate_count} "
                f"строк-дубликатов."
            )

            recommendations.append(
                f"Проверить дубликаты "
                f"на листе '{sheet_name}' "
                f"перед удалением."
            )

        # =============================================
        # ЧИСЛА КАК ТЕКСТ
        # =============================================

        if text_numbers:
            warnings.append(
                f"Лист '{sheet_name}': "
                f"{len(text_numbers)} "
                f"числовых значений "
                f"хранятся как текст."
            )

            recommendations.append(
                f"Преобразовать числовые "
                f"значения из текста в числа "
                f"на листе '{sheet_name}'."
            )

        # =============================================
        # ЗАКРЕПЛЕНИЕ ШАПКИ
        # =============================================

        max_row = int(
            sheet.get(
                "max_row",
                0,
            )
            or 0
        )

        freeze_panes = sheet.get(
            "freeze_panes"
        )

        if (
            max_row > 10
            and not freeze_panes
        ):
            recommendations.append(
                f"Закрепить строку заголовков "
                f"на листе '{sheet_name}'."
            )

        # =============================================
        # ФИЛЬТР
        # =============================================

        auto_filter = sheet.get(
            "auto_filter"
        )

        tables = sheet.get(
            "tables",
            [],
        )

        if (
            max_row > 5
            and not auto_filter
            and not tables
        ):
            recommendations.append(
                f"Добавить фильтр "
                f"на лист '{sheet_name}'."
            )

        # =============================================
        # ШИРИНА СТОЛБЦОВ
        # =============================================

        columns = sheet.get(
            "columns",
            [],
        )

        default_width_columns = []

        for column in columns:
            width = column.get(
                "width"
            )

            letter = column.get(
                "letter",
                "",
            )

            if (
                width is None
                or width <= 13
            ):
                if letter:
                    default_width_columns.append(
                        letter
                    )

        if (
            int(
                sheet.get(
                    "max_column",
                    0,
                )
                or 0
            ) > 1
            and default_width_columns
        ):
            recommendations.append(
                f"Проверить автоширину "
                f"столбцов на листе "
                f"'{sheet_name}'."
            )

        # =============================================
        # БОЛЬШОЙ ЛИСТ
        # =============================================

        if max_row > 1000:
            recommendations.append(
                f"Лист '{sheet_name}' содержит "
                f"более 1000 строк. "
                f"Рекомендуется проверить "
                f"фильтры, закрепление шапки "
                f"и удобство навигации."
            )

        # =============================================
        # ФОРМУЛЫ
        # =============================================

        formula_count = int(
            sheet.get(
                "formula_count",
                0,
            )
            or 0
        )

        if formula_count > 0:
            recommendations.append(
                f"На листе '{sheet_name}' "
                f"обнаружено {formula_count} формул. "
                f"Перед серьёзным редактированием "
                f"их следует сохранить."
            )

    recommendations = list(
        dict.fromkeys(
            recommendations
        )
    )

    warnings = list(
        dict.fromkeys(
            warnings
        )
    )

    return {
        "document_type": "Excel",

        "filename": document.get(
            "filename",
            "",
        ),

        "sheet_count": int(
            document.get(
                "sheet_count",
                0,
            )
            or 0
        ),

        "total_rows": total_rows,

        "total_columns": (
            total_columns
        ),

        "formula_count": (
            total_formulas
        ),

        "duplicate_rows": (
            total_duplicates
        ),

        "text_number_cells": (
            total_text_numbers
        ),

        "warnings": warnings,

        "recommendations": (
            recommendations
        ),

        "sheets": document.get(
            "sheets",
            [],
        ),
    }


def analyze_word(document):
    warnings = []
    recommendations = []

    paragraph_count = int(
        document.get(
            "paragraph_count",
            0,
        )
        or 0
    )

    non_empty_paragraphs = int(
        document.get(
            "non_empty_paragraphs",
            0,
        )
        or 0
    )

    empty_paragraphs = int(
        document.get(
            "empty_paragraphs",
            0,
        )
        or 0
    )

    heading_count = int(
        document.get(
            "heading_count",
            0,
        )
        or 0
    )

    table_count = int(
        document.get(
            "table_count",
            0,
        )
        or 0
    )

    image_count = int(
        document.get(
            "image_count",
            0,
        )
        or 0
    )

    # =============================================
    # ЗАГОЛОВКИ
    # =============================================

    if (
        non_empty_paragraphs > 10
        and heading_count == 0
    ):
        warnings.append(
            "В документе много текста, "
            "но не обнаружено структурных "
            "заголовков Word."
        )

        recommendations.append(
            "Разделить документ "
            "на логические разделы "
            "и использовать стили "
            "Heading 1 / Heading 2."
        )

    # =============================================
    # ПУСТЫЕ АБЗАЦЫ
    # =============================================

    if empty_paragraphs > 10:
        warnings.append(
            f"Обнаружено много пустых "
            f"абзацев: {empty_paragraphs}."
        )

        recommendations.append(
            "Проверить лишние пустые "
            "абзацы и интервалы "
            "между блоками текста."
        )

    # =============================================
    # ТАБЛИЦЫ
    # =============================================

    if table_count > 0:
        recommendations.append(
            "Проверить единообразие "
            "оформления таблиц."
        )

    # =============================================
    # БОЛЬШОЙ ДОКУМЕНТ
    # =============================================

    if paragraph_count > 100:
        recommendations.append(
            "Документ достаточно большой. "
            "Рекомендуется проверить "
            "структуру заголовков "
            "и навигацию."
        )

    # =============================================
    # ИЗОБРАЖЕНИЯ
    # =============================================

    if image_count > 0:
        recommendations.append(
            "Проверить размеры и "
            "выравнивание изображений."
        )

    return {
        "document_type": "Word",

        "filename": document.get(
            "filename",
            "",
        ),

        "paragraph_count": (
            paragraph_count
        ),

        "heading_count": (
            heading_count
        ),

        "table_count": (
            table_count
        ),

        "image_count": (
            image_count
        ),

        "warnings": list(
            dict.fromkeys(
                warnings
            )
        ),

        "recommendations": list(
            dict.fromkeys(
                recommendations
            )
        ),

        "headings": document.get(
            "headings",
            [],
        ),

        "tables": document.get(
            "tables",
            [],
        ),
    }


# =========================================================
# ГЛАВНАЯ ФУНКЦИЯ
# =========================================================


def analyze_document_structure(
    document
):
    if not document:
        return None

    document_type = document.get(
        "type"
    )

    if document_type == "excel":
        return analyze_excel(
            document
        )

    if document_type == "word":
        return analyze_word(
            document
        )

    return None