import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

import page_manager

from .view.main_menu_pg_ui import Ui_main_menu_pg


class MainMenuPageQWidget(page_manager.BasePageQWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()

        self.ui.instalocker_btn.clicked.connect(lambda: self.page_manager.switch_to_page('instalocker_pg'))
        self.ui.stream_hunter_btn.clicked.connect(lambda: self.page_manager.switch_to_page('stream_hunter_pg'))

    def setup_ui(self):
        self.ui = Ui_main_menu_pg()
        self.ui.setupUi(self)
