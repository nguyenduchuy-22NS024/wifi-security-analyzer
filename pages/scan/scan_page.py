from PySide6.QtWidgets import QHeaderView, QMenu, QTableWidgetItem, QWidget
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor, Qt

from pages.scan.ui_scan import Ui_Form


class ScanPage(QWidget):

    analyze_data = Signal(str, str)
    attack_data = Signal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Start with the empty page shown
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageEmpty)

        # Set the table to resize columns to fit their contents
        self.ui.tableScanData.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.ui.tableScanData.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        # Enable custom context menu for the table
        self.ui.tableScanData.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableScanData.customContextMenuRequested.connect(self.show_context_menu)

    # Method to update the scan results in the table
    def update_scan_results(self, networks, interface):
        # print(networks)
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageData)
        self.ui.tableScanData.setRowCount(0)  # Clear existing rows

        for network in networks:
            row_position = self.ui.tableScanData.rowCount()
            self.ui.tableScanData.insertRow(row_position)

            self.ui.tableScanData.setItem(
                row_position, 0, QTableWidgetItem(network["ssid"])
            )
            self.ui.tableScanData.setItem(
                row_position, 1, QTableWidgetItem(network["ssid_hex"])
            )
            self.ui.tableScanData.setItem(
                row_position, 2, QTableWidgetItem(network["bssid"])
            )
            self.ui.tableScanData.setItem(
                row_position, 3, QTableWidgetItem(network["mode"])
            )

            self.ui.tableScanData.setItem(
                row_position, 4, QTableWidgetItem(network["chan"])
            )
            self.ui.tableScanData.setItem(
                row_position, 5, QTableWidgetItem(network["freq"])
            )
            self.ui.tableScanData.setItem(
                row_position, 6, QTableWidgetItem(network["rate"])
            )
            self.ui.tableScanData.setItem(
                row_position, 7, QTableWidgetItem(network["bandwidth"])
            )
            self.ui.tableScanData.setItem(
                row_position, 8, QTableWidgetItem(network["signal"])
            )

            self.ui.tableScanData.setItem(
                row_position, 9, QTableWidgetItem(network["signal_level"])
            )

            self.ui.tableScanData.setItem(
                row_position, 10, QTableWidgetItem(network["bars"])
            )

            self.ui.tableScanData.setItem(
                row_position, 11, QTableWidgetItem(network["security"])
            )

            self.ui.tableScanData.setItem(
                row_position, 12, QTableWidgetItem(network["security_level"])
            )

            self.ui.tableScanData.setItem(
                row_position, 13, QTableWidgetItem(network["wpa_flags"])
            )

            self.ui.tableScanData.setItem(
                row_position, 14, QTableWidgetItem(network["rsn_flags"])
            )

            self.ui.tableScanData.setItem(
                row_position, 15, QTableWidgetItem(network["active"])
            )

            self.ui.tableScanData.setItem(
                row_position, 16, QTableWidgetItem(network["in_use"])
            )

            self.ui.tableScanData.setItem(row_position, 17, QTableWidgetItem(interface))

            if "Low Risk" in network["security_level"]:
                color = "#ccffcc"
            elif "Medium Risk" in network["security_level"]:
                color = "#fff5cc"
            elif (
                "High Risk" in network["security_level"]
                or "Critical" in network["security_level"]
                or "Unknown" in network["security_level"]
            ):
                color = "#ffcccc"
            else:
                color = "#ffffff"

            for col in range(self.ui.tableScanData.columnCount()):
                item = self.ui.tableScanData.item(row_position, col)
                if item:
                    item.setBackground(QColor(color))

    # Method to show context menu when right-clicking on a table row
    def show_context_menu(self, position):
        menu = QMenu()

        # Add actions to the context menu
        action_attack = menu.addAction("Attack")
        action_analyze = menu.addAction("Analyze")

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

    # Method to handle the "Analyze" action from the context menu
    def analyze_network(self, row):
        # Get the BSSID from the selected row and emit the signal to analyze it
        bssid = self.ui.tableScanData.item(row, 2).text()
        interface = self.ui.tableScanData.item(row, 17).text()
        self.analyze_data.emit(bssid, interface)

    # Method to handle the "Attack" action from the context menu
    def attack_network(self, row):
        # Get the BSSID from the selected row and emit the signal to attack it
        bssid = self.ui.tableScanData.item(row, 2).text()
        self.attack_data.emit(bssid)
