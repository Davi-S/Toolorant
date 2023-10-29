import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

import animations

from .checkboxqpushbutton import CheckBoxQPushButton


class SecondaryCheckBoxQPushButton(CheckBoxQPushButton):
    normal_color = QtGui.QColor(255, 255, 255, 255)
    hover_color = QtGui.QColor(15, 27, 35, 255)
    color_animation_duration = 200

    normal_background = QtGui.QColor(15, 27, 35, 255)
    hover_background = QtGui.QColor(255, 255, 255, 255)
    background_animation_duration = 200

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.color_animation = animations.StyleSheetAnimation(
            widget=self,
            style_key='color',
            start_value=self.normal_color,
            end_value=self.hover_color,
            duration=self.color_animation_duration
        )
        self.background_animation = animations.StyleSheetAnimation(
            widget=self,
            style_key='background-color',
            start_value=self.normal_background,
            end_value=self.hover_background,
            duration=self.background_animation_duration
        )

    def enterEvent(self, event):
        super().enterEvent(event)
        if self.is_checked:
            return
        self.color_animation.start_animation()
        self.background_animation.start_animation()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if self.is_checked:
            return
        self.color_animation.start_animation(reversed=True)
        self.background_animation.start_animation(reversed=True)