from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from database.database import authentication


class LoginPage(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setContentsMargins(150,50,150,50)

        project_title = QLabel("Student Management System")
        project_title.setStyleSheet("""font-family: Times New Roman;font-size: 35px;font-weight:bold;""")
        project_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(project_title)
        layout.setSpacing(10)


        layout.addSpacing(50)
        title = QLabel("Login")
        title.setFixedHeight(100)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px;font-weight;bold")
        layout.addWidget(title)
        layout.addSpacing(20)


        username_layout = QVBoxLayout()
        username_layout.setContentsMargins(0,0,0,0)
        username_layout.setSpacing(0)

        username = QLabel("Username")
        username.setFixedHeight(20)
        username_layout.addWidget(username)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        username_layout.addWidget(self.username_input)

        layout.addLayout(username_layout)
        layout.addSpacing(10)

        password_layout = QVBoxLayout()
        password_layout.setContentsMargins(0,0,0,0)
        password_layout.setSpacing(0)

        password = QLabel("Password")
        password.setFixedHeight(20)
        password_layout.addWidget(password)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        layout.addSpacing(15)


        login_button = QPushButton("Login")
        login_button.clicked.connect(
            self.login
        )
        layout.addWidget(login_button)

        register_button = QPushButton("Create Account")
        register_button.clicked.connect(
            self.main_window.show_register
        )

        layout.addWidget(register_button)
        layout.addSpacing(150)

        self.setLayout(layout)


    def login(self):

        username = self.username_input.text().strip()
        password = self.password_input.text()

        if username == "":

            QMessageBox.warning(
                self,
                "Error",
                "Please enter username."
            )

            return

        if password == "":

            QMessageBox.warning(
                self,
                "Error",
                "Please enter password."
            )

            return

        user = authentication(
            username,
            password
        )

        if user:

            self.username_input.clear()
            self.password_input.clear()

            self.main_window.show_dashboard()

        else:

            QMessageBox.warning(
                self,
                "Login Failed",
                "Invalid username or password."
            )