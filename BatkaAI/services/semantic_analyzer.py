import json
import requests


OLLAMA_URL = (
    "http://localhost:11434/api/generate"
)

MODEL = "qwen3:4b"


# =========================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =========================================================


def _safe_float(
    value,
    default=0.0
):
    try:
        result = float(
            value
        )

        if result < 0:
            result = 0.0

        if result > 1:
            result = 1.0

        return result

    except Exception:
        return default


def _normalize_text(
    value
):
    if value is None:
        return ""

    return (
        str(value)
        .strip()
        .lower()
        .replace("ё", "е")
    )


def _unique_strings(
    values
):
    result = []
    used = set()

    for value in values:
        text = str(
            value
        ).strip()

        if not text:
            continue

        key = text.lower()

        if key in used:
            continue

        used.add(
            key
        )

        result.append(
            text
        )

    return result


def _call_qwen(
    prompt
):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    raw = (
        data.get("response")
        or data.get("thinking")
        or "{}"
    )

    if not raw:
        return {}

    try:
        result = json.loads(
            raw
        )

    except json.JSONDecodeError:
        return {}

    if not isinstance(
        result,
        dict
    ):
        return {}

    return result


# =========================================================
# EXCEL: СБОР ЗАГОЛОВКОВ
# =========================================================


def _collect_excel_headers(
    structure_analysis
):
    headers = []

    for sheet in structure_analysis.get(
        "sheets",
        []
    ):
        for header in sheet.get(
            "headers",
            []
        ):
            if header is None:
                continue

            text = str(
                header
            ).strip()

            if text:
                headers.append(
                    text
                )

    return _unique_strings(
        headers
    )


# =========================================================
# EXCEL: ДЕТЕРМИНИРОВАННЫЙ АНАЛИЗ
# =========================================================


