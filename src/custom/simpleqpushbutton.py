import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

import animations


class SimpleQPushButton(QtWidgets.QPushButton):
    normal_color = QtGui.QColor(255, 255, 255, 255)
    hover_color = QtGui.QColor(255, 70, 85, 255)
    color_animation_duration = 200

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.color_animation = animations.StyleSheetAnimation(
            widget=self,
            style_key='color',
            start_value=self.normal_color,
            end_value=self.hover_color,
            duration=self.color_animation_duration
        )

    def enterEvent(self, event):
        super().enterEvent(event)
        self.color_animation.start_animation()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.color_animation.start_animation(reversed=True)
