FILEPATH = "./assets/todos.txt"


def get_todos(filepath=FILEPATH):
    """ Read a text file and return a list of to-do items """
    with open(filepath, 'r') as file:
        todos_list = file.readlines()
    return todos_list


def write_todos(todos_list, filepath=FILEPATH):
    """ Write the list of to-do items in the text file """
    with open(filepath, 'w') as file:
        file.writelines(todos_list)


if __name__ == "__main__":
    print(get_todos())
