import logging

import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

import animations
import game_resources as gr
import mainwindowqmainwindow
import page_manager
from settings import user_settings

from . import profile as prof
from .instalocker import Instalocker
from .mapagentformqframe import MapAgentFormQFrame
from .mapagentqframe import MapAgentQFrame
from .profileitemqframe import ProfileItemQFrame
from .view.instalocker_pg_ui import Ui_instalocker_pg


logger = logging.getLogger(__name__)

class InstalockerPageQWidget(page_manager.BasePageQWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.setup_animations()
        
        # Setup instalocker
        self.instalocker = Instalocker(
            client=mainwindowqmainwindow.get_main_window().client,
            profile=prof.Profile.load(user_settings.instalocker.profile),
            select_delay=user_settings.instalocker.select_delay,
            lock_delay=user_settings.instalocker.lock_delay
        )
        
        # Create and show initial profiles
        for profile in prof.get_all_profiles():
            self.add_profile_item(profile)

        # Load the profile from the user settings
        # See the "self.set_profile" setter
        self.set_profile = prof.Profile.load(user_settings.instalocker.profile) if user_settings.instalocker.profile is not None else None
        if self.set_profile:
            # simulate a hover and click on the profile that is to be set
            # this is made to apply the proper styles
            for idx in range(self.ui.profile_list_lw.count()):
                item = self.ui.profile_list_lw.item(idx)
                widget = self.ui.profile_list_lw.itemWidget(item)
                if isinstance(widget, ProfileItemQFrame) and widget.name == self.set_profile.name:
                    widget.set_profile_btn_enter_event()
                    widget.set_profile_btn_clicked()
                    
        # Connect signals
        self.ui.menu_btn.clicked.connect(lambda: self.page_manager.switch_to_page('main_menu_pg'))
        self.ui.create_profile_btn.clicked.connect(self.create_profile_btn_clicked)
        self.ui.add_profile_btn.clicked.connect(self.add_profile_btn_clicked)
        self.ui.start_stop_btn.clicked.connect(self.start_stop_btn_clicked)
        self.ui.select_spin.valueChanged.connect(self.select_spin_value_changed)
        self.ui.lock_spin.valueChanged.connect(self.lock_spin_value_changed)
        # Make spin boxes do not respond to mouse wheel
        self.ui.select_spin.wheelEvent = lambda event: None
        self.ui.lock_spin.wheelEvent = lambda event: None


    @property
    def set_profile(self):
        return self._set_profile
    
    @set_profile.setter
    def set_profile(self, profile: prof.Profile | None):
        # Set the profile in all places where it must be
        self._set_profile = profile
        self.instalocker.profile = profile
        user_settings.instalocker.profile = profile.name if profile else None
        user_settings.persist()
        
    @property
    def select_delay(self):
        return self._select_delay
    
    @select_delay.setter
    def select_delay(self, value):
        self._select_delay = value
        self.instalocker.select_delay = value
        user_settings.instalocker.select_delay = value
        user_settings.persist()
        
    @property
    def lock_delay(self):
        return self._lock_delay
    
    @lock_delay.setter
    def lock_delay(self, value):
        self._lock_delay = value
        self.instalocker.lock_delay = value
        user_settings.instalocker.lock_delay = value
        user_settings.persist()
    
    def setup_ui(self):
        self.ui = Ui_instalocker_pg()
        self.ui.setupUi(self)
        self.ui.select_spin.setValue(user_settings.instalocker.select_delay)
        self.ui.lock_spin.setValue(user_settings.instalocker.lock_delay)
        # The "add profile frame" starts hidden and will be visible when creating a new profile
        self.ui.add_profile_frm.hide()

    def setup_animations(self):
        self.add_profile_btn_icon_animation = animations.ScaleIconAnimation(
            widget=self.ui.add_profile_btn,
            scale_factor=0.950,
            duration=1
        )
        self.ui.add_profile_btn.enterEvent = lambda event: self.add_profile_btn_icon_animation.start_animation()
        self.ui.add_profile_btn.leaveEvent = lambda event: self.add_profile_btn_icon_animation.start_animation(reversed=True)

    def on_page_enter(self):
        super().on_page_enter()
        # Change the client of the instalocker if its region is different from the actual main window client region
        # This is usually only needed on the first run of the application
        if self.instalocker.client.region != mainwindowqmainwindow.get_main_window().client.region:
            self.instalocker.client = mainwindowqmainwindow.get_main_window().client
    
    def add_profile_item(self, profile: prof.Profile, last_item: bool=False):
        logger.debug(f'Adding profile item "{profile.name}"')
        # Create the profile item
        profile_item = ProfileItemQFrame(profile.name)
        # Connect signals
        profile_item.delete_button_clicked.connect(lambda profile=profile: self.profile_item_delete_button_clicked(profile))
        profile_item.set_button_clicked.connect(lambda profile=profile: self.profile_item_set_profile_button_clicked(profile))
        if last_item:
            # Remove the bottom margin if it is the last item
            profile_item.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        # Add the profile item to the list widget
        list_item = QtWidgets.QListWidgetItem(self.ui.profile_list_lw)
        list_item.setSizeHint(profile_item.sizeHint())
        self.ui.profile_list_lw.setItemWidget(list_item, profile_item)
    
    def remove_profile_item(self, profile: ProfileItemQFrame | prof.Profile):
        logger.debug(f'Removing profile item "{profile.name}"')
        removed = False
        for idx in range(self.ui.profile_list_lw.count()):
            item = self.ui.profile_list_lw.item(idx)
            widget = self.ui.profile_list_lw.itemWidget(item)
            if widget is profile or (isinstance(widget, ProfileItemQFrame) and widget.name == profile.name):
                self.ui.profile_list_lw.takeItem(idx)
                removed = True
        return removed
    
    def profile_item_delete_button_clicked(self, profile: prof.Profile):
        logger.info(f'Delete button clicked for profile "{profile.name}"')
        self.remove_profile_item(profile)
        # Check if the deleted profile was set and remove its references
        if self.set_profile and (self.set_profile.name == profile.name):
            self.set_profile = None
        profile.delete()

    def profile_item_set_profile_button_clicked(self, profile: prof.Profile):
        logger.info(f'Set button clicked for profile "{profile.name}"')
        self.set_profile = profile
        self.ui.profile_info_lw.clear()
        self.show_profile_info(self.set_profile)

    def show_profile_info(self, profile: prof.Profile):
        for map, agent in profile.map_agent.items():
            map_agent = MapAgentQFrame(map.name, agent.name if agent is not None else 'NONE')
            list_item = QtWidgets.QListWidgetItem(self.ui.profile_info_lw)
            list_item.setSizeHint(map_agent.sizeHint())
            self.ui.profile_info_lw.setItemWidget(list_item, map_agent)
        # Remove the bottom margin from the last item
        map_agent.ui.map_agent_outer_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        list_item.setSizeHint(map_agent.sizeHint())

    def create_profile_btn_clicked(self):
        logger.info('Create profile button clicked')
        logger.debug(f'{self.ui.create_profile_btn.is_checked=}')
        self.ui.new_profile_name_ledt.setText('')
        if self.ui.create_profile_btn.is_checked:
            self.toggle_profiles_items_buttons(False)
            self.ui.add_profile_frm.show()
            self.ui.profile_info_lw.clear()
            self.show_map_agent_form_items()
        else:
            self.toggle_profiles_items_buttons(True)
            self.ui.add_profile_frm.hide()
            self.ui.profile_info_lw.clear()
            if self.set_profile:
                self.show_profile_info(self.set_profile)

    def toggle_profiles_items_buttons(self, value: bool):
        for idx in range(self.ui.profile_list_lw.count()):
            item = self.ui.profile_list_lw.item(idx)
            widget = self.ui.profile_list_lw.itemWidget(item)
            if isinstance(widget, ProfileItemQFrame):
                widget.toggle_buttons(value)

    def show_map_agent_form_items(self):
        # TODO: This function is taking too long to run. need to improve the map-agent-form items creation
        # Create map-agent-form items
        map_agent_form_items = []
        for map in gr.Map:
            map_agent = MapAgentFormQFrame(map.name)
            map_agent_form_items.append(map_agent)
        # Remove the bottom margin from the last item
        map_agent.ui.map_agent_form_outer_horizontal_layout.setContentsMargins(0, 0, 0, 0)

        # Add the map-agent-form items to the list widget
        for map_agent in map_agent_form_items:
            list_item = QtWidgets.QListWidgetItem(self.ui.profile_info_lw)
            list_item.setSizeHint(map_agent.sizeHint())
            self.ui.profile_info_lw.setItemWidget(list_item, map_agent)

    def add_profile_btn_clicked(self):  # sourcery skip: avoid-builtin-shadow
        logger.info('Add profile button clicked')
        # Get profile name and game map
        profile_name = self.ui.new_profile_name_ledt.text()
        if not profile_name:
            self.ui.new_profile_name_ledt.setPlaceholderText('Please enter a name')
            return
        logger.debug(f'{profile_name=}')
        profile_map_agent = {}
        for idx in range(self.ui.profile_info_lw.count()):
            item = self.ui.profile_info_lw.item(idx)
            widget = self.ui.profile_info_lw.itemWidget(item)
            if isinstance(widget, MapAgentFormQFrame):
                map = gr.Map[widget.ui.mab_form_lbl.text()]
                agent = gr.Agent[widget.ui.agent_form_cb.currentText()] if widget.ui.agent_form_cb.currentText() != "NONE" else None
                profile_map_agent[map] = agent
        logger.debug(f'{profile_map_agent=}')
        
        # Create and show the new profile
        profile = prof.Profile(profile_name, profile_map_agent)
        profile.save()
        # Delete item if it has the same name and add new one (this is basically an edit).
        # If the new profile does not has the same name it will not be deleted (because it does not exist)
        self.remove_profile_item(profile)
        self.add_profile_item(profile)
        
        # Simulate a click on the create profile button to close profile creation
        # Need to change the "is_checked" manually because it is toggled on mouse release and the "click" event does not trigger it
        self.ui.create_profile_btn.is_checked = False
        self.ui.create_profile_btn.click()
        self.ui.create_profile_btn.leaveEvent(None)
        logger.info(f'Profile "{profile.name}" created successfully')
        
    def start_stop_btn_clicked(self):
        if self.ui.start_stop_btn.is_checked:
            mainwindowqmainwindow.get_main_window().websocket.add_listener(self.instalocker)
            logger.info('Instalocker started successfully')
        else:
            mainwindowqmainwindow.get_main_window().websocket.remove_listener(self.instalocker)
            logger.info('Instalocker stopped successfully')
    
    def select_spin_value_changed(self, value):
        logger.info(f'Select delay changed to {value}')
        self.select_delay = value
        
    def lock_spin_value_changed(self, value):
        logger.info(f'Lock delay changed to {value}')
        self.lock_delay = value
        