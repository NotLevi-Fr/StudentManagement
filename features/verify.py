from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QListWidgetItem
)

from database.database import add_student


class VerifyPage(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window
        self.data = {}

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(50,30,50,30)
        self.layout.setSpacing(10)


        title = QLabel("Verify Student Information")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""font-family: Times New Roman;font-size: 35px;font-weight: bold;""")
        self.layout.addWidget(title)


        self.info = QLabel()
        self.layout.addWidget(self.info)

        # self.subjects_layout = QVBoxLayout()
        # self.subjects_layout.setSpacing(2)
        # self.layout.addLayout(self.subjects_layout)

        self.subjects = QLabel()
        self.subjects.setStyleSheet("""font-family: Times New Roman; font-size: 20px; font-weight: normal;""")
        self.layout.addWidget(self.subjects)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_student)
        self.layout.addWidget(self.submit_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)


    def load_data(self, data):

        self.data = data

        text = (
            "Full Name: \t" + data["fullname"] + "\n\n"
            "Age: \t" + str(data["age"]) + "\n\n"
            "Address: \t" + data["address"] + "\n\n"
            "Contact: \t" + data["contact"] + "\n\n"
            "Email: \t" + data["email"] + "\n\n"
            "Course: \t" + data["course"] + "\n\n"
            "Year Level: \t" + data["year_level"]
        )
        self.info.setStyleSheet("""font-family: Times New Roman;font-size: 20px;font-weight: normal;""")

        self.info.setText(text)

        subject_text = "Selected Subjects:\n"
        for subject in data["subjects"]:
            subject_text += subject + "\n"

        self.subjects.setText(subject_text)




    def submit_student(self):

        if len(self.data["subjects"]) == 0:

            QMessageBox.warning(
                self,
                "Error",
                "Please select at least one subject."
            )

            return

        add_student(
            self.data["fullname"],
            self.data["age"],
            self.data["address"],
            self.data["contact"],
            self.data["email"],
            self.data["course"],
            self.data["year_level"],
            self.data["subjects"]
        )

        QMessageBox.information(
            self,
            "Success",
            "Student added successfully."
        )

        self.main_window.pending_student = None

        self.main_window.show_dashboard()


    def go_back(self):

        self.main_window.add_student_page.selected_subjects.clear()

        for subject in self.data["subjects"]:

            item = QListWidgetItem(subject)
            item.setData(Qt.ItemDataRole.UserRole, subject)

            self.main_window.add_student_page.selected_subjects.addItem(
                item
            )

        self.main_window.add_student_page.selected_label.setText(
            "Selected Subjects: "
            + str(len(self.data["subjects"]))
            + "/10"
        )

        self.main_window.show_add_student()