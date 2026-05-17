import sys, json
from PySide6.QtWidgets import QApplication, QMainWindow
from ui_mainwindow import Ui_MainWindow

from pages.dashboard.dashboard_page import DashboardPage
from pages.scan.scan_page import ScanPage
from pages.analyze.analyze_page import AnalyzePage
from pages.trusted.trusted_page import TrustedPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize pages
        self.dashboard_page = DashboardPage()
        self.scan_page = ScanPage()
        self.analyze_page = AnalyzePage()
        self.trusted_page = TrustedPage()

        # Add pages to stacked widget
        self.ui.stackedWidget.addWidget(self.dashboard_page)
        self.ui.stackedWidget.addWidget(self.scan_page)
        self.ui.stackedWidget.addWidget(self.analyze_page)
        self.ui.stackedWidget.addWidget(self.trusted_page)

        # Connect navigation buttons
        self.ui.btnDashboard.clicked.connect(self.navigate_page)
        self.ui.btnScan.clicked.connect(self.navigate_page)
        self.ui.btnAnalyze.clicked.connect(self.navigate_page)

        # Start on dashboard page
        self.ui.stackedWidget.setCurrentWidget(self.dashboard_page)

        # Connect signals between pages
        self.dashboard_page.networks_data.connect(self.scan_page.update_scan_results)
        self.scan_page.analyze_bssid.connect(self.analyze_page.update_analyze_results)

        self.navigate_page()

    # Navigation logic for sidebar buttons
    def navigate_page(self):
        sender = self.sender()

        if sender == self.ui.btnDashboard:
            self.ui.stackedWidget.setCurrentWidget(self.dashboard_page)

        elif sender == self.ui.btnScan:
            self.ui.stackedWidget.setCurrentWidget(self.scan_page)

        elif sender == self.ui.btnAnalyze:
            self.ui.stackedWidget.setCurrentWidget(self.analyze_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
