import page_manager
from settings import app_settings

from .view.main_menu_pg_ui import Ui_main_menu_pg


class MainMenuPageQWidget(page_manager.BasePageQWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()

        self.ui.instalocker_btn.clicked.connect(lambda: self.page_manager.switch_to_page('instalocker_pg'))
        self.ui.stream_hunter_btn.clicked.connect(lambda: self.page_manager.switch_to_page('stream_hunter_pg'))
        self.ui.ranker_btn.clicked.connect(lambda: self.page_manager.switch_to_page('ranker_pg'))

    def setup_ui(self):
        self.ui = Ui_main_menu_pg()
        self.ui.setupUi(self)
        self.ui.version_lbl.setText(app_settings.version)
