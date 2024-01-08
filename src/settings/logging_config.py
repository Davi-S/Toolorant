# sourcery skip: move-assign-in-block, use-named-expression
import logging
import logging.config
import os
from pathlib import Path

from color_logging import ColoramaFormatter

# Set and create the logs folder
LOGS_FOLDER = Path(__file__).resolve().parent.parent / '.logs/'
if not LOGS_FOLDER.exists():
    os.makedirs(LOGS_FOLDER)

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
            'class': 'logging.FileHandler',
            'filename': str(LOGS_FOLDER.joinpath("spam.log")),
            'mode': 'a',
            'formatter': 'file',
            'encoding': 'utf-8'
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
