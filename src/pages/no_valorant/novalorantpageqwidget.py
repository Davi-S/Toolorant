import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

import mainwindowqmainwindow
import page_manager

from .view.no_valorant_pg_ui import Ui_main_menu_pg


class NoValorantPageQWidget(page_manager.BasePageQWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.callback = None

        self.ui.reload_btn.clicked.connect(self.reload_btn_clicked)

    def setup_ui(self):
        self.ui = Ui_main_menu_pg()
        self.ui.setupUi(self)

    def on_page_enter(self, *args, **kwargs):
        super().on_page_enter(*args, **kwargs)
        # The callback function will be called if the dependencies are connect successfully.
        # It is usually a function to return to the page that called this page
        if 'callback' in kwargs:
            self.callback = kwargs['callback']

    def reload_btn_clicked(self):
        self.ui.reload_btn.setEnabled(False)
        # Try to connect the dependencies and setup the pages
        main_window = mainwindowqmainwindow.get_main_window()
        if main_window.setup_dependencies() and main_window.connect_dependencies():
            main_window.setup_pages()
            # Exit page
            if self.callback:
                self.callback()
            else:
                self.page_manager.switch_to_page(self.page_manager.pages[0][1])
        self.ui.reload_btn.setEnabled(True)
