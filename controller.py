from datetime import datetime
from uuid import UUID
from model import TaskManager, TaskStatus
from mvc import ConsoleView


class TaskController:

    def __init__(self):
        self.task_manager = TaskManager()
        self.console_view = ConsoleView()

    def create_task_flow(self):
        description_text = input("Enter task description: ").strip()
        if not description_text:
            self.console_view.display_error("Task description cannot be empty!")
            return

        date_input = input(
            "Enter scheduled date and time (format: YYYY-MM-DD HH:MM): "
        ).strip()

        # Нормализуем пробелы, чтобы избежать ошибок парсинга
        date_input = " ".join(date_input.split())

        try:
            scheduled_date = datetime.strptime(date_input, "%Y-%m-%d %H:%M")
        except ValueError:
            self.console_view.display_error(
                "Incorrect datetime format! Please use YYYY-MM-DD HH:MM."
            )
            return

        created_task = self.task_manager.add_task(
            description=description_text, scheduled_at=scheduled_date
        )
        self.console_view.display_message(
            f"New task created successfully. Assigned ID: {created_task.id}"
        )

    def change_status_flow(self):
        input_id = input("Enter target task ID for status update: ").strip()
        try:
            target_uuid = UUID(input_id)
        except ValueError:
            self.console_view.display_error("Invalid UUID syntax!")
            return

        try:
            existing_task = self.task_manager.get_task(target_uuid)
        except ValueError:
            existing_task = None

        if not existing_task:
            self.console_view.display_error("Specified task ID does not exist!")
            return

        print("Select new task state:")
        print("1. In Progress")
        print("2. Completed")
        option = input("Enter option (1-2): ").strip()

        if option == "1":
            updated_status = TaskStatus.IN_PROGRESS
        elif option == "2":
            updated_status = TaskStatus.COMPLETED
        else:
            self.console_view.display_error("Invalid selection option!")
            return

        self.task_manager.update_task(target_uuid, status=updated_status)
        self.console_view.display_message("Task status successfully updated!")

    def delete_task_flow(self):
        input_id = input("Enter task ID to remove: ").strip()
        try:
            target_uuid = UUID(input_id)
        except ValueError:
            self.console_view.display_error("Invalid UUID syntax!")
            return

        is_deleted = self.task_manager.delete_task(target_uuid)
        if is_deleted:
            self.console_view.display_message("Task was permanently removed!")
        else:
            self.console_view.display_error("Could not find task with this ID!")

    def update_task_flow(self):
        input_id = input("Enter task ID to modify: ").strip()
        try:
            target_uuid = UUID(input_id)
        except ValueError:
            self.console_view.display_error("Invalid UUID syntax!")
            return

        try:
            current_task = self.task_manager.get_task(target_uuid)
        except ValueError:
            current_task = None

        if not current_task:
            self.console_view.display_error("Specified task ID does not exist!")
            return

        print("Press Enter without typing to skip updating a field.")
        updated_desc = (
                input(f"New description [{current_task.description}]: ").strip()
                or None
        )

        formatted_time = current_task.scheduled_at.strftime("%Y-%m-%d %H:%M")
        raw_time = input(f"New scheduled time [{formatted_time}]: ").strip()
        updated_schedule = None

        if raw_time:
            raw_time = " ".join(raw_time.split())
            try:
                updated_schedule = datetime.strptime(raw_time, "%Y-%m-%d %H:%M")
            except ValueError:
                self.console_view.display_error(
                    "Invalid datetime format. Schedule remained unchanged."
                )

        self.task_manager.update_task(
            target_uuid, description=updated_desc, scheduled_at=updated_schedule
        )
        self.console_view.display_message("Task details successfully modified!")

    def show_all_tasks_flow(self):
        all_tasks = self.task_manager.get_tasks()
        self.console_view.display_task_table(all_tasks)

    def filter_tasks_flow(self):
        print("Select status for filtering:")
        print("1. ToDo")
        print("2. In Progress")
        print("3. Completed")
        choice_option = input("Your selection (1-3): ").strip()

        available_statuses = {
            "1": TaskStatus.TODO,
            "2": TaskStatus.IN_PROGRESS,
            "3": TaskStatus.COMPLETED,
        }
        selected_status = available_statuses.get(choice_option)
        if not selected_status:
            self.console_view.display_error("Invalid filtering choice!")
            return

        filtered_list = self.task_manager.filter_by_status(selected_status)
        self.console_view.display_task_table(filtered_list)

    def show_task_by_id_flow(self):
        input_id = input("Enter task ID to view: ").strip()
        try:
            target_uuid = UUID(input_id)
        except ValueError:
            self.console_view.display_error("Invalid UUID syntax!")
            return

        try:
            target_task = self.task_manager.get_task(target_uuid)
        except ValueError:
            target_task = None

        self.console_view.display_single_task(target_task)