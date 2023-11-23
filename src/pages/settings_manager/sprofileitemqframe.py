import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

import animations


class SProfileItemQFrame(QtWidgets.QFrame):
    icon_animation_duration = 1

    send_button_clicked = QtCore.Signal()
    delete_button_clicked = QtCore.Signal()

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.setup_ui()
        self.setup_animations()

        self.ui.send_to_game_btn.enterEvent = self.send_to_game_btn_enter_event
        self.ui.send_to_game_btn.leaveEvent = self.send_to_game_btn_leave_event
        self.ui.send_to_game_btn.clicked.connect(self.send_to_game_btn_clicked)

        self.ui.delete_s_profile_btn.enterEvent = self.delete_s_profile_btn_enter_event
        self.ui.delete_s_profile_btn.leaveEvent = self.delete_s_profile_btn_leave_event
        self.ui.delete_s_profile_btn.clicked.connect(
            self.delete_s_profile_btn_clicked)

    def setup_ui(self):
        self.ui = Ui_profile_item_frm()
        self.ui.setupUi(self, self.name)

    def setup_animations(self):
        self.send_to_game_btn_icon_animation = animations.ScaleIconAnimation(
            widget=self.ui.send_to_game_btn,
            scale_factor=0.950,
            duration=self.icon_animation_duration
        )

        self.delete_s_profile_btn_icon_animation = animations.ScaleIconAnimation(
            widget=self.ui.delete_s_profile_btn,
            scale_factor=0.950,
            duration=self.icon_animation_duration
        )

    def send_to_game_btn_enter_event(self, event=None):
        if not self.ui.send_to_game_btn.isEnabled():
            return
        self.send_to_game_btn_icon_animation.start_animation()
        self.send_to_game_btn_icon_animation.start_animation()

    def send_to_game_btn_leave_event(self, event=None):
        if not self.ui.send_to_game_btn.isEnabled():
            return
        self.send_to_game_btn_icon_animation.start_animation(reversed=True)
        self.send_to_game_btn_icon_animation.start_animation(reversed=True)

    def send_to_game_btn_clicked(self):
        self.send_button_clicked.emit()

    def delete_s_profile_btn_enter_event(self, event=None):
        if not self.ui.delete_s_profile_btn.isEnabled():
            return
        self.delete_s_profile_btn_icon_animation.start_animation()

    def delete_s_profile_btn_leave_event(self, event=None):
        if not self.ui.delete_s_profile_btn.isEnabled():
            return
        self.delete_s_profile_btn_icon_animation.start_animation(reversed=True)

    def delete_s_profile_btn_clicked(self):
        self.delete_button_clicked.emit()

    def toggle_buttons(self, value):
        # Deactivate both set and delete buttons
        self.ui.send_to_game_btn.setEnabled(value)
        self.ui.delete_s_profile_btn.setEnabled(value)
        # Make buttons borders gray
        if value:
            self.setStyleSheet(
                """QAbstractButton#send_to_game_btn {
                    border: 2px solid white;
                    border-left: none;
                }
                QAbstractButton#delete_s_profile_btn {
                    border: 2px solid #FF4655;
                    border-left: none;
                }"""
            )
        else:
            self.setStyleSheet(
                """QAbstractButton#send_to_game_btn {
                    border: 2px solid grey;
                    border-left: none;
                }
                QAbstractButton#delete_s_profile_btn {
                    border: 2px solid grey;
                    border-left: none;
                }"""
            )


class Ui_profile_item_frm:
    # TODO: add tooltips to confirm operations
    def setupUi(self, s_profile_item_frm, name):
        if not s_profile_item_frm.objectName():
            s_profile_item_frm.setObjectName(u"s_profile_item_frm")

        self.horizontalLayout = QtWidgets.QHBoxLayout(s_profile_item_frm)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 6)
        
        self.s_profile_name_lbl = QtWidgets.QLabel(s_profile_item_frm)
        self.s_profile_name_lbl.setObjectName(u"s_profile_name_lbl")
        self.s_profile_name_lbl.setMinimumSize(QtCore.QSize(0, 45))
        self.s_profile_name_lbl.setMaximumSize(QtCore.QSize(16777215, 45))
        self.s_profile_name_lbl.setText(name)
        self.horizontalLayout.addWidget(self.s_profile_name_lbl)

        self.send_to_game_btn = QtWidgets.QToolButton(s_profile_item_frm)
        self.send_to_game_btn.setObjectName(u"send_to_game_btn")
        self.send_to_game_btn.setMinimumSize(QtCore.QSize(45, 45))
        self.send_to_game_btn.setMaximumSize(QtCore.QSize(45, 45))
        icon = QtGui.QIcon()
        icon.addFile(
            u":/icons/icons/arrow-down.png",
            QtCore.QSize(),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        icon.addFile(
            u":/icons/icons/arrow-down.png",
            QtCore.QSize(),
            QtGui.QIcon.Disabled,
            QtGui.QIcon.Off
        )
        self.send_to_game_btn.setIcon(icon)
        self.send_to_game_btn.setIconSize(QtCore.QSize(12, 12))
        self.horizontalLayout.addWidget(self.send_to_game_btn)

        self.delete_s_profile_btn = QtWidgets.QToolButton(s_profile_item_frm)
        self.delete_s_profile_btn.setObjectName(u"delete_s_profile_btn")
        self.delete_s_profile_btn.setMinimumSize(QtCore.QSize(45, 45))
        self.delete_s_profile_btn.setMaximumSize(QtCore.QSize(45, 45))
        icon1 = QtGui.QIcon()
        icon1.addFile(
            u":/icons/icons/trash_bin.png",
            QtCore.QSize(),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        icon1.addFile(
            u":/icons/icons/trash_bin.png",
            QtCore.QSize(),
            QtGui.QIcon.Disabled,
            QtGui.QIcon.Off
        )
        self.delete_s_profile_btn.setIcon(icon1)
        self.horizontalLayout.addWidget(self.delete_s_profile_btn)