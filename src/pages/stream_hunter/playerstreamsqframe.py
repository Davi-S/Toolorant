import logging

import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

logger = logging.getLogger(__name__)


class PlayerStreamsQFrame(QtWidgets.QFrame):
    def __init__(self, player_name: str, player_agent: str, streams: list[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.player_name = player_name
        self.player_agent = player_agent
        self.streams = streams
        self.setup_ui()

    def setup_ui(self):
        self.ui = Ui_player_streams_frm()
        self.ui.setupUi(
            self,
            self.player_name,
            self.player_agent,
            self.streams
        )


class Ui_player_streams_frm(object):
    def setupUi(self, player_streams_frm, player_name: str, player_agent: str, streams_links: list[str]):
        if not player_streams_frm.objectName():
            player_streams_frm.setObjectName(u"player_streams_frm")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(player_streams_frm)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.player_frm = QtWidgets.QFrame(player_streams_frm)
        self.player_frm.setObjectName(u"player_frm")
        self.player_frm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.player_frm.setFrameShadow(QtWidgets.QFrame.Raised)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.player_frm)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.player_name = QtWidgets.QLabel(self.player_frm)
        self.player_name.setObjectName(u"player_name")
        self.player_name.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.player_name.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.player_name.setText(player_name)
        self.horizontalLayout.addWidget(self.player_name)

        self.player_agent = QtWidgets.QLabel(self.player_frm)
        self.player_agent.setObjectName(u"player_agent")
        self.player_agent.setText(player_agent)
        self.horizontalLayout.addWidget(self.player_agent)

        self.verticalLayout_2.addWidget(self.player_frm)

        self.streams_frm = QtWidgets.QFrame(player_streams_frm)
        self.streams_frm.setObjectName(u"streams_frm")
        self.streams_frm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.streams_frm.setFrameShadow(QtWidgets.QFrame.Raised)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.streams_frm)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # Dynamically add the stream links
        for idx, link in enumerate(streams_links):
            stream = QtWidgets.QLabel(self.streams_frm)
            stream.setObjectName(f'stream_{idx}')
            stream.setAlignment(QtCore.Qt.AlignCenter)
            stream.setText(link)
            self.__setattr__(
                f'stream_{idx}', QtWidgets.QLabel(self.streams_frm)
            )

            self.verticalLayout.addWidget(stream)
            self.verticalLayout.setStretch(idx, 1)

        self.verticalLayout_2.addWidget(self.streams_frm)
