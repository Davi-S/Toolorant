import logging
from pathlib import Path

import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

import page_manager
import pages.instalocker.instalockerpageqwidget as instalocker_pg
import pages.main_menu.mainmenupageqwidget as main_menu_pg
import pages.no_valorant.novalorantpageqwidget as no_valorant_pg
from client import CustomClient
from settings import app_settings, user_settings
from view.main_ui import Ui_MainWindow
from websocket import WebSocket


logger = logging.getLogger(__name__)

def load_style_sheet(name):
    with open(name, 'r') as file:
        style_sheet = file.read()
    return style_sheet


class MainWindowQMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        logger.info('Initializing MainWindow')
        super().__init__()
        self.setup_ui()
        self.setup_dependencies()
        self.setup_pages()
        
        # If the dependencies are not connect successfully the "no_valorant_pg" page will be displayed.
        # Its only possible to leave the "no_valorant_pg" page if the dependencies are connected.
        if not self.connect_dependencies():
            self.page_manager.switch_to_page(
                page_name='no_valorant_pg',
                callback=lambda: self.page_manager.switch_to_page('main_menu_pg'))
        
        # Connect signals
        self.ui.close_btn.clicked.connect(self.close)
        self.ui.minimize_btn.clicked.connect(self.showMinimized)
        
    def setup_ui(self) -> None:
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(
            self.windowFlags() |
            QtCore.Qt.FramelessWindowHint
        )
        self.setStyleSheet(load_style_sheet(Path(__file__).resolve().parent / 'view/main.qss'))

    def setup_pages(self) -> None:
        self.page_manager = page_manager.PageManager(self.ui.stackedWidget)
        self.page_manager.add_page(main_menu_pg.MainMenuPageQWidget, 'main_menu_pg')
        self.page_manager.add_page(instalocker_pg.InstalockerPageQWidget, 'instalocker_pg')
        self.page_manager.add_page(no_valorant_pg.NoValorantPageQWidget, 'no_valorant_pg')
        
    def setup_dependencies(self):
        # callback_on_stop will call the "no_valorant_pg" page every time the websocket stops.
        self.websocket = WebSocket(
            callback_on_stop=lambda: self.page_manager.switch_to_page(
                page_name='no_valorant_pg',
                # This callback will return to the page that was set before the websocket stops
                callback=lambda: self.page_manager.switch_to_page(self.page_manager.previous_page[1]))
        )
        self.client = CustomClient(user_settings.region)
    
    def connect_dependencies(self) -> bool:
        # Only try to connect if the dependencies do not pass the check
        if self._check_dependencies():
            return True
        
        # Create another instance of the client if it was created using default region (usually "na").
        # Then check if this new instance was also created with the default region.
        # Will only try to connect when the client instance is not created with default region.
        # There will be no errors if a client created with the default region is activate, but the client will not work as intended.
        # The client is usually only created with default region on the first run.
        # After the program find the region on valorant files, the region is saved on the user settings file and load on every startup.
        # If a new region (different from the one in the user settings) is find on the valorant file, it is saved on the user settings files.
        if self.client.using_default_region:
            self.client = CustomClient()
        if self.client.using_default_region:
            return False
        
        try:
            self.client.activate()
            self.websocket.start(
                self.client.lockfile['port'],
                self.client.lockfile['password']
            )
            logger.warn('Websocket and Client started successfully')
            # Save the new region
            if self.client.region != user_settings.region:
                user_settings.region = self.client.region
                user_settings.persist()
            return True
        except Exception as e:
            logger.error(f'Could not start the Websocket and/or Client due to error: {e}')
            return False
        
    def _check_dependencies(self):
        # Only check for the dependencies if the settings is set to do so.
        # This is useful to test the application when the dependencies are not essential
        if app_settings.check_dependencies:
            return self.websocket.is_running and self.client.is_active
        return True
    
    
def get_main_window() -> MainWindowQMainWindow | None:
    # sourcery skip: use-next
    # Global function to find the MainWindowQMainWindow in application
    app = QtWidgets.QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, MainWindowQMainWindow):
            return widget
    return None
