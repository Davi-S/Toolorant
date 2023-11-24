import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

import animations
import game_resources as gr

AGENT_OPTIONS = ['NONE', 'DODGE'] + [agent.name for agent in gr.Agent]

class MapAgentFormQFrame(QtWidgets.QFrame):
    color_animation_duration = 200
    
    def __init__(self, map, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.map = map
        self.setup_ui()
        self.setup_animations()

    def setup_ui(self):
        self.ui = Ui_map_agent_frm()
        self.ui.setupUi(self, self.map)

    def setup_animations(self):
        self.map_lbl_color_animation = animations.StyleSheetAnimation(
            widget=self.ui.mab_form_lbl,
            style_key='color',
            start_value=QtGui.QColor(255, 255, 255, 255),
            end_value=QtGui.QColor(255, 70, 85, 255),
            duration=self.color_animation_duration
        )
        self.agent_lbl_color_animation = animations.StyleSheetAnimation(
            widget=self.ui.agent_form_cb,
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
    def setupUi(self, map_agent_form_frm, map):
        if not map_agent_form_frm.objectName():
            map_agent_form_frm.setObjectName(u"map_agent_form_frm")
        # using inner and outer layouts fo the margin wont push the border
        self.map_agent_form_outer_horizontal_layout = QtWidgets.QHBoxLayout(map_agent_form_frm)
        self.map_agent_form_outer_horizontal_layout.setSpacing(0)
        self.map_agent_form_outer_horizontal_layout.setObjectName(u"map_agent_form_outer_horizontal_layout")
        self.map_agent_form_outer_horizontal_layout.setContentsMargins(0, 0, 0, 6)
        
        self.map_agent_form_inner_frm = QtWidgets.QFrame(map_agent_form_frm)
        self.map_agent_form_inner_frm.setObjectName(u"map_agent_form_inner_frm")
        self.map_agent_form_inner_frm.setMaximumSize(QtCore.QSize(16777215, 45))
        
        self.outer_layout = QtWidgets.QHBoxLayout(self.map_agent_form_inner_frm)
        self.outer_layout.setSpacing(0)
        self.outer_layout.setObjectName(u"outer_layout")
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        
        self.mab_form_lbl = QtWidgets.QLabel(self.map_agent_form_inner_frm)
        self.mab_form_lbl.setObjectName(u"mab_form_lbl")
        self.mab_form_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.mab_form_lbl.setText(map)
        self.outer_layout.addWidget(self.mab_form_lbl)

        self.agent_form_frm = QtWidgets.QFrame(self.map_agent_form_inner_frm)
        self.agent_form_frm.setObjectName(u"agent_form_frm")
        self.agent_form_frm.setMinimumSize(QtCore.QSize(0, 45))
        self.agent_form_frm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.agent_form_frm.setFrameShadow(QtWidgets.QFrame.Raised)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.agent_form_frm)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        # setContentsMargins with magic numbers for balance.
        # these numbers are related to the size of dropdown-arrow
        self.horizontalLayout.setContentsMargins(50, 0, 50-17, 3)
        
        self.agent_form_cb = QtWidgets.QComboBox(self.agent_form_frm)
        self.agent_form_cb.setObjectName(u"agent_form_cb")
        self.agent_form_cb.setFrame(False)
        self.agent_form_cb.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.agent_form_cb.addItems(AGENT_OPTIONS)
        # Remove the ability to choose with mouse wheel
        self.agent_form_cb.wheelEvent = lambda event: ... 
        # center text by making it editable and read only
        self.agent_form_cb.setEditable(True)
        self.agent_form_cb.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.agent_form_cb.lineEdit().setReadOnly(True)
        self.horizontalLayout.addWidget(self.agent_form_cb)

        self.outer_layout.addWidget(self.agent_form_frm)

        self.map_agent_form_outer_horizontal_layout.addWidget(self.map_agent_form_inner_frm)
