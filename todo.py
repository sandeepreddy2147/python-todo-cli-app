import json
import os

# Define the file name for storing tasks
TODO_FILE = 'todolist.json'

def clear_screen():
    """Clears the console screen for a cleaner UI."""
    # 'nt' is for Windows, 'posix' is for macOS/Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def load_tasks_from_file():
    """
    Loads tasks from the JSON file.
    Returns an empty list if the file doesn't exist.
    """
    try:
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks_to_file(tasks):
    """Saves the entire list of tasks to the JSON file."""
    with open(TODO_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)
    print("\n✅ Your tasks have been saved!")

def get_next_unique_no(tasks):
    """Calculates the next unique number for a new task."""
    if not tasks:
        return 1
    # Find the maximum unique number and add 1
    return max(task['uniqueNo'] for task in tasks) + 1

def display_tasks(tasks):
    """Displays all the tasks in a formatted way."""
    clear_screen()
    print("╔══════════════════════════════════════╗")
    print("║          MY TASKS                    ║")
    print("╚══════════════════════════════════════╝")

    if not tasks:
        print("\nYour to-do list is empty. Add a task to get started!\n")
        return

    # Sort tasks to show incomplete ones first
    tasks.sort(key=lambda x: x['isChecked'])

    for i, task in enumerate(tasks, 1):
        status = "✅" if task['isChecked'] else "🔲"
        # Apply a line-through effect by adding a special character sequence
        text = task['text']
        if task['isChecked']:
            # ANSI escape code for strikethrough text
            text = f"\033[9m{text}\033[0m"

        print(f"{i}. {status} {text}")
    print("-" * 38)


def add_task(tasks):
    """Prompts the user to add a new task."""
    print("\n--- Add a New Task ---")
    user_input = input("What needs to be done? > ")

    if not user_input.strip():
        print("\n⚠️  Task cannot be empty. Please enter valid text.")
        return

    new_todo = {
        'text': user_input,
        'uniqueNo': get_next_unique_no(tasks),
        'isChecked': False
    }
    tasks.append(new_todo)
    print(f"\n✨ Task '{user_input}' added successfully!")
    save_tasks_to_file(tasks)


def toggle_task_status(tasks):
    """Marks a task as complete or incomplete."""
    display_tasks(tasks)
    if not tasks:
        return
        
    try:
        task_num = int(input("\nEnter the number of the task to mark as complete/incomplete: "))
        if 1 <= task_num <= len(tasks):
            # Adjust index since list is 0-indexed
            task_index = task_num - 1
            tasks[task_index]['isChecked'] = not tasks[task_index]['isChecked']
            status_text = "complete" if tasks[task_index]['isChecked'] else "incomplete"
            print(f"\n✔️ Task {task_num} marked as {status_text}.")
            save_tasks_to_file(tasks)
        else:
            print("\n⚠️  Invalid task number.")
    except ValueError:
        print("\n⚠️  Invalid input. Please enter a number.")


def delete_task(tasks):
    """Deletes a selected task from the list."""
    display_tasks(tasks)
    if not tasks:
        return
        
    try:
        task_num = int(input("\nEnter the number of the task to delete: "))
        if 1 <= task_num <= len(tasks):
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete task {task_num}? (y/n): ").lower()
            if confirm == 'y':
                removed_task = tasks.pop(task_num - 1)
                print(f"\n🗑️ Task '{removed_task['text']}' has been deleted.")
                save_tasks_to_file(tasks)
            else:
                print("\nDeletion cancelled.")
        else:
            print("\n⚠️  Invalid task number.")
    except ValueError:
        print("\n⚠️  Invalid input. Please enter a number.")


def main():
    """Main function to run the application loop."""
    todo_list = load_tasks_from_file()

    while True:
        display_tasks(todo_list)
        print("\nWhat would you like to do?")
        print("  1. Add a new task")
        print("  2. Mark task as complete/incomplete")
        print("  3. Delete a task")
        print("  4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == '1':
            add_task(todo_list)
        elif choice == '2':
            toggle_task_status(todo_list)
        elif choice == '3':
            delete_task(todo_list)
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n⚠️  Invalid choice. Please select a number from 1 to 4.")

        input("\nPress Enter to return to the menu...")


if __name__ == "__main__":
    main()