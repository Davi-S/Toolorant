import PySide6.QtWidgets as QtWidgets
import PySide6.QtGui as QtGui
import PySide6.QtCore as QtCore
from .player import Player

# TODO: use enum for table headers
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
    
    _blue_team_color = QtGui.QColor(102, 194, 169)
    _red_team_color = QtGui.QColor(240, 92, 87)
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
        self.setShowGrid(False)
        
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
        self.setColumnWidth(self.COLUMNS.index('Party'),         self._char_size * 1)   
        self.setColumnWidth(self.COLUMNS.index('Agent'),         self._char_size * 6)
        self.setColumnWidth(self.COLUMNS.index('Current Rank'),  self._char_size * 7)
        self.setColumnWidth(self.COLUMNS.index('Peak Rank'),     self._char_size * 7)
        self.setColumnWidth(self.COLUMNS.index('Rank Rating'),   self._char_size * 3.5)
        self.setColumnWidth(self.COLUMNS.index('Win Rate'),      self._char_size * 3.5)   
        self.setColumnWidth(self.COLUMNS.index('KD'),            self._char_size * 3.5)         
        self.setColumnWidth(self.COLUMNS.index('HS'),            self._char_size * 3.5)         
        self.setColumnWidth(self.COLUMNS.index('Account Level'), self._char_size * 3.5)

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
            self.setRowHeight(row, self._row_height)
            self.set_table_item(row, self.COLUMNS.index('Party'), player.party, background=QtGui.QColor(0, 0, 0, 0), font_size=9)
            self.set_table_item(row, self.COLUMNS.index('Name'), player.full_name, foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('Agent'), player.agent.name, foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('Current Rank'), player.current_rank.name, foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('Rank Rating'), player.rank_rating, foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('Peak Rank'), player.peak_rank.name, foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('Win Rate'), player.win_rate, foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('KD'), player.kills_per_deaths, foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('HS'), player.head_shot, foreground=player.team)
            self.set_table_item(row, self.COLUMNS.index('Account Level'), player.account_level, foreground=player.team)

    def set_table_item(self, row, column, value, background=None, foreground=None, font_size=None):
        item = QtWidgets.QTableWidgetItem(str(value))
        # Background
        if background is None:
            # Alternate row colors
            if row % 2 == 0:
                item.setBackground(QtGui.QColor(51, 61, 68))  
            else:
                item.setBackground(QtGui.QColor(255, 255, 255, 0))
        else:
            item.setBackground(background)
        # Text color
        if foreground is not None:
            color = self._blue_team_color if foreground == 'Blue' else self._red_team_color
            item.setForeground(color)
        # Set font size
        if font_size is not None:
            font = item.font()
            font.setPointSize(font_size)
            item.setFont(font)
        self.setItem(row, column, item)