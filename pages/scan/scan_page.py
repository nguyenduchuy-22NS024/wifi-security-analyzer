import json

from PySide6.QtWidgets import QHeaderView, QMenu, QTableWidgetItem, QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor, Qt, QIcon

from pages.scan.ui_scan import Ui_Form
from services.analyze_networks import analyze_scan_table


class ScanPage(QWidget):

    analyze_bssid = Signal(str, list)
    attack_items = Signal(str, str, str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.networks = []

        # Start with the empty page shown
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageEmpty)

        # Set the table to resize columns to fit their contents
        # self.ui.tableScanData.horizontalHeader().setSectionResizeMode(
        #     QHeaderView.ResizeToContents
        # )

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

        # Enable custom context menu for the table
        self.ui.tableScanData.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableScanData.customContextMenuRequested.connect(self.show_context_menu)

    # Method to update the scan results in the table
    def update_scan_results(self, networks):
        self.networks = networks
        table_data = analyze_scan_table(networks)
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageData)
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
            bssid = bssid_item.text()
            self.analyze_bssid.emit(bssid, self.networks)

    # Method to show context menu when right-clicking on a table row
    def show_context_menu(self, position):
        menu = QMenu()

        # Add actions to the context menu
        action_analyze = menu.addAction("Analyze")
        action_attack = menu.addAction("Attack")

        # Get the row that was right-clicked
        index = self.ui.tableScanData.indexAt(position)
        row = index.row()

        # If no valid row is clicked, do not show the menu
        if row < 0:
            return

        action = menu.exec(self.ui.tableScanData.viewport().mapToGlobal(position))

        if action == action_analyze:
            self.analyze_network(row)
        elif action == action_attack:
            self.attack_network(row)

    def analyze_network(self, row):
        bssid_item = self.ui.tableScanData.item(row, 2).text()
        self.analyze_bssid.emit(bssid_item, self.networks)
        
    def attack_network(self, row):
        ssid_item = self.ui.tableScanData.item(row, 1).text()
        bssid_item = self.ui.tableScanData.item(row, 2).text()
        chan_item = self.ui.tableScanData.item(row, 5).text()
        self.attack_items.emit(ssid_item, bssid_item, chan_item)
