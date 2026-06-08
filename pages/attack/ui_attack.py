# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'attack.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1016, 720)
        Form.setStyleSheet(u"background-color: #ffffff;")
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frHeader = QFrame(self.frame)
        self.frHeader.setObjectName(u"frHeader")
        self.frHeader.setMaximumSize(QSize(16777215, 64))
        self.frHeader.setStyleSheet(u"#lblPageName {\n"
"	font-size: 20px;\n"
"	text-transform: uppercase;\n"
"	font-weight: bold;\n"
"	color: #ed0049;\n"
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
"#btnMonitorMode {\n"
"	background-color: #0f518c;\n"
"	border: none;\n"
"	padding: 8px;\n"
"	border-radius: 4px;\n"
"	color: #ffffff;\n"
"	font-weight: bold;\n"
"	font-size: 16px;\n"
"}")
        self.frHeader.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout_2 = QHBoxLayout(self.frHeader)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.lblPageIcon = QLabel(self.frHeader)
        self.lblPageIcon.setObjectName(u"lblPageIcon")
        self.lblPageIcon.setMaximumSize(QSize(48, 48))
        self.lblPageIcon.setPixmap(QPixmap(u":/root/resources/icons8-sword-48.png"))

        self.horizontalLayout_2.addWidget(self.lblPageIcon)

        self.lblPageName = QLabel(self.frHeader)
        self.lblPageName.setObjectName(u"lblPageName")

        self.horizontalLayout_2.addWidget(self.lblPageName)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.lblMonitorStatus = QLabel(self.frHeader)
        self.lblMonitorStatus.setObjectName(u"lblMonitorStatus")

        self.horizontalLayout_2.addWidget(self.lblMonitorStatus)

        self.btnMonitorMode = QPushButton(self.frHeader)
        self.btnMonitorMode.setObjectName(u"btnMonitorMode")
        self.btnMonitorMode.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.btnMonitorMode)

        self.cbInterfaces = QComboBox(self.frHeader)
        self.cbInterfaces.addItem("")
        self.cbInterfaces.addItem("")
        self.cbInterfaces.addItem("")
        self.cbInterfaces.setObjectName(u"cbInterfaces")
        self.cbInterfaces.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.cbInterfaces)


        self.verticalLayout.addWidget(self.frHeader)

        self.frBody = QFrame(self.frame)
        self.frBody.setObjectName(u"frBody")
        self.frBody.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayout_2 = QVBoxLayout(self.frBody)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.frBody)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.pageEmpty = QWidget()
        self.pageEmpty.setObjectName(u"pageEmpty")
        self.frEmpty = QFrame(self.pageEmpty)
        self.frEmpty.setObjectName(u"frEmpty")
        self.frEmpty.setGeometry(QRect(0, 0, 1016, 652))
        self.frEmpty.setFrameShape(QFrame.Shape.NoFrame)
        self.frEmpty.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frEmpty)
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(8, 8, 8, 8)
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


        self.verticalLayout_5.addWidget(self.frStatus)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.pageEmpty)
        self.pageData = QWidget()
        self.pageData.setObjectName(u"pageData")
        self.frData = QFrame(self.pageData)
        self.frData.setObjectName(u"frData")
        self.frData.setGeometry(QRect(0, 0, 1016, 652))
        self.frData.setMinimumSize(QSize(1016, 652))
        self.frData.setFrameShape(QFrame.Shape.NoFrame)
        self.frData.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frData)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frTarget = QFrame(self.frData)
        self.frTarget.setObjectName(u"frTarget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frTarget.sizePolicy().hasHeightForWidth())
        self.frTarget.setSizePolicy(sizePolicy)
        self.frTarget.setStyleSheet(u"#lblTarget {\n"
"	font-size: 16px;\n"
"	font-weight: bold;\n"
"	color: #0f518c;\n"
"}\n"
"\n"
"#lblBSSID, #lblSSID, #lblChan {\n"
"	font-size: 14px;\n"
"	border-right: 1px solid black;\n"
"	padding-right: 8px;\n"
"}")
        self.frTarget.setFrameShape(QFrame.Shape.NoFrame)
        self.frTarget.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frTarget)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.lblTarget = QLabel(self.frTarget)
        self.lblTarget.setObjectName(u"lblTarget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lblTarget.sizePolicy().hasHeightForWidth())
        self.lblTarget.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.lblTarget)

        self.lblSSID = QLabel(self.frTarget)
        self.lblSSID.setObjectName(u"lblSSID")
        sizePolicy1.setHeightForWidth(self.lblSSID.sizePolicy().hasHeightForWidth())
        self.lblSSID.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.lblSSID)

        self.lblBSSID = QLabel(self.frTarget)
        self.lblBSSID.setObjectName(u"lblBSSID")
        sizePolicy1.setHeightForWidth(self.lblBSSID.sizePolicy().hasHeightForWidth())
        self.lblBSSID.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.lblBSSID)

        self.lblChan = QLabel(self.frTarget)
        self.lblChan.setObjectName(u"lblChan")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lblChan.sizePolicy().hasHeightForWidth())
        self.lblChan.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.lblChan)

        self.btnBack = QPushButton(self.frTarget)
        self.btnBack.setObjectName(u"btnBack")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btnBack.sizePolicy().hasHeightForWidth())
        self.btnBack.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.btnBack)


        self.verticalLayout_4.addWidget(self.frTarget)

        self.frCapture = QFrame(self.frData)
        self.frCapture.setObjectName(u"frCapture")
        sizePolicy.setHeightForWidth(self.frCapture.sizePolicy().hasHeightForWidth())
        self.frCapture.setSizePolicy(sizePolicy)
        self.frCapture.setStyleSheet(u"#lblCapture {\n"
"	font-size: 16px;\n"
"	font-weight: bold;\n"
"	color: #0f518c;\n"
"}")
        self.frCapture.setFrameShape(QFrame.Shape.NoFrame)
        self.frCapture.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frCapture)
        self.verticalLayout_7.setSpacing(4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(8, 8, 8, 8)
        self.lblCapture = QLabel(self.frCapture)
        self.lblCapture.setObjectName(u"lblCapture")

        self.verticalLayout_7.addWidget(self.lblCapture)

        self.frAction = QFrame(self.frCapture)
        self.frAction.setObjectName(u"frAction")
        self.frAction.setStyleSheet(u"#lblCaptureStatus {\n"
"	font-size: 14px;\n"
"	font-weight: bold;\n"
"}\n"
"\n"
"#btnCapture, #btnDeauth {\n"
"	padding: 8px 16px;\n"
"}")
        self.frAction.setFrameShape(QFrame.Shape.NoFrame)
        self.frAction.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frAction)
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(4, 4, 4, 4)
        self.lblCaptureStatus = QLabel(self.frAction)
        self.lblCaptureStatus.setObjectName(u"lblCaptureStatus")

        self.horizontalLayout_5.addWidget(self.lblCaptureStatus)

        self.btnCapture = QPushButton(self.frAction)
        self.btnCapture.setObjectName(u"btnCapture")
        sizePolicy3.setHeightForWidth(self.btnCapture.sizePolicy().hasHeightForWidth())
        self.btnCapture.setSizePolicy(sizePolicy3)

        self.horizontalLayout_5.addWidget(self.btnCapture)

        self.btnDeauth = QPushButton(self.frAction)
        self.btnDeauth.setObjectName(u"btnDeauth")
        sizePolicy3.setHeightForWidth(self.btnDeauth.sizePolicy().hasHeightForWidth())
        self.btnDeauth.setSizePolicy(sizePolicy3)

        self.horizontalLayout_5.addWidget(self.btnDeauth)


        self.verticalLayout_7.addWidget(self.frAction)


        self.verticalLayout_4.addWidget(self.frCapture)

        self.frCrack = QFrame(self.frData)
        self.frCrack.setObjectName(u"frCrack")
        sizePolicy.setHeightForWidth(self.frCrack.sizePolicy().hasHeightForWidth())
        self.frCrack.setSizePolicy(sizePolicy)
        self.frCrack.setStyleSheet(u"#lblCrack {\n"
"	font-size: 16px;\n"
"	font-weight: bold;\n"
"	color: #0f518c;\n"
"}\n"
"")
        self.frCrack.setFrameShape(QFrame.Shape.NoFrame)
        self.frCrack.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frCrack)
        self.verticalLayout_6.setSpacing(4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(8, 8, 8, 8)
        self.lblCrack = QLabel(self.frCrack)
        self.lblCrack.setObjectName(u"lblCrack")

        self.verticalLayout_6.addWidget(self.lblCrack)

        self.frConfigWordlist = QFrame(self.frCrack)
        self.frConfigWordlist.setObjectName(u"frConfigWordlist")
        sizePolicy.setHeightForWidth(self.frConfigWordlist.sizePolicy().hasHeightForWidth())
        self.frConfigWordlist.setSizePolicy(sizePolicy)
        self.frConfigWordlist.setStyleSheet(u"#btnBrowse, #btnAttack {\n"
"	padding: 8px 16px;\n"
"}\n"
"\n"
"#lblWordlist {\n"
"	font-size: 14px;\n"
"	font-weight: bold;\n"
"}\n"
"\n"
"#lineWordlistFilePath {\n"
"	padding: 8px 4px;\n"
"}")
        self.frConfigWordlist.setFrameShape(QFrame.Shape.NoFrame)
        self.frConfigWordlist.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frConfigWordlist)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.lblWordlist = QLabel(self.frConfigWordlist)
        self.lblWordlist.setObjectName(u"lblWordlist")

        self.horizontalLayout_3.addWidget(self.lblWordlist)

        self.lineWordlistFilePath = QLineEdit(self.frConfigWordlist)
        self.lineWordlistFilePath.setObjectName(u"lineWordlistFilePath")

        self.horizontalLayout_3.addWidget(self.lineWordlistFilePath)

        self.btnBrowse = QPushButton(self.frConfigWordlist)
        self.btnBrowse.setObjectName(u"btnBrowse")
        sizePolicy3.setHeightForWidth(self.btnBrowse.sizePolicy().hasHeightForWidth())
        self.btnBrowse.setSizePolicy(sizePolicy3)

        self.horizontalLayout_3.addWidget(self.btnBrowse)

        self.btnAttack = QPushButton(self.frConfigWordlist)
        self.btnAttack.setObjectName(u"btnAttack")
        sizePolicy3.setHeightForWidth(self.btnAttack.sizePolicy().hasHeightForWidth())
        self.btnAttack.setSizePolicy(sizePolicy3)

        self.horizontalLayout_3.addWidget(self.btnAttack)


        self.verticalLayout_6.addWidget(self.frConfigWordlist)


        self.verticalLayout_4.addWidget(self.frCrack)

        self.frLog = QFrame(self.frData)
        self.frLog.setObjectName(u"frLog")
        self.frLog.setStyleSheet(u"#lblLog {\n"
"	font-size: 16px;\n"
"	font-weight: bold;\n"
"	color: #0f518c;\n"
"}")
        self.frLog.setFrameShape(QFrame.Shape.NoFrame)
        self.frLog.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frLog)
        self.verticalLayout_9.setSpacing(4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(8, 8, 8, 8)
        self.lblLog = QLabel(self.frLog)
        self.lblLog.setObjectName(u"lblLog")
        sizePolicy.setHeightForWidth(self.lblLog.sizePolicy().hasHeightForWidth())
        self.lblLog.setSizePolicy(sizePolicy)

        self.verticalLayout_9.addWidget(self.lblLog)

        self.frLogging = QFrame(self.frLog)
        self.frLogging.setObjectName(u"frLogging")
        self.frLogging.setFrameShape(QFrame.Shape.NoFrame)
        self.frLogging.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_9.addWidget(self.frLogging)


        self.verticalLayout_4.addWidget(self.frLog)

        self.frResult = QFrame(self.frData)
        self.frResult.setObjectName(u"frResult")
        sizePolicy.setHeightForWidth(self.frResult.sizePolicy().hasHeightForWidth())
        self.frResult.setSizePolicy(sizePolicy)
        self.frResult.setStyleSheet(u"#lblResult {\n"
"	font-size: 16px;\n"
"	font-weight: bold;\n"
"	color: #0f518c;\n"
"}\n"
"\n"
"#lblValue {\n"
"	font-size: 14px;\n"
"}")
        self.frResult.setFrameShape(QFrame.Shape.NoFrame)
        self.frResult.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frResult)
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(8, 8, 8, 8)
        self.lblResult = QLabel(self.frResult)
        self.lblResult.setObjectName(u"lblResult")
        sizePolicy1.setHeightForWidth(self.lblResult.sizePolicy().hasHeightForWidth())
        self.lblResult.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.lblResult)

        self.lblValue = QLabel(self.frResult)
        self.lblValue.setObjectName(u"lblValue")

        self.horizontalLayout_4.addWidget(self.lblValue)


        self.verticalLayout_4.addWidget(self.frResult)

        self.stackedWidget.addWidget(self.pageData)
        self.pageScan = QWidget()
        self.pageScan.setObjectName(u"pageScan")
        self.frScanData = QFrame(self.pageScan)
        self.frScanData.setObjectName(u"frScanData")
        self.frScanData.setGeometry(QRect(0, 0, 1016, 652))
        self.frScanData.setFrameShape(QFrame.Shape.NoFrame)
        self.frScanData.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frScanData)
        self.verticalLayout_8.setSpacing(4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.tableScanData = QTableWidget(self.frScanData)
        if (self.tableScanData.columnCount() < 8):
            self.tableScanData.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableScanData.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableScanData.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableScanData.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableScanData.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableScanData.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableScanData.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableScanData.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableScanData.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        if (self.tableScanData.rowCount() < 1):
            self.tableScanData.setRowCount(1)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableScanData.setVerticalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableScanData.setItem(0, 1, __qtablewidgetitem9)
        self.tableScanData.setObjectName(u"tableScanData")
        self.tableScanData.setFrameShape(QFrame.Shape.NoFrame)
        self.tableScanData.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableScanData.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableScanData.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableScanData.setGridStyle(Qt.PenStyle.DashDotDotLine)
        self.tableScanData.setSortingEnabled(True)
        self.tableScanData.horizontalHeader().setStretchLastSection(False)

        self.verticalLayout_8.addWidget(self.tableScanData)

        self.stackedWidget.addWidget(self.pageScan)

        self.verticalLayout_2.addWidget(self.stackedWidget)


        self.verticalLayout.addWidget(self.frBody)


        self.verticalLayout_3.addWidget(self.frame)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lblPageIcon.setText("")
        self.lblPageName.setText(QCoreApplication.translate("Form", u"Attack", None))
        self.lblMonitorStatus.setText("")
        self.btnMonitorMode.setText(QCoreApplication.translate("Form", u"Change Mode", None))
        self.cbInterfaces.setItemText(0, QCoreApplication.translate("Form", u"New Item", None))
        self.cbInterfaces.setItemText(1, QCoreApplication.translate("Form", u"New Item", None))
        self.cbInterfaces.setItemText(2, QCoreApplication.translate("Form", u"New Item", None))

        self.lblStatusIcon.setText("")
        self.lblStatusText.setText(QCoreApplication.translate("Form", u"No data.", None))
        self.lblTarget.setText(QCoreApplication.translate("Form", u"Target:", None))
        self.lblSSID.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lblBSSID.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lblChan.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.btnBack.setText(QCoreApplication.translate("Form", u"Back", None))
        self.lblCapture.setText(QCoreApplication.translate("Form", u"Capture Handshake:", None))
        self.lblCaptureStatus.setText(QCoreApplication.translate("Form", u"Status:", None))
        self.btnCapture.setText(QCoreApplication.translate("Form", u"Start Capture", None))
        self.btnDeauth.setText(QCoreApplication.translate("Form", u"Send De-auth", None))
        self.lblCrack.setText(QCoreApplication.translate("Form", u"Crack Password:", None))
        self.lblWordlist.setText(QCoreApplication.translate("Form", u"File Wordlist:", None))
        self.btnBrowse.setText(QCoreApplication.translate("Form", u"Browse...", None))
        self.btnAttack.setText(QCoreApplication.translate("Form", u"Start Crack", None))
        self.lblLog.setText(QCoreApplication.translate("Form", u"Log:", None))
        self.lblResult.setText(QCoreApplication.translate("Form", u"Password:", None))
        self.lblValue.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        ___qtablewidgetitem = self.tableScanData.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"IN-USE", None))
        ___qtablewidgetitem1 = self.tableScanData.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"SSID", None))
        ___qtablewidgetitem2 = self.tableScanData.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"BSSID", None))
        ___qtablewidgetitem3 = self.tableScanData.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"SIGNAL", None))
        ___qtablewidgetitem4 = self.tableScanData.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"BARS", None))
        ___qtablewidgetitem5 = self.tableScanData.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"CHANNEL", None))
        ___qtablewidgetitem6 = self.tableScanData.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"BANDWIDTH", None))
        ___qtablewidgetitem7 = self.tableScanData.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"SECURITY", None))
        ___qtablewidgetitem8 = self.tableScanData.verticalHeaderItem(0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"New Row", None))

        __sortingEnabled = self.tableScanData.isSortingEnabled()
        self.tableScanData.setSortingEnabled(False)
        self.tableScanData.setSortingEnabled(__sortingEnabled)

    # retranslateUi

