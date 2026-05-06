# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'suspicious.ui'
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
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1016, 720)
        Form.setStyleSheet(u"background-color: #ffffff;")
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
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
"	color: #ba0003;\n"
"}")
        self.frHeader.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout_2 = QHBoxLayout(self.frHeader)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.lblPageIcon = QLabel(self.frHeader)
        self.lblPageIcon.setObjectName(u"lblPageIcon")
        self.lblPageIcon.setMaximumSize(QSize(48, 48))
        self.lblPageIcon.setPixmap(QPixmap(u":/root/resources/icons8-wifi-alert-48.png"))

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
        self.horizontalLayout_3 = QHBoxLayout(self.frBody)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.frBody)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.pageEmpty = QWidget()
        self.pageEmpty.setObjectName(u"pageEmpty")
        self.frEmpty = QFrame(self.pageEmpty)
        self.frEmpty.setObjectName(u"frEmpty")
        self.frEmpty.setGeometry(QRect(0, 0, 1016, 652))
        self.frEmpty.setFrameShape(QFrame.Shape.StyledPanel)
        self.frEmpty.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frEmpty)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.frEmpty)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.stackedWidget.addWidget(self.pageEmpty)
        self.pageData = QWidget()
        self.pageData.setObjectName(u"pageData")
        self.frData = QFrame(self.pageData)
        self.frData.setObjectName(u"frData")
        self.frData.setGeometry(QRect(0, 0, 1016, 652))
        self.frData.setFrameShape(QFrame.Shape.StyledPanel)
        self.frData.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frData)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.frData)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.stackedWidget.addWidget(self.pageData)

        self.horizontalLayout_3.addWidget(self.stackedWidget)


        self.verticalLayout.addWidget(self.frBody)


        self.horizontalLayout.addWidget(self.frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lblPageIcon.setText("")
        self.lblPageName.setText(QCoreApplication.translate("Form", u"Suspicious Networks", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Empty", None))
        self.label.setText(QCoreApplication.translate("Form", u"Data", None))
    # retranslateUi