def _detect_excel_purpose(
    headers
):
    normalized = {
        _normalize_text(
            header
        )
        for header in headers
    }

    joined = " ".join(
        normalized
    )

    # -----------------------------------------------------
    # Продажи / финансовая таблица
    # -----------------------------------------------------

    sales_words = {
        "продажи",
        "выручка",
        "доход",
        "расходы",
        "затраты",
        "прибыль",
        "себестоимость",
        "месяц",
        "оборот",
    }

    sales_hits = [
        word
        for word in sales_words
        if word in joined
    ]

    if (
        "продажи" in joined
        and (
            "месяц" in joined
            or "прибыль" in joined
            or "расходы" in joined
        )
    ):
        return {
            "document_purpose": (
                "Таблица продаж и финансовых показателей"
            ),

            "confidence": 0.96,

            "description": (
                "В книге представлены показатели "
                "продаж по периодам, а также связанные "
                "финансовые показатели."
            ),

            "important_columns": [
                header
                for header in headers
                if _normalize_text(
                    header
                )
                in sales_words
            ],

            "semantic_recommendations": [
                (
                    "Сохранить формулы расчёта прибыли "
                    "и итоговых показателей."
                ),
                (
                    "Для денежных столбцов можно "
                    "использовать единый числовой "
                    "или денежный формат."
                ),
                (
                    "Для анализа динамики удобно "
                    "использовать диаграмму продаж "
                    "по периодам."
                ),
            ]
        }

    if len(
        sales_hits
    ) >= 3:
        return {
            "document_purpose": (
                "Финансовая таблица"
            ),

            "confidence": 0.88,

            "description": (
                "По названиям столбцов документ "
                "содержит финансовые показатели."
            ),

            "important_columns": [
                header
                for header in headers
                if _normalize_text(
                    header
                )
                in sales_words
            ],

            "semantic_recommendations": [
                (
                    "Проверить единый формат "
                    "финансовых значений."
                ),
                (
                    "Сохранить существующие формулы "
                    "при редактировании."
                ),
            ]
        }

    # -----------------------------------------------------
    # Сотрудники
    # -----------------------------------------------------

    employee_words = {
        "фио",
        "фамилия",
        "имя",
        "отчество",
        "должность",
        "отдел",
        "подразделение",
        "сотрудник",
        "табельный номер",
    }

    employee_hits = [
        word
        for word in employee_words
        if word in joined
    ]

    if len(
        employee_hits
    ) >= 2:
        return {
            "document_purpose": (
                "База сотрудников"
            ),

            "confidence": 0.90,

            "description": (
                "Структура похожа на кадровую "
                "или административную базу сотрудников."
            ),

            "important_columns": [
                header
                for header in headers
                if any(
                    word
                    in _normalize_text(
                        header
                    )
                    for word in employee_words
                )
            ],

            "semantic_recommendations": [
                (
                    "Проверить уникальность записей "
                    "сотрудников."
                ),
                (
                    "Закрепить строку заголовков "
                    "и использовать фильтры."
                ),
            ]
        }

    # -----------------------------------------------------
    # IT-инвентаризация
    # -----------------------------------------------------

    inventory_words = {
        "ip",
        "ip адрес",
        "mac",
        "mac адрес",
        "компьютер",
        "пк",
        "hostname",
        "имя пк",
        "серийный номер",
        "инвентарный номер",
        "оборудование",
        "модель",
    }

    inventory_hits = [
        word
        for word in inventory_words
        if word in joined
    ]

    if len(
        inventory_hits
    ) >= 2:
        return {
            "document_purpose": (
                "База учёта IT-оборудования"
            ),

            "confidence": 0.90,

            "description": (
                "Структура похожа на реестр "
                "компьютеров, сетевых адресов "
                "и оборудования."
            ),

            "important_columns": [
                header
                for header in headers
                if any(
                    word
                    in _normalize_text(
                        header
                    )
                    for word in inventory_words
                )
            ],

            "semantic_recommendations": [
                (
                    "Проверить уникальность IP, MAC "
                    "и инвентарных номеров."
                ),
                (
                    "Сделать удобный поиск "
                    "по пользователю и имени ПК."
                ),
            ]
        }

    # -----------------------------------------------------
    # Учёт товаров
    # -----------------------------------------------------

    goods_words = {
        "товар",
        "наименование",
        "артикул",
        "количество",
        "цена",
        "стоимость",
        "остаток",
        "склад",
    }

    goods_hits = [
        word
        for word in goods_words
        if word in joined
    ]

    if len(
        goods_hits
    ) >= 3:
        return {
            "document_purpose": (
                "Товарная или складская таблица"
            ),

            "confidence": 0.86,

            "description": (
                "Структура похожа на учёт товаров, "
                "остатков или стоимости."
            ),

            "important_columns": [
                header
                for header in headers
                if any(
                    word
                    in _normalize_text(
                        header
                    )
                    for word in goods_words
                )
            ],

            "semantic_recommendations": [
                (
                    "Проверить числовые форматы "
                    "для цены и количества."
                ),
                (
                    "Добавить фильтрацию "
                    "и сортировку по ключевым полям."
                ),
            ]
        }

    return None


# =========================================================
# EXCEL: QWEN
# =========================================================


def _analyze_excel_with_qwen(
    structure_analysis,
    headers
):
    sheets = []

    for sheet in structure_analysis.get(
        "sheets",
        []
    ):
        sheets.append(
            {
                "name": sheet.get(
                    "name"
                ),

                "headers": sheet.get(
                    "headers",
                    []
                ),

                "rows": sheet.get(
                    "max_row",
                    0
                ),

                "columns": sheet.get(
                    "max_column",
                    0
                ),

                "formula_count": sheet.get(
                    "formula_count",
                    0
                )
            }
        )

    prompt = f"""
Ты — модуль содержательного анализа Excel
локального помощника Batka AI.

Тебе передана реальная структура существующей
Excel-книги.

Определи наиболее вероятное назначение документа.

ВАЖНО:

1. Не придумывай значения и столбцы.
2. Используй реальные заголовки.
3. Если видишь Месяц, Продажи, Расходы, Прибыль,
   это таблица продаж и финансовых показателей.
4. Если видишь ФИО, Должность, Отдел,
   это база сотрудников.
5. Если видишь IP, MAC, ПК, оборудование,
   это база IT-инфраструктуры.
6. confidence должен быть числом от 0 до 1.
7. Не возвращай confidence = 0,
   если назначение очевидно из заголовков.

Верни ТОЛЬКО JSON:

{{
    "document_purpose": "",
    "confidence": 0.0,
    "description": "",
    "important_columns": [],
    "semantic_recommendations": []
}}

Все реальные заголовки:

{json.dumps(
    headers,
    ensure_ascii=False,
    indent=2
)}

Структура листов:

{json.dumps(
    sheets,
    ensure_ascii=False,
    indent=2
)}
"""

    return _call_qwen(
        prompt
    )


