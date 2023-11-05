# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'no_valorant_pg.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
    QWidget)

from custom.secondaryqpushbutton import SecondaryQPushButton
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
        self.reload_lbl = QLabel(self.main_frm)
        self.reload_lbl.setObjectName(u"reload_lbl")
        self.reload_lbl.setGeometry(QRect(0, 167, 958, 111))
        self.reload_lbl.setAlignment(Qt.AlignCenter)
        self.reload_btn = SecondaryQPushButton(self.main_frm)
        self.reload_btn.setObjectName(u"reload_btn")
        self.reload_btn.setGeometry(QRect(358, 280, 241, 45))
        self.reload_btn.setMinimumSize(QSize(0, 45))

        self.retranslateUi(main_menu_pg)

        QMetaObject.connectSlotsByName(main_menu_pg)
    # setupUi

    def retranslateUi(self, main_menu_pg):
        main_menu_pg.setWindowTitle(QCoreApplication.translate("main_menu_pg", u"Form", None))
        self.reload_lbl.setText(QCoreApplication.translate("main_menu_pg", u"Please open valorant and reload Toolorant", None))
        self.reload_btn.setText(QCoreApplication.translate("main_menu_pg", u"RELOAD", None))
    # retranslateUi

