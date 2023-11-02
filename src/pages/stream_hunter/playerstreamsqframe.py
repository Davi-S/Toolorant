import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets


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
            
        self.player_streams_frm_vertical_layout = QtWidgets.QVBoxLayout(player_streams_frm)
        self.player_streams_frm_vertical_layout.setSpacing(0)
        self.player_streams_frm_vertical_layout.setObjectName(u"player_streams_frm_vertical_layout")
        self.player_streams_frm_vertical_layout.setContentsMargins(0, 0, 0, 0)
        
        self.player_frm = QtWidgets.QFrame(player_streams_frm)
        self.player_frm.setObjectName(u"player_frm")
        
        self.player_frm_horizontal_layout = QtWidgets.QHBoxLayout(self.player_frm)
        self.player_frm_horizontal_layout.setSpacing(6)
        self.player_frm_horizontal_layout.setObjectName(u"player_frm_horizontal_layout")
        self.player_frm_horizontal_layout.setContentsMargins(0, 0, 0, 24)
        
        self.player_left_spc = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.player_frm_horizontal_layout.addItem(self.player_left_spc)

        self.player_name_lbl = QtWidgets.QLabel(self.player_frm)
        self.player_name_lbl.setObjectName(u"player_name_lbl")
        self.player_name_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.player_name_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.player_name_lbl.setText(player_name)
        self.player_frm_horizontal_layout.addWidget(self.player_name_lbl)

        self.player_agent_lbl = QtWidgets.QLabel(self.player_frm)
        self.player_agent_lbl.setObjectName(u"player_agent_lbl")
        self.player_agent_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.player_agent_lbl.setText(f'({player_agent})')
        self.player_frm_horizontal_layout.addWidget(self.player_agent_lbl)

        self.player_right_spc = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.player_frm_horizontal_layout.addItem(self.player_right_spc)

        self.player_streams_frm_vertical_layout.addWidget(self.player_frm)

        self.streams_frm = QtWidgets.QFrame(player_streams_frm)
        self.streams_frm.setObjectName(u"streams_frm")
        
        self.streams_frm_vertical_layout = QtWidgets.QVBoxLayout(self.streams_frm)
        self.streams_frm_vertical_layout.setSpacing(0)
        self.streams_frm_vertical_layout.setObjectName(u"streams_frm_vertical_layout")
        self.streams_frm_vertical_layout.setContentsMargins(0, 0, 0, 0)
        
        # Dynamically add links
        if not streams_links:
            self.no_stream = QtWidgets.QLabel(self.streams_frm)
            self.no_stream.setObjectName(u"no_stream")
            self.no_stream.setAlignment(QtCore.Qt.AlignCenter)
            self.no_stream.setMinimumSize(QtCore.QSize(0, 36))
            self.no_stream.setMaximumSize(QtCore.QSize(16777215, 36))
            self.no_stream.setText('No potential streams found')
            self.streams_frm_vertical_layout.addWidget(self.no_stream)

        else:
            for idx, link in enumerate(streams_links):
                stream_frm = QtWidgets.QFrame(self.streams_frm)
                self.__setattr__(f'stream{idx}_frm', stream_frm)
                stream_frm.setObjectName(u"stream_frm")
                
                stream_frm_horizontal_layout = QtWidgets.QHBoxLayout(stream_frm)
                self.__setattr__(f'stream{idx}_frm_horizontal_layout', stream_frm_horizontal_layout)
                stream_frm_horizontal_layout.setSpacing(0)
                stream_frm_horizontal_layout.setObjectName(u"stream_frm_horizontal_layout")
                stream_frm_horizontal_layout.setContentsMargins(0, 0, 0, 0)
                
                stream_left_spc = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.__setattr__(f'stream{idx}_left_spc', stream_left_spc)
                stream_frm_horizontal_layout.addItem(stream_left_spc)

                stream_link_lbl = QtWidgets.QLabel(stream_frm)
                self.__setattr__(f'stream{idx}_link_lbl', stream_link_lbl)
                stream_link_lbl.setObjectName(u"stream_link_lbl")
                stream_link_lbl.setMinimumSize(QtCore.QSize(0, 36))
                stream_link_lbl.setMaximumSize(QtCore.QSize(16777215, 36))
                stream_link_lbl.setTextFormat(QtCore.Qt.RichText)
                stream_link_lbl.setAlignment(QtCore.Qt.AlignCenter)
                stream_link_lbl.setText(link)
                stream_link_lbl.mousePressEvent = lambda event, stream=stream_link_lbl: QtWidgets.QApplication.clipboard().setText(stream.text())
                stream_link_lbl.mouseReleaseEvent = lambda event: QtWidgets.QToolTip.showText(event.screenPos().toPoint(), 'Copied to clipboard', msecShowTime=2000)
                # TODO: make the tooltip follow the mouse
                stream_link_lbl.enterEvent = lambda event: QtWidgets.QToolTip.showText(event.screenPos().toPoint(), 'Click to copy to clipboard', msecShowTime=2000)
                stream_frm_horizontal_layout.addWidget(stream_link_lbl)

                stream_right_spc = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.__setattr__(f'stream{idx}_right_spc', stream_right_spc)
                stream_frm_horizontal_layout.addItem(stream_right_spc)
                
                self.streams_frm_vertical_layout.addWidget(stream_frm)


        self.streams_bottom_spc = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.streams_frm_vertical_layout.addItem(self.streams_bottom_spc)

        self.player_streams_frm_vertical_layout.addWidget(self.streams_frm)
