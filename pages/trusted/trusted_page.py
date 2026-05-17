from PySide6.QtWidgets import QWidget
from pages.trusted.ui_trusted import Ui_Form


class TrustedPage(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
