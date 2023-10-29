import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets


class CheckBoxQPushButton(QtWidgets.QPushButton):
    """Base class that adds a variable to check if a push button is active of not, like a checkbox"""
    # Using a pushbutton as a checkbox because its not possible to align the text on the center in a normal checkbox
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.is_checked = False
        
    def mouseReleaseEvent(self, event):
        self.is_checked = not self.is_checked
        super().mouseReleaseEvent(event)