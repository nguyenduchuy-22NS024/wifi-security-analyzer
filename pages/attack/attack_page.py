import os, subprocess, datetime

from PySide6.QtWidgets import QWidget, QFileDialog, QTextEdit, QVBoxLayout, QMessageBox
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QHeaderView, QMenu, QTableWidgetItem, QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor, Qt, QIcon

from pages.attack.ui_attack import Ui_Form
from services.scan_networks import get_network_interfaces
from services.attack_network import toggle_monitor_mode
from services.deauth_worker import DeauthWorker
from services.capture_worker import CaptureWorker
from services.crack_worker import CrackWorker
from services.analyze_networks import analyze_scan_table


class AttackPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Target data from Scan page
        self.target_ssid = ""
        self.target_bssid = ""
        self.target_chan = ""
        self.captured_cap_path = ""
        self.networks = []

        # Workers management
        self.cap_worker = None
        self.deauth_worker = None
        self.crack_worker = None

        # Initialize Log area (Console)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff; 
                color: #0a0a46; 
                font-family: 'Courier New', monospace;
                font-size: 16px;
                border: 1px solid #333;
            }
        """)

        # Add log_output to frLog frame in UI
        if self.ui.frLog.layout() is None:
            log_layout = QVBoxLayout(self.ui.frLog)
            log_layout.setContentsMargins(5, 5, 5, 5)
            log_layout.addWidget(self.log_output)
        else:
            self.ui.frLog.layout().addWidget(self.log_output)

        # Initial state: Show empty page when no Wi-Fi data is available
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageEmpty)

        self.setup_connections()
        self.load_interfaces()
        self.setup_table()
        
    def back_action(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageScan)
        print("Back")

    def setup_table(self):
        header = self.ui.tableScanData.horizontalHeader()

        # Các cột nhỏ thì vừa khít nội dung
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # In-use
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # SSID
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # BSSID
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Signal
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Bars
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Channel
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Band

        header.setSectionResizeMode(7, QHeaderView.Stretch)  # Security

        # Tắt thanh cuộn ngang
        # self.ui.tableScanData.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.tableScanData.itemDoubleClicked.connect(self.on_row_double_clicked)

    def update_scan_results(self, networks):
        self.networks = networks
        table_data = analyze_scan_table(networks)
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageScan)
        self.ui.tableScanData.setRowCount(0)

        for network in table_data:
            row_position = self.ui.tableScanData.rowCount()
            self.ui.tableScanData.insertRow(row_position)

            # --- Cột 0: IN-USE ---
            in_use_text = "●" if network["in_use"] else ""
            item_in_use = QTableWidgetItem(in_use_text)
            item_in_use.setTextAlignment(Qt.AlignCenter)
            self.ui.tableScanData.setItem(row_position, 0, item_in_use)

            # --- Cột 1, 2, 3 ---
            self.ui.tableScanData.setItem(
                row_position, 1, QTableWidgetItem(network["ssid"])
            )
            self.ui.tableScanData.setItem(
                row_position, 2, QTableWidgetItem(network["bssid"])
            )
            self.ui.tableScanData.setItem(
                row_position, 3, QTableWidgetItem(network["signal"])
            )

            # --- Cột 4: BARS ---
            item_bars = QTableWidgetItem()
            level = network["bar_level"]
            icon_path = f":/root/resources/icons8-wifi-{level}-24.png"
            item_bars.setIcon(QIcon(icon_path))
            item_bars.setTextAlignment(Qt.AlignCenter)
            self.ui.tableScanData.setItem(row_position, 4, item_bars)

            # --- Cột 5, 6 ---
            self.ui.tableScanData.setItem(
                row_position, 5, QTableWidgetItem(str(network["channel"]))
            )
            self.ui.tableScanData.setItem(
                row_position, 6, QTableWidgetItem(network["band"])
            )

            # --- Cột 7: SECURITY ---
            sec_text = network["security"]
            self.ui.tableScanData.setItem(row_position, 7, QTableWidgetItem(sec_text))

            # --- MÀU SẮC DỰA TRÊN RISK ---
            if "Very Low Risk" in sec_text:
                color = "#d1ffd1"
            elif "Low Risk" in sec_text:
                color = "#e5ffcc"
            elif "Medium Risk" in sec_text:
                color = "#fff5cc"
            elif any(x in sec_text for x in ["High Risk", "Critical", "Unknown"]):
                color = "#ffcccc"
            else:
                color = "#ffffff"

            # Áp dụng màu nền
            for col in range(self.ui.tableScanData.columnCount()):
                item = self.ui.tableScanData.item(row_position, col)
                if item:
                    item.setBackground(QColor(color))

    def on_row_double_clicked(self, item):
        """Xử lý khi người dùng nhấn đúp vào bất kỳ ô nào trong dòng"""
        row = item.row()
        bssid_item = self.ui.tableScanData.item(row, 2)

        if bssid_item:
            # bssid = bssid_item.text()
            self.target_ssid = self.ui.tableScanData.item(row, 1).text()
            self.target_bssid = self.ui.tableScanData.item(row, 2).text()
            self.target_chan = self.ui.tableScanData.item(row, 5).text()
            # print(self.target_ssid, self.target_bssid, self.target_chan)
            
            self.ui.stackedWidget.setCurrentWidget(self.ui.pageData)
            self.get_items(self.target_ssid, self.target_bssid, self.target_chan)
            
            
            # self.analyze_bssid.emit(bssid, self.networks)

    def setup_connections(self):
        """Connect button events"""
        self.ui.btnMonitorMode.clicked.connect(self.toggle_monitor_mode)
        self.ui.btnBrowse.clicked.connect(self.browse_wordlist)

        # Main function buttons with Toggle logic
        self.ui.btnCapture.clicked.connect(self.toggle_capture)
        self.ui.btnDeauth.clicked.connect(self.toggle_deauth)
        self.ui.btnAttack.clicked.connect(self.toggle_crack)
        self.ui.btnBack.clicked.connect(self.back_action)

    # --- HELPERS ---
    def write_log(self, message):
        """Write information to the log interface"""
        time = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{time}]> {message}")
        # Auto-scroll to the bottom
        self.log_output.verticalScrollBar().setValue(
            self.log_output.verticalScrollBar().maximum()
        )

    def get_interface(self):
        """Get selected interface from ComboBox"""
        iface = self.ui.cbInterfaces.currentText()
        if iface == "Select Interface" or not iface:
            QMessageBox.warning(
                self, "Warning", "Please select a network interface (Wi-Fi Card)!"
            )
            return None
        return iface

    def is_monitor_mode(self, iface):
        """Check if the interface is in monitor mode"""
        try:
            # Quick check via name or using iw
            res = subprocess.run(["iw", iface, "info"], capture_output=True, text=True)
            return "type monitor" in res.stdout or "mon" in iface
        except:
            return "mon" in iface

    # --- VALIDATION ---
    def validate_for_wifi_actions(self):
        """Check if the network card is ready for Capture/Deauth"""
        iface = self.get_interface()
        if not iface:
            return None

        if not self.is_monitor_mode(iface):
            QMessageBox.critical(
                self,
                "Monitor Mode Required",
                f"Interface '{iface}' is not in Monitor Mode!\n"
                "You need to click 'Change Mode' to use this feature.",
            )
            return None
        return iface

    # --- CAPTURE CONTROL LOGIC ---
    @Slot()
    def toggle_capture(self):
        # If running -> Stop
        if self.cap_worker and self.cap_worker.isRunning():
            self.cap_worker.stop()
            self.write_log("Requesting to stop Capture...")
            return

        # If not running -> Validate and Start
        iface = self.validate_for_wifi_actions()
        if iface:
            self.write_log(f"Starting Handshake Capture [SSID: {self.target_ssid}]")
            self.ui.btnCapture.setText("STOP CAPTURE")
            self.ui.btnCapture.setStyleSheet(
                "background-color: #f44336; color: white; font-weight: bold;"
            )

            self.cap_worker = CaptureWorker(iface, self.target_bssid, self.target_chan)
            self.cap_worker.status_msg.connect(self.write_log)
            self.cap_worker.handshake_found.connect(self.on_handshake_captured)
            self.cap_worker.finished.connect(self.reset_capture_ui)
            self.cap_worker.start()
            self.ui.btnDeauth.setEnabled(True)

    def reset_capture_ui(self):
        self.ui.btnCapture.setText("Start Capture")
        self.ui.btnCapture.setStyleSheet("")
        self.write_log("Capture process has finished.")

    def on_handshake_captured(self, path):
        self.captured_cap_path = path
        self.ui.lblCaptureStatus.setText("Status: HANDSHAKE CAPTURED!")
        self.ui.lblCaptureStatus.setStyleSheet("color: #4caf50; font-weight: bold;")
        self.ui.btnAttack.setEnabled(True)
        QMessageBox.information(
            self,
            "Success",
            "Handshake captured.",
        )

    # --- DEAUTH CONTROL LOGIC ---
    @Slot()
    def toggle_deauth(self):
        if self.deauth_worker and self.deauth_worker.isRunning():
            self.deauth_worker.stop()
            self.ui.btnDeauth.setText("Start Deauth")
            self.ui.btnDeauth.setStyleSheet("")
            return

        iface = self.validate_for_wifi_actions()
        if iface:
            self.write_log("Starting continuous Deauth packet transmission...")
            self.ui.btnDeauth.setText("STOP DEAUTH")
            self.ui.btnDeauth.setStyleSheet(
                "background-color: #f44336; color: white; font-weight: bold;"
            )

            self.deauth_worker = DeauthWorker(iface, self.target_bssid)
            self.deauth_worker.status_msg.connect(self.write_log)
            self.deauth_worker.start()

    # --- CRACK CONTROL LOGIC (PASSWORD ATTACK) ---
    @Slot()
    def toggle_crack(self):
        # If running -> Stop
        if self.crack_worker and self.crack_worker.isRunning():
            self.crack_worker.stop()
            self.reset_crack_ui()
            self.write_log("Stopping the cracking process... please wait.")
            return

        # Check cracking conditions
        wordlist = self.ui.lineWordlistFilePath.text()
        if not self.captured_cap_path or not os.path.exists(self.captured_cap_path):
            QMessageBox.warning(
                self, "Error", "Handshake file not found! Please perform Capture first."
            )
            return
        if not wordlist or not os.path.exists(wordlist):
            QMessageBox.warning(
                self, "Error", "Please select a password dictionary file (.txt)!"
            )
            return

        # Start cracking
        self.write_log("Starting Dictionary Attack...")
        self.ui.btnAttack.setText("STOP CRACKING")
        self.ui.btnAttack.setStyleSheet(
            "background-color: #f44336; color: white; font-weight: bold;"
        )
        self.ui.lblValue.setText("Cracking...")

        self.crack_worker = CrackWorker(
            self.captured_cap_path, wordlist, self.target_bssid
        )
        self.crack_worker.status_msg.connect(self.write_log)
        self.crack_worker.result_found.connect(self.on_crack_result)
        self.crack_worker.finished.connect(self.reset_crack_ui)
        self.crack_worker.start()

    def reset_crack_ui(self):
        self.ui.btnAttack.setText("Start Attack")
        self.ui.btnAttack.setStyleSheet("")

    def on_crack_result(self, success, password):
        if success:
            self.ui.lblValue.setText(password)
            self.ui.lblValue.setStyleSheet("color: #f44336; font-weight: bold;")
            QMessageBox.critical(self, "Password Found!", f"Wi-Fi Password: {password}")
        else:
            self.ui.lblValue.setText("Not Found")
            QMessageBox.warning(
                self, "Failed", "Password not found in the selected dictionary."
            )

    def browse_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Dictionary File", "", "Text Files (*.txt)"
        )
        if file_path:
            self.ui.lineWordlistFilePath.setText(file_path)

    def toggle_monitor_mode(self):
        current_iface = self.ui.cbInterfaces.currentText()
        if current_iface == "Select Interface":
            return

        success, new_name, msg = toggle_monitor_mode(current_iface)
        if success:
            self.write_log(f"Network Mode: {msg}")
            self.load_interfaces()
            self.ui.cbInterfaces.setCurrentText(new_name)
            self.ui.lblMonitorStatus.setText(f"Mode: {new_name}")
        else:
            QMessageBox.critical(self, "Error", f"Failed to change mode: {msg}")

    def get_items(self, ssid, bssid, chan):
        """Receive data from Scan page and initialize Attack page UI"""
        self.target_ssid = ssid
        self.target_bssid = bssid
        self.target_chan = chan

        # Reset UI for new target
        self.captured_cap_path = ""
        self.log_output.clear()
        self.ui.lblValue.setText("None")
        self.ui.lblCaptureStatus.setText("Status: Waiting...")
        self.ui.lblCaptureStatus.setStyleSheet("")
        self.ui.btnAttack.setEnabled(False)
        self.ui.btnDeauth.setEnabled(False)

        # Display target info
        self.ui.lblSSID.setText(f"SSID: {ssid}")
        self.ui.lblBSSID.setText(f"BSSID: {bssid}")
        self.ui.lblChan.setText(f"CHANNEL: {chan}")

        self.ui.stackedWidget.setCurrentWidget(self.ui.pageData)
        self.write_log(f"Target selected: {ssid} ({bssid})")

    def load_interfaces(self):
        """Load list of available network interfaces"""
        interfaces = get_network_interfaces()
        self.ui.cbInterfaces.clear()
        self.ui.cbInterfaces.addItems(["Select Interface"] + interfaces)
