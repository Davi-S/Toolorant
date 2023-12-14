import PySide6.QtWidgets as QtWidgets


class RankTableQTableWidget(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()

    def setup_ui(self):
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Name", "Score"])
        self.populate_table()

    def populate_table(self):
        # Add some sample data for visualization
        data = [('Player1', '100'), ('Player2', '90'), ('Player3', '80')]

        self.setRowCount(len(data))
        for row, (name, score) in enumerate(data):
            name_item = QtWidgets.QTableWidgetItem(name)
            score_item = QtWidgets.QTableWidgetItem(score)
            self.setItem(row, 0, name_item)
            self.setItem(row, 1, score_item)
