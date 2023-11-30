import PySide6.QtCore as QtCore
import PySide6.QtWidgets as QtWidgets

import mainwindowqmainwindow
from settings import user_settings


class DraggableQFrame(QtWidgets.QFrame): 
    """A custom QFrame class that allows for dragging and moving its QMainWindow."""
    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        main_window = mainwindowqmainwindow.get_main_window()
        delta = QtCore.QPoint(event.globalPos() - self.old_pos)
        new_pos = main_window.pos() + delta
        main_window.move(new_pos)
        user_settings.window_position = new_pos.x(), new_pos.y()
        user_settings.persist()
        self.old_pos = event.globalPos()

