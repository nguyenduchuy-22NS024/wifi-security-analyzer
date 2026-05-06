# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1016, 720)
        Form.setMinimumSize(QSize(1016, 720))
        Form.setMaximumSize(QSize(1016, 720))
        Form.setStyleSheet(u"background-color: #ffffff;")
        self.horizontalLayout_4 = QHBoxLayout(Form)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frHeader = QFrame(self.frame)
        self.frHeader.setObjectName(u"frHeader")
        self.frHeader.setMaximumSize(QSize(16777215, 64))
        self.frHeader.setStyleSheet(u"#lblPageName {\n"
"	font-size: 20px;\n"
"	text-transform: uppercase;\n"
"	font-weight: bold;\n"
"	color: #1976d2;\n"
"}")
        self.frHeader.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout = QHBoxLayout(self.frHeader)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.lblPageIcon = QLabel(self.frHeader)
        self.lblPageIcon.setObjectName(u"lblPageIcon")
        self.lblPageIcon.setMinimumSize(QSize(48, 48))
        self.lblPageIcon.setMaximumSize(QSize(48, 48))
        self.lblPageIcon.setPixmap(QPixmap(u":/root/resources/icons8-dashboard-48.png"))

        self.horizontalLayout.addWidget(self.lblPageIcon)

        self.lblPageName = QLabel(self.frHeader)
        self.lblPageName.setObjectName(u"lblPageName")

        self.horizontalLayout.addWidget(self.lblPageName)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.frScan = QFrame(self.frHeader)
        self.frScan.setObjectName(u"frScan")
        self.frScan.setStyleSheet(u"#btnScan {\n"
"	background-color: #1976d2;\n"
"	border: none;\n"
"	padding: 8px;\n"
"	border-radius: 4px;\n"
"	color: #ffffff;\n"
"	font-weight: bold;\n"
"	font-size: 16px;\n"
"}\n"
"\n"
"#cbInterfaces {\n"
"	padding: 8px;\n"
"}\n"
"\n"
"#cbInterfaces QAbstractItemView{\n"
"	border: none;\n"
"	color: #000000;\n"
"}\n"
"\n"
"#cbInterfaces::item {\n"
"	color: #000000;\n"
"}\n"
"\n"
"")
        self.frScan.setFrameShape(QFrame.Shape.NoFrame)
        self.frScan.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frScan)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.btnScan = QPushButton(self.frScan)
        self.btnScan.setObjectName(u"btnScan")
        self.btnScan.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.btnScan)

        self.cbInterfaces = QComboBox(self.frScan)
        self.cbInterfaces.addItem("")
        self.cbInterfaces.addItem("")
        self.cbInterfaces.addItem("")
        self.cbInterfaces.setObjectName(u"cbInterfaces")
        self.cbInterfaces.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.cbInterfaces)


        self.horizontalLayout.addWidget(self.frScan)


        self.verticalLayout_2.addWidget(self.frHeader)

        self.frBody = QFrame(self.frame)
        self.frBody.setObjectName(u"frBody")
        self.frBody.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayout_3 = QVBoxLayout(self.frBody)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.frBody)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.pageEmpty = QWidget()
        self.pageEmpty.setObjectName(u"pageEmpty")
        self.frEmpty = QFrame(self.pageEmpty)
        self.frEmpty.setObjectName(u"frEmpty")
        self.frEmpty.setGeometry(QRect(0, 0, 1016, 652))
        self.frEmpty.setMinimumSize(QSize(0, 0))
        self.frEmpty.setFrameShape(QFrame.Shape.NoFrame)
        self.frEmpty.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frEmpty)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(8, 8, 8, 8)
        self.frStatus = QFrame(self.frEmpty)
        self.frStatus.setObjectName(u"frStatus")
        self.frStatus.setMinimumSize(QSize(0, 48))
        self.frStatus.setMaximumSize(QSize(16777215, 64))
        self.frStatus.setStyleSheet(u"#lblStatusText {\n"
"	color: #2196f3;\n"
"	font-weight: bold;\n"
"	font-size: 16px;\n"
"}")
        self.frStatus.setFrameShape(QFrame.Shape.NoFrame)
        self.frStatus.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frStatus)
        self.horizontalLayout_9.setSpacing(4)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(8, 8, 8, 8)
        self.lblStatusIcon = QLabel(self.frStatus)
        self.lblStatusIcon.setObjectName(u"lblStatusIcon")
        self.lblStatusIcon.setMinimumSize(QSize(32, 32))
        self.lblStatusIcon.setMaximumSize(QSize(32, 32))
        self.lblStatusIcon.setPixmap(QPixmap(u":/root/resources/icons8-info-32.png"))

        self.horizontalLayout_9.addWidget(self.lblStatusIcon)

        self.lblStatusText = QLabel(self.frStatus)
        self.lblStatusText.setObjectName(u"lblStatusText")
        self.lblStatusText.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.lblStatusText)


        self.verticalLayout_4.addWidget(self.frStatus)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.pageEmpty)
        self.pageData = QWidget()
        self.pageData.setObjectName(u"pageData")
        self.frData = QFrame(self.pageData)
        self.frData.setObjectName(u"frData")
        self.frData.setGeometry(QRect(0, 0, 1016, 652))
        self.frData.setMinimumSize(QSize(0, 0))
        self.frData.setFrameShape(QFrame.Shape.NoFrame)
        self.frData.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frData)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frCard = QFrame(self.frData)
        self.frCard.setObjectName(u"frCard")
        self.frCard.setMaximumSize(QSize(16777215, 64))
        self.frCard.setStyleSheet(u"#frCard1, #frCard2, #frCard3, #frCard4 {\n"
"	border-radius: 8px;\n"
"	border: 1px solid #dfdfdf;\n"
"}\n"
"\n"
"#frCard1 {\n"
"	border: 1px solid #2196f3;\n"
"}\n"
"\n"
"#frCard2 {\n"
"	border: 1px solid #43a047;\n"
"}\n"
"\n"
"#frCard3 {\n"
"	border: 1px solid #e6d355;\n"
"}\n"
"\n"
"#frCard4 {\n"
"	border: 1px solid #f44336;\n"
"}")
        self.frCard.setFrameShape(QFrame.Shape.NoFrame)
        self.frCard.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frCard)
        self.horizontalLayout_8.setSpacing(4)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(8, 0, 8, 0)
        self.frCard1 = QFrame(self.frCard)
        self.frCard1.setObjectName(u"frCard1")
        self.frCard1.setStyleSheet(u"#lblCardName1, #lblCardValue1 {\n"
"	font-size: 20px;\n"
"	font-weight: bold;\n"
"	color: #2196f3;\n"
"}")
        self.frCard1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frCard1.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frCard1)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(8, 0, 8, 0)
        self.lblCardLogo1 = QLabel(self.frCard1)
        self.lblCardLogo1.setObjectName(u"lblCardLogo1")
        self.lblCardLogo1.setMaximumSize(QSize(48, 48))
        self.lblCardLogo1.setPixmap(QPixmap(u":/root/resources/icons8-wifi-48.png"))

        self.horizontalLayout_3.addWidget(self.lblCardLogo1)

        self.lblCardName1 = QLabel(self.frCard1)
        self.lblCardName1.setObjectName(u"lblCardName1")

        self.horizontalLayout_3.addWidget(self.lblCardName1)

        self.lblCardValue1 = QLabel(self.frCard1)
        self.lblCardValue1.setObjectName(u"lblCardValue1")
        self.lblCardValue1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lblCardValue1)


        self.horizontalLayout_8.addWidget(self.frCard1)

        self.frCard2 = QFrame(self.frCard)
        self.frCard2.setObjectName(u"frCard2")
        self.frCard2.setStyleSheet(u"#lblCardName2, #lblCardValue2 {\n"
"	font-size: 20px;\n"
"	font-weight: bold;\n"
"	color: #43a047;\n"
"}")
        self.frCard2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frCard2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frCard2)
        self.horizontalLayout_7.setSpacing(4)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(8, 0, 8, 0)
        self.lblCardLogo2 = QLabel(self.frCard2)
        self.lblCardLogo2.setObjectName(u"lblCardLogo2")
        self.lblCardLogo2.setMaximumSize(QSize(48, 48))
        self.lblCardLogo2.setPixmap(QPixmap(u":/root/resources/icons8-secure-48.png"))

        self.horizontalLayout_7.addWidget(self.lblCardLogo2)

        self.lblCardName2 = QLabel(self.frCard2)
        self.lblCardName2.setObjectName(u"lblCardName2")

        self.horizontalLayout_7.addWidget(self.lblCardName2)

        self.lblCardValue2 = QLabel(self.frCard2)
        self.lblCardValue2.setObjectName(u"lblCardValue2")
        self.lblCardValue2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_7.addWidget(self.lblCardValue2)


        self.horizontalLayout_8.addWidget(self.frCard2)

        self.frCard3 = QFrame(self.frCard)
        self.frCard3.setObjectName(u"frCard3")
        self.frCard3.setStyleSheet(u"#lblCardName3, #lblCardValue3 {\n"
"	font-size: 20px;\n"
"	font-weight: bold;\n"
"	color: #e6d355;\n"
"}")
        self.frCard3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frCard3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frCard3)
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(8, 0, 8, 0)
        self.lblCardLogo3 = QLabel(self.frCard3)
        self.lblCardLogo3.setObjectName(u"lblCardLogo3")
        self.lblCardLogo3.setMaximumSize(QSize(48, 48))
        self.lblCardLogo3.setPixmap(QPixmap(u":/root/resources/icons8-warning-48.png"))

        self.horizontalLayout_5.addWidget(self.lblCardLogo3)

        self.lblCardName3 = QLabel(self.frCard3)
        self.lblCardName3.setObjectName(u"lblCardName3")
        self.lblCardName3.setToolTipDuration(5)

        self.horizontalLayout_5.addWidget(self.lblCardName3)

        self.lblCardValue3 = QLabel(self.frCard3)
        self.lblCardValue3.setObjectName(u"lblCardValue3")
        self.lblCardValue3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.lblCardValue3)


        self.horizontalLayout_8.addWidget(self.frCard3)

        self.frCard4 = QFrame(self.frCard)
        self.frCard4.setObjectName(u"frCard4")
        self.frCard4.setStyleSheet(u"#lblCardName4, #lblCardValue4 {\n"
"	font-size: 20px;\n"
"	font-weight: bold;\n"
"	color: #f44336;\n"
"}")
        self.frCard4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frCard4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frCard4)
        self.horizontalLayout_6.setSpacing(4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(8, 0, 8, 0)
        self.lblCardLogo4 = QLabel(self.frCard4)
        self.lblCardLogo4.setObjectName(u"lblCardLogo4")
        self.lblCardLogo4.setMaximumSize(QSize(48, 48))
        self.lblCardLogo4.setPixmap(QPixmap(u":/root/resources/icons8-warning-2-48.png"))

        self.horizontalLayout_6.addWidget(self.lblCardLogo4)

        self.lblCardName4 = QLabel(self.frCard4)
        self.lblCardName4.setObjectName(u"lblCardName4")
        self.lblCardName4.setWordWrap(True)

        self.horizontalLayout_6.addWidget(self.lblCardName4)

        self.lblCardValue4 = QLabel(self.frCard4)
        self.lblCardValue4.setObjectName(u"lblCardValue4")
        self.lblCardValue4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.lblCardValue4)


        self.horizontalLayout_8.addWidget(self.frCard4)


        self.verticalLayout.addWidget(self.frCard)

        self.frChart = QFrame(self.frData)
        self.frChart.setObjectName(u"frChart")
        self.frChart.setFrameShape(QFrame.Shape.StyledPanel)
        self.frChart.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frChart)

        self.stackedWidget.addWidget(self.pageData)

        self.verticalLayout_3.addWidget(self.stackedWidget)


        self.verticalLayout_2.addWidget(self.frBody)


        self.horizontalLayout_4.addWidget(self.frame)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lblPageIcon.setText("")
        self.lblPageName.setText(QCoreApplication.translate("Form", u"Dashboard", None))
        self.btnScan.setText(QCoreApplication.translate("Form", u"Start Scan", None))
        self.cbInterfaces.setItemText(0, QCoreApplication.translate("Form", u"New Item", None))
        self.cbInterfaces.setItemText(1, QCoreApplication.translate("Form", u"New Item", None))
        self.cbInterfaces.setItemText(2, QCoreApplication.translate("Form", u"New Item", None))

        self.lblStatusIcon.setText("")
        self.lblStatusText.setText(QCoreApplication.translate("Form", u"No data.", None))
        self.lblCardLogo1.setText("")
        self.lblCardName1.setText(QCoreApplication.translate("Form", u"Total APs:", None))
        self.lblCardValue1.setText(QCoreApplication.translate("Form", u"0", None))
        self.lblCardLogo2.setText("")
        self.lblCardName2.setText(QCoreApplication.translate("Form", u"Strong Security:", None))
        self.lblCardValue2.setText(QCoreApplication.translate("Form", u"0", None))
        self.lblCardLogo3.setText("")
        self.lblCardName3.setText(QCoreApplication.translate("Form", u"Weak Security:", None))
        self.lblCardValue3.setText(QCoreApplication.translate("Form", u"0", None))
        self.lblCardLogo4.setText("")
        self.lblCardName4.setText(QCoreApplication.translate("Form", u"Suspicious APs:", None))
        self.lblCardValue4.setText(QCoreApplication.translate("Form", u"0", None))
    # retranslateUi

