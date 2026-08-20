import time
from dataclasses import dataclass, field


@dataclass
class TaskStep:
    title: str
    status: str = "pending"
    duration: float = 0.0
    error: str = ""


@dataclass
class TaskManager:
    title: str
    steps: list[TaskStep] = field(default_factory=list)

    started_at: float = 0.0
    finished_at: float = 0.0

    def add_step(self, title):
        step = TaskStep(
            title=title
        )

        self.steps.append(
            step
        )

        return step

    def start(self):
        self.started_at = time.time()

        print()
        print("=" * 60)
        print(f"Batka выполняет задачу: {self.title}")
        print("=" * 60)

    def run_step(self, step, function, *args, **kwargs):
        index = self.steps.index(step) + 1
        total = len(self.steps)

        print()
        print(
            f"[{index}/{total}] "
            f"{step.title}..."
        )

        step.status = "running"

        started = time.time()

        try:
            result = function(
                *args,
                **kwargs
            )

            step.duration = (
                time.time()
                - started
            )

            if result is False:
                step.status = "error"

                print(
                    f"      ✗ Ошибка"
                )

                return False

            step.status = "done"

            print(
                f"      ✓ Готово "
                f"({step.duration:.2f} сек.)"
            )

            return result

        except Exception as e:
            step.duration = (
                time.time()
                - started
            )

            step.status = "error"
            step.error = (
                f"{type(e).__name__}: {e}"
            )

            print(
                f"      ✗ Ошибка: "
                f"{step.error}"
            )

            return False

    def finish(self):
        self.finished_at = time.time()

        duration = (
            self.finished_at
            - self.started_at
        )

        errors = [
            step
            for step in self.steps
            if step.status == "error"
        ]

        print()
        print("-" * 60)

        if errors:
            print(
                f"✗ Задача завершена с ошибками "
                f"за {duration:.2f} сек."
            )

        else:
            print(
                f"✓ Задача выполнена "
                f"за {duration:.2f} сек."
            )

        print("-" * 60)
        print()