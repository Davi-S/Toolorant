# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stream_hunter_pg.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QSizePolicy, QWidget)

from custom.topoptionqtoolbutton import TopOptionQToolButton
import resources.images_rc

class Ui_stream_hunter_pg(object):
    def setupUi(self, stream_hunter_pg):
        if not stream_hunter_pg.objectName():
            stream_hunter_pg.setObjectName(u"stream_hunter_pg")
        stream_hunter_pg.resize(1080, 610)
        self.stream_hunter_main_frm = QFrame(stream_hunter_pg)
        self.stream_hunter_main_frm.setObjectName(u"stream_hunter_main_frm")
        self.stream_hunter_main_frm.setGeometry(QRect(61, 61, 958, 488))
        self.stream_hunter_main_frm.setStyleSheet(u"")
        self.stream_hunter_main_frm.setFrameShape(QFrame.StyledPanel)
        self.stream_hunter_main_frm.setFrameShadow(QFrame.Raised)
        self.menu_btn = TopOptionQToolButton(stream_hunter_pg)
        self.menu_btn.setObjectName(u"menu_btn")
        self.menu_btn.setGeometry(QRect(57, 6, 53, 37))
        self.menu_btn.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/icons/losangle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_btn.setIcon(icon)
        self.menu_btn.setIconSize(QSize(9, 9))
        self.menu_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.menu_btn.setAutoRaise(False)
        self.horizontal_line_top = QWidget(stream_hunter_pg)
        self.horizontal_line_top.setObjectName(u"horizontal_line_top")
        self.horizontal_line_top.setGeometry(QRect(0, 12, 1080, 3))
        self.horizontal_line_top.setStyleSheet(u"")
        self.horizontal_line_top.setProperty("line", True)
        self.horizontal_line_bottom = QWidget(stream_hunter_pg)
        self.horizontal_line_bottom.setObjectName(u"horizontal_line_bottom")
        self.horizontal_line_bottom.setGeometry(QRect(0, 595, 1080, 3))
        self.horizontal_line_bottom.setStyleSheet(u"")
        self.horizontal_line_bottom.setProperty("line", True)

        self.retranslateUi(stream_hunter_pg)

        QMetaObject.connectSlotsByName(stream_hunter_pg)
    # setupUi

    def retranslateUi(self, stream_hunter_pg):
        stream_hunter_pg.setWindowTitle(QCoreApplication.translate("stream_hunter_pg", u"Form", None))
        self.menu_btn.setText(QCoreApplication.translate("stream_hunter_pg", u"MENU", None))
    # retranslateUi

