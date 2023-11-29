import PySide6.QtCore as QtCore
import PySide6.QtWidgets as QtWidgets
from pathlib import Path


def load_style_sheet(name):
    with open(name, 'r') as file:
        style_sheet = file.read()
    return style_sheet


class UpdateNotifierQDialog(QtWidgets.QDialog):
    def __init__(self, latest_version: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.latest_version = latest_version
        self.setup_ui()

    def setup_ui(self):
        self.ui = Ui_update_dlog()
        self.ui.setupUi(self, self.latest_version)
        self.setWindowFlags(
            self.windowFlags() |
            QtCore.Qt.FramelessWindowHint
        )

class Ui_update_dlog(object):
    def setupUi(self, update_dlog, latest_version):
        if not update_dlog.objectName():
            update_dlog.setObjectName(u"update_dlog")
        update_dlog.setWindowTitle("Toolorant update checker")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(update_dlog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        self.label = QtWidgets.QLabel(update_dlog)
        self.label.setObjectName(u"label")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText(f'A new update ({latest_version}) is available!\nDo you want to update?')
        self.verticalLayout.addWidget(self.label)

        self.buttonBox = QtWidgets.QDialogButtonBox(update_dlog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.No |
            QtWidgets.QDialogButtonBox.Yes
        )
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(update_dlog.accept)
        self.buttonBox.rejected.connect(update_dlog.reject)
