from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

from pages.dashboard.ui_dashboard import Ui_Form
from services.wifi_service import WifiService
from services.scan_worker import ScanWorker


class DashboardPage(QWidget):

    scan_data = Signal(list, str)  # Signal to emit scan results to the dashboard
    suspicious_data = Signal(list)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Initialize WifiService
        self.wifi_service = WifiService()

        self.load_interfaces()
        self.ui.btnScan.clicked.connect(self.start_scan)
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageEmpty)

    # Update dashboard with scan results
    def update_dashboard(self, networks):
        # print(networks)
        # Get stats and update UI
        stats = self.wifi_service.analyze_dashboard(networks)
        self.ui.lblCardValue1.setText(str(stats["total"]))
        self.ui.lblCardValue2.setText(str(stats["strong"]))
        self.ui.lblCardValue3.setText(str(stats["weak_total"]))
        self.ui.lblCardValue4.setText(str(len(stats["suspicious"])))
        self.ui.frCard3.setToolTip(
            f"Medium: {stats['medium']}\n"
            f"Weak: {stats['weak']}\n"
            f"Open: {stats['open']}"
        )
        self.suspicious_data.emit(stats["suspicious"])
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
        self.worker = ScanWorker(self.wifi_service, interface)
        # Connect signals to handle results and errors
        self.worker.scan_completed.connect(self.on_scan_completed)
        self.worker.scan_error.connect(self.on_scan_error)
        # Start the worker thread
        self.worker.start()

    def on_scan_completed(self, networks, interface):
        self.update_dashboard(networks)
        self.ui.lblStatusText.setText("Scan completed")
        self.ui.btnScan.setEnabled(True)
        self.ui.btnScan.setText("Scan")
        
        self.scan_data.emit(networks, interface)  # Emit the scan results to the dashboard

    def on_scan_error(self, error_message):
        self.ui.lblStatusText.setText(f"Error: {error_message}")
        self.ui.btnScan.setEnabled(True)
        self.ui.btnScan.setText("Scan")

    # Load wifi interfaces into the combo box
    def load_interfaces(self):
        interfaces = self.wifi_service.get_interfaces()
        self.ui.cbInterfaces.clear()
        self.ui.cbInterfaces.addItems(["Select Interface"] + interfaces)
