from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
    QListWidget,
    QListWidgetItem
)

from subjects.subjects import get_subjects, get_subject_map
from database.database import get_student, update_student


class UpdateStudentPage(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window
        self.student_id = None

        layout = QVBoxLayout()

        title = QLabel("Update Student")
        layout.addWidget(title)

        self.fullname = QLineEdit()
        self.fullname.setPlaceholderText("Full Name")
        layout.addWidget(self.fullname)

        self.address = QLineEdit()
        self.address.setPlaceholderText("Address")
        layout.addWidget(self.address)

        self.age = QLineEdit()
        self.age.setPlaceholderText("Age")
        layout.addWidget(self.age)

        self.contact = QLineEdit()
        self.contact.setPlaceholderText("Contact")
        layout.addWidget(self.contact)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        layout.addWidget(self.email)

        self.course = QComboBox()
        self.course.addItems([
            "BSCS",
            "BSIT",
            "BSCpE"
        ])
        layout.addWidget(self.course)

        self.yearlvl = QComboBox()
        self.yearlvl.addItems([
            "1st",
            "2nd",
            "3rd",
            "4th",
            "5th"
        ])
        layout.addWidget(self.yearlvl)

        layout.addWidget(QLabel("Available Subjects"))

        self.subject_list = QListWidget()
        layout.addWidget(self.subject_list)

        layout.addWidget(QLabel("Selected Subjects"))

        self.selected_subjects = QListWidget()
        layout.addWidget(self.selected_subjects)

        buttons = QHBoxLayout()

        self.add_button = QPushButton("Add Subject")
        self.add_button.clicked.connect(self.add_subject)
        buttons.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Subject")
        self.remove_button.clicked.connect(self.remove_subject)
        buttons.addWidget(self.remove_button)

        layout.addLayout(buttons)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_student)
        layout.addWidget(self.save_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.main_window.show_view_student)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.load_subjects()


    def load_subjects(self):

        self.subject_list.clear()

        subjects = get_subjects()

        for subject in subjects:

            item = QListWidgetItem(
                str(subject[1])
                + ". "
                + subject[2]
                + " - "
                + subject[3]
                + ", Room "
                + subject[4]
            )

            item.setData(Qt.ItemDataRole.UserRole, subject[2])

            self.subject_list.addItem(item)


    def load_student(self, student_id):

        student = get_student(student_id)

        if student is None:
            return

        self.student_id = student[0]

        self.fullname.setText(student[1])
        self.age.setText(str(student[2]))
        self.address.setText(student[3])
        self.contact.setText(student[4])
        self.email.setText(student[5])

        self.course.setCurrentText(student[6])
        self.yearlvl.setCurrentText(student[7])

        self.selected_subjects.clear()

        if student[8]:

            import json

            subjects = json.loads(student[8])
            subject_map = get_subject_map()

            for subject in subjects:

                info = subject_map.get(subject)

                if info is None:
                    text = subject
                else:
                    text = (
                        str(info[1])
                        + ". "
                        + info[2]
                        + " - "
                        + info[3]
                        + ", Room "
                        + info[4]
                    )

                item = QListWidgetItem(text)
                item.setData(Qt.ItemDataRole.UserRole, subject)

                self.selected_subjects.addItem(item)


    def add_subject(self):

        if self.selected_subjects.count() >= 10:

            QMessageBox.warning(
                self,
                "Limit",
                "You can only select 10 subjects."
            )

            return

        item = self.subject_list.currentItem()

        if item is None:
            return

        subject = item.data(Qt.ItemDataRole.UserRole)

        for i in range(self.selected_subjects.count()):

            if self.selected_subjects.item(i).data(Qt.ItemDataRole.UserRole) == subject:

                QMessageBox.warning(
                    self,
                    "Subject",
                    "Subject is already selected."
                )

                return

        selected_item = QListWidgetItem(item.text())
        selected_item.setData(Qt.ItemDataRole.UserRole, subject)

        self.selected_subjects.addItem(selected_item)


    def remove_subject(self):

        row = self.selected_subjects.currentRow()

        if row >= 0:
            self.selected_subjects.takeItem(row)


    def save_student(self):

        fullname = self.fullname.text().strip()
        address = self.address.text().strip()
        age = self.age.text().strip()
        contact = self.contact.text().strip()
        email = self.email.text().strip()

        if fullname == "":
            QMessageBox.warning(
                self,
                "Error",
                "Please enter full name."
            )
            return

        if address == "":
            QMessageBox.warning(
                self,
                "Error",
                "Please enter address."
            )
            return

        if age == "":
            QMessageBox.warning(
                self,
                "Error",
                "Please enter age."
            )
            return

        try:
            age = int(age)

        except ValueError:

            QMessageBox.warning(
                self,
                "Error",
                "Age must be a number."
            )

            return

        if contact == "":
            QMessageBox.warning(
                self,
                "Error",
                "Please enter contact."
            )
            return

        if email == "":
            QMessageBox.warning(
                self,
                "Error",
                "Please enter email."
            )
            return

        if self.selected_subjects.count() == 0:

            QMessageBox.warning(
                self,
                "Error",
                "Please select at least one subject."
            )

            return

        subjects = []

        for i in range(self.selected_subjects.count()):

            subjects.append(
                self.selected_subjects.item(i).data(Qt.ItemDataRole.UserRole)
            )

        update_student(
            self.student_id,
            fullname,
            age,
            address,
            contact,
            email,
            self.course.currentText(),
            self.yearlvl.currentText(),
            subjects
        )

        QMessageBox.information(
            self,
            "Success",
            "Student updated successfully."
        )

        self.main_window.show_dashboard()