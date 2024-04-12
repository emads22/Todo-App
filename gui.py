import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QListWidget, QGridLayout,
                             QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QSizePolicy, QMessageBox, QFileDialog, QInputDialog)
from PyQt6.QtCore import QTimer, QTime, QDate
import functions
import traceback


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do App")

        # Calculate the center position of the screen (x,y) to show app in middle of view-port
        screen = QApplication.primaryScreen().geometry()
        x_center = (screen.width() - self.width()) // 2
        y_center = (screen.height() - self.height()) // 2
        self.setGeometry(x_center, y_center, 500, 300)

        # Set theme (custom style sheet)
        self.setStyleSheet("""            
            background-color: #FF9800;
            color: #FEFDED;
            font-size: 15px;
            font-weight: bold;
        """)

        # Set up a QTimer to update the time label every minute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(60000)  # Update every 60000 milliseconds (1 minute)

        # Initialize selected to-do in listbox
        self.todo_selected = None
        # Initialize list of all todos from the external file 'todos.txt' using functions module
        try:
            todos_list = functions.get_todos()
            # strip the "\n" from each item in order to add them nicely in the list box
            self.all_todos_list = [item.strip() for item in todos_list]
        # if this external file wasnt found, then create a new one with an empty list
        except FileNotFoundError:
            functions.write_todos([])

        # Create a central widget
        main_central_widget = QWidget(self)
        self.setCentralWidget(main_central_widget)

        # Create widgets
        # start with current time
        self.time_label = QLabel(f"{QTime.currentTime().toString('hh:mm')}")
        self.time_label.setStyleSheet("color: #0C2D57;")

        # start with current date e.g.: "Tue, Mar 26, 2024"
        self.date_label = QLabel(
            f"{QDate.currentDate().toString('ddd, MMM d, yyyy')}")
        self.date_label.setStyleSheet("color: #0C2D57;")

        self.todo_input = QLineEdit()
        self.todo_input.setStyleSheet("color: #0C2D57;")
        self.todo_input.setPlaceholderText(" Add a new to-do ")

        self.add_button = QPushButton("Save")
        self.add_button.setStyleSheet("background-color: #2C7865;")
        self.add_button.clicked.connect(self.save_todo)

        self.all_todos_list_listbox = QListWidget()
        self.all_todos_list_listbox.setStyleSheet("color: #0C2D57;")
        # directly load it wth data to show them on main window
        self.reload_todos_listbox()
        # Connecting the signal to a slot (function) when a to-do a listbox item is changed or clicked on (selected)
        self.all_todos_list_listbox.currentItemChanged.connect(
            self.on_current_item_changed)
        self.all_todos_list_listbox.itemClicked.connect(
            self.on_current_item_changed)

        edit_button = QPushButton("Edit")
        edit_button.setStyleSheet("background-color: #2C7865;")
        edit_button.clicked.connect(self.edit_todo)

        complete_button = QPushButton("Complete")
        complete_button.setStyleSheet("background-color: #2C7865;")
        complete_button.clicked.connect(self.complete_todo)

        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet("background-color: #2C7865;")
        clear_button.clicked.connect(self.clear_input)

        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("background-color: #E72929;")
        exit_button.clicked.connect(self.close)

        # Create a main layout from main sentral widget
        main_layout = QVBoxLayout(main_central_widget)

        # First Layout for time and date labels
        time_date_layout = QHBoxLayout()
        time_date_layout.addWidget(self.time_label)
        # Add stretchable space to push date label to the far right
        time_date_layout.addStretch()
        time_date_layout.addWidget(self.date_label)

        # Second Layout for to-do input and add button
        input_add_clear_layout = QHBoxLayout()
        input_add_clear_layout.addWidget(self.todo_input)
        input_add_clear_layout.addWidget(self.add_button)
        input_add_clear_layout.addWidget(clear_button)
        # Set spacing between buttons and input
        input_add_clear_layout.setSpacing(10)

        # Third Layout for listbox, edit, complete, and exit buttons
        last_layout = QHBoxLayout()
        # create 2 sub vertical layouts to left and right inside thirs layout
        listbox_sublayout_left = QVBoxLayout()
        edit_complete_exit_sublayout_right = QVBoxLayout()
        # add widgets to left sub layout (listbox)
        listbox_sublayout_left.addWidget(self.all_todos_list_listbox)
        # add widgets to right sub layout (edit, complete, and exit buttons)
        edit_complete_exit_sublayout_right.addWidget(edit_button)
        edit_complete_exit_sublayout_right.addWidget(complete_button)
        # Add stretchable space to push exit button to the far bottom
        edit_complete_exit_sublayout_right.addStretch()
        edit_complete_exit_sublayout_right.addWidget(exit_button)
        edit_complete_exit_sublayout_right.setSpacing(
            10)  # Set spacing between buttons
        # add these 2 sub layouts to their parent
        last_layout.addLayout(listbox_sublayout_left)
        # Add spacing between left and right sub-layouts
        last_layout.addSpacing(15)
        last_layout.addLayout(edit_complete_exit_sublayout_right)

        # Add the three layouts to the main layout
        main_layout.addLayout(time_date_layout)
        main_layout.addSpacing(10)  # Add spacing between layouts
        main_layout.addLayout(input_add_clear_layout)
        main_layout.addSpacing(10)  # Add spacing between layouts
        main_layout.addLayout(last_layout)

        # Add padding to main layout (left, top, right, bottom)
        main_layout.setContentsMargins(
            10, 10, 10, 10)

    def update_time(self):
        # Show the time by changing the time label in the app
        current_time = QTime.currentTime()
        display_text = current_time.toString("hh:mm")
        self.time_label.setText(display_text)

    def on_current_item_changed(self, current_item):
        # set the selected to-do property once a to-do is chosen (to be edited or completed)
        if current_item:
            self.todo_selected = current_item.text()

    def clear_input(self):
        # clear input and selected to-do item
        self.todo_input.clear()
        self.todo_selected = None

    def edit_todo(self):
        if self.todo_selected is None:
            # display warning
            self.pop_up_warning(
                "Warning", "Please select a to-do item from the list to edit it.")
        else:
            # populate the input wth the selected to-do to be able to change it
            self.todo_input.setText(" " + self.todo_selected)

    def save_todo(self):
        # If theres no selected to-do means its adding a new to-do
        if self.todo_selected is None:
            new_todo = self.todo_input.text().strip()
            if new_todo == "":
                # if no value entered display a warning
                self.pop_up_warning(
                    "Warning", "The field is blank. There is nothing to add.")
            else:
                # otherwise add it to the list
                self.all_todos_list.append(new_todo)

        # Otherwise this save action is for updating a to-do
        else:
            # get the index of this selected to-do in the list (that is populated in the input)
            index = self.all_todos_list.index(self.todo_selected)
            # get the updated to-do
            updated_todo = self.todo_input.text().strip()
            if updated_todo == "":
                self.pop_up_warning(
                    "Warning", "The field is blank. There is nothing to update.")
            elif updated_todo == self.todo_selected:
                self.pop_up_warning(
                    "Warning", "The value of this todo item remains unchanged. There is nothing to update.")
            else:
                # update it in the list
                self.all_todos_list[index] = updated_todo

        # reload the listbox in all cases (save or edit)
        self.reload_todos_listbox()

    def complete_todo(self):
        if self.todo_selected is None:
            # display warning
            self.pop_up_warning(
                "Warning", "Please select a to-do item from the list to mark it as complete.")
        else:
            # Remove this selected to-do from the list
            self.all_todos_list.remove(self.todo_selected)
            # reload the list of all todos in the listbox so the removed to-do is also removed from listbox
            self.reload_todos_listbox()

    def reload_todos_listbox(self):
        # save the current state of the listbox to the external file (reload comes after an action add, edit or complete)
        # add "\n" for each item to be written correctly in external file
        todos_list_to_save = [item + "\n" for item in self.all_todos_list]
        functions.write_todos(todos_list_to_save)
        # clear and reload the listbox
        self.all_todos_list_listbox.clear()
        self.all_todos_list_listbox.addItems(self.all_todos_list)
        # Reset the selected to-do back to None and clear the input
        self.clear_input()

    def pop_up_warning(self, title, message):
        # Create an instance of CustomMessageBox
        msg_box = CustomMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.addButton(QMessageBox.StandardButton.Ok)
        # Display the custom QMessageBox
        msg_box.exec()


class CustomMessageBox(QMessageBox):
    # create this custom class and inherit everything from QMessageBox class and change the style
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet(
            """
            QMessageBox {
                background-color: #FF9800;
                color: #FEFDED;
                font-size: 15px;
                font-weight: bold;
            }

            QLabel {
                color: #0C2D57; /* Change text color for all labels */
            }

            QPushButton {
                background-color: #2C7865;
                color: #FEFDED;
                font-size: 15px;
                font-weight: bold;
            }
            """
        )


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        run_app()
    except Exception as e:
        # print(f"An error occurred while running the application:\n{e}\n")
        traceback.print_exc()
