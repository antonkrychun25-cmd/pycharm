from __future__ import annotations
from model import Task


class ConsoleView:

    @staticmethod
    def display_message(message: str):
        print(f"\n[INFO] {message}")

    @staticmethod
    def display_error(message: str):
        print(f"\n[ERROR] {message}")

    @staticmethod
    def display_task_table(tasks: list[Task]):
        if not tasks:
            print("\n[!] Tasks list is empty.")
            return

        header = (
            f"{'ID':<36} | {'Status':<12} | {'Scheduled at':<19} |"
            f" {'Created at':<19} | {'Description':<30}"
        )
        separator = "=" * len(header)
        print("\n" + separator)
        print(header)
        print(separator)
        for t in tasks:
            sched = t.scheduled_at.strftime("%Y-%m-%d %H:%M")
            created = t.created_at.strftime("%Y-%m-%d %H:%M")
            print(
                f"{str(t.id):<36} | {t.status.value:<12} | {sched:<19} |"
                f" {created:<19} | {t.description:<30}"
            )
        print(separator + "\n")

    @staticmethod
    def display_single_task(task: Task | None):
        if not task:
            print("\n[ERROR] Task with such ID does not exist.")
            return
        print("\n--- Task Details ---")
        print(f"ID:           {task.id}")
        print(f"Description:  {task.description}")
        print(f"Status:       {task.status.value}")
        print(f"Scheduled at: {task.scheduled_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Created at:   {task.created_at.strftime('%Y-%m-%d %H:%M')}")
        print("=" * 38)