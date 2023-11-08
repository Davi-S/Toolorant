import logging

import PySide6.QtCore as QtCore

import mainwindowqmainwindow
import page_manager

from .playerstreamsqframe import PlayerStreamsQFrame
from .stream_hunter import StreamHunter
from .view.stream_hunter_pg_ui import Ui_stream_hunter_pg

logger = logging.getLogger(__name__)


class StreamHunterPageQWidget(page_manager.BasePageQWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.hunt_thread = HuntQThread(
            stream_hunter=StreamHunter(
                client=mainwindowqmainwindow.get_main_window().client
            )
        )
        self.ui.menu_btn.clicked.connect(lambda: self.page_manager.switch_to_page('main_menu_pg'))
        self.ui.hunt_btn.clicked.connect(self.hunt_btn_clicked)
        self.hunt_thread.hunt_result.connect(self.update_ui_with_results)

    def setup_ui(self):
        self.ui = Ui_stream_hunter_pg()
        self.ui.setupUi(self)

    def hunt_btn_clicked(self):
        self.ui.hunt_btn.setEnabled(False)
        self.ui.hunt_btn.setText('HUNTING STREAMS...')
        # Start the hunt operation in a separate thread to not block the UI
        self.hunt_thread.start()

    def update_ui_with_results(self, players_streams):
        self.ui.hunt_btn.setText('HUNT STREAMS')
        # Clear the layout from previous items
        for i in reversed(range(self.ui.player_streams_layout.count())): 
            self.ui.player_streams_layout.itemAt(i).widget().deleteLater()
        row_column = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
        for (row, col), ((player, agent), streams) in zip(row_column, players_streams.items()):
            # make the last (second) row expand
            span = (2, 2) if row == 1 else (1, 1)
            frame = PlayerStreamsQFrame(player, agent, streams)
            self.ui.player_streams_layout.addWidget(frame, row, col, *span)
        self.ui.hunt_btn.setEnabled(True)


class HuntQThread(QtCore.QThread):
    # Using object type because dict does not work as intended. https://stackoverflow.com/a/43977161/14593213
    hunt_result = QtCore.Signal(object)

    def __init__(self, stream_hunter: StreamHunter):
        super().__init__()
        self.stream_hunter = stream_hunter

    def run(self):
        players_streams = self.stream_hunter.hunt()
        self.hunt_result.emit(players_streams)
