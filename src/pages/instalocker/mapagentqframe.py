import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

import animations


class MapAgentQFrame(QtWidgets.QFrame):
    color_animation_duration = 200

    def __init__(self, map, agent, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.map = map
        self.agent = agent
        self.setup_ui()
        self.setup_animations()

    def setup_ui(self):
        self.ui = Ui_map_agent_frm()
        self.ui.setupUi(self, self.map, self.agent)

    def setup_animations(self):
        self.map_lbl_color_animation = animations.StyleSheetAnimation(
            widget=self.ui.map_lbl,
            style_key='color',
            start_value=QtGui.QColor(255, 255, 255, 255),
            end_value=QtGui.QColor(255, 70, 85, 255),
            duration=self.color_animation_duration
        )
        self.agent_lbl_color_animation = animations.StyleSheetAnimation(
            widget=self.ui.agent_lbl,
            style_key='color',
            start_value=QtGui.QColor(255, 255, 255, 255),
            end_value=QtGui.QColor(255, 70, 85, 255),
            duration=self.color_animation_duration
        )

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.map_lbl_color_animation.start_animation()
        self.agent_lbl_color_animation.start_animation()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.map_lbl_color_animation.start_animation(reversed=True)
        self.agent_lbl_color_animation.start_animation(reversed=True)


class Ui_map_agent_frm:
    def setupUi(self, map_agent_frm, map, agent):
        # sourcery skip: extract-duplicate-method
        if not map_agent_frm.objectName():
            map_agent_frm.setObjectName(u"map_agent_frm")

        # Add bottom margin on the inner layout and add a border on the outer frame
        # This way the margin will not push the border
        self.map_agent_outer_horizontal_layout = QtWidgets.QHBoxLayout(map_agent_frm)
        self.map_agent_outer_horizontal_layout.setSpacing(0)
        self.map_agent_outer_horizontal_layout.setObjectName(u"map_agent_outer_horizontal_layout")
        self.map_agent_outer_horizontal_layout.setContentsMargins(0, 0, 0, 6)

        self.map_agent_inner_frm = QtWidgets.QFrame(map_agent_frm)
        self.map_agent_inner_frm.setObjectName(u"map_agent_inner_frm")
        self.map_agent_inner_frm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.map_agent_inner_frm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.map_agent_inner_frm.setMinimumSize(QtCore.QSize(0, 45))

        self.map_agent_inner_horizontal_layout = QtWidgets.QHBoxLayout(self.map_agent_inner_frm)
        self.map_agent_inner_horizontal_layout.setSpacing(0)
        self.map_agent_inner_horizontal_layout.setObjectName(u"map_agent_inner_horizontal_layout")
        self.map_agent_inner_horizontal_layout.setContentsMargins(0, 0, 0, 0)

        self.map_lbl = QtWidgets.QLabel(self.map_agent_inner_frm)
        self.map_lbl.setObjectName(u"map_lbl")
        self.map_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.map_lbl.setText(map)
        self.map_agent_inner_horizontal_layout.addWidget(self.map_lbl)

        self.agent_lbl = QtWidgets.QLabel(self.map_agent_inner_frm)
        self.agent_lbl.setObjectName(u"agent_lbl")
        self.agent_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.agent_lbl.setText(agent)
        self.map_agent_inner_horizontal_layout.addWidget(self.agent_lbl)

        self.map_agent_outer_horizontal_layout.addWidget(self.map_agent_inner_frm)
