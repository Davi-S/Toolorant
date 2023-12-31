from __future__ import annotations

import logging

import PySide6.QtCore as QtCore
import PySide6.QtWidgets as QtWidgets

logger = logging.getLogger(__name__)


class BasePageQWidget(QtWidgets.QWidget):
    fade_animation_duration = 250

    def __init__(self, page_manager: PageManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_manager = page_manager
        self._setup_opacity_animation()

    def on_page_enter(self, *args, **kwargs):
        self._run_blocking_animation(self.fade_in_animation)

    def on_page_leave(self):
        self._run_blocking_animation(self.fade_out_animation)

    def _setup_opacity_animation(self):
        self.graphics_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.graphics_effect)
        self.graphics_effect.setOpacity(1)
        self.fade_in_animation = self._create_opacity_animation(0, 1)
        self.fade_out_animation = self._create_opacity_animation(1, 0)

    def _create_opacity_animation(self, start_value, end_value):
        animation = QtCore.QPropertyAnimation(self.graphics_effect, b"opacity")
        animation.setDuration(self.fade_animation_duration)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        return animation

    def _run_blocking_animation(self, animation):
        # Block the animation call so the enter/leave animations don't overlap each other
        # TODO: this is raising errors:
        #     QBasicTimer::stop: Failed. Possibly trying to stop from a different thread
        #     QObject::killTimer: Timers cannot be stopped from another thread
        loop = QtCore.QEventLoop()
        animation.finished.connect(loop.quit)
        animation.start()
        loop.exec_()


class PageManager:
    def __init__(self, stacked_widget: QtWidgets.QStackedWidget):
        self.stacked_widget = stacked_widget
        self.pages: list[set[int, str]] = []
        self.previous_page = None

    def add_page(self, page_widget: BasePageQWidget, page_name: str):
        # The first added page will not receive the page enter event
        if self.page_exists(page_name):
            logger.info(f'A page with the name "{page_name}" already exists.')
            return False
        page = page_widget(self)
        index = self.stacked_widget.addWidget(page)
        self.pages.append((index, page_name))
        logger.info(f'Added page "{page_name}" ({page_widget.__name__})')
        return True
    
    def remove_page(self, _page: str | int):
        if type(_page) == str:
            for page in self.pages:
                if page[1] == _page:
                    idx = page[0]
                    self.pages.remove(page)
                    break
        else:
            idx = _page
        widget = self.stacked_widget.widget(idx)
        self.stacked_widget.removeWidget(widget)
        widget.deleteLater()
        logger.info(f'Page "{_page}" deleted')
    
    def clear(self):
        count = 0
        for _ in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()
            count += 1
        self.pages.clear()
        if count > 0:
            logger.info(f'All pages deleted. Total of {count} pages')
        else:
            logger.info('No pages were deleted')

    def switch_to_page(self, page_name: str, *args, **kwargs):
        for page in self.pages:
            if page_name == page[1]:
                logger.debug(f'Switching from page "{self.pages[self.stacked_widget.currentIndex()][1]}" to page "{page_name}"')
                self.previous_page = self.pages[self.stacked_widget.currentIndex()]
                self.page_leave(self.stacked_widget.currentIndex())
                self.stacked_widget.setCurrentIndex(page[0])
                self.page_enter(page[0], *args, **kwargs)

    def page_enter(self, page_idx: int, *args, **kwargs):
        page: BasePageQWidget = self.stacked_widget.widget(page_idx)
        page.on_page_enter(*args, **kwargs)

    def page_leave(self, page_idx: int):
        page: BasePageQWidget = self.stacked_widget.widget(page_idx)
        page.on_page_leave()

    def page_exists(self, page_name):
        return any(page_name == name for _, name in self.pages)
