from PySide6.QtCore import QThread, Signal


class AnalyzeWorker(QThread):
    analyze_completed = Signal(list)
    analyze_error = Signal(str)

    def __init__(self, service):
        super().__init__()
        self.service = service

    def run(self):
        try:
            analyze_result = self.service.analyze()
            self.analyze_completed.emit(analyze_result)
        except Exception as e:
            self.analyze_error.emit(str(e))
