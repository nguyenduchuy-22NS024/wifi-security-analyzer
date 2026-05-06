from PySide6.QtWidgets import QWidget

from pages.analyze.ui_analyze import Ui_Form
from services.analyze_service import AnalyzeService
from services.analyze_worker import AnalyzeWorker


class AnalyzePage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.stackedWidget.setCurrentWidget(self.ui.pageEmpty)

    def update_analyze_result(self, analyze_result):
        print(analyze_result)

    def analyze_network(self, bssid, interface):
        print("Analyzing network with BSSID:", bssid, interface)
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageEmpty)
        self.ui.lblStatusText.setText(f"Analyzing BSSID {bssid}...")

        service = AnalyzeService(bssid, interface)
        self.worker = AnalyzeWorker(service)
        self.worker.analyze_completed.connect(self.on_analyze_completed)
        self.worker.analyze_error.connect(self.on_analyze_error)
        self.worker.start()

    def on_analyze_completed(self, analyze_result):
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageData)
        self.update_analyze_result(analyze_result)

    def on_analyze_error(self, error_message):
        self.ui.lblStatusText.setText(f"Error: {error_message}")
