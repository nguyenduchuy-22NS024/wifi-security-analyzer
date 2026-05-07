# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'scan.ui'
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
    QSizePolicy, QSpacerItem, QStackedWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
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
"	color: #3bd8b1;\n"
"}")
        self.frHeader.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout_2 = QHBoxLayout(self.frHeader)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.lblPageIcon = QLabel(self.frHeader)
        self.lblPageIcon.setObjectName(u"lblPageIcon")
        self.lblPageIcon.setMaximumSize(QSize(48, 48))
        self.lblPageIcon.setPixmap(QPixmap(u":/root/resources/icons8-radar-48.png"))

        self.horizontalLayout_2.addWidget(self.lblPageIcon)

        self.lblPageName = QLabel(self.frHeader)
        self.lblPageName.setObjectName(u"lblPageName")

        self.horizontalLayout_2.addWidget(self.lblPageName)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


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
        self.frData.setFrameShape(QFrame.Shape.NoFrame)
        self.frData.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frData)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tableScanData = QTableWidget(self.frData)
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

        self.verticalLayout_4.addWidget(self.tableScanData)

        self.frFilter = QFrame(self.frData)
        self.frFilter.setObjectName(u"frFilter")
        self.frFilter.setFrameShape(QFrame.Shape.StyledPanel)
        self.frFilter.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frFilter)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.lineEdit = QLineEdit(self.frFilter)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.lineEdit_2 = QLineEdit(self.frFilter)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_3.addWidget(self.lineEdit_2)

        self.comboBox_2 = QComboBox(self.frFilter)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_3.addWidget(self.comboBox_2)

        self.comboBox = QComboBox(self.frFilter)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_3.addWidget(self.comboBox)


        self.verticalLayout_4.addWidget(self.frFilter)

        self.stackedWidget.addWidget(self.pageData)

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
        self.lblPageName.setText(QCoreApplication.translate("Form", u"Scan results", None))
        self.lblStatusIcon.setText("")
        self.lblStatusText.setText(QCoreApplication.translate("Form", u"No data.", None))
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

