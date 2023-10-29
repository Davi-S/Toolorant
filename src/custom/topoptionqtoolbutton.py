import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

import animations


class TopOptionQToolButton(QtWidgets.QToolButton):
    # Tool buttons can have the icon on top of the text
    normal_color = QtGui.QColor(255, 255, 255, 255)
    hover_color = QtGui.QColor(255, 70, 85, 255)
    color_animation_duration = 200

    icon_rotation = 180
    icon_animation_duration = 350

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.color_animation = animations.StyleSheetAnimation(
            widget=self,
            style_key='color',
            start_value=self.normal_color,
            end_value=self.hover_color,
            duration=self.color_animation_duration
        )
        self.icon_animation = animations.RotateIconAnimation(
            widget=self,
            rotation_angle=self.icon_rotation,
            duration=self.icon_animation_duration
        )

    def enterEvent(self, event):
        super().enterEvent(event)
        self.color_animation.start_animation()
        self.icon_animation.start_animation()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.color_animation.start_animation(reversed=True)
        self.icon_animation.start_animation(reversed=True)
