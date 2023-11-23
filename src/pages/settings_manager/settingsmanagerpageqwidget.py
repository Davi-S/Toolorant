import logging

import PySide6.QtWidgets as QtWidgets

import animations
import mainwindowqmainwindow
import page_manager

from . import s_profile as s_prof
from .sprofileitemqframe import SProfileItemQFrame
from .view.settings_manager_pg_ui import Ui_settings_manager_pg

logger = logging.getLogger(__name__)


class SettingsManagerPageQWidget(page_manager.BasePageQWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.setup_animations()

        # Show saved profiles
        for profile in s_prof.get_all_s_profiles_name():
            self.add_profile_item(profile)

        # Connect signals
        self.ui.menu_btn.clicked.connect(lambda: self.page_manager.switch_to_page('main_menu_pg'))
        self.ui.create_s_profile_btn.clicked.connect(self.create_profile_btn_clicked)
        self.ui.add_s_profile_btn.clicked.connect(self.add_profile_btn_clicked)

    def setup_ui(self):
        self.ui = Ui_settings_manager_pg()
        self.ui.setupUi(self)
        # The "add profile frame" starts hidden and will be visible when creating a new profile
        self.ui.add_s_profile_frm.hide()

    def setup_animations(self):
        self.add_profile_btn_icon_animation = animations.ScaleIconAnimation(
            widget=self.ui.add_s_profile_btn,
            scale_factor=0.950,
            duration=1
        )
        self.ui.add_s_profile_btn.enterEvent = lambda event: self.add_profile_btn_icon_animation.start_animation()
        self.ui.add_s_profile_btn.leaveEvent = lambda event: self.add_profile_btn_icon_animation.start_animation(reversed=True)

    def add_profile_item(self, profile_name: str, last_item: bool = False):
        logger.debug(f'Adding profile item "{profile_name}"')
        # Create the profile item
        profile_item = SProfileItemQFrame(profile_name)
        # Connect signals
        profile_item.delete_button_clicked.connect(lambda profile=profile_name: self.s_profile_item_delete_button_clicked(profile))
        profile_item.send_button_clicked.connect(lambda profile=profile_name: self.s_profile_item_send_button_clicked(profile))
        if last_item:
            # Remove the bottom margin if it is the last item
            profile_item.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        # Add the profile item to the list widget
        list_item = QtWidgets.QListWidgetItem(self.ui.s_profile_list_lw)
        list_item.setSizeHint(profile_item.sizeHint())
        self.ui.s_profile_list_lw.setItemWidget(list_item, profile_item)

    def remove_profile_item(self, profile: SProfileItemQFrame | str) -> bool:
        profile_name = profile if isinstance(profile, str) else profile.name
        logger.debug(f'Removing profile item "{profile_name}"')
        removed = False
        for idx in range(self.ui.s_profile_list_lw.count()):
            item = self.ui.s_profile_list_lw.item(idx)
            widget = self.ui.s_profile_list_lw.itemWidget(item)
            if widget is profile or (isinstance(widget, SProfileItemQFrame) and widget.name == profile_name):
                self.ui.s_profile_list_lw.takeItem(idx)
                removed = True
        return removed

    def s_profile_item_delete_button_clicked(self, profile_name: str):
        logger.info(f'Delete button clicked for profile "{profile_name}"')
        self.remove_profile_item(profile_name)
        s_prof.delete(profile_name)

    def s_profile_item_send_button_clicked(self, profile_name: str):
        logger.info(f'Set button clicked for profile "{profile_name}"')
        local_settings = s_prof.load(profile_name)
        mainwindowqmainwindow.get_main_window().client.put_player_settings(local_settings)

    def create_profile_btn_clicked(self):
        logger.info('Create profile button clicked')
        logger.debug(f'{self.ui.create_s_profile_btn.is_checked=}')
        self.ui.new_s_profile_name_ledt.setText('')
        if self.ui.create_s_profile_btn.is_checked:
            self.toggle_profiles_items_buttons(False)
            self.ui.add_s_profile_frm.show()
        else:
            self.toggle_profiles_items_buttons(True)
            self.ui.add_s_profile_frm.hide()

    def toggle_profiles_items_buttons(self, value: bool):
        for idx in range(self.ui.s_profile_list_lw.count()):
            item = self.ui.s_profile_list_lw.item(idx)
            widget = self.ui.s_profile_list_lw.itemWidget(item)
            if isinstance(widget, SProfileItemQFrame):
                widget.toggle_buttons(value)

    def add_profile_btn_clicked(self):
        logger.info('Add profile button clicked')
        # Get profile name
        s_profile_name = self.ui.new_s_profile_name_ledt.text()
        if not s_profile_name:
            self.ui.new_s_profile_name_ledt.setPlaceholderText('Please enter a name')
            return
        logger.debug(f'{s_profile_name=}')
        
        game_settings = mainwindowqmainwindow.get_main_window().client.rnet_fetch_settings()
        
        # Save the new profile
        s_prof.save(s_profile_name, game_settings)
        
        # Delete item if it has the same name and add new one (this is basically an edit).
        # If the new profile does not has the same name it will not be deleted (because it does not exist)
        self.remove_profile_item(s_profile_name)
        self.add_profile_item(s_profile_name)

        # Simulate a click on the create profile button to close profile creation
        # Need to change the "is_checked" manually because it is toggled on mouse release and the "click" event does not trigger it
        self.ui.create_s_profile_btn.is_checked = False
        self.ui.create_s_profile_btn.click()
        self.ui.create_s_profile_btn.leaveEvent(None)
        logger.info(f'Profile "{s_profile_name}" created successfully')
