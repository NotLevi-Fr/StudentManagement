from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QMessageBox
)

from database.database import get_all_students, get_student as db_get_student


class ViewStudentPage(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout()

        title = QLabel("Students")
        layout.addWidget(title)


        self.student_list = QListWidget()
        layout.addWidget(self.student_list)

        buttons = QHBoxLayout()

        self.view_button = QPushButton("View")
        self.view_button.clicked.connect(self.view_student)
        buttons.addWidget(self.view_button)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_student)
        buttons.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_student)
        buttons.addWidget(self.delete_button)

        layout.addLayout(buttons)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.main_window.show_dashboard)
        layout.addWidget(self.back_button)

        self.setLayout(layout)


    def load_students(self):

        self.student_list.clear()



        students = get_all_students()

        for student in students:

            text = (
                str(student[0])
                + " | "
                + student[1]
                + " | "
                + student[6]
                + " | "
                + student[7]
            )

            self.student_list.addItem(text)


    def get_selected_student_id(self):

        item = self.student_list.currentItem()

        if item is None:
            return None

        text = item.text()

        student_id = text.split(" | ")[0]

        return int(student_id)


    def view_student(self):

        student_id = self.get_selected_student_id()

        if student_id is None:

            QMessageBox.warning(
                self,
                "Error",
                "Please select a student."
            )

            return

        student = db_get_student(student_id)

        if student is None:
            QMessageBox.warning(self,"Error","Student not found.")
            return

        self.main_window.student_detail_page.load_student(student)

        self.main_window.show_student_detail()


    def update_student(self):

        student_id = self.get_selected_student_id()

        if student_id is None:

            QMessageBox.warning(
                self,
                "Error",
                "Please select a student."
            )

            return

        self.main_window.update_student_page.load_student(
            student_id
        )

        self.main_window.show_update_student()


    def delete_student(self):

        student_id = self.get_selected_student_id()

        if student_id is None:

            QMessageBox.warning(
                self,
                "Error",
                "Please select a student."
            )

            return

        answer = QMessageBox.question(
            self,
            "Delete Student",
            "Are you sure you want to delete this student?"
        )

        if answer == QMessageBox.StandardButton.Yes:

            from database.database import delete_student

            delete_student(student_id)

            self.load_students()

            QMessageBox.information(
                self,
                "Success",
                "Student deleted successfully."
            )