import logging

import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

from .player import Player

logger = logging.getLogger(__name__)

# TODO: use enum for table headers
class RankTableQTableWidget(QtWidgets.QTableWidget):
    COLUMNS = [
        'Name',
        'Agent',
        'Current Rank',
        'Rank Rating',
        'Peak Rank',
        'Win Rate',
        'K/D',
        'K/M',
        'Account Level',
    ]
    # Got from testing
    _char_size = 18
    # Fits 10 rows perfectly on the table. (Table Height - Header Height) / 10
    _row_height = 37  
    
    _blue_team_color = QtGui.QColor(102, 194, 169)
    _red_team_color = QtGui.QColor(240, 92, 87)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()

    def setup_ui(self):
        logger.debug('See only')
        # Make table "see only"
        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontalHeader().setSectionsClickable(False)
        self.verticalHeader().setSectionsClickable(False)
        self.horizontalHeader().setSectionsMovable(False)
        self.verticalHeader().setSectionsMovable(False)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        
        logger.debug('Hide stuff')
        # Hide stuff
        self.verticalHeader().setVisible(False)
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.setShowGrid(False)
        
        logger.debug('Other attributes')
        # Set other attributes
        self.horizontalHeader().setMinimumSectionSize(self._char_size)
        self.setColumnCount(len(self.COLUMNS))
        self.setHorizontalHeaderLabels(self.COLUMNS)
        self.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        logger.debug('Stretch headers')
        # Set stretch factor for headers that should expand as needed
        for i, column in enumerate(self.COLUMNS):
            if column not in ['Agent', 'Current Rank', 'Peak Rank', 'Rank Rating', 'Win Rate', 'K/D', 'K/M', 'Account Level']:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                
        logger.debug('Fixed size headers')
        # Set headers fixed widths
        self.setColumnWidth(self.COLUMNS.index('Agent'),         self._char_size * 6)
        self.setColumnWidth(self.COLUMNS.index('Current Rank'),  self._char_size * 7)
        self.setColumnWidth(self.COLUMNS.index('Peak Rank'),     self._char_size * 7)
        self.setColumnWidth(self.COLUMNS.index('Rank Rating'),   self._char_size * 3.5)
        self.setColumnWidth(self.COLUMNS.index('Win Rate'),      self._char_size * 3.5)   
        self.setColumnWidth(self.COLUMNS.index('K/D'),           self._char_size * 3.5)         
        self.setColumnWidth(self.COLUMNS.index('K/M'),           self._char_size * 3.5)         
        self.setColumnWidth(self.COLUMNS.index('Account Level'), self._char_size * 3.5)

        logger.debug('Headers aliases')
        # Set alias names for specific headers
        alias_names = {
            'Name': '',
            'Agent': '',
            'Rank Rating': 'RR',
            'Win Rate': 'WR (%)',
            'Account Level': 'LVL',
            }
        for name, alias in alias_names.items():
            column_index = self.COLUMNS.index(name)
            self.setHorizontalHeaderItem(column_index, QtWidgets.QTableWidgetItem(alias))

    def populate_table(self, player_list: list[Player]):
        logger.debug('Populating table')
        self.setRowCount(len(player_list))
        for row, player in enumerate(player_list):
            self.setRowHeight(row, self._row_height)
            self.set_table_item(row, self.COLUMNS.index('Name'), player.full_name, foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('Agent'), player.agent.name.title(), foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('Current Rank'), player.current_rank.name.replace('_', ' ').title(), foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('Rank Rating'), player.rank_rating, foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('Peak Rank'), player.peak_rank.name.replace('_', ' ').title(), foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('Win Rate'), player.win_rate, foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('K/D'), player.kills_per_death, foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('K/M'), player.kills_per_match, foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('Account Level'), player.account_level, foreground=player.team)

    def set_table_item(self, row, column, value, foreground=None):
        item = QtWidgets.QTableWidgetItem(str(value))
        # Alternate row colors
        if row % 2 == 0:
            item.setBackground(QtGui.QColor(51, 61, 68))  
        else:
            item.setBackground(QtGui.QColor(255, 255, 255, 0))
        # Text color
        if foreground is not None:
            color = self._blue_team_color if foreground == 'Blue' else self._red_team_color
            item.setForeground(color)
        self.setItem(row, column, item)