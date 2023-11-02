import logging

import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

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
        self.stream_hunter = StreamHunter(
            client=mainwindowqmainwindow.get_main_window().client
        )

        self.ui.menu_btn.clicked.connect(lambda: self.page_manager.switch_to_page('main_menu_pg'))
        self.ui.hunt_btn.clicked.connect(self.hunt_btn_clicked)

    def setup_ui(self):
        self.ui = Ui_stream_hunter_pg()
        self.ui.setupUi(self)

    def hunt_btn_clicked(self):
        players_streams = self.stream_hunter.hunt()
        row_column = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
        for (row, col), (player, streams) in zip(row_column, players_streams.items()):
            # make the last (second) row expand
            span = (2, 2) if row == 1 else (1, 1)
            frame = PlayerStreamsQFrame(player[0], player[1], streams)
            self.ui.player_streams_layout.addWidget(frame, row, col, *span)
