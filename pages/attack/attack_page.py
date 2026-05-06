from PySide6.QtWidgets import QWidget

from pages.attack.ui_attack import Ui_Form


class AttackPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def attack_network(self, bssid):
        # print("Attacking network with BSSID:", bssid)
        return