# =========================================================
# EXCEL: ГЛАВНАЯ ФУНКЦИЯ
# =========================================================


def analyze_excel_semantics(
    structure_analysis
):
    headers = (
        _collect_excel_headers(
            structure_analysis
        )
    )

    # Сначала надёжные правила
    deterministic = (
        _detect_excel_purpose(
            headers
        )
    )

    # Потом Qwen
    try:
        qwen_result = (
            _analyze_excel_with_qwen(
                structure_analysis,
                headers
            )
        )

    except Exception:
        qwen_result = {}

    qwen_purpose = str(
        qwen_result.get(
            "document_purpose",
            ""
        )
        or ""
    ).strip()

    qwen_confidence = (
        _safe_float(
            qwen_result.get(
                "confidence",
                0
            )
        )
    )

    # Если Qwen дал сильный ответ,
    # можно использовать его.
    if (
        qwen_purpose
        and qwen_purpose.lower()
        not in {
            "не определено",
            "неизвестно",
            "unknown",
        }
        and qwen_confidence >= 0.75
    ):
        return {
            "document_purpose": (
                qwen_purpose
            ),

            "confidence": (
                qwen_confidence
            ),

            "description": str(
                qwen_result.get(
                    "description",
                    ""
                )
                or ""
            ),

            "important_columns": (
                _unique_strings(
                    qwen_result.get(
                        "important_columns",
                        []
                    )
                )
            ),

            "semantic_recommendations": (
                _unique_strings(
                    qwen_result.get(
                        "semantic_recommendations",
                        []
                    )
                )
            )
        }

    # Если Qwen не справился,
    # используем надёжный локальный анализ.
    if deterministic:
        return deterministic

    # Если Qwen хоть что-то понял
    if (
        qwen_purpose
        and qwen_purpose.lower()
        not in {
            "не определено",
            "неизвестно",
            "unknown",
        }
    ):
        return {
            "document_purpose": (
                qwen_purpose
            ),

            "confidence": (
                qwen_confidence
            ),

            "description": str(
                qwen_result.get(
                    "description",
                    ""
                )
                or ""
            ),

            "important_columns": (
                _unique_strings(
                    qwen_result.get(
                        "important_columns",
                        []
                    )
                )
            ),

            "semantic_recommendations": (
                _unique_strings(
                    qwen_result.get(
                        "semantic_recommendations",
                        []
                    )
                )
            )
        }

    return {
        "document_purpose": (
            "Табличный документ"
        ),

        "confidence": 0.40,

        "description": (
            "Назначение документа нельзя "
            "уверенно определить только "
            "по имеющейся структуре."
        ),

        "important_columns": headers,

        "semantic_recommendations": []
    }


# =========================================================
# WORD: ДЕТЕРМИНИРОВАННЫЙ АНАЛИЗ
# =========================================================


def _detect_word_purpose(
    raw_document
):
    texts = []

    for heading in raw_document.get(
        "headings",
        []
    ):
        texts.append(
            heading.get(
                "text",
                ""
            )
        )

    for paragraph in raw_document.get(
        "paragraph_preview",
        []
    )[:30]:
        texts.append(
            paragraph.get(
                "text",
                ""
            )
        )

    joined = _normalize_text(
        " ".join(
            texts
        )
    )

    if (
        "отчет" in joined
        or "итоги работы" in joined
        or "выполненные работы" in joined
    ):
        return {
            "document_purpose": (
                "Отчёт"
            ),

            "confidence": 0.92,

            "description": (
                "Документ содержит признаки "
                "рабочего или итогового отчёта."
            ),

            "semantic_recommendations": [
                (
                    "Сохранить логическую структуру "
                    "заголовков и разделов."
                ),
                (
                    "Привести оформление таблиц "
                    "и основного текста к единому стилю."
                ),
            ]
        }

    if "договор" in joined:
        return {
            "document_purpose": (
                "Договор"
            ),

            "confidence": 0.94,

            "description": (
                "По тексту документ похож на договор."
            ),

            "semantic_recommendations": [
                (
                    "Не изменять юридическое содержание "
                    "без явного указания пользователя."
                ),
                (
                    "Автоматически менять только "
                    "безопасное оформление."
                ),
            ]
        }

    if (
        "инструкция" in joined
        or "порядок выполнения" in joined
    ):
        return {
            "document_purpose": (
                "Инструкция"
            ),

            "confidence": 0.90,

            "description": (
                "Документ содержит признаки инструкции "
                "или регламента."
            ),

            "semantic_recommendations": [
                (
                    "Проверить структуру разделов "
                    "и последовательность шагов."
                ),
            ]
        }

    return None


