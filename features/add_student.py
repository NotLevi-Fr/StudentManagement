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

from subjects.subjects import get_subjects


class AddStudentPage(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        self.main_window.show_dashboard()

        layout = QVBoxLayout()
        layout.setContentsMargins(100, 50,100, 50)

        title = QLabel("Add Student")
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

        subject_label = QLabel("Available Subjects")
        layout.addWidget(subject_label)

        self.subject_list = QListWidget()
        layout.addWidget(self.subject_list)

        self.selected_label = QLabel("Selected Subjects: 0/10")
        layout.addWidget(self.selected_label)

        self.selected_subjects = QListWidget()
        layout.addWidget(self.selected_subjects)

        buttons = QHBoxLayout()

        self.add_subject_button = QPushButton("Add Subject")
        self.add_subject_button.clicked.connect(self.add_subject)
        buttons.addWidget(self.add_subject_button)

        self.remove_subject_button = QPushButton("Remove Subject")
        self.remove_subject_button.clicked.connect(self.remove_subject)
        buttons.addWidget(self.remove_subject_button)

        layout.addLayout(buttons)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        layout.addWidget(self.next_button)

        self.backbtn = QPushButton("Back")
        self.backbtn.clicked.connect(self.main_window.show_dashboard)
        layout.addWidget(self.backbtn)

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

        self.selected_label.setText(
            "Selected Subjects: "
            + str(self.selected_subjects.count())
            + "/10"
        )


    def remove_subject(self):

        row = self.selected_subjects.currentRow()

        if row >= 0:

            self.selected_subjects.takeItem(row)

            self.selected_label.setText(
                "Selected Subjects: "
                + str(self.selected_subjects.count())
                + "/10"
            )


    def next_page(self):

        fullname = self.fullname.text().strip()
        address = self.address.text().strip()
        age = self.age.text().strip()
        contact = self.contact.text().strip()
        email = self.email.text().strip()

        if fullname == "":
            QMessageBox.warning(self, "Error", "Please enter full name.")
            return

        if address == "":
            QMessageBox.warning(self, "Error", "Please enter address.")
            return

        if age == "":
            QMessageBox.warning(self, "Error", "Please enter age.")
            return

        if contact == "":
            QMessageBox.warning(self, "Error", "Please enter contact.")
            return

        if email == "":
            QMessageBox.warning(self, "Error", "Please enter email.")
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

        data = {
            "fullname": fullname,
            "age": age,
            "address": address,
            "contact": contact,
            "email": email,
            "course": self.course.currentText(),
            "year_level": self.yearlvl.currentText(),
            "subjects": subjects
        }

        self.main_window.pending_student = data

        self.main_window.verify_page.load_data(data)

        self.main_window.show_verify()