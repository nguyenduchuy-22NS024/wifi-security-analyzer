# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QSize(1280, 720))
        MainWindow.setMaximumSize(QSize(1280, 720))
        icon = QIcon()
        icon.addFile(u":/root/resources/icons8-wifi-64.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"#centralwidget {\n"
"	\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"#frSidebar {\n"
"	background-color: #eff0f1;\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frSidebar = QFrame(self.centralwidget)
        self.frSidebar.setObjectName(u"frSidebar")
        self.frSidebar.setMinimumSize(QSize(260, 0))
        self.frSidebar.setMaximumSize(QSize(260, 16777215))
        self.frSidebar.setStyleSheet(u"")
        self.frSidebar.setFrameShape(QFrame.Shape.NoFrame)
        self.frSidebar.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frSidebar)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frBrand = QFrame(self.frSidebar)
        self.frBrand.setObjectName(u"frBrand")
        self.frBrand.setStyleSheet(u"#lblName {\n"
"	font-size: 20px;\n"
"	color: rgb(13, 98, 171);\n"
"	font-weight: bold;\n"
"	text-transform: uppercase;\n"
"}")
        self.frBrand.setFrameShape(QFrame.Shape.NoFrame)
        self.frBrand.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frBrand)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(12, 0, 12, 0)
        self.lblLogo = QLabel(self.frBrand)
        self.lblLogo.setObjectName(u"lblLogo")
        self.lblLogo.setMinimumSize(QSize(64, 64))
        self.lblLogo.setMaximumSize(QSize(64, 64))
        self.lblLogo.setPixmap(QPixmap(u":/root/resources/icons8-wifi-64.png"))

        self.horizontalLayout_2.addWidget(self.lblLogo)

        self.lblName = QLabel(self.frBrand)
        self.lblName.setObjectName(u"lblName")
        self.lblName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblName.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.lblName)


        self.verticalLayout.addWidget(self.frBrand)

        self.frNav = QFrame(self.frSidebar)
        self.frNav.setObjectName(u"frNav")
        self.frNav.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	padding: 4px 8px;\n"
"	text-align: left;\n"
"	font-size: 16px;\n"
"	text-transform: uppercase;\n"
"	font-weight: 500;\n"
"}\n"
"\n"
"QPushButton:hover, QPushButton:checked{\n"
"	background-color: #ffffff;\n"
"	font-weight: bold;\n"
"}\n"
"\n"
"#btnDashboard {\n"
"	color: #1976d2;\n"
"}\n"
"\n"
"#btnScan{\n"
"	color: #3bd8b1;\n"
"}\n"
"\n"
"#btnAttack{\n"
"	color: #ed0049;\n"
"}\n"
"\n"
"#btnAnalyze {\n"
"	color: #6fc6d4;\n"
"}")
        self.frNav.setFrameShape(QFrame.Shape.NoFrame)
        self.frNav.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frNav)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.btnDashboard = QPushButton(self.frNav)
        self.btnDashboard.setObjectName(u"btnDashboard")
        icon1 = QIcon()
        icon1.addFile(u":/root/resources/icons8-dashboard-32.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnDashboard.setIcon(icon1)
        self.btnDashboard.setIconSize(QSize(32, 32))
        self.btnDashboard.setCheckable(True)
        self.btnDashboard.setChecked(True)
        self.btnDashboard.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.btnDashboard)

        self.btnScan = QPushButton(self.frNav)
        self.btnScan.setObjectName(u"btnScan")
        icon2 = QIcon()
        icon2.addFile(u":/root/resources/icons8-radar-32.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnScan.setIcon(icon2)
        self.btnScan.setIconSize(QSize(32, 32))
        self.btnScan.setCheckable(True)
        self.btnScan.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.btnScan)

        self.btnAnalyze = QPushButton(self.frNav)
        self.btnAnalyze.setObjectName(u"btnAnalyze")
        icon3 = QIcon()
        icon3.addFile(u":/root/resources/icons8-analysis-32.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAnalyze.setIcon(icon3)
        self.btnAnalyze.setIconSize(QSize(32, 32))
        self.btnAnalyze.setCheckable(True)
        self.btnAnalyze.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.btnAnalyze)

        self.btnAttack = QPushButton(self.frNav)
        self.btnAttack.setObjectName(u"btnAttack")
        icon4 = QIcon()
        icon4.addFile(u":/root/resources/icons8-sword-32.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAttack.setIcon(icon4)
        self.btnAttack.setIconSize(QSize(32, 32))
        self.btnAttack.setCheckable(True)
        self.btnAttack.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.btnAttack)


        self.verticalLayout.addWidget(self.frNav)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.frVerison = QFrame(self.frSidebar)
        self.frVerison.setObjectName(u"frVerison")
        self.frVerison.setFrameShape(QFrame.Shape.NoFrame)
        self.frVerison.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frVerison)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.lblVersion = QLabel(self.frVerison)
        self.lblVersion.setObjectName(u"lblVersion")
        self.lblVersion.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.lblVersion)


        self.verticalLayout.addWidget(self.frVerison)


        self.horizontalLayout.addWidget(self.frSidebar)

        self.frContent = QFrame(self.centralwidget)
        self.frContent.setObjectName(u"frContent")
        self.frContent.setFrameShape(QFrame.Shape.NoFrame)
        self.frContent.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frContent)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.frContent)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_4.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.frContent)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Wi-Fi Security Analyzer", None))
        self.lblName.setText(QCoreApplication.translate("MainWindow", u"Wi-Fi Security Analyzer", None))
        self.btnDashboard.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.btnScan.setText(QCoreApplication.translate("MainWindow", u"Scan", None))
        self.btnAnalyze.setText(QCoreApplication.translate("MainWindow", u"Analyze", None))
        self.btnAttack.setText(QCoreApplication.translate("MainWindow", u"Attack", None))
        self.lblVersion.setText(QCoreApplication.translate("MainWindow", u"v1.0.6 - nguyenduchuy", None))
    # retranslateUi

