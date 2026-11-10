from datetime import datetime
from uuid import UUID
from model import TaskRepository, TaskState
from mvc import AppView


class AppController:

    def __init__(self):
        self.repo = TaskRepository()
        self.view = AppView()

    def process_add_task(self):
        text_input = input("Enter task text: ").strip()
        if not text_input:
            self.view.show_alert("Task text cannot be empty!")
            return

        raw_date = input(
            "Enter target date (format: YYYY-MM-DD HH:MM): "
        ).strip()
        raw_date = " ".join(raw_date.split())

        try:
            parsed_date = datetime.strptime(raw_date, "%Y-%m-%d %H:%M")
        except ValueError:
            self.view.show_alert(
                "Invalid datetime format! Use YYYY-MM-DD HH:MM."
            )
            return

        created_entry = self.repo.create_item(
            content=text_input, target_time=parsed_date
        )
        self.view.show_info(
            f"Record created successfully. ID: {created_entry.uid}"
        )

    def process_change_state(self):
        id_str = input("Enter item ID to update status: ").strip()
        try:
            target_uuid = UUID(id_str)
        except ValueError:
            self.view.show_alert("Invalid UUID format!")
            return

        try:
            target_item = self.repo.fetch_by_id(target_uuid)
        except ValueError:
            target_item = None

        if not target_item:
            self.view.show_alert("Task record does not exist!")
            return

        print("Select new state:")
        print("1. In Progress")
        print("2. Done")
        opt = input("Choice (1-2): ").strip()

        if opt == "1":
            new_st = TaskState.IN_PROGRESS
        elif opt == "2":
            new_st = TaskState.DONE
        else:
            self.view.show_alert("Unknown state option!")
            return

        self.repo.modify_item(target_uuid, state=new_st)
        self.view.show_info("Status updated successfully!")

    def process_delete_task(self):
        id_str = input("Enter item ID to delete: ").strip()
        try:
            target_uuid = UUID(id_str)
        except ValueError:
            self.view.show_alert("Invalid UUID format!")
            return

        success = self.repo.remove_item(target_uuid)
        if success:
            self.view.show_info("Record deleted successfully!")
        else:
            self.view.show_alert("Record with this ID was not found!")

    def process_edit_task(self):
        id_str = input("Enter item ID to edit: ").strip()
        try:
            target_uuid = UUID(id_str)
        except ValueError:
            self.view.show_alert("Invalid UUID format!")
            return

        try:
            curr_item = self.repo.fetch_by_id(target_uuid)
        except ValueError:
            curr_item = None

        if not curr_item:
            self.view.show_alert("Task record does not exist!")
            return

        print("Leave empty to keep existing value.")
        new_content = (
            input(f"New content [{curr_item.content}]: ").strip() or None
        )

        old_dt = curr_item.target_time.strftime("%Y-%m-%d %H:%M")
        dt_input = input(f"New target date [{old_dt}]: ").strip()
        new_dt = None

        if dt_input:
            dt_input = " ".join(dt_input.split())
            try:
                new_dt = datetime.strptime(dt_input, "%Y-%m-%d %H:%M")
            except ValueError:
                self.view.show_alert(
                    "Invalid date format. Time left unchanged."
                )

        self.repo.modify_item(
            target_uuid, content=new_content, target_time=new_dt
        )
        self.view.show_info("Task record modified successfully!")

    def process_show_all(self):
        all_records = self.repo.fetch_all()
        self.view.render_table(all_records)

    def process_filter_by_state(self):
        print("Select status filter:")
        print("1. Pending")
        print("2. In Progress")
        print("3. Done")
        num_choice = input("Option (1-3): ").strip()

        status_map = {
            "1": TaskState.PENDING,
            "2": TaskState.IN_PROGRESS,
            "3": TaskState.DONE,
        }
        selected_st = status_map.get(num_choice)
        if not selected_st:
            self.view.show_alert("Invalid selection choice!")
            return

        results = self.repo.filter_by_state(selected_st)
        self.view.render_table(results)

    def process_show_by_id(self):
        id_str = input("Enter item ID to inspect: ").strip()
        try:
            target_uuid = UUID(id_str)
        except ValueError:
            self.view.show_alert("Invalid UUID format!")
            return

        try:
            found_item = self.repo.fetch_by_id(target_uuid)
        except ValueError:
            found_item = None

        self.view.render_item(found_item)