# =========================================================
# WORD: QWEN
# =========================================================


def analyze_word_semantics(
    raw_document
):
    deterministic = (
        _detect_word_purpose(
            raw_document
        )
    )

    headings = [
        item.get(
            "text",
            ""
        )
        for item in raw_document.get(
            "headings",
            []
        )
    ]

    paragraphs = [
        item.get(
            "text",
            ""
        )
        for item in raw_document.get(
            "paragraph_preview",
            []
        )[:20]
    ]

    table_previews = []

    for table in raw_document.get(
        "tables",
        []
    )[:5]:
        table_previews.append(
            table.get(
                "preview",
                []
            )[:5]
        )

    prompt = f"""
Ты — модуль содержательного анализа Word
локального помощника Batka AI.

Определи назначение существующего документа.

Не придумывай информацию.

Верни ТОЛЬКО JSON:

{{
    "document_purpose": "",
    "confidence": 0.0,
    "description": "",
    "semantic_recommendations": []
}}

confidence — число от 0 до 1.

Заголовки:

{json.dumps(
    headings,
    ensure_ascii=False,
    indent=2
)}

Фрагменты текста:

{json.dumps(
    paragraphs,
    ensure_ascii=False,
    indent=2
)}

Таблицы:

{json.dumps(
    table_previews,
    ensure_ascii=False,
    indent=2
)}
"""

    try:
        qwen = _call_qwen(
            prompt
        )

    except Exception:
        qwen = {}

    purpose = str(
        qwen.get(
            "document_purpose",
            ""
        )
        or ""
    ).strip()

    confidence = _safe_float(
        qwen.get(
            "confidence",
            0
        )
    )

    if (
        purpose
        and purpose.lower()
        not in {
            "не определено",
            "неизвестно",
            "unknown",
        }
        and confidence >= 0.75
    ):
        return {
            "document_purpose": purpose,

            "confidence": confidence,

            "description": str(
                qwen.get(
                    "description",
                    ""
                )
                or ""
            ),

            "semantic_recommendations": (
                _unique_strings(
                    qwen.get(
                        "semantic_recommendations",
                        []
                    )
                )
            )
        }

    if deterministic:
        return deterministic

    if purpose:
        return {
            "document_purpose": purpose,

            "confidence": confidence,

            "description": str(
                qwen.get(
                    "description",
                    ""
                )
                or ""
            ),

            "semantic_recommendations": (
                _unique_strings(
                    qwen.get(
                        "semantic_recommendations",
                        []
                    )
                )
            )
        }

    return {
        "document_purpose": (
            "Word-документ"
        ),

        "confidence": 0.40,

        "description": (
            "Назначение документа пока "
            "нельзя определить уверенно."
        ),

        "semantic_recommendations": []
    }


# =========================================================
# UNIVERSAL
# =========================================================


def analyze_semantics(
    raw_document,
    structure_analysis
):
    document_type = (
        raw_document.get(
            "type"
        )
    )

    if document_type == "excel":
        return (
            analyze_excel_semantics(
                structure_analysis
            )
        )

    if document_type == "word":
        return (
            analyze_word_semantics(
                raw_document
            )
        )

    return {
        "document_purpose": (
            "Неизвестный документ"
        ),

        "confidence": 0,

        "description": "",

        "semantic_recommendations": []
    }