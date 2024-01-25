from datetime import datetime, timedelta
import json
import os
from dateutil.parser import parse


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.data_file = 'tasks.json'

        # Load existing tasks from the data file
        self.load_tasks()

    def load_tasks(self):
        try:
            if self.data_file_exists():
                with open(self.data_file, 'r') as file:
                    self.tasks = json.load(file)
        except Exception as e:
            print(f"Error loading tasks: {e}")

    def save_tasks(self):
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.tasks, file, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def data_file_exists(self):
        try:
            return os.path.exists(self.data_file)
        except Exception as e:
            print(f"Error checking file existence: {e}")
            return False

    def show_tasks(self):
        try:
            if not self.tasks:
                print("No tasks available.")
            else:
                for index, task in enumerate(self.tasks, start=1):
                    print(f"{index}. {task['title']} - {'Completed' if task['completed'] else 'Pending'}")
        except Exception as e:
            print(f"Error showing tasks: {e}")

    def add_task(self, title, due_date=None):
        try:
            new_task = {'title': title, 'completed': False, 'due_date': due_date}
            self.tasks.append(new_task)
            self.save_tasks()
            print(f"Task '{title}' added successfully.")
        except Exception as e:
            print(f"Error adding task: {e}")

    def edit_task(self, task_index, new_title, new_due_date):
        try:
            if 1 <= task_index <= len(self.tasks):
                self.tasks[task_index - 1]['title'] = new_title
                self.tasks[task_index - 1]['due_date'] = new_due_date
                self.save_tasks()
                print("Task edited successfully.")
            else:
                print("Invalid task index.")
        except Exception as e:
            print(f"Error editing task: {e}")

    def delete_task(self, task_index):
        try:
            if 1 <= task_index <= len(self.tasks):
                deleted_task = self.tasks.pop(task_index - 1)
                self.save_tasks()
                print(f"Task '{deleted_task['title']}' deleted successfully.")
            else:
                print("Invalid task index.")
        except Exception as e:
            print(f"Error deleting task: {e}")

    def prioritize_task(self, task_index):
        try:
            if 1 <= task_index <= len(self.tasks):
                self.tasks[task_index - 1]['priority'] = True
                self.save_tasks()
                print("Task prioritized successfully.")
            else:
                print("Invalid task index.")
        except Exception as e:
            print(f"Error prioritizing task: {e}")

    def search_tasks(self, keyword):
        try:
            result_tasks = [task for task in self.tasks if keyword.lower() in task['title'].lower()]
            if result_tasks:
                print(f"Search Results for '{keyword}':")
                for index, task in enumerate(result_tasks, start=1):
                    print(f"{index}. {task['title']} - {'Completed' if task['completed'] else 'Pending'}")
            else:
                print(f"No tasks found for '{keyword}'.")
        except Exception as e:
            print(f"Error searching tasks: {e}")

    def notify_upcoming_tasks(self, days_threshold=3):
        try:
            current_date = datetime.now().date()

            upcoming_tasks = [task for task in self.tasks if 'due_date' in task
                              and task['due_date'] is not None
                              and task['due_date'] != ''
                              and not task['completed']]

            if not upcoming_tasks:
                print("No upcoming tasks.")
                return

            print(f"Upcoming Tasks (within {days_threshold} days):")
            
            for task in upcoming_tasks:
                try:
                    due_date = parse(task['due_date']).date()
                    days_until_due = (due_date - current_date).days

                    if days_until_due <= days_threshold:
                        print(f"- {task['title']} (Due Date: {task['due_date']}, Days until Due: {days_until_due})")

                except ValueError:
                    print(f"Skipping task '{task['title']}' due to invalid date format: {task['due_date']}")

        except Exception as e:
            print(f"Error notifying upcoming tasks: {e}")






# Your main function to interact with the TaskManager
def main():
    task_manager = TaskManager()

    while True:
        print("\nTask Management System")
        print("1. Show Tasks")
        print("2. Add Task")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Prioritize Task")
        print("6. Search Tasks")
        print("7. Notify Upcoming Tasks")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            task_manager.show_tasks()
        elif choice == '2':
            title = input("Enter task title: ")
            due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ")
            task_manager.add_task(title, due_date)
        elif choice == '3':
            task_manager.show_tasks()
            task_index = int(input("Enter the task index to edit: "))
            new_title = input("Enter the new task title: ")
            new_due_date = input("Enter the new due date (YYYY-MM-DD) or leave blank: ")
            task_manager.edit_task(task_index, new_title, new_due_date)
        elif choice == '4':
            task_manager.show_tasks()
            task_index = int(input("Enter the task index to delete: "))
            task_manager.delete_task(task_index)
        elif choice == '5':
            task_manager.show_tasks()
            task_index = int(input("Enter the task index to prioritize: "))
            task_manager.prioritize_task(task_index)
        elif choice == '6':
            keyword = input("Enter the keyword to search tasks: ")
            task_manager.search_tasks(keyword)
        elif choice == '7':
            task_manager.notify_upcoming_tasks()
        elif choice == '8':
            print("Exiting Task Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
