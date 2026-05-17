import json
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter
from PySide6.QtCharts import QChart, QChartView, QPieSeries

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

        for frame in [self.ui.frCipher, self.ui.frMfp, self.ui.frWps, self.ui.frAuth]:
            if not frame.layout():
                QVBoxLayout(frame)

        self.load_interfaces()
        self.ui.btnScan.clicked.connect(self.start_scan)
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageEmpty)

    def update_dashboard(self, networks):
        stats = analyze_dashboard_stats(networks)

        # 1. Cập nhật các thẻ số liệu (Cards)
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

        # 2. Vẽ 4 biểu đồ bảo mật
        self.render_charts(stats)

        self.ui.stackedWidget.setCurrentWidget(self.ui.pageData)

    def render_charts(self, stats):
        # Biểu đồ 1: Cipher Distribution
        self.setup_chart(self.ui.frCipher, stats["cipher_dist"], "Cipher Distribution")

        # Biểu đồ 2: Security Detailed
        self.setup_chart(self.ui.frMfp, stats["mfp_dist"], "Security Protocols")

        # Biểu đồ 3: WPS Status
        self.setup_chart(self.ui.frWps, stats["wps_dist"], "WPS Vulnerability")

        # Biểu đồ 4: Authentication
        self.setup_chart(self.ui.frAuth, stats["auth_dist"], "Authentication Types")

    def setup_chart(self, frame, data_dict, title):
        """Xóa biểu đồ cũ và thêm biểu đồ mới vào Frame"""
        # Xóa widget cũ trong layout
        layout = frame.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Tạo series dữ liệu
        series = QPieSeries()
        for label, value in data_dict.items():
            if value > 0:  # Chỉ hiển thị các mục có dữ liệu
                series.append(f"{label}: {value}", value)

        # Tạo Chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setAlignment(Qt.AlignRight)
        chart.setBackgroundVisible(False)

        # Tạo ChartView
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(chart_view)

    # --- Các hàm start_scan, on_scan_completed giữ nguyên như cũ ---
    def start_scan(self):
        interface = self.ui.cbInterfaces.currentText()
        if not interface or interface == "Select Interface":
            return
        self.ui.lblStatusText.setText(f"Scanning on {interface}...")
        self.ui.btnScan.setEnabled(False)
        self.ui.btnScan.setText("Scanning...")
        self.worker = ScanWorker(interface)
        self.worker.scan_completed.connect(self.on_scan_completed)
        self.worker.scan_error.connect(self.on_scan_error)
        self.worker.start()

    def on_scan_completed(self, networks):
        self.networks = networks
        self.update_dashboard(self.networks)
        self.ui.lblStatusText.setText("Scan completed")
        self.ui.btnScan.setEnabled(True)
        self.ui.btnScan.setText("Scan")
        self.networks_data.emit(self.networks)
        # print(json.dumps(self.networks))

    def on_scan_error(self, error_message):
        self.ui.lblStatusText.setText(f"Error: {error_message}")
        self.ui.btnScan.setEnabled(True)
        self.ui.btnScan.setText("Scan")

    def load_interfaces(self):
        interfaces = get_network_interfaces()
        self.ui.cbInterfaces.clear()
        self.ui.cbInterfaces.addItems(["Select Interface"] + interfaces)
