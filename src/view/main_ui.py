# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QMainWindow, QSizePolicy,
    QStackedWidget, QToolButton, QWidget)

from custom.draggableqframe import DraggableQFrame
import resources.images_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1080, 610)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWindowTitle(u"Toolorant")
        icon = QIcon()
        icon.addFile(u":/favicon/favicon.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"")
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 0, 1080, 610))
        self.top_buttons_frm = QFrame(self.centralwidget)
        self.top_buttons_frm.setObjectName(u"top_buttons_frm")
        self.top_buttons_frm.setGeometry(QRect(1019, 0, 61, 61))
        self.top_buttons_frm.setFrameShape(QFrame.StyledPanel)
        self.top_buttons_frm.setFrameShadow(QFrame.Raised)
        self.minimize_btn = QToolButton(self.top_buttons_frm)
        self.minimize_btn.setObjectName(u"minimize_btn")
        self.minimize_btn.setGeometry(QRect(0, 22, 16, 16))
        self.minimize_btn.setCursor(QCursor(Qt.ArrowCursor))
        self.minimize_btn.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/minus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimize_btn.setIcon(icon1)
        self.minimize_btn.setIconSize(QSize(16, 16))
        self.close_btn = QToolButton(self.top_buttons_frm)
        self.close_btn.setObjectName(u"close_btn")
        self.close_btn.setGeometry(QRect(27, 22, 16, 16))
        self.close_btn.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/times.png", QSize(), QIcon.Normal, QIcon.Off)
        self.close_btn.setIcon(icon2)
        self.close_btn.setIconSize(QSize(16, 16))
        self.draggable_area_frm = DraggableQFrame(self.centralwidget)
        self.draggable_area_frm.setObjectName(u"draggable_area_frm")
        self.draggable_area_frm.setGeometry(QRect(0, 0, 1080, 12))
        self.draggable_area_frm.setCursor(QCursor(Qt.SizeAllCursor))
        self.draggable_area_frm.setStyleSheet(u"")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.minimize_btn.setText("")
        self.close_btn.setText("")
        pass
    # retranslateUi

