import logging

CONFIG_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': { 
        'default': { 
            'format': '%(levelname)s:%(name)s:%(message)s'
        },
        'simple': {
            'format': '%(filename)s : %(levelname)s : %(message)s'
        },
        'simple_precise': {
            'format': '%(asctime)s : %(funcName)s : %(levelname)s : %(message)s'
        },
        'precise': {
            'format': '%(asctime)s : %(filename)s : %(funcName)s : %(levelname)s : %(message)s'
        },
        'full_precise': {
            'format': '%(asctime)s : %(filename)s : %(funcName)s :  %(name)s : %(levelname)s : %(message)s'
        }
    },

    'handlers': { 
        'to_console': { 
            'class': 'logging.StreamHandler',
            'formatter': 'precise',
            'level': 'WARNING'
        },
        'to_console_spam': { 
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'to_file_spam': { 
            'class': 'logging.FileHandler',
            'filename': 'logs\\spam.log',
            'formatter': 'precise'
        }
    },
    'loggers': {},
    
    'root': {
        'level': 'DEBUG',
        'handlers': ['to_file_spam', 'to_console']
    }
}


def create_file_handler(filename, mode='a', encoding=None, delay=False, errors=None,
                        formatter_str=CONFIG_DICT['formatters']['simple_precise']['format'],
                        level='WARNING'):
    filename = f'logs\\{filename}.log'
    file_handler = logging.FileHandler(filename, mode, encoding, delay, errors)
    formatter = logging.Formatter(formatter_str)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(eval(f'logging.{level}'))
    return file_handler