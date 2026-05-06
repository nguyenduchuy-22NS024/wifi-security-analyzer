# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'analyze.ui'
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
"	color: #6fc6d4;\n"
"}")
        self.frHeader.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout_2 = QHBoxLayout(self.frHeader)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.lblPageIcon = QLabel(self.frHeader)
        self.lblPageIcon.setObjectName(u"lblPageIcon")
        self.lblPageIcon.setMaximumSize(QSize(48, 48))
        self.lblPageIcon.setPixmap(QPixmap(u":/root/resources/icons8-analysis-48.png"))

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
        self.frEmpty.setFrameShape(QFrame.Shape.NoFrame)
        self.frEmpty.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frEmpty)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(8, 8, 8, 8)
        self.frStatus = QFrame(self.frEmpty)
        self.frStatus.setObjectName(u"frStatus")
        self.frStatus.setStyleSheet(u"#lblStatusText {\n"
"	color: #2196f3;\n"
"	font-weight: bold;\n"
"	font-size: 16px;\n"
"}")
        self.frStatus.setFrameShape(QFrame.Shape.NoFrame)
        self.frStatus.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frStatus)
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(8, 8, 8, 8)
        self.lblStatusIcon = QLabel(self.frStatus)
        self.lblStatusIcon.setObjectName(u"lblStatusIcon")
        self.lblStatusIcon.setMinimumSize(QSize(32, 32))
        self.lblStatusIcon.setMaximumSize(QSize(32, 32))
        self.lblStatusIcon.setPixmap(QPixmap(u":/root/resources/icons8-info-32.png"))

        self.horizontalLayout_4.addWidget(self.lblStatusIcon)

        self.lblStatusText = QLabel(self.frStatus)
        self.lblStatusText.setObjectName(u"lblStatusText")
        self.lblStatusText.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.lblStatusText)


        self.verticalLayout_3.addWidget(self.frStatus)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.pageEmpty)
        self.pageData = QWidget()
        self.pageData.setObjectName(u"pageData")
        self.frData = QFrame(self.pageData)
        self.frData.setObjectName(u"frData")
        self.frData.setGeometry(QRect(0, 0, 1016, 652))
        self.frData.setMinimumSize(QSize(1016, 652))
        self.frData.setFrameShape(QFrame.Shape.NoFrame)
        self.frData.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frData)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frInfoScore = QFrame(self.frData)
        self.frInfoScore.setObjectName(u"frInfoScore")
        self.frInfoScore.setMaximumSize(QSize(16777215, 192))
        self.frInfoScore.setFrameShape(QFrame.Shape.StyledPanel)
        self.frInfoScore.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frInfoScore)
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(8, 8, 8, 8)
        self.frInfo = QFrame(self.frInfoScore)
        self.frInfo.setObjectName(u"frInfo")
        self.frInfo.setFrameShape(QFrame.Shape.StyledPanel)
        self.frInfo.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frInfo)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.frInfo1 = QFrame(self.frInfo)
        self.frInfo1.setObjectName(u"frInfo1")
        self.frInfo1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frInfo1.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_10.addWidget(self.frInfo1)

        self.frInfo2 = QFrame(self.frInfo)
        self.frInfo2.setObjectName(u"frInfo2")
        self.frInfo2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frInfo2.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_10.addWidget(self.frInfo2)


        self.horizontalLayout_5.addWidget(self.frInfo)

        self.frScore = QFrame(self.frInfoScore)
        self.frScore.setObjectName(u"frScore")
        self.frScore.setMaximumSize(QSize(128, 128))
        self.frScore.setFrameShape(QFrame.Shape.StyledPanel)
        self.frScore.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_5.addWidget(self.frScore)


        self.verticalLayout_2.addWidget(self.frInfoScore)

        self.frDetails = QFrame(self.frData)
        self.frDetails.setObjectName(u"frDetails")
        self.frDetails.setFrameShape(QFrame.Shape.StyledPanel)
        self.frDetails.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frDetails)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(self.frDetails)
        self.label.setObjectName(u"label")

        self.horizontalLayout_7.addWidget(self.label)


        self.verticalLayout_2.addWidget(self.frDetails)

        self.frAnalyze = QFrame(self.frData)
        self.frAnalyze.setObjectName(u"frAnalyze")
        self.frAnalyze.setFrameShape(QFrame.Shape.StyledPanel)
        self.frAnalyze.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frAnalyze)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.frPros = QFrame(self.frAnalyze)
        self.frPros.setObjectName(u"frPros")
        self.frPros.setFrameShape(QFrame.Shape.StyledPanel)
        self.frPros.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frPros)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_2 = QLabel(self.frPros)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_8.addWidget(self.label_2)


        self.horizontalLayout_6.addWidget(self.frPros)

        self.frCons = QFrame(self.frAnalyze)
        self.frCons.setObjectName(u"frCons")
        self.frCons.setFrameShape(QFrame.Shape.StyledPanel)
        self.frCons.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frCons)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_3 = QLabel(self.frCons)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_9.addWidget(self.label_3)


        self.horizontalLayout_6.addWidget(self.frCons)


        self.verticalLayout_2.addWidget(self.frAnalyze)

        self.stackedWidget.addWidget(self.pageData)

        self.horizontalLayout_3.addWidget(self.stackedWidget)


        self.verticalLayout.addWidget(self.frBody)


        self.horizontalLayout.addWidget(self.frame)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lblPageIcon.setText("")
        self.lblPageName.setText(QCoreApplication.translate("Form", u"analyze network", None))
        self.lblStatusIcon.setText("")
        self.lblStatusText.setText(QCoreApplication.translate("Form", u"No data.", None))
        self.label.setText(QCoreApplication.translate("Form", u"Details", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Pros", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Cons", None))
    # retranslateUi

