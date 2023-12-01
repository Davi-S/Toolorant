# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_menu_pg.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLayout,
    QSizePolicy, QVBoxLayout, QWidget)

from custom.bigoptionqpushbutton import BigOptionQPushButton
from custom.simpleqpushbutton import SimpleQPushButton
import resources.images_rc

class Ui_main_menu_pg(object):
    def setupUi(self, main_menu_pg):
        if not main_menu_pg.objectName():
            main_menu_pg.setObjectName(u"main_menu_pg")
        main_menu_pg.resize(1080, 610)
        self.main_frm = QFrame(main_menu_pg)
        self.main_frm.setObjectName(u"main_frm")
        self.main_frm.setGeometry(QRect(61, 61, 958, 488))
        self.main_frm.setStyleSheet(u"")
        self.main_frm.setFrameShape(QFrame.StyledPanel)
        self.main_frm.setFrameShadow(QFrame.Raised)
        self.options_frm = QFrame(self.main_frm)
        self.options_frm.setObjectName(u"options_frm")
        self.options_frm.setGeometry(QRect(0, 176, 308, 135))
        self.options_frm.setFrameShape(QFrame.StyledPanel)
        self.options_frm.setFrameShadow(QFrame.Raised)
        self.options_frm.setLineWidth(1)
        self.verticalLayout_2 = QVBoxLayout(self.options_frm)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.instalocker_btn = BigOptionQPushButton(self.options_frm)
        self.instalocker_btn.setObjectName(u"instalocker_btn")
        self.instalocker_btn.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/icons/losangle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.instalocker_btn.setIcon(icon)
        self.instalocker_btn.setIconSize(QSize(9, 9))
        self.instalocker_btn.setFlat(False)

        self.verticalLayout_2.addWidget(self.instalocker_btn, 0, Qt.AlignLeft)

        self.stream_hunter_btn = BigOptionQPushButton(self.options_frm)
        self.stream_hunter_btn.setObjectName(u"stream_hunter_btn")
        self.stream_hunter_btn.setIcon(icon)
        self.stream_hunter_btn.setIconSize(QSize(9, 9))

        self.verticalLayout_2.addWidget(self.stream_hunter_btn, 0, Qt.AlignLeft)

        self.ranker_btn = BigOptionQPushButton(self.options_frm)
        self.ranker_btn.setObjectName(u"ranker_btn")
        self.ranker_btn.setIcon(icon)
        self.ranker_btn.setIconSize(QSize(9, 9))

        self.verticalLayout_2.addWidget(self.ranker_btn, 0, Qt.AlignLeft)

        self.settings_btn = SimpleQPushButton(self.main_frm)
        self.settings_btn.setObjectName(u"settings_btn")
        self.settings_btn.setGeometry(QRect(881, 467, 77, 21))
        self.settings_btn.setLayoutDirection(Qt.RightToLeft)
        self.vertical_line = QWidget(main_menu_pg)
        self.vertical_line.setObjectName(u"vertical_line")
        self.vertical_line.setGeometry(QRect(66, 0, 3, 610))
        self.vertical_line.setStyleSheet(u"")
        self.vertical_line.setProperty("line", True)
        self.version_lbl = QLabel(main_menu_pg)
        self.version_lbl.setObjectName(u"version_lbl")
        self.version_lbl.setGeometry(QRect(1005, 580, 60, 20))
        self.version_lbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.retranslateUi(main_menu_pg)

        QMetaObject.connectSlotsByName(main_menu_pg)
    # setupUi

    def retranslateUi(self, main_menu_pg):
        main_menu_pg.setWindowTitle(QCoreApplication.translate("main_menu_pg", u"Form", None))
        self.instalocker_btn.setText(QCoreApplication.translate("main_menu_pg", u"   INSTALOCKER", None))
        self.stream_hunter_btn.setText(QCoreApplication.translate("main_menu_pg", u"   STREAM HUNTER", None))
        self.ranker_btn.setText(QCoreApplication.translate("main_menu_pg", u"   RANKER", None))
        self.settings_btn.setText(QCoreApplication.translate("main_menu_pg", u"SETTINGS", None))
        self.version_lbl.setText("")
    # retranslateUi

