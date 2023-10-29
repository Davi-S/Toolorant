import functools
import typing as t

import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets


def animation_running(animation: QtCore.QAbstractAnimation) -> bool:
    """
    Checks if the animation is currently running.

    Args:
        animation: The animation to check.

    Returns:
        bool: True if the animation is running, False otherwise.
    """
    return animation.state() == QtCore.QAbstractAnimation.Running



def start_animation(animation: QtCore.QVariantAnimation, start_value: t.Any, end_value: t.Any, duration: int) -> None:
    """
    Starts the animation with the specified start value, end value, and duration.

    Args:
        animation: The animation to start.
        start_value: The start value of the animation.
        end_value: The end value of the animation.
        duration: The duration of the animation in milliseconds.

    Returns:
        None
    """
    if animation_running(animation):
        animation.stop()
    animation.setDuration(duration)
    animation.setStartValue(start_value)
    animation.setEndValue(end_value)
    animation.start()


class VariantAnimation:
    """Base class with basic parameters for the variant animation"""
    def __init__(self,
                 widget: QtWidgets.QWidget,
                 start_value: t.Any,
                 end_value: t.Any,
                 duration: int) -> None:
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self._widget = widget


class StyleSheetAnimation(VariantAnimation):
    """Can animate any style sheet attribute"""
    def __init__(self, widget: QtWidgets.QWidget, style_key: str, start_value: t.Any, end_value: t.Any, duration: int) -> None:
        super().__init__(widget, start_value, end_value, duration)
        self.style_key = style_key

        self._current_style_value = self.start_value
        self._change_style(self.style_key, self.start_value)

        self._animation = self._create_animation()

    def _create_animation(self):
        animation = QtCore.QVariantAnimation(self._widget)
        animation.valueChanged.connect(
            functools.partial(self._change_style, self.style_key))
        return animation

    def _change_style(self, style_key: str, _style_value) -> None:
        if type(_style_value) == QtGui.QColor:
            style_value = _style_value.name()

        # Edit or append to the style sheet.
        # If we use just "setStyleSheet" with the new style, all the previous styles and animations would be lost
        current_style_sheet = self._widget.styleSheet()
        if (start_idx := current_style_sheet.find(style_key)) > -1:
            start_value_idx = start_idx + len(style_key) + 2
            end_value_idx = current_style_sheet.find(';', start_value_idx)
            new_style_sheet = current_style_sheet[:start_value_idx] + style_value + current_style_sheet[end_value_idx:]

        else:
            new_style_sheet = f"{current_style_sheet} {style_key}: {style_value};"

        self._widget.setStyleSheet(new_style_sheet)
        self._current_style_value = _style_value

    def start_animation(self, reversed: bool = False):
        end_value = self.start_value if reversed else self.end_value
        start_animation(
            animation=self._animation,
            start_value=self._current_style_value,
            end_value=end_value,
            duration=self._animation.currentTime()
            if animation_running(self._animation)
            else self.duration
        )


class RotateIconAnimation(VariantAnimation):
    """Can animate the widget icon with a rotation"""
    def __init__(self, widget: QtWidgets.QWidget, rotation_angle: int, duration: int) -> None:
        super().__init__(widget, 0, rotation_angle, duration)
        self._original_pixmap: QtGui.QPixmap = None
        self._pixmap_center: QtCore.QPointF = None
        self._current_angle = 0
        self._painter = QtGui.QPainter()

        self._animation = self._create_animation()

    def _create_animation(self):
        animation = QtCore.QVariantAnimation(self._widget)
        animation.valueChanged.connect(self._rotate_pixmap)
        return animation

    def _rotate_pixmap(self, angle: int) -> None:
        if not self._original_pixmap:
            self._original_pixmap = self._widget.icon().pixmap(self._widget.iconSize())
            self._pixmap_center = QtCore.QPointF(
                self._original_pixmap.width() / 2, self._original_pixmap.height() / 2
            )
        self._current_angle = angle
        self._widget.setIcon(QtGui.QIcon(
            self._get_rotated_pixmap(self._current_angle)))

    def _get_rotated_pixmap(self, angle: int) -> QtGui.QPixmap:
        rotated_pixmap = QtGui.QPixmap(self._original_pixmap.size())
        rotated_pixmap.fill(QtCore.Qt.transparent)

        self._painter.begin(rotated_pixmap)
        with self._painter as painter:
            self._painter.setRenderHints(
                QtGui.QPainter.SmoothPixmapTransform |
                QtGui.QPainter.Antialiasing
            )
            painter.translate(self._pixmap_center)
            painter.rotate(angle)
            painter.translate(-self._pixmap_center)
            painter.drawPixmap(0, 0, self._original_pixmap)

        return rotated_pixmap

    def start_animation(self, reversed=False):
        end_value = 0 if reversed else self.end_value
        start_animation(
            animation=self._animation,
            start_value=self._current_angle,
            end_value=end_value,
            duration=self._animation.currentTime()
            if animation_running(self._animation)
            else self.duration
        )
        
        
class ScaleIconAnimation(VariantAnimation):
    """Can animate a widget icon with a scale"""
    def __init__(self, widget: QtWidgets.QWidget, scale_factor: float, duration: int):
        super().__init__(widget, 1.0, scale_factor, duration)
        self._original_pixmap: QtGui.QPixmap = None
        self._current_scale = 1.0
        self._painter = QtGui.QPainter()

        self._animation = self._create_animation()

    def _create_animation(self):
        animation = QtCore.QVariantAnimation(self._widget)
        animation.valueChanged.connect(self._scale_pixmap)
        return animation

    def _scale_pixmap(self, scale_factor: float):
        if not self._original_pixmap:
            self._original_pixmap = self._widget.icon().pixmap(self._widget.iconSize())
            
        self._current_scale = scale_factor
        scaled_pixmap = self._get_scaled_pixmap(self._current_scale)
        icon = QtGui.QIcon()
        icon.addPixmap(scaled_pixmap)
        icon.addPixmap(
            scaled_pixmap,
            QtGui.QIcon.Disabled,
            QtGui.QIcon.Off
        )
        self._widget.setIcon(icon)
        

    def _get_scaled_pixmap(self, scale_factor: float):
        width = int(self._original_pixmap.width() * scale_factor)
        height = int(self._original_pixmap.height() * scale_factor)
        return self._original_pixmap.scaled(
            width,
            height,
            aspectMode=QtCore.Qt.KeepAspectRatio,
            mode=QtCore.Qt.SmoothTransformation,
        )

    def start_animation(self, reversed=False):
        end_value = 1.0 if reversed else self.end_value
        start_animation(
            animation=self._animation,
            start_value=self._current_scale,
            end_value=end_value,
            duration=self._animation.currentTime()
            if animation_running(self._animation)
            else self.duration
        )
