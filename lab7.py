from controller import AppController


def run_app():
    app = AppController()

    while True:
        print("\n=== TASK MANAGEMENT SYSTEM (MVC) ===")
        print("1. Add new task")
        print("2. Update task status")
        print("3. Remove task")
        print("4. Edit task details")
        print("5. Display all tasks")
        print("6. Filter tasks by state")
        print("7. Find task by UUID")
        print("0. Exit program")

        select = input("\nSelect operation: ").strip()

        if select == "1":
            app.process_add_task()
        elif select == "2":
            app.process_change_state()
        elif select == "3":
            app.process_delete_task()
        elif select == "4":
            app.process_edit_task()
        elif select == "5":
            app.process_show_all()
        elif select == "6":
            app.process_filter_by_state()
        elif select == "7":
            app.process_show_by_id()
        elif select == "0":
            print("Shutting down system. Goodbye!")
            break
        else:
            print("[WARNING] Unknown command option. Try again.")


if __name__ == "__main__":
    run_app()