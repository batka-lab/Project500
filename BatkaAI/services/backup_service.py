import shutil

from datetime import datetime
from pathlib import Path


def create_backup(file_path):
    """
    Создаёт резервную копию рядом с оригиналом.

    Пример:

    База.xlsx

    ->

    База_backup_2026-08-20_154500.xlsx
    """

    file_path = Path(
        file_path
    )

    if not file_path.exists():
        print(
            f"Файл для резервного копирования "
            f"не найден: {file_path}"
        )

        return None

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H%M%S"
    )

    backup_name = (
        f"{file_path.stem}"
        f"_backup_"
        f"{timestamp}"
        f"{file_path.suffix}"
    )

    backup_path = (
        file_path.parent
        / backup_name
    )

    shutil.copy2(
        file_path,
        backup_path
    )

    print(
        f"Резервная копия создана: "
        f"{backup_path}"
    )

    return backup_path