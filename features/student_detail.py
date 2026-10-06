from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)


class StudentDetailPage(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout()

        title = QLabel("Student Details")
        layout.addWidget(title)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""font-family: Times new Roman;font-size:30px;font-weight:bold""")

        layout.addSpacing(10)

        self.info = QLabel()
        layout.addWidget(self.info)

        self.subjects = QLabel()
        layout.addWidget(self.subjects)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(
            self.goback
        )

        layout.addWidget(self.back_button)

        self.setLayout(layout)


    def load_student(self, student):

        if student is None:
            return

        self.info.setText(
            "ID: ".ljust(20) + str(student[0]) + "\n\n"
            "Full Name: ".ljust(20) + student[1] + "\n\n"
            "Age: ".ljust(20) + str(student[2]) + "\n\n"
            "Address: ".ljust(20) + student[3] + "\n\n"
            "Contact: ".ljust(20) + student[4] + "\n\n"
            "Email: ".ljust(20) + student[5] + "\n\n"
            "Course: ".ljust(20) + student[6] + "\n\n"
            "Year Level: ".ljust(20) + student[7]
        )
        self.info.setStyleSheet("font-size: 15px;font-weight: normal;")

        subject_text = "Subjects:\n"


        if student[8]:

            import json

            subjects = json.loads(student[8])

            for subject in subjects:

                subject_text += "• " + subject + "\n"

        else:

            subject_text += "No subjects"

        self.subjects.setText(subject_text)
        self.subjects.setStyleSheet("font-size: 15px;font-weight: normal;")


    def go_back(self):

        self.main_window.show_dashboard()

    def goback(self):
        self.main_window.show_view_student()