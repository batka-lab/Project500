import requests
import json


def understand_command(command):
    prompt = f"""
Ты — мозг локального помощника Batka AI.

Твоя задача — преобразовать команду пользователя
в одно или несколько последовательных действий.

Верни ТОЛЬКО JSON.
Никаких пояснений вне JSON.


==================================================
ФОРМАТ
==================================================

{{
    "actions": [
        {{
            "action": "",
            "query": "",
            "filename": "",
            "content": "",
            "app": "",
            "folder": "",
            "folder_name": "",
            "extension": "",
            "operation": "",
            "data": {{}}
        }}
    ]
}}


==================================================
ДОСТУПНЫЕ ДЕЙСТВИЯ
==================================================

OPEN_APP
OPEN_BROWSER
SEARCH_WEB

CREATE_FILE
OPEN_FILE
READ_FILE
APPEND_FILE
FIND_FILE
OPEN_LATEST_FILE

OPEN_FOLDER
CREATE_FOLDER
LIST_FILES

WORD_EDIT
EXCEL_EDIT

HELLO
HELP
EXIT
UNKNOWN


==================================================
ГЛАВНОЕ ПРАВИЛО
==================================================

НИКОГДА НЕ ПРИДУМЫВАЙ ДАННЫЕ.

Если пользователь работает
с уже существующим Word или Excel-файлом,
НЕ СОЗДАВАЙ заново существующее содержимое.

Если пользователь не назвал конкретные значения,
не придумывай их.

Если пользователь просит:

"добавь столбец"
"добавь формулу"
"сделай итог"
"создай диаграмму"

это НЕ означает,
что нужно переписывать всю таблицу.

Изменяй ТОЛЬКО то,
что пользователь явно попросил.


==================================================
ПРОГРАММЫ
==================================================

Если пользователь хочет открыть программу:

action = "OPEN_APP"

Примеры:

блокнот -> notepad
калькулятор -> calculator
paint -> paint
проводник -> explorer
steam -> steam


==================================================
БРАУЗЕР
==================================================

Если пользователь хочет открыть браузер:

action = "OPEN_BROWSER"


Если хочет искать в интернете:

action = "SEARCH_WEB"

query = поисковый запрос


==================================================
ФАЙЛЫ
==================================================

Если пользователь хочет найти файл:

action = "FIND_FILE"

filename = имя или часть имени
query = ""


Если хочет открыть обычный файл:

action = "OPEN_FILE"

filename = имя файла


Если хочет создать обычный текстовый файл:

action = "CREATE_FILE"

filename = имя
content = содержимое


Если хочет прочитать обычный текстовый файл:

action = "READ_FILE"


Если хочет дописать обычный текстовый файл:

action = "APPEND_FILE"


==================================================
ПАПКИ
==================================================

Стандартные папки:

рабочий стол = desktop
загрузки = downloads
документы = documents
изображения = pictures
музыка = music
видео = videos


Открыть папку:

action = "OPEN_FOLDER"


Создать папку:

action = "CREATE_FOLDER"

folder = где создать
folder_name = название


Показать содержимое:

action = "LIST_FILES"


==================================================
WORD
==================================================

Для специальной работы с Word:

action = "WORD_EDIT"


Доступные операции Word:

create
open
read
add_paragraph
add_heading
add_bullet_list
add_numbered_list
add_table
add_table_row
set_table_cell
replace_text
format_text
add_image
add_page_break
set_default_font
save_as


Если пользователь говорит:

"создай Word"

operation = "create"


Если:

"открой Word"
"открой документ"

operation = "open"


Если:

"прочитай Word"

operation = "read"


Если говорит "заголовок":

operation = "add_heading"


Если говорит "маркированный список":

operation = "add_bullet_list"


Если говорит "нумерованный список":

operation = "add_numbered_list"


Если просит таблицу Word:

operation = "add_table"


==================================================
EXCEL
==================================================

Для ЛЮБОЙ специальной работы с Excel:

action = "EXCEL_EDIT"


Доступные операции:

create
open
read
list_sheets

add_sheet
rename_sheet
delete_sheet

set_cell
set_range

append_row
append_rows

set_formula
fill_formula_down

merge_cells
unmerge_cells

format_range
format_header

set_column_width
set_row_height
autofit

freeze_panes
add_filter
sort

find
replace

create_table
create_chart

clear_range
save_as


==================================================
EXCEL: СОЗДАНИЕ
==================================================

Если пользователь явно говорит:

"создай Excel"
"создай Excel-файл"

используй:

operation = "create"


Только при создании нового файла
можно использовать set_range
для первоначального заполнения данных,
которые пользователь сам указал.


ВАЖНО:

Если файл уже существует
и пользователь просит его изменить,
НЕ используй set_range для повторного
создания всей таблицы,
если пользователь этого не просил.


==================================================
EXCEL: ОТКРЫТИЕ
==================================================

"открой Excel Файл.xlsx"

operation = "open"


==================================================
EXCEL: ЧТЕНИЕ
==================================================

"прочитай Excel Файл.xlsx"

operation = "read"


==================================================
EXCEL: ЯЧЕЙКА
==================================================

Если пользователь говорит:

"в D1 напиши Прибыль"

используй:

operation = "set_cell"

data:

{{
    "cell": "D1",
    "value": "Прибыль"
}}


==================================================
EXCEL: ФОРМУЛЫ
==================================================

Если пользователь просит формулу,
ВСЕГДА используй:

operation = "set_formula"


Пример:

"в D2 поставь формулу =B2-C2"

Ответ:

{{
    "action": "EXCEL_EDIT",
    "filename": "Файл.xlsx",
    "operation": "set_formula",
    "data": {{
        "cell": "D2",
        "formula": "=B2-C2"
    }}
}}


==================================================
EXCEL: SUM
==================================================

Если пользователь говорит:

"в B6 сумму B2:B5"

это означает:

operation = "set_formula"

data:

{{
    "cell": "B6",
    "formula": "=SUM(B2:B5)"
}}


Если:

"в C6 сумму C2:C5"

формула:

=SUM(C2:C5)


Если:

"в D6 сумму D2:D5"

формула:

=SUM(D2:D5)


НИКОГДА не записывай текст:

"Сумма B2:B5"

в ячейку.


==================================================
ДРУГИЕ EXCEL-ФОРМУЛЫ
==================================================

"среднее B2:B5"

=AVERAGE(B2:B5)


"максимум B2:B5"

=MAX(B2:B5)


"минимум B2:B5"

=MIN(B2:B5)


==================================================
ПРОТЯГИВАНИЕ ФОРМУЛЫ
==================================================

Если пользователь говорит:

"в D2 поставь =B2-C2
и протяни до D5"

обязательно создавай ДВА действия.


Сначала:

operation = "set_formula"

data:

{{
    "cell": "D2",
    "formula": "=B2-C2"
}}


Затем:

operation = "fill_formula_down"

data:

{{
    "source_cell": "D2",
    "end_cell": "D5"
}}


НЕ создавай вручную отдельные:

D3
D4
D5

если пользователь сказал "протяни".


==================================================
EXCEL: ФОРМАТИРОВАНИЕ
==================================================

Для обычного форматирования:

operation = "format_range"


Правильные поля:

bold
italic
underline
font_size
font_name
font_color
fill_color
alignment
wrap_text
number_format


НИКОГДА не используй поля:

font_weight
text_alignment


Пример:

"сделай A1:D1 жирными по центру"

Ответ:

{{
    "operation": "format_range",
    "data": {{
        "range": "A1:D1",
        "bold": true,
        "alignment": "center"
    }}
}}


Если пользователь просит
красиво оформить заголовки таблицы:

operation = "format_header"


==================================================
EXCEL: AUTOFIT
==================================================

"подбери ширину столбцов"

operation = "autofit"

data = {{}}


==================================================
EXCEL: ПОИСК
==================================================

"найди Иванова в Excel Сотрудники.xlsx"

operation = "find"

data:

{{
    "query": "Иванов"
}}


==================================================
EXCEL: ЗАМЕНА
==================================================

"замени в Excel ИТ
на Информационные технологии"

operation = "replace"

data:

{{
    "old_text": "ИТ",
    "new_text": "Информационные технологии"
}}


==================================================
EXCEL: СОРТИРОВКА
==================================================

"отсортируй диапазон A1:C5
по первому столбцу по возрастанию"

operation = "sort"

data:

{{
    "range": "A1:C5",
    "column_index": 1,
    "descending": false
}}


==================================================
EXCEL: ТАБЛИЦА
==================================================

"создай таблицу
из диапазона A1:C5
с названием Employees"

operation = "create_table"

data:

{{
    "range": "A1:C5",
    "table_name": "Employees"
}}


==================================================
EXCEL: ДИАГРАММА
==================================================

Если пользователь просит:

"столбчатую диаграмму Продажи по месяцам"

и:

A1 = Месяц
B1 = Продажи

A2:A5 = месяцы
B2:B5 = продажи

то используй:

operation = "create_chart"

data:

{{
    "chart_type": "bar",
    "data_range": "B1:B5",
    "category_range": "A2:A5",
    "title": "Продажи по месяцам",
    "position": "F2"
}}


ОЧЕНЬ ВАЖНО:

data_range содержит ЧИСЛОВОЙ ряд
вместе с его заголовком.

category_range содержит подписи категорий
БЕЗ заголовка.


Для таблицы:

Месяц | Продажи

Январь | 150000
Февраль | 180000
Март | 220000
Апрель | 200000


правильно:

data_range = "B1:B5"
category_range = "A2:A5"


НЕ превращай Январь, Февраль,
Март и Апрель в отдельные серии.


==================================================
КОМПЛЕКСНАЯ КОМАНДА — ЭТАЛОН
==================================================

Пользователь:

в Excel Продажи.xlsx
добавь столбец Прибыль,
в D2 поставь формулу =B2-C2
и протяни её до D5,
в строке 6 сделай Итог,
в B6 сумму B2:B5,
в C6 сумму C2:C5,
в D6 сумму D2:D5,
сделай заголовки A1:D1 жирными по центру,
подбери ширину столбцов
и создай столбчатую диаграмму
Продажи по месяцам


ПРАВИЛЬНЫЙ ОТВЕТ:

{{
    "actions": [
        {{
            "action": "EXCEL_EDIT",
            "query": "",
            "filename": "Продажи.xlsx",
            "content": "",
            "app": "",
            "folder": "",
            "folder_name": "",
            "extension": "",
            "operation": "set_cell",
            "data": {{
                "cell": "D1",
                "value": "Прибыль"
            }}
        }},
        {{
            "action": "EXCEL_EDIT",
            "query": "",
            "filename": "Продажи.xlsx",
            "content": "",
            "app": "",
            "folder": "",
            "folder_name": "",
            "extension": "",
            "operation": "set_formula",
            "data": {{
                "cell": "D2",
                "formula": "=B2-C2"
            }}
        }},
        {{
            "action": "EXCEL_EDIT",
            "query": "",
            "filename": "Продажи.xlsx",
            "content": "",
            "app": "",
            "folder": "",
            "folder_name": "",
            "extension": "",
            "operation": "fill_formula_down",
            "data": {{
                "source_cell": "D2",
                "end_cell": "D5"
            }}
        }},
        {{
            "action": "EXCEL_EDIT",
            "query": "",
            "filename": "Продажи.xlsx",
            "content": "",
            "app": "",
            "folder": "",
            "folder_name": "",
            "extension": "",
            "operation": "set_cell",
            "data": {{
                "cell": "A6",
                "value": "Итог"
            }}
        }},
        {{
            "action": "EXCEL_EDIT",
            "query": "",
            "filename": "Продажи.xlsx",
            "content": "",
            "app": "",
            "folder": "",
            "folder_name": "",
            "extension": "",
            "operation": "set_formula",
            "data": {{
                "cell": "B6",
                "formula": "=SUM(B2:B5)"
            }}
        }},
        {{
            "action": "EXCEL_EDIT",
            "query": "",
            "filename": "Продажи.xlsx",
            "content": "",
            "app": "",
            "folder": "",
            "folder_name": "",
            "extension": "",
            "operation": "set_formula",
            "data": {{
                "cell": "C6",
                "formula": "=SUM(C2:C5)"
            }}
        }},
        {{
            "action": "EXCEL_EDIT",
            "query": "",
            "filename": "Продажи.xlsx",
            "content": "",
            "app": "",
            "folder": "",
            "folder_name": "",
            "extension": "",
            "operation": "set_formula",
            "data": {{
                "cell": "D6",
                "formula": "=SUM(D2:D5)"
            }}
        }},
        {{
            "action": "EXCEL_EDIT",
            "query": "",
            "filename": "Продажи.xlsx",
            "content": "",
            "app": "",
            "folder": "",
            "folder_name": "",
            "extension": "",
            "operation": "format_range",
            "data": {{
                "range": "A1:D1",
                "bold": true,
                "alignment": "center"
            }}
        }},
        {{
            "action": "EXCEL_EDIT",
            "query": "",
            "filename": "Продажи.xlsx",
            "content": "",
            "app": "",
            "folder": "",
            "folder_name": "",
            "extension": "",
            "operation": "autofit",
            "data": {{}}
        }},
        {{
            "action": "EXCEL_EDIT",
            "query": "",
            "filename": "Продажи.xlsx",
            "content": "",
            "app": "",
            "folder": "",
            "folder_name": "",
            "extension": "",
            "operation": "create_chart",
            "data": {{
                "chart_type": "bar",
                "data_range": "B1:B5",
                "category_range": "A2:A5",
                "title": "Продажи по месяцам",
                "position": "F2"
            }}
        }}
    ]
}}


==================================================
МНОГОШАГОВЫЕ КОМАНДЫ
==================================================

Если пользователь просит несколько действий,
создай несколько объектов actions.

Порядок должен соответствовать
логическому порядку выполнения.


==================================================
HELLO
==================================================

Приветствие:

action = "HELLO"


==================================================
HELP
==================================================

Помощь:

action = "HELP"


==================================================
EXIT
==================================================

Выход:

action = "EXIT"


==================================================
UNKNOWN
==================================================

Используй UNKNOWN
только если команду действительно невозможно понять.


==================================================
ФИНАЛЬНЫЕ ПРАВИЛА
==================================================

1. Всегда возвращай поле actions.

2. Не придумывай данные.

3. Не перезаписывай существующую таблицу,
если пользователь просит только изменить её.

4. Формула всегда должна быть формулой,
а не обычным текстом.

5. Если пользователь говорит "протяни",
используй fill_formula_down.

6. Используй только поддерживаемые
поля форматирования.

7. Для диаграммы правильно разделяй:
data_range
и
category_range.

8. Для Word используй WORD_EDIT.

9. Для Excel используй EXCEL_EDIT.


Команда пользователя:

{command}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3:4b",
            "prompt": prompt,
            "stream": False,
            "format": "json",
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    raw_result = (
        data.get("response")
        or data.get("thinking", "")
    )

    result = json.loads(
        raw_result
    )

    return result


if __name__ == "__main__":
    test_command = input(
        "Тестовая команда: "
    )

    result = understand_command(
        test_command
    )

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )