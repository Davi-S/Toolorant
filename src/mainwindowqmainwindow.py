import logging
from pathlib import Path

import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets
import requests
from packaging import version

import page_manager
import pages.instalocker.instalockerpageqwidget as instalocker_pg
import pages.main_menu.mainmenupageqwidget as main_menu_pg
import pages.no_valorant.novalorantpageqwidget as no_valorant_pg
import pages.stream_hunter.streamhunterpageqwidget as stream_hunter_pg
from client import CustomClient
from settings import app_settings, user_settings
from updatenotifierqdialog import UpdateNotifierQDialog
from view.main_ui import Ui_MainWindow
from websocket import WebSocket

logger = logging.getLogger(__name__)

def load_style_sheet(name):
    with open(name, 'r') as file:
        style_sheet = file.read()
    return style_sheet


class MainWindowQMainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        logger.info('Initializing MainWindow')
        super().__init__()
        self.setup_ui()
        self.check_updates()
        
        # Connect signals
        self.ui.close_btn.clicked.connect(self.close)
        self.ui.minimize_btn.clicked.connect(self.showMinimized)
        
        # Setup dependencies and pages
        # The pages need to be setup after the dependencies
        self.page_manager = page_manager.PageManager(self.ui.stackedWidget)
        self.page_manager.add_page(no_valorant_pg.NoValorantPageQWidget, 'no_valorant_pg')
        if app_settings.check_dependencies:
            # Setup and validate the dependencies
            if self.setup_dependencies() and self.connect_dependencies():
                self.setup_pages()
                self.page_manager.switch_to_page('main_menu_pg')
            else:
                # If the dependencies are not connect successfully the "no_valorant_pg" page will be displayed.
                # Its only possible to leave the "no_valorant_pg" page when the dependencies are connected.
                self.page_manager.switch_to_page(
                    page_name='no_valorant_pg',
                    callback=lambda: self.page_manager.switch_to_page('main_menu_pg')
                )
        else:
            logger.warning('Not checking dependencies')
            # Setup dependencies without any validation and do not connect them
            self.setup_dependencies()
            self.setup_pages()
            self.page_manager.switch_to_page('main_menu_pg')

    def setup_ui(self) -> None:
        """Create ui and apply global stylesheets"""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(
            self.windowFlags() |
            QtCore.Qt.FramelessWindowHint
        )
        self.setStyleSheet(load_style_sheet(Path(__file__).resolve().parent / 'view/main.qss'))
        
    def check_updates(self) -> None:
        response = requests.get("https://api.github.com/repos/Davi-S/Toolorant/releases/latest")
        latest_version = response.json()["tag_name"]
        latest_version = version.parse(latest_version)

        current_version = app_settings.version
        current_version = version.parse(current_version)
        
        if latest_version > current_version:
            dialog = UpdateNotifierQDialog(latest_version)
            reply = dialog.exec_()
            if reply == QtWidgets.QDialog.Accepted:
                QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://github.com/Davi-S/Toolorant/releases/latest'))
        
    def setup_dependencies(self) -> bool:
        """
        Create the dependencies (client and websocket) and return True is they are good of False if they are bad.
        All websockets are good.
        A good client is a client created with the region found on valorant files.
        
        Note that this function will always create the dependencies. The return value indicates if the crated dependencies are good or not
        """
        return self.setup_websocket() and self.setup_client()   
    
    def connect_dependencies(self) -> bool:          
        """Activate the client and start the websocket"""      
        try:
            self.client.activate()
            self.websocket.start(
                self.client.lockfile['port'],
                self.client.lockfile['password']
            )
            logger.warn('Websocket and Client started successfully')
            # Save the region
            if self.client.region != user_settings.region:
                user_settings.region = self.client.region
                user_settings.persist()
            return True
        except Exception as e:
            logger.error(f'Could not start the Websocket and/or Client due to error: {e}')
            return False
    
    def setup_websocket(self) -> bool:
        """Set a WebSocket object on the self.websocket attribute"""
        self.websocket = WebSocket(
            callback_on_stop=lambda: self.page_manager.switch_to_page(
                page_name='no_valorant_pg',
                # This callback will return to the page that was set before the websocket stops
                callback=lambda: self.page_manager.switch_to_page(self.page_manager.previous_page[1]))
        )
        return True
    
    def setup_client(self) -> bool:
        """
        Set a Client object on the self.client attribute.
        Return True if the client was created with a good region (not the default "na")
        """
        self.client = CustomClient(user_settings.region)
        return self.client.is_good_region   
    
    def setup_pages(self) -> None:
        """Add the main pages to the main window"""
        self.page_manager.clear()
        self.page_manager.add_page(main_menu_pg.MainMenuPageQWidget, 'main_menu_pg')
        self.page_manager.add_page(instalocker_pg.InstalockerPageQWidget, 'instalocker_pg')
        self.page_manager.add_page(stream_hunter_pg.StreamHunterPageQWidget, 'stream_hunter_pg')
    

def get_main_window() -> MainWindowQMainWindow | None:
    """Returns the MainWindowQMainWindow in the application (if any)"""
    app = QtWidgets.QApplication.instance()
    return next(
        (
            widget
            for widget in app.topLevelWidgets()
            if isinstance(widget, MainWindowQMainWindow)
        ),
        None,
    )
