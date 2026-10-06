from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from database.database import get_all_enrollments


class EnrollmentRecordsPage(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(10)

        title = QLabel("Enrollment Records")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""font-family: Times New Roman;font-size: 35px;font-weight: bold;""")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Student",
            "Course",
            "Year",
            "Code",
            "Subject",
            "Time",
            "Room",
            "Date Enrolled"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.back_button = QPushButton("Back")
        self.back_button.setObjectName("back")
        self.back_button.clicked.connect(self.main_window.show_dashboard)
        layout.addWidget(self.back_button)

        self.setLayout(layout)


    def load_records(self):

        records = get_all_enrollments()

        self.table.setRowCount(len(records))

        for row_index, record in enumerate(records):

            for column_index, value in enumerate(record):

                self.table.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem(str(value))
                )
