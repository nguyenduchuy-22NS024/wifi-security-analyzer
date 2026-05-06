from PySide6.QtCore import QThread, Signal


class ScanWorker(QThread):
    scan_completed = Signal(list, str)
    scan_error = Signal(str)

    def __init__(self, wifi_service, interface):
        super().__init__()
        self.wifi_service = wifi_service
        self.interface = interface

    def run(self):
        try:
            networks = self.wifi_service.scan_networks(self.interface)
            self.scan_completed.emit(networks, self.interface)
        except Exception as e:
            self.scan_error.emit(str(e))
