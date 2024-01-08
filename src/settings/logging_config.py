# sourcery skip: move-assign-in-block, use-named-expression
import datetime
import logging
import logging.config
import logging.handlers
import os
from pathlib import Path

from color_logging import ColoramaFormatter

# Set and create the logs folder
LOGS_FOLDER = Path(__file__).resolve().parent.parent / '.logs/'
if not LOGS_FOLDER.exists():
    os.makedirs(LOGS_FOLDER)


def rollover_all_rotating_handlers():
    handlers = logging.getLogger().handlers
    for handler in handlers:
        if isinstance(handler, logging.handlers.RotatingFileHandler) and Path(handler.baseFilename).is_file():
            handler.doRollover()


class CustomRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, filename: str, mode: str = "a", maxBytes: int = 0, backupCount: int = 0, encoding: str | None = None, delay: bool = False, errors: str | None = None) -> None:
        super().__init__(self.get_new_filename(Path(filename)), mode, maxBytes, backupCount, encoding, delay, errors)

    @staticmethod
    def get_new_filename(filename: Path):
        now = datetime.datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H-%M-%S")      
        new_full_path = filename.with_name(f'{dt_string} {filename.name}')
        return str(new_full_path)


# Base dict config
dict_config = {
    'version': 1,
    'formatters': {
        'colorama': {
            '()': ColoramaFormatter,
            'fmt': '{levelname:<8} {FORE_LIGHTBLACK_EX}:{STYLE_RESET_ALL} {name} {FORE_LIGHTBLACK_EX}:{STYLE_RESET_ALL} {funcName} {FORE_LIGHTBLACK_EX}:{STYLE_RESET_ALL} {message}',
            'style': '{',
            'color_config': {
                logging.DEBUG: {
                    'name': 'STYLE_DIM',
                    'funcName': 'STYLE_DIM'
                },
                logging.INFO: {
                    'levelname': 'FORE_CYAN',
                    'name': 'FORE_CYAN,STYLE_DIM',
                    'funcName': 'FORE_CYAN,STYLE_DIM'
                },
                logging.WARNING: {
                    'levelname': 'FORE_YELLOW',
                    'name': 'FORE_YELLOW,STYLE_DIM',
                    'funcName': 'FORE_YELLOW,STYLE_DIM'
                },
                logging.ERROR: {
                    'levelname': 'FORE_RED',
                    'name': 'FORE_RED,STYLE_DIM',
                    'funcName': 'FORE_RED,STYLE_DIM'
                },
                logging.CRITICAL: {
                    'levelname': 'BACK_RED,STYLE_BRIGHT',
                    'name': 'BACK_RED,STYLE_DIM,STYLE_BRIGHT',
                    'funcName': 'BACK_RED,STYLE_DIM,STYLE_BRIGHT'
                }
            }
        },
        'file': {
            'format': '[{asctime}] {levelname:<8} : {name} : {funcName} : {message}',
            'style': '{'
        }
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'colorama',
        },
        'spam': {
            'class': f'{__name__}.CustomRotatingFileHandler',  # Defined in the same file
            'filename': str(LOGS_FOLDER.joinpath("spam.log")),
            'encoding': 'utf-8',
            'delay': True,
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['spam', 'stream']
    },
    'loggers': {
        'urllib3.connectionpool': {
            'handlers': [],
            'level': 'INFO'
        },
        'websockets.client': {
            'handlers': [],
            'level': 'INFO'
        },
        'asyncio': {
            'handlers': [],
            'level': 'INFO'
        }
    }
}
