# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'instalocker_pg.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSizePolicy, QSpinBox, QToolButton,
    QVBoxLayout, QWidget)

from custom.primarycheckboxqpushbutton import PrimaryCheckBoxQPushButton
from custom.secondarycheckboxqpushbutton import SecondaryCheckBoxQPushButton
from custom.topoptionqtoolbutton import TopOptionQToolButton
import resources.images_rc

class Ui_instalocker_pg(object):
    def setupUi(self, instalocker_pg):
        if not instalocker_pg.objectName():
            instalocker_pg.setObjectName(u"instalocker_pg")
        instalocker_pg.resize(1080, 610)
        instalocker_pg.setStyleSheet(u"")
        self.lock_frm = QFrame(instalocker_pg)
        self.lock_frm.setObjectName(u"lock_frm")
        self.lock_frm.setGeometry(QRect(216, 567, 122, 25))
        self.lock_frm.setFrameShape(QFrame.StyledPanel)
        self.lock_frm.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.lock_frm)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.lock_lbl = QLabel(self.lock_frm)
        self.lock_lbl.setObjectName(u"lock_lbl")

        self.horizontalLayout_4.addWidget(self.lock_lbl)

        self.lock_spin = QSpinBox(self.lock_frm)
        self.lock_spin.setObjectName(u"lock_spin")
        self.lock_spin.setCursor(QCursor(Qt.IBeamCursor))
        self.lock_spin.setWrapping(False)
        self.lock_spin.setFrame(False)
        self.lock_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.lock_spin.setMaximum(30)
        self.lock_spin.setValue(2)

        self.horizontalLayout_4.addWidget(self.lock_spin)

        self.horizontal_line_bottom = QWidget(instalocker_pg)
        self.horizontal_line_bottom.setObjectName(u"horizontal_line_bottom")
        self.horizontal_line_bottom.setGeometry(QRect(0, 595, 1080, 3))
        self.horizontal_line_bottom.setStyleSheet(u"")
        self.horizontal_line_bottom.setProperty("line", True)
        self.select_frm = QFrame(instalocker_pg)
        self.select_frm.setObjectName(u"select_frm")
        self.select_frm.setGeometry(QRect(61, 567, 131, 25))
        self.select_frm.setFrameShape(QFrame.StyledPanel)
        self.select_frm.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.select_frm)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.select_lbl = QLabel(self.select_frm)
        self.select_lbl.setObjectName(u"select_lbl")

        self.horizontalLayout_3.addWidget(self.select_lbl)

        self.select_spin = QSpinBox(self.select_frm)
        self.select_spin.setObjectName(u"select_spin")
        self.select_spin.setCursor(QCursor(Qt.IBeamCursor))
        self.select_spin.setFrame(False)
        self.select_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.select_spin.setMaximum(30)
        self.select_spin.setValue(3)

        self.horizontalLayout_3.addWidget(self.select_spin)

        self.main_frm = QFrame(instalocker_pg)
        self.main_frm.setObjectName(u"main_frm")
        self.main_frm.setGeometry(QRect(61, 61, 958, 488))
        self.main_frm.setFrameShape(QFrame.StyledPanel)
        self.main_frm.setFrameShadow(QFrame.Raised)
        self.left_frm = QFrame(self.main_frm)
        self.left_frm.setObjectName(u"left_frm")
        self.left_frm.setGeometry(QRect(0, 0, 320, 488))
        self.left_frm.setMinimumSize(QSize(320, 488))
        self.left_frm.setFrameShape(QFrame.StyledPanel)
        self.left_frm.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.left_frm)
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 3, 0)
        self.start_stop_btn = PrimaryCheckBoxQPushButton(self.left_frm)
        self.start_stop_btn.setObjectName(u"start_stop_btn")
        self.start_stop_btn.setMinimumSize(QSize(0, 45))

        self.verticalLayout_3.addWidget(self.start_stop_btn)

        self.profile_list_lw = QListWidget(self.left_frm)
        self.profile_list_lw.setObjectName(u"profile_list_lw")
        self.profile_list_lw.setStyleSheet(u"")
        self.profile_list_lw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.profile_list_lw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.profile_list_lw.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.profile_list_lw.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.profile_list_lw.setSpacing(0)

        self.verticalLayout_3.addWidget(self.profile_list_lw)

        self.add_profile_frm = QFrame(self.left_frm)
        self.add_profile_frm.setObjectName(u"add_profile_frm")
        self.add_profile_frm.setMinimumSize(QSize(0, 45))
        self.add_profile_frm.setMaximumSize(QSize(16777215, 45))
        self.add_profile_frm.setFrameShape(QFrame.StyledPanel)
        self.add_profile_frm.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.add_profile_frm)
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(12, 0, 0, 0)
        self.new_profile_name_ledt = QLineEdit(self.add_profile_frm)
        self.new_profile_name_ledt.setObjectName(u"new_profile_name_ledt")
        self.new_profile_name_ledt.setFrame(False)
        self.new_profile_name_ledt.setClearButtonEnabled(False)

        self.horizontalLayout.addWidget(self.new_profile_name_ledt)

        self.add_profile_btn = QToolButton(self.add_profile_frm)
        self.add_profile_btn.setObjectName(u"add_profile_btn")
        self.add_profile_btn.setMinimumSize(QSize(45, 45))
        self.add_profile_btn.setMaximumSize(QSize(16777215, 16777215))
        self.add_profile_btn.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/icons/plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.add_profile_btn.setIcon(icon)
        self.add_profile_btn.setIconSize(QSize(12, 12))

        self.horizontalLayout.addWidget(self.add_profile_btn)


        self.verticalLayout_3.addWidget(self.add_profile_frm)

        self.create_profile_btn = SecondaryCheckBoxQPushButton(self.left_frm)
        self.create_profile_btn.setObjectName(u"create_profile_btn")
        self.create_profile_btn.setMinimumSize(QSize(0, 45))

        self.verticalLayout_3.addWidget(self.create_profile_btn)

        self.right_frm = QFrame(self.main_frm)
        self.right_frm.setObjectName(u"right_frm")
        self.right_frm.setGeometry(QRect(320, 0, 638, 488))
        self.right_frm.setMinimumSize(QSize(638, 488))
        self.right_frm.setFrameShape(QFrame.StyledPanel)
        self.right_frm.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.right_frm)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(3, 0, 0, 0)
        self.profile_info_lw = QListWidget(self.right_frm)
        self.profile_info_lw.setObjectName(u"profile_info_lw")
        self.profile_info_lw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.profile_info_lw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.profile_info_lw.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.profile_info_lw.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.horizontalLayout_2.addWidget(self.profile_info_lw)

        self.menu_btn = TopOptionQToolButton(instalocker_pg)
        self.menu_btn.setObjectName(u"menu_btn")
        self.menu_btn.setGeometry(QRect(57, 6, 53, 37))
        self.menu_btn.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/losangle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_btn.setIcon(icon1)
        self.menu_btn.setIconSize(QSize(9, 9))
        self.menu_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.menu_btn.setAutoRaise(False)
        self.horizontal_line_top = QWidget(instalocker_pg)
        self.horizontal_line_top.setObjectName(u"horizontal_line_top")
        self.horizontal_line_top.setGeometry(QRect(0, 12, 1080, 3))
        self.horizontal_line_top.setStyleSheet(u"")
        self.horizontal_line_top.setProperty("line", True)

        self.retranslateUi(instalocker_pg)

        QMetaObject.connectSlotsByName(instalocker_pg)
    # setupUi

    def retranslateUi(self, instalocker_pg):
        instalocker_pg.setWindowTitle(QCoreApplication.translate("instalocker_pg", u"Form", None))
        self.lock_lbl.setText(QCoreApplication.translate("instalocker_pg", u"Lock delay:", None))
        self.lock_spin.setSuffix(QCoreApplication.translate("instalocker_pg", u"s", None))
        self.lock_spin.setPrefix("")
        self.select_lbl.setText(QCoreApplication.translate("instalocker_pg", u"Select delay:", None))
        self.select_spin.setSuffix(QCoreApplication.translate("instalocker_pg", u"s", None))
        self.start_stop_btn.setText(QCoreApplication.translate("instalocker_pg", u"DEACTIVATED", None))
        self.new_profile_name_ledt.setText("")
        self.new_profile_name_ledt.setPlaceholderText(QCoreApplication.translate("instalocker_pg", u"New profile name", None))
        self.add_profile_btn.setText("")
        self.create_profile_btn.setText(QCoreApplication.translate("instalocker_pg", u"Create profile", None))
        self.menu_btn.setText(QCoreApplication.translate("instalocker_pg", u"MENU", None))
    # retranslateUi

