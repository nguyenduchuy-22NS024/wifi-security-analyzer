import json
from PySide6.QtWidgets import QWidget

from pages.suspicious.ui_suspicious import Ui_Form
from services.scan_networks import detect_suspicious_networks


class SuspiciousPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.networks = []

    def update_suspicious_results(self, networks):
        self.networks = networks
        suspicious_networks = detect_suspicious_networks(self.networks)
        print(suspicious_networks)
        
        self.ui.label_2.setText(json.dumps(suspicious_networks, indent=4))