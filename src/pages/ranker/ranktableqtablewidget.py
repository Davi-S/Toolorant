import PySide6.QtWidgets as QtWidgets
import PySide6.QtGui as QtGui
import PySide6.QtCore as QtCore
from .player import Player


class RankTableQTableWidget(QtWidgets.QTableWidget):
    COLUMNS = [
        'Party',
        'Name',
        'Agent',
        'Current Rank',
        'Rank Rating',
        'Peak Rank',
        'Win Rate',
        'KD',
        'HS',
        'Account Level',
    ]
    # Got from testing
    _char_size = 18
    # Fits 10 rows perfectly on the table. (Table Height - Header Height) / 10
    _row_height = 37  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()

    def setup_ui(self):
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
        
        # Hide stuff
        self.verticalHeader().setVisible(False)
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        # self.setShowGrid(False)
        
        # Set other attributes
        self.horizontalHeader().setMinimumSectionSize(self._char_size)
        self.setColumnCount(len(self.COLUMNS))
        self.setHorizontalHeaderLabels(self.COLUMNS)
        self.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        # Set stretch factor for columns that should expand as needed
        for i, column in enumerate(self.COLUMNS):
            if column not in ['Party', 'Agent', 'Current Rank', 'Peak Rank', 'Rank Rating', 'Win Rate', 'KD', 'HS', 'Account Level']:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                
        # Set columns fixed widths
        # Using 0.8 multiplier because numbers are narrower than letters characters
        self.setColumnWidth(self.COLUMNS.index('Party'),         0.8 * self._char_size * 1)   
        self.setColumnWidth(self.COLUMNS.index('Agent'),         1.0 * self._char_size * 6) # Minimum size: 6
        self.setColumnWidth(self.COLUMNS.index('Current Rank'),  1.0 * self._char_size * 7) # Minimum size: 7
        self.setColumnWidth(self.COLUMNS.index('Peak Rank'),     1.0 * self._char_size * 7) # Minimum size: 7
        self.setColumnWidth(self.COLUMNS.index('Rank Rating'),   0.8 * self._char_size * 5) # Minimum size: 2
        self.setColumnWidth(self.COLUMNS.index('Win Rate'),      0.8 * self._char_size * 5) # Minimum size: 3   
        self.setColumnWidth(self.COLUMNS.index('KD'),            0.8 * self._char_size * 5) # Minimum size: 2         
        self.setColumnWidth(self.COLUMNS.index('HS'),            0.8 * self._char_size * 5) # Minimum size: 3         
        self.setColumnWidth(self.COLUMNS.index('Account Level'), 0.8 * self._char_size * 5) # Minimum size: 3

        # Set alias names for specific headers
        alias_names = {
            'Name': '',
            'Agent': '',
            'Party': '',
            'Rank Rating': 'RR',
            'Win Rate': 'WR',
            'Account Level': 'LVL',
            }
        for actual_name, alias in alias_names.items():
            column_index = self.COLUMNS.index(actual_name)
            self.setHorizontalHeaderItem(column_index, QtWidgets.QTableWidgetItem(alias))

        
    def populate_table(self, player_list: list[Player]):
        self.setRowCount(len(player_list))
        for row, player in enumerate(player_list):
            self.set_table_item(row, self.COLUMNS.index('Party'), player.party)
            self.set_table_item(row, self.COLUMNS.index('Name'), player.full_name)
            self.set_table_item(row, self.COLUMNS.index('Agent'), player.agent.name)
            self.set_table_item(row, self.COLUMNS.index('Current Rank'), player.current_rank.name)
            self.set_table_item(row, self.COLUMNS.index('Rank Rating'), player.rank_rating)
            self.set_table_item(row, self.COLUMNS.index('Peak Rank'), player.peak_rank.name)
            self.set_table_item(row, self.COLUMNS.index('Win Rate'), player.win_rate)
            self.set_table_item(row, self.COLUMNS.index('KD'), player.kills_per_deaths)
            self.set_table_item(row, self.COLUMNS.index('HS'), player.head_shot)
            self.set_table_item(row, self.COLUMNS.index('Account Level'), player.account_level)

    def set_table_item(self, row, column, value, alignment=None):
        item = QtWidgets.QTableWidgetItem(str(value))
        self.setItem(row, column, item)
        if alignment is not None:
            item.setTextAlignment(alignment)