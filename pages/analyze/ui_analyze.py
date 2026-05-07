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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QSizePolicy, QSpacerItem, QStackedWidget,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)
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
        self.frInfoScore.setMinimumSize(QSize(0, 192))
        self.frInfoScore.setMaximumSize(QSize(16777215, 192))
        self.frInfoScore.setStyleSheet(u"#lblInfoScoreHeader {\n"
"	font-size: 16px;\n"
"	font-weight: bold;\n"
"}")
        self.frInfoScore.setFrameShape(QFrame.Shape.NoFrame)
        self.frInfoScore.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frInfoScore)
        self.verticalLayout_6.setSpacing(4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(8, 8, 8, 8)
        self.lblInfoScoreHeader = QLabel(self.frInfoScore)
        self.lblInfoScoreHeader.setObjectName(u"lblInfoScoreHeader")
        self.lblInfoScoreHeader.setMaximumSize(QSize(16777215, 32))

        self.verticalLayout_6.addWidget(self.lblInfoScoreHeader)

        self.frInfoScoreContent = QFrame(self.frInfoScore)
        self.frInfoScoreContent.setObjectName(u"frInfoScoreContent")
        self.frInfoScoreContent.setFrameShape(QFrame.Shape.NoFrame)
        self.frInfoScoreContent.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frInfoScoreContent)
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frInfo = QFrame(self.frInfoScoreContent)
        self.frInfo.setObjectName(u"frInfo")
        self.frInfo.setFrameShape(QFrame.Shape.NoFrame)
        self.frInfo.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frInfo)
        self.horizontalLayout_10.setSpacing(4)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frInfo1 = QFrame(self.frInfo)
        self.frInfo1.setObjectName(u"frInfo1")
        self.frInfo1.setStyleSheet(u"#lblSSID, #lblBSSID, #lblSecurity, #lblFreqChan, #lblInterface, #lblScore {\n"
"	font-size: 16px;\n"
"}")
        self.frInfo1.setFrameShape(QFrame.Shape.NoFrame)
        self.frInfo1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frInfo1)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.lblSSID = QLabel(self.frInfo1)
        self.lblSSID.setObjectName(u"lblSSID")

        self.verticalLayout_4.addWidget(self.lblSSID)

        self.lblBSSID = QLabel(self.frInfo1)
        self.lblBSSID.setObjectName(u"lblBSSID")

        self.verticalLayout_4.addWidget(self.lblBSSID)

        self.lblSecurity = QLabel(self.frInfo1)
        self.lblSecurity.setObjectName(u"lblSecurity")

        self.verticalLayout_4.addWidget(self.lblSecurity)


        self.horizontalLayout_10.addWidget(self.frInfo1)

        self.frInfo2 = QFrame(self.frInfo)
        self.frInfo2.setObjectName(u"frInfo2")
        self.frInfo2.setStyleSheet(u"#lblSSID, #lblBSSID, #lblSecurity, #lblFreqChan, #lblInterface, #lblScore {\n"
"	font-size: 16px;\n"
"}")
        self.frInfo2.setFrameShape(QFrame.Shape.NoFrame)
        self.frInfo2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frInfo2)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.lblFreqChan = QLabel(self.frInfo2)
        self.lblFreqChan.setObjectName(u"lblFreqChan")

        self.verticalLayout_5.addWidget(self.lblFreqChan)

        self.lblInterface = QLabel(self.frInfo2)
        self.lblInterface.setObjectName(u"lblInterface")

        self.verticalLayout_5.addWidget(self.lblInterface)

        self.lblScore = QLabel(self.frInfo2)
        self.lblScore.setObjectName(u"lblScore")

        self.verticalLayout_5.addWidget(self.lblScore)


        self.horizontalLayout_10.addWidget(self.frInfo2)


        self.horizontalLayout_5.addWidget(self.frInfo)

        self.frScore = QFrame(self.frInfoScoreContent)
        self.frScore.setObjectName(u"frScore")
        self.frScore.setMaximumSize(QSize(136, 136))
        self.frScore.setFrameShape(QFrame.Shape.NoFrame)
        self.frScore.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_5.addWidget(self.frScore)


        self.verticalLayout_6.addWidget(self.frInfoScoreContent)


        self.verticalLayout_2.addWidget(self.frInfoScore)

        self.frDetails = QFrame(self.frData)
        self.frDetails.setObjectName(u"frDetails")
        self.frDetails.setMinimumSize(QSize(0, 250))
        self.frDetails.setMaximumSize(QSize(16777215, 250))
        self.frDetails.setStyleSheet(u"#lblDetailsHeader {\n"
"	font-size: 16px;\n"
"	font-weight: bold;\n"
"}")
        self.frDetails.setFrameShape(QFrame.Shape.NoFrame)
        self.frDetails.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frDetails)
        self.verticalLayout_7.setSpacing(4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(8, 8, 8, 8)
        self.lblDetailsHeader = QLabel(self.frDetails)
        self.lblDetailsHeader.setObjectName(u"lblDetailsHeader")
        self.lblDetailsHeader.setMaximumSize(QSize(16777215, 32))

        self.verticalLayout_7.addWidget(self.lblDetailsHeader)

        self.frDetailsContent = QFrame(self.frDetails)
        self.frDetailsContent.setObjectName(u"frDetailsContent")
        self.frDetailsContent.setFrameShape(QFrame.Shape.NoFrame)
        self.frDetailsContent.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frDetailsContent)
        self.verticalLayout_11.setSpacing(4)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.treeWidget = QTreeWidget(self.frDetailsContent)
        QTreeWidgetItem(self.treeWidget)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout_11.addWidget(self.treeWidget)


        self.verticalLayout_7.addWidget(self.frDetailsContent)


        self.verticalLayout_2.addWidget(self.frDetails)

        self.frSummary = QFrame(self.frData)
        self.frSummary.setObjectName(u"frSummary")
        self.frSummary.setStyleSheet(u"#lblSummaryHeader {\n"
"	font-size: 16px;\n"
"	font-weight: bold;\n"
"}")
        self.frSummary.setFrameShape(QFrame.Shape.NoFrame)
        self.frSummary.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frSummary)
        self.verticalLayout_8.setSpacing(4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.lblSummaryHeader = QLabel(self.frSummary)
        self.lblSummaryHeader.setObjectName(u"lblSummaryHeader")
        self.lblSummaryHeader.setMaximumSize(QSize(16777215, 32))

        self.verticalLayout_8.addWidget(self.lblSummaryHeader)

        self.frSummaryContent = QFrame(self.frSummary)
        self.frSummaryContent.setObjectName(u"frSummaryContent")
        self.frSummaryContent.setFrameShape(QFrame.Shape.NoFrame)
        self.frSummaryContent.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frSummaryContent)
        self.horizontalLayout_7.setSpacing(4)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frPros = QFrame(self.frSummaryContent)
        self.frPros.setObjectName(u"frPros")
        self.frPros.setStyleSheet(u"#lblProsHeader {\n"
"	font-size: 14px;\n"
"	font-weight: 600;\n"
"}")
        self.frPros.setFrameShape(QFrame.Shape.NoFrame)
        self.frPros.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frPros)
        self.verticalLayout_10.setSpacing(4)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.lblProsHeader = QLabel(self.frPros)
        self.lblProsHeader.setObjectName(u"lblProsHeader")
        self.lblProsHeader.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_10.addWidget(self.lblProsHeader)

        self.frProsContent = QFrame(self.frPros)
        self.frProsContent.setObjectName(u"frProsContent")
        self.frProsContent.setFrameShape(QFrame.Shape.NoFrame)
        self.frProsContent.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frProsContent)
        self.verticalLayout_12.setSpacing(4)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frProsContent)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_12.addWidget(self.label_2)


        self.verticalLayout_10.addWidget(self.frProsContent)


        self.horizontalLayout_7.addWidget(self.frPros)

        self.frCons = QFrame(self.frSummaryContent)
        self.frCons.setObjectName(u"frCons")
        self.frCons.setStyleSheet(u"#lblConsHeader {\n"
"	font-size: 14px;\n"
"	font-weight: 600;\n"
"}")
        self.frCons.setFrameShape(QFrame.Shape.NoFrame)
        self.frCons.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frCons)
        self.verticalLayout_9.setSpacing(4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.lblConsHeader = QLabel(self.frCons)
        self.lblConsHeader.setObjectName(u"lblConsHeader")
        self.lblConsHeader.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_9.addWidget(self.lblConsHeader)

        self.frConsContent = QFrame(self.frCons)
        self.frConsContent.setObjectName(u"frConsContent")
        self.frConsContent.setFrameShape(QFrame.Shape.NoFrame)
        self.frConsContent.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frConsContent)
        self.verticalLayout_13.setSpacing(4)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.frConsContent)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_13.addWidget(self.label_3)


        self.verticalLayout_9.addWidget(self.frConsContent)


        self.horizontalLayout_7.addWidget(self.frCons)


        self.verticalLayout_8.addWidget(self.frSummaryContent)


        self.verticalLayout_2.addWidget(self.frSummary)

        self.stackedWidget.addWidget(self.pageData)

        self.horizontalLayout_3.addWidget(self.stackedWidget)


        self.verticalLayout.addWidget(self.frBody)


        self.horizontalLayout.addWidget(self.frame)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lblPageIcon.setText("")
        self.lblPageName.setText(QCoreApplication.translate("Form", u"analyze network", None))
        self.lblStatusIcon.setText("")
        self.lblStatusText.setText(QCoreApplication.translate("Form", u"No data.", None))
        self.lblInfoScoreHeader.setText(QCoreApplication.translate("Form", u"Information:", None))
        self.lblSSID.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lblBSSID.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lblSecurity.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lblFreqChan.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lblInterface.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lblScore.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lblDetailsHeader.setText(QCoreApplication.translate("Form", u"Details:", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"Value", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Property", None))

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Form", u"2", None))
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Form", u"1", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.lblSummaryHeader.setText(QCoreApplication.translate("Form", u"Summary:", None))
        self.lblProsHeader.setText(QCoreApplication.translate("Form", u"Good:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Content", None))
        self.lblConsHeader.setText(QCoreApplication.translate("Form", u"Bad:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Content", None))
    # retranslateUi

