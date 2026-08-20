import json
from datetime import datetime
from pathlib import Path


HISTORY_DIR = (
    Path.home()
    / ".batka_ai"
)

HISTORY_FILE = (
    HISTORY_DIR
    / "history.json"
)


def _ensure_history():
    HISTORY_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text(
            "[]",
            encoding="utf-8"
        )


def load_history():
    _ensure_history()

    try:
        content = HISTORY_FILE.read_text(
            encoding="utf-8"
        )

        data = json.loads(
            content
        )

        if isinstance(data, list):
            return data

        return []

    except Exception:
        return []


def save_history(history):
    _ensure_history()

    HISTORY_FILE.write_text(
        json.dumps(
            history,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


def add_history_entry(
    command,
    status,
    task_type="general",
    filename="",
    duration=0.0,
    backup_path="",
    details=None
):
    history = load_history()

    entry = {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),

        "command": command,

        "status": status,

        "task_type": task_type,

        "filename": filename,

        "duration": round(
            float(duration or 0),
            3
        ),

        "backup_path": (
            str(backup_path)
            if backup_path
            else ""
        ),

        "details": (
            details
            if details is not None
            else {}
        )
    }

    history.append(
        entry
    )

    # Не даём истории расти бесконечно
    history = history[-1000:]

    save_history(
        history
    )

    return entry


def show_history(limit=20):
    history = load_history()

    if not history:
        print(
            "История Batka AI пока пуста."
        )

        return True

    items = history[
        -limit:
    ]

    items.reverse()

    print()
    print("=" * 70)
    print("ИСТОРИЯ BATKA AI")
    print("=" * 70)

    for item in items:
        status = item.get(
            "status"
        )

        icon = (
            "✓"
            if status == "success"
            else "✗"
        )

        timestamp = item.get(
            "timestamp",
            ""
        )

        command = item.get(
            "command",
            ""
        )

        filename = item.get(
            "filename",
            ""
        )

        duration = item.get(
            "duration",
            0
        )

        print()

        print(
            f"{icon} {timestamp}"
        )

        print(
            f"  Команда: {command}"
        )

        if filename:
            print(
                f"  Файл: {filename}"
            )

        print(
            f"  Время: {duration:.2f} сек."
        )

        backup_path = item.get(
            "backup_path"
        )

        if backup_path:
            print(
                f"  Backup: {backup_path}"
            )

    print()
    print("=" * 70)

    return True