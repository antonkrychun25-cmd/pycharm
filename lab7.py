from controller import TaskController


def main():
    controller = TaskController()

    while True:
        print("\n=== TODO LIST APP (MVC) ===")
        print("1. Create task")
        print("2. Change task status")
        print("3. Delete task")
        print("4. Edit task (description/time)")
        print("5. Show all tasks")
        print("6. Filter tasks by status")
        print("7. Show task by ID")
        print("0. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            controller.create_task_flow()
        elif choice == "2":
            controller.change_status_flow()
        elif choice == "3":
            controller.delete_task_flow()
        elif choice == "4":
            controller.update_task_flow()
        elif choice == "5":
            controller.show_all_tasks_flow()
        elif choice == "6":
            controller.filter_tasks_flow()
        elif choice == "7":
            controller.show_task_by_id_flow()
        elif choice == "0":
            print("Exiting application. Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Please try again.")


if __name__ == "__main__":
    main()