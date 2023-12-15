import logging

import PySide6.QtCore as QtCore
import PySide6.QtWidgets as QtWidgets

import mainwindowqmainwindow
import page_manager

from .player import Player
from .ranker import Ranker
from .ranktableqtablewidget import RankTableQTableWidget
from .view.ranker_pg_ui import Ui_ranker_pg

logger = logging.getLogger(__name__)


class RankerPageQWidget(page_manager.BasePageQWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.ranker_thread = RankerQThread(
            ranker=Ranker(
                client=mainwindowqmainwindow.get_main_window().client
            )
        )

        self.ui.menu_btn.clicked.connect(lambda: self.page_manager.switch_to_page('main_menu_pg'))
        self.ui.rank_btn.clicked.connect(self.rank_btn_clicked)

        self.ranker_thread.rank_result.connect(self.update_ui_with_results)

    def setup_ui(self):
        self.ui = Ui_ranker_pg()
        self.ui.setupUi(self)
        # Setup table
        table = RankTableQTableWidget(self.ui.players_ranks_frm)
        layout = QtWidgets.QVBoxLayout(self.ui.players_ranks_frm)
        layout.addWidget(table)
        self.ui.players_ranks_frm.setLayout(layout)
        self.ui.rank_table_tbl = table

    def rank_btn_clicked(self):
        logger.info('Rank button clicked')
        self.ui.rank_btn.setEnabled(False)
        self.ui.rank_btn.setText('GETTING RANKS...')
        # Start the rank operation in a separate thread to not block the UI
        self.ranker_thread.start()

    def update_ui_with_results(self, rank_result: list[Player]):
        logger.info('Updating UI')
        self.ui.rank_btn.setText('GET RANK')
        
        # TODO: order the player list
        self.ui.rank_table_tbl.populate_table(rank_result)
        
        self.ui.rank_btn.setEnabled(True)
        logger.info('UI updated')


class RankerQThread(QtCore.QThread):
    # Using object type because dict does not work as intended. https://stackoverflow.com/a/43977161/14593213
    rank_result = QtCore.Signal(list)

    def __init__(self, ranker: Ranker):
        super().__init__()
        self.ranker = ranker

    def run(self):
        result = self.ranker.rank()
        self.rank_result.emit(result)
