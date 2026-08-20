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
        []
    ):
        name = sheet.get(
            "name",
            "Без имени"
        )

        rows = int(
            sheet.get(
                "max_row",
                0
            )
            or 0
        )

        columns = int(
            sheet.get(
                "max_column",
                0
            )
            or 0
        )

        formulas = int(
            sheet.get(
                "formula_count",
                0
            )
            or 0
        )

        duplicates = int(
            sheet.get(
                "duplicate_count",
                0
            )
            or 0
        )

        text_numbers = sheet.get(
            "text_numbers",
            []
        )

        total_rows += rows
        total_columns += columns
        total_formulas += formulas
        total_duplicates += duplicates
        total_text_numbers += len(
            text_numbers
        )

        headers = sheet.get(
            "headers",
            []
        )

        empty_headers = [
            index
            for index, header
            in enumerate(
                headers,
                start=1
            )
            if (
                header is None
                or str(header).strip() == ""
            )
        ]

        if empty_headers:
            warnings.append(
                f"Лист '{name}': "
                f"пустые заголовки "
                f"{empty_headers}."
            )

        if duplicates:
            warnings.append(
                f"Лист '{name}': "
                f"{duplicates} строк-дубликатов."
            )

            recommendations.append(
                f"Проверить дубликаты "
                f"на листе '{name}'."
            )

        if text_numbers:
            warnings.append(
                f"Лист '{name}': "
                f"{len(text_numbers)} чисел "
                f"хранятся как текст."
            )

        if (
            rows > 5
            and not sheet.get(
                "freeze_panes"
            )
        ):
            recommendations.append(
                f"Закрепить строку заголовков "
                f"на листе '{name}'."
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
            recommendations.append(
                f"Добавить фильтр "
                f"на лист '{name}'."
            )

        if columns > 1:
            recommendations.append(
                f"Проверить автоширину "
                f"столбцов на листе '{name}'."
            )

        if formulas:
            recommendations.append(
                f"Сохранить существующие "
                f"{formulas} формул "
                f"на листе '{name}'."
            )

    return {
        "document_type": "Excel",

        "filename": document.get(
            "filename",
            ""
        ),

        "sheet_count": document.get(
            "sheet_count",
            0
        ),

        "total_rows": total_rows,

        "total_columns": total_columns,

        "formula_count": total_formulas,

        "duplicate_rows": total_duplicates,

        "text_number_cells": (
            total_text_numbers
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

        "sheets": document.get(
            "sheets",
            []
        )
    }


def analyze_word(document):
    warnings = []
    recommendations = []

    paragraph_count = int(
        document.get(
            "paragraph_count",
            0
        )
        or 0
    )

    non_empty = int(
        document.get(
            "non_empty_paragraphs",
            0
        )
        or 0
    )

    empty = int(
        document.get(
            "empty_paragraphs",
            0
        )
        or 0
    )

    headings = document.get(
        "headings",
        []
    )

    tables = document.get(
        "tables",
        []
    )

    images = int(
        document.get(
            "image_count",
            0
        )
        or 0
    )

    if (
        non_empty > 10
        and not headings
    ):
        warnings.append(
            "Документ содержит много текста, "
            "но структурные заголовки "
            "не обнаружены."
        )

        recommendations.append(
            "Добавить структурные заголовки."
        )

    if empty > 10:
        warnings.append(
            f"Много пустых абзацев: "
            f"{empty}."
        )

        recommendations.append(
            "Проверить лишние "
            "пустые абзацы."
        )

    if tables:
        recommendations.append(
            "Привести таблицы "
            "к единому оформлению."
        )

    if images:
        recommendations.append(
            "Проверить размеры "
            "и выравнивание изображений."
        )

    if headings:
        recommendations.append(
            "Привести заголовки "
            "к единому стилю."
        )

    recommendations.append(
        "Проверить единообразие "
        "шрифта основного текста."
    )

    return {
        "document_type": "Word",

        "filename": document.get(
            "filename",
            ""
        ),

        "paragraph_count": paragraph_count,

        "heading_count": len(
            headings
        ),

        "table_count": len(
            tables
        ),

        "image_count": images,

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

        "headings": headings,

        "tables": tables
    }


def analyze_document_structure(
    document
):
    if not document:
        return None

    if (
        document.get("type")
        == "excel"
    ):
        return analyze_excel(
            document
        )

    if (
        document.get("type")
        == "word"
    ):
        return analyze_word(
            document
        )

    return None