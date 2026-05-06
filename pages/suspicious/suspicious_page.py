from PySide6.QtWidgets import QWidget

from pages.suspicious.ui_suspicious import Ui_Form


class SuspiciousPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def update_suspicious_networks(self, suspicious_data):
        print(suspicious_data)