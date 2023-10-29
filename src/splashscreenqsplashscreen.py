import PySide6.QtWidgets as QtWidgets


class SplashScreenQSplashScreen(QtWidgets.QSplashScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Center the splash screen counting the task bar
        screen = QtWidgets.QApplication.instance().primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.move(
            (screen_geometry.width() - self.size().width()) // 2,
            (screen_geometry.height() - self.size().height()) // 2,
        )