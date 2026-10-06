from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)


class DashboardPage(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setContentsMargins(100,50,100,50)
        layout.setSpacing(5)
        subtitle = QLabel("Welcome to!")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size:20px")
        layout.addWidget(subtitle)

        layout.addSpacing(10)

        title = QLabel("Student Management System")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""font-family: Times New Roman;font-size: 35px;font-weight: bold;""")
        layout.addWidget(title)

        layout.addSpacing(200)

        add_button = QPushButton("Add Student")
        add_button.clicked.connect(
            self.main_window.show_add_student
        )
        layout.addWidget(add_button)

        view_button = QPushButton("View Students")
        view_button.clicked.connect(
            self.view_students
        )
        layout.addWidget(view_button)

        records_button = QPushButton("Enrollment Records")
        records_button.clicked.connect(
            self.enrollment_records
        )
        layout.addWidget(records_button)

        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(
            self.main_window.show_login
        )
        layout.addWidget(logout_button)
        layout.addSpacing(200)

        self.setLayout(layout)


    def view_students(self):

        self.main_window.view_student_page.load_students()

        self.main_window.show_view_student()


    def enrollment_records(self):

        self.main_window.enrollment_records_page.load_records()

        self.main_window.show_enrollment_records()