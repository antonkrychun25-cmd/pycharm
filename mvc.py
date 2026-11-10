from __future__ import annotations
from model import TodoItem


class AppView:

    @staticmethod
    def show_info(msg: str):
        print(f"\n[SUCCESS] {msg}")

    @staticmethod
    def show_alert(msg: str):
        print(f"\n[WARNING] {msg}")

    @staticmethod
    def render_table(items: list[TodoItem]):
        if not items:
            print("\n[!] No records found in database.")
            return

        header = (
            f"{'UUID':<36} | {'Status':<12} | {'Target Time':<19} |"
            f" {'Created At':<19} | {'Task Content':<30}"
        )
        line = "-" * len(header)
        print("\n" + line)
        print(header)
        print(line)
        for entry in items:
            t_time = entry.target_time.strftime("%Y-%m-%d %H:%M")
            c_time = entry.timestamp.strftime("%Y-%m-%d %H:%M")
            print(
                f"{str(entry.uid):<36} | {entry.state.value:<12} | {t_time:<19} |"
                f" {c_time:<19} | {entry.content:<30}"
            )
        print(line + "\n")

    @staticmethod
    def render_item(item: TodoItem | None):
        if not item:
            print("\n[WARNING] Task record was not found.")
            return
        print("\n=== Item Overview ===")
        print(f"ID:          {item.uid}")
        print(f"Content:     {item.content}")
        print(f"Status:      {item.state.value}")
        print(f"Scheduled:   {item.target_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"Created:     {item.timestamp.strftime('%Y-%m-%d %H:%M')}")
        print("=" * 38)