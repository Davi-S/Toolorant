import logging

import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

import page_manager

from .view.stream_hunter_pg_ui import Ui_stream_hunter_pg

logger = logging.getLogger(__name__)


class StreamHunterPageQWidget(page_manager.BasePageQWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        
        self.ui.menu_btn.clicked.connect(lambda: self.page_manager.switch_to_page('main_menu_pg'))
        self.ui.hunt_btn.clicked.connect(self.hunt_btn_clicked)
        
    def setup_ui(self):
        self.ui = Ui_stream_hunter_pg()
        self.ui.setupUi(self)
        
    def hunt_btn_clicked(self):
        pass