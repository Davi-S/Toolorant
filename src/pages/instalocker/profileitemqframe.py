import contextlib

import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

import animations


class ProfileItemQFrame(QtWidgets.QFrame):
    color_animation_duration = 200
    background_animation_duration = 200
    icon_animation_duration = 1

    # Set profile is a variable that holds the information of the last set profile item.
    # All profiles items know which one is the active for style proposes.
    # The instalocker will know the set profile by the signal emitted on click
    set_profile = None

    set_button_clicked = QtCore.Signal()
    delete_button_clicked = QtCore.Signal()

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.setup_ui()
        self.setup_animations()

        self.ui.set_profile_btn.enterEvent = self.set_profile_btn_enter_event
        self.ui.set_profile_btn.leaveEvent = self.set_profile_btn_leave_event
        self.ui.set_profile_btn.clicked.connect(self.set_profile_btn_clicked)

        self.ui.delete_profile_btn.enterEvent = self.delete_profile_btn_enter_event
        self.ui.delete_profile_btn.leaveEvent = self.delete_profile_btn_leave_event
        self.ui.delete_profile_btn.clicked.connect(self.delete_profile_btn_clicked)

    def setup_ui(self):
        self.ui = Ui_profile_item_frm()
        self.ui.setupUi(self, self.name)
        
    def setup_animations(self):
        self.set_profile_btn_color_animation = animations.StyleSheetAnimation(
            widget=self.ui.set_profile_btn,
            style_key='color',
            start_value=QtGui.QColor(255, 255, 255, 255),
            end_value=QtGui.QColor(15, 27, 35, 255),
            duration=self.color_animation_duration
        )

        self.set_profile_btn_background_animation = animations.StyleSheetAnimation(
            widget=self.ui.set_profile_btn,
            style_key='background-color',
            start_value=QtGui.QColor(15, 27, 35, 255),
            end_value=QtGui.QColor(255, 255, 255, 255),
            duration=self.background_animation_duration
        )

        self.delete_profile_btn_icon_animation = animations.ScaleIconAnimation(
            widget=self.ui.delete_profile_btn,
            scale_factor=0.950,
            duration=self.icon_animation_duration
        )

    def set_profile_btn_enter_event(self, event=None):
        if not self.ui.set_profile_btn.isEnabled():
            return
        # Do not animate if it is the set profile. The set profile must have a "freezed" animation
        if ProfileItemQFrame.set_profile is self:
            return
        self.set_profile_btn_color_animation.start_animation()
        self.set_profile_btn_background_animation.start_animation()

    def set_profile_btn_leave_event(self, event=None):
        if not self.ui.set_profile_btn.isEnabled():
            return
        # Do not animate if it is the set profile. The set profile must have a "freezed" animation
        if ProfileItemQFrame.set_profile is self:
            return
        self.set_profile_btn_color_animation.start_animation(reversed=True)
        self.set_profile_btn_background_animation.start_animation(
            reversed=True)

    def set_profile_btn_clicked(self):
        self.set_button_clicked.emit()
        if ProfileItemQFrame.set_profile is self:
            return
        if ProfileItemQFrame.set_profile:
            # save the old set profile in a temp variable because if we call the
            # on_set_profile_btn_leave before changing the set profile, the reversed
            # animation will not occur
            temp = ProfileItemQFrame.set_profile
            ProfileItemQFrame.set_profile = self
            # Internal C++ object already deleted.
            with contextlib.suppress(RuntimeError):
                temp.set_profile_btn_leave_event()
        else:
            ProfileItemQFrame.set_profile = self

    def delete_profile_btn_enter_event(self, event=None):
        if not self.ui.delete_profile_btn.isEnabled():
            return
        self.delete_profile_btn_icon_animation.start_animation()

    def delete_profile_btn_leave_event(self, event=None):
        if not self.ui.delete_profile_btn.isEnabled():
            return
        self.delete_profile_btn_icon_animation.start_animation(reversed=True)

    def delete_profile_btn_clicked(self):
        self.delete_button_clicked.emit()

    def toggle_buttons(self, value):
        # Deactivate both set and delete buttons
        self.ui.set_profile_btn.setEnabled(value)
        self.ui.delete_profile_btn.setEnabled(value)
        # Make buttons borders gray
        if value:
            self.setStyleSheet(
                """QAbstractButton#set_profile_btn {
                    border: 2px solid white;
                }
                QAbstractButton#delete_profile_btn {
                    border: 2px solid #FF4655;
                    border-left: none;
                }"""
            )
        else:
            self.setStyleSheet(
                """QAbstractButton#set_profile_btn {
                    border: 2px solid grey;
                }
                QAbstractButton#delete_profile_btn {
                    border: 2px solid grey;
                    border-left: none;
                }"""
            )


class Ui_profile_item_frm:
    def setupUi(self, profile_item_frm, name):
        if not profile_item_frm.objectName():
            profile_item_frm.setObjectName(u"profile_item_frm")

        self.horizontalLayout = QtWidgets.QHBoxLayout(profile_item_frm)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 6)

        self.set_profile_btn = QtWidgets.QPushButton(profile_item_frm)
        self.set_profile_btn.setObjectName(u"set_profile_btn")
        self.set_profile_btn.setMinimumSize(QtCore.QSize(45, 45))
        self.set_profile_btn.setText(name)
        self.horizontalLayout.addWidget(self.set_profile_btn)

        self.delete_profile_btn = QtWidgets.QToolButton(profile_item_frm)
        self.delete_profile_btn.setObjectName(u"delete_profile_btn")
        self.delete_profile_btn.setMinimumSize(QtCore.QSize(45, 45))
        icon = QtGui.QIcon()
        # Using same file for the disabled button so the icon wont change when the set and delete buttons are disabled
        icon.addFile(
            u":/icons/icons/trash_bin.png",
            QtCore.QSize(),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        icon.addFile(
            u":/icons/icons/trash_bin.png",
            QtCore.QSize(),
            QtGui.QIcon.Disabled,
            QtGui.QIcon.Off
        )
        self.delete_profile_btn.setIcon(icon)
        self.delete_profile_btn.setIconSize(QtCore.QSize(12, 12))
        self.delete_profile_btn.setText(name)
        self.horizontalLayout.addWidget(self.delete_profile_btn)
