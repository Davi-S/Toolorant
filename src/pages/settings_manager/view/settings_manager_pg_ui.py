# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_manager_pg.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QLineEdit, QListWidget, QListWidgetItem, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

from custom.secondarycheckboxqpushbutton import SecondaryCheckBoxQPushButton
from custom.topoptionqtoolbutton import TopOptionQToolButton
import resources.images_rc

class Ui_settings_manager_pg(object):
    def setupUi(self, settings_manager_pg):
        if not settings_manager_pg.objectName():
            settings_manager_pg.setObjectName(u"settings_manager_pg")
        settings_manager_pg.resize(1080, 614)
        settings_manager_pg.setStyleSheet(u"")
        self.horizontal_line_bottom = QWidget(settings_manager_pg)
        self.horizontal_line_bottom.setObjectName(u"horizontal_line_bottom")
        self.horizontal_line_bottom.setGeometry(QRect(0, 595, 1080, 3))
        self.horizontal_line_bottom.setStyleSheet(u"")
        self.horizontal_line_bottom.setProperty("line", True)
        self.main_frm = QFrame(settings_manager_pg)
        self.main_frm.setObjectName(u"main_frm")
        self.main_frm.setGeometry(QRect(61, 61, 958, 488))
        self.main_frm.setFrameShape(QFrame.StyledPanel)
        self.main_frm.setFrameShadow(QFrame.Raised)
        self.center_frm = QFrame(self.main_frm)
        self.center_frm.setObjectName(u"center_frm")
        self.center_frm.setGeometry(QRect(269, 0, 420, 488))
        self.center_frm.setMinimumSize(QSize(320, 488))
        self.center_frm.setFrameShape(QFrame.StyledPanel)
        self.center_frm.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.center_frm)
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.s_profile_list_lw = QListWidget(self.center_frm)
        self.s_profile_list_lw.setObjectName(u"s_profile_list_lw")
        self.s_profile_list_lw.setStyleSheet(u"")
        self.s_profile_list_lw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.s_profile_list_lw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.s_profile_list_lw.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.s_profile_list_lw.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.s_profile_list_lw.setSpacing(0)

        self.verticalLayout_3.addWidget(self.s_profile_list_lw)

        self.add_s_profile_frm = QFrame(self.center_frm)
        self.add_s_profile_frm.setObjectName(u"add_s_profile_frm")
        self.add_s_profile_frm.setMinimumSize(QSize(0, 45))
        self.add_s_profile_frm.setMaximumSize(QSize(16777215, 45))
        self.add_s_profile_frm.setFrameShape(QFrame.StyledPanel)
        self.add_s_profile_frm.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.add_s_profile_frm)
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(12, 0, 0, 0)
        self.new_s_profile_name_ledt = QLineEdit(self.add_s_profile_frm)
        self.new_s_profile_name_ledt.setObjectName(u"new_s_profile_name_ledt")
        self.new_s_profile_name_ledt.setFrame(False)
        self.new_s_profile_name_ledt.setClearButtonEnabled(False)

        self.horizontalLayout.addWidget(self.new_s_profile_name_ledt)

        self.add_s_profile_btn = QToolButton(self.add_s_profile_frm)
        self.add_s_profile_btn.setObjectName(u"add_s_profile_btn")
        self.add_s_profile_btn.setMinimumSize(QSize(45, 45))
        self.add_s_profile_btn.setMaximumSize(QSize(16777215, 16777215))
        self.add_s_profile_btn.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/icons/plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.add_s_profile_btn.setIcon(icon)
        self.add_s_profile_btn.setIconSize(QSize(12, 12))

        self.horizontalLayout.addWidget(self.add_s_profile_btn)


        self.verticalLayout_3.addWidget(self.add_s_profile_frm)

        self.create_s_profile_btn = SecondaryCheckBoxQPushButton(self.center_frm)
        self.create_s_profile_btn.setObjectName(u"create_s_profile_btn")
        self.create_s_profile_btn.setMinimumSize(QSize(0, 45))

        self.verticalLayout_3.addWidget(self.create_s_profile_btn)

        self.menu_btn = TopOptionQToolButton(settings_manager_pg)
        self.menu_btn.setObjectName(u"menu_btn")
        self.menu_btn.setGeometry(QRect(57, 6, 53, 37))
        self.menu_btn.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/losangle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_btn.setIcon(icon1)
        self.menu_btn.setIconSize(QSize(9, 9))
        self.menu_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.menu_btn.setAutoRaise(False)
        self.horizontal_line_top = QWidget(settings_manager_pg)
        self.horizontal_line_top.setObjectName(u"horizontal_line_top")
        self.horizontal_line_top.setGeometry(QRect(0, 12, 1080, 3))
        self.horizontal_line_top.setStyleSheet(u"")
        self.horizontal_line_top.setProperty("line", True)

        self.retranslateUi(settings_manager_pg)

        QMetaObject.connectSlotsByName(settings_manager_pg)
    # setupUi

    def retranslateUi(self, settings_manager_pg):
        settings_manager_pg.setWindowTitle(QCoreApplication.translate("settings_manager_pg", u"Form", None))
        self.new_s_profile_name_ledt.setText("")
        self.new_s_profile_name_ledt.setPlaceholderText(QCoreApplication.translate("settings_manager_pg", u"New profile name", None))
        self.add_s_profile_btn.setText("")
        self.create_s_profile_btn.setText(QCoreApplication.translate("settings_manager_pg", u"Import from game", None))
        self.menu_btn.setText(QCoreApplication.translate("settings_manager_pg", u"MENU", None))
    # retranslateUi

