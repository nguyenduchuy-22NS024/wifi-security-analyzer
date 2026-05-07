from PySide6.QtCore import QThread, Signal
from services.scan_networks import scan_networks


class ScanWorker(QThread):
    scan_completed = Signal(list)
    scan_error = Signal(str)

    def __init__(self, interface):
        super().__init__()
        self.interface = interface

    def run(self):
        try:
            networks = scan_networks(self.interface)
            self.scan_completed.emit(networks)
        except Exception as e:
            self.scan_error.emit(str(e))
