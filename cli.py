import time

import functions


def todo_app_cli():
    """ a To-Do app built on Command Line Interface (CLI)"""

    now = time.strftime("%b %d, %Y %H:%M:%S")
    print(f"\nIt is, {now}.")

    while True:
        user_action = input(
            "\nType add, show, edit, complete, or exit:  ").strip()

        if user_action.startswith("add"):
            try:
                new_todo = user_action[4:]
                all_todos = functions.get_todos()
                all_todos.append(new_todo + "\n")
                functions.write_todos(all_todos)
            except FileNotFoundError:
                print(
                    "\n--- No file found for the To-Do list. Creating new empty one. ---")
                functions.write_todos([])
                continue

        elif user_action.startswith("show"):
            try:
                all_todos = functions.get_todos()
                if len(all_todos) == 0:
                    print("\n--- No items found in the To-do list. ---")
                else:
                    print()
                    for index, item in enumerate(all_todos):
                        row = f"{index + 1}- {item.strip('\n')}"
                        print(row)
            except FileNotFoundError:
                print("\n--- No file found for the To-Do list. ---")
                continue

        elif user_action.startswith("edit"):
            try:
                number = int(user_action[5:])
                index = number - 1
                all_todos = functions.get_todos()
                if index < len(all_todos):
                    new_todo = input("\nEnter new todo item:  ").strip()
                    all_todos[index] = new_todo + "\n"
                    functions.write_todos(all_todos)
                else:
                    print("\n--- There is no to-do item with that number. ---")

            except ValueError:
                print("\n--- Your command is not valid. ---")
                continue

        elif user_action.startswith("complete"):
            try:
                number = int(user_action[9:])
                index = number - 1
                all_todos = functions.get_todos()
                todo_to_remove = all_todos[index].strip('\n')
                all_todos.pop(index)
                functions.write_todos(all_todos)
                message = f'\n--- "{
                    todo_to_remove}" removed from the To-do list successfully. ---'
                print(message)

            except ValueError:
                print("\n--- Your command is not valid. ---")
                continue

            except IndexError:
                print("\n--- There is no to-do item with that number. ---")
                continue

        elif user_action == "exit":
            print("\n\n--- Thank you for using this app. Goodbye! ---\n")
            break

        else:
            print("\n--- Invalid Command. ---")


if __name__ == "__main__":
    todo_app_cli()
