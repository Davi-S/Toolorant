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
        self.horizontalLayout.setContentsMargins(0, 0, 0, 12)

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

        if not streams_links:
            self.no_stream = QtWidgets.QLabel(self.streams_frm)
            self.no_stream.setObjectName(u"no_stream")
            self.no_stream.setAlignment(QtCore.Qt.AlignCenter)
            self.no_stream.setMinimumSize(QtCore.QSize(0, 36))
            self.no_stream.setMaximumSize(QtCore.QSize(500, 36))
            self.no_stream.setText('No potential streams found')
            self.verticalLayout.addWidget(self.no_stream)

        else:
            for idx, link in enumerate(streams_links):
                stream = QtWidgets.QLabel(self.streams_frm)
                stream.setObjectName(f'stream_{idx}')
                stream.setAlignment(QtCore.Qt.AlignCenter)
                stream.setMinimumSize(QtCore.QSize(0, 36))
                stream.setMaximumSize(QtCore.QSize(500, 36))
                stream.setText(link)
                stream.mousePressEvent = lambda event, stream=stream: QtWidgets.QApplication.clipboard().setText(stream.text())
                # TODO: make the tooltip follow the mouse
                stream.setMouseTracking(True)
                stream.mouseMoveEvent = lambda event: QtWidgets.QToolTip.showText(event.screenPos().toPoint(), 'Click to copy to clipboard', msecShowTime=2000)
        
                self.__setattr__(
                    f'stream_{idx}', QtWidgets.QLabel(self.streams_frm)
                )
                self.verticalLayout.addWidget(stream)
        self.verticalSpacer = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(self.verticalSpacer)
        
        self.verticalLayout_2.addWidget(self.streams_frm)
