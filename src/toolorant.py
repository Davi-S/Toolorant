def main():
    print(f'===== Called "{__file__}" file =====')
    print('===== Starting slash screen =====')
    # SPLASH SCREEN
    import PySide6.QtWidgets as QtWidgets
    from splashscreenqsplashscreen import SplashScreenQSplashScreen
    app = QtWidgets.QApplication()
    splash = SplashScreenQSplashScreen()
    splash.show()

    print('===== Starting logging configuration =====')
    # SETUP LOGGING
    import logging
    import logging.config
    from settings.logging_config import dict_config
    logging.config.dictConfig(dict_config)
    print('===== Finished logging configuration =====')

    print('===== Starting imports =====')
    # IMPORTS
    import sys
    from mainwindowqmainwindow import MainWindowQMainWindow
    print('===== Finished imports =====')

    print('===== Starting main code =====')
    main_window = MainWindowQMainWindow()
    main_window.show()
    splash.finish(main_window)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
