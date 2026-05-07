import json

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

from pages.dashboard.ui_dashboard import Ui_Form
from services.scan_worker import ScanWorker
from services.scan_networks import get_network_interfaces
from services.analyze_networks import analyze_dashboard_stats


class DashboardPage(QWidget):

    networks_data = Signal(list)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.networks = []

        self.load_interfaces()

        self.ui.btnScan.clicked.connect(self.start_scan)
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageEmpty)

    # Update dashboard with scan results
    def update_dashboard(self, networks):
        # print(networks)
        # Get stats and update UI
        stats = analyze_dashboard_stats(networks)
        # print(stats)
        self.ui.lblCardValue1.setText(str(stats["total_aps"]))
        self.ui.lblCardValue2.setText(str(stats["strong_security"]))
        self.ui.lblCardValue3.setText(str(stats["weak_security"]))
        self.ui.lblCardValue4.setText(str(stats["suspicious_aps"]))

        self.ui.frCard2.setToolTip(
            f"Very Low Risk: {stats['risk_dist']["Very Low Risk"]}\n"
            f"Low Risk: {stats['risk_dist']["Low Risk"]}\n"
            f"Medium Risk: {stats['risk_dist']["Medium Risk"]}"
        )
        self.ui.frCard3.setToolTip(
            f"High Risk: {stats['risk_dist']["High Risk"]}\n"
            f"Critical: {stats['risk_dist']["Critical"]}"
        )

        self.ui.frCard4.setToolTip("Click to view details")

        self.ui.stackedWidget.setCurrentWidget(self.ui.pageData)

    # Start scanning
    def start_scan(self):
        interface = self.ui.cbInterfaces.currentText()
        if not interface or interface == "Select Interface":
            print("Please select a valid interface")
            return

        # Update UI to show scanning status
        self.ui.lblStatusText.setText(f"Scanning on {interface}...")
        self.ui.btnScan.setEnabled(False)
        self.ui.btnScan.setText("Scanning...")

        # Create and start the worker thread for scanning
        self.worker = ScanWorker(interface)
        # Connect signals to handle results and errors
        self.worker.scan_completed.connect(self.on_scan_completed)
        self.worker.scan_error.connect(self.on_scan_error)
        # Start the worker thread
        self.worker.start()

    def on_scan_completed(self, networks):
        self.networks = networks
        self.update_dashboard(self.networks)
        self.ui.lblStatusText.setText("Scan completed")
        self.ui.btnScan.setEnabled(True)
        self.ui.btnScan.setText("Scan")
        self.networks_data.emit(networks)

    def on_scan_error(self, error_message):
        self.ui.lblStatusText.setText(f"Error: {error_message}")
        self.ui.btnScan.setEnabled(True)
        self.ui.btnScan.setText("Scan")

    # Load wifi interfaces into the combo box
    def load_interfaces(self):
        interfaces = get_network_interfaces()
        self.ui.cbInterfaces.clear()
        self.ui.cbInterfaces.addItems(["Select Interface"] + interfaces)
