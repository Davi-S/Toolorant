# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ranker_pg.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QSizePolicy,
    QWidget)

from custom.primaryqpushbutton import PrimaryQPushButton
from custom.topoptionqtoolbutton import TopOptionQToolButton
import resources.images_rc

class Ui_ranker_pg(object):
    def setupUi(self, ranker_pg):
        if not ranker_pg.objectName():
            ranker_pg.setObjectName(u"ranker_pg")
        ranker_pg.resize(1080, 610)
        self.main_frm = QFrame(ranker_pg)
        self.main_frm.setObjectName(u"main_frm")
        self.main_frm.setGeometry(QRect(61, 61, 958, 488))
        self.main_frm.setStyleSheet(u"")
        self.main_frm.setFrameShape(QFrame.StyledPanel)
        self.main_frm.setFrameShadow(QFrame.Raised)
        self.rank_btn = PrimaryQPushButton(self.main_frm)
        self.rank_btn.setObjectName(u"rank_btn")
        self.rank_btn.setGeometry(QRect(319, 0, 320, 45))
        self.rank_btn.setMinimumSize(QSize(0, 45))
        self.players_ranks_frm = QFrame(self.main_frm)
        self.players_ranks_frm.setObjectName(u"players_ranks_frm")
        self.players_ranks_frm.setGeometry(QRect(0, 71, 958, 417))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.players_ranks_frm.sizePolicy().hasHeightForWidth())
        self.players_ranks_frm.setSizePolicy(sizePolicy)
        self.players_ranks_frm.setMinimumSize(QSize(958, 417))
        self.players_ranks_frm.setMaximumSize(QSize(958, 417))
        self.players_ranks_frm.setFrameShape(QFrame.StyledPanel)
        self.players_ranks_frm.setFrameShadow(QFrame.Raised)
        self.player_streams_layout = QGridLayout(self.players_ranks_frm)
        self.player_streams_layout.setObjectName(u"player_streams_layout")
        self.player_streams_layout.setHorizontalSpacing(12)
        self.player_streams_layout.setVerticalSpacing(0)
        self.player_streams_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_btn = TopOptionQToolButton(ranker_pg)
        self.menu_btn.setObjectName(u"menu_btn")
        self.menu_btn.setGeometry(QRect(57, 6, 53, 37))
        self.menu_btn.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/icons/losangle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_btn.setIcon(icon)
        self.menu_btn.setIconSize(QSize(9, 9))
        self.menu_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.menu_btn.setAutoRaise(False)
        self.horizontal_line_top = QWidget(ranker_pg)
        self.horizontal_line_top.setObjectName(u"horizontal_line_top")
        self.horizontal_line_top.setGeometry(QRect(0, 12, 1080, 3))
        self.horizontal_line_top.setStyleSheet(u"")
        self.horizontal_line_top.setProperty("line", True)
        self.horizontal_line_bottom = QWidget(ranker_pg)
        self.horizontal_line_bottom.setObjectName(u"horizontal_line_bottom")
        self.horizontal_line_bottom.setGeometry(QRect(0, 595, 1080, 3))
        self.horizontal_line_bottom.setStyleSheet(u"")
        self.horizontal_line_bottom.setProperty("line", True)

        self.retranslateUi(ranker_pg)

        QMetaObject.connectSlotsByName(ranker_pg)
    # setupUi

    def retranslateUi(self, ranker_pg):
        ranker_pg.setWindowTitle(QCoreApplication.translate("ranker_pg", u"Form", None))
        self.rank_btn.setText(QCoreApplication.translate("ranker_pg", u"GET RANK", None))
        self.menu_btn.setText(QCoreApplication.translate("ranker_pg", u"MENU", None))
    # retranslateUi

