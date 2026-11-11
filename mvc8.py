from datetime import datetime
from model8 import TaskRepository, TaskState


class AppView:
    def render_table(self, tasks):
        if not tasks:
            print("\n--- No tasks found ---")
            return
        print("\n" + "=" * 65)
        print(f"{'ID':<5} | {'Content':<25} | {'Target Time':<18} | {'State':<10}")
        print("-" * 65)
        for task in tasks:
            t_str = task.target_time.strftime("%Y-%m-%d %H:%M") if task.target_time else "N/A"
            print(f"{task.id:<5} | {task.content:<25} | {t_str:<18} | {task.state.value:<10}")
        print("=" * 65)

    def show_info(self, msg):
        print(f"[INFO] {msg}")

    def show_alert(self, msg):
        print(f"[ERROR] {msg}")


def run_app():
    repo = TaskRepository()
    view = AppView()

    while True:
        print("\n=== TODO App (PostgreSQL Docker) ===")
        print("1. View all tasks")
        print("2. Add new task")
        print("3. View task by ID")
        print("4. Update task state")
        print("5. Edit task content")
        print("6. Delete task")
        print("7. Filter tasks by state")
        print("8. Exit")

        choice = input("Select option (1-8): ").strip()

        if choice == "1":
            tasks = repo.get_all()
            view.render_table(tasks)

        elif choice == "2":
            content = input("Enter task content: ").strip()
            date_str = input("Enter target time (YYYY-MM-DD HH:MM): ").strip()
            try:
                target_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                item = repo.create(content, target_time)
                view.show_info(f"Task created successfully! (ID: {item.id})")
            except ValueError:
                view.show_alert("Invalid date format! Use YYYY-MM-DD HH:MM")

        elif choice == "3":
            raw_id = input("Enter task ID: ").strip()
            if raw_id.isdigit():
                task = repo.get_by_id(int(raw_id))
                if task:
                    view.render_table([task])
                else:
                    view.show_alert("Task not found!")
            else:
                view.show_alert("ID must be an integer!")

        elif choice == "4":
            raw_id = input("Enter task ID: ").strip()
            if raw_id.isdigit():
                print("Select new state: 1. PENDING | 2. IN_PROGRESS | 3. DONE")
                st = input("Choice (1-3): ").strip()
                st_map = {"1": TaskState.PENDING, "2": TaskState.IN_PROGRESS, "3": TaskState.DONE}
                if st in st_map:
                    if repo.update_state(int(raw_id), st_map[st]):
                        view.show_info("Status updated!")
                    else:
                        view.show_alert("Task not found!")
                else:
                    view.show_alert("Invalid state selection!")
            else:
                view.show_alert("ID must be an integer!")

        elif choice == "5":
            raw_id = input("Enter task ID to edit: ").strip()
            if raw_id.isdigit():
                new_content = input("Enter new content: ").strip()
                if repo.update_content(int(raw_id), new_content):
                    view.show_info("Task content updated!")
                else:
                    view.show_alert("Task not found!")
            else:
                view.show_alert("ID must be an integer!")

        elif choice == "6":
            raw_id = input("Enter task ID to delete: ").strip()
            if raw_id.isdigit():
                if repo.delete(int(raw_id)):
                    view.show_info("Task deleted!")
                else:
                    view.show_alert("Task not found!")
            else:
                view.show_alert("ID must be an integer!")

        elif choice == "7":
            print("Select state: 1. PENDING | 2. IN_PROGRESS | 3. DONE")
            st = input("Choice (1-3): ").strip()
            st_map = {"1": TaskState.PENDING, "2": TaskState.IN_PROGRESS, "3": TaskState.DONE}
            if st in st_map:
                tasks = repo.filter_by_state(st_map[st])
                view.render_table(tasks)
            else:
                view.show_alert("Invalid choice!")

        elif choice == "8":
            print("Exiting application...")
            break
        else:
            view.show_alert("Invalid menu option!